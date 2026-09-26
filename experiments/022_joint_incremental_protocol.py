"""Experiment 022: joint incremental-information challenge.

This experiment is intentionally computational. It does not establish biological
validity; it tests whether the candidate CEH signal adds information beyond a
joint temporal baseline under a controlled synthetic world.
"""

from ceh.joint_incremental import joint_incremental_evaluate
from ceh.synthetic import directional_trajectory, null_trajectory


def build_dataset(n_transition=12, n_null=12, seed=100):
    trajectories = []
    transition_times = []
    for i in range(n_transition):
        trajectories.append(
            directional_trajectory(
                n_steps=60,
                n_features=4,
                transition_start=35,
                noise=0.03,
                seed=seed + i,
            )
        )
        transition_times.append(35)

    for i in range(n_null):
        trajectories.append(
            null_trajectory(
                n_steps=60,
                n_features=4,
                noise=0.12,
                seed=seed + 1000 + i,
            )
        )
        # No-transition trajectory: no cutoff can become a positive event.
        transition_times.append(10_000)

    return trajectories, transition_times


if __name__ == "__main__":
    trajectories, transition_times = build_dataset()
    result = joint_incremental_evaluate(
        trajectories,
        transition_times,
        horizon=30,
        window=5,
        train_fraction=0.6,
    )
    print(result)
