import numpy as np

from ceh.convergence import convergence_index, pairwise_distance_matrix
from ceh.nulls import permute_trajectories


def test_pairwise_distance_matrix_is_symmetric():
    x = np.array([[0.0, 0.0], [3.0, 4.0], [0.0, 4.0]])
    d = pairwise_distance_matrix(x)
    assert np.allclose(d, d.T)
    assert np.allclose(np.diag(d), 0.0)


def test_convergence_increases_when_trajectories_contract():
    x = np.array([
        [[0.0], [0.0], [0.0]],
        [[2.0], [1.0], [0.1]],
        [[4.0], [2.0], [0.2]],
    ])
    score = convergence_index(x)
    assert score > 0.5


def test_permutation_preserves_shape_and_slice_distribution():
    x = np.arange(3 * 4 * 2, dtype=float).reshape(3, 4, 2)
    shuffled = permute_trajectories(x, seed=10)
    assert shuffled.shape == x.shape
    for t in range(x.shape[1]):
        assert np.allclose(np.sort(x[:, t], axis=0), np.sort(shuffled[:, t], axis=0))
