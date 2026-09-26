from experiments._026_adversarial_geometry_null import run


def test_formal_adversarial_run_has_all_null_scenarios():
    rows = run(seed=7, replicates=50)
    assert {row["name"] for row in rows} == {
        "direction_only",
        "convergence_only",
        "geometry_matched",
    }
    for row in rows:
        assert row["endpoint"] == "trajectory_level_incremental_delta_auroc"
        assert row["test_trajectories"] > 0
        assert 0.0 <= row["p_value"] <= 1.0
        assert 0.0 <= row["q_value"] <= 1.0
