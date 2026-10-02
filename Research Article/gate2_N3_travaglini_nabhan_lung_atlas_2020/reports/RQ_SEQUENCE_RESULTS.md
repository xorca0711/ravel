# Nb4 sequential RQ analysis: results and decisions

**Completed 3 October 2026 KST.** The three scoped branches were run in order
after their specification and code were frozen. All were real count-based
analyses, followed by independent table checks. The epithelial perturbation
interaction and mature AT1 contribution remain untested because these inputs
do not contain the required linked measurements.

[Pipeline](RQ_PIPELINES.md) · [Evidence across existing studies](RQ_EVIDENCE_MATRIX.md) ·
[Literature screen](RQ_LITERATURE_SCREEN.md) · [Figures 13–15](../FIGURES.md#figure-13-captured-composition-and-c3-expression) ·
[Complete figure atlas](../figures/rq_sequence_v2/Nb4_complete_atlas.pdf)

## Decisions after the complete sequence

| Branch | Result | Narrowing decision |
|---|---|---|
| Nb4-RQ1: fibroblast composition and C3 | A fixed subtype mixture markedly attenuates the apparent C3 difference between the two primary-eligible source 10x donors. RNA-library weighting gives the same qualitative conclusion. | Keep subtype composition and within-subtype output separate. Prioritize an independently attributed subtype response; normal atlases cannot estimate an epithelial-identity interaction. |
| Nb4-RQ1b: C3 versus the A22 chemokine endpoint | The fixed panel shares C3's subtype direction in primary source/cell comparisons, but the nuclear donors and a lower-coverage source donor disagree. Gene omission does not remove these opposing contexts. | Keep C3 and chemokines as separate endpoints. Neither C3 nor a whole-complement score can stand in for general chemokine competence. |
| Nb4-RQ2: MYRF and AT1 maturation | Source AT1-versus-AT2 enrichment persists, but mesothelial discrimination is weak in the sole eligible source comparison. The separate human reference has only one eligible AT1 donor. | Retain MYRF as a reference candidate, with mesothelial context explicit. Do not advance to a maturation model without an independently measured linked endpoint. |

No new global A-number, acceptance decision or claim grade was created.
Prior unfavorable A22/A13 results are retained. These follow-ups do not rescue
their broader predictive hypotheses.

## Nb4-RQ1: what captured composition can explain descriptively

The two-population accounting identity was evaluated in every eligible
donor/assay/anatomy/protocol stratum. The reference fixes alveolar and
adventitial representation equally; it is not a claim about physiological
tissue proportions. Primary source fibroblast comparisons retain P1/P3 in
each assay. External single cells retain four donors; nuclei retain two.
These are overlapping donor identities across assays, not additive replication.

In source 10x, captured adventitial fractions are approximately 0.75 in P1
and 0.09 in P3. The P1/P3 ratio of mean per-cell C3 CPM is **4.92** for the
captured mixture and **1.27** for the equal-subtype reference. With
library-weighted pseudobulk CPM, the corresponding ratios are **3.97** and
**1.42**. These are descriptive ratios between two donors, not variance
explained, causal mediation, or a tissue-abundance estimate.

The composition departure can be positive or negative by donor. External
cells need not behave like nuclei, and the original sparse coverage remains.
All strata, including those failing the count floor, are recorded. The
lower-floor sensitivity is retained separately; it does not replace primary
eligibility.

**Narrowed RQ:** does an independently verified change in epithelial identity
alter a defined fibroblast subtype's C3 output, beyond selection of that
subtype? A subtype-by-perturbation comparison would test this; these normal
atlases only establish the need for that distinction. The new primary
literature screen also shows that adventitial C3 expression/function is
already studied, so rediscovering it is not a novelty claim.

[Stratum accounting](../runs/rq1_composition_v1/stratum_accounting.tsv) ·
[Donor accounting](../runs/rq1_composition_v1/donor_accounting.tsv) ·
[Decision and gate](../runs/rq1_composition_v1/decision.json) ·
[Run record](../runs/rq1_composition_v1/run_record.json)

## Nb4-RQ1b: a fixed endpoint is still context dependent

The inherited seven chemokines were held fixed: CCL2, CXCL1, CXCL2, CXCL3,
CXCL6, CXCL8 and CXCL12. Their panel is an unweighted mean of donor gene-wise
alveolar-minus-adventitial log2(CPM+1) contrasts. This transfers the gene
definition, not the original mixed-culture TMM normalization or its estimand.

At the primary floor, C3 and the fixed panel both favor adventitial
fibroblasts in the two eligible source 10x donors, the same two source SS2
donors, and all four eligible external single-cell donors. In both eligible
external nuclear donors, C3 remains adventitial-enriched while the fixed
panel favors alveolar fibroblasts. These directions persist for every
leave-one-gene-out panel in each primary-eligible donor.

The declared lower floor adds source 10x P2, where the C3 contrast is
**−2.68** and the fixed panel **+1.85**, again opposite. Every gene-omission
panel retains that opposition. This donor was not silently removed after
the discrepancy appeared: it remains an explicitly labeled sensitivity
case in Figure 14. Other primary donor directions remain unchanged.

**Narrowed RQ:** is a subtype-specific epithelial response associated with
C3 output, particular chemokines, or both in a defined sampling context?
Agreement of normal-subtype contrasts does not establish co-regulation.
Differences among donors, tissue preparation and nuclear/cell sampling are
confounded here; no capture-specific cause is assigned. Individual chemokines
remain visible, and whole-complement enrichment remains a separate earlier
negative portability result.

[All gene contrasts](../runs/rq1b_endpoint_v1/donor_effects.tsv) ·
[Fixed and gene-omission panels](../runs/rq1b_endpoint_v1/panel_sensitivity.tsv) ·
[Coverage](../runs/rq1b_endpoint_v1/coverage.tsv) ·
[Run record](../runs/rq1b_endpoint_v1/run_record.json)

## Nb4-RQ2: MYRF specificity does not establish mature contribution

MYRF AT1-versus-AT2 differences retain the earlier source result: mean
**+5.58** in 10x and **+7.34** in SS2 log2(CPM+1), with positive directions
in all three source donors in each assay. They are the same donors measured
by different assays.

The AT1-versus-mesothelium question has only one eligible source 10x donor,
P1, with a contrast of **+0.054**. No source SS2 pair meets even the
sensitivity floor. Thus strong AT1-versus-AT2 enrichment cannot be promoted
to broad AT1-exclusive expression.

The independent Murthy reference was rejoined from candidate epithelial
labels to three original filtered count matrices. Only DD047Q has adequate
AT1 coverage: its MYRF contrasts are **+3.71** versus candidate AT2 and
**+1.12** versus candidate mesothelium. The other donors have no or very few
candidate AT1 cells. Neither floor supplies three eligible donors. These
labels exclude MYRF from the repository marker panel but remain
computational candidates, not independent identity validation. Companion AT1
markers are archived as context, not mature outcomes. AGER is unavailable in
the curated SS2 gene universe and remains missing rather than imputed.

**Narrowed RQ:** within verified alveolar epithelium, does a MYRF-associated
component add information about independently measured mature AT1 contribution
beyond the shared transition program? The existing A8 contract remains
binding: protein, morphology or traced output must be linked to RNA in
verified biological units, with timing appropriate to association or
prediction. No eligible linked endpoint is present here, so no maturation
model was fit. The mesothelial developmental literature reinforces the
need for compartment-specific interpretation.

[Reference contrasts](../runs/rq2_myrf_v1/donor_effects.tsv) ·
[All coverage](../runs/rq2_myrf_v1/coverage.tsv) ·
[Endpoint gate](../runs/rq2_myrf_v1/endpoint_gate.json) ·
[Run record](../runs/rq2_myrf_v1/run_record.json)

## Verification and reproducibility

Six independent validation groups passed: exact mixture identities and
weights, eligibility floors, equal-stratum donor aggregation, fixed and
gene-omission panel arithmetic, **138 comparisons against earlier overlapping
source/external fits**, and the preserved mature-endpoint/replication gates.
The initial RQ renders formed a fifteen-page atlas. The final render revision
adds the declared P2 sensitivity and explicit failed coverage, with no
numerical refitting. Final figures were visually inspected.

[Validation record](../runs/rq_validation_v1/checks.json) ·
[Final render record](../figures/rq_sequence_v2/run_record.json)

The local invocation pattern is:

```powershell
& $Python analysis/scripts/run_with_environment.py --site-packages '<scientific-site-packages>' `
  "$Package/scripts/15_rq1_composition.py" --source-root '<read-only-cache-repository>'
# Then 16_rq1b_endpoint.py, followed by 17_rq2_myrf.py.
# Figure script 18 and validator 19 follow completed numerical runs.
```

The delivered versions refuse existing output directories. Choose new output
versions and a documented amendment for a new execution. Historical numerical
and figure snapshots remain immutable. The standard-library
[archive verifier](../scripts/verify_archive.py) is the repeatable read-only
check for the deposited package.

The complete feasible sequence is finished. Testing the biological interaction,
secreted/recipient function or mature contribution requires newly qualified
linked data; it cannot be supplied by additional fitting of these normal atlases.
