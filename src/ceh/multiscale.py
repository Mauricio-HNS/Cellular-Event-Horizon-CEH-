from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class MultiscaleState:
    """Explicit state layers for a physical-to-cellular synthetic world."""
    physical: float
    damage: float
    repair: float
    nuclear: float
    cellular: float

    def as_vector(self) -> np.ndarray:
        return np.array(
            [self.physical, self.damage, self.repair, self.nuclear, self.cellular],
            dtype=float,
        )


def step_multiscale(
    state: MultiscaleState,
    perturbation: float,
    dt: float = 0.01,
    damage_rate: float = 0.8,
    repair_rate: float = 0.5,
    nuclear_rate: float = 0.25,
    cellular_rate: float = 0.15,
) -> MultiscaleState:
    """Advance a minimal causal chain: physical → damage → repair → nuclear → cellular.

    This is a synthetic mathematical laboratory, not a mechanistic biological model.
    """
    if dt <= 0:
        raise ValueError("dt must be positive")

    physical = float(perturbation)
    damage = max(0.0, state.damage + dt * (damage_rate * physical - repair_rate * state.repair))
    repair = max(0.0, state.repair + dt * (damage - state.repair))
    nuclear = state.nuclear + dt * nuclear_rate * (damage - nuclear)
    cellular = state.cellular + dt * cellular_rate * (nuclear - cellular)

    return MultiscaleState(
        physical=physical,
        damage=damage,
        repair=repair,
        nuclear=nuclear,
        cellular=cellular,
    )


def simulate_multiscale(
    perturbations: np.ndarray,
    initial: MultiscaleState | None = None,
    dt: float = 0.01,
) -> list[MultiscaleState]:
    perturbations = np.asarray(perturbations, dtype=float)
    state = initial or MultiscaleState(0.0, 0.0, 0.0, 0.0, 0.0)
    states = [state]
    for perturbation in perturbations:
        state = step_multiscale(state, float(perturbation), dt=dt)
        states.append(state)
    return states
