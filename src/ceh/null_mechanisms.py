from __future__ import annotations

import numpy as np


def nonnormal_linear_system(
    steps: int = 1000,
    dt: float = 0.01,
    coupling: float = 8.0,
    seed: int = 7,
    sigma: float = 0.05,
) -> np.ndarray:
    """Stable non-normal 2D system with transient amplification.

    The eigenvalues remain negative; apparent warning signals can arise
    without a bifurcation. This is an adversarial CEH null mechanism.
    """
    if steps < 1 or dt <= 0 or sigma < 0:
        raise ValueError("invalid simulation parameters")
    rng = np.random.default_rng(seed)
    x = np.zeros((steps + 1, 2), dtype=float)
    A = np.array([[-1.0, coupling], [0.0, -1.0]])
    for i in range(steps):
        x[i + 1] = x[i] + dt * (A @ x[i]) + sigma * np.sqrt(dt) * rng.normal(size=2)
    return x


def clustered_events(
    n_events: int,
    dimensions: int = 2,
    cluster_scale: float = 0.08,
    seed: int = 7,
) -> np.ndarray:
    """Generate spatially clustered synthetic microscopic events."""
    if n_events < 1 or dimensions < 1 or cluster_scale <= 0:
        raise ValueError("invalid event parameters")
    rng = np.random.default_rng(seed)
    centers = rng.uniform(-1.0, 1.0, size=(max(1, n_events // 10), dimensions))
    assignments = rng.integers(0, len(centers), size=n_events)
    return centers[assignments] + rng.normal(
        scale=cluster_scale, size=(n_events, dimensions)
    )
