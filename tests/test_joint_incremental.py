import numpy as np

from ceh.joint_incremental import joint_incremental_evaluate
from experiments_022_helper import make_dataset


def test_joint_incremental_uses_trajectory_split():
    trajectories, transition_times = make_dataset()
    result = joint_incremental_evaluate(
        trajectories,
        transition_times,
        horizon=30,
        window=5,
        train_fraction=0.6,
    )
    assert result.train_trajectories + result.test_trajectories == len(trajectories)
    assert result.test_trajectories >= 3
    assert result.test_cutoffs > 0
    assert result.positives > 0
    assert np.isfinite(result.delta_auroc)


def test_joint_incremental_requires_enough_trajectories():
    trajectories, transition_times = make_dataset(n_transition=3, n_null=2)
    try:
        joint_incremental_evaluate(trajectories, transition_times)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
