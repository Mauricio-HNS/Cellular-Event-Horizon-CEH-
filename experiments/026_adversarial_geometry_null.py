"""Experiment 026: geometry-matched adversarial null.

Question:
Can CEH distinguish a labeled transition mechanism from trajectories that
reproduce directionality, acceleration and/or convergence without a transition?

This experiment is a falsification control, not a claim of biological
validity.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

import numpy as np

from ceh.adversarial_nulls import (
    convergence_without_transition,
    matched_directional_noise,
    matched_geometry_population,
)
from ceh.baselines import ceh_signal


@dataclass(frozen=True)
class NullScenario:
    name: str
    n_trajectories: int
    n_steps: int
    n_features: int
    labeled_transition: bool = False


def _trajectory_ceh_score(x: np.ndarray) -> float:
    values = []
    for t in range(len(x)):
        try:
            values.append(float(ceh_signal(x, t, window=4)))
        except ValueError:
            values.append(0.0)
    return float(np.max(values))


def score_population(trajectories):
    return np.asarray([_trajectory_ceh_score(x) for x in trajectories], dtype=float)


def build_scenarios(seed: int = 7):
    return [
        (
            NullScenario("direction_only", 24, 60, 4),
            matched_directional_noise(seed=seed),
        ),
        (
            NullScenario("convergence_only", 24, 60, 4),
            convergence_without_transition(seed=seed + 1),
        ),
        (
            NullScenario("geometry_matched", 24, 60, 4),
            matched_geometry_population(seed=seed + 2),
        ),
    ]


def run(seed: int = 7):
    rows = []
    for spec, trajectories in build_scenarios(seed):
        scores = score_population(trajectories)
        rows.append(
            {
                **asdict(spec),
                "mean_ceh_score": float(scores.mean()),
                "std_ceh_score": float(scores.std()),
                "max_ceh_score": float(scores.max()),
            }
        )
    return rows


def write_result(path: str | Path = "results/026-adversarial-geometry-null.json"):
    rows = run()
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return p


if __name__ == "__main__":
    print(write_result())
