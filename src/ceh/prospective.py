"""Prospective CEH analysis.

The defining rule is strict temporal separation: features at cutoff t are
computed only from observations available through t.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from .trajectory import trajectory_features

@dataclass(frozen=True)
class ProspectiveWindow:
    cutoff: int
    features: dict[str, float]

def extract_window(trajectory: np.ndarray, cutoff: int) -> ProspectiveWindow:
    """Extract features using observations up to and including cutoff."""
    x = np.asarray(trajectory, dtype=float)
    if x.ndim != 2:
        raise ValueError("trajectory must have shape (time, features)")
    if cutoff < 1 or cutoff >= len(x):
        raise ValueError("cutoff must leave at least two observations")
    return ProspectiveWindow(cutoff=cutoff, features=trajectory_features(x[: cutoff + 1]))

def future_displacement(trajectory: np.ndarray, cutoff: int) -> float:
    """Measure later displacement from the cutoff state."""
    x = np.asarray(trajectory, dtype=float)
    if cutoff < 0 or cutoff >= len(x) - 1:
        raise ValueError("cutoff must leave at least one future observation")
    return float(np.linalg.norm(x[-1] - x[cutoff]))
