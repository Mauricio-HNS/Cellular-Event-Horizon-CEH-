# CEH Hypothesis

## Primary hypothesis

A dynamic region may exist in cellular state-space where subtle changes that are weakly informative in isolation become jointly directional and increasingly convergent toward an emergent state.

We call this candidate region the **Cellular Event Horizon (CEH)**.

## Falsifiable formulation

Let a cellular trajectory be:

X = {x_0, x_1, ..., x_T}

and let a candidate horizon score be:

H(X_t) = f(D_t, Q_t, A_t, C_t)

where:

- D = displacement or drift from a reference regime;
- Q = directional persistence;
- A = acceleration of state change;
- C = convergence among independent trajectories.

The hypothesis is not that a high H means disease.

The hypothesis is that, under controlled experiments, a high-horizon region may contain information about an approaching state transition that is not recoverable from an equivalent snapshot-only representation.

## Required falsification tests

- time-shuffled controls;
- null trajectories;
- observation noise;
- missing observations;
- snapshot-only baselines;
- parameter sensitivity;
- independent seeds;
- independent datasets;
- out-of-sample evaluation.

A CEH score that performs only in the ordered synthetic world is insufficient evidence.
