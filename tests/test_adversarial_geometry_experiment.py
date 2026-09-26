import importlib.util
from pathlib import Path


def _load_experiment():
    path = Path(__file__).parents[1] / "experiments" / "026_adversarial_geometry_null.py"
    spec = importlib.util.spec_from_file_location("ceh_experiment_026", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_formal_adversarial_run_has_all_null_scenarios():
    rows = _load_experiment().run(seed=7, replicates=50)
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
