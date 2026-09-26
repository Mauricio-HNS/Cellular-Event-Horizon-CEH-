"""Population-level synthetic dynamical systems."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class PopulationWorldConfig:
    entities: int = 24
    dimensions: int = 4
    steps: int = 60
    transition_fraction: float = 0.55
    noise: float = 0.01
    seed: int = 17

@dataclass(frozen=True)
class PopulationWorld:
    states: np.ndarray
    regimes: np.ndarray
    transition_time: int
    intervention_time: int

def generate_population(config: PopulationWorldConfig = PopulationWorldConfig()) -> PopulationWorld:
    if min(config.entities, config.dimensions, config.steps) < 2:
        raise ValueError("entities, dimensions and steps must be >= 2")
    if not 0.2 < config.transition_fraction < 0.9:
        raise ValueError("transition_fraction must be between 0.2 and 0.9")
    rng = np.random.default_rng(config.seed)
    n, d, tmax = config.entities, config.dimensions, config.steps
    transition = int(tmax * config.transition_fraction)
    intervention = max(1, transition - 5)
    states = np.zeros((tmax, n, d))
    states[0] = rng.normal(0, 0.08, (n, d))
    target_a = np.zeros((n, d))
    target_b = np.zeros((n, d))
    target_b[:, 0] = 1.0
    target_b[:, 1] = 0.35
    regimes = np.zeros((tmax, n), dtype=int)
    for t in range(1, tmax):
        target = target_a if t < transition else target_b
        rate = 0.025 if t < transition else 0.06
        states[t] = states[t - 1] + rate * (target - states[t - 1])
        if t == intervention:
            states[t, :, 0] += 0.15
        states[t] += rng.normal(0, config.noise, (n, d))
        if t >= transition:
            regimes[t] = 1
    return PopulationWorld(states, regimes, transition, intervention)
