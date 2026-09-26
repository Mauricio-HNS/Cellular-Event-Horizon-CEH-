"""Blind horizon detection on a synthetic population world."""
from ceh.population import PopulationWorldConfig, generate_population
from ceh.detector import detect_horizons

def main() -> None:
    world = generate_population(PopulationWorldConfig(entities=12, dimensions=5, steps=80))
    detections = []
    for entity in range(world.states.shape[1]):
        candidates = detect_horizons(world.states[:, entity, :], window=5)
        best = max(candidates, key=lambda c: c.score, default=None)
        detections.append(None if best is None else best.time)
    print("known transition:", world.transition_time)
    print("blind detections:", detections)

if __name__ == "__main__":
    main()
