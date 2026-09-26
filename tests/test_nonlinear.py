import numpy as np

from ceh.bifurcation import sweep_saddle_node
from ceh.nonlinear import SaddleNode, euler_maruyama


def test_saddle_node_fixed_points_and_stability():
    system = SaddleNode(1.0)
    assert set(np.round(system.fixed_points(), 8)) == {-1.0, 1.0}
    assert system.stable_fixed_points() == (1.0,)
    assert system.unstable_fixed_points() == (-1.0,)


def test_saddle_node_has_no_fixed_point_below_bifurcation():
    assert SaddleNode(-0.1).fixed_points() == ()


def test_stochastic_simulation_is_reproducible():
    a = euler_maruyama(SaddleNode(0.5), 0.6, 0.001, 100, sigma=0.1, seed=42)
    b = euler_maruyama(SaddleNode(0.5), 0.6, 0.001, 100, sigma=0.1, seed=42)
    np.testing.assert_array_equal(a, b)


def test_bifurcation_sweep():
    result = sweep_saddle_node(np.array([-1.0, 0.0, 1.0]))
    assert np.isnan(result["stable"][0])
    assert np.isnan(result["unstable"][0])
    assert result["stable"][2] == 1.0
    assert result["unstable"][2] == -1.0
