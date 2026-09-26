# Experimental Design

Universal Biological Dynamics is built around a hierarchy of evidence.

## Level 1 — Computational identifiability

Create synthetic systems where the generating dynamics are known.

Questions:
- Can the method recover a known transition?
- Can it reject a matched null?
- How sensitive is it to noise, sparsity and missingness?

## Level 2 — Temporal integrity

Freeze information at a cutoff:

```
past | CUT | future
x₀ ... xₜ | ✕ | xₜ₊₁ ... xₜ₊ₖ
```

Only the past may construct the representation.

## Level 3 — Baseline challenge

Compare the proposed representation against simpler alternatives:

- snapshot-only;
- distance-to-reference;
- temporal summary;
- established trajectory methods;
- appropriate domain-specific baselines.

A method is interesting only if it contributes information that the alternatives do not already provide.

## Level 4 — Multimodal convergence

Ask whether independent modalities identify compatible transition geometry.

Agreement is evidence of consistency, not proof of mechanism.

## Level 5 — Perturbation challenge

Where experiments exist, intervene on the system and test whether the predicted response changes.

A successful prediction does not automatically establish causality; causal interpretation requires an appropriate experimental design.

## Level 6 — Cross-system transfer

Freeze the analysis protocol and evaluate across:
- cell types;
- conditions;
- datasets;
- laboratories;
- measurement technologies.

## Level 7 — Independent replication

The strongest computational result is one that another analysis can reproduce on genuinely unseen data.

## Failure is a result

The framework records:
- false positives;
- null results;
- instability;
- modality disagreement;
- dataset-specific behavior;
- failure under perturbation.

The goal is not to force universal behavior. It is to discover where transferability actually exists.
