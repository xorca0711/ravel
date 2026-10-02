# Nb4 sequential RQ pipelines

**Owner authorized sequential execution after refinement, 3 October 2026 KST.**
These are exposed-data follow-ups: the original Nb4 directions and existing
A22/A13/A8 results were known before this specification. The three branches
below qualify narrower parts of two biological RQs. They do not create three
new global questions or replace missing intervention/function measurements.

| Order and branch | Biological question and ownership | Executable question now | Boundary |
|---|---|---|---|
| 1 · Nb4-RQ1 | Does epithelial identity change C3-associated output differently by fibroblast subtype? A22, with A13 context | How does the captured alveolar/adventitial mixture contribute to C3 RNA relative to a fixed subtype mixture? | Normal atlases cannot estimate the proposed identity-by-subtype interaction. Captured proportions are not tissue abundance. |
| 2 · Nb4-RQ1b | Does the proposed response concern C3, chemokines or both? Endpoint branch of RQ1/A22 | Does C3 share the direction of subtype contrasts with the seven fixed A22 chemokines across donors and assays? | Subtype contrast agreement is not co-regulation, secreted output, response to perturbation or recipient function. |
| 3 · Nb4-RQ2 | Does a MYRF-associated component add information about mature AT1 contribution? A8 | Does MYRF reference expression distinguish AT1 from AT2 and mesothelium, including a separate human reference? | RNA-defined labels are not independent mature contribution; a linked non-RNA endpoint remains required. |

## 1. Composition and within-subtype expression

Use original 10x/SS2 separately and the Madissoon fibroblast subset, retaining
normal lung, original distal anatomy and external matched donor/location/
assay/protocol strata. Both fibroblast subtypes must have at least 20 cells;
10 is a declared sensitivity. For each stratum, let p be the captured
adventitial fraction and mA/mD the mean per-cell C3 CPM in alveolar/adventitial
fibroblasts. Record:

- observed mixture M = (1-p)mA + p mD;
- equal-subtype reference S = (mA+mD)/2;
- composition departure M-S = (p-1/2)(mD-mA).

This is an exact accounting identity for the two captured populations, not a
causal decomposition. Repeat using total-library weights and pseudobulk CPM
to show the effect of RNA-content weighting. Do not compare absolute CPM
across SS2 and 10x as if equivalent. Average eligible stratum estimates equally
within donor/assay; report donors rather than treating strata as replicates.
Archive all excluded strata. Validate identities numerically.

A perturbation interpretation requires separately verified epithelial identity,
fibroblast subtype and amounts in paired independent biological units. The
estimand would be the difference between subtype-specific paired changes;
no sign is predicted from baseline normal-atlas contrasts.

## 2. C3 versus the inherited A22 chemokine endpoint

Keep the Nb3/A22 seven-gene panel fixed: CCL2, CXCL1, CXCL2, CXCL3, CXCL6,
CXCL8 and CXCL12. Recover all genes from raw matrices, using full-gene library
denominators and exact symbols. Never replace a missing symbol by zero.
Calculate alveolar-minus-adventitial log2(CPM+1) pseudobulk differences within
the same strata and floors as branch 1. Average strata equally by donor.

The seven-gene score is the mean of those gene-wise log differences, explicitly
a normal-atlas adaptation of the fixed panel; it does not reproduce Nb3 TMM
normalization. Report individual genes, sign agreement with C3, the fixed
panel and every leave-one-gene-out panel. A panel is unavailable if any member
is missing. Zero contrasts are uninformative, not positive agreement.
Report leave-one-donor-out cohort means; no cell-level p-values, donor-population
significance or cohort/assay pooling. Stop at endpoint separation if directions
are not portable; do not optimize panel membership for C3 agreement.

## 3. MYRF reference and mature-outcome gate

Use source normal distal AT1, AT2 and mesothelial populations, with the same
20-cell primary and 10-cell sensitivity floors. Recover the already analyzed
Murthy GSE178360 epithelial subset's candidate labels by exact sample/barcode
join to original filtered count matrices. Its marker definition excludes MYRF,
but labels remain computational candidates; no annotation independence is
claimed. Keep all three donors and failed coverage visible.

Estimate MYRF, AGER, HOPX, PDPN and AQP5 AT1-versus-AT2 and
AT1-versus-mesothelium contrasts from raw counts, by donor. Missing genes
remain missing. A three-donor threshold is required for a replicated
description. The Murthy metadata inspected before this contract shows only
one primary-eligible AT1 donor, so its role is a descriptive stress test,
not confirmatory replication. Include the A8 endpoint gate explicitly:
no linked non-RNA mature output in these atlases means no maturation model,
no RNA-versus-RNA surrogate outcome and no functional conclusion.

## Sequence, evidence and outputs

Run scripts 15, 16 and 17 in order; each creates its own immutable run folder
and depends on the preceding completed receipt. Source paths are supplied
read-only with --source-root. New calculations never overwrite earlier runs.
Each stage saves coverage, donor estimates, decision summaries, source hashes,
configuration and code snapshots. A separate figure script renders the three
executed stages. A final arithmetic validator checks the saved tables without
rerunning the numerical fits.

Read the [cross-study evidence](RQ_EVIDENCE_MATRIX.md), [literature screen](RQ_LITERATURE_SCREEN.md),
[frozen specification](../config/rq_sequence_v1.json) and
[derived questions](RQ_DERIVATION.md). Results will be reported separately.
