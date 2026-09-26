"""Simple baselines for prospective transition experiments."""
from __future__ import annotations
import numpy as np

def snapshot_signal(states: np.ndarray, cutoff: int) -> float:
    x = np.asarray(states, dtype=float)
    if cutoff < 0 or cutoff >= len(x):
        raise ValueError("invalid cutoff")
    return float(np.linalg.norm(x[cutoff]))

def temporal_signal(states: np.ndarray, cutoff: int, window: int = 3) -> float:
    x = np.asarray(states, dtype=float)
    if window < 2 or cutoff < window:
        raise ValueError("cutoff must contain the requested history")
    delta = x[1:cutoff + 1] - x[:cutoff]
    recent = delta[-window:]
    return float(np.linalg.norm(np.mean(recent, axis=0)))

def ceh_signal(states: np.ndarray, cutoff: int, window: int = 4) -> float:
    """Minimal prospective CEH construct: directionality × acceleration."""
    x = np.asarray(states, dtype=float)
    if window < 3 or cutoff < window + 1:
        raise ValueError("insufficient history")
    delta = x[1:cutoff + 1] - x[:cutoff]
    recent = delta[-window:]
    direction = np.linalg.norm(np.mean(recent, axis=0))
    acceleration = np.linalg.norm(np.mean(np.diff(recent, axis=0), axis=0))
    return float(direction * (1.0 + acceleration))
