# S7 method v1: concurrent-control RNA response contrasts in two Hamdan donors

19 November 2026. **Reviewed specification for frozen execution.** The coordinator approved the
concrete contract, exact source map, implementation and constructed verification
on 19 November; execution is authorized after the required setup checks/commit.
Owner `Nk17-P01`; analysis `Nk17-P01.s7_hamdan_response_v1`.
The [current S6 decision](S6_DECISION_V2.md) and [literature context](LITERATURE_CONTEXT.md)
own the biological rationale and published overlap. This is an exposed,
shared-source descriptive estimand extension, not exact STEM reproduction,
independent biological replication or a new global RQ.

## Question, unit and exposure

Does a positive inflamed-derived versus noninflamed-derived post-challenge RNA
contrast also describe a larger response to challenge after subtracting the
concurrent control contrast in the same patient? The biological source is paired
intestinal organoid histories from patients 4 and 83. The computational units are
deposited bulk-RNA libraries, two per history/condition/patient. Exact culture,
aliquot and technical/biological-replicate nesting is unresolved; no replicate
suffix pairing or extra independent patients is inferred. Pairing by donor does
not eliminate anatomical-site, culture-composition or preparation alternatives.

The single 24-hour endpoint measures relative RNA response magnitude, not speed,
absolute transcription, pathway activation, memory storage, barrier function or
repair. Actual paper results and Naik S2–S6C are exposed. Source metadata, the count
header and supplement have been read; no new Hamdan gene effect has been computed
for this design. Constructed-data tests/previews are separate from source results.

## Exact sources and comparison

Official GSE282444 count gzip: 4,163,489 bytes, SHA-256
`391f6e91822118b216a38966bf60f32ab7e6e1ea713150a731f5aebc7fe75575`.
It has seven annotation columns (`GeneId`, `Chromosome`, `Start`, `End`, `Length`,
`GeneName`, `GeneBiotype`) and 56 library columns. Source file hashes/acquisition
routes are retained in ignored `raw_data/hamdan2026_s7_sources_v1/` and the
contract. The exact [source map](S7_HAMDAN_SOURCE_MAP_V1.json) binds every selected
GSM, patient, history, condition, replicate suffix, case-sensitive count column,
GEO description and title. `PI` in these column names maps to the paper's **I,
inflamed-derived**, not an assumed recovered Naik-like human state.

| Patient | History | Concurrent condition | GSMs (suffix 1 / 2) | Exact count columns (1 / 2) |
|---|---|---|---|---|
| 4 | NI | control | GSM8643398 / GSM8643399 | `4_NI_control_1` / `4_NI_control_2` |
| 4 | NI | TNF10 | GSM8643396 / GSM8643397 | `4_NI_TNF10_1` / `4_NI_TNF10_2` |
| 4 | I | control | GSM8643407 / GSM8643408 | `4_PI_control_1` / `4_PI_control_2` |
| 4 | I | TNF10 | GSM8643405 / GSM8643406 | `4_PI_TNF10_1` / `4_PI_TNF10_2` |
| 83 | NI | control | GSM8643414 / GSM8643415 | `83_NI_Control_1` / `83_NI_Control_2` |
| 83 | NI | TNF10 | GSM8643409 / GSM8643410 | `83_NI-1_TNF10` / `83_NI-2_TNF10` |
| 83 | I | control | GSM8643421 / GSM8643422 | `83_PI_Control_1` / `83_PI_Control_2` |
| 83 | I | TNF10 | GSM8643416 / GSM8643417 | `83_PI-1_TNF10` / `83_PI-2_TNF10` |

Use only these 16 libraries. The other 36 baseline triplicates are a separate
design and never substitute for concurrent controls. The four patient-4 TNF100
columns are not a shared challenge and are excluded by exact names, not substring
matching. Require exact header order and unique IDs/selected columns; all selected
counts must be finite nonnegative integers. Preserve every supplied annotation
and every gene row in source order; duplicated gene symbols do not merge GeneIds.
No chromosome/biotype restriction or symbol remapping is applied.

GEO assigns GPL20301/HiSeq4000; main paper Methods name NextSeq2000. GEO hg38 and
STAR/featureCounts are retained. Main Methods name DESeq2; supplement pp. 3–4
name pairwise edgeR and STEM normalization. These discrepancies do not authorize
an inferred correction or exact-author-pipeline claim. Supplement S7 p. 18 uses
NI-control, NI-stimulated, I-control, I-stimulated; that categorical profile is
distinct from the interaction below. Its exact transformed input/gene membership
is not qualified. No published STEM/2252-peak/1904-gene set is reconstructed here.

## Normalization and estimand fixed before source effects

Normalize each patient's eight libraries **separately**, using all supplied genes.
No pooled two-patient fit, batch correction, differential-expression model or
outcome-based normalization is used.

Primary median-of-ratios (MOR): let `G+` be genes with strictly positive counts in
all eight libraries of that patient. For `g` in `G+`, compute
`q_g = exp(mean_i(log c_gi))`; for each library compute the ordinary median
`m_i = median_g(c_gi/q_g)`, averaging the two middle **ratios** for an even count.
Then `s_i = m_i / exp(mean_j(log m_j))`. An empty `G+`, nonpositive total or
nonfinite/nonpositive factor stops the run. Do not replace the reference set or
substitute another estimator. Sensitivity: `s_i = T_i / exp(mean_j(log T_j))`,
where `T_i` sums all source gene counts for that library. Both methods are
reported equally completely, with MOR designated primary prospectively.

For each gene, patient, method and history/condition, average the two normalized
counts and **then** transform: `e_hc = log2(mean_i(c_gi/s_i) + 1)`. This is not the
mean of library log values. All factors are centered to geometric mean one
within patient; `+1` is one count on that declared relative normalized scale.
Its influence at low abundance remains a limit, not a biological cutoff.

`B = e_I0 − e_NI0` (concurrent-control difference)

`P = e_IT − e_NIT` (post-challenge difference)

`R_I = e_IT − e_I0; R_NI = e_NIT − e_NI0`

**`A = P − B = R_I − R_NI`** (response interaction).

Report all four e values, both responses, B, P, A, eight raw counts and eight
normalized counts for every donor/gene/method. The log-scale A is a difference
of regularized relative log responses, not an absolute RNA increment. Positive A
can mean stronger induction or less repression; R_I/R_NI must accompany it.

## Eligibility, zeros and finite-library support

All gene rows remain exported. A gene is eligible for that patient's descriptive
distribution if **any of its eight raw counts is positive**. All-eight-zero genes
are retained and labeled structurally all-zero, with zero e/contrasts. No minimum
expression/biological-effect threshold is invented. Save any raw zero and each
condition's both-zero flag separately. No imputation or eligible-row drop.

Computational sign is positive above `1e-10`, negative below `-1e-10`, otherwise
computational zero. This tolerance is not evidence of equivalence or a meaningful
biological margin. Record zero status for B/P/R_I/R_NI/A independently from raw
zero flags. An interaction range containing zero is another, distinct statement.

For a finite spread diagnostic use each library's `log2(c/s+1)` and all 16
Cartesian combinations of one library from each of I_T, I_0, NI_T, NI_0.
Save minimum/maximum A and whether the range contains computational zero. These
are unpaired library combinations, not 16 experiments, confidence limits or a
new patient count. They need not be centered on the group-mean-then-log estimand;
no claim that their midpoint equals A is made.

## Complete summaries, display and decision

For each patient/method separately, save source/eligible/all-zero counts,
zero-flag denominators, complete 3-by-3 sign tables for P versus A and R_NI versus
R_I, A-positive constituent-response counts, range-zero counts and quantiles
(2.5/25/50/75/97.5 percentiles, linear interpolation) of B/P/R_NI/R_I/A and abs(A).
Conditional counts/fractions for P-positive records explicitly use that subset's
denominator; an empty denominator is null, not zero. No gene is a biological
replicate. No pooled patient estimate, patient-population p-value, confidence
interval, equivalence claim, hypothesis-ranking or pathway enrichment is made.

Prospective coordinator addition, before any source effects: alongside the
unchanged full eligible sign tables, report both sign tables separately for
eligible genes with **any of the eight raw counts zero** and with **none zero**.
Use only those eight raw counts, never contrast/range-zero flags. Save each
stratum's denominator, all nine counts and fractions; empty-stratum fractions
are null. This checks whether interpretation changes with raw-count zeros without
changing eligibility or introducing an abundance/effect threshold.

For each patient/gene, export total-minus-MOR A and sign/zero changes; summarize
those differences on the same raw-count eligible denominator. Both donors and
both normalizations remain even if they disagree. No selected-gene success panel.
One six-panel figure (two patient columns) displays all eligible genes: primary
P versus A, primary R_NI versus R_I, and primary versus total-count A. Show zero
and equality reference lines, full-range axes and density color scales; bins are
gene counts, not patients. PNG and vector PDF have the same content.

Positive P with nonpositive A narrows the post-contrast interpretation; positive
A with negative constituent responses describes reduced repression. Agreement
strengthens only this finite-source relative-RNA description. Donor/normalization/
zero/range dependence remains informative. None selects a causal memory mechanism
or repair target. Stop after this comparison and review, rather than adding a
score, threshold or cohort to obtain an agreeable result.

## Verification, resource bounds and execution boundary

The main implementation uses pandas/NumPy. A separate verifier reparses source
gzip/SOFT with stdlib CSV and independently computes factors, transformations,
all 16 ranges and summaries with 50-digit Decimal; it checks every exported
gene/count/annotation/flag/denominator. Scaled floating tolerance is `1e-10`.
Constructed tests cover all-zero records, even-median ratios, library depth,
post-positive/interaction-negative, monotonic equal increments, less repression,
normalization sensitivity, empty denominators and identity/count failures. Layout
previews use constructed data only. Verification success is arithmetic evidence.

Local Windows Python is sufficient in principle; no install, WSL, GPU or new
cloud service is required. Planned limits: 2 GiB process memory, 30 minutes
including independent verification, and 500 MiB new run outputs. Compressed TSVs
retain all rows. These are execution ceilings, not measured resource claims;
record actual runtime, package versions and output bytes. Stop/preserve failures
without overwriting a run or silently changing choices.
Process peak memory is recorded in main and verifier, with a 2 GiB observed-peak
check; the verifier has the remaining 30-minute timeout. Post-stage runtime/byte
checks are cooperative checks, not OS-level resource isolation.

The registered [reviewed contract](../../analysis/research/contracts/Nk17-P01.s7_hamdan_response_v1.json)
binds method, map, sources and implementation. Concrete review is complete; setup preflight, research gate and 20,416 repository
checks passed. Freeze and commit accepted hashes before invoking the research
runner. The entrypoint rejects draft status. No actual-source output, receipt,
scientific acceptance, external inquiry or publication exists for S7 at preparation.
