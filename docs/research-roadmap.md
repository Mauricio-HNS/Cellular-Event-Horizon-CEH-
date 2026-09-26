# Research Roadmap

## 0. Formal hypothesis
- define the state-space assumptions;
- define candidate horizon components;
- define uncertainty;
- define null models before evaluating results.

## 1. Synthetic falsification
- ordered transition worlds;
- null worlds;
- shuffled time;
- variable noise;
- missing observations;
- trajectory branching;
- multiple independent trajectories.

## 2. Baselines
Compare against:
- snapshot-only features;
- simple distance-to-reference models;
- standard trajectory representations;
- established trajectory inference methods where appropriate.

The purpose is not to replace existing methods without evidence. CEH must demonstrate incremental information.

## 3. Prospective evaluation
Given observations only up to time t, test whether CEH features contain information about a later transition.

No future observations may influence the representation at t.

## 4. Biological datasets
Use public datasets with documented experimental design. Begin with datasets where temporal structure or experimentally induced state transitions can be defended.

## 5. Multimodal extension
Investigate whether independent modalities converge on the same candidate transition region.

## 6. Independent replication
Freeze the method and test it on data not used during development.

## 7. Translation
Only after reproducible computational evidence should biological validation or translational research be considered.

### Success criterion

The project succeeds scientifically if the hypothesis becomes clearer through evidence.

A robust negative result is preferable to an unsupported positive claim.
