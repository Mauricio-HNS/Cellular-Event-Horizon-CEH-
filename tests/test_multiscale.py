import numpy as np

from ceh.multiscale import MultiscaleState, simulate_multiscale
from ceh.early_warning import rolling_autocorrelation, rolling_variance


def test_multiscale_perturbation_propagates_across_layers():
    perturbations = np.ones(100)
    states = simulate_multiscale(perturbations, dt=0.01)
    matrix = np.array([s.as_vector() for s in states])
    assert matrix[-1, 1] > 0
    assert matrix[-1, 3] > 0
    assert matrix[-1, 4] > 0


def test_early_warning_statistics_have_expected_lengths():
    values = np.linspace(0, 1, 30)
    assert rolling_variance(values, 10).shape == (21,)
    assert rolling_autocorrelation(values, 10).shape == (21,)
