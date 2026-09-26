"""Trajectory-level feature extraction."""

from __future__ import annotations

import numpy as np

from .dynamics import acceleration, drift, velocity
from .horizon import directionality


def trajectory_features(
    trajectory: np.ndarray,
    *,
    reference: np.ndarray | None = None,
) -> dict[str, float]:
    """Return transparent features for one trajectory."""
    x = np.asarray(trajectory, dtype=float)
    if x.ndim != 2:
        raise ValueError("trajectory must have shape (time, features)")

    v = velocity(x)
    a = acceleration(x)
    d = drift(x, reference)

    return {
        "mean_drift": float(np.mean(d)),
        "final_drift": float(d[-1]),
        "directionality": float(directionality(x)),
        "mean_speed": float(np.mean(np.linalg.norm(v, axis=1))),
        "mean_acceleration": float(
            np.mean(np.linalg.norm(a, axis=1)) if len(a) else 0.0
        ),
    }
