"""Independent observation channels for synthetic population worlds."""
from __future__ import annotations
import numpy as np

def project(states: np.ndarray, matrix: np.ndarray, noise: float = 0.0, seed: int = 7) -> np.ndarray:
    x = np.asarray(states, dtype=float)
    m = np.asarray(matrix, dtype=float)
    if x.ndim != 3 or m.ndim != 2 or x.shape[-1] != m.shape[1]:
        raise ValueError("expected states (time, entities, features) and matrix (outputs, features)")
    y = np.einsum("tef,of->teo", x, m)
    if noise:
        rng = np.random.default_rng(seed)
        y = y + rng.normal(0.0, noise, y.shape)
    return y

def independent_modalities(states: np.ndarray, outputs: int = 3, seed: int = 7):
    x = np.asarray(states, dtype=float)
    if x.ndim != 3:
        raise ValueError("states must have shape (time, entities, features)")
    rng = np.random.default_rng(seed)
    matrices = [rng.normal(size=(outputs, x.shape[-1])) for _ in range(2)]
    return tuple(project(x, matrix, noise=0.01, seed=seed + i)
                 for i, matrix in enumerate(matrices))
