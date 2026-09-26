"""Pre-specified benchmark protocol and multiplicity correction."""
from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import numpy as np

@dataclass(frozen=True)
class Protocol:
    primary_endpoint: str = "trajectory_level_auroc"
    primary_method: str = "ceh"
    primary_comparator: str = "early_warning"
    horizon: int = 30
    window: int = 5
    alpha: float = 0.05
    bootstrap_replicates: int = 2000
    permutation_replicates: int = 2000
    train_fraction: float = 0.60
    null_mechanism: str = "matched_no_transition"
    success_rule: str = "held_out_incremental_signal_with_fdr_adjusted_p_lt_alpha"

def benjamini_hochberg(p_values):
    p=np.asarray(p_values,dtype=float)
    if p.ndim!=1: raise ValueError("p_values must be one-dimensional")
    if len(p)==0: return p.copy()
    if np.any(~np.isfinite(p)) or np.any((p<0)|(p>1)): raise ValueError("p-values must be finite and in [0,1]")
    m=len(p); order=np.argsort(p); ranked=p[order]
    adjusted=np.empty(m)
    running=1.0
    for i in range(m-1,-1,-1):
        rank=i+1
        running=min(running,rank*ranked[i]/m)
        adjusted[i]=running
    out=np.empty(m); out[order]=np.minimum(adjusted,1.0)
    return out

def write_protocol(path="docs/benchmark-protocol.json"):
    protocol=Protocol()
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(asdict(protocol),indent=2)+"\n",encoding="utf-8")
    return protocol,p

def multiplicity_table(names,p_values,alpha=0.05):
    p=np.asarray(p_values,float)
    q=benjamini_hochberg(p)
    return [{"test":str(n),"p_value":float(x),"q_value":float(y),"reject_fdr":bool(y<alpha)}
            for n,x,y in zip(names,p,q)]
