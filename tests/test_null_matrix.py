import numpy as np
from ceh.null_matrix import generate_null_matrix

def test_null_matrix_contains_both_scenarios():
    x=[np.ones((40,1)) for _ in range(2)]
    rows=generate_null_matrix(x,[20]*2,x,[9999]*2,horizon=10,
        noises=("gaussian",),missingness=(0,),dimensions=(1,),modalities=("state",))
    scenarios={r.scenario for r in rows}
    assert scenarios=={"pooled_transition_vs_no_transition"}
