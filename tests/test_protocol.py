import numpy as np
from ceh.protocol import benjamini_hochberg, multiplicity_table

def test_bh_controls_monotone_adjustment():
    q=benjamini_hochberg([0.01,0.02,0.5])
    assert np.all((q>=0)&(q<=1))
    assert q[0]<=q[1]<=q[2]

def test_multiplicity_table():
    rows=multiplicity_table(["a","b"],[.001,.8])
    assert rows[0]["q_value"]<=rows[1]["q_value"]
    assert rows[0]["reject_fdr"] is True
