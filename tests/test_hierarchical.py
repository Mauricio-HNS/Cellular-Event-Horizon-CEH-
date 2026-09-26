import numpy as np
from ceh.hierarchical import hierarchical_evaluate

def test_hierarchical_returns_trajectory_counts():
    trajectories=[]
    for seed in range(8):
        rng=np.random.default_rng(seed)
        trajectories.append(np.cumsum(rng.normal(size=(80,1)),axis=0))
    rows=hierarchical_evaluate(trajectories,[55]*8,horizon=10,n_boot=50)
    assert rows
    assert all(r.trajectories==8 for r in rows)
    assert all(r.bootstrap_auroc_low<=r.bootstrap_auroc_high for r in rows)
