"""Multiscale synthetic bridge.

The perturbation is intentionally abstract: it represents a physical input
without pretending to reproduce a real radiation transport calculation.
"""
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from ceh.multiscale import MultiscaleState, simulate_multiscale
from ceh.early_warning import rolling_variance, rolling_autocorrelation

time = np.arange(0.0, 20.0, 0.02)
pulse = np.exp(-((time - 4.0) / 0.12) ** 2)
perturbation = pulse + 0.15 * np.exp(-((time - 8.0) / 0.3) ** 2)

states = simulate_multiscale(
    perturbation,
    initial=MultiscaleState(0, 0, 0, 0, 0),
    dt=0.02,
)
matrix = np.array([s.as_vector() for s in states])

cellular = matrix[:, 4]
variance = rolling_variance(cellular, window=25)
autocorrelation = rolling_autocorrelation(cellular, window=25)

print("MULTISCALE PHYSICAL BRIDGE")
print("steps:", len(states))
print("peak physical input:", float(matrix[:, 0].max()))
print("peak damage:", float(matrix[:, 1].max()))
print("peak nuclear response:", float(matrix[:, 3].max()))
print("peak cellular response:", float(matrix[:, 4].max()))
print("late variance:", float(variance[-1]))
print("late lag-1 autocorrelation:", float(autocorrelation[-1]))
