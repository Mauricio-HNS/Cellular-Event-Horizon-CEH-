"""Hierarchical uncertainty for trajectory-correlated prospective benchmarks."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .benchmark import score_at_cutoff
from .metrics import auprc, auroc

@dataclass(frozen=True)
class HierarchicalResult:
    method: str
    trajectory_auroc: float
    trajectory_auprc: float
    bootstrap_auroc_low: float
    bootstrap_auroc_high: float
    bootstrap_auprc_low: float
    bootstrap_auprc_high: float
    trajectories: int
    positive_trajectories: int
    negative_trajectories: int

def trajectory_level_scores(states, transition_time, horizon, method, window=5):
    """Reduce each trajectory to one prospective score and one event label."""
    start=max(window+2,1)
    stop=min(len(states)-1,transition_time+horizon)
    scores=[]
    labels=[]
    for cutoff in range(start,stop+1):
        value=score_at_cutoff(states,cutoff,method,window)
        if np.isfinite(value):
            scores.append(float(value))
            labels.append(int(0 < transition_time-cutoff <= horizon))
    if not scores or not any(labels) or all(labels):
        return float("nan"), float("nan")
    # Event-level reduction: maximum score before the known transition,
    # compared with the maximum score outside the event window.
    y=np.asarray(labels,dtype=int); s=np.asarray(scores,float)
    event=s[y==1]
    control=s[y==0]
    return float(np.max(event)), float(np.max(control))

def hierarchical_evaluate(trajectories, transition_times, horizon=30,
                          methods=("snapshot","temporal","early_warning","ceh"),
                          n_boot=2000, seed=7):
    trajectories=list(trajectories); transition_times=list(transition_times)
    if len(trajectories)!=len(transition_times): raise ValueError("trajectory/transition lengths differ")
    if len(trajectories)<4: raise ValueError("at least four trajectories are required")
    rng=np.random.default_rng(seed)
    results=[]
    for method in methods:
        event=[]; control=[]
        for x,t0 in zip(trajectories,transition_times):
            e,c=trajectory_level_scores(x,t0,horizon,method)
            if np.isfinite(e) and np.isfinite(c):
                event.append(e); control.append(c)
        event=np.asarray(event); control=np.asarray(control)
        if len(event)<2: continue
        # Pairing is retained inside each trajectory; uncertainty resamples trajectories.
        observed=float(np.mean(event[:,None]>control[None,:])+
                       .5*np.mean(event[:,None]==control[None,:]))
        ap_scores=np.concatenate([event,control])
        ap_labels=np.r_[np.ones(len(event),dtype=int),np.zeros(len(control),dtype=int)]
        observed_ap=float(auprc(ap_scores,ap_labels))
        auc_boot=[]; ap_boot=[]
        for _ in range(n_boot):
            idx=rng.integers(0,len(event),len(event))
            eb=event[idx]; cb=control[idx]
            auc_boot.append(float(np.mean(eb[:,None]>cb[None,:])+
                                  .5*np.mean(eb[:,None]==cb[None,:])))
            ss=np.concatenate([eb,cb]); yy=np.r_[np.ones(len(eb),dtype=int),np.zeros(len(cb),dtype=int)]
            ap_boot.append(float(auprc(ss,yy)))
        results.append(HierarchicalResult(method,observed,observed_ap,
            *map(float,np.quantile(auc_boot,[.025,.975])),
            *map(float,np.quantile(ap_boot,[.025,.975])),
            len(event),len(event),len(control)))
    return results
