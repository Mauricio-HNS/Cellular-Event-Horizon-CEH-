import numpy as np
from ceh.null_benchmark import maximum_horizon_score, calibrate_against_time_null
from ceh.detection_metrics import lead_time, within_window

def test_null_calibration_is_reproducible():
    x = np.cumsum(np.ones((20, 3)), axis=0)
    a = calibrate_against_time_null(x, window=4, permutations=20, seed=3)
    b = calibrate_against_time_null(x, window=4, permutations=20, seed=3)
    np.testing.assert_allclose(a.null_scores, b.null_scores)
    assert a.empirical_p >= 0.0 and a.empirical_p <= 1.0

def test_detection_metrics():
    assert lead_time(7, 10) == 3
    assert within_window(9, 10, 1)
    assert not within_window(7, 10, 1)
