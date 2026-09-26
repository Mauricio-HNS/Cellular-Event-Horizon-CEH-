"""Null-model utilities for CEH experiments."""

from __future__ import annotations

import numpy as np


def permute_trajectories(
    trajectories: np.ndarray,
    *,
    seed: int = 7,
) -> np.ndarray:
    """Permute trajectory identities independently at each time point.

    This preserves each time slice's marginal distribution while destroying
    persistent identity-level temporal coupling.
    """
    x = np.asarray(trajectories, dtype=float)
    if x.ndim != 3:
        raise ValueError("trajectories must have shape (n_trajectories, time, features)")

    rng = np.random.default_rng(seed)
    out = x.copy()
    for t in range(x.shape[1]):
        out[:, t] = out[rng.permutation(x.shape[0]), t]
    return out


def shuffle_time_axis(
    trajectories: np.ndarray,
    *,
    seed: int = 7,
) -> np.ndarray:
    """Apply one common random time permutation to all trajectories."""
    x = np.asarray(trajectories, dtype=float)
    if x.ndim != 3:
        raise ValueError("trajectories must have shape (n_trajectories, time, features)")

    rng = np.random.default_rng(seed)
    return x[:, rng.permutation(x.shape[1]), :]
