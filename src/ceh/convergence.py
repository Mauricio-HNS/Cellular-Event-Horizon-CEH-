"""Trajectory convergence metrics for the CEH hypothesis.

The functions are deliberately geometric and model-agnostic. Statistical
significance must be established against an explicit null model before any
biological interpretation.
"""

from __future__ import annotations

import numpy as np


def pairwise_distance_matrix(states: np.ndarray) -> np.ndarray:
    """Return Euclidean distances between rows of a state matrix."""
    x = np.asarray(states, dtype=float)
    if x.ndim != 2 or len(x) < 2:
        raise ValueError("states must have shape (n_trajectories, features)")
    delta = x[:, None, :] - x[None, :, :]
    return np.linalg.norm(delta, axis=-1)


def convergence_index(
    trajectories: np.ndarray,
    *,
    baseline_window: int = 1,
    final_window: int = 1,
) -> float:
    """Measure relative contraction among synchronized trajectories.

    trajectories has shape (n_trajectories, time, features). The score is
    bounded to [0, 1], where larger values mean stronger relative contraction.
    It is not a probability and has no biological interpretation by itself.
    """
    x = np.asarray(trajectories, dtype=float)
    if x.ndim != 3:
        raise ValueError("trajectories must have shape (n_trajectories, time, features)")
    n, t, _ = x.shape
    if n < 2 or t < 2:
        raise ValueError("at least 2 trajectories and 2 time points are required")
    if baseline_window < 1 or final_window < 1:
        raise ValueError("window sizes must be positive")
    if baseline_window + final_window > t:
        raise ValueError("windows exceed available time points")

    baseline = x[:, :baseline_window].mean(axis=1)
    final = x[:, -final_window:].mean(axis=1)

    base_d = pairwise_distance_matrix(baseline)
    final_d = pairwise_distance_matrix(final)

    upper = np.triu_indices(n, k=1)
    initial = float(np.mean(base_d[upper]))
    ending = float(np.mean(final_d[upper]))

    if initial <= 1e-12:
        return 1.0 if ending <= 1e-12 else 0.0

    return float(np.clip(1.0 - ending / initial, -1.0, 1.0) * 0.5 + 0.5)
