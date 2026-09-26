"""Controlled nonlinear laboratory: saddle-node bifurcation.

This experiment is mathematical ground truth, not biological evidence.
"""
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from ceh.bifurcation import sweep_saddle_node
from ceh.nonlinear import SaddleNode, euler_maruyama


mu_values = np.linspace(-0.25, 1.0, 26)
branches = sweep_saddle_node(mu_values)

print("SADDLE-NODE LABORATORY")
print("mu range:", (float(mu_values.min()), float(mu_values.max())))
print("stable branch at mu=1:", branches["stable"][-1])
print("unstable branch at mu=1:", branches["unstable"][-1])

for sigma in (0.0, 0.03, 0.10):
    trajectory = euler_maruyama(
        SaddleNode(0.15), x0=0.35, dt=0.001, steps=2000, sigma=sigma, seed=11
    )
    print(
        f"sigma={sigma:.2f} "
        f"mean_last_100={trajectory[-100:].mean():.5f} "
        f"std_last_100={trajectory[-100:].std():.5f}"
    )
