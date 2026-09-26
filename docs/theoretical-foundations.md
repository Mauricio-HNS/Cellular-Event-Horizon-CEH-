# Theoretical Foundations

## 1. Scope

CEH is positioned within established mathematical and biological frameworks: dynamical systems, stochastic processes, attractor and basin analysis, bifurcation theory, state-space models, manifold representations, information theory, causal intervention and statistical inference.

The objective is not to rename these fields. It is to formulate a precise, falsifiable question at their intersection.

## 2. Observation versus state

A biological experiment does not expose the complete state of a cell.

`x_t ∈ M` represents a latent state, while `y_t = h(x_t) + η_t` represents an observation process.

This prevents the repository from treating a measured vector as biological reality.

## 3. Dynamics

A deterministic approximation is `dx/dt = f(x,t,u)`.

A stochastic formulation is `dx = f(x,t,u)dt + G(x,t,u)dW_t`.

Stochasticity belongs in the model assumptions rather than being treated only as software noise.

## 4. Attractors and basins

For `dx/dt = f(x)`, a fixed point `x*` satisfies `f(x*) = 0`. Local stability can be studied through the Jacobian `J(x*) = ∂f/∂x` evaluated at the fixed point.

CEH must not assume that a transition region is itself an attractor. It may be transient, unstable, metastable, or associated with a change in basin geometry.

## 5. Bifurcation and criticality

A parameterized system `dx/dt = f(x, λ)` can change qualitative behavior when a control parameter crosses a critical value.

Saddle-node, transcritical, pitchfork and Hopf bifurcations are candidate mechanisms that must be treated as competing explanations, not evidence for CEH.

## 6. Transition probability

For a future transition time `T`, a prospective quantity of interest is `P(T ≤ t+τ | Y_0:t)`.

A central comparison is `P(T ≤ t+τ | Y_t)` versus `P(T ≤ t+τ | Y_0:t)`.

This asks whether temporal history contributes information beyond the instantaneous state.

## 7. Information contribution

A candidate information-theoretic question is whether `I(T;Y_0:t) > I(T;Y_t)` under controlled evaluation.

This is a hypothesis. Estimation must account for finite samples, dependence, censoring, representation choice and multiple testing.

## 8. Causality

Prediction is not causation. Interventions can be represented using `do(U=u)` and evaluated through future response distributions.

The eventual program should test whether inferred transition geometry changes predictably under controlled perturbations.

## 9. CEH hypothesis

> A CEH candidate is a temporally localized region of latent state space in which the conditional distribution of future transition outcomes changes systematically, robustly and prospectively, beyond information available from the instantaneous state and beyond matched null dynamics.

This definition is intentionally difficult to satisfy.

## 10. Required evidence

- temporal integrity;
- snapshot and trajectory baselines;
- matched nulls;
- uncertainty estimates;
- representation sensitivity;
- robustness to noise and missingness;
- prospective validation;
- independent datasets;
- perturbational challenge where feasible.

## 11. Failure modes

Potential explanations for an apparent CEH include measurement artifact, batch effect, dimensionality-reduction artifact, temporal sampling artifact, generic acceleration, changing variance, selection bias, leakage, model misspecification and unrelated nonstationarity.

## 12. Scientific status

The foundations are established theoretical tools. CEH remains a hypothesis under investigation.

A successful computational benchmark is not biological validation. A biological association is not causal proof. A causal result is not automatically generalizable.

The project advances by eliminating alternative explanations, not by accumulating increasingly elaborate scores.
