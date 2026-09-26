import numpy as np

from ceh.joint_incremental import joint_incremental_evaluate
from ceh.synthetic import directional_trajectory, null_trajectory


def make_dataset(n_transition=12, n_null=12):
    trajectories = [
        directional_trajectory(60, 4, 35, 0.03, 100 + i)
        for i in range(n_transition)
    ]
    trajectories += [
        null_trajectory(60, 4, 0.12, 1000 + i)
        for i in range(n_null)
    ]
    return trajectories, [35] * n_transition + [10_000] * n_null


def test_joint_incremental_uses_trajectory_split():
    trajectories, transition_times = make_dataset()
    result = joint_incremental_evaluate(
        trajectories, transition_times, horizon=30, window=5, train_fraction=0.6
    )
    assert result.train_trajectories + result.test_trajectories == len(trajectories)
    assert result.test_trajectories >= 3
    assert result.test_cutoffs > 0
    assert result.positives > 0
    assert np.isfinite(result.delta_auroc)


def test_joint_incremental_requires_enough_trajectories():
    trajectories, transition_times = make_dataset(3, 2)
    try:
        joint_incremental_evaluate(trajectories, transition_times)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
