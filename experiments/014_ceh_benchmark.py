"""CEH benchmark matrix: transition, no-transition, non-normal and heavy-tailed controls."""
from __future__ import annotations
import numpy as np
from ceh.benchmark import evaluate_cutoffs
from ceh.null_mechanisms import nonnormal_linear_system
from ceh.noise import heavy_tailed

def saddle_transition(seed, steps=180, sigma=0.015):
    rng=np.random.default_rng(seed); x=np.empty((steps+1,1)); x[0]=1.4
    for i in range(steps):
        mu=0.35-0.0035*i
        x[i+1,0]=x[i,0]+(mu-x[i,0]**2)*0.08+sigma*rng.normal()
    return x

def stable_control(seed, steps=180, sigma=0.015):
    rng=np.random.default_rng(seed); x=np.zeros((steps+1,1)); x[0]=1.0
    for i in range(steps):
        x[i+1,0]=x[i,0]-0.12*x[i,0]*0.08+sigma*rng.normal()
    return x

def heavy_tail_transition(seed, steps=180):
    x=saddle_transition(seed,steps,sigma=0.0)
    x[:,0]+=heavy_tailed(len(x),scale=0.012,df=2.0,seed=seed)
    return x

def run_scenario(name, trajectories, transitions):
    print(f"\n=== {name} ===")
    for row in evaluate_cutoffs(trajectories,transitions,horizon=30):
        print(f"{row.method:14s} AUROC={row.auroc:.3f} AUPRC={row.auprc:.3f} n={row.n} positives={row.positives}")

def run():
    seeds=range(12)
    run_scenario("controlled transition",[saddle_transition(s) for s in seeds],[105]*12)
    run_scenario("heavy-tailed transition",[heavy_tail_transition(s) for s in seeds],[105]*12)
    run_scenario("stable control",[stable_control(s) for s in seeds],[9999]*12)
    run_scenario("stable non-normal",[nonnormal_linear_system(steps=180,seed=s) for s in seeds],[9999]*12)

if __name__=="__main__":
    run()
