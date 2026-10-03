# A17: numerical model and observation specification

3 October 2026. This is a proposed development specification accompanying the
[A17 conditional package](../packages_2026-10-03/A17.md). The versioned kernel
is qualified on synthetic cases; no England cohort fit, founder-state selection
or scientific acceptance is claimed. Existing scripts, FU_S plans and outputs
remain intact. A later biological comparison needs its own complete contract.

## Evidence, decision and source variants

The decision is whether a persistent founder component contributes predictive
information beyond switching and observation alternatives. The
[current source accounting](../../roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md)
recovers 11 source-indexed mice at 1/2/4 weeks (4/4/3) and 16,113 retained RFP
clone measurements, size ≥2. Terminal cohorts are not longitudinal observations
of the same clone. The 58 accounting rows are mouse/channel summaries, not 58
independent animals or 58 clones. Source-indexed IDs are not recovered animal names.

The [parameter trace](../../roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/mutant_parameter_trace.json)
maps the script's `sigma_s` to the function's fast rate and `sigma_p` to its
slow rate. Script nominal net rates are 3.1/0.9 per week before day 14 and
0.5/0.01 afterward, with renewal probabilities 0.7. The script fast-founder
fraction is 0.08. The transcribed manuscript `f_S=0.16` and early slow expansion
1.1/week remain separate evidence; symbol correspondence and the parameters
used for published curves are unresolved. Do not select whichever variant fits
better and then label it source reproduction.

General birth/death/switching inference is already a methodological precedent
([Gunnarsson, Foo and Leder, 2023](https://doi.org/10.1016/j.jtbi.2023.111497)).
The accessible primary abstract distinguishes information in cell fractions
and cell numbers. Its identifiability conclusions are not imported into this
filtered, cross-sectional clone-size design; full methods were not re-audited.
The contribution here is correct implementation and an explicit observation
model for the repository's particular comparison, not a new branching theory.

## Candidate generator

Let a clone contain `(F,S)` cells at time `t`. These are latent model states,
not CD177 classes or molecular identities. In each declared time regime:

| Event | Change `(F,S)` | Propensity |
|---|---|---|
| F birth | `(1,0)` | `b_F F` |
| F loss | `(-1,0)` | `d_F F` |
| S birth | `(0,1)` | `b_S S` |
| S loss | `(0,-1)` | `d_S S` |
| F → S | `(-1,1)` | `k_FS F` |
| S → F | `(1,-1)` | `k_SF S` |

All rates are finite and nonnegative. The next event uses the sum of these
propensities and their complete cumulative distribution. A waiting time crossing
a regime boundary is discarded at that boundary and resampled under the next
regime; no event is applied after the observation time. Extinction is absorbing.
Zero event rate advances to the next regime. Size/event caps cause an explicit
failure; a capped simulation must never be treated as an observed terminal clone.

Founder state is a Bernoulli draw with probability `pi_F`, including exact zero
and one endpoints. This avoids the archived zero-based allocation's extra
fast founder. A fixed-count founder allocation would be a different declared
Monte Carlo design, not a silent substitute for a random mixture.

The intended comparison families are:

- **Persistent founder:** latent starting class mixture, `k_FS=k_SF=0`.
- **Switching:** a declared common starting state with cell-state switching.
- **Combined:** initial heterogeneity plus switching.

An exogenous time-regime change is distinct from cell-state switching and must
be handled consistently across all families. The proposed switching start state,
rate constraints and parameter-search domains still require a biological
comparison contract; this numerical stage has not chosen fitted values.

## Observation model and primary score

Write `p_theta(n,t)` for a model's full terminal size distribution, including
zero and one. Under the restricted observation assumption that every clone of
size ≥2 is equally detected without merging, the measured law is

`q_theta(n,t) = p_theta(n,t) / P_theta(N(t) >= 2)`, for `n >= 2`.

This assumption must be challenged; it is not recovered source metadata.
More generally, detection weights `w(n,t)` enter both numerator and denominator.
Merged clones require a separate measurement model. Unknown detection or merger
cannot be estimated without constraints simply to improve model fit.

The proposed primary score is mean held-out log `q` within each mouse, followed
by equal weighting across held-out mice. Use the same 11 leave-one-mouse-out
folds for every family and show each mouse/time contribution; tune all parameters
using training mice only. Internal folds on already exposed data do not create
independent validation. Fold differences share training data and are not 11
independent model-training experiments.

The earlier package's “clone-size/count distribution” does **not** license a
clone-number or extinction likelihood. The retained vectors do not, by themselves,
give the number of labelled founders, missing clones or detection probability.
Observed numbers of retained clones may describe sampling effort; model their
biological incidence only if the relevant sampling/ascertainment denominator is
qualified. No extinction estimate is inferred from a size ≥2 histogram.

Use exact/unbinned probabilities where justified. If a numerical solver groups
sizes, freeze a common complete partition and tail bin across all families.
Preserve model probability in unobserved bins. Do not renormalize at the observed
maximum, drop poorly fitted tails or replace zero model probability with an
arbitrary epsilon. A simulator-frequency histogram is not yet a qualified
likelihood; probability accuracy and tail mass need their own checks.

## Identifiability and fairness

There is a concrete nonidentifiable submodel: if `b_F=b_S=b` and `d_F=d_S=d`,
the total-size process has birth propensity `b(F+S)` and loss propensity
`d(F+S)`. Both switching events leave `F+S` unchanged. Thus every switching-rate
choice gives the same total-size law. Total sizes alone cannot distinguish
switching in this submodel. This is a mathematical property, not a negative
biological result. The equal-growth synthetic case checks its numerical consequence.

Distinct-rate regimes may contain more information, but practical recoverability
must be demonstrated under the actual observation schedule and mouse sampling.
Recovery studies must include boundary and overlapping families, alternate
starting-state assumptions, missed/merged clones and source parameter variants.
Report equivalent predictions and broad parameter regions rather than converting
optimizer convergence into identifiable cell classes.

Before a biological fit: freeze model domains and complexity controls, the
observation sensitivities, solver/probability accuracy, folds, scoring aggregation,
source variants and a defensible predictive precision criterion. A combined
model's additional flexibility cannot be called founder evidence by in-sample fit.
No clinical/biological effect threshold, sample-size guarantee or latent molecular
identity has been supplied by this stage.

## Executed numerical qualification

The [frozen contract](../../../analysis/research/contracts/A17.kernel_qualification_v1.json)
binds new code and tests, plus five synthetic cases, two seeds and 6,000
realizations per case/seed. All ten checks passed against exact single-type
mean/extinction laws, including a proportional piecewise clock and equal-growth
switching. Six-standard-error limits quantify Monte Carlo accuracy only.
Eight targeted tests cover loss, absorbing extinction, regime/observation
boundaries, switching conservation, founder endpoints, caps and probability support.

[Results](../../../analysis/research/runs/a17_kernel_qualification_v1/qualification.json)
and [receipt](../../../analysis/research/runs/a17_kernel_qualification_v1/receipt.json)
retain the actual run. Independent standard-library RK4 integration of first
moment, second moment and extinction equations agreed with the reference
quantities within `1e-8`. That is numerical verification, not biological replication.
The full biological fit remains unrun for the explicit conditions above.
