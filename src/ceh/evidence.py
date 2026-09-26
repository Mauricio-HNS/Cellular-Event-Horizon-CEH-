"""Evidence-derived research direction scoring for CEH.

Unavailable evidence is represented explicitly as missing rather than as a
scientific failure. Direction summaries should only aggregate measured
dimensions.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import numpy as np

from .direction import DIMENSIONS, DirectionSnapshot, append_snapshot, validate_snapshot


@dataclass(frozen=True)
class EvidenceItem:
    dimension: str
    value: float | None
    source: str
    metric: str
    note: str = ""


@dataclass(frozen=True)
class EvidenceSnapshot:
    timestamp: str
    dimensions: dict[str, float | None]
    measured: tuple[str, ...]
    note: str = ""


def _clip(value: float) -> float:
    return float(np.clip(value, 0.0, 1.0))


def score_from_rows(rows, *, method="ceh", comparator="early_warning"):
    rows = [dict(r) for r in rows]
    selected = [r for r in rows if r.get("method") == method]
    if not selected:
        raise ValueError(f"no rows found for method={method}")

    deltas = [
        float(r["delta_auroc"])
        for r in selected
        if "delta_auroc" in r and np.isfinite(r["delta_auroc"])
    ]
    if deltas:
        robustness = np.mean(np.asarray(deltas) >= 0)
        incremental = _clip(0.5 + 2.0 * float(np.median(deltas)))
    else:
        aurocs = [
            float(r["auroc"]) for r in selected if np.isfinite(r.get("auroc", np.nan))
        ]
        robustness = np.mean(np.asarray(aurocs) >= 0.5) if aurocs else np.nan
        incremental = np.nan

    null_rows = [
        r for r in rows
        if r.get("mechanism") == "matched_no_transition"
        and r.get("method") == method
    ]
    fprs = [
        float(r["false_positive_rate"])
        for r in null_rows
        if "false_positive_rate" in r and np.isfinite(r["false_positive_rate"])
    ]
    null_resistance = _clip(1.0 - float(np.mean(fprs))) if fprs else np.nan

    return {
        "robustness": None if not np.isfinite(robustness) else _clip(robustness),
        "incremental_information": (
            None if not np.isfinite(incremental) else incremental
        ),
        "null_resistance": (
            None if not np.isfinite(null_resistance) else null_resistance
        ),
    }


def build_evidence_snapshot(
    timestamp: str,
    *,
    evidence: dict[str, float | None],
    note: str = "",
) -> EvidenceSnapshot:
    dimensions = {name: evidence.get(name) for name in DIMENSIONS}
    measured = tuple(name for name, value in dimensions.items() if value is not None)
    for value in dimensions.values():
        if value is not None:
            _clip(float(value))
    return EvidenceSnapshot(timestamp, dimensions, measured, note)


def build_snapshot(
    timestamp: str,
    *,
    evidence: dict[str, float | None],
    note: str = "",
) -> DirectionSnapshot:
    """Compatibility adapter for the legacy complete snapshot format.

    Only call this after all dimensions have been measured. It intentionally
    rejects missing evidence rather than converting missing values to zero.
    """
    missing = [name for name in DIMENSIONS if evidence.get(name) is None]
    if missing:
        raise ValueError(f"cannot build complete direction snapshot; missing: {missing}")
    dimensions = {name: _clip(float(evidence[name])) for name in DIMENSIONS}
    snapshot = DirectionSnapshot(timestamp, dimensions, note)
    validate_snapshot(snapshot)
    return snapshot


def write_evidence_report(path: str | Path, items: list[EvidenceItem]) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps([asdict(i) for i in items], indent=2) + "\n",
        encoding="utf-8",
    )
    return p


def record_snapshot(path: str | Path, snapshot: DirectionSnapshot) -> Path:
    return append_snapshot(path, snapshot)
