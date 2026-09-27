# A2 interpretation correction, 27 September 2026

**Subsequent source recovery:** [P1](../../../docs/roadmap_runs/2026-09-27/P1_SCREEN_DESIGN.md) resolves part of the design uncertainty below: the four wells are mixture splits and regular medium includes recombinant EGF. Remaining uncertainty concerns the preparation/lot crosswalk, quantitative ligand conditions and causal route.

This dated review supersedes the inference and next-budget recommendations in
`LEG2_DEPTH_STANDARDISED_RESULTS.md` and the older status in `STAGE5_SYNTHESIS.md`.
Their numerical artifacts, specifications and historical bytes are preserved.
See the [repository audit](../../../docs/audits/2026-09-27-rq-rationale/REPORT.md).

## What the two legs support

The depth-standardized machinery/activation estimate is **positive and not
statistically established**: rho 0.2931, nominal p 0.185637 in 22 donors. This is
not no coupling, a bound on its maximum size, or an equivalence result. The
change from the raw-detection estimate demonstrates sensitivity to the measurement.
It does not identify how much was caused by technical depth. The arbitrary 0.4
diagnostic threshold is a gate, not proof that residual confounding is absent.
Comparing correlations to control pairs does not itself test their difference
or exclude unmeasured co-regulation.

Leg 1 retains the observed AREG median +0.036 and ITGB6 median -0.938 log2 CPM.
The AREG estimate gives no demonstrated decrement in this design, rather than
evidence of zero epithelial contribution. Its partial perturbation, fixed target
positions, unresolved preparations and possible recipient ligand supply limit
interpretation. Cross-species, separately normalized mean logCPM values do not
quantify relative secreted ligand supply or show how much protein was removed.
Recipient AREG RNA supports a plausible autocrine rival; it does not prove active
autocrine signalling. The post hoc size/content checks do not establish equivalence
or eliminate viability, cell-state, guide or position effects for ITGB6.

## The 100-molecule recommendation does not follow from the test

For a realized integer library, exact expected detection at budget B is
`1 - choose(N-K,B)/choose(N,B)`. Its conditional value can depend on N even when
the plug-in ratio K/N is held fixed. That is finite-population sampling, not by
itself a defective depth standardization.

Under an ideal molecule-sampling model `K ~ Binomial(N,p)`, averaging that
conditional expectation gives **`1-(1-p)^B` for every N >= B**, including N=B.
The [independent exact enumeration](../../../docs/audits/2026-09-27-rq-rationale/evidence.json)
checks this identity. The old test also inserts fractional `rate*N` into a
gamma-function extension; fractional molecules are not a hypergeometric sample.
Its conditional spread therefore does not prove that B=1000 is invalid or that
B≈100 is the only valid next analysis. Smaller budgets also change the estimand
and sensitivity. This identity assumes ideal sampling; it does not establish
depth-independent biology in a heterogeneous real cohort.

Do not launch a 100-molecule pass merely to cross a significance/depth threshold.
Any further measurement study needs an independently motivated estimand, count
sampling model, retention/saturation diagnostics and a decision it could change.
Neither an additional null nor an additional positive result in this cohort
would settle delivery versus abundance.

## Biological decision remains open

The present two legs do not contrast spatial delivery at controlled effective
ligand dose. Delivery and abundance can jointly determine response. A discriminating
design should vary source proximity or presentation and ligand dose separately,
verify receptor engagement, and account for recipient ligand production and
alternative ligands. Spatial RNA alone supplies neither effective ligand dose nor
a causal delivery test. The completed descriptive stages remain complete; a
further association screen requires a new, explicit purpose.
