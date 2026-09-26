"""Controlled synthetic worlds for falsification experiments."""

from __future__ import annotations

import numpy as np


def directional_trajectory(
    n_steps: int = 40,
    n_features: int = 4,
    transition_start: int = 20,
    noise: float = 0.03,
    seed: int = 7,
) -> np.ndarray:
    """Generate a trajectory with a known directional transition."""
    if n_steps < 3 or n_features < 1:
        raise ValueError("n_steps >= 3 and n_features >= 1 are required")
    if not 0 <= transition_start < n_steps:
        raise ValueError("transition_start must be inside the trajectory")

    rng = np.random.default_rng(seed)
    x = rng.normal(0.0, noise, size=(n_steps, n_features))
    direction = np.linspace(0.0, 1.0, n_steps - transition_start)[:, None]
    weights = np.linspace(0.4, 1.0, n_features)[None, :]
    x[transition_start:] += direction * weights
    return x


def null_trajectory(
    n_steps: int = 40,
    n_features: int = 4,
    noise: float = 0.5,
    seed: int = 7,
) -> np.ndarray:
    """Generate observations with no intended temporal direction."""
    rng = np.random.default_rng(seed)
    return rng.normal(0.0, noise, size=(n_steps, n_features))


def shuffle_time(trajectory: np.ndarray, seed: int = 7) -> np.ndarray:
    """Destroy temporal ordering while preserving the observations."""
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(trajectory))
    return np.asarray(trajectory)[order]
