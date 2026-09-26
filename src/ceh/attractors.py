"""Attractor and convergence diagnostics for controlled experiments."""
from __future__ import annotations
import numpy as np

def centroid(states: np.ndarray) -> np.ndarray:
    x = np.asarray(states, dtype=float)
    if x.ndim < 2:
        raise ValueError("states must have a feature axis")
    return np.nanmean(x.reshape(-1, x.shape[-1]), axis=0)

def basin_distance(states: np.ndarray, target: np.ndarray) -> np.ndarray:
    x = np.asarray(states, dtype=float)
    y = np.asarray(target, dtype=float)
    if x.shape[-1] != y.shape[-1]:
        raise ValueError("target dimension must match state dimension")
    return np.linalg.norm(x - y, axis=-1)

def convergence_over_time(states: np.ndarray) -> np.ndarray:
    x = np.asarray(states, dtype=float)
    if x.ndim != 3:
        raise ValueError("states must have shape (time, entities, features)")
    values = []
    for frame in x:
        distances = np.linalg.norm(frame[:, None, :] - frame[None, :, :], axis=-1)
        values.append(float(distances.sum() / max(1, x.shape[1] * (x.shape[1] - 1))))
    return np.asarray(values)
