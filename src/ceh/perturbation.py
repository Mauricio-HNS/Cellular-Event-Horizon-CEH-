"""Intervention abstractions for biological dynamical experiments."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Perturbation:
    values: np.ndarray
    label: str = "unspecified"

    def __post_init__(self) -> None:
        values = np.asarray(self.values, dtype=float)
        if values.ndim != 1:
            raise ValueError("values must be a one-dimensional intervention vector")
        object.__setattr__(self, "values", values)

def transition_step(state: np.ndarray, context: np.ndarray, intervention: np.ndarray,
                    dynamics, noise: np.ndarray | None = None) -> np.ndarray:
    """Apply an explicit dynamical map; no biological interpretation is assumed."""
    x = np.asarray(state, dtype=float)
    e = np.asarray(context, dtype=float)
    u = np.asarray(intervention, dtype=float)
    next_state = np.asarray(dynamics(x, e, u), dtype=float)
    if next_state.shape != x.shape:
        raise ValueError("dynamics must preserve state shape")
    if noise is not None:
        n = np.asarray(noise, dtype=float)
        if n.shape != x.shape:
            raise ValueError("noise must match state shape")
        next_state = next_state + n
    return next_state
