import numpy as np

from ceh.inference import bootstrap_mean_difference, paired_sign_flip


def test_bootstrap_operates_on_trajectory_deltas():
    result = bootstrap_mean_difference(
        np.array([0.10, 0.04, -0.01, 0.08, 0.03]),
        replicates=300,
        seed=2,
    )
    assert result.replicates == 300
    assert result.lower <= result.estimate <= result.upper


def test_sign_flip_returns_valid_p_value():
    result = paired_sign_flip(
        np.array([0.10, 0.08, 0.05, 0.02, 0.06]),
        replicates=500,
        seed=2,
    )
    assert 0.0 < result.p_value <= 1.0
    assert result.observed > 0


def test_rejects_nonfinite_values():
    try:
        paired_sign_flip(np.array([0.1, np.nan]))
    except ValueError:
        return
    raise AssertionError("expected non-finite validation failure")
