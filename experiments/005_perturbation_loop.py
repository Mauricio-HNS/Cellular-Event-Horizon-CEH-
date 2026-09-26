"""Synthetic perturbation-response loop.

The experiment demonstrates the architecture:
state -> context/intervention -> next state.
It makes no biological claim.
"""
import numpy as np

from ceh.perturbation import transition_step

def linear_dynamics(state, context, intervention):
    return state + 0.1 * context + intervention

def main() -> None:
    state = np.array([0.0, 0.0])
    context = np.array([1.0, -1.0])
    intervention = np.array([0.5, 0.0])
    next_state = transition_step(state, context, intervention, linear_dynamics)
    print("state:", state)
    print("next_state:", next_state)

if __name__ == "__main__":
    main()
