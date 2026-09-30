# A21 extension results and hypothesis refinement

**Vascular structural maintenance is the most grounded next mechanism to test.**
The extension completes the eligible source reanalysis and family comparison.
It does not establish Fzd4-dependent repair in normal adult capillaries.

## 1. Recovered source data distinguish structure from vascular function

Previously unavailable publisher archives were retrieved from the current
Springer media endpoint. Five workbooks provide 88 source observations across
panels; this is not 88 unique mice. Legends describe biological replicates and
nested image fields, but rows are anonymous and cannot be joined across outcomes.
Exact source cells, group labels and hashes are retained in
[source observations](tables/source_observations.tsv) and the
[workbook manifest](metadata/workbook_manifest.json).

| Source comparison | Empty / control mean | Intervention mean | Difference | Source-reported n, intervention / comparator |
|---|---:|---:|---:|---:|
| Fig. 7F, Fzd4 restoration after endothelial Foxf1 loss: nuclear beta-catenin-positive ECs | 4.83% | 45.82% | +40.99 percentage points | 4 / 5 |
| Fig. 7G, same group comparison: collagen IV area relative to CD31 area | 25.82% | 57.99% | +32.16 percentage points | 5 / 5 |
| Fig. 7E, same group comparison: Fzd4-positive gCap ECs | 9.68% | 37.37% | +27.69 percentage points | 4 / 5 |
| Fig. 7D, same group comparison: tumor size | 72.34 mm^3 | 21.40 mm^3 | -50.94 mm^3 | 11 / 7 |
| Fig. 3F, endothelial Foxf1 loss versus control: lectin area relative to CD31 area | 29.74% | 4.90% | -24.84 percentage points | 3 / 3 |

These are descriptive unpaired differences, with all observations and ranges
available in [source summaries](tables/source_summary.tsv). No new P values,
confidence intervals, equality-to-control claim or mechanistic mediation is fitted.
The first four rows concern Fzd4 restoration in tumor vessels; the last concerns
Foxf1 loss in a separate comparison. Thus functional impairment after Foxf1 loss
and structural recovery after Fzd4 restoration cannot be combined into a claim of
Fzd4-mediated perfusion rescue. Figure 7 does not measure normal capillary lineage
output. Junctional RNA in Appendix S3 adds structural context, not a barrier assay.
Source: [Bian et al., 2024](https://doi.org/10.1038/s44321-024-00064-8).

The Figure 7E workbook names uncorrected Fisher LSD while the published legend
names Tukey. The deposited values are retained; source significance symbols are
not reused. The Figure 3F axis measures an area ratio, not the fraction of vessels
counted. Both distinctions are recorded in the source mapping.

## 2. The family-wide comparison supplies no robust replacement-receptor lead

All ten Fzd symbols map uniquely to the raw matrix. Thirty-six predefined genes
were extracted for the same 5,423 endothelial cells from 12 animals as parent A21.
This extension is not a new cohort. All 3,744 overlapping parent expression rows
reconcile. Counts are summed per animal/state across technical pools, and primary
contrasts require 20 cells in each state. There are 3, 3, 2 and 3 eligible pairs
at control, day 3, day 5 and day 7; the days contain different animals.

No alternative receptor meets the frozen RNA nomination rule: replicated
transitional enrichment in at least two injury conditions, adequate detection,
and agreement at the 20- and 10-cell floors. This rule selects candidates; it is
not a powered test of receptor absence or compensation.

- Fzd6 meets the per-condition rule at one injury day with the primary floor,
  and two days at the 10-cell floor. Its day-3 mean is positive but only one of
  three pairs is positive. The lead therefore depends on eligibility and unit
  direction, rather than showing consistent enrichment.
- Fzd8 meets the rule only at day 5: two positive pairs and six detected
  transitional cells. It is lower in all three day-7 pairs, so a sustained
  replacement interpretation is unsupported.
- Fzd10 maps to the matrix but has no counts in the examined major/transitional
  states. Sparse or zero RNA observations are not proof of biological absence.

All receptors, per-animal values, detection counts and all fixed floors remain in
[paired differences](tables/paired_differences.tsv),
[contrast summaries](tables/contrast_summary.tsv) and
[candidate decisions](tables/candidate_summary.tsv). All 828 summarized contrast
directions agree under the parent author-denominator sensitivity.

The independent-state validation gate remains unmet. The inspected GSE262927
metadata supplies CAP1/CAP2, not a compatible independently annotated
major/transitional gCap comparison. Reusing its coarse labels would not validate
this substate contrast. No outcome-led reclustering was performed and no
independent replication is claimed.

## 3. Coherent receptor context narrows the biological proposal

Foxf1 is newly assessed and lower in all 11 primary transitional-minus-major
pairs, alongside the previously observed Fzd4 and Lrp6 decreases. Its day-specific
mean differences are -0.92, -1.11, -0.48 and -0.49 log2(CPM+1). This coherence is
consistent with a different endothelial maintenance context. It does not prove
that Foxf1 regulates Fzd4 in these cells, that transitional cells arose from state
0, or that reduced RNA makes Fzd4 dispensable. Axin2 detection is sparse and
canonical-response genes do not establish signaling activity or responsiveness.

The tumor rescue and atlas contrasts involve different systems and units. They
cannot identify a shared causal sequence. A newly located
[Levey et al. 2026 preprint](https://pubmed.ncbi.nlm.nih.gov/41890033/) reports
FZD4/LRP5 agonist effects on retinal pericyte coverage and barrier function.
This is unreviewed cross-organ plausibility; it does not establish a lung PDGFB
mechanism and was not pooled into this analysis.

## Hypothesis refinement and discriminating biological outcomes

**Focused working hypothesis:** Fzd4-dependent signaling sustains or restores
capillary vascular integrity during adult alveolar repair, and that competence
permits subsequent gCap renewal and aerocyte descendant production.

| Biological explanation | Discriminating outcome under an eligible receptor perturbation |
|---|---|
| Maintenance constrains later repopulation | Earlier vascular-function impairment followed by reduced traced output; temporal order alone is insufficient for mediation |
| Fzd4 directly promotes regenerative entry | Reduced early entry and later output with independently preserved or characterized maintenance |
| Fzd4 selectively supports aerocyte production | Reduced absolute aerocyte descendant yield with preserved gCap renewal and maintenance |
| Fzd4 supports vessels without affecting repair output | Vascular performance changes while both descendant outcomes remain within predefined useful-effect margins |
| Alternate Fzd receptors maintain response | Independent receptor engagement/dependency evidence; current RNA screen nominates none robustly |

The [functional design](FUNCTIONAL_DESIGN.md) preserves total lineage-output
estimands and states what would weaken each explanation. No new operational
intervention schedule, assay-specific effect margin or power estimate is invented.
Priority 3 is specified, not executed: none of the inspected sources joins adult
normal-lung Fzd4 perturbation, initial gCap identity, traced outcomes and vascular
performance. The search is bounded, not evidence that such a dataset cannot exist.

## Decision

Keep A21 conditional and focus the next functional work on vascular integrity
versus lineage specificity. Defer a compensating-receptor mechanism unless new
independent evidence supplies a candidate. Do not extend correlation, cell-floor
searches or pseudotime in these same data to fill the causal gap. Prior A19/A20
and A21 scientific evidence is preserved; the universal README is unchanged.
