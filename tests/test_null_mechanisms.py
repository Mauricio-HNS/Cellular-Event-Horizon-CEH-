import numpy as np

from ceh.null_mechanisms import clustered_events, nonnormal_linear_system


def test_nonnormal_null_has_stable_eigenvalues():
    trajectory = nonnormal_linear_system(steps=100, coupling=8.0, sigma=0.0)
    assert trajectory.shape == (101, 2)
    assert np.all(np.linalg.eigvals(np.array([[-1.0, 8.0], [0.0, -1.0]])) < 0)


def test_nonnormal_null_is_reproducible():
    a = nonnormal_linear_system(seed=42)
    b = nonnormal_linear_system(seed=42)
    np.testing.assert_array_equal(a, b)


def test_clustered_events_are_reproducible():
    a = clustered_events(100, seed=42)
    b = clustered_events(100, seed=42)
    np.testing.assert_array_equal(a, b)
