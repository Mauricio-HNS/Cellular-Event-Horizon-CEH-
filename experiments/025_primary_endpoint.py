"""Experiment 025: pre-specified primary CEH incremental endpoint.

Computational protocol only. No biological or clinical interpretation is
attached to a passing statistical result.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
import numpy as np

from ceh.baselines import snapshot_signal, temporal_signal, ceh_signal
from ceh.early_warning import rolling_autocorrelation, rolling_variance
from ceh.inference import paired_auc_bootstrap, paired_auc_permutation
from ceh.joint_trajectory_level import evaluate_joint_trajectory_level
from ceh.multiplicity import primary_endpoint_gate
from ceh.synthetic import directional_trajectory, null_trajectory


@dataclass(frozen=True)
class PrimaryEndpointResult:
    delta_auroc: float
    delta_auprc: float
    p_value: float
    ci_lower: float
    ci_upper: float
    significant: bool
    interpretation: str


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


def build_dataset(n_transition=24, n_null=24, seed=100):
    trajectories = []
    transition_times = []

    for i in range(n_transition):
        trajectories.append(
            directional_trajectory(
                n_steps=60, n_features=4, transition_start=35,
                noise=0.03, seed=seed + i,
            )
        )
        transition_times.append(35)

    for i in range(n_null):
        trajectories.append(
            null_trajectory(
                n_steps=60, n_features=4, noise=0.12,
                seed=seed + 1000 + i,
            )
        )
        transition_times.append(10_000)

    return trajectories, transition_times


def run_primary_endpoint(
    trajectories,
    transition_times,
    *,
    alpha=0.05,
    replicates=2000,
    seed=7,
):
    result = evaluate_joint_trajectory_level(
        trajectories,
        transition_times,
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
    significant = primary_endpoint_gate(
        p_value=permutation.p_value,
        effect=result.delta_auroc,
        ci_lower=ci.lower,
        alpha=alpha,
    )
    return PrimaryEndpointResult(
        delta_auroc=result.delta_auroc,
        delta_auprc=result.delta_auprc,
        p_value=permutation.p_value,
        ci_lower=ci.lower,
        ci_upper=ci.upper,
        significant=significant,
        interpretation=(
            "primary computational endpoint passed statistical gate"
            if significant
            else "primary computational endpoint did not pass statistical gate"
        ),
    )


def write_result(path: str | Path, result: PrimaryEndpointResult) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(asdict(result), indent=2) + "\n", encoding="utf-8")
    return p


if __name__ == "__main__":
    trajectories, transition_times = build_dataset()
    result = run_primary_endpoint(trajectories, transition_times)
    print(result)
