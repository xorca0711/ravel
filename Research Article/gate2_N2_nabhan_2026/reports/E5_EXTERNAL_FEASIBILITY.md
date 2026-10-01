# E5: external evidence, metadata and descriptive pilot

**1 October 2026.** Public data support a narrower epithelial-response candidate:
**does injury/signalling context alter ERBB3 dependence of inflammatory output,
separately from the receptor requirement for AT2 renewal?** The normal-renewal,
cancer-dependency and clinical-injury claims remain separate. This review
identified an accessible epithelial perturbation dataset and ran a bounded
descriptive pilot. It does not validate the full chain proposed in the notes.

## Public-source search and dataset decisions

| Public resource | Verified availability and useful contrast | Decision / limit |
|---|---|---|
| [GSE306184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE306184), linked to [Kim et al., 2025](https://doi.org/10.1038/s42003-025-08940-w) | Fourteen human epithelial libraries; EGFR siRNA, ERBB3 siRNA and matched control under two source contexts, plus uninjured controls. Fourteen deposited read-count workbooks downloaded | **Executed descriptive pilot.** Useful receptor/context comparison; donor identities, cell identity and protocol conflicts prevent a normal-AT2 functional conclusion |
| [GSE97053](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE97053) | Nine libraries: AT2, AEP-depleted AT2 and AEP from three source-labelled patients; processed CSV archive available | **Feasible expression context candidate.** Sample titles support within-patient contrasts after alias/assay audit; no ERBB perturbation or dependency endpoint. Overall-design text mentions chromatin despite RNA-seq title/type, so verify file units before use. No analysis run here |
| [GSE135893](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135893) | Already processed in the repository's [human lung analysis](../../gate2_C3_yu_lee_choi_min_2026/trials/u5_liana_robustness/GSE135893/run_record.json) | **Reusable disease/state context, not new replication.** Donor-level AT2 receptor coverage could contextualize E5; expression does not demonstrate necessity. No duplicate full-cohort run |
| [DepMap 26Q1 release](https://forum.depmap.org/t/announcing-the-26q1-release/4606), [data structure](https://depmap.org/portal/data_page/) | Official release documents CRISPR gene effects, model annotations and omics. Model/condition/profile identifiers and default-profile flags govern joins | **Specified cancer-context branch; not executed.** Portal download access returned a verification page in this session. No file manifest, model intersection or line count was recovered. Current-release analysis would be an extension, not reproduction of the paper's unresolved 93/96-line cohort |

The linked Kim study reports context in which EGFR/ERBB3 suppression reduces
injury-associated signalling. That is a competing biological context to the
simple assertion that receptor inhibition necessarily impairs repair. Its
cultured epithelial cells are not automatically equivalent to freshly isolated
AT2 stem cells. The study's protein and injury experiments remain published
evidence, separate from the RNA calculation below.

## Metadata audit and limits

The [sample manifest](../runs/E5_metadata_v1/sample_manifest.tsv) and
[complete metadata](../runs/E5_metadata_v1/sample_metadata.json) retain the
original fields. Two libraries occur in each of seven groups. Replication
labels and library suffixes do not establish separate donors or paired
preparations, so suffixes were not treated as matching factors.

Three conflicts matter. Human epithelial titles and GRCh38 processing coexist
with mouse husbandry/restraint text. GEO calls one context “cytokine”, while
the paper describes growth-factor treatment. Processing text mentions FPKM,
whereas every workbook header and the supplementary description identify read
counts. The downloaded values are all nonnegative integers, supporting use as
**deposited count values**, without resolving the erroneous protocol fields.
The pilot retains `Cyto` as a source label and makes no exact-dose or timing
interaction claim. No uninjured EGFR/ERBB3 knockdown group is deposited.

The source workbooks contain 46,427 rows each, collapsing two repeated-symbol
rows to 46,425 symbols; no blank-symbol counts were discarded. Library totals
range from 49,379,370 to 71,965,612. All 19 frozen marker/receptor symbols are
present. Presence as a row is distinct from expression: SFTPC and SFTPA1 have
zero deposited counts, and only ABCA3 among the five AT2 markers reaches CPM 1
in both control libraries in each context. AT2/AT1 score changes therefore
cannot establish maintenance or maturation in this culture.

## What was calculated

The [contract](../config/Nb3_E5_external_v1.json) was saved after exposure to
the published findings and sample/header metadata, before inspecting expression
values. This is an exploratory, source-informed specification, not an unseen
validation. For four knockdown/context contrasts, the calculation compares
mean log2(CPM + 1) against the two context-matched controls. A positive-count
median-ratio normalization supplies a prespecified sensitivity. The six fixed
inflammatory genes are IL6, CXCL8, CCL2, CXCL10, NFKBIA and SOCS3; their mean is
a marker summary, not a full pathway or measured secretion endpoint. No
biological p-values or confidence intervals were calculated.

| Contrast | Target's own RNA, CPM scale | Inflammatory-marker mean, CPM | Same mean, normalization sensitivity |
|---|---:|---:|---:|
| EGFR knockdown, Cyto | −1.292 | −0.166 | −0.156 |
| ERBB3 knockdown, Cyto | −0.265 | −0.145 | −0.120 |
| EGFR knockdown, IR | −1.221 | +0.264 | +0.249 |
| ERBB3 knockdown, IR | −0.900 | −0.299 | −0.264 |

These are differences of mean transformed abundance, not fold changes in cell
number or proof of functional editing. The mean conceals mixed genes: in the
ERBB3/IR contrast IL6, CXCL8, CCL2 and CXCL10 decrease, while NFKBIA and SOCS3
slightly increase. The receptor/context pattern is a lead, not uniform
inflammatory suppression. Unequal target perturbation, viability, general
stress and culture identity remain rivals. Differences between IR and Cyto can
be described; an injury-versus-uninjured knockdown interaction cannot be fitted
because the latter group is missing.

[Figure 9](../FIGURES.md#figure-9-external-e5-epithelial-response-pilot) shows
the target response, individual inflammatory genes and AT2 coverage.
[Gene contrasts](../runs/E5_external_v1/gene_contrasts.tsv),
[panel contrasts](../runs/E5_external_v1/panel_contrasts.tsv),
[selected counts](../runs/E5_external_v1/selected_source_counts.tsv),
[library QC](../runs/E5_external_v1/sample_design_qc.tsv) and the
[run receipt](../runs/E5_external_v1/run_record.json) retain all results.
In the QC table, the first column named `index` contains GSM identifiers;
the figure reader explicitly validates and renames that key without changing
the saved numerical run.

## Specified epithelial-function candidate

**Hypothesis.** ERBB3 contributes to epithelial renewal in a competent AT2
context but can support inflammatory output in an injured epithelial context.
This is a proposed context dependence, not a demonstrated sign reversal of the
same endpoint: Nb3 measures organoid coverage, whereas the external pilot
measures RNA in a different culture. ERBB2 remains a separate renewal/cancer
arm because this RNA deposit has no ERBB2 knockdown group.

**Discriminator.** A comparable epithelial population with verified identity,
receptor engagement and matched baseline/injury perturbations must connect
renewal/mature output with secreted inflammatory output. A coherent interaction
under that design would support the hypothesis. An effect explained entirely
by loss of viable cells, unequal engagement or culture identity would weaken
it. The public pilot can prioritize contrasts; it cannot replace those outcomes.

**Cancer branch.** Before a DepMap fit, freeze one release and explicit lung
subtype inclusion, validate model/condition/default-omics mappings, and report
the matched model count. Prespecify ERBB2 and ERBB3 gene effects, relevant
receptor/genotype/copy-number context, and an AT2-associated expression score
that excludes the tested receptor genes. Compare associations within an
eligible lung subtype, with model-level dependence and small-cohort limits
explicit. An AT2-like expression association would not identify a cell of
origin or establish normal-cell dependence. A drug-specific clinical injury
mechanism would still need separate evidence.

**Review decision.** Retain E5 as a distinct, now more specific epithelial
function candidate. It is not A9's fibroblast AREG-recipient question, A22's
epithelial-to-fibroblast identity question, or A23's phosphate hypothesis.
No new global ID or claim grade is assigned by this pilot.
