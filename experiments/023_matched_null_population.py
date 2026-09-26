"""Experiment 023: population-level matched null challenge.

Tests whether a prospective CEH signal distinguishes transition trajectories from
matched no-transition trajectories without relying on a control window inside
the same transitioning trajectory.
"""

from ceh.benchmark import evaluate_cutoffs
from ceh.null_population import matched_directional_population, matched_no_transition


def run(n=24, steps=60, features=4, transition_start=35):
    transitions, times = matched_directional_population(
        n, steps, features, transition_start, noise=0.03, seed=200
    )
    nulls = matched_no_transition(
        n, steps, features, noise=0.03, seed=1200
    )

    # Null trajectories have no event. They are represented by an event time
    # beyond the observed horizon so prospective labels remain zero.
    trajectories = transitions + nulls
    transition_times = times + [10_000] * len(nulls)

    return evaluate_cutoffs(
        trajectories,
        transition_times,
        horizon=30,
        methods=("snapshot", "temporal", "early_warning", "ceh"),
        window=5,
    )


if __name__ == "__main__":
    for row in run():
        print(row)
