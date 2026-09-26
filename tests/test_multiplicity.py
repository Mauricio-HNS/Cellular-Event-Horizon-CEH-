from ceh.multiplicity import benjamini_hochberg, primary_endpoint_gate


def test_bh_returns_q_values_in_range():
    result = benjamini_hochberg([0.001, 0.02, 0.20, 0.8], alpha=0.05)
    assert len(result.q_values) == 4
    assert all(0 <= q <= 1 for q in result.q_values)
    assert result.rejected[0]


def test_primary_endpoint_requires_positive_effect_and_ci():
    assert primary_endpoint_gate(
        p_value=0.01, effect=0.08, ci_lower=0.02, q_value=0.03
    )
    assert not primary_endpoint_gate(
        p_value=0.01, effect=0.08, ci_lower=-0.01, q_value=0.03
    )


def test_primary_endpoint_rejects_non_significant_q_value():
    assert not primary_endpoint_gate(
        p_value=0.01, effect=0.08, ci_lower=0.02, q_value=0.20
    )
