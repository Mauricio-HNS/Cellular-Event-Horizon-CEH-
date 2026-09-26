# Validation Protocol

A CEH result should be treated as evidence only when it survives progressively harder controls.

## Level 1 — Synthetic identifiability

Use worlds with known transition structure and null worlds without it.

## Level 2 — Temporal integrity

Shuffle timestamps while preserving observations. A genuine temporal signal should degrade when temporal information is destroyed.

## Level 3 — Snapshot challenge

Compare CEH-derived features against a model that receives equivalent observations without trajectory information.

## Level 4 — Robustness

Repeat across seeds, noise levels, missingness patterns and parameter settings.

## Level 5 — Biological benchmark

Use public biological datasets with clearly documented labels and acquisition design. Keep evaluation data isolated from method development.

## Level 6 — Independent replication

Test the final protocol on a dataset not used to define the method.

No single successful experiment establishes the hypothesis.
