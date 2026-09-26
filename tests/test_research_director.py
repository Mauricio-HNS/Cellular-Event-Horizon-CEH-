from ceh.falsification_matrix import assemble
from ceh.research_director import build_plan


def test_director_does_not_turn_missing_evidence_into_failure():
    rows = assemble(
        [
            {
                "method": "ceh",
                "mechanism": "matched_no_transition",
                "auroc": 0.51,
                "auprc": 0.50,
                "delta_auroc": None,
                "n": 20,
                "positives": 0,
            },
            {
                "method": "ceh",
                "mechanism": "synthetic_transition",
                "auroc": 0.72,
                "auprc": 0.70,
                "delta_auroc": 0.08,
                "n": 20,
                "positives": 10,
            },
        ],
        experiment="test",
    )
    plan = build_plan(rows, evidence_rows=[
        {"method": "ceh", "mechanism": "synthetic_transition", "delta_auroc": 0.08}
    ])
    assert "biological_validation" in plan.unavailable_dimensions
    assert any("biological validation" in x.lower() for x in plan.critical_weaknesses)


def test_director_prioritizes_null_and_incremental_gaps():
    rows = assemble(
        [
            {
                "method": "ceh",
                "mechanism": "synthetic_transition",
                "auroc": 0.72,
                "auprc": 0.70,
                "delta_auroc": 0.08,
                "n": 20,
                "positives": 10,
            }
        ],
        experiment="test",
    )
    plan = build_plan(rows)
    assert plan.actions[0].priority == 1
    assert "null" in plan.actions[0].action.lower()
