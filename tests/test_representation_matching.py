import numpy as np

from ceh.representation_matching import geometry_signature, match_controls


def test_geometry_signature_is_finite():
    x = np.cumsum(np.ones((20, 3)), axis=0)
    s = geometry_signature(x)
    assert s.shape == (3,)
    assert np.all(np.isfinite(s))


def test_matching_is_reproducible_and_size_preserving():
    target = [np.cumsum(np.random.default_rng(i).normal(size=(20, 3)), axis=0) for i in range(4)]
    pool = [np.cumsum(np.random.default_rng(100 + i).normal(size=(20, 3)), axis=0) for i in range(12)]
    a = match_controls(target, pool)
    b = match_controls(target, pool)
    assert len(a) == len(target)
    assert all(x.shape == target[0].shape for x in a)
    assert all(np.array_equal(x, y) for x, y in zip(a, b))
