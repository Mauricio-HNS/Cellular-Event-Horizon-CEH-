"""Representation-matched adversarial controls.

Controls are selected from a large no-transition pool to match the empirical
distribution of candidate geometry features in the transition population.
Matching is a computational control, not biological validation.
"""
from __future__ import annotations

import numpy as np


def geometry_signature(
    trajectory: np.ndarray,
    *,
    window: int = 4,
) -> np.ndarray:
    """Return direction, acceleration and convergence summary features."""
    x = np.asarray(trajectory, dtype=float)
    if x.ndim != 2 or x.shape[0] < window + 2:
        raise ValueError("trajectory is too short")
    delta = np.diff(x, axis=0)
    recent = delta[-window:]
    direction = np.linalg.norm(np.mean(recent, axis=0))
    acceleration = np.linalg.norm(np.mean(np.diff(recent, axis=0), axis=0))
    pairwise = np.linalg.norm(x[:, None, :] - x[None, :, :], axis=-1)
    upper = pairwise[np.triu_indices(len(x), k=1)]
    convergence = float(np.mean(upper[-max(1, len(upper) // 10):]))
    return np.array([direction, acceleration, convergence], dtype=float)


def match_controls(
    target_trajectories: list[np.ndarray],
    control_pool: list[np.ndarray],
    *,
    window: int = 4,
) -> list[np.ndarray]:
    """Greedily select controls closest in standardized geometry space."""
    if not target_trajectories or not control_pool:
        raise ValueError("target and control populations must be non-empty")

    target = np.vstack([
        geometry_signature(x, window=window) for x in target_trajectories
    ])
    pool = np.vstack([
        geometry_signature(x, window=window) for x in control_pool
    ])
    mean = target.mean(axis=0)
    scale = np.where(target.std(axis=0) < 1e-12, 1.0, target.std(axis=0))
    target_z = (target - mean) / scale
    pool_z = (pool - mean) / scale

    remaining = list(range(len(control_pool)))
    selected = []
    for row in target_z:
        distances = np.linalg.norm(pool_z[remaining] - row, axis=1)
        position = int(np.argmin(distances))
        idx = remaining.pop(position)
        selected.append(control_pool[idx])
    return selected
