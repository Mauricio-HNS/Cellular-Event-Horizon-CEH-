"""Null-world calibration for blind horizon detection."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .detector import detect_horizons

@dataclass(frozen=True)
class NullCalibration:
    observed_score: float
    null_scores: np.ndarray
    empirical_p: float
    z_score: float

def maximum_horizon_score(states: np.ndarray, window: int = 5) -> float:
    candidates = detect_horizons(states, window=window)
    return float(max((c.score for c in candidates), default=0.0))

def shuffled_maximum_score(states: np.ndarray, window: int = 5, seed: int = 7) -> float:
    rng = np.random.default_rng(seed)
    x = np.asarray(states, dtype=float)
    shuffled = x[rng.permutation(x.shape[0])]
    return maximum_horizon_score(shuffled, window=window)

def calibrate_against_time_null(states: np.ndarray, window: int = 5,
                                permutations: int = 500, seed: int = 7) -> NullCalibration:
    if permutations < 1:
        raise ValueError("permutations must be positive")
    observed = maximum_horizon_score(states, window)
    null = np.array(
        [shuffled_maximum_score(states, window, seed + i) for i in range(permutations)]
    )
    p = float((1 + np.sum(null >= observed)) / (permutations + 1))
    sd = float(np.std(null, ddof=1))
    z = 0.0 if sd == 0 else float((observed - np.mean(null)) / sd)
    return NullCalibration(observed, null, p, z)
