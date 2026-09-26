# CEH Research Navigator

## Purpose

The Research Navigator is the program-level control layer for Cellular Event Horizon (CEH). Its job is not to maximize code output. Its job is to determine whether the research program is accumulating credible evidence and where the next unit of engineering or scientific effort has the highest expected value.

## Core principle

```
work performed != scientific progress
```

Progress is measured through evidence:

1. Prospective validity
2. Incremental information beyond established baselines
3. Resistance to matched null mechanisms
4. Generalization across trajectories, dimensions, modalities and noise
5. Leakage-safe evaluation
6. Trajectory-level uncertainty
7. Reproducibility
8. External biological validation
9. Literature-aware novelty

## Direction vector

Each review should track the direction of these dimensions over time:

| Dimension | Question |
|---|---|
| Robustness | Does the signal survive realistic observation perturbations? |
| Incremental information | Does CEH add information beyond snapshot, temporal and early-warning baselines? |
| Null resistance | Does it disappear under matched no-transition and adversarial nulls? |
| Generalization | Does it survive held-out trajectories and unseen conditions? |
| Statistical strength | Are uncertainty and multiplicity handled at the correct unit? |
| Reproducibility | Can the result be regenerated deterministically? |
| Novelty | Is the proposed contribution distinguishable from existing literature? |
| Biological validation | Has synthetic evidence been replaced by real biological evidence? |

## Allocation rule

The navigator should prioritize work that can change the scientific conclusion.

High-value work usually includes:

- fixing leakage or invalid null designs;
- strengthening matched transition/no-transition benchmarks;
- testing incremental information jointly against strong baselines;
- adding independent synthetic mechanisms that could falsify CEH;
- validating on held-out datasets;
- identifying whether observed effects are representation or preprocessing artifacts;
- mapping claims precisely against current literature.

Low-value work includes:

- cosmetic refactors with no scientific consequence;
- adding another metric without changing the inference;
- adding increasingly elaborate synthetic layers without new falsification power;
- increasing repository complexity merely to make it look more sophisticated.

## Stop conditions

The navigator must explicitly recommend stopping or changing direction when:

- CEH does not add information beyond strong baselines;
- performance disappears under matched nulls;
- apparent gains depend on leakage;
- gains are limited to one synthetic mechanism;
- results are unstable under trajectory-level uncertainty;
- literature shows the proposed novelty is already established;
- biological validation repeatedly fails.

A negative result is a valid research outcome and must not be hidden.

## Required review output

Every periodic review should contain:

### 1. Direction
What changed since the previous review?

### 2. Evidence
What documented results support progress?

### 3. Weakness
What currently prevents a stronger scientific claim?

### 4. Highest-value next actions
Exactly three actions, ordered by expected information gain.

### 5. Deprioritize
Work that should not consume significant effort now.

### 6. Falsification status
What important hypothesis has been challenged, and what remains unchallenged?

### 7. Resource allocation
Where engineering/research effort should go next and why.

## Scientific guardrail

CEH is a research hypothesis. Computational benchmark performance is not biological evidence, clinical evidence, diagnostic evidence, prognostic evidence, or therapeutic evidence.

The navigator must never convert synthetic success into a biological claim.
