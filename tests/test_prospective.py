import numpy as np
from ceh.prospective import extract_window, future_displacement

def test_prospective_features_do_not_include_future_rows():
    x = np.array([[0.0], [1.0], [2.0], [100.0]])
    result = extract_window(x, cutoff=2)
    assert result.features["final_drift"] == 2.0

def test_future_displacement_is_separate_target():
    x = np.array([[0.0], [1.0], [2.0], [100.0]])
    assert future_displacement(x, cutoff=2) == 98.0
