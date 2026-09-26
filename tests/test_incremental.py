import numpy as np
from ceh.incremental import incremental_evaluate

def test_incremental_uses_heldout_trajectories():
    x=[]
    for seed in range(8):
        rng=np.random.default_rng(seed)
        x.append(np.cumsum(rng.normal(size=(80,1)),axis=0))
    rows=incremental_evaluate(x,[55]*8,horizon=10,train_fraction=.5)
    assert rows
    assert all(r.n_test>0 for r in rows)
    assert all(np.isfinite(r.delta_auroc) for r in rows)
