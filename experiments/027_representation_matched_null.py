"""Experiment 027: representation-matched no-transition controls."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

import numpy as np

from ceh.adversarial_nulls import matched_geometry_population
from ceh.baselines import ceh_signal, snapshot_signal, temporal_signal
from ceh.early_warning import rolling_autocorrelation, rolling_variance
from ceh.inference import paired_auc_bootstrap, paired_auc_permutation
from ceh.joint_trajectory_level import evaluate_joint_trajectory_level
from ceh.multiplicity import primary_endpoint_gate
from ceh.representation_matching import match_controls
from ceh.synthetic import directional_trajectory


@dataclass(frozen=True)
class MatchConfig:
    n_transition: int = 24
    n_pool: int = 192
    n_features: int = 4
    n_steps: int = 60
    transition_time: int = 35
    train_fraction: float = 0.6
    horizon: int = 30
    window: int = 5
    seed: int = 7


def _safe_series(x, fn):
    out = np.zeros(len(x), dtype=float)
    for t in range(len(x)):
        try:
            out[t] = float(fn(x, t))
        except ValueError:
            out[t] = 0.0
    return out


def _snapshot(x):
    return _safe_series(x, snapshot_signal)


def _temporal(x):
    return _safe_series(x, lambda a, t: temporal_signal(a, t, window=3))


def _early_warning(x):
    values = np.linalg.norm(x, axis=1)
    out = np.zeros(len(values), dtype=float)
    if len(values) >= 5:
        out[4:] = np.nan_to_num(
            rolling_variance(values, window=5)
            + rolling_autocorrelation(values, window=5),
            nan=0.0,
            posinf=0.0,
            neginf=0.0,
        )
    return out


def _ceh(x):
    return _safe_series(x, lambda a, t: ceh_signal(a, t, window=4))


def build_dataset(config: MatchConfig = MatchConfig()):
    transition = [
        directional_trajectory(
            n_steps=config.n_steps,
            n_features=config.n_features,
            transition_start=config.transition_time,
            noise=0.03,
            seed=config.seed + i,
        )
        for i in range(config.n_transition)
    ]
    pool = matched_geometry_population(
        n_trajectories=config.n_pool,
        n_steps=config.n_steps,
        n_features=config.n_features,
        seed=config.seed + 1000,
    )
    controls = match_controls(transition, pool)
    return transition, controls


def run(config: MatchConfig = MatchConfig(), replicates: int = 2000):
    transition, controls = build_dataset(config)
    trajectories = transition + controls
    times = [config.transition_time] * len(transition) + [10_000] * len(controls)

    result = evaluate_joint_trajectory_level(
        trajectories,
        times,
        snapshot_scorer=_snapshot,
        temporal_scorer=_temporal,
        early_warning_scorer=_early_warning,
        ceh_scorer=_ceh,
        horizon=config.horizon,
        window=config.window,
        train_fraction=config.train_fraction,
        seed=config.seed,
    )
    ci = paired_auc_bootstrap(
        result.test_labels, result.baseline_scores, result.full_scores,
        replicates=replicates, seed=config.seed,
    )
    permutation = paired_auc_permutation(
        result.test_labels, result.baseline_scores, result.full_scores,
        replicates=replicates, seed=config.seed,
    )
    gate = primary_endpoint_gate(
        permutation.p_value,
        result.delta_auroc,
        ci.lower,
        alpha=0.05,
    )
    return {
        "experiment": "027_representation_matched_null",
        "endpoint": "held_out_trajectory_level_delta_auroc",
        "baseline_auroc": result.baseline_auroc,
        "full_auroc": result.full_auroc,
        "delta_auroc": result.delta_auroc,
        "delta_auprc": result.delta_auprc,
        "ci_lower": ci.lower,
        "ci_upper": ci.upper,
        "p_value": permutation.p_value,
        "primary_gate": gate,
        "n_test_trajectories": result.n_trajectories,
        "test_positives": result.positives,
        "matching": asdict(config),
        "interpretation_guard": (
            "This tests whether CEH adds computational information against "
            "geometry-matched no-transition controls. It does not establish "
            "biological validity, causality, diagnosis, prognosis or treatment."
        ),
    }


def write_result(path: str | Path = "results/027-representation-matched-null.json"):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(run(), indent=2) + "\n", encoding="utf-8")
    return p


if __name__ == "__main__":
    print(write_result())
