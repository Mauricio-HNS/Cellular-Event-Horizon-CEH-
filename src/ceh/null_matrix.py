"""Factorial benchmark with transition and matched null mechanisms."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import csv, json
from pathlib import Path
from typing import Iterable
import numpy as np
from .benchmark import score_at_cutoff
from .metrics import auprc, auroc
from .noise import gaussian, heavy_tailed, impulse_contaminated
from .null_mechanisms import nonnormal_linear_system

@dataclass(frozen=True)
class NullMatrixRow:
    scenario: str
    noise: str
    missingness: float
    dimensionality: int
    modality: str
    mechanism: str
    method: str
    auroc: float
    auprc: float
    n: int
    positives: int

def _missing(x, rate, seed):
    y=np.asarray(x,float).copy()
    if not 0 <= rate < 1: raise ValueError("missingness must be in [0, 1)")
    if rate == 0: return y
    rng=np.random.default_rng(seed); mask=rng.random(y.shape)<rate; y[mask]=np.nan
    for j in range(y.shape[1]):
        finite=np.flatnonzero(np.isfinite(y[:,j]))
        if len(finite)==0: y[:,j]=0; continue
        y[:finite[0],j]=y[finite[0],j]
        for i in range(finite[0]+1,len(y)):
            if not np.isfinite(y[i,j]): y[i,j]=y[i-1,j]
    return y

def _embed(x, dim, seed):
    x=np.asarray(x,float)
    if x.ndim==1: x=x[:,None]
    if x.shape[1]==dim: return x.copy()
    rng=np.random.default_rng(seed)
    basis=rng.normal(size=(x.shape[1],dim))
    basis/=np.maximum(np.linalg.norm(basis,axis=0,keepdims=True),1e-12)
    return x@basis+rng.normal(0,.01,size=(len(x),dim))

def _modality(x, name, seed):
    if name=="state": return x.copy()
    if name=="scaled": return x*np.linspace(.7,1.3,x.shape[1])
    if name=="noisy": return x+gaussian(x.shape,.02,seed)
    if name=="heavy_tail": return x+heavy_tailed(x.shape,.01,2,seed)
    raise ValueError(f"unknown modality: {name}")

def _observe(base, noise, miss, dim, modality, seed):
    if noise=="gaussian": x=base+gaussian(base.shape,.01,seed)
    elif noise=="heavy_tail": x=base+heavy_tailed(base.shape,.01,2,seed)
    elif noise=="impulse": x=impulse_contaminated(base,.02,.08,seed)
    else: raise ValueError(f"unknown noise: {noise}")
    return _missing(_modality(_embed(x,dim,seed),modality,seed),miss,seed)

def _scores(x,t0,horizon,method):
    s=[]; y=[]
    for cutoff in range(7,min(len(x)-1,t0+horizon)+1):
        v=score_at_cutoff(x,cutoff,method,5)
        if np.isfinite(v):
            s.append(float(v)); y.append(int(0<t0-cutoff<=horizon))
    return np.asarray(s),np.asarray(y,dtype=int)

def generate_null_matrix(transition_trajectories, transition_times, null_trajectories, null_transition_times,
                         *, horizon=30, methods=("snapshot","temporal","early_warning","ceh"),
                         noises=("gaussian","heavy_tail","impulse"), missingness=(0,.1,.3),
                         dimensions=(1,4,16), modalities=("state","scaled","noisy","heavy_tail")):
    trans=list(transition_trajectories); tt=list(transition_times)
    nulls=list(null_trajectories); nt=list(null_transition_times)
    if len(trans)!=len(tt) or len(nulls)!=len(nt): raise ValueError("trajectory/transition lengths differ")
    rows=[]
    scenarios=(("transition",trans,tt),("no_transition",nulls,nt))
    for scenario, trajectories, times in scenarios:
        for seed,(base,t0) in enumerate(zip(trajectories,times)):
            for noise in noises:
                for miss in missingness:
                    for dim in dimensions:
                        for modality in modalities:
                            x=_observe(base,noise,miss,dim,modality,seed)
                            for method in methods:
                                s,y=_scores(x,t0,horizon,method)
                                if len(s)>1 and len(np.unique(y))==2:
                                    rows.append(NullMatrixRow(scenario,noise,float(miss),int(dim),modality,
                                        "matched_null" if scenario=="no_transition" else "controlled_transition",
                                        method,float(auroc(s,y)),float(auprc(s,y)),len(y),int(y.sum())))
    return rows

def write_null_results(rows: Iterable[NullMatrixRow], output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True); rows=list(rows)
    fields=list(NullMatrixRow.__dataclass_fields__)
    csv_path=out/"ceh-null-matrix.csv"; json_path=out/"ceh-null-matrix.json"
    with csv_path.open("w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=fields); w.writeheader(); w.writerows(asdict(r) for r in rows)
    json_path.write_text(json.dumps([asdict(r) for r in rows],indent=2),encoding="utf-8")
    return csv_path,json_path

def make_nonnormal_controls(count=12,steps=180):
    return [nonnormal_linear_system(steps=steps,seed=s) for s in range(count)]
