"""Experiment 025: pre-specified primary CEH incremental endpoint.

The primary endpoint is defined before secondary analyses:
held-out trajectory-level incremental AUROC of CEH over the joint baseline
(snapshot + temporal + early-warning).

This experiment intentionally keeps statistical inference separate from
biological interpretation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
import numpy as np

from ceh.inference import bootstrap_mean_difference, paired_sign_flip
from ceh.joint_trajectory_level import evaluate_joint_trajectory_level
from ceh.multiplicity import primary_endpoint_gate


@dataclass(frozen=True)
class PrimaryEndpointResult:
    delta_auroc: float
    delta_auprc: float
    p_value: float
    ci_lower: float
    ci_upper: float
    significant: bool
    interpretation: str


def primary_endpoint(
    trajectory_deltas: np.ndarray,
    *,
    delta_auroc: float,
    delta_auprc: float,
    alpha: float = 0.05,
    replicates: int = 2000,
    seed: int = 7,
) -> PrimaryEndpointResult:
    ci = bootstrap_mean_difference(
        trajectory_deltas,
        replicates=replicates,
        confidence=0.95,
        seed=seed,
    )
    permutation = paired_sign_flip(
        trajectory_deltas,
        replicates=replicates,
        alternative="greater",
        seed=seed,
    )
    significant = primary_endpoint_gate(
        p_value=permutation.p_value,
        effect=delta_auroc,
        ci_lower=ci.lower,
        alpha=alpha,
    )
    interpretation = (
        "primary computational endpoint passed statistical gate"
        if significant
        else "primary computational endpoint did not pass statistical gate"
    )
    return PrimaryEndpointResult(
        delta_auroc=float(delta_auroc),
        delta_auprc=float(delta_auprc),
        p_value=permutation.p_value,
        ci_lower=ci.lower,
        ci_upper=ci.upper,
        significant=significant,
        interpretation=interpretation,
    )


def write_result(path: str | Path, result: PrimaryEndpointResult) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(asdict(result), indent=2) + "\n", encoding="utf-8")
    return p
