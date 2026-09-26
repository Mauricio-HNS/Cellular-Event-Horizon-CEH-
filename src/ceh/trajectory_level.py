"""Independent trajectory-level evaluation for prospective CEH benchmarks.

The unit of inference is one trajectory, not one cutoff. A trajectory receives
one prospective score computed from information available before its event.
No future observations are used in the score.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .metrics import auprc, auroc


@dataclass(frozen=True)
class TrajectoryScore:
    trajectory_id: int
    label: int
    score: float


@dataclass(frozen=True)
class TrajectoryLevelResult:
    auroc: float
    auprc: float
    scores: tuple[TrajectoryScore, ...]
    n_trajectories: int
    positives: int


def prospective_max_score(
    scores: np.ndarray,
    transition_time: int,
    *,
    horizon: int,
    window: int,
) -> float:
    """Return the maximum score in the pre-event window only.

    For a no-transition trajectory, all observed cutoffs are eligible negatives.
    """
    scores = np.asarray(scores, dtype=float)
    if scores.ndim != 1:
        raise ValueError("scores must be one-dimensional")
    if transition_time >= len(scores):
        return float(np.max(scores))
    start = max(0, transition_time - horizon)
    end = max(start + 1, transition_time - window)
    return float(np.max(scores[start:end]))


def evaluate_trajectory_level(
    trajectories: list[np.ndarray],
    transition_times: list[int],
    scorer,
    *,
    horizon: int = 30,
    window: int = 5,
) -> TrajectoryLevelResult:
    """Score each trajectory independently and evaluate event vs no-event."""
    if len(trajectories) != len(transition_times):
        raise ValueError("trajectory and transition_time lengths must match")
    if len(trajectories) < 2:
        raise ValueError("at least two trajectories are required")

    rows = []
    for idx, (trajectory, transition_time) in enumerate(
        zip(trajectories, transition_times)
    ):
        x = np.asarray(trajectory, dtype=float)
        if x.ndim != 2 or x.shape[0] < 2:
            raise ValueError("each trajectory must have shape (time, features)")
        cutoff_scores = np.asarray(scorer(x), dtype=float)
        if cutoff_scores.ndim != 1 or len(cutoff_scores) != len(x):
            raise ValueError("scorer must return one score per time point")
        label = int(transition_time < len(x))
        score = prospective_max_score(
            cutoff_scores,
            transition_time,
            horizon=horizon,
            window=window,
        )
        rows.append(TrajectoryScore(idx, label, score))

    labels = np.asarray([r.label for r in rows], dtype=int)
    values = np.asarray([r.score for r in rows], dtype=float)
    if len(np.unique(labels)) < 2:
        raise ValueError("trajectory-level AUROC requires both classes")

    return TrajectoryLevelResult(
        auroc=auroc(labels, values),
        auprc=auprc(labels, values),
        scores=tuple(rows),
        n_trajectories=len(rows),
        positives=int(labels.sum()),
    )
