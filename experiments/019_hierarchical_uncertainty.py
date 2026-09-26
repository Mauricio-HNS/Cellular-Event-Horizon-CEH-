"""Trajectory-level bootstrap benchmark."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from ceh.hierarchical import hierarchical_evaluate

def transition(seed,steps=180,sigma=.015):
    rng=np.random.default_rng(seed); x=np.empty((steps+1,1)); x[0]=1.4
    for i in range(steps):
        mu=.35-.0035*i
        x[i+1,0]=x[i,0]+(mu-x[i,0]**2)*.08+sigma*rng.normal()
    return x

def run():
    trajectories=[transition(s) for s in range(24)]
    rows=hierarchical_evaluate(trajectories,[105]*24,horizon=30,n_boot=2000)
    payload=[r.__dict__ for r in rows]
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/ceh-hierarchical.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    for r in rows:
        print(f"{r.method:14s} event_AUROC={r.trajectory_auroc:.3f} CI95=[{r.bootstrap_auroc_low:.3f},{r.bootstrap_auroc_high:.3f}] trajectories={r.trajectories}")
if __name__=="__main__": run()
