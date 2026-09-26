"""Multiplicity control for the CEH falsification program.

The primary endpoint should remain identifiable before analysis. Secondary
experiments and null challenges are corrected for multiplicity so a collection
of favorable tests is not mistaken for independent confirmation.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class FDRResult:
    p_values: tuple[float, ...]
    q_values: tuple[float, ...]
    rejected: tuple[bool, ...]
    alpha: float


def benjamini_hochberg(p_values, *, alpha: float = 0.05) -> FDRResult:
    p = np.asarray(p_values, dtype=float)
    if p.ndim != 1 or len(p) == 0:
        raise ValueError("p_values must be a non-empty one-dimensional array")
    if not np.all(np.isfinite(p)) or np.any((p < 0) | (p > 1)):
        raise ValueError("p_values must be finite values in [0, 1]")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    m = len(p)
    order = np.argsort(p)
    ranked = p[order]
    q_ranked = np.empty(m, dtype=float)

    running = 1.0
    for i in range(m - 1, -1, -1):
        running = min(running, ranked[i] * m / (i + 1))
        q_ranked[i] = running

    q = np.empty(m, dtype=float)
    q[order] = q_ranked
    rejected = q <= alpha

    return FDRResult(
        p_values=tuple(float(x) for x in p),
        q_values=tuple(float(x) for x in q),
        rejected=tuple(bool(x) for x in rejected),
        alpha=alpha,
    )


def primary_endpoint_gate(
    *,
    p_value: float,
    effect: float,
    ci_lower: float,
    q_value: float | None = None,
    alpha: float = 0.05,
) -> bool:
    """Conservative gate for the pre-specified primary incremental endpoint."""
    if not all(np.isfinite(x) for x in [p_value, effect, ci_lower]):
        raise ValueError("primary endpoint values must be finite")
    if q_value is not None and not np.isfinite(q_value):
        raise ValueError("q_value must be finite when supplied")

    significance = p_value < alpha
    if q_value is not None:
        significance = significance and q_value < alpha

    return bool(significance and effect > 0 and ci_lower > 0)
