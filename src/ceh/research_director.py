"""Autonomous research-direction engine for the CEH program.

The director ranks information-gain opportunities from measured evidence and
explicitly reserves literature intelligence and self-evaluation as mandatory
inputs to each research cycle. It does not infer truth from scores, never
treats missing evidence as failure, and never rewrites historical evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path

from .direction import DIMENSIONS
from .evidence import build_evidence_snapshot, score_from_rows
from .falsification_matrix import FalsificationRow, summarize


@dataclass(frozen=True)
class ResearchAction:
    priority: int
    action: str
    reason: str
    scientific_question: str
    implementation_target: str


@dataclass(frozen=True)
class ResearchPlan:
    current_direction: str
    measured_dimensions: tuple[str, ...]
    unavailable_dimensions: tuple[str, ...]
    strongest_evidence: tuple[str, ...]
    critical_weaknesses: tuple[str, ...]
    actions: tuple[ResearchAction, ...]
    falsification_status: str
    literature_required: bool = True
    self_evaluation_required: bool = True


def build_plan(
    rows: list[FalsificationRow],
    *,
    evidence_rows: list[dict] | None = None,
    method: str = "ceh",
) -> ResearchPlan:
    summary = summarize(rows, method=method)
    evidence = score_from_rows(evidence_rows or [], method=method) if evidence_rows else {}

    measured = tuple(k for k, v in evidence.items() if v is not None)
    unavailable = tuple(k for k in DIMENSIONS if k not in measured)

    strengths = []
    weaknesses = []

    if summary.n_rows:
        strengths.append(
            f"{summary.n_rows} measured {method} benchmark rows are available."
        )
    if summary.median_delta_auroc is not None:
        strengths.append(
            f"Median reported delta AUROC is {summary.median_delta_auroc:.4f}; "
            "this is an empirical benchmark quantity, not biological validation."
        )
    if summary.null_rows == 0:
        weaknesses.append("No matched/adversarial null rows are currently represented.")
    if summary.transition_rows == 0:
        weaknesses.append("No transition-positive benchmark rows are currently represented.")
    if "incremental_information" in unavailable:
        weaknesses.append("Incremental information has not yet been measured from verified rows.")
    if "biological_validation" in unavailable:
        weaknesses.append("External biological validation is not measured in the current computational matrix.")

    actions = []
    priority = 1

    if summary.null_rows == 0:
        actions.append(ResearchAction(
            priority, "Add matched and adversarial null mechanisms",
            "Without null mechanisms, apparent signal can remain compatible with confounding dynamics.",
            "Does CEH survive mechanisms that reproduce temporal structure without the proposed transition mechanism?",
            "experiments/023_matched_null_population.py and src/ceh/null_matrix.py",
        ))
        priority += 1

    if "incremental_information" in unavailable:
        actions.append(ResearchAction(
            priority, "Complete joint incremental evaluation",
            "The key scientific claim requires information beyond strong baseline representations.",
            "Does CEH add prospective information conditional on snapshot, temporal and early-warning features?",
            "src/ceh/joint_incremental.py and experiments/022_joint_incremental_protocol.py",
        ))
        priority += 1

    actions.append(ResearchAction(
        priority,
        "Promote trajectory-level held-out evaluation to the primary endpoint",
        "Cutoff-level rows can overweight long trajectories and violate the intended population-level inference.",
        "Does the result replicate when each trajectory contributes one independent held-out score?",
        "src/ceh/hierarchical.py and src/ceh/joint_incremental.py",
    ))
    priority += 1

    if "biological_validation" in unavailable:
        actions.append(ResearchAction(
            priority,
            "Define external biological validation before claiming generalization",
            "Synthetic worlds cannot establish biological validity.",
            "Does the representation reproduce prospectively on an independently sourced biological dataset?",
            "docs/RESEARCH_DIRECTOR.md and a future external-data benchmark",
        ))

    if summary.null_rows and summary.transition_rows:
        status = "computational evidence assembled; falsification remains active"
    else:
        status = "insufficient matrix coverage for a meaningful falsification conclusion"

    direction = (
        "prioritize conclusion-changing null, incremental and trajectory-level tests"
        if actions else "maintain current falsification program"
    )

    return ResearchPlan(
        direction,
        measured,
        unavailable,
        tuple(strengths),
        tuple(weaknesses),
        tuple(actions),
        status,
        literature_required=True,
        self_evaluation_required=True,
    )


def write_plan(path: str | Path, plan: ResearchPlan) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(asdict(plan), indent=2) + "\n", encoding="utf-8")
    return p
