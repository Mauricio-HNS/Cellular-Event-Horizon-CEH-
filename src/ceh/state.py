"""Explicit biological state representation.

The module intentionally stays modality-agnostic: a biological state is an
array plus metadata describing what was measured and how it was represented.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class BiologicalState:
    values: np.ndarray
    modality: str = "unspecified"
    timestamp: float | None = None

    def __post_init__(self) -> None:
        values = np.asarray(self.values, dtype=float)
        if values.ndim != 1:
            raise ValueError("values must be a one-dimensional state vector")
        object.__setattr__(self, "values", values)

    @property
    def dimension(self) -> int:
        return int(self.values.shape[0])
