"""Prospective baseline challenge on a controlled synthetic world."""
from ceh.population import PopulationWorldConfig, generate_population
from ceh.baselines import snapshot_signal, temporal_signal, ceh_signal
from ceh.statistics import bootstrap_mean

def main() -> None:
    world = generate_population(PopulationWorldConfig(entities=20, dimensions=5, steps=70))
    cutoff = world.transition_time - 1
    snapshot = [snapshot_signal(world.states[: , i, :].mean(axis=0), cutoff) for i in range(20)]
    temporal = [temporal_signal(world.states[:, i, :].mean(axis=0), cutoff) for i in range(20)]
    ceh = [ceh_signal(world.states[:, i, :].mean(axis=0), cutoff) for i in range(20)]
    for name, values in (("snapshot", snapshot), ("temporal", temporal), ("ceh", ceh)):
        lo, hi = bootstrap_mean(values)
        print(name, "mean=", sum(values) / len(values), "95% bootstrap CI=", (lo, hi))

if __name__ == "__main__":
    main()
