"""Experiment 026: formal adversarial geometry falsification.

Question:
Can the CEH candidate add prospective information about a labeled transition
when the no-transition controls reproduce directionality, acceleration and/or
convergence geometry?

This is a mechanism-specific computational falsification test. It does not
establish biological validity.
"""
from dataclasses import asdict, dataclass
import json
from pathlib import Path

import numpy as np

from ceh.adversarial_nulls import (
    convergence_without_transition,
    matched_directional_noise,
    matched_geometry_population,
)
from ceh.baselines import ceh_signal, snapshot_signal, temporal_signal
from ceh.early_warning import rolling_autocorrelation, rolling_variance
from ceh.inference import paired_auc_bootstrap, paired_auc_permutation
from ceh.joint_trajectory_level import evaluate_joint_trajectory_level
from ceh.multiplicity import benjamini_hochberg
from ceh.synthetic import directional_trajectory


@dataclass(frozen=True)
class NullScenario:
    name: str
    n_trajectories: int
    n_steps: int
    n_features: int
    labeled_transition: bool = False


def _safe_series(x, fn):
    out = np.zeros(len(x), dtype=float)
    for t in range(len(x)):
        try:
            out[t] = float(fn(x, t))
        except ValueError:
            out[t] = 0.0
    return out


def _snapshot_series(x):
    return _safe_series(x, snapshot_signal)


def _temporal_series(x):
    return _safe_series(x, lambda a, t: temporal_signal(a, t, window=3))


def _early_warning_series(x):
    values = np.linalg.norm(x, axis=1)
    if len(values) < 5:
        return np.zeros(len(values), dtype=float)
    variance = rolling_variance(values, window=5)
    autocorrelation = rolling_autocorrelation(values, window=5)
    signal = np.nan_to_num(
        variance + autocorrelation, nan=0.0, posinf=0.0, neginf=0.0
    )
    out = np.zeros(len(values), dtype=float)
    out[4:] = signal
    return out


def _ceh_series(x):
    return _safe_series(x, lambda a, t: ceh_signal(a, t, window=4))


def build_scenarios(seed: int = 7):
    """Return matched transition data and three geometry-only null populations."""
    transition = [
        directional_trajectory(
            n_steps=60,
            n_features=4,
            transition_start=35,
            noise=0.03,
            seed=seed + i,
        )
        for i in range(24)
    ]
    transition_times = [35] * len(transition)

    nulls = [
        (
            NullScenario("direction_only", 24, 60, 4),
            matched_directional_noise(seed=seed + 100),
        ),
        (
            NullScenario("convergence_only", 24, 60, 4),
            convergence_without_transition(seed=seed + 200),
        ),
        (
            NullScenario("geometry_matched", 24, 60, 4),
            matched_geometry_population(seed=seed + 300),
        ),
    ]
    return transition, transition_times, nulls


def run(seed: int = 7, replicates: int = 2000):
    transition, transition_times, nulls = build_scenarios(seed)
    rows = []

    for spec, controls in nulls:
        trajectories = transition + controls
        transition_times_all = transition_times + [10_000] * len(controls)

        result = evaluate_joint_trajectory_level(
            trajectories,
            transition_times_all,
            snapshot_scorer=_snapshot_series,
            temporal_scorer=_temporal_series,
            early_warning_scorer=_early_warning_series,
            ceh_scorer=_ceh_series,
            horizon=30,
            window=5,
            train_fraction=0.6,
            seed=seed,
        )
        ci = paired_auc_bootstrap(
            result.test_labels,
            result.baseline_scores,
            result.full_scores,
            replicates=replicates,
            seed=seed,
        )
        permutation = paired_auc_permutation(
            result.test_labels,
            result.baseline_scores,
            result.full_scores,
            replicates=replicates,
            seed=seed,
        )

        rows.append(
            {
                **asdict(spec),
                "endpoint": "trajectory_level_incremental_delta_auroc",
                "baseline_auroc": result.baseline_auroc,
                "full_auroc": result.full_auroc,
                "delta_auroc": result.delta_auroc,
                "baseline_auprc": result.baseline_auprc,
                "full_auprc": result.full_auprc,
                "delta_auprc": result.delta_auprc,
                "ci_lower": ci.lower,
                "ci_upper": ci.upper,
                "p_value": permutation.p_value,
                "test_trajectories": result.n_trajectories,
                "test_positives": result.positives,
            }
        )

    fdr = benjamini_hochberg([row["p_value"] for row in rows], alpha=0.05)
    for row, q, rejected in zip(rows, fdr.q_values, fdr.rejected):
        row["q_value"] = q
        row["fdr_rejected"] = rejected

    return rows


def write_result(
    path: str | Path = "results/026-adversarial-geometry-null.json",
):
    rows = run()
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(
            {
                "experiment": "026_adversarial_geometry_null",
                "status": "computed_when_executed",
                "question": (
                    "Does CEH add prospective information beyond joint "
                    "snapshot, temporal and early-warning baselines against "
                    "geometry-matched no-transition controls?"
                ),
                "interpretation_guard": (
                    "A result here tests mechanism-specific computational "
                    "discrimination only; it does not establish biological "
                    "validity, causality, diagnosis, prognosis or treatment."
                ),
                "rows": rows,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return p


if __name__ == "__main__":
    print(write_result())
