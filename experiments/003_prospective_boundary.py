"""Experiment 003: strict past/future separation."""

from ceh.prospective import extract_window, future_displacement
from ceh.synthetic import directional_trajectory

def run(seed: int = 7, cutoff: int = 20) -> dict[str, float]:
    trajectory = directional_trajectory(seed=seed)
    window = extract_window(trajectory, cutoff)
    return {
        "cutoff": float(window.cutoff),
        "past_directionality": window.features["directionality"],
        "past_drift": window.features["final_drift"],
        "future_displacement_target": future_displacement(trajectory, cutoff),
    }

if __name__ == "__main__":
    for name, value in run().items():
        print(f"{name}: {value:.6f}")
