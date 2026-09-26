# Benchmark Matrix

The program should compare hypotheses, not only models.

| Question | Minimal baseline | CEH / UBD extension | Required evidence |
|---|---|---|---|
| Where is the system? | Snapshot | State representation | Reconstruction quality |
| Where is it going? | Snapshot + simple temporal summary | Trajectory dynamics | Prospective evaluation |
| Is a transition approaching? | Existing transition predictors | CEH | Held-out future |
| Do modalities agree? | Single modality | Multimodal state | Cross-modal consistency |
| Does intervention change the path? | Observational association | Perturbation model | Experimental response |
| Does the principle transfer? | Dataset-specific model | Cross-system dynamics | External replication |

## Benchmark rule

No new method should be evaluated only against a weak baseline selected for convenience.

The benchmark set should be frozen before final evaluation whenever practical.

## Primary metrics

Depending on the scientific question:

- prospective discrimination;
- calibration;
- effect size;
- uncertainty interval;
- null separation;
- robustness;
- cross-dataset transfer;
- perturbation-response accuracy.

A single leaderboard score is insufficient for a scientific claim.


## Factorial robustness extension

The current benchmark implementation extends the matrix across three noise mechanisms, three missingness levels, three state dimensionalities and four observation modalities, while comparing snapshot, temporal-history, early-warning and candidate CEH signals under the same prospective cutoff protocol.

This creates 432 method-condition combinations per trajectory set before aggregation. Transition labels remain independent of the observation transformation.

The extension is explicitly a robustness test, not biological evidence. Future layers must include no-transition controls under the same observation conditions, stable non-normal dynamics, calibration on held-out trajectories, trajectory-level uncertainty and public longitudinal biological datasets with independently defined transitions.
