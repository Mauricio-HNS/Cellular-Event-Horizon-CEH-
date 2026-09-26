# Blind Horizon Detection

The next experimental layer asks whether a horizon can be detected without revealing the transition boundary to the detector.

## Protocol

1. Generate a controlled world.
2. Hide the known transition label.
3. Provide observations available up to each candidate time.
4. Calculate the CEH signal.
5. Produce candidate horizon times.
6. Compare detections with hidden ground truth.
7. Repeat under null, noise and missingness conditions.

The detector must never receive future observations when producing a candidate.

A high CEH score is not proof of a biological transition. The benchmark asks whether the score contains prospective information beyond simpler baselines and survives null controls.

For every detection, report lead time, false discoveries, missed transitions, null-world detection rate, noise robustness, missingness robustness and performance across seeds.
