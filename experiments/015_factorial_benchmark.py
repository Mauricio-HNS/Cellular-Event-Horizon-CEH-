"""Factorial CEH benchmark: noise, missingness, dimensionality and modality."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
from ceh.benchmark_matrix import generate_matrix, write_results

def transition(seed, steps=180, sigma=0.015):
    import numpy as np
    rng=np.random.default_rng(seed)
    x=np.empty((steps+1,1))
    x[0]=1.4
    for i in range(steps):
        mu=0.35-0.0035*i
        x[i+1,0]=x[i,0]+(mu-x[i,0]**2)*0.08+sigma*rng.normal()
    return x

def run():
    trajectories=[transition(seed) for seed in range(12)]
    rows=generate_matrix(
        trajectories,[105]*12,horizon=30,
        noises=("gaussian","heavy_tail","impulse"),
        missingness=(0.0,0.1,0.3),
        dimensions=(1,4,16),
        modalities=("state","scaled","noisy","heavy_tail"),
    )
    csv_path,json_path=write_results(rows,Path("artifacts"))
    summary={"rows":len(rows),"csv":str(csv_path),"json":str(json_path),
             "factors":{"noise":3,"missingness":3,"dimensions":3,"modalities":4,"methods":4}}
    Path("artifacts/ceh-benchmark-summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    run()
