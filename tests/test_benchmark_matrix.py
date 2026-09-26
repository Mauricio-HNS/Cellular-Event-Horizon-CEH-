import numpy as np

from ceh.benchmark_matrix import apply_missingness, embed_dimension, modality_view


def test_embedding_has_requested_dimension():
    x = np.arange(20, dtype=float)[:, None]
    assert embed_dimension(x, 4, seed=2).shape == (20, 4)


def test_missingness_preserves_shape_and_finiteness():
    x = np.ones((20, 3))
    y = apply_missingness(x, 0.3, seed=4)
    assert y.shape == x.shape
    assert np.isfinite(y).all()


def test_modalities_preserve_shape():
    x = np.ones((20, 4))
    for modality in ("state", "scaled", "noisy", "heavy_tail"):
        assert modality_view(x, modality, seed=3).shape == x.shape
