"""Quantitative research-direction tracking for the CEH program."""
from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import numpy as np

DIMENSIONS = (
    "robustness", "incremental_information", "null_resistance",
    "generalization", "statistical_strength", "reproducibility",
    "novelty", "biological_validation",
)

@dataclass(frozen=True)
class DirectionSnapshot:
    timestamp: str
    dimensions: dict[str, float]
    note: str = ""

@dataclass(frozen=True)
class DirectionReport:
    previous_timestamp: str | None
    current_timestamp: str
    changes: dict[str, float]
    direction_index: float
    improving: tuple[str, ...]
    stable: tuple[str, ...]
    declining: tuple[str, ...]
    priority: tuple[str, ...]
    deprioritize: tuple[str, ...]

def validate_snapshot(snapshot: DirectionSnapshot) -> None:
    if set(snapshot.dimensions) != set(DIMENSIONS):
        raise ValueError("snapshot dimensions must exactly match DIMENSIONS")
    values = np.asarray(list(snapshot.dimensions.values()), dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("snapshot values must be finite")
    if np.any((values < 0) | (values > 1)):
        raise ValueError("snapshot values must be between 0 and 1")

def direction_report(current: DirectionSnapshot,
                     previous: DirectionSnapshot | None = None,
                     improve_threshold: float = 0.05,
                     decline_threshold: float = -0.05) -> DirectionReport:
    validate_snapshot(current)
    if previous is not None:
        validate_snapshot(previous)
        changes = {k: current.dimensions[k] - previous.dimensions[k] for k in DIMENSIONS}
        previous_timestamp = previous.timestamp
    else:
        changes = {k: 0.0 for k in DIMENSIONS}
        previous_timestamp = None
    improving = tuple(k for k, v in changes.items() if v >= improve_threshold)
    declining = tuple(k for k, v in changes.items() if v <= decline_threshold)
    stable = tuple(k for k, v in changes.items()
                   if k not in improving and k not in declining)
    index = float(np.mean(list(current.dimensions.values())))
    priority = tuple(sorted(DIMENSIONS, key=lambda k: (current.dimensions[k], changes[k]))[:3])
    deprioritize = tuple(k for k in DIMENSIONS if current.dimensions[k] >= 0.8 and changes[k] >= 0)
    return DirectionReport(previous_timestamp, current.timestamp, changes, index,
                           improving, stable, declining, priority, deprioritize)

def append_snapshot(path: str | Path, snapshot: DirectionSnapshot) -> Path:
    validate_snapshot(snapshot)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    records = []
    if p.exists() and p.read_text(encoding="utf-8").strip():
        records = json.loads(p.read_text(encoding="utf-8"))
    records.append(asdict(snapshot))
    p.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    return p
