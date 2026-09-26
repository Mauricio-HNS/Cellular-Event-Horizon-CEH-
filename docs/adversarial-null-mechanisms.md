# Adversarial Null Mechanisms

A serious transition detector must survive mechanisms that look like transitions but are not the target transition.

This repository therefore treats null models as mechanistic competitors, not merely shuffled datasets.

## 1. Non-normal transient amplification

A stable linear system can have strongly non-orthogonal modes. Its eigenvalues can remain negative while trajectories experience transient amplification.

The laboratory uses:

`[
A =
\begin{pmatrix}
-1 & k \
0 & -1
\end{pmatrix}
]`

All eigenvalues are -1 for any finite k, so there is no linear stability loss.

Nevertheless, stochastic forcing can produce large transient excursions.

This matters because recent work shows that pseudo-bifurcation-like early-warning signatures can arise in stochastic non-normal systems without an actual loss of stability. citeturn0search11

Therefore:

**amplification ≠ bifurcation**

## 2. Non-Gaussian noise

Classical variance and autocorrelation indicators rely on assumptions about the stochastic process. Recent mathematical work shows that alpha-stable non-Gaussian noise can invalidate classical early-warning interpretations and motivate alternative scaling-based indicators. citeturn0search7

Future CEH benchmarks should therefore include:

- Gaussian noise;
- heavy-tailed noise;
- alpha-stable noise;
- temporally correlated noise;
- state-dependent noise.

## 3. Spatial clustering without transition

Radiation track structure demonstrates that microscopic energy-deposition events can be strongly spatially clustered around DNA. citeturn0search1turn0search2

The repository now has a purely mathematical clustered-event generator.

It deliberately contains no biological labels.

The question is whether an algorithm incorrectly interprets spatial clustering alone as evidence of a state transition.

## 4. Why this changes CEH

The detector now faces three competing explanations:

```
TRUE TRANSITION
       vs
TRANSIENT AMPLIFICATION
       vs
NOISE / SPATIAL CLUSTERING
```

A CEH candidate becomes stronger only when these alternatives can be separated.

## 5. Required evidence

Future experiments should report:

- transition detection rate;
- false discovery rate;
- lead time;
- calibration;
- robustness to noise distribution;
- robustness to observation modality;
- performance against mechanistic nulls;
- incremental information beyond snapshot state.

The project should prefer a negative result over a detector that confuses these mechanisms.
