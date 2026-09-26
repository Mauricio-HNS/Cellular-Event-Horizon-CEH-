import numpy as np

from ceh.inference import paired_auc_bootstrap, paired_auc_permutation
from ceh.multiplicity import primary_endpoint_gate


def test_paired_auc_inference_runs():
    labels = np.array([0, 0, 0, 1, 1, 1, 0, 1])
    baseline = np.array([0.1, 0.2, 0.3, 0.45, 0.5, 0.55, 0.25, 0.6])
    full = np.array([0.1, 0.2, 0.25, 0.7, 0.8, 0.75, 0.3, 0.9])

    ci = paired_auc_bootstrap(labels, baseline, full, replicates=200)
    perm = paired_auc_permutation(labels, baseline, full, replicates=200)

    assert ci.lower <= ci.estimate <= ci.upper
    assert 0 <= perm.p_value <= 1


def test_primary_gate_requires_positive_lower_bound():
    assert primary_endpoint_gate(
        p_value=0.01,
        effect=0.2,
        ci_lower=0.05,
    )
    assert not primary_endpoint_gate(
        p_value=0.01,
        effect=0.2,
        ci_lower=-0.01,
    )
