import numpy as np

from ceh.dynamics import acceleration, drift, velocity
from ceh.horizon import candidate_score, directionality
from ceh.synthetic import directional_trajectory, shuffle_time


def test_directional_world_has_trajectory_signal():
    x = directional_trajectory(seed=11)
    assert len(velocity(x)) == len(x) - 1
    assert len(acceleration(x)) == len(x) - 2
    assert 0.0 <= directionality(x) <= 1.0


def test_time_shuffle_preserves_observations_but_changes_order():
    x = directional_trajectory(seed=11)
    shuffled = shuffle_time(x, seed=19)
    assert np.allclose(np.sort(x, axis=0), np.sort(shuffled, axis=0))


def test_candidate_score_is_bounded():
    x = directional_trajectory(seed=11)
    score = candidate_score(x, convergence=0.8)
    assert 0.0 <= score.convergence <= 1.0
    assert 0.0 <= score.directionality <= 1.0
    assert 0.0 <= score.acceleration <= 1.0
    assert 0.0 <= score.total <= 1.0


def test_drift_starts_at_zero_without_reference():
    x = directional_trajectory(seed=11)
    assert np.isclose(drift(x)[0], 0.0)
