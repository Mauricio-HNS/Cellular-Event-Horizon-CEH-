"""Incremental-information benchmark for prospective transition signals.

The key question is whether the candidate CEH score adds information beyond
snapshot, temporal-history, and early-warning signals under the same cutoff.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .benchmark import score_at_cutoff

@dataclass(frozen=True)
class IncrementalRow:
    method: str
    base: str
    delta_auroc: float
    delta_auprc: float
    n_test: int
    positives: int

def _rank_auc(scores, labels):
    s=np.asarray(scores,float); y=np.asarray(labels,int)
    pos=s[y==1]; neg=s[y==0]
    if len(pos)==0 or len(neg)==0: return float("nan")
    return float(np.mean(pos[:,None]>neg[None,:])+.5*np.mean(pos[:,None]==neg[None,:]))

def _ap(scores, labels):
    s=np.asarray(scores,float); y=np.asarray(labels,int)
    p=int(y.sum())
    if p==0: return float("nan")
    order=np.argsort(-s,kind="mergesort"); yy=y[order]
    tp=np.cumsum(yy); fp=np.cumsum(1-yy)
    precision=tp/np.maximum(tp+fp,1); recall=tp/p
    return float(np.sum(np.diff(np.r_[0.,recall])*precision))

def _z(x):
    x=np.asarray(x,float)
    return (x-np.mean(x))/max(float(np.std(x)),1e-12)

def _residual_target(candidate, base_features):
    """Remove linear information explained by the baseline features."""
    X=np.column_stack([np.ones(len(candidate)), *[_z(v) for v in base_features]])
    y=_z(candidate)
    beta=np.linalg.lstsq(X,y,rcond=None)[0]
    return y-X@beta

def incremental_evaluate(trajectories, transition_times, horizon=30, methods=("snapshot","temporal","early_warning","ceh"), train_fraction=.6, window=5):
    trajectories=list(trajectories); transition_times=list(transition_times)
    if len(trajectories)!=len(transition_times): raise ValueError("trajectory/transition lengths differ")
    if len(trajectories)<4: raise ValueError("at least four trajectories are required")
    split=max(2,int(len(trajectories)*train_fraction))
    split=min(split,len(trajectories)-2)
    rows=[]
    for candidate in methods:
        if candidate in ("snapshot",):
            continue
        for base_name in ("snapshot","temporal","early_warning"):
            train_c=[]; train_b=[]; train_y=[]; test_c=[]; test_b=[]; test_y=[]
            for idx,(states,t0) in enumerate(zip(trajectories,transition_times)):
                cs=[]; bs=[]; ys=[]
                for cutoff in range(max(window+2,1),min(len(states)-1,t0+horizon)+1):
                    c=score_at_cutoff(states,cutoff,candidate,window)
                    if not np.isfinite(c): continue
                    b=score_at_cutoff(states,cutoff,base_name,window)
                    if not np.isfinite(b): continue
                    cs.append(c); bs.append(b); ys.append(int(0<t0-cutoff<=horizon))
                if idx<split: train_c.extend(cs); train_b.extend(bs); train_y.extend(ys)
                else: test_c.extend(cs); test_b.extend(bs); test_y.extend(ys)
            if not test_c or len(set(test_y))<2: continue
            # Residualize candidate against the baseline using training data only.
            tc=np.asarray(train_c); tb=np.asarray(train_b)
            X=np.column_stack([np.ones(len(tc)),_z(tb)])
            beta=np.linalg.lstsq(X,_z(tc),rcond=None)[0]
            test_res=_z(np.asarray(test_c))-np.column_stack([np.ones(len(test_c)),_z(np.asarray(test_b))])@beta
            test_candidate=np.asarray(test_c)
            y=np.asarray(test_y)
            rows.append(IncrementalRow(candidate,base_name,
                _rank_auc(test_res,y)-_rank_auc(np.asarray(test_b),y),
                _ap(test_res,y)-_ap(np.asarray(test_b),y),
                len(y),int(y.sum())))
    return rows
