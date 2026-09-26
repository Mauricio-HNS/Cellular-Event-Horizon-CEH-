import numpy as np
from ceh.detector import detect_horizons, first_candidate

def test_detector_produces_only_observation_time_candidates():
    x = np.cumsum(np.ones((20, 2)), axis=0)
    candidates = detect_horizons(x, window=4)
    assert candidates
    assert all(0 < c.time < len(x) for c in candidates)

def test_first_candidate_returns_highest_score():
    x = np.cumsum(np.ones((15, 2)), axis=0)
    candidates = detect_horizons(x, window=3)
    best = first_candidate(candidates)
    assert best is not None
    assert best.score == max(c.score for c in candidates)
