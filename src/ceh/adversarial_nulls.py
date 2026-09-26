"""Adversarial null mechanisms that mimic CEH feature geometry.

These controls are deliberately designed to reproduce individual ingredients
of the candidate signal without encoding a CEH-specific transition mechanism.
A CEH result that disappears under these controls is not evidence for
mechanism-specific information.
"""
from __future__ import annotations

import numpy as np


def matched_directional_noise(
    n_trajectories: int = 24,
    n_steps: int = 60,
    n_features: int = 4,
    *,
    drift_scale: float = 0.08,
    acceleration_scale: float = 0.015,
    noise: float = 0.03,
    seed: int = 7,
) -> list[np.ndarray]:
    """Directional + accelerating trajectories with no labeled transition."""
    if min(n_trajectories, n_steps, n_features) < 2:
        raise ValueError("dimensions must be >= 2")
    if drift_scale <= 0 or acceleration_scale < 0 or noise < 0:
        raise ValueError("invalid scale parameters")

    rng = np.random.default_rng(seed)
    direction = rng.normal(size=n_features)
    direction /= np.linalg.norm(direction)

    trajectories = []
    for _ in range(n_trajectories):
        x = np.zeros((n_steps, n_features), dtype=float)
        velocity = np.zeros(n_features, dtype=float)
        for t in range(1, n_steps):
            velocity += acceleration_scale * direction
            x[t] = (
                x[t - 1]
                + drift_scale * direction
                + velocity
                + noise * rng.normal(size=n_features)
            )
        trajectories.append(x)
    return trajectories


def convergence_without_transition(
    n_trajectories: int = 24,
    n_steps: int = 60,
    n_features: int = 4,
    *,
    attractor_scale: float = 0.02,
    noise: float = 0.03,
    seed: int = 7,
) -> list[np.ndarray]:
    """Trajectories that converge toward a common attractor without events."""
    if min(n_trajectories, n_steps, n_features) < 2:
        raise ValueError("dimensions must be >= 2")
    if attractor_scale <= 0 or noise < 0:
        raise ValueError("invalid scale parameters")

    rng = np.random.default_rng(seed)
    attractor = rng.normal(scale=attractor_scale, size=n_features)
    trajectories = []

    for _ in range(n_trajectories):
        x = rng.normal(scale=1.0, size=(n_features,))
        trajectory = np.empty((n_steps, n_features), dtype=float)
        for t in range(n_steps):
            trajectory[t] = x
            x = x + 0.12 * (attractor - x) + noise * rng.normal(size=n_features)
        trajectories.append(trajectory)

    return trajectories


def matched_geometry_population(
    n_trajectories: int = 24,
    n_steps: int = 60,
    n_features: int = 4,
    *,
    seed: int = 7,
) -> list[np.ndarray]:
    """Null population combining direction, acceleration and convergence."""
    directional = matched_directional_noise(
        n_trajectories=n_trajectories,
        n_steps=n_steps,
        n_features=n_features,
        seed=seed,
    )
    convergent = convergence_without_transition(
        n_trajectories=n_trajectories,
        n_steps=n_steps,
        n_features=n_features,
        seed=seed + 1,
    )
    return [
        0.5 * a + 0.5 * b
        for a, b in zip(directional, convergent)
    ]
