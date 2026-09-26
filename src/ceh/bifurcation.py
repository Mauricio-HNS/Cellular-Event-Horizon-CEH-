from __future__ import annotations

import numpy as np

from .nonlinear import SaddleNode


def sweep_saddle_node(mu_values: np.ndarray) -> dict[str, np.ndarray]:
    """Return fixed-point branches and stability across a parameter sweep."""
    mu_values = np.asarray(mu_values, dtype=float)
    stable = np.full(mu_values.shape, np.nan)
    unstable = np.full(mu_values.shape, np.nan)
    for i, mu in np.ndenumerate(mu_values):
        system = SaddleNode(float(mu))
        stable_points = system.stable_fixed_points()
        unstable_points = system.unstable_fixed_points()
        if stable_points:
            stable[i] = stable_points[0]
        if unstable_points:
            unstable[i] = unstable_points[0]
    return {"mu": mu_values, "stable": stable, "unstable": unstable}
