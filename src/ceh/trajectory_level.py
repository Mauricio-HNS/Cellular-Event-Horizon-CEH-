"""Independent trajectory-level evaluation for prospective CEH benchmarks.

No-transition controls must use explicit pseudo-event times so positives and
controls are scored under the same pre-event window rule.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .metrics import auprc, auroc
from .pseudo_event import aggregate_pseudo_event_scores

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

def prospective_window_score(scores, evaluation_time: int, *, horizon: int, window: int) -> float:
    values = np.asarray(scores, dtype=float)
    if values.ndim != 1 or evaluation_time < 1:
        raise ValueError("scores must be one-dimensional and evaluation_time positive")
    start = max(0, evaluation_time - horizon)
    end = min(max(start + 1, evaluation_time - window), len(values))
    if start >= len(values):
        start = len(values) - 1
    return float(np.max(values[start:end]))

def prospective_max_score(scores, transition_time: int, *, horizon: int, window: int) -> float:
    return prospective_window_score(scores, transition_time, horizon=horizon, window=window)

def evaluate_trajectory_level(trajectories, transition_times, scorer, *, horizon: int = 30, window: int = 5, pseudo_event_times=None) -> TrajectoryLevelResult:
    if len(trajectories) != len(transition_times):
        raise ValueError("trajectory and transition_time lengths must match")
    if len(trajectories) < 2:
        raise ValueError("at least two trajectories are required")
    no_event = [i for i, t in enumerate(transition_times) if t >= len(trajectories[i])]
    pseudo = None if pseudo_event_times is None else np.asarray(pseudo_event_times, dtype=int)
    if no_event and (pseudo is None or pseudo.ndim != 2 or pseudo.shape[1] != len(no_event)):
        raise ValueError("pseudo_event_times must have shape (replicates, n_no_event)")
    rows = []
    cursor = 0
    for idx, (trajectory, transition_time) in enumerate(zip(trajectories, transition_times)):
        x = np.asarray(trajectory, dtype=float)
        if x.ndim != 2 or x.shape[0] < 2:
            raise ValueError("each trajectory must have shape (time, features)")
        cutoff_scores = np.asarray(scorer(x), dtype=float)
        if cutoff_scores.ndim != 1 or len(cutoff_scores) != len(x):
            raise ValueError("scorer must return one score per time point")
        label = int(transition_time < len(x))
        score = prospective_window_score(cutoff_scores, transition_time, horizon=horizon, window=window) if label else aggregate_pseudo_event_scores(cutoff_scores, pseudo[:, cursor], horizon=horizon, window=window)
        if not label:
            cursor += 1
        rows.append(TrajectoryScore(idx, label, score))
    labels = np.asarray([r.label for r in rows], dtype=int)
    values = np.asarray([r.score for r in rows], dtype=float)
    if len(np.unique(labels)) < 2:
        raise ValueError("trajectory-level AUROC requires both classes")
    return TrajectoryLevelResult(auroc=auroc(values, labels), auprc=auprc(values, labels), scores=tuple(rows), n_trajectories=len(rows), positives=int(labels.sum()))
