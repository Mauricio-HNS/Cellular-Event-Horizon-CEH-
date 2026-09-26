import pytest
from ceh.evidence import build_snapshot, score_from_rows

def test_score_from_rows_uses_documented_rows():
    rows=[
        {"method":"ceh","delta_auroc":0.10},
        {"method":"ceh","delta_auroc":0.00},
        {"method":"ceh","delta_auroc":-0.02},
    ]
    scores=score_from_rows(rows)
    assert scores["robustness"] == pytest.approx(2/3)
    assert scores["incremental_information"] == pytest.approx(0.5533333333)

def test_missing_null_evidence_is_not_fabricated():
    scores=score_from_rows([{"method":"ceh","delta_auroc":0.05}])
    assert scores["null_resistance"] is None

def test_build_snapshot_has_all_dimensions():
    snapshot=build_snapshot("2026-09-26T00:00:00Z", evidence={
        "robustness":.8,"incremental_information":.6,
        "null_resistance":.5,"generalization":.4,
        "statistical_strength":.3,"reproducibility":.2,
        "novelty":.1,"biological_validation":0.0})
    assert set(snapshot.dimensions)=={
        "robustness","incremental_information","null_resistance",
        "generalization","statistical_strength","reproducibility",
        "novelty","biological_validation"}

def test_invalid_dimension_is_rejected():
    with pytest.raises(ValueError):
        build_snapshot("now", evidence={"robustness":2.0})
