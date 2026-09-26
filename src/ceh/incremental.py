"""Incremental-information benchmark with train-fitted normalization."""
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

def _fit_z(x):
    x=np.asarray(x,float)
    return float(np.mean(x)), max(float(np.std(x)),1e-12)

def _apply_z(x, mean, std):
    return (np.asarray(x,float)-mean)/std

def incremental_evaluate(trajectories, transition_times, horizon=30,
                         methods=("snapshot","temporal","early_warning","ceh"),
                         train_fraction=.6, window=5):
    trajectories=list(trajectories); transition_times=list(transition_times)
    if len(trajectories)!=len(transition_times): raise ValueError("trajectory/transition lengths differ")
    if len(trajectories)<4: raise ValueError("at least four trajectories are required")
    split=max(2,int(len(trajectories)*train_fraction)); split=min(split,len(trajectories)-2)
    rows=[]
    for candidate in methods:
        if candidate=="snapshot": continue
        for base_name in ("snapshot","temporal","early_warning"):
            train_c=[]; train_b=[]; train_y=[]; test_c=[]; test_b=[]; test_y=[]
            for idx,(states,t0) in enumerate(zip(trajectories,transition_times)):
                cs=[]; bs=[]; ys=[]
                for cutoff in range(max(window+2,1),min(len(states)-1,t0+horizon)+1):
                    c=score_at_cutoff(states,cutoff,candidate,window)
                    b=score_at_cutoff(states,cutoff,base_name,window)
                    if np.isfinite(c) and np.isfinite(b):
                        cs.append(c); bs.append(b); ys.append(int(0<t0-cutoff<=horizon))
                if idx<split:
                    train_c.extend(cs); train_b.extend(bs); train_y.extend(ys)
                else:
                    test_c.extend(cs); test_b.extend(bs); test_y.extend(ys)
            if not test_c or len(set(test_y))<2 or len(set(train_y))<2: continue
            cm,csd=_fit_z(train_c); bm,bsd=_fit_z(train_b)
            zc_train=_apply_z(train_c,cm,csd); zb_train=_apply_z(train_b,bm,bsd)
            beta=np.linalg.lstsq(np.column_stack([np.ones(len(zb_train)),zb_train]),zc_train,rcond=None)[0]
            zc_test=_apply_z(test_c,cm,csd); zb_test=_apply_z(test_b,bm,bsd)
            residual=zc_test-np.column_stack([np.ones(len(zb_test)),zb_test])@beta
            y=np.asarray(test_y)
            rows.append(IncrementalRow(candidate,base_name,
                _rank_auc(residual,y)-_rank_auc(zb_test,y),
                _ap(residual,y)-_ap(zb_test,y),len(y),int(y.sum())))
    return rows
