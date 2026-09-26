# CEH Benchmark

The benchmark is the project's central falsification instrument.

## Primary comparison

**snapshot state → temporal history → early-warning statistics → candidate CEH**

Every method receives only observations available at the prospective cutoff. The transition label is generated independently from the predictor.

## Benchmark matrix

| Scenario | Purpose |
|---|---|
| Controlled nonlinear transition | Known mathematical ground truth |
| Heavy-tailed transition | Test sensitivity to non-Gaussian noise |
| Stable control | No transition; expose false alarms |
| Stable non-normal system | Transient amplification without eigenvalue instability |

The next benchmark layer should add missingness, observation-model changes, multimodal representations and real public biological trajectories with independently defined transition annotations.

## Primary endpoints

- AUROC
- AUPRC

These are ranking metrics. They do not prove a biological mechanism.

## Secondary endpoints

- false-positive rate at a threshold calibrated without test trajectories;
- detection rate;
- lead time;
- robustness to noise and missingness;
- calibration;
- cross-seed reproducibility;
- incremental information beyond snapshot and established temporal indicators.

## Adversarial principle

A method that performs well only on the synthetic dynamics that inspired it has not demonstrated generality.

Non-normal transient amplification, heavy-tailed noise, observation artifacts and no-transition worlds are therefore treated as mandatory challenges.

## Interpretation

CEH is a candidate construct, not an established biological phenomenon. A benchmark can reject it.

The strongest result is not a high score in isolation. It is reproducible incremental information beyond simpler alternatives that survives matched null mechanisms and representation changes.

A negative result is also scientifically valuable: the repository should preserve it and revise the hypothesis rather than tune around it.
