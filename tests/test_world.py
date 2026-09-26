import numpy as np
from ceh.world import WorldConfig, generate_world
from ceh.observations import observe

def test_world_is_reproducible():
    a = generate_world(WorldConfig(seed=11))
    b = generate_world(WorldConfig(seed=11))
    np.testing.assert_allclose(a.states, b.states)
    assert a.transition_time == b.transition_time

def test_world_has_known_transition_boundary():
    world = generate_world(WorldConfig(steps=20))
    assert world.transition_time == 10
    assert world.perturbation_time == 6

def test_observation_noise_and_missingness():
    world = generate_world(WorldConfig(seed=3))
    observed = observe(world.states, noise=0.1, missing_rate=0.2, seed=4)
    assert observed.shape == world.states.shape
    assert np.isnan(observed).any()
