import numpy as np
from ceh.heldout import held_out_evaluate, trajectory_scores

def test_trajectory_scores_are_prospective():
    x=np.linspace(1,0,50)[:,None]
    s,y=trajectory_scores(x,35,10,"snapshot")
    assert len(s)==len(y)
    assert np.isfinite(s).all()

def test_heldout_split_and_metrics():
    trajectories=[np.ones((60,1))*i for i in range(8)]
    results=held_out_evaluate(trajectories,[35]*8,horizon=10,train_fraction=0.5)
    assert len(results)==4
    assert all(r.train_trajectories==4 for r in results)
    assert all(r.test_trajectories==4 for r in results)
