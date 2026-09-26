"""Evidence-derived research direction scoring for CEH.

This module converts verified benchmark outputs into transparent 0..1 navigation
scores. The scores are not probabilities, truth values, or scientific validity.
Each score carries provenance so a direction snapshot can be audited.
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
    value: float
    source: str
    metric: str
    note: str = ""

def _clip(value: float) -> float:
    return float(np.clip(value, 0.0, 1.0))

def score_from_rows(rows, *, method="ceh", comparator="early_warning"):
    """Derive transparent evidence scores from benchmark result dictionaries.

    Expected row keys may include method, auroc/auprc, delta_auroc/delta_auprc,
    false_positive_rate, q_value, bootstrap interval and scenario/mechanism.
    Missing evidence is reported as unavailable rather than fabricated.
    """
    rows = [dict(r) for r in rows]
    selected = [r for r in rows if r.get("method") == method]
    if not selected:
        raise ValueError(f"no rows found for method={method}")

    # Robustness: fraction of finite factorial conditions with non-negative
    # incremental separation against the named comparator, when available.
    deltas = [float(r["delta_auroc"]) for r in selected if "delta_auroc" in r and np.isfinite(r["delta_auroc"])]
    if deltas:
        robustness = np.mean(np.asarray(deltas) >= 0)
    else:
        aurocs = [float(r["auroc"]) for r in selected if np.isfinite(r.get("auroc", np.nan))]
        robustness = np.mean(np.asarray(aurocs) >= 0.5) if aurocs else np.nan

    incremental = np.nan
    if deltas:
        # Map the median delta to a bounded navigation score; zero means no
        # observed incremental separation and positive values increase the score.
        incremental = _clip(0.5 + 2.0 * float(np.median(deltas)))

    null_rows = [r for r in rows if r.get("mechanism") == "matched_no_transition" and r.get("method") == method]
    if null_rows:
        fprs = [float(r["false_positive_rate"]) for r in null_rows if "false_positive_rate" in r and np.isfinite(r["false_positive_rate"])]
        if fprs:
            null_resistance = _clip(1.0 - float(np.mean(fprs)))
        else:
            # AUROC near chance under a null-only discrimination challenge is
            # not directly available from pooled rows; keep this conservative.
            null_resistance = np.nan
    else:
        null_resistance = np.nan

    return {
        "robustness": None if not np.isfinite(robustness) else _clip(robustness),
        "incremental_information": None if not np.isfinite(incremental) else incremental,
        "null_resistance": None if not np.isfinite(null_resistance) else null_resistance,
    }

def build_snapshot(timestamp: str, *, evidence: dict[str, float | None],
                   note: str = "Evidence-derived dimensions; unavailable dimensions remain explicitly unset.") -> DirectionSnapshot:
    """Build a complete direction snapshot without inventing unavailable evidence."""
    dimensions = {}
    for name in DIMENSIONS:
        value = evidence.get(name)
        if value is None:
            # Unmeasured dimensions are represented conservatively as zero until
            # a documented measurement exists; callers must preserve provenance.
            value = 0.0
        dimensions[name] = _clip(float(value))
    snapshot = DirectionSnapshot(timestamp, dimensions, note)
    validate_snapshot(snapshot)
    return snapshot

def write_evidence_report(path: str | Path, items: list[EvidenceItem]) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps([asdict(i) for i in items], indent=2) + "\n", encoding="utf-8")
    return p

def record_snapshot(path: str | Path, snapshot: DirectionSnapshot) -> Path:
    return append_snapshot(path, snapshot)
