"""Observation operators for synthetic worlds."""
from __future__ import annotations
import numpy as np

def observe(states: np.ndarray, *, noise: float = 0.0, missing_rate: float = 0.0,
            seed: int = 7) -> np.ndarray:
    """Generate an imperfect observation stream from latent states."""
    x = np.asarray(states, dtype=float).copy()
    if x.ndim != 2:
        raise ValueError("states must have shape (time, features)")
    if not 0 <= missing_rate < 1:
        raise ValueError("missing_rate must be in [0, 1)")
    rng = np.random.default_rng(seed)
    if noise:
        x += rng.normal(0.0, noise, x.shape)
    if missing_rate:
        mask = rng.random(x.shape) < missing_rate
        x[mask] = np.nan
    return x
