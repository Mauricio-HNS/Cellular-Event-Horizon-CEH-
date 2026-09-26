"""Joint incremental-information evaluation at the trajectory level.

The primary CEH challenge is whether CEH adds held-out information after
snapshot, temporal, and early-warning signals are modeled together.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .benchmark import score_at_cutoff
from .metrics import auprc, auroc


@dataclass(frozen=True)
class JointIncrementalResult:
    candidate: str
    baseline_methods: tuple[str, ...]
    train_trajectories: int
    test_trajectories: int
    test_cutoffs: int
    positives: int
    baseline_auroc: float
    full_auroc: float
    delta_auroc: float
    baseline_auprc: float
    full_auprc: float
    delta_auprc: float


def _zfit(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = np.mean(x, axis=0)
    std = np.maximum(np.std(x, axis=0), 1e-12)
    return mean, std


def _features(states, cutoff, methods, window):
    values = [score_at_cutoff(states, cutoff, m, window) for m in methods]
    return np.asarray(values, dtype=float)


def _collect(
    trajectories,
    transition_times,
    methods,
    horizon,
    window,
):
    rows = []
    for trajectory, t0 in zip(trajectories, transition_times):
        for cutoff in range(max(window + 2, 1), len(trajectory)):
            values = _features(trajectory, cutoff, methods, window)
            if not np.all(np.isfinite(values)):
                continue
            label = int(0 < t0 - cutoff <= horizon)
            rows.append((values, label))
    if not rows:
        return np.empty((0, len(methods))), np.empty(0, dtype=int)
    return (
        np.vstack([r[0] for r in rows]),
        np.asarray([r[1] for r in rows], dtype=int),
    )


def _linear_score(train_x, train_y, test_x):
    mean, std = _zfit(train_x)
    z_train = (train_x - mean) / std
    z_test = (test_x - mean) / std
    design = np.column_stack([np.ones(len(z_train)), z_train])
    beta = np.linalg.lstsq(design, train_y.astype(float), rcond=None)[0]
    return design @ beta, np.column_stack([np.ones(len(z_test)), z_test]) @ beta


def joint_incremental_evaluate(
    trajectories,
    transition_times,
    *,
    candidate="ceh",
    baseline_methods=("snapshot", "temporal", "early_warning"),
    horizon=30,
    window=5,
    train_fraction=0.6,
):
    """Evaluate candidate information beyond a jointly fitted baseline.

    Splitting is by trajectory. Feature normalization and model fitting use only
    training trajectories. Test trajectories are never used for fitting.
    """

    trajectories = list(trajectories)
    transition_times = list(transition_times)
    if len(trajectories) != len(transition_times):
        raise ValueError("trajectory/transition lengths differ")
    if len(trajectories) < 6:
        raise ValueError("at least six trajectories are required")
    if not 0.5 <= train_fraction < 1:
        raise ValueError("train_fraction must be in [0.5, 1)")

    split = max(3, int(len(trajectories) * train_fraction))
    split = min(split, len(trajectories) - 3)

    train_traj = trajectories[:split]
    train_t = transition_times[:split]
    test_traj = trajectories[split:]
    test_t = transition_times[split:]

    base = tuple(baseline_methods)
    train_b, train_y = _collect(train_traj, train_t, base, horizon, window)
    test_b, test_y = _collect(test_traj, test_t, base, horizon, window)

    full_methods = base + (candidate,)
    train_f, _ = _collect(train_traj, train_t, full_methods, horizon, window)
    test_f, _ = _collect(test_traj, test_t, full_methods, horizon, window)

    if len(test_y) < 2 or len(np.unique(test_y)) < 2:
        raise ValueError("test set must contain both classes")

    _, base_pred = _linear_score(train_b, train_y, test_b)
    _, full_pred = _linear_score(train_f, train_y, test_f)

    return JointIncrementalResult(
        candidate=candidate,
        baseline_methods=base,
        train_trajectories=len(train_traj),
        test_trajectories=len(test_traj),
        test_cutoffs=len(test_y),
        positives=int(test_y.sum()),
        baseline_auroc=float(auroc(base_pred[:, 0], test_y)),
        full_auroc=float(auroc(full_pred[:, 0], test_y)),
        delta_auroc=float(auroc(full_pred[:, 0], test_y) - auroc(base_pred[:, 0], test_y)),
        baseline_auprc=float(auprc(base_pred[:, 0], test_y)),
        full_auprc=float(auprc(full_pred[:, 0], test_y)),
        delta_auprc=float(auprc(full_pred[:, 0], test_y) - auprc(base_pred[:, 0], test_y)),
    )
