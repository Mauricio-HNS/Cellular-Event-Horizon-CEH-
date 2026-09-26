"""Generate a controlled synthetic world with known transition timing.

This is a methodological benchmark, not a biological model.
"""
from ceh.world import WorldConfig, generate_world

def main() -> None:
    world = generate_world(WorldConfig(dimensions=5, steps=60, noise=0.01))
    print("states:", world.states.shape)
    print("perturbation_time:", world.perturbation_time)
    print("transition_time:", world.transition_time)
    print("known_regime_change:", world.transition_time)

if __name__ == "__main__":
    main()
