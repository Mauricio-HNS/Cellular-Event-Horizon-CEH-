import numpy as np
from ceh.permutation import permutation_test_trajectories

def test_permutation_is_reproducible():
    x=[]
    for seed in range(8):
        rng=np.random.default_rng(seed)
        x.append(np.cumsum(rng.normal(size=(80,1)),axis=0))
    a=permutation_test_trajectories(x,[55]*8,horizon=10,permutations=100,seed=4)
    b=permutation_test_trajectories(x,[55]*8,horizon=10,permutations=100,seed=4)
    assert [r.p_value for r in a]==[r.p_value for r in b]
