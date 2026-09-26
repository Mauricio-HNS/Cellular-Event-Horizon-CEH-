"""Trajectory-level evaluation with held-out calibration and bootstrap uncertainty."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .benchmark import score_at_cutoff
from .metrics import auprc, auroc, false_positive_rate

@dataclass(frozen=True)
class HeldOutResult:
    method: str
    train_trajectories: int
    test_trajectories: int
    auroc: float
    auprc: float
    false_positive_rate: float
    threshold: float
    positives: int
    negatives: int
    bootstrap_auroc_low: float
    bootstrap_auroc_high: float

def trajectory_scores(states, transition_time, horizon, method, window=5):
    scores, labels = [], []
    start=max(window+2,1)
    stop=min(len(states)-1, transition_time+horizon)
    for cutoff in range(start,stop+1):
        score=score_at_cutoff(states,cutoff,method,window)
        if np.isfinite(score):
            scores.append(float(score))
            labels.append(int(0 < transition_time-cutoff <= horizon))
    return np.asarray(scores), np.asarray(labels,dtype=int)

def _bootstrap_auc(scores, labels, seed=7, n_boot=1000):
    rng=np.random.default_rng(seed)
    scores=np.asarray(scores); labels=np.asarray(labels)
    if len(scores)<2 or len(np.unique(labels))<2:
        return float("nan"),float("nan")
    values=[]
    for _ in range(n_boot):
        idx=rng.integers(0,len(scores),len(scores))
        s,y=scores[idx],labels[idx]
        if len(np.unique(y))==2:
            values.append(auroc(s,y))
    if not values:
        return float("nan"),float("nan")
    return tuple(np.quantile(values,[0.025,0.975]))

def held_out_evaluate(trajectories, transition_times, horizon=30, methods=("snapshot","temporal","early_warning","ceh"), train_fraction=0.5, quantile=0.95, seed=7):
    trajectories=list(trajectories); transition_times=list(transition_times)
    if len(trajectories)!=len(transition_times): raise ValueError("trajectory/transition lengths differ")
    if not 0.0 < train_fraction < 1.0: raise ValueError("train_fraction must be between 0 and 1")
    split=max(1,int(len(trajectories)*train_fraction))
    if split>=len(trajectories): split=len(trajectories)-1
    results=[]
    for method in methods:
        train_s=[]; train_y=[]
        for x,t0 in zip(trajectories[:split],transition_times[:split]):
            s,y=trajectory_scores(x,t0,horizon,method)
            train_s.append(s); train_y.append(y)
        train_s=np.concatenate(train_s); train_y=np.concatenate(train_y)
        threshold=float(np.quantile(train_s[train_y==0],quantile)) if np.any(train_y==0) else float("inf")
        test_s=[]; test_y=[]
        for x,t0 in zip(trajectories[split:],transition_times[split:]):
            s,y=trajectory_scores(x,t0,horizon,method)
            test_s.append(s); test_y.append(y)
        test_s=np.concatenate(test_s); test_y=np.concatenate(test_y)
        low,high=_bootstrap_auc(test_s,test_y,seed=seed)
        results.append(HeldOutResult(
            method,split,len(trajectories)-split,float(auroc(test_s,test_y)),
            float(auprc(test_s,test_y)),float(false_positive_rate(test_s,test_y,threshold)),
            threshold,int(test_y.sum()),int((test_y==0).sum()),float(low),float(high)
        ))
    return results
