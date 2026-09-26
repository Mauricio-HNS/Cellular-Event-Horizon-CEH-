"""Distribution-free utilities for controlled CEH experiments."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class PermutationResult:
    observed: float
    null_mean: float
    p_value: float
    effect_size: float
    null: np.ndarray

def permutation_test(values: np.ndarray, statistic: float, permutations: int = 1000,
                     seed: int = 7) -> PermutationResult:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.size < 2:
        raise ValueError("values must be a one-dimensional sample")
    if permutations < 1:
        raise ValueError("permutations must be positive")
    rng = np.random.default_rng(seed)
    null = np.empty(permutations)
    center = float(np.mean(x))
    for i in range(permutations):
        shuffled = rng.permutation(x)
        null[i] = float(np.mean(shuffled - center))
    observed = float(statistic)
    p = float((1 + np.sum(np.abs(null) >= abs(observed))) / (permutations + 1))
    scale = float(np.std(null, ddof=1))
    effect = 0.0 if scale == 0 else float((observed - np.mean(null)) / scale)
    return PermutationResult(observed, float(np.mean(null)), p, effect, null)

def bootstrap_mean(values: np.ndarray, iterations: int = 1000, seed: int = 7) -> tuple[float, float]:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.size < 2:
        raise ValueError("values must be a one-dimensional sample")
    rng = np.random.default_rng(seed)
    means = np.empty(iterations)
    for i in range(iterations):
        means[i] = np.mean(rng.choice(x, size=x.size, replace=True))
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))
