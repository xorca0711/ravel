# Bounded execution specification v1

3 November 2026. Exposed follow-through to [CUT_OR_FILL_PLAN](CUT_OR_FILL_PLAN.md).
This specification freezes implementation choices before new numerical outcomes.
It is not human scientific acceptance. Existing source/cluster/score outcomes,
coverage tables and the source inventories inspected in this session are exposed.
No effect margin, novel mechanism, independent replicate or power is invented.

## A5 metadata refresh

Refresh GEO series/filelist, the complete author tree, Zenodo 16412867 file list,
public Shiny entry HTML and bioRxiv version metadata. Compare against the existing
56-library crosswalk and unchanged filelist hash. Endpoint: source and map
availability, not programme expression. Library is a source unit; mouse identity
remains unknown. Stop before matrix analysis without a barcode/library/mouse/author
state export and reconciliation of 56 libraries versus 55 mice. Existing fixed Guo
component, exclusions, activated-AT2 reference and 500-UMI scale remain binding.
The public HTML inspection does not audit a live websocket session or prove that
no author export exists elsewhere. All source requests retain acquisition hashes.

## A17 recoverability and observation specification

The biological units remain the 11 source-indexed mice at terminal weeks 1/2/4
(4/4/3), with their actual retained-clone counts. No empirical size outcome is fit.
The intended families have the same finite nonnegative birth/loss rates and the
same time boundary at week 2. Persistent: pi in [0,1], both switching rates zero.
Switching: one common starting cell, F or S assessed separately, nonnegative
switching rates. Combined: pi in [0,1] plus switching. States have no molecular
identity. Equal growth, zero switching and founder endpoints remain valid overlaps.
No source evidence supplies biologically justified upper rate bounds or a fitted
complexity penalty; numerical fixtures are not substituted as biological domains.

The two source variants are retained: script pi=.08, early slow net=.9/week;
manuscript transcription pi=.16, early slow net=1.1/week. The latter is not claimed
to reproduce published curves. Fast early net=3.1, late fast/slow=.5/.01; renewal
=.7 gives birth=net*.7/.4 and loss=net*.3/.4. Illustrative distinct-rate switching
fixtures use (kFS,kSF)=(.1,.2), common S; (.2,.1), common F; combined pi=.08 with
(.1,.2). These finite examples test observation ambiguity, not rate plausibility.

A backward probability-generating-function coefficient ODE supplies sizes 0..64
and the exact remaining tail >=65; repeat at 128 and regroup as a numerical
qualification (tolerance 2e-7), with independent scalar no-switching PGF checks.
Integrate the late regime before the early regime for backward composition.
Keep probabilities of zero and one, then condition on >=2. No observed maximum,
arbitrary likelihood epsilon or omitted tail is used.

Equal detection of all size>=2 clones is a conditional assumption, not recovered
metadata. With unqualified size/time-specific detection w, any positive candidate
laws q_i admit the same selected law: h(n)=min_i q_i(n), w_i(n)=h(n)/q_i(n),
then normalize h. This holds on the complete partition and, pointwise, on the
unbinned countable support. It is an existence counterexample, not fitted detection.
Report uniform-detection pairwise KL separately; it may distinguish fixed laws.
Simulate 200 datasets per family, seed 20261103, with the actual per-mouse retained
sample sizes, and equal-mouse log loss under the common observed law. Computational
replicates are not mice. This added solver/ascertainment question reuses the prior
kernel/denominator checks rather than rerunning them.

Stop empirical mechanism selection if actual ascertainment remains unqualified.
Unknown weights or merger cannot be fit to improve a cohort result. A future
conditional prediction run requires bounded justified observation assumptions,
fair domains, identical leave-mouse-out folds and training-only fitting; its result
would remain model-conditional. Retained counts do not identify extinction or
founder incidence. Uniform-detection model indistinguishability is not presumed.

## A25 supported exploratory comparison

Primary scope: source-labelled male microglia, cortex only, >=20 cells per mouse,
3/2/4 mice at 3/18/24 months. Cortex is a declared single region with all nine male
mice; no region is selected by new model outcomes. Other regions and females are
outside this run. Old females are absent. Source processing/cohort confounding
and previous cluster/outcome exposure remain. No source cluster enters a predictor.

Use the hash-verified official raw.X integer-valued full-gene read counts, not
integrated/clipped X or assumed UMIs. Join exact official cell IDs via the frozen
bridge; require count totals equal deposited n_counts. Per cell log1p(CPM) uses
its own full-library total. Every outer fold holds one entire mouse. Training
only: equal-mouse mean/variance/detection; genes detected in >=10% weighted cells,
then top 500 variance genes (stable input-order tie break); standardized weighted
PCA, five components, deterministic signs, unit training variance. No test cell
enters feature/latent fitting. All models in a fold share that representation.

1. Endpoint mixture: diagonal Gaussian components estimated with equal-mouse
   weights from young and old training mice. At each of the three ages, fit its
   mixing proportion on training animals by bounded one-dimensional likelihood.
2. Flexible continuous age: quadratic interpolation of each Gaussian mean and
   log variance across the three observed ages. At these ages this is exactly
   an independent Gaussian moment fit per age, allowing nonmonotone mean and
   dispersion. It does not assume a straight-line age response.
3. Additional RNA component: same fixed endpoint components, plus one diagonal
   Gaussian fitted to middle-age training mice with weighted EM. Initialize its
   moments at the middle-age Gaussian and weight .5; other weights inherit half
   of the endpoint mixture. Endpoint-age predictions remain the endpoint model.

All diagonal variances have the same .05 floor on the standardized PC scale.
EM has a 300-iteration budget and 1e-8 likelihood convergence tolerance; report
nonconvergence and withhold interpretation if it occurs. No seed/feature/model
sweep follows an unfavorable result. These are explicit representation families,
not all possible continuous or discrete biological models; held-out comparisons
address their predictive adequacy and contain a capacity/assumption limitation.

Primary endpoint: per-mouse mean held-out negative log density in the common
five-dimensional representation, then equal-mouse mean. Both extra-versus-endpoint
and extra-versus-continuous gains are retained, together with absolute losses and
every mouse. No p-value or equivalence claim. Deleting one mouse from the saved
loss aggregation describes sensitivity, not independent fold-training uncertainty.
For both middle-age holdouts, report extra-component posterior occupancy and the
cosine between reconstructed gene-space extra-minus-endpoint directions. This is
a coherence diagnostic, not a fate/function or discrete-state validation.
Two middle-age mice leave one for fitting in each relevant fold. Mixed gain,
unstable direction or weak support cannot establish a distinct middle-age state.
Even consistent gain is only conditional RNA-configuration evidence in this scope.

## A30 saved-state join qualification

Inputs are the immutable state table and independently exported barcode/QC table.
Audit actual shared keys, raw-key uniqueness and join multiplicity by donor and
compartment. Do not join by row order, row count or score similarity. If no
provenance key associates a saved state with a raw barcode, stop the dependent
lineage/doublet and expression/detection-matched null. This does not falsify the
existing all-cell or restricted association; it limits a new measurement audit.
No old loaded-panel size-only null is expanded. A qualified future amendment must
keep donor and Monte Carlo uncertainty, population restrictions and coverage losses
separate. Activation exclusion, causal induction, residency and regulatory-function
claims remain unsupported. Original keyed membership or a separately validated
reconstruction would be the enabling input, not another activation-bin analysis.
