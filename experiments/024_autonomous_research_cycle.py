"""Experiment 024: autonomous evidence -> falsification -> research cycle.

This script turns existing verified benchmark rows into an auditable research
plan. It does not invent benchmark results and does not claim biological validity.
"""
from __future__ import annotations

import json
from pathlib import Path

from ceh.falsification_matrix import assemble
from ceh.research_director import build_plan, write_plan


def load_rows(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def run(
    matrix_path: str = "artifacts/falsification-matrix.json",
    output_path: str = "artifacts/autonomous-research-plan.json",
):
    raw = load_rows(matrix_path)
    rows = assemble(raw, experiment="aggregated")
    plan = build_plan(rows, evidence_rows=raw)
    write_plan(output_path, plan)
    return plan


if __name__ == "__main__":
    plan = run()
    print(plan)
