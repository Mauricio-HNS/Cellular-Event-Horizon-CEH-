"""Trajectory dynamics used by the CEH hypothesis."""

from __future__ import annotations

import numpy as np


def velocity(trajectory: np.ndarray) -> np.ndarray:
    """Estimate first-order state velocity along a trajectory."""
    x = np.asarray(trajectory, dtype=float)
    if x.ndim != 2 or len(x) < 2:
        raise ValueError("trajectory must have shape (time, features) with at least 2 observations")
    return np.diff(x, axis=0)


def acceleration(trajectory: np.ndarray) -> np.ndarray:
    """Estimate second-order state change."""
    v = velocity(trajectory)
    if len(v) < 2:
        return np.empty((0, trajectory.shape[1]), dtype=float)
    return np.diff(v, axis=0)


def drift(trajectory: np.ndarray, reference: np.ndarray | None = None) -> np.ndarray:
    """Measure distance from a reference state at every time point."""
    x = np.asarray(trajectory, dtype=float)
    if x.ndim != 2:
        raise ValueError("trajectory must be a 2D array")
    ref = x[0] if reference is None else np.asarray(reference, dtype=float)
    if ref.shape != (x.shape[1],):
        raise ValueError("reference must match the feature dimension")
    return np.linalg.norm(x - ref, axis=1)
