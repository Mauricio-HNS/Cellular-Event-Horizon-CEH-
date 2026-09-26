"""Dependency-light ranking and detection metrics for prospective benchmarks."""
from __future__ import annotations
import numpy as np

def _validate(scores, labels):
    s=np.asarray(scores,dtype=float); y=np.asarray(labels,dtype=int)
    if s.ndim!=1 or y.ndim!=1 or len(s)!=len(y) or len(s)<2: raise ValueError("scores and labels must be equal 1D arrays")
    if not np.all(np.isfinite(s)): raise ValueError("scores must be finite")
    if not np.all((y==0)|(y==1)): raise ValueError("labels must be binary")
    return s,y

def auroc(scores, labels):
    s,y=_validate(scores,labels); pos=s[y==1]; neg=s[y==0]
    if len(pos)==0 or len(neg)==0: return float("nan")
    return float(np.mean(pos[:,None]>neg[None,:]) + 0.5*np.mean(pos[:,None]==neg[None,:]))

def auprc(scores, labels):
    s,y=_validate(scores,labels); order=np.argsort(-s,kind="mergesort"); yy=y[order]
    positives=int(np.sum(yy))
    if positives==0: return float("nan")
    tp=np.cumsum(yy); fp=np.cumsum(1-yy)
    precision=tp/np.maximum(tp+fp,1); recall=tp/positives
    return float(np.sum((recall-np.concatenate(([0.0],recall[:-1])))*precision))

def detection_rate(scores, labels, threshold):
    s,y=_validate(scores,labels); p=s[y==1]
    return float(np.mean(p>=threshold)) if len(p) else float("nan")

def false_positive_rate(scores, labels, threshold):
    s,y=_validate(scores,labels); n=s[y==0]
    return float(np.mean(n>=threshold)) if len(n) else float("nan")
