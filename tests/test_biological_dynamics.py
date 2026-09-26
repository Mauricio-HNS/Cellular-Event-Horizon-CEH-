import numpy as np
import pytest

from ceh.state import BiologicalState
from ceh.perturbation import transition_step
from ceh.multimodal import concatenate_modalities, modality_agreement

def test_state_is_explicit_and_one_dimensional():
    state = BiologicalState(np.array([1.0, 2.0]), modality="imaging")
    assert state.dimension == 2
    assert state.modality == "imaging"

def test_state_rejects_matrix():
    with pytest.raises(ValueError):
        BiologicalState(np.ones((2, 2)))

def test_transition_step_preserves_shape():
    out = transition_step(
        np.array([1.0, 2.0]),
        np.array([0.1]),
        np.array([0.2, 0.3]),
        lambda x, e, u: x + u,
    )
    np.testing.assert_allclose(out, [1.2, 2.3])

def test_modalities_are_explicitly_composed():
    out = concatenate_modalities(np.array([1, 2]), np.array([3, 4, 5]))
    np.testing.assert_array_equal(out, [1, 2, 3, 4, 5])

def test_agreement_is_bounded():
    score = modality_agreement(np.array([1.0, 0.0]), np.array([0.8, 0.2]))
    assert -1.0 <= score <= 1.0
