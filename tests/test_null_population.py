import numpy as np

from ceh.null_population import matched_directional_population, matched_no_transition


def test_matched_populations_have_same_shape():
    transitions, times = matched_directional_population(6, 40, 3, 24)
    nulls = matched_no_transition(6, 40, 3)
    assert len(transitions) == len(nulls)
    assert transitions[0].shape == nulls[0].shape == (40, 3)
    assert times == [24] * 6


def test_null_population_has_no_intended_event():
    nulls = matched_no_transition(8, 50, 4, seed=11)
    assert len(nulls) == 8
    assert all(np.isfinite(x).all() for x in nulls)
    assert np.asarray(nulls).shape == (8, 50, 4)
