"""Trajectory-level uncertainty and paired permutation inference."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .metrics import auroc


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


def paired_auc_bootstrap(
    labels, baseline_scores, full_scores, *, replicates=2000,
    confidence=0.95, seed=7,
) -> BootstrapCI:
    """Paired bootstrap of AUROC(full)-AUROC(baseline) over trajectories."""
    y = np.asarray(labels, dtype=int)
    base = np.asarray(baseline_scores, dtype=float)
    full = np.asarray(full_scores, dtype=float)
    if not (y.ndim == base.ndim == full.ndim == 1):
        raise ValueError("all inputs must be one-dimensional")
    if not (len(y) == len(base) == len(full)) or len(y) < 4:
        raise ValueError("paired arrays must have equal length >= 4")
    if len(np.unique(y)) < 2:
        raise ValueError("labels must contain both classes")
    if not (np.all(np.isfinite(base)) and np.all(np.isfinite(full))):
        raise ValueError("scores must be finite")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")

    observed = auroc(y, full) - auroc(y, base)
    rng = np.random.default_rng(seed)
    estimates = []
    for _ in range(replicates):
        idx = rng.integers(0, len(y), size=len(y))
        if len(np.unique(y[idx])) < 2:
            continue
        estimates.append(auroc(y[idx], full[idx]) - auroc(y[idx], base[idx]))
    if len(estimates) < max(100, replicates // 10):
        raise ValueError("too many bootstrap samples lost a class")
    values = np.asarray(estimates)
    alpha = 1.0 - confidence
    return BootstrapCI(float(observed), float(np.quantile(values, alpha / 2)),
                       float(np.quantile(values, 1 - alpha / 2)), len(values))


def paired_auc_permutation(
    labels, baseline_scores, full_scores, *, replicates=2000, seed=7,
) -> PermutationResult:
    """Permutation test by swapping paired model scores within trajectories."""
    y = np.asarray(labels, dtype=int)
    base = np.asarray(baseline_scores, dtype=float)
    full = np.asarray(full_scores, dtype=float)
    if not (y.ndim == base.ndim == full.ndim == 1):
        raise ValueError("all inputs must be one-dimensional")
    if not (len(y) == len(base) == len(full)) or len(y) < 4:
        raise ValueError("paired arrays must have equal length >= 4")
    if len(np.unique(y)) < 2:
        raise ValueError("labels must contain both classes")
    if not (np.all(np.isfinite(base)) and np.all(np.isfinite(full))):
        raise ValueError("scores must be finite")

    observed = float(auroc(y, full) - auroc(y, base))
    rng = np.random.default_rng(seed)
    extreme = 0
    for _ in range(replicates):
        swap = rng.integers(0, 2, size=len(y)).astype(bool)
        perm_base = np.where(swap, full, base)
        perm_full = np.where(swap, base, full)
        delta = auroc(y, perm_full) - auroc(y, perm_base)
        if delta >= observed:
            extreme += 1
    return PermutationResult(observed, float((extreme + 1) / (replicates + 1)), replicates)


def bootstrap_mean_difference(
    deltas: np.ndarray, *, replicates=2000, confidence=0.95, seed=7,
) -> BootstrapCI:
    values = np.asarray(deltas, dtype=float)
    if values.ndim != 1 or len(values) < 2 or not np.all(np.isfinite(values)):
        raise ValueError("deltas must be a finite one-dimensional array")
    rng = np.random.default_rng(seed)
    samples = rng.integers(0, len(values), size=(replicates, len(values)))
    boot = values[samples].mean(axis=1)
    alpha = 1.0 - confidence
    return BootstrapCI(float(values.mean()), float(np.quantile(boot, alpha / 2)),
                       float(np.quantile(boot, 1 - alpha / 2)), replicates)


def paired_sign_flip(
    deltas: np.ndarray, *, replicates=2000, alternative="greater", seed=7,
) -> PermutationResult:
    values = np.asarray(deltas, dtype=float)
    if values.ndim != 1 or len(values) < 2 or not np.all(np.isfinite(values)):
        raise ValueError("deltas must be a finite one-dimensional array")
    if alternative not in {"greater", "two-sided"}:
        raise ValueError("alternative must be 'greater' or 'two-sided'")
    observed = float(values.mean())
    rng = np.random.default_rng(seed)
    signs = rng.choice(np.array([-1.0, 1.0]), size=(replicates, len(values)))
    null = (signs * values).mean(axis=1)
    extreme = np.count_nonzero(
        null >= observed if alternative == "greater"
        else np.abs(null) >= abs(observed)
    )
    return PermutationResult(observed, float((extreme + 1) / (replicates + 1)), replicates)
