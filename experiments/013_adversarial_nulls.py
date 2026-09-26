"""Adversarial controls for CEH.

Two mechanisms are deliberately included:
1. stable non-normal dynamics can amplify fluctuations without a bifurcation;
2. spatially clustered events can be generated without assigning biological meaning.

These controls prevent CEH from equating amplification or clustering with transition.
"""
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from ceh.null_mechanisms import clustered_events, nonnormal_linear_system

trajectory = nonnormal_linear_system(steps=2000, coupling=8.0, seed=13)
A = np.array([[-1.0, 8.0], [0.0, -1.0]])
print("ADVERSARIAL NULL LABORATORY")
print("eigenvalues:", np.linalg.eigvals(A))
print("maximum state norm:", float(np.linalg.norm(trajectory, axis=1).max()))
print("final state norm:", float(np.linalg.norm(trajectory[-1])))

events = clustered_events(1000, dimensions=2, cluster_scale=0.05, seed=13)
print("clustered events:", events.shape)
print("event centroid:", events.mean(axis=0))
