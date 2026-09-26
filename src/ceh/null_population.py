"""Matched transition/no-transition population generators.

The null population preserves dimensionality, length and observation noise while
removing the transition mechanism. This is intended to challenge CEH against a
population-level alternative rather than a within-trajectory control window.
"""

from __future__ import annotations

import numpy as np


def matched_no_transition(
    n_trajectories: int,
    n_steps: int,
    n_features: int,
    *,
    noise: float = 0.03,
    seed: int = 7,
) -> list[np.ndarray]:
    """Generate stationary trajectories matched to a transition population."""
    if min(n_trajectories, n_steps, n_features) < 2:
        raise ValueError("all dimensions must be >= 2")
    rng = np.random.default_rng(seed)
    return [
        rng.normal(0.0, noise, size=(n_steps, n_features))
        for _ in range(n_trajectories)
    ]


def matched_directional_population(
    n_trajectories: int,
    n_steps: int,
    n_features: int,
    transition_start: int,
    *,
    noise: float = 0.03,
    seed: int = 7,
) -> tuple[list[np.ndarray], list[int]]:
    """Generate a matched transition population with known event times."""
    if not 2 <= transition_start < n_steps:
        raise ValueError("transition_start must leave a pre-transition segment")
    rng = np.random.default_rng(seed)
    trajectories = []
    for _ in range(n_trajectories):
        x = rng.normal(0.0, noise, size=(n_steps, n_features))
        direction = np.linspace(0.0, 1.0, n_steps - transition_start)[:, None]
        weights = np.linspace(0.4, 1.0, n_features)[None, :]
        x[transition_start:] += direction * weights
        trajectories.append(x)
    return trajectories, [transition_start] * n_trajectories
