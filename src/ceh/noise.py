"""Synthetic noise mechanisms for adversarial transition benchmarks."""
from __future__ import annotations
import numpy as np

def gaussian(size, sigma=1.0, seed=7):
    if sigma < 0: raise ValueError("sigma must be non-negative")
    return np.random.default_rng(seed).normal(0.0,sigma,size=size)

def heavy_tailed(size, scale=1.0, df=2.0, seed=7):
    if scale < 0 or df <= 0: raise ValueError("invalid heavy-tailed parameters")
    return np.random.default_rng(seed).standard_t(df,size=size)*scale

def impulse_contaminated(values, probability=0.02, magnitude=8.0, seed=7):
    if not 0 <= probability <= 1 or magnitude < 0: raise ValueError("invalid contamination parameters")
    x=np.asarray(values,dtype=float).copy()
    rng=np.random.default_rng(seed)
    mask=rng.random(x.shape)<probability
    return x + mask*rng.normal(0.0,magnitude,size=x.shape)
