"""Candidate Cellular Event Horizon metrics.

A horizon is represented as a scored region, not a clinical label.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .dynamics import acceleration, drift, velocity


@dataclass(frozen=True)
class HorizonScore:
    """Transparent components of a candidate horizon score."""

    drift: float
    directionality: float
    acceleration: float
    convergence: float

    @property
    def total(self) -> float:
        return float(np.mean([
            self.drift,
            self.directionality,
            self.acceleration,
            self.convergence,
        ]))


def directionality(trajectory: np.ndarray) -> float:
    """Return mean normalized cosine similarity between consecutive velocities."""
    v = velocity(trajectory)
    if len(v) < 2:
        return 0.0

    a = v[:-1]
    b = v[1:]
    denom = np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1)
    valid = denom > 0
    if not np.any(valid):
        return 0.0

    cos = np.sum(a[valid] * b[valid], axis=1) / denom[valid]
    return float(np.mean((cos + 1.0) / 2.0))


def acceleration_signal(trajectory: np.ndarray) -> float:
    """Return a bounded magnitude of second-order state change."""
    a = acceleration(trajectory)
    if len(a) == 0:
        return 0.0
    return float(np.tanh(np.mean(np.linalg.norm(a, axis=1))))


def candidate_score(
    trajectory: np.ndarray,
    convergence: float = 0.0,
) -> HorizonScore:
    """Compute transparent, non-clinical CEH component scores.

    v0.1 deliberately exposes simple components instead of hiding them in a
    learned black box. Calibration and statistical testing belong to later
    experimental stages.
    """
    x = np.asarray(trajectory, dtype=float)
    d = drift(x)
    d_norm = float(np.tanh(np.mean(d)))

    return HorizonScore(
        drift=d_norm,
        directionality=directionality(x),
        acceleration=acceleration_signal(x),
        convergence=float(np.clip(convergence, 0.0, 1.0)),
    )
