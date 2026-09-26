import numpy as np
from ceh.baselines import snapshot_signal, temporal_signal, ceh_signal
from ceh.statistics import bootstrap_mean

def test_baselines_are_finite():
    x = np.cumsum(np.ones((12, 3)), axis=0)
    assert np.isfinite(snapshot_signal(x, 8))
    assert np.isfinite(temporal_signal(x, 8))
    assert np.isfinite(ceh_signal(x, 8))

def test_bootstrap_interval_is_ordered():
    lo, hi = bootstrap_mean(np.arange(10.0), iterations=100, seed=2)
    assert lo <= hi
    assert np.isfinite(lo) and np.isfinite(hi)
