# Mathematical Framework

## 1. Cellular state

Represent an observation at time t as a vector:

x_t ∈ R^d

The representation may eventually combine multiple modalities, but v0.1 uses generic numeric state vectors.

## 2. Trajectory

A trajectory is an ordered sequence:

X = (x_0, x_1, ..., x_T)

Temporal order is part of the experimental information. Any method that uses future observations to characterize an earlier state is considered leakage unless explicitly defined as retrospective analysis.

## 3. Drift

For a reference state r:

D_t = ||x_t - r||

The reference must be defined independently of future evaluation observations.

## 4. Directionality

Let:

v_t = x_t - x_(t-1)

Directionality measures persistence between consecutive velocity vectors. The v0.1 implementation uses normalized cosine similarity.

## 5. Acceleration

Let:

a_t = v_t - v_(t-1)

Acceleration captures changes in the direction or magnitude of state movement. It is not interpreted as a biological force.

## 6. Convergence

For multiple trajectories, convergence should quantify whether independent trajectories become closer in state-space than expected under an appropriate null model.

The implementation of convergence is intentionally deferred beyond v0.1 because the null model is scientifically important: a convergence score without a justified reference distribution can be misleading.

## 7. Candidate horizon

The CEH hypothesis proposes that a region may emerge when several signals jointly increase:

H_t = f(D_t, Q_t, A_t, C_t)

The function f is not assumed to be uniquely correct. Alternative formulations should be benchmarked rather than selected because they produce attractive results.

## 8. Prediction boundary

A future version may define a prospective horizon by asking whether information available at time t improves prediction of a transition occurring after t.

This is the strongest version of the hypothesis because it forces a strict temporal separation between evidence and target.
