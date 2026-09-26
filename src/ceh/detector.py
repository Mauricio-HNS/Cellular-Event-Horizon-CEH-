"""Prospective horizon detection without future observations."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class HorizonCandidate:
    time: int
    score: float
    directionality: float
    acceleration: float

def detect_horizons(states: np.ndarray, window: int = 5, threshold: float = 0.0) -> list[HorizonCandidate]:
    x = np.asarray(states, dtype=float)
    if x.ndim != 2:
        raise ValueError("states must have shape (time, features)")
    if window < 3 or len(x) <= window + 1:
        raise ValueError("trajectory is too short for the requested window")
    velocity = np.diff(x, axis=0)
    candidates = []
    for t in range(window + 1, len(x)):
        recent = velocity[t - window:t]
        direction = float(np.linalg.norm(np.mean(recent, axis=0)))
        acceleration = float(np.linalg.norm(np.mean(np.diff(recent, axis=0), axis=0)))
        score = direction * (1.0 + acceleration)
        if score >= threshold:
            candidates.append(HorizonCandidate(t, score, direction, acceleration))
    return candidates

def first_candidate(candidates: list[HorizonCandidate]) -> HorizonCandidate | None:
    return max(candidates, key=lambda c: c.score, default=None)
