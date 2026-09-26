import numpy as np

from ceh.joint_trajectory_level import evaluate_joint_trajectory_level


def norm(x):
    return np.linalg.norm(x, axis=1)


def temporal(x):
    return np.r_[0.0, np.linalg.norm(np.diff(x, axis=0), axis=1)]


def early(x):
    return np.r_[0.0, np.var(x, axis=1)]


def ceh(x):
    v = temporal(x)
    return np.r_[0.0, np.diff(v)]


def test_joint_evaluation_is_trajectory_level():
    rng = np.random.default_rng(21)
    trajectories = []
    times = []
    for i in range(12):
        x = rng.normal(0, 0.05, size=(50, 3))
        if i < 6:
            x[32:] += np.linspace(0, 2, 18)[:, None]
            times.append(32)
        else:
            times.append(10_000)
        trajectories.append(x)

    result = evaluate_joint_trajectory_level(
        trajectories,
        times,
        snapshot_scorer=norm,
        temporal_scorer=temporal,
        early_warning_scorer=early,
        ceh_scorer=ceh,
        seed=4,
    )

    assert result.n_trajectories >= 2
    assert result.positives > 0
    assert np.isfinite(result.delta_auroc)
    assert np.isfinite(result.delta_auprc)


def test_requires_both_classes():
    rng = np.random.default_rng(3)
    trajectories = [rng.normal(size=(20, 2)) for _ in range(6)]
    try:
        evaluate_joint_trajectory_level(
            trajectories, [10_000] * 6,
            snapshot_scorer=norm,
            temporal_scorer=temporal,
            early_warning_scorer=early,
            ceh_scorer=ceh,
        )
    except ValueError:
        return
    raise AssertionError("expected class validation failure")
