from ceh.experiment_planner import make_primary_incremental_spec, to_json


def test_primary_spec_is_falsifiable_and_grouped():
    spec = make_primary_incremental_spec()
    assert spec.experiment_id == "022_joint_incremental_protocol"
    assert spec.evaluation_unit == "trajectory"
    assert "joint_baseline" in spec.comparators
    assert spec.falsification_criteria
    assert "trajectory" in spec.statistical_test


def test_primary_spec_serializes():
    spec = make_primary_incremental_spec(horizon=20, window=5)
    payload = to_json(spec)
    assert "022_joint_incremental_protocol" in payload
    assert "I(Y; Z_CEH | Z_base) > 0" in payload


def test_invalid_horizon():
    try:
        make_primary_incremental_spec(horizon=5, window=5)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
