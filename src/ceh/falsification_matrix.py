"""Unified falsification matrix for the CEH research program.

This module does not declare biological validity. It assembles verified benchmark
rows into an auditable evidence table and explicitly distinguishes measured
dimensions from unavailable evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable
import json
from pathlib import Path
import numpy as np


@dataclass(frozen=True)
class FalsificationRow:
    experiment: str
    method: str
    scenario: str
    mechanism: str
    auroc: float | None
    auprc: float | None
    delta_auroc: float | None
    n: int
    positives: int


@dataclass(frozen=True)
class FalsificationSummary:
    method: str
    measured_experiments: tuple[str, ...]
    n_rows: int
    mean_auroc: float | None
    median_delta_auroc: float | None
    null_rows: int
    transition_rows: int


def _finite(value):
    return value is not None and np.isfinite(value)


def assemble(rows: Iterable[dict], *, experiment: str) -> list[FalsificationRow]:
    out = []
    for row in rows:
        out.append(
            FalsificationRow(
                experiment=experiment,
                method=str(row.get("method", "")),
                scenario=str(row.get("scenario", "unspecified")),
                mechanism=str(row.get("mechanism", "unspecified")),
                auroc=float(row["auroc"]) if _finite(row.get("auroc")) else None,
                auprc=float(row["auprc"]) if _finite(row.get("auprc")) else None,
                delta_auroc=(
                    float(row["delta_auroc"])
                    if _finite(row.get("delta_auroc"))
                    else None
                ),
                n=int(row.get("n", 0)),
                positives=int(row.get("positives", 0)),
            )
        )
    return out


def summarize(rows: Iterable[FalsificationRow], *, method="ceh") -> FalsificationSummary:
    selected = [r for r in rows if r.method == method]
    aurocs = [r.auroc for r in selected if r.auroc is not None]
    deltas = [r.delta_auroc for r in selected if r.delta_auroc is not None]
    null_rows = [
        r for r in selected
        if r.mechanism in {"matched_no_transition", "time_shuffle", "nonnormal"}
    ]
    transition_rows = [r for r in selected if r.positives > 0]

    return FalsificationSummary(
        method=method,
        measured_experiments=tuple(sorted({r.experiment for r in selected})),
        n_rows=len(selected),
        mean_auroc=float(np.mean(aurocs)) if aurocs else None,
        median_delta_auroc=float(np.median(deltas)) if deltas else None,
        null_rows=len(null_rows),
        transition_rows=len(transition_rows),
    )


def write_matrix(path: str | Path, rows: Iterable[FalsificationRow]) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(row) for row in rows]
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return p


def write_summary(path: str | Path, summary: FalsificationSummary) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(asdict(summary), indent=2) + "\n", encoding="utf-8")
    return p
