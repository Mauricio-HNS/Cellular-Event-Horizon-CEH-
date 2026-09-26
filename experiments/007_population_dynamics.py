"""Population-level synthetic dynamics benchmark."""
from ceh.population import PopulationWorldConfig, generate_population
from ceh.attractors import convergence_over_time
from ceh.modalities import independent_modalities

def main() -> None:
    world = generate_population(PopulationWorldConfig())
    convergence = convergence_over_time(world.states)
    modality_a, modality_b = independent_modalities(world.states)
    print("population:", world.states.shape)
    print("known intervention:", world.intervention_time)
    print("known transition:", world.transition_time)
    print("convergence_before:", float(convergence[world.transition_time - 1]))
    print("convergence_after:", float(convergence[-1]))
    print("modality_shapes:", modality_a.shape, modality_b.shape)

if __name__ == "__main__":
    main()
