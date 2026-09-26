"""Evaluation primitives for prospective transition experiments."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class ProspectiveResult:
    cutoff: int
    signal: float
    future_target: float

def future_distance(states: np.ndarray, cutoff: int) -> float:
    x = np.asarray(states, dtype=float)
    if cutoff < 0 or cutoff >= len(x) - 1:
        raise ValueError("cutoff must leave future observations")
    return float(np.linalg.norm(x[-1] - x[cutoff]))

def evaluate_cutoff(states: np.ndarray, cutoff: int, signal: float) -> ProspectiveResult:
    return ProspectiveResult(
        cutoff=cutoff,
        signal=float(signal),
        future_target=future_distance(states, cutoff),
    )
