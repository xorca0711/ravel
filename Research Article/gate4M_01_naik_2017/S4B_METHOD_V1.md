# S4B v1: sensitivity to the observed baseline reference

18 November 2026. Prospective, explicitly exposed sensitivity following
coordinator-reviewed [S4](S4_RESULTS_V1.md), preserved at `628631e`. No S4B
calculation has run at this specification. S4's normalization and evidence remain
unchanged. The coordinator authorized this bounded extension before S3.

## Purpose and reference choices

S4 decomposed post-wound history differences from baseline, but exposed two
baseline Xist/Y-marker profiles despite uniformly recorded female metadata.
Both history groups contain each broad profile. That balance is not proof that
all history contrasts are biased, nor proof that the discrepancy cancels.
The question is whether the numerical baseline-adjusted contrasts depend on
which observed baseline reference is used. Coherent reference choices add an
interpretable diagnostic to S4's unstructured all-combination spread; this is
not a search for a favorable result or a correction of the source.

| Reference | History | Control | Meaning |
|---|---|---|---|
| Primary | Mean of GSM2440991/992 | Mean of GSM2440989/990 | Original two-library/group S4 baseline |
| C2/H2 reference | GSM2440992 | GSM2440990 | Observed Xist-high/Y-low profile in S4 QC |
| C1/H1 reference | GSM2440991 | GSM2440989 | Observed Xist-low/Y-high profile in S4 QC |

The alternatives have **one library per history**. They are not verified sex
strata, matched animals, independent replicates, exclusions or preferred
replacements. No sex identity, batch, exact pool membership or mechanism is
assigned. The source's female labels are retained. The alternative choices were
selected after viewing S4 QC; that exposure is part of the analysis rationale.

## Fixed inputs and arithmetic

Use only frozen S4 outputs/context. Hold the original joint MOR and joint
total-count factors, all normalized values, wound group means, post-wound effects,
47,729-gene universe, qualification flags and selected examples fixed. Do not
download raw data, refit factors or re-filter genes using an alternative reference.

For each alternative r and normalization, compute
`L0_r = log2((baseline_history_library + 1)/(baseline_control_library + 1))`.
Retain the original primary baseline and both alternatives side by side. At W6
and W12 compute `A_t,r = frozen_L_t − L0_r`, retaining frozen `L_t` and primary
`A_t`. The change is `A_t,r − A_t,primary = L0_primary − L0_r` and is therefore
**identical at both wound times by construction**. It is not a second independent
replication of reference sensitivity. Show this identity explicitly.

Retain unregularized estimates when all required terms are defined, otherwise
`NA`. Flag zeros and MOR reference values below one, including the primary
group-mean flag. These identify possible pseudocount dependence, not biological
absence. Keep continuous shifts, alternative-versus-primary sign changes, and
MOR-versus-total adjusted sign changes. Use S4's `1e-10` computational tie rule;
create no biological stability/equivalence threshold, p-value or confidence interval.

## Universes and summaries

For each wound phase retain exactly S4's all-gene, baseline/wound expression
union and baseline intersection. Qualification is copied from the frozen table,
not recomputed for one-library alternatives. Report gene counts; signed and
absolute primary/alternative adjusted-effect quantiles; signed/absolute reference
shift quantiles; primary-versus-alternative sign-change fractions; normalization
sign changes; and reference-zero/low-value fractions. Every gene remains in the
compressed full table, including rows outside display universes.

Keep S4's six selected examples in their original order and selection labels,
adding all reference outcomes without selecting new winners. One four-panel
PNG/PDF figure compares each alternative adjusted effect with the primary at
W6/W12 in the corresponding frozen expression union. Use identity lines and
describe density colours; no trajectories or implied pairs.

## Validation, interpretation and next decision

Test the new arithmetic on small artificial frozen-output fixtures, including
unequal values, zeros, undefined unregularized ratios, exact ties, copied
qualification and unchanged example selection. The real contract binds S4 input
hashes; independent standard-library verification rereads those frozen values,
recomputes primary/alternative baselines and adjusted contrasts, checks copied
fields/flags/examples and key summary fractions. Reuse the completed S4
normalization/source verification without rerunning it. Freeze/commit the new
contract/code before governed execution; preserve failed real runs if any.

Pre-freeze artificial-fixture test passed on 64 genes: 6,384 independent checks,
maximum scaled error `8.8818e-16`; deliberate summary corruption was rejected.
The fixture includes a defined baseline with an undefined unregularized wound
ratio, so the identical-shift check is applied only where the adjusted values
are defined. No real S4B values were calculated by this test.

If reference choice materially changes continuous magnitudes/directions, narrow
downstream claims about the source's baseline-adjusted transcription. If it is
stable, only this specific sensitivity is narrowed; unknown identity, biological
unit, compartment and preparation effects remain. No favorable alternative is
selected as a replacement. This remains finite-library, shared-source evidence.

After execution, verify/register the receipt, review the figure, update current
interpretation records and preserve the local results. Return for coordinator
review before S3/S5/S6. S3 source acquisition is a separate permission contingent
on runtime/storage qualification; it supplies no S4B dependency. No broad methods
extraction, safeguard change, push, PR, Notion edit or publication is authorized.
The coordinator separately authorized reproducible project-local reader/runtime
preparation after S4B; an absent preinstalled reader is not a scientific source hold.
