"""Prospective incremental-information challenge."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from ceh.incremental import incremental_evaluate

def transition(seed,steps=180,sigma=.015):
    rng=np.random.default_rng(seed); x=np.empty((steps+1,1)); x[0]=1.4
    for i in range(steps):
        mu=.35-.0035*i
        x[i+1,0]=x[i,0]+(mu-x[i,0]**2)*.08+sigma*rng.normal()
    return x

def run():
    trajectories=[transition(s) for s in range(24)]
    rows=incremental_evaluate(trajectories,[105]*24,horizon=30,train_fraction=.6)
    payload=[r.__dict__ for r in rows]
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/ceh-incremental.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    for r in rows:
        print(f"{r.method:14s} vs {r.base:14s} ΔAUROC={r.delta_auroc:+.3f} ΔAUPRC={r.delta_auprc:+.3f} n={r.n_test}")
if __name__=="__main__": run()
