"""Experiment 002: convergence versus identity-permutation null."""

import numpy as np

from ceh.convergence import convergence_index
from ceh.nulls import permute_trajectories


def synthetic_converging_world(
    n_trajectories: int = 24,
    n_steps: int = 30,
    n_features: int = 3,
    seed: int = 7,
) -> np.ndarray:
    """Create independent trajectories converging toward a common state."""
    rng = np.random.default_rng(seed)
    starts = rng.normal(0.0, 1.0, size=(n_trajectories, n_features))
    target = np.zeros(n_features)
    alpha = np.linspace(0.0, 1.0, n_steps)[None, :, None]
    noise = rng.normal(0.0, 0.015, size=(n_trajectories, n_steps, n_features))
    return (1.0 - alpha) * starts[:, None, :] + alpha * target + noise


def run(seed: int = 7) -> dict[str, float]:
    world = synthetic_converging_world(seed=seed)
    observed = convergence_index(world)
    null = convergence_index(permute_trajectories(world, seed=seed + 1))
    return {"observed_convergence": observed, "identity_null": null}


if __name__ == "__main__":
    for name, value in run().items():
        print(f"{name}: {value:.6f}")
