import numpy as np
from ceh.noise import gaussian, heavy_tailed, impulse_contaminated

def test_noise_reproducibility():
    assert np.array_equal(gaussian(20,seed=3),gaussian(20,seed=3))
    assert np.array_equal(heavy_tailed(20,seed=3),heavy_tailed(20,seed=3))

def test_impulse_contamination_preserves_shape():
    x=np.ones((10,2))
    assert impulse_contaminated(x,seed=3).shape==x.shape
