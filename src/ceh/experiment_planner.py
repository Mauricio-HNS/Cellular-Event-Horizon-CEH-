"""Autonomous experiment planning for the Cellular Event Horizon program.

The planner converts verified research evidence into a falsifiable, reproducible
experiment specification. It does not assign scientific truth; it exposes the
assumptions and tests required to challenge a hypothesis.
"""

from dataclasses import dataclass, asdict
from typing import Any, Mapping, Sequence
import json


@dataclass(frozen=True)
class ExperimentSpec:
    experiment_id: str
    hypothesis: str
    mechanism: str
    primary_endpoint: str
    comparators: tuple[str, ...]
    controls: tuple[str, ...]
    null_mechanisms: tuple[str, ...]
    mathematical_formulation: str
    evaluation_unit: str
    split_strategy: str
    leakage_guards: tuple[str, ...]
    statistical_test: str
    multiplicity_plan: str
    acceptance_criteria: tuple[str, ...]
    falsification_criteria: tuple[str, ...]
    information_gain: str
    implementation_targets: tuple[str, ...]
    stop_conditions: tuple[str, ...]


def _tuple(values: Sequence[str] | None) -> tuple[str, ...]:
    return tuple(values or ())


def make_primary_incremental_spec(
    *,
    horizon: int = 30,
    window: int = 5,
    alpha: float = 0.05,
) -> ExperimentSpec:
    """Create the primary experiment for testing incremental CEH information.

    The design treats trajectories as the independent experimental units and
    requires CEH to add information beyond a joint baseline of snapshot,
    temporal and early-warning signals.
    """

    if horizon <= window:
        raise ValueError("horizon must be greater than window")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    return ExperimentSpec(
        experiment_id="022_joint_incremental_protocol",
        hypothesis=(
            "At a prospective cutoff, a CEH representation contains information "
            "about a future transition that is not explained jointly by snapshot, "
            "temporal and established early-warning features."
        ),
        mechanism=(
            "A localized latent dynamical configuration changes the conditional "
            "distribution of future transition outcomes."
        ),
        primary_endpoint=(
            "Held-out trajectory-level residual AUROC and AUPRC after adding CEH "
            "to the jointly fitted baseline."
        ),
        comparators=("snapshot", "temporal", "early_warning", "joint_baseline"),
        controls=(
            "matched no-transition trajectories",
            "transition trajectories with event windows held out",
            "representation-matched controls",
        ),
        null_mechanisms=(
            "time-shuffled trajectories preserving marginal observations",
            "stable non-normal dynamics without transition",
            "clustered events without the proposed CEH mechanism",
            "matched no-transition population",
        ),
        mathematical_formulation=(
            "For trajectory i and cutoff t, fit p_base = P(Y=1 | Z_base) and "
            "p_full = P(Y=1 | Z_base, Z_CEH) using training trajectories only; "
            "test whether p_full provides positive held-out incremental information. "
            "The CEH claim is operationalized as I(Y; Z_CEH | Z_base) > 0."
        ),
        evaluation_unit="trajectory",
        split_strategy="grouped train/test split by trajectory; no trajectory crosses splits",
        leakage_guards=(
            "fit normalization only on training trajectories",
            "fit baseline and full models only on training trajectories",
            "freeze the event definition before test evaluation",
            "never use future observations beyond the cutoff",
            "bootstrap trajectories rather than cutoffs",
        ),
        statistical_test=(
            "paired held-out comparison of full versus joint-baseline predictions, "
            "with trajectory bootstrap confidence intervals and a trajectory-level "
            "permutation test."
        ),
        multiplicity_plan=(
            f"Primary alpha={alpha}; secondary endpoints and null-mechanism analyses "
            "controlled with Benjamini-Hochberg FDR."
        ),
        acceptance_criteria=(
            "positive held-out residual AUROC relative to the joint baseline",
            "effect persists across independent null mechanisms",
            "effect is not explained by representation dimension or normalization",
            "trajectory-level uncertainty excludes a practically negligible effect",
        ),
        falsification_criteria=(
            "CEH provides no incremental held-out information beyond the joint baseline",
            "effect disappears under a representation-preserving control",
            "effect is reproduced by matched null mechanisms",
            "performance depends on information unavailable at the prospective cutoff",
        ),
        information_gain=(
            "This experiment can directly weaken the central claim because it asks "
            "whether CEH adds information after strong temporal alternatives are "
            "already available, rather than merely showing that CEH correlates with "
            "future transitions."
        ),
        implementation_targets=(
            "src/ceh/incremental.py",
            "src/ceh/hierarchical.py",
            "src/ceh/permutation.py",
            "src/ceh/evidence.py",
            "experiments/022_joint_incremental_protocol.py",
            "tests/test_incremental.py",
            "tests/test_hierarchical.py",
        ),
        stop_conditions=(
            "stop adding new CEH features until the joint-baseline challenge is passed",
            "stop interpreting cutoff-level bootstrap results as trajectory-level evidence",
            "stop treating unmeasured research-direction dimensions as zero evidence",
        ),
    )


def to_dict(spec: ExperimentSpec) -> dict[str, Any]:
    return asdict(spec)


def to_json(spec: ExperimentSpec, *, indent: int = 2) -> str:
    return json.dumps(to_dict(spec), indent=indent, sort_keys=True)


def write_spec(spec: ExperimentSpec, path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(to_dict(spec), handle, indent=2, sort_keys=True)
        handle.write("\n")
