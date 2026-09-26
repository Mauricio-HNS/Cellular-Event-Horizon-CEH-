import numpy as np
from ceh.metrics import auroc, auprc
from ceh.benchmark import score_at_cutoff

def test_perfect_ranking():
    s=np.array([0.1,0.2,0.8,0.9]); y=np.array([0,0,1,1])
    assert auroc(s,y)==1.0
    assert auprc(s,y)>0.99

def test_prospective_score_ignores_future():
    x=np.arange(30,dtype=float).reshape(15,2)
    a=score_at_cutoff(x,8,"ceh")
    x[9:]=999999
    assert score_at_cutoff(x,8,"ceh")==a
