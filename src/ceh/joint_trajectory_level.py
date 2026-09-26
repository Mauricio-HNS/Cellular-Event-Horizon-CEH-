"""Trajectory-level joint incremental evaluation.

Primary question: does CEH add prospective information beyond snapshot,
temporal and early-warning representations when each trajectory is one
independent unit of inference?
"""
from dataclasses import dataclass
import numpy as np

from .metrics import auprc, auroc
from .trajectory_level import prospective_max_score


@dataclass(frozen=True)
class JointTrajectoryResult:
    baseline_auroc: float
    baseline_auprc: float
    full_auroc: float
    full_auprc: float
    delta_auroc: float
    delta_auprc: float
    n_trajectories: int
    positives: int
    test_labels: tuple[int, ...]
    baseline_scores: tuple[float, ...]
    full_scores: tuple[float, ...]


def _feature_vector(x: np.ndarray, scorer, transition_time: int, horizon: int, window: int) -> float:
    scores = np.asarray(scorer(x), dtype=float)
    return prospective_max_score(scores, transition_time, horizon=horizon, window=window)


def _standardize(train: np.ndarray, test: np.ndarray):
    mean = train.mean(axis=0)
    scale = train.std(axis=0)
    scale = np.where(scale < 1e-12, 1.0, scale)
    return (train - mean) / scale, (test - mean) / scale


def _fit_linear(train_x, train_y):
    design = np.column_stack([np.ones(len(train_x)), train_x])
    return np.linalg.lstsq(design, train_y, rcond=None)[0]


def _predict(beta, x):
    return np.column_stack([np.ones(len(x)), x]) @ beta


def evaluate_joint_trajectory_level(
    trajectories: list[np.ndarray],
    transition_times: list[int],
    *,
    snapshot_scorer,
    temporal_scorer,
    early_warning_scorer,
    ceh_scorer,
    train_fraction: float = 0.6,
    horizon: int = 30,
    window: int = 5,
    seed: int = 7,
) -> JointTrajectoryResult:
    if len(trajectories) != len(transition_times):
        raise ValueError("trajectory and transition_time lengths must match")
    if len(trajectories) < 6:
        raise ValueError("at least six trajectories are required")
    if not 0.5 <= train_fraction < 1.0:
        raise ValueError("train_fraction must be in [0.5, 1)")

    features = []
    labels = []
    for x, transition_time in zip(trajectories, transition_times):
        x = np.asarray(x, dtype=float)
        if x.ndim != 2 or x.shape[0] < 2:
            raise ValueError("each trajectory must have shape (time, features)")
        base = [
            _feature_vector(x, snapshot_scorer, transition_time, horizon, window),
            _feature_vector(x, temporal_scorer, transition_time, horizon, window),
            _feature_vector(x, early_warning_scorer, transition_time, horizon, window),
        ]
        ceh = _feature_vector(x, ceh_scorer, transition_time, horizon, window)
        features.append(base + [ceh])
        labels.append(int(transition_time < len(x)))

    features = np.asarray(features, dtype=float)
    labels = np.asarray(labels, dtype=int)
    if len(np.unique(labels)) < 2:
        raise ValueError("both transition and no-transition trajectories are required")

    rng = np.random.default_rng(seed)
    # Stratify the trajectory split so the held-out set contains both classes.
    class_indices = [np.flatnonzero(labels == cls) for cls in (0, 1)]
    train_parts = []
    test_parts = []
    for idx in class_indices:
        shuffled = rng.permutation(idx)
        n_train = max(1, int(len(shuffled) * train_fraction))
        n_train = min(n_train, len(shuffled) - 1)
        train_parts.append(shuffled[:n_train])
        test_parts.append(shuffled[n_train:])
    train_idx = np.concatenate(train_parts)
    test_idx = np.concatenate(test_parts)
    train_idx = rng.permutation(train_idx)
    test_idx = rng.permutation(test_idx)
    if len(np.unique(labels[test_idx])) < 2:
        raise ValueError("test split must contain both trajectory classes")

    train_base, test_base = _standardize(features[train_idx, :3], features[test_idx, :3])
    train_full, test_full = _standardize(features[train_idx], features[test_idx])

    beta_base = _fit_linear(train_base, labels[train_idx])
    beta_full = _fit_linear(train_full, labels[train_idx])

    base_score = _predict(beta_base, test_base)
    full_score = _predict(beta_full, test_full)
    y = labels[test_idx]

    base_auc = auroc(base_score, y)
    full_auc = auroc(full_score, y)
    base_ap = auprc(base_score, y)
    full_ap = auprc(full_score, y)

    return JointTrajectoryResult(
        baseline_auroc=base_auc,
        baseline_auprc=base_ap,
        full_auroc=full_auc,
        full_auprc=full_ap,
        delta_auroc=full_auc - base_auc,
        delta_auprc=full_ap - base_ap,
        n_trajectories=len(test_idx),
        positives=int(y.sum()),
        test_labels=tuple(int(v) for v in y),
        baseline_scores=tuple(float(v) for v in base_score),
        full_scores=tuple(float(v) for v in full_score),
    )
