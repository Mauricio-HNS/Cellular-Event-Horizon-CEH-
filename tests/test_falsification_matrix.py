from ceh.falsification_matrix import assemble, summarize


def test_matrix_preserves_missing_evidence():
    rows = assemble(
        [
            {
                "method": "ceh",
                "scenario": "matched",
                "mechanism": "matched_no_transition",
                "auroc": None,
                "auprc": None,
                "delta_auroc": None,
                "n": 12,
                "positives": 0,
            }
        ],
        experiment="023",
    )
    assert rows[0].auroc is None
    assert rows[0].delta_auroc is None


def test_summary_separates_null_and_transition_rows():
    rows = assemble(
        [
            {
                "method": "ceh",
                "mechanism": "matched_no_transition",
                "auroc": 0.51,
                "auprc": 0.50,
                "delta_auroc": 0.01,
                "n": 24,
                "positives": 0,
            },
            {
                "method": "ceh",
                "mechanism": "synthetic_transition",
                "auroc": 0.72,
                "auprc": 0.70,
                "delta_auroc": 0.08,
                "n": 24,
                "positives": 12,
            },
        ],
        experiment="023",
    )
    summary = summarize(rows)
    assert summary.n_rows == 2
    assert summary.null_rows == 1
    assert summary.transition_rows == 1
    assert summary.median_delta_auroc == 0.045
