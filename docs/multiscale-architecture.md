# Multiscale Physical-to-Cellular Architecture

## Motivation

Radiation biology provides a concrete example in which spatially and temporally structured physical energy deposition propagates through molecular damage, DNA/chromatin organization and cellular response. Track-structure and microdosimetry literature explicitly argues for multiscale modelling across these levels. citeturn0search0turn0search1turn0search11

Recent work also emphasizes that nuclear architecture and genome organization participate in the dynamics of DNA-damage response. citeturn0search13

CEH therefore adds an explicit multiscale computational interface:

physical → damage → repair → nuclear → cellular

## Synthetic state model

The current implementation uses:

P(t) = physical perturbation
D(t) = damage burden
R(t) = repair activity
N(t) = nuclear state
C(t) = cellular state

The implementation is intentionally phenomenological. It is a scaffold for testing information flow, not a validated radiobiological model.

## Why the delay matters

Each layer has its own relaxation scale. Therefore the cellular trajectory can lag the physical input.

This creates an experimentally useful distinction:

snapshot:
C(t)

history:
C(0:t)

multiscale history:
P(0:t), D(0:t), R(0:t), N(0:t), C(0:t)

The research question becomes whether additional upstream information improves prediction of a future transition.

## Early-warning challenge

The project now includes baseline indicators:

- rolling variance;
- lag-1 autocorrelation;
- relaxation-rate proxy.

These are comparison baselines, not CEH components by definition.

A CEH candidate should demonstrate incremental predictive information beyond these established indicators.

## Physical realism boundary

The synthetic perturbation is not a radiation transport simulation.

A future physics module may use experimentally or computationally justified distributions for:

- energy-deposition clusters;
- linear energy transfer;
- radial dose;
- DNA target geometry;
- clustered lesions.

Existing Monte Carlo frameworks such as PARTRAC and PHITS demonstrate that explicit track-structure modelling at DNA/subcellular scales is feasible, but reproducing those systems is outside the current scope. citeturn0search6turn0search7

## Falsification path

The multiscale hypothesis fails if:

1. upstream layers add no information;
2. apparent predictive gain disappears under matched temporal nulls;
3. results depend entirely on representation;
4. noise destroys the signal;
5. snapshot state explains the future equally well.

A successful result would still not establish a biological law. It would justify a more specific experimental question.
