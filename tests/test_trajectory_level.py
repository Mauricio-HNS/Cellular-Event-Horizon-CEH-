import numpy as np

from ceh.trajectory_level import evaluate_trajectory_level


def score_norm(x):
    return np.linalg.norm(x, axis=1)


def test_trajectory_is_unit_of_inference():
    rng = np.random.default_rng(5)
    trajectories = [
        rng.normal(size=(40, 3)),
        rng.normal(size=(40, 3)),
        rng.normal(size=(40, 3)),
        rng.normal(size=(40, 3)),
    ]
    trajectories[0][30:] += 2.0
    trajectories[1][30:] += 2.0
    result = evaluate_trajectory_level(
        trajectories,
        [30, 30, 10_000, 10_000],
        score_norm,
        horizon=20,
        window=3,
    )
    assert result.n_trajectories == 4
    assert result.positives == 2
    assert len(result.scores) == 4
    assert np.isfinite(result.auroc)
    assert np.isfinite(result.auprc)


def test_no_transition_uses_observed_history_only():
    rng = np.random.default_rng(8)
    x = rng.normal(size=(20, 2))
    result = evaluate_trajectory_level(
        [x, x.copy()],
        [10_000, 10],
        score_norm,
        horizon=10,
        window=2,
    )
    assert result.scores[0].label == 0
    assert result.scores[1].label == 1
