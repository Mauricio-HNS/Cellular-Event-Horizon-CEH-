from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class SaddleNode:
    """Canonical saddle-node normal form: dx/dt = mu - x^2."""

    mu: float

    def drift(self, x: float | np.ndarray) -> float | np.ndarray:
        return self.mu - np.square(x)

    def fixed_points(self) -> tuple[float, ...]:
        if self.mu < 0:
            return ()
        root = float(np.sqrt(self.mu))
        return (root,) if self.mu == 0 else (root, -root)

    def jacobian(self, x: float) -> float:
        return -2.0 * float(x)

    def stable_fixed_points(self) -> tuple[float, ...]:
        return tuple(x for x in self.fixed_points() if self.jacobian(x) < 0)

    def unstable_fixed_points(self) -> tuple[float, ...]:
        return tuple(x for x in self.fixed_points() if self.jacobian(x) > 0)


def euler_maruyama(
    system: SaddleNode,
    x0: float,
    dt: float,
    steps: int,
    sigma: float = 0.0,
    seed: int = 7,
) -> np.ndarray:
    """Simulate dx = (mu - x^2)dt + sigma dW using Euler-Maruyama."""
    if dt <= 0 or steps < 1 or sigma < 0:
        raise ValueError("dt and steps must be positive and sigma must be non-negative")
    rng = np.random.default_rng(seed)
    trajectory = np.empty(steps + 1, dtype=float)
    trajectory[0] = x0
    noise_scale = sigma * np.sqrt(dt)
    for i in range(steps):
        trajectory[i + 1] = (
            trajectory[i]
            + system.drift(trajectory[i]) * dt
            + noise_scale * rng.normal()
        )
    return trajectory
