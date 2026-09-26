"""Leakage-safe benchmark protocol for prospective transition signals."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .baselines import snapshot_signal, temporal_signal, ceh_signal
from .early_warning import rolling_variance, rolling_autocorrelation
from .metrics import auroc, auprc

@dataclass(frozen=True)
class BenchmarkRow:
    method: str
    auroc: float
    auprc: float
    n: int
    positives: int

def _ew_signal(states, cutoff, window):
    x=np.asarray(states,dtype=float)[:cutoff+1]
    scalar=np.linalg.norm(x,axis=1)
    if len(scalar)<window: return float("nan")
    v=rolling_variance(scalar,window)
    a=rolling_autocorrelation(scalar,window)
    return float(v[-1]) + (float(a[-1]) if len(a) and np.isfinite(a[-1]) else 0.0)

def score_at_cutoff(states, cutoff, method, window=5):
    """Score using observations through cutoff only; future observations are excluded."""
    if cutoff < 0 or cutoff >= len(states): raise ValueError("invalid cutoff")
    if method=="snapshot": return snapshot_signal(states,cutoff)
    if method=="temporal": return temporal_signal(states,cutoff,window=max(2,window-1))
    if method=="early_warning": return _ew_signal(states,cutoff,max(3,window))
    if method=="ceh": return ceh_signal(states,cutoff,window=max(3,window))
    raise ValueError(f"unknown method: {method}")

def evaluate_cutoffs(trajectories, transition_times, horizon, methods=("snapshot","temporal","early_warning","ceh"), window=5):
    """Evaluate identical prospective cutoffs against independently known transitions."""
    if len(trajectories)!=len(transition_times): raise ValueError("trajectory/transition lengths differ")
    if horizon < 1: raise ValueError("horizon must be positive")
    rows=[]
    for method in methods:
        scores=[]; labels=[]
        for states,t0 in zip(trajectories,transition_times):
            start=max(window+2,1); stop=min(len(states)-1,t0+horizon)
            for cutoff in range(start,stop+1):
                try: score=score_at_cutoff(states,cutoff,method,window)
                except ValueError: continue
                if not np.isfinite(score): continue
                scores.append(score); labels.append(int(0 < t0-cutoff <= horizon))
        if scores:
            y=np.asarray(labels)
            rows.append(BenchmarkRow(method,auroc(scores,labels),auprc(scores,labels),len(scores),int(y.sum())))
    return rows
