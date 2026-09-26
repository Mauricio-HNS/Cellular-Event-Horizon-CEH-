"""Trajectory-block permutation tests preserving within-trajectory structure."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .hierarchical import trajectory_level_scores

@dataclass(frozen=True)
class PermutationResult:
    method: str
    observed_auc: float
    null_mean: float
    null_std: float
    p_value: float
    permutations: int
    trajectories: int

def _auc(event, control):
    e=np.asarray(event,float); c=np.asarray(control,float)
    return float(np.mean(e[:,None]>c[None,:])+.5*np.mean(e[:,None]==c[None,:]))

def permutation_test_trajectories(trajectories, transition_times, horizon=30,
                                  methods=("snapshot","temporal","early_warning","ceh"),
                                  permutations=2000, seed=7):
    trajectories=list(trajectories); transition_times=list(transition_times)
    if len(trajectories)!=len(transition_times): raise ValueError("trajectory/transition lengths differ")
    if len(trajectories)<4: raise ValueError("at least four trajectories are required")
    if permutations<100: raise ValueError("permutations must be >= 100")
    rng=np.random.default_rng(seed); results=[]
    for method in methods:
        events=[]; controls=[]
        for x,t0 in zip(trajectories,transition_times):
            e,c=trajectory_level_scores(x,t0,horizon,method)
            if np.isfinite(e) and np.isfinite(c):
                events.append(e); controls.append(c)
        events=np.asarray(events); controls=np.asarray(controls)
        if len(events)<4: continue
        observed=_auc(events,controls)
        # Null: randomly reassign event/control labels across trajectories.
        pooled=np.column_stack([events,controls])
        null=[]
        for _ in range(permutations):
            swap=rng.integers(0,2,len(pooled)).astype(bool)
            e=np.where(swap,pooled[:,1],pooled[:,0])
            c=np.where(swap,pooled[:,0],pooled[:,1])
            null.append(_auc(e,c))
        null=np.asarray(null)
        p=(1+int(np.sum(null>=observed)))/(permutations+1)
        results.append(PermutationResult(method,observed,float(null.mean()),float(null.std(ddof=1)),
            float(p),permutations,len(events)))
    return results
