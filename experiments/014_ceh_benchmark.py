"""Run the first dependency-light CEH benchmark."""
from __future__ import annotations
import numpy as np
from ceh.benchmark import evaluate_cutoffs
from ceh.null_mechanisms import nonnormal_linear_system

def saddle_transition(seed, steps=180):
    rng=np.random.default_rng(seed); x=np.empty((steps+1,1)); x[0]=1.4
    for i in range(steps):
        mu=0.35 - 0.0035*i
        x[i+1,0]=x[i,0]+(mu-x[i,0]**2)*0.08+0.015*rng.normal()
    return x

def stable_control(seed, steps=180):
    rng=np.random.default_rng(seed); x=np.zeros((steps+1,1)); x[0]=1.0
    for i in range(steps):
        x[i+1,0]=x[i,0]-0.12*x[i,0]*0.08+0.015*rng.normal()
    return x

def run():
    trajectories=[saddle_transition(s) for s in range(12)]
    transitions=[105]*len(trajectories)
    rows=evaluate_cutoffs(trajectories,transitions,horizon=30)
    print("Scenario: saddle-node-like synthetic transition")
    for r in rows: print(f"{r.method:14s} AUROC={r.auroc:.3f} AUPRC={r.auprc:.3f} n={r.n}")

    nulls=[nonnormal_linear_system(steps=180,seed=s) for s in range(12)]
    rows=evaluate_cutoffs(nulls,[9999]*len(nulls),horizon=30)
    print("\nScenario: stable non-normal null")
    for r in rows: print(f"{r.method:14s} AUROC={r.auroc} AUPRC={r.auprc} n={r.n}")

if __name__=="__main__":
    run()
