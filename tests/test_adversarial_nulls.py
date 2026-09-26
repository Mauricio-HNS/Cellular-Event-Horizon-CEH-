import numpy as np

from ceh.adversarial_nulls import (
    convergence_without_transition,
    matched_directional_noise,
    matched_geometry_population,
)


def test_directional_null_is_reproducible():
    a = matched_directional_noise(seed=11)
    b = matched_directional_noise(seed=11)
    assert np.allclose(a[0], b[0])


def test_convergence_null_has_expected_shape():
    trajectories = convergence_without_transition(
        n_trajectories=5, n_steps=20, n_features=3
    )
    assert len(trajectories) == 5
    assert trajectories[0].shape == (20, 3)


def test_geometry_population_preserves_population_size():
    trajectories = matched_geometry_population(
        n_trajectories=7, n_steps=20, n_features=3
    )
    assert len(trajectories) == 7
    assert all(np.isfinite(x).all() for x in trajectories)
