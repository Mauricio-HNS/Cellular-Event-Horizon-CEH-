"""Synthetic biological worlds with known generating dynamics.

These worlds are methodological instruments. They are not biological simulations
and must never be presented as biological evidence.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class WorldConfig:
    dimensions: int = 4
    steps: int = 40
    noise: float = 0.01
    seed: int = 7

@dataclass(frozen=True)
class World:
    states: np.ndarray
    transition_time: int
    perturbation_time: int
    latent_regime: np.ndarray

def generate_world(config: WorldConfig = WorldConfig()) -> World:
    if config.dimensions < 2 or config.steps < 4:
        raise ValueError("dimensions must be >=2 and steps must be >=4")
    rng = np.random.default_rng(config.seed)
    d, n = config.dimensions, config.steps
    states = np.zeros((n, d), dtype=float)
    states[0] = rng.normal(0.0, 0.05, d)

    transition_time = n // 2
    perturbation_time = transition_time - 4
    target = np.zeros(d)
    target[0] = 1.0

    for t in range(1, n):
        previous = states[t - 1]
        drift = 0.04 * (target - previous) if t >= transition_time else -0.02 * previous
        perturbation = 0.0
        if t == perturbation_time:
            perturbation = 0.12
        states[t] = previous + drift
        states[t, 0] += perturbation
        states[t] += rng.normal(0.0, config.noise, d)

    regime = np.zeros(n, dtype=int)
    regime[transition_time:] = 1
    return World(states, transition_time, perturbation_time, regime)
