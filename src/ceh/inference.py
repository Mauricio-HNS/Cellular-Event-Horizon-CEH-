"""Trajectory-level uncertainty and paired permutation inference.

All resampling units are trajectories. Cutoffs inside a trajectory are never
treated as independent replicates.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class BootstrapCI:
    estimate: float
    lower: float
    upper: float
    replicates: int


@dataclass(frozen=True)
class PermutationResult:
    observed: float
    p_value: float
    replicates: int


def bootstrap_mean_difference(
    deltas: np.ndarray,
    *,
    replicates: int = 2000,
    confidence: float = 0.95,
    seed: int = 7,
) -> BootstrapCI:
    values = np.asarray(deltas, dtype=float)
    if values.ndim != 1 or len(values) < 2:
        raise ValueError("at least two trajectory-level deltas are required")
    if not np.all(np.isfinite(values)):
        raise ValueError("deltas must be finite")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")

    rng = np.random.default_rng(seed)
    samples = rng.integers(0, len(values), size=(replicates, len(values)))
    boot = values[samples].mean(axis=1)
    alpha = 1.0 - confidence
    return BootstrapCI(
        estimate=float(values.mean()),
        lower=float(np.quantile(boot, alpha / 2)),
        upper=float(np.quantile(boot, 1 - alpha / 2)),
        replicates=replicates,
    )


def paired_sign_flip(
    deltas: np.ndarray,
    *,
    replicates: int = 2000,
    alternative: str = "greater",
    seed: int = 7,
) -> PermutationResult:
    """Paired sign-flip test over independent trajectory-level contrasts."""
    values = np.asarray(deltas, dtype=float)
    if values.ndim != 1 or len(values) < 2:
        raise ValueError("at least two trajectory-level deltas are required")
    if not np.all(np.isfinite(values)):
        raise ValueError("deltas must be finite")
    if alternative not in {"greater", "two-sided"}:
        raise ValueError("alternative must be 'greater' or 'two-sided'")

    observed = float(values.mean())
    rng = np.random.default_rng(seed)
    signs = rng.choice(np.array([-1.0, 1.0]), size=(replicates, len(values)))
    null = (signs * values).mean(axis=1)

    if alternative == "greater":
        extreme = np.count_nonzero(null >= observed)
    else:
        extreme = np.count_nonzero(np.abs(null) >= abs(observed))

    p_value = float((extreme + 1) / (replicates + 1))
    return PermutationResult(observed, p_value, replicates)
