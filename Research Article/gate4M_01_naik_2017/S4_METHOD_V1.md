# S4 v1: baseline-adjusted history differences after wounding

18 November 2026. Prospective specification after coordinator-reviewed
[S2 v1](S2_RESULTS_V1.md), before S4 numerical effects or the new marker readout.
The owner/coordinator authorized this bounded S4 directly; S3 retains its stage
number and has not run. S2 results are preserved in `5bf472e` and its PDF exports
in `7eecc71`. This shared-source research is separate from the learning project.

## Biological purpose, comparison and limits

The published source links inflammatory history with later wound responses.
S2 found smaller but heterogeneous recovered-baseline RNA differences, including
the both-time expression-qualified subset. A post-wound history difference could
therefore contain a baseline offset as well as a different sampled response.
S4 asks how much the observed post-wound history/control log ratio differs from
the observed baseline ratio. It describes relative RNA in these libraries; it
does not establish a response rate, faster repair or a cell-intrinsic mechanism.

| Phase | Control libraries | Prior-inflammation libraries |
|---|---|---|
| B0: unwounded D30 baseline | GSM2440989, GSM2440990 | GSM2440991, GSM2440992 |
| W6: 6 hours after D30 wounding | GSM2440993, GSM2440994 | GSM2440995, GSM2440996 |
| W12: 12 hours after D30 wounding | GSM2440997, GSM2440998 | GSM2440999, GSM2441000 |

S1M's crosswalk confirms RNA-seq, D30, the wound-hour/history assignments and
HiSeq 2500/single layout for all 12. The exact 47,729 ordered versioned gene IDs
and every library will be retained. The biological source is the paper's pooled
epithelial preparations; the analysis unit is a deposited library (two/group).
The reported duplicate pools remain positive evidence, while exact membership,
preparation batches and animal overlap are not established. No pairing is inferred
from replicate labels. Baseline versus wound-edge compartment/selection and
cell composition can contribute to the contrasts; a common instrument/layout
does not resolve those differences or prove equal processing batches.

## One common normalization/reference scale

Estimate one joint median-of-ratios (MOR) reference over the 12 libraries using
genes positive in all 12: exponential median log ratio to each gene's geometric
mean, then center library factors to geometric mean one. Normalize every gene,
including rows excluded from factor estimation. Reuse the unchanged, already
tested S2 `normalize` and four-library `contrast` helpers, bound as code in the
new contract. Do not edit or overwrite S2 code or results.

The common scale makes the added one comparable across all six groups. It also
permits direct within-history wound/baseline contrasts. Joint MOR assumes a
sufficiently stable center of relative gene abundances; broad/asymmetric wound
changes could challenge that assumption. The sole normalization sensitivity is
joint total-count scaling: each library total divided by the geometric mean of
all 12 totals. Output ordinary CPM too. This is not an absolute-RNA measurement,
a DESeq2 model fit or a batch correction. Official source/vignette references and
the normalization convention are recorded in [S2's method](S2_METHOD_V1.md).
S4's jointly normalized baseline values may differ from S2's four-library
normalization; neither replaces or silently revises the other estimand.

## Endpoints, zeros and finite-library spread

For each phase t, retain arithmetic normalized means `H_t` and `C_t`, and
`L_t = log2((H_t + 1)/(C_t + 1))`. The primary endpoint is `A_t = L_t - L_B0`
for W6 and W12, retaining each component. Also retain each history group's
`log2((group_t + 1)/(group_B0 + 1))`; their difference equals `A_t`.
Repeat group means/contrasts under the total-count sensitivity. Provide
unregularized ratios wherever every required mean is positive, otherwise `NA`.
The one-count pseudocount is technical regularization, not a biological margin.

Show raw, MOR, total-scaled and CPM values for all 12 libraries. Flag individual,
group and phase-wide zeros; group means below one; and expression qualification.
The adjusted low-mean flag considers all four involved group means. Keep
per-group log-value ranges, all four H/C library-combination ranges per phase,
all four within-history wound/baseline ranges, and all **16** adjusted library
combinations. The adjusted minimum is `min(L_t combinations) - max(L_B0
combinations)`, and the maximum is the converse. These ranges enumerate possible
unpaired library combinations, not independent effects, matching or confidence
intervals. Retain normalization sign changes and ranges spanning/touching zero.
Use `1e-10` solely as a computational tie/boundary tolerance, as in S2.

## Expression universes, summaries and examples

At each phase, CPM ≥ 1 in at least two of its four libraries qualifies a gene.
The primary universe for each adjusted comparison is the **union of baseline
and that wound phase**. Its sensitivity is the **intersection with baseline**;
also summarize all deposited genes. This makes zero-floor/low-baseline effects
visible without discarding acute-only or wound-only expression. Qualification
does not require expression in both history groups. QC and the W6/W12 comparison
use the global three-phase union, with an all-three-qualified sensitivity.

For each comparison/universe report continuous baseline, post-wound and adjusted
effect quantiles and absolute-effect quantiles; the fraction whose absolute
post-wound effect exceeds baseline (and ties); normalization changes; low/zero
flags; adjusted 16-combination range widths and zero inclusion; and each group's
wound/baseline contrast. Describe Pearson/Spearman W6/W12 adjusted-effect profile
correspondence and opposite nonzero directions in the two common universes.
Report unadjusted W6/W12 history-effect Pearson/Spearman correlations alongside
the adjusted correlations in those same universes. Both adjusted effects subtract
the same estimated baseline, so baseline variation/error can induce or strengthen
their correspondence. It is not independent temporal corroboration. This small
diagnostic was added at coordinator review before freeze; no correlation test or
additional model is introduced.
Genes are features, never biological replicates for p-values or intervals.
No equivalence, response, recovery, kinetic or repair threshold/class is created.

Six unique examples, ties broken by exact gene ID, are selected prospectively:
maximum and minimum signed W6 adjusted effect in its union; maximum and minimum
signed W12 adjusted effect in its union; strongest opposite W6/W12 adjusted
directions among all-three-qualified genes, ranked by the smaller absolute
effect; and widest adjusted 16-combination range across eligible comparisons.
Take the next unused gene for a slot. If no opposite-direction example exists,
report that absence and leave its plot slot empty. Signed extrema are reported
honestly even if a universe lacks one sign. These selected examples do not
estimate aggregate frequencies and remain vulnerable to selection/noise.

## Exposed marker QC

S2's Xist spread motivates a prespecified readout, not an independent cohort.
Read exact-version annotation and raw/MOR/total/CPM values for the following
names in all 12 libraries. Metadata-only inspection of the existing M9 GTF found:

| Name | Exact M9 gene ID | Chromosome |
|---|---|---|
| Xist | ENSMUSG00000086503.3 | chrX |
| Ddx3y | ENSMUSG00000069045.11 | chrY |
| Eif2s3y | ENSMUSG00000069049.11 | chrY |
| Kdm5d | ENSMUSG00000056673.14 | chrY |
| Uty | ENSMUSG00000068457.14 | chrY |

Retain exact annotation coverage and any absent/ambiguous identities without
substituting another gene. The saved GEO characteristics record `Sex: female`
for these libraries; preserve that recorded field alongside the marker readout.
It is not independently verified pool membership or biological sex. Describe
consistency/discordance only; do not assign sex, infer matching, exclude a sample
or correct a batch from these markers. No new broad methods extraction is needed.

## Figures, validation and stopping point

Produce three measured figures as 300-dpi PNG and PDF: (1) library totals,
joint factors, marker log2(CPM + 1) heatmap and global-union profile correlation;
(2) baseline/post-wound components, adjusted W6/W12 comparison, union/intersection
absolute-effect distributions and MOR/total-count sensitivities; (3) all library
values for the six selected examples, with count-scale group means transformed
for display and no connecting trajectories. Annotation labels do not imply gene
function. Full gene tables are compressed losslessly to keep artifacts bounded.

Before real execution, test the full path using explicitly artificial counts,
including zeros, unequal library depths, unequal group means, missing annotation,
marker rows and exact numerical ties. Freeze/commit the method, contract and code
after synthetic verification and input preflight. A separate standard-library
verifier must reread all 12 real inputs and recompute normalization, every gene's
values/components/adjusted effects, flags, unpaired ranges, annotation/marker
joins and source labels without importing the numerical helpers. Preserve any
failed real run and amend with a new version if needed.

Pre-freeze validation: analytical zero/offset/all-combination checks and the
full 47,729-row, 12-library artificial pipeline passed. After the coordinator's
correlation diagnostic was added, the final synthetic verifier passed 7,255,847
checks, including 60 marker rows and independent correlation/rank calculations;
maximum scaled error was `2.1102e-15`. The 17-input, five-code, 16-output S4
contract passed input preflight. These are synthetic/metadata checks, not real
S4 outcomes. No S4 numerical run has occurred at this setup checkpoint.

This is exposed description: published results and S2 baseline effects/Xist
heterogeneity were viewed; the new freeze cannot remove that exposure. No S4
effect or new five-marker count profile was viewed before this specification.
Retain informative positive, negative and inconsistent findings. After the
governed run, verify/register its receipt, review the figures, update current
interpretation records and make the authorized local commit. Return for
coordinator review **before S3 or S5**. No external publication is authorized;
the earlier service-restriction history and held extraction remain unchanged.
