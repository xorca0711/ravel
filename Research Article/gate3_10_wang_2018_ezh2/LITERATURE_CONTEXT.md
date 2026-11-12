# Literature context and source access: Wang 2018

Review dates **11–12 November 2026, Asia/Seoul**. The first pass framed source
reproduction. The technical pass recovered the publisher supplement and audited
the day-four RNA source. [Entry point](README.md) · [Results](RESULTS_V1.md).

## Published premise and repository observation

Wang's main Results and Figures 5–7 distinguish Foxp3 instability, cytokine
changes in FOXP3-retaining cells, acute versus developmental disruption, and
residual deficient Tregs versus the tested depletion comparator. S3B–C supplies
a narrower cultured RNA result, explicitly incomplete for several inflammatory
cytokines. The [current Dp1 follow-up](../gate3_09_dupage_2015/CANDIDATE_ANALYSIS_RESULT_V1.md)
adds context-dependent loss/gain RNA directions, not a new tumor experiment.
The [Zhang interpretation](../gate3_11_zhang_2026_nk/INTERPRETATION_AND_ACCESS_V1.md)
separately concerns NK responses after local Treg removal.

Wang's S3B–C already reports positive TNF and inflammatory enrichment and the
Il10, Tgfb1 and Il2 directions. The adapted reconstruction recovers those
directions in the deposited counts and shows that the Hallmark rank patterns
are stable to the tested control and library choices. This is shared-source
evidence. Cell-cycle and apoptosis ranks move in opposite directions, raising
the remaining question of whether the RNA response persists within the same
recovered Treg state once recovery and composition are measured. The fixed
Wang/DuPage/Peeters panel reinforces context dependence, with reciprocal
Igfbp4 RNA directions but discordant or fragile transfer for other genes.
[Stage results and evidence ledger](RESULTS_V1.md).

## Primary sources and actual reading depth

| Source/version | Exact relevant locator | Use and access limit |
|---|---|---|
| [Wang et al. 2018, final article](https://doi.org/10.1016/j.celrep.2018.05.050) and [publisher supplement](https://ars.els-cdn.com/content/image/1-s2.0-S2211124718307964-mmc1.pdf) | Figures 1–7, supplement p. 2 and Figure S3 p. 5, Data and Software Availability | Relevant legends and methods read. S3 was visually inspected. The supplement supplies culture and Java GSEA details; exact normalization, ranking, mapping and the panel/sample crosswalk remain unresolved. |
| [GSE114298](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE114298), GEO files, BioSample and ENA | Nine GSMs, deposited GRCm38.78 counts, nine SRR runs | Count matrix and complete sample crosswalk verified. GEO's WT label contains four +/+ and one fl/+ library. Mouse/pool linkage and processing blocks remain unknown. |
| [DuPage et al. 2015](https://doi.org/10.1016/j.immuni.2015.01.007) and [current Dp1 source review](../gate3_09_dupage_2015/SOURCE_REVIEW.md) | Activated-Treg maintenance premise; existing S0–S3 and candidate follow-up | Reused the current repository source review, amendment and exposed results. Stored PDF located in the same collection; no new full reread or numerical rerun. |
| [Peeters et al. 2024, final article](https://doi.org/10.1016/j.celrep.2024.114724) | Figures 4–5: activation/migration and EAE; Figures 6–7: H3K27me3/transcriptomic context | Stored PDF text, relevant legends and methods excerpts read; current Dp1 reanalysis reused. Hyperactive EZH2 can improve immune suppression in an autoimmune setting. Gain is not an interchangeable inverse of cultured loss; chromatin changes are not a uniform global on/off switch. |
| [Goswami et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6118570/) | Figure 3C and Supplementary Figure 10B, with Rag1 comparison in Figure 3F | The Results describe CPI-1205/anti–CTLA-4 combination-associated changes in Tregs and effector subsets, with the cited Rag1 comparison specific to MB49. This establishes the prior combination in its tested settings. |
| [Hou et al. 2025, final publication; PMC author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC11717634/) | Figure 4 and S8C–F; Figure 5; Discussion | Relevant Results/legends read: transient ex-vivo inhibition in OT-I cells and Ezh2 knockout have different consequences. This is a CD8/ACT timing and cell-type boundary, not a replication of Treg reprogramming. |
| [Zhang et al. 2026](https://doi.org/10.1126/sciimmunol.adx4411) and [current repository results](../gate3_11_zhang_2026_nk/RESULTS.md) | Figure 3 RNA; Figures 5–7 functional/circuit evidence, as qualified in the current addendum | Stored PDF located; reused the existing full source review and released-data reconstruction. Local depletion and NK recipient biology differ from Wang's assays and systemic DTR comparator. Shared source measurements do not add replication. |

The owner-supplied Notion parent page, Results page and Discussion page were all
read. Their emphasis on context-specific plasticity, acute versus constitutive
loss, depletion versus residual cells, and checkpoint implications informed the
plan. They are reading notes, not additional experimental evidence. Private
workspace ancestry and personal planning are not copied into this public package.

## Search record and coverage

Source discovery used the connected Notion and Google Drive tools and web search.
Notion: `EZH2`, then the supplied page and its descendants. Drive: `Research Papers`
(no exact folder hit), then `EZH2`; followed the identified paper's parents.
The relevant stored collection resolved to
`Research_Article / SAP_Thesis study / Gate3 / Dupage`, containing Wang 2018,
DuPage 2015, Peeters 2024, Zhang 2026 and the DuPage 2016 plasticity review.
The two Wang/Peeters PDFs were fetched as readable text. Other source papers
were located and their sufficiently recent repository reviews reused.

Web queries included the exact Wang title with `RNA sequencing GEO` in the
initial source check; the exact title with `supplementary pdf`; and
`EZH2 regulatory T cells cancer reprogramming 2024 2025 2026 primary study`.
A subsequent Figure 6/Figure 7 and GSE114298/DESeq2 search stalled and was stopped;
it supplies no evidence. Direct publisher/PMC/GEO retrieval followed the returned
leads. The recent scan also surfaced lymphoma/ACT and tumor-cell studies; these
were not treated as fully read Treg-validation papers. No systematic citation
census or exhaustive correction/retraction audit was completed.

On 12 November the technical pass searched the accession with the exact count
filename, GEO GSM and SRA identifiers, the paper title with S3/GSEA and
supplement terms, and the DOI with `FlowRepository source data FCS tumor
measurements`. It checked the publisher supplement, the GEO file routes,
Europe PMC XML, ENA runs, BioSample records and the public article data statement.
The [source ledger](SOURCE_QUALIFICATION.md) records exact URLs, versions, sizes,
hash bindings and failed routes. Per-animal FCS and longitudinal tumor
measurements with cohort crosswalks were not located in these routes.

## Current estimand, alternatives and informative outcomes

The supported estimand is the day-four deficient-minus-control relative RNA
contrast in deposited libraries. Population composition, survival/expansion
and genotype-linked batch remain alternatives. The measured shift is partial.
The control-restricted analysis and one-library omission checks preserve the
two inflammatory rank directions and the mixed culture-state pattern. The
human Figure 2 associations cannot resolve either culture selection or a
genotype effect in this system, so the follow-up closed after the five-gene
mouse comparison.

A tumor-specific effect, active recipient stimulation, mediator necessity and
persistence each require different measurements. Wang already addresses some
of these at the functional level; the plan identifies exact residual questions
instead of claiming that RNA alone fills them. New experiments are conditional,
with actual unit, timing, assay and precision still to be qualified.
