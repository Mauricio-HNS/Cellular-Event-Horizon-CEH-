"""Prospective pseudo-event controls for symmetric trajectory evaluation.

Pseudo-event times are sampled from the empirical event-time distribution and
used to score no-transition trajectories under exactly the same pre-event
window rule as transitioning trajectories.
"""
from __future__ import annotations

import numpy as np


def sample_pseudo_event_times(
    event_times,
    n_controls: int,
    *,
    replicates: int = 1000,
    seed: int = 7,
) -> np.ndarray:
    times = np.asarray(event_times, dtype=int)
    if times.ndim != 1 or len(times) == 0:
        raise ValueError("event_times must be a non-empty one-dimensional array")
    if np.any(times < 1):
        raise ValueError("event_times must be positive")
    if n_controls < 1 or replicates < 1:
        raise ValueError("n_controls and replicates must be positive")
    rng = np.random.default_rng(seed)
    return rng.choice(times, size=(replicates, n_controls), replace=True)


def aggregate_pseudo_event_scores(
    scores,
    pseudo_event_times,
    *,
    horizon: int,
    window: int,
) -> float:
    times = np.asarray(pseudo_event_times, dtype=int)
    if times.ndim != 1 or len(times) == 0:
        raise ValueError("pseudo_event_times must be a non-empty one-dimensional array")
    values = [
        _window_score(scores, int(t), horizon=horizon, window=window)
        for t in times
    ]
    return float(np.median(values))


def _window_score(scores, evaluation_time: int, *, horizon: int, window: int) -> float:
    values = np.asarray(scores, dtype=float)
    if values.ndim != 1 or len(values) < 2:
        raise ValueError("scores must be one-dimensional with at least two values")
    if evaluation_time < 1 or evaluation_time > len(values):
        raise ValueError("evaluation_time must lie within the observed trajectory")
    if horizon < 1 or window < 1 or window >= horizon:
        raise ValueError("require horizon > window >= 1")
    end = min(evaluation_time - window, len(values))
    start = max(0, evaluation_time - horizon)
    if end <= start:
        raise ValueError("pseudo-event does not leave a valid pre-event window")
    return float(np.max(values[start:end]))
