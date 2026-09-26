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
