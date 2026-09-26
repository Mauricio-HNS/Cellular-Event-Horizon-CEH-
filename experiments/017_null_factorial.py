"""Matched transition/null factorial benchmark."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from ceh.null_matrix import generate_null_matrix, write_null_results, make_nonnormal_controls

def transition(seed,steps=180,sigma=.015):
    rng=np.random.default_rng(seed); x=np.empty((steps+1,1)); x[0]=1.4
    for i in range(steps):
        mu=.35-.0035*i
        x[i+1,0]=x[i,0]+(mu-x[i,0]**2)*.08+sigma*rng.normal()
    return x

def stable(seed,steps=180):
    rng=np.random.default_rng(seed); x=np.zeros((steps+1,1)); x[0]=1.
    for i in range(steps): x[i+1,0]=x[i,0]-.12*x[i,0]*.08+.015*rng.normal()
    return x

def run():
    transitions=[transition(s) for s in range(12)]
    nulls=[stable(s) for s in range(12)]
    rows=generate_null_matrix(transitions,[105]*12,nulls,[9999]*12,horizon=30)
    _,json_path=write_null_results(rows,Path("artifacts"))
    summary={"rows":len(rows),"scenarios":["transition","no_transition"],
             "nonnormal_controls":len(make_nonnormal_controls()),"output":str(json_path)}
    Path("artifacts/ceh-null-matrix-summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__": run()
