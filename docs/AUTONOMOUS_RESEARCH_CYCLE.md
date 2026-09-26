# Autonomous Research Cycle

The CEH repository now contains an explicit computational loop for autonomous
research navigation.

```text
OBSERVE
  ↓
AUDIT
  ↓
ASSEMBLE EVIDENCE
  ↓
FALSIFY
  ↓
IDENTIFY HIGHEST-INFORMATION GAP
  ↓
DESIGN NEXT EXPERIMENT
  ↓
IMPLEMENT
  ↓
MEASURE
  └──────────────→ OBSERVE
```

## What the director may conclude

The director may identify:

- missing controls;
- missing null mechanisms;
- insufficient incremental evidence;
- leakage or inference-unit problems;
- missing external validation;
- experiments that should be deprioritized.

It may recommend a concrete experiment, mathematical formulation, statistical
test, implementation target, or data requirement.

## What it may not conclude

The engine does not convert benchmark scores into biological truth.

In particular:

- synthetic performance is not biological validation;
- computational prediction is not clinical evidence;
- an evidence score is not a probability of validity;
- missing evidence is not negative evidence;
- one successful mechanism does not establish generality;
- novelty is not inferred from the absence of a competing implementation.

## Primary scientific objective

The highest-value question remains:

> Does a prospective CEH representation provide reproducible information about
> future cellular transition beyond strong temporal, snapshot and early-warning
> baselines under held-out trajectories and adversarial null mechanisms?

A positive computational result remains a hypothesis-supporting result only.
A failed result is retained as falsification evidence and should redirect the
research program.
