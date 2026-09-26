"""Held-out calibration and trajectory-level uncertainty benchmark."""
from __future__ import annotations
import json
from pathlib import Path
from ceh.heldout import held_out_evaluate

def transition(seed,steps=180,sigma=0.015):
    import numpy as np
    rng=np.random.default_rng(seed)
    x=np.empty((steps+1,1)); x[0]=1.4
    for i in range(steps):
        mu=0.35-0.0035*i
        x[i+1,0]=x[i,0]+(mu-x[i,0]**2)*0.08+sigma*rng.normal()
    return x

def run():
    trajectories=[transition(s) for s in range(20)]
    results=held_out_evaluate(trajectories,[105]*20,horizon=30,train_fraction=0.6)
    payload=[r.__dict__ for r in results]
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/ceh-heldout.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    for r in results:
        print(f"{r.method:14s} test_AUROC={r.auroc:.3f} AUPRC={r.auprc:.3f} FPR={r.false_positive_rate:.3f} CI95=[{r.bootstrap_auroc_low:.3f},{r.bootstrap_auroc_high:.3f}]")

if __name__=="__main__":
    run()
