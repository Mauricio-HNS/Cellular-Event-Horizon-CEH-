"""Factorial benchmark design for prospective transition signals."""
from __future__ import annotations

from dataclasses import dataclass, asdict
import csv
import json
from pathlib import Path
from typing import Iterable

import numpy as np

from .benchmark import score_at_cutoff
from .noise import gaussian, heavy_tailed, impulse_contaminated
from .null_mechanisms import nonnormal_linear_system


@dataclass(frozen=True)
class MatrixRow:
    scenario: str
    noise: str
    missingness: float
    dimensionality: int
    modality: str
    mechanism: str
    method: str
    auroc: float
    auprc: float
    n: int
    positives: int


def apply_missingness(x: np.ndarray, rate: float, seed: int) -> np.ndarray:
    """Mask observations without changing the latent trajectory length."""
    if not 0.0 <= rate < 1.0:
        raise ValueError("missingness must be in [0, 1)")
    y = np.asarray(x, dtype=float).copy()
    if rate == 0.0:
        return y
    rng = np.random.default_rng(seed)
    mask = rng.random(y.shape) < rate
    y[mask] = np.nan
    # Keep each cutoff score computable: carry the last observed value forward.
    for j in range(y.shape[1]):
        last = 0.0
        for i in range(len(y)):
            if np.isfinite(y[i, j]):
                last = y[i, j]
            else:
                y[i, j] = last
    return y


def embed_dimension(x: np.ndarray, dimensions: int, seed: int) -> np.ndarray:
    """Project a scalar or low-dimensional trajectory into a controlled state space."""
    if dimensions < 1:
        raise ValueError("dimensions must be positive")
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    if x.shape[1] == dimensions:
        return x.copy()
    rng = np.random.default_rng(seed)
    basis = rng.normal(size=(x.shape[1], dimensions))
    basis /= np.maximum(np.linalg.norm(basis, axis=0, keepdims=True), 1e-12)
    z = x @ basis
    nuisance = rng.normal(0.0, 0.01, size=z.shape)
    return z + nuisance


def modality_view(x: np.ndarray, modality: str, seed: int) -> np.ndarray:
    """Create deterministic observation-model variants without changing labels."""
    x = np.asarray(x, dtype=float)
    if modality == "state":
        return x
    if modality == "scaled":
        scale = np.linspace(0.7, 1.3, x.shape[1])
        return x * scale
    if modality == "noisy":
        return x + gaussian(x.shape, sigma=0.02, seed=seed)
    if modality == "heavy_tail":
        return x + heavy_tailed(x.shape, scale=0.01, df=2.0, seed=seed)
    raise ValueError(f"unknown modality: {modality}")


def _labels_and_scores(
    trajectory: np.ndarray,
    transition_time: int,
    horizon: int,
    method: str,
    window: int,
) -> tuple[np.ndarray, np.ndarray]:
    scores, labels = [], []
    start = max(window + 2, 1)
    stop = min(len(trajectory) - 1, transition_time + horizon)
    for cutoff in range(start, stop + 1):
        score = score_at_cutoff(trajectory, cutoff, method, window=window)
        if np.isfinite(score):
            scores.append(float(score))
            labels.append(int(0 < transition_time - cutoff <= horizon))
    return np.asarray(scores), np.asarray(labels, dtype=int)


def rank_metric(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float]:
    from .metrics import auroc, auprc
    return auroc(scores, labels), auprc(scores, labels)


def generate_matrix(
    trajectories: Iterable[np.ndarray],
    transition_times: Iterable[int],
    *,
    horizon: int = 30,
    methods=("snapshot", "temporal", "early_warning", "ceh"),
    noises=("gaussian", "heavy_tail", "impulse"),
    missingness=(0.0, 0.1),
    dimensions=(1, 4),
    modalities=("state", "scaled", "noisy"),
    mechanism="controlled_transition",
) -> list[MatrixRow]:
    """Run a reproducible factorial benchmark across observation conditions."""
    rows: list[MatrixRow] = []
    trajectories = list(trajectories)
    transition_times = list(transition_times)
    if len(trajectories) != len(transition_times):
        raise ValueError("trajectory/transition lengths differ")

    for seed, (base, t0) in enumerate(zip(trajectories, transition_times)):
        for noise_name in noises:
            if noise_name == "gaussian":
                noisy = np.asarray(base, dtype=float) + gaussian(np.asarray(base).shape, 0.01, seed)
            elif noise_name == "heavy_tail":
                noisy = np.asarray(base, dtype=float) + heavy_tailed(np.asarray(base).shape, 0.01, 2.0, seed)
            elif noise_name == "impulse":
                noisy = impulse_contaminated(base, 0.02, 0.08, seed)
            else:
                raise ValueError(f"unknown noise: {noise_name}")

            for miss in missingness:
                for dim in dimensions:
                    embedded = embed_dimension(noisy, dim, seed)
                    for mod in modalities:
                        observed = modality_view(embedded, mod, seed)
                        observed = apply_missingness(observed, miss, seed)
                        for method in methods:
                            scores_all, labels_all = [], []
                            s, y = _labels_and_scores(observed, t0, horizon, method, 5)
                            if len(s):
                                scores_all.append(s)
                                labels_all.append(y)
                            if not scores_all:
                                continue
                            scores = np.concatenate(scores_all)
                            labels = np.concatenate(labels_all)
                            auroc_value, auprc_value = rank_metric(scores, labels)
                            rows.append(MatrixRow(
                                scenario="transition",
                                noise=noise_name,
                                missingness=float(miss),
                                dimensionality=int(dim),
                                modality=mod,
                                mechanism=mechanism,
                                method=method,
                                auroc=float(auroc_value),
                                auprc=float(auprc_value),
                                n=int(len(labels)),
                                positives=int(labels.sum()),
                            ))
    return rows


def write_results(rows: Iterable[MatrixRow], output_dir: str | Path) -> tuple[Path, Path]:
    """Write machine-readable CSV and JSON artifacts for reproducible inspection."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    csv_path = out / "ceh-benchmark-matrix.csv"
    json_path = out / "ceh-benchmark-matrix.json"

    fieldnames = list(asdict(rows[0]).keys()) if rows else list(MatrixRow.__dataclass_fields__.keys())
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    json_path.write_text(json.dumps([asdict(row) for row in rows], indent=2), encoding="utf-8")
    return csv_path, json_path


def stable_null(steps: int = 180, dimensions: int = 1, seed: int = 7) -> np.ndarray:
    """Stable control with no transition label."""
    x = np.zeros((steps + 1, 1))
    rng = np.random.default_rng(seed)
    x[0, 0] = 1.0
    for i in range(steps):
        x[i + 1, 0] = x[i, 0] - 0.12 * x[i, 0] * 0.08 + 0.015 * rng.normal()
    return embed_dimension(x, dimensions, seed)


def nonnormal_null(steps: int = 180, dimensions: int = 4, seed: int = 7) -> np.ndarray:
    """Stable non-normal system used as an amplification-only adversarial control."""
    return embed_dimension(nonnormal_linear_system(steps=steps, seed=seed), dimensions, seed)
