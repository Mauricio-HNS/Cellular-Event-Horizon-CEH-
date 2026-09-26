# CEH Benchmark

The benchmark is the project's central falsification instrument.

## Question

Does a candidate Cellular Event Horizon signal identify an upcoming transition using only information available at the cutoff, and does it add information beyond simpler alternatives?

Primary comparison:

snapshot state → temporal history → established early-warning statistics → candidate CEH

CEH is treated as a hypothesis. The benchmark is allowed to reject it.

## Protocol

For each trajectory, a transition time is defined independently from the observations used by the predictor. At cutoff t, the predictor receives only Y_0...Y_t. A positive label means the known transition occurs within the prespecified horizon.

No method may inspect future observations while producing the score.

## Metrics

Primary:
- AUROC
- AUPRC

Secondary:
- detection rate at a calibration-derived threshold
- false-positive rate
- lead time
- robustness to observation noise and missingness
- calibration
- performance across independent seeds

## Adversarial controls

The benchmark must include:
1. a mathematical transition with known ground truth;
2. stable non-normal dynamics that can transiently amplify without a bifurcation;
3. noise regimes that can create misleading temporal structure;
4. no-transition controls;
5. later, real public biological trajectories with independently defined transition annotations.

A CEH signal that performs well only on its own synthetic construction is not evidence of a biological phenomenon.

## Interpretation

Success requires incremental value, not a high score in isolation. The key comparison is whether CEH remains informative after simpler temporal and early-warning baselines, and whether the result survives null mechanisms and representation changes.

Failure is a valid scientific result. The repository should preserve failed benchmarks rather than tuning the method until it wins.

## Reproducibility

Every benchmark should record:
- random seed;
- simulator parameters;
- cutoff and prediction horizon;
- observation model;
- missingness/noise settings;
- method version;
- metric definitions.
