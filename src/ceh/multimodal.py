"""Small, explicit utilities for multimodal state reconstruction."""
from __future__ import annotations
import numpy as np

def concatenate_modalities(*modalities: np.ndarray) -> np.ndarray:
    """Concatenate aligned modality vectors into one explicit representation."""
    if not modalities:
        raise ValueError("at least one modality is required")
    arrays = [np.asarray(m, dtype=float) for m in modalities]
    if any(a.ndim != 1 for a in arrays):
        raise ValueError("each modality must be one-dimensional")
    return np.concatenate(arrays)

def modality_agreement(*representations: np.ndarray) -> float:
    """Return mean pairwise cosine agreement between modality representations."""
    if len(representations) < 2:
        raise ValueError("at least two representations are required")
    arrays = [np.asarray(r, dtype=float) for r in representations]
    if any(a.ndim != 1 for a in arrays):
        raise ValueError("representations must be one-dimensional")
    scores = []
    for i, a in enumerate(arrays):
        for b in arrays[i + 1:]:
            denom = np.linalg.norm(a) * np.linalg.norm(b)
            scores.append(0.0 if denom == 0 else float(np.dot(a, b) / denom))
    return float(np.mean(scores))
