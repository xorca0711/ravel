# Navarro remaining-work follow-up and public human-cell context

10 November 2026. Owner **Nn26-P01**, ungated.
[Study home](../README.md) · [Figure gallery](../FIGURES.md) ·
[Frozen follow-up plan](PLAN.md) · [Original animal results](../RESULTS.md) ·
[Original pooled RNA results](../RNA_RESULTS.md) · [Validation](VALIDATION.md)

The later [question-development assessment](../QUESTION_DEVELOPMENT_20261110.md)
uses these completed results to consider recipient responses and sustained
neuronal output. It launches no new numerical stage and leaves this report's
findings and limitations intact.

**The bounded follow-up is executed.** Public-source refresh did not resolve
Navarro's alias/dose/donor gaps. Additional diagnostics preserve the two
unmatched animal statistics. Newly sourced human GEO matrices support a separate
donor-paired RNA description, with a consistent GZMB pattern and mixed IFNG
directions. They do not supply missing D25K, aged-brain or injury-repair data.

## 1. Refreshed sources and unresolved identity

NCBI BioSample attributes are unchanged from the original snapshot. The main
BioSample still describes mixed ages and provides no cell-to-mouse assignment.
ENA still lists 20 project runs, including the six named main IL-10 libraries.
The author repository remains at `c08010bb29f0cb9b56143a25f6a2b1c28692cf70`.
Zenodo's latest-version endpoints still resolve to data record 17594828 and code
record 18174039; the inspected author tree has no external hallmark `.rda`.

This refresh therefore cannot connect all eight RDS aliases to six published
main libraries or establish the WT1/Mut1 and WT50/Mut50 numerical doses. It also
cannot recover the authors' downstream Micro_types exclusions or unpool mice.
WT5/Mut5 retains its earlier indirect figure/code association, not a newly
verified barcode-to-dose join.

[Source/version snapshot](../../../analysis/research/runs/nn26_public_source_followup_v1/source_refresh.json)
and [exact input manifest](../../../analysis/research/runs/nn26_public_source_followup_v1/input_manifest.json).
Primary sources: [BioProject](https://www.ebi.ac.uk/ena/browser/view/PRJNA1365936),
[processed objects](https://zenodo.org/records/17594828),
[archived code](https://zenodo.org/records/18174039),
[author tree at the inspected commit](https://github.com/PalomaNavarro/TargetingImmuneCellsSVZ/tree/c08010bb29f0cb9b56143a25f6a2b1c28692cf70).

## 2. Residual animal-test diagnostics

The new diagnostic verified all **40 source observations** in the two affected
comparisons against raw workbook XML. It did not omit observations, round their
values, search exclusions or replace the original analyses. Seven fixed method
conventions were retained for each comparison; tie-ignoring references are
marked inapplicable when ties exist.

| Endpoint / comparison | Observed n | Reported P | Existing exact absolute-tail P | Follow-up disposition |
|---|---|---|---|---|
| Open-field D25K–control | 15 / 13 | 0.59942 | 0.594163 | No applicable tested convention reproduces the reported rounding; workbook formulas omit the first listed observation in both groups |
| IFITM3 WT–control | 6 / 6 | 0.0173 | 0.025974 | No tested convention matches; the reported rounding is not attainable under the standard two-sided untied exact rank distribution for these sample sizes |

The open-field mean formulas are `AVERAGE(D95:D108)` and `AVERAGE(E95:E108)`.
The source observations begin at row 94. Cached means are 2022.8333 and 1918.0;
the unchanged complete lists give 1987.0 and 1940.3333. This identifies the mean
formula discrepancy, not the cause of the reported P-value mismatch. The IFITM3
finding restricts the standard exact-test explanation; it does not identify
the authors' undocumented software settings or prove which source is wrong.

The existing **38/40** exact-rank reconciliation remains the current total.
Original analysis-project settings or corrected source data would be needed to
resolve the residuals. Direct cognition null tests, mixed nesting doses, neural
marker scale/nesting ambiguities and the lack of WT cognition remain unchanged.
[All conventions](../../../analysis/research/runs/nn26_residual_diagnostics_v3/test_conventions.csv) ·
[Formula/support audit](../../../analysis/research/runs/nn26_residual_diagnostics_v3/diagnostic.json).

## 3. New public deposits: qualified separate context

[Canaria et al. (2026)](https://doi.org/10.1038/s41586-026-11176-1), Fig. 2g–h,
already report RNA contrasts for a different engineered IL-10R agonist in human
PBMCs and activated T cells. Fig. 2e is a separate protein-secretion assay.
The published selectivity mechanism is an exposed premise; this reanalysis
does not infer TYK2 dependence from transcript counts or reproduce the paper's
edgeR differential-expression model. The GEO series are reused from that same
human study, not independent replications of each other or of D25K in aged brain.

| Deposit | Material and design retained | Data qualified |
|---|---|---|
| [GSE318914](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE318914) | Quiescent and LPS-stimulated PBMCs; 3, 6, 24 h; PBS, IL-10, IL-10-Fc, ms-IL10R agonist; three reported donors | 72 explicitly joined libraries; 19,984 protein-coding genes |
| [GSE318915](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE318915) | T cells; 6, 24, 48 h; the same four treatment labels; three reported donors | 36 explicitly joined libraries; 19,984 protein-coding genes |

Every matrix column joins to a GSM through the deposited `Library name` field,
not sample ordering. Counts are nonnegative integers; all four treatments are
present in each donor/time/activation stratum. D1/D2/D3 are matched **within
series only**. Six unique people, matched donors across series, donor ages/sexes,
or a dose mapping for every library are not inferred from these labels.
The publisher's 24-hour figure caption provides assay context; it does not
replace missing sample-level protocol/dose metadata for every deposited time.

The authorized download acquired both complete processed matrices and family
SOFT records. Large sequencing reads and the original 2.2-GB Navarro RDS were
not required. Exact hashes and retrieval URLs are retained through the input
manifest and frozen raw-input provenance; raw public inputs remain ignored.
[Sample crosswalk](../../../analysis/research/runs/nn26_public_source_followup_v1/public_sample_crosswalk.csv) ·
[Qualification](../../../analysis/research/runs/nn26_public_source_followup_v1/public_deposit_qualification.json).

## 4. Donor-paired RNA results

The [human-context plan](HUMAN_CONTEXT_PLAN_V1.md) fixed STAT3, SOCS3, TNF, IFNG
and GZMB, all times/conditions and four contrasts before execution. CPM uses
the sum of the **19,984 deposited protein-coding gene counts**, not all aligned
reads or an inferred whole-transcriptome total. Differences are paired
log2(CPM+1), not log2 fold changes from a DE model. Every donor is retained;
the range is descriptive and no P value or confidence interval is reported.

| T-cell marker / time | Median IL-10–PBS | Donors above / below zero | Median agonist–IL-10 | Donors above / below zero |
|---|---:|---|---:|---|
| GZMB, 6 h | +1.118 | 3 / 0 | −0.959 | 0 / 3 |
| GZMB, 24 h | +2.003 | 3 / 0 | −1.760 | 0 / 3 |
| GZMB, 48 h | +1.217 | 3 / 0 | −1.173 | 0 / 3 |
| IFNG, 6 h | +0.036 | 2 / 1 | −0.091 | 1 / 2 |
| IFNG, 24 h | +0.192 | 2 / 1 | −0.044 | 1 / 2 |
| IFNG, 48 h | +0.141 | 2 / 1 | −0.063 | 1 / 2 |

GZMB consistently increases with IL-10 relative to PBS and is lower under the
agonist than IL-10 in these reported T-cell donors. IFNG is small and mixed
across donors. A lower agonist–IL-10 difference does not establish equivalence
to PBS. Full agonist–PBS and IL-10-Fc contrasts, including exceptions, remain in
the figures and tables. PBMC TNF depends on time/activation; at 24 h the
IL-10–PBS median is −0.327 in LPS-stimulated PBMCs with one donor increasing,
versus −1.280 in quiescent PBMCs with all three decreasing. The other fixed
markers and complete earlier-time comparisons remain visible.

This provides a donor-resolved contextual example of selective RNA responses
under a **different engineered agonist**. Bulk composition, activation, time,
donor variation and compositional normalization remain alternatives to a broad
functional interpretation. RNA is not secretion, repair or cognitive benefit;
there is no D25K, age factorial or aged-brain intervention in these deposits.

[540 measurements](../../../analysis/research/runs/nn26_human_context_description_v1/measurements.csv) ·
[540 paired contrasts](../../../analysis/research/runs/nn26_human_context_description_v1/paired_contrasts.csv) ·
[180 complete summaries](../../../analysis/research/runs/nn26_human_context_description_v1/contrast_summaries.csv) ·
[Figures](../FIGURES.md#external-human-cell-context).

## 5. Verification, access record and remaining decisions

All three new stages have successful, hash-verified receipts. The human stage
performed 1,368 independent arithmetic checks: NumPy versus streamed library
sums, scalar versus vector normalization, log-ratio reconstruction of paired
differences and ordered-value median checks. Both new PNGs were visually
inspected; all SVG/PNG outputs and original evidence are retained. No script
warning was recorded in the human stage.

| Stage | Freeze | Receipt |
|---|---|---|
| Source refresh / public matrix qualification | `557eb98` | [Receipt](../../../analysis/research/runs/nn26_public_source_followup_v1/receipt.json) |
| Residual statistic diagnostic | `557eb98` | [Receipt](../../../analysis/research/runs/nn26_residual_diagnostics_v3/receipt.json) |
| Human-cell context description | `8b6aef4` | [Receipt and environment](../../../analysis/research/runs/nn26_human_context_description_v1/receipt.json) |

Search/access date: **10 November 2026, Asia/Seoul**. Exact targeted web queries
included `"D25K" "GEO" brain IL10`, `"D25K" "BioProject" aged brain`,
`"TargetingImmuneCellsSVZ" "WT50"`, `"s41586-026-11176-1" authors`, and
`"Engineered TYK2 dependence" "Fig. 2" RNA`. Entrez queries were
`D25K OR (IL10 AND subventricular)` in BioProject and
`GSE318914[ACCN] OR GSE318915[ACCN]` in GDS. The BioProject query returned the
original project only; that bounded search does not prove no other dataset
exists. Six BioSamples, current ENA project metadata, author GitHub head/tree,
Zenodo latest-version endpoints and both complete GEO family/count files were
checked. Browser-page errors for GEO/Nature did not imply absent data: direct
GEO text/FTP HTTPS routes succeeded. Publisher indexed text supplied the
Canaria Fig. 2 caption and Data availability; no full-paper or supplementary
functional reproduction is claimed. This was a source/eligibility search,
not a comprehensive novelty review or new experiment proposal.

| Remaining question | What would permit further work |
|---|---|
| Exact Navarro dose/library mapping | An explicit alias/barcode/accession/dose crosswalk, especially the extra WT50/Mut50 conditions |
| Exact authors' microglial plots/score | Downstream retained-cell identities and the original external hallmark file/version |
| Two source P discrepancies | Original analysis-project options and/or corrected numerical source tables; no observation deletion to force agreement |
| Population D25K effects or age modification | Independent eligible D25K/WT biological units and matched young/old treatment contrasts |
| Injury repair or cognition mediation | A suitable injury/recovery or perturbation/linkage design, not additional resampling of current cells |

No author contact, human acceptance, claim-grade promotion or global RQ was
created. Current feasible work is complete; the listed holds are retained.
