"""Experiment 001: ordered world vs shuffled-time and null controls.

This is intentionally a small falsification experiment. It does not claim
biological relevance; it checks whether the transparent trajectory signals
respond to temporal structure in a controlled synthetic world.
"""

from ceh.horizon import candidate_score
from ceh.synthetic import directional_trajectory, null_trajectory, shuffle_time


def run(seed: int = 7) -> dict[str, float]:
    ordered = directional_trajectory(seed=seed)
    shuffled = shuffle_time(ordered, seed=seed + 1)
    null = null_trajectory(seed=seed)

    return {
        "ordered_total": candidate_score(ordered).total,
        "shuffled_total": candidate_score(shuffled).total,
        "null_total": candidate_score(null).total,
    }


if __name__ == "__main__":
    result = run()
    for key, value in result.items():
        print(f"{key}: {value:.6f}")
