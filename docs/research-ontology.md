# Research Ontology

The Universal Biological Dynamics program needs a vocabulary that remains stable when the biological system changes.

| Object | Meaning | Observable? |
|---|---|---|
| **State** | Representation of the system at a defined time | Partially |
| **Context** | Environmental and experimental conditions | Yes, when measured |
| **Trajectory** | Ordered sequence of states | Reconstructed |
| **Transition** | Change between regimes or states | Inferred/tested |
| **Perturbation** | Deliberate change applied to the system | Experimental |
| **Response** | Measured consequence of a perturbation | Observed |
| **Attractor** | Candidate region toward which dynamics converge | Inferred |
| **Horizon** | Candidate region preceding an emergent transition | Hypothesized |
| **Uncertainty** | Limits of measurement and inference | Required |
| **Evidence** | Result surviving predefined controls | Required |

## The separation that matters

The framework distinguishes:

```
OBSERVATION ≠ STATE
STATE ≠ TRAJECTORY
TRAJECTORY ≠ CAUSAL MECHANISM
PREDICTION ≠ CAUSALITY
CORRELATION ≠ BIOLOGICAL PROOF
```

This separation is foundational. It prevents a computational representation from silently becoming a biological claim.

## Research object

A complete experiment can be represented as:

```
E = (S, E, u, Y, τ, U)
```

where:

- **S** = observed/reconstructed states;
- **E** = context;
- **u** = perturbation;
- **Y** = measured outcome;
- **τ** = temporal structure;
- **U** = uncertainty.

The objective is to determine which relationships among these objects are reproducible.
