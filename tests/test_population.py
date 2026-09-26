import numpy as np
from ceh.population import PopulationWorldConfig, generate_population
from ceh.attractors import convergence_over_time
from ceh.modalities import independent_modalities

def test_population_shape_and_reproducibility():
    config = PopulationWorldConfig(entities=8, dimensions=3, steps=30, seed=9)
    a = generate_population(config)
    b = generate_population(config)
    assert a.states.shape == (30, 8, 3)
    np.testing.assert_allclose(a.states, b.states)
    assert a.transition_time == b.transition_time

def test_convergence_is_time_resolved():
    world = generate_population(PopulationWorldConfig(entities=6, steps=25))
    values = convergence_over_time(world.states)
    assert values.shape == (25,)
    assert np.isfinite(values).all()

def test_independent_modalities_have_expected_shape():
    world = generate_population(PopulationWorldConfig(entities=5, dimensions=4, steps=20))
    a, b = independent_modalities(world.states, outputs=2)
    assert a.shape == (20, 5, 2)
    assert b.shape == (20, 5, 2)
