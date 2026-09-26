"""Calibrate blind CEH detection against shuffled-time null worlds."""
from ceh.population import PopulationWorldConfig, generate_population
from ceh.null_benchmark import calibrate_against_time_null

def main() -> None:
    world = generate_population(PopulationWorldConfig(entities=1, dimensions=5, steps=80))
    result = calibrate_against_time_null(world.states[:, 0, :], window=5, permutations=250)
    print("known transition:", world.transition_time)
    print("observed maximum CEH:", result.observed_score)
    print("null mean:", float(result.null_scores.mean()))
    print("empirical p:", result.empirical_p)
    print("null z-score:", result.z_score)

if __name__ == "__main__":
    main()
