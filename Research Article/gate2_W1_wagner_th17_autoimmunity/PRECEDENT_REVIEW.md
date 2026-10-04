# Six-branch precedent review — 4 October 2026

This continues the interrupted review after planning commit `1527bea`.
Published-source interpretation is separated from the repository's
[first metadata result](RESULTS.md). All six branches remain proposed; this
bounded review neither accepts a global RQ nor certifies novelty.

## Comparison and decision ledger

| Branch | Closest inspected comparison and strongest rival | What remains informative | Contribution / readiness |
|---|---|---|---|
| P01 | Wagner's network scores; eFPA directly compares network integration with cognate enzyme expression. Depth, expression structure and information sharing can explain apparent gains. | A fixed Th17-specific baseline comparison, with biological blocks and graph construction handled honestly; biochemical ground truth is still absent. | Measurement validation. General network-versus-expression superiority is already tested elsewhere. |
| P02 | Wagner's reaction heterogeneity and Wang's PGAM perturbation already establish nonuniform glycolytic behavior. Mapping, orientation and aggregation are rivals. | Reconstruct declared reaction effects and expose what the chosen pathway summary hides; retain weak/discordant effects. | Source replication and representation comparison. PGAM score-sign ambiguity blocks importing its signature as a reference. |
| P03 | Puleston tests lineage markers across cell divisions and reports dysregulation beyond slowed proliferation. Growth-only explanations were already examined. | Compare the exact Wagner DFMO context and endpoints with genetic Odc/hypusine contexts; distinguish aggregate shift, within-division response and durable regulatory function. | Context/model discrimination. Bulk RNA cannot settle selection or cell conversion. |
| P04 | Wagner measures endpoint-dependent JMJD3 effects. Li and Liu report different context-dependent differentiation consequences of Jmjd3 loss. | A direct genotype-by-treatment interaction on each prespecified endpoint and scale, with uncertainty and design support. | Endpoint-specific source replication. A significant/non-significant contrast is not an interaction. |
| P05 | Choi tests IL-1 withdrawal and glycolysis; the AHR organoid study measures fibroblast response and AT1 spheroid output. Persistent input and stromal change remain rivals. | An early feature linked to later absolute lineage-supported mature output in the same independent preparations, beyond baseline state and continued exposure. | Conditional predictive extension. Feature, model, interval and functional assay remain unspecified. |
| P06 | Yadav tests myeloid ARG1/ornithine supply, recipient proline/collagen and OAT dependence. Hamanaka provides a distinct human fibroblast arginine context. | A nominated, biologically justified boundary comparison of measured supply and recipient routing under different compartments or media. | Broad supply-versus-use question already directly tested; exact boundary extension remains unspecified. |

No Wg biological effect was computed for this ledger. Prior source outcomes and
the owner's notes were already exposed. The six cards retain their units,
endpoints, alternatives, decisions and stop conditions; none is prioritized.

## Primary-source locators and actual reading depth

**P01 — method specificity.** [Wagner 2021](https://doi.org/10.1016/j.cell.2021.05.045),
Fig. 1–2 and STAR Methods, remains the source. The 2025
[eFPA article](https://doi.org/10.1038/s44320-025-00090-9), published online
17 February, was added in this continuation: Results Fig. 3/5, expanded figures,
“Method benchmarking using SIMMER dataset” and “Analysis of single-cell data
with eFPA” were read in full-text XML. It compares enzyme-only and network
representations, including an in-house Compass implementation; its single-cell
comparison disables sharing and calls that comparator Compass-. These are
different algorithms/settings and data, not validation of this Th17 contrast.
Appendix Text S1 (SIMMER benchmarking) and S4 (single-cell comparison,
pages 22–23) were also inspected after the publisher download failed and Europe
PMC supplied the appendix. S4 changes sharing, penalties and normalization;
a faithful comparator requires those choices, not the Compass name alone. [METAFlux](https://doi.org/10.1038/s41467-023-40457-w)
Results, limitations and supplementary comparison, and
[scFEA](https://doi.org/10.1101/gr.271205.120) matched-metabolomics validation
section, supply additional comparator context. They do not supply missing Th17
biological units or cell-matched measured flux.

**P02 — PGAM.** [Wang et al.](https://doi.org/10.1016/j.celrep.2025.115799),
online 5 June 2025, Cell Reports issue 24 June: Results Fig. 1–4, STAR Methods
processing/signature sections and supplemental PDF S1–S4 legends were read.
S1 reports viability and secreted cytokines; S4 uses donor pseudobulks in human
MS. Results defines pathogenicity as pro-inflammatory minus pro-regulatory;
the signature Methods states the opposite subtraction. No authoritative
resolution was recovered. Do not silently choose a sign. The five deposited workbooks were inspected for sheet identity and endpoints:
S1 lists modules/HVG flags (63 pro-inflammatory and 30 pro-regulatory HVGs);
S3–S6 contain differential expression, signature correlations and program markers.
They do not settle the subtraction sign. A separately named S2 workbook is absent
from the retrieved supplement bundle. Author scoring code and exact numerical
PGAM reproduction remain unresolved. The narrow representation
task can reproduce Wagner's own score table without that signature.

**P03 — lineage versus growth.** [Puleston et al.](https://doi.org/10.1016/j.cell.2021.06.007),
online 2 July 2021, issue 5 August: Results Fig. 2–7, embedded supplemental
figures/legends S1–S7, and relevant STAR Methods on differentiation, flow,
RNA/ATAC and statistics were read from complete XML. S1J–L/S2A explicitly
compare yield, proliferation and division-stratified lineage markers; S4A–B
extends the comparison to Dohh deficiency. Fig. 6–7 and S6 address chromatin
and rescue in the hypusine/acetylation model. These results preclude presenting
“beyond proliferation” or polyamine control of lineage fidelity as an unanswered
general question. Cell-division conditioning still does not identify tracked
conversion or durable suppressive function in Wagner's particular setting.
Supplemental numerical source matrices were not newly reproduced.

**P04 — JMJD3 context.** [Li 2014](https://doi.org/10.1038/ncomms6780),
Fig. 1–6 and differentiation/ChIP Methods, reports context-dependent subset and
plasticity effects. [Liu 2015](https://doi.org/10.1093/jmcb/mjv022), Results and
supplemental figures, reports a role in Th17 differentiation. These are not
exchangeable deletion, polarization or disease settings. Neither substitutes
for Wagner Fig. 6G–H/S6E–F's exact DFMO-by-genotype interaction, and neither
establishes formal mediation of that interaction. Their existence strengthens
the need to keep endpoint, condition, time and baseline genotype effects explicit.

**P05 — lung competence.** [Choi 2020](https://doi.org/10.1016/j.stem.2020.06.020),
Fig. 4/7, S6 and organoid/metabolic Methods, already tests glycolysis and
withdrawal-associated maturation. The 2025
[AHR organoid study](https://doi.org/10.1038/s42003-025-08446-5), published
9 July, adds longitudinal RNA and AT1 spheroid readouts; Results, assay/analysis
Methods and supplemental text were reviewed. Stromal effects are an explicit
alternative to epithelial-intrinsic competence. Spheroid counts, markers and
single-cell snapshots do not establish the proposed same-preparation early
predictor-to-later functional outcome linkage. The existing A1/A14 source holds
remain; another state score does not fill them.

**P06 — ornithine boundaries.** [Yadav 2025](https://doi.org/10.1172/JCI188734),
online 28 August, issue 3 November: Results Fig. 3–6, supplemental Fig. 3C–E,
and coculture, metabolite and human slice Methods were inspected. It directly
tests source ARG1, ornithine, recipient proline/collagen and OAT dependence;
the α-SMA endpoint differs. [Hamanaka 2025](https://doi.org/10.1042/BCJ20253033),
published 17 June, Results Fig. 1–5, media/tracing Methods and S1–S5, finds a
different role for extracellular arginine in cultured human fibroblasts. This
is a context constraint, not a refutation using identical inputs. A useful new
boundary test must specify recipient, supply, medium, time and endpoint before
further data search or computation.

## Version, correction and shared-data audit

The recovered Europe PMC core records were inspected for linked updates,
comments, publication types and dates. Live publisher/DOI pages and targeted
correction searches supplemented them. No linked erratum/retraction was found
in the inspected records; this is a bounded check, not a guarantee. Publisher
redirect/challenge failures are retained as access limitations.

| Evidence lineage | Version or data relationship | Consequence |
|---|---|---|
| Wagner 2021 | Sorted 2015 source cells; GSE75109/GSE75111 are child series. 2021 assays are GSE162300/GSE162382/GSE165088. | Reanalysis of the author example is source reconstruction. |
| PGAM 2025 | Published successor of bioRxiv `10.1101/2024.08.18.607992`; new mouse GSE289733/GSE290297, reused human GSE138266. | Do not label its new mouse data as the same 2015 cells; human reuse remains shared evidence. |
| PGAM/Treg | Preprint `10.1101/2024.06.23.600101` links to [eLife RP104423](https://doi.org/10.7554/eLife.104423), 28 July 2025. Published full-text Methods/data availability read; includes GSE138266. | Preprint and successor are one lineage; its human MS data overlap the PGAM paper. Publication format/review history is retained. |
| Puleston 2021 | GSE157598 parent; RNA GSE157596 and ATAC GSE157597. | Distinct study from Wagner; multiple assays/contrasts are not automatically independent animals. |
| Yadav 2025 | Published successor of bioRxiv `10.1101/2023.09.06.556606`; GSE242510 new coculture and GSE70867 reused BAL; also reuses published lung atlases. | Count source cohorts, not papers. Mapping to existing repository atlas observations must precede a combined analysis. |
| Hamanaka 2025 | Published successor of “Role of Arginine…” preprint `10.1101/2024.11.01.618293`; GSE273882 new HLF RNA and GSE135893 reused atlas. | Use the published article; do not count the preprint or reused atlas as replication. |

Cross-study animal identity was not audited to individual records. Distinct
accessions establish separate deposits, not automatic biological independence.

## Search and citation-tracing record

Date: **4 October 2026, Asia/Seoul**. The earlier scratch cache was recovered
without rerunning its broad searches. New web queries were unrestricted by
author or institution. Recent terms 2024/2025/2026 supplemented foundational
queries; they are not an exhaustive date filter. Actual continuation queries:

1. `Compass metabolic scores benchmarking expression smoothing scFEA METAFlux Th17 2024 2025 2026`
2. `Th17 PGAM pathogenicity pro regulatory glycolysis negative 2025 2026`
3. `polyamine Odc helper T cell division independent lineage fidelity selection`
4. `JMJD3 DFMO Th17 cytokine transcriptome dependence demethylase contradictory`
5. `alveolar transitional state early metabolic prediction mature AT1 output withdrawal glycolysis 2024 2025 2026`
6. `lung fibroblast ornithine supply recipient metabolism arginine independent metabolism Yadav Hamanaka`
7. `"10.1016/j.celrep.2025.115799" correction erratum retraction`
8. `"10.1016/j.cell.2021.06.007" correction erratum retraction`
9. `"Compass" "benchmark" "expression" "2025" metabolic`
10. `"JMJD3" "DFMO" "Th17" "2024" "2025" "2026"`

Backward tracing used the closest papers' reference/data sections to the 2015
Th17 source, JMJD3 studies and lung atlases. Forward tracing reused the saved
Europe PMC citation lists: 449 Wagner and 555 Choi records were retrieved.
This continuation screened titles for method/metabolism/lineage and
transitional/stromal links and examined the close sources above; it did **not**
read all 1,004 citing papers. Citation counts are coverage facts, not support.
Reviews/search snippets were discovery aids, not the basis of the ledger.

## Stop point and explicit remaining work

The branch-level bounded comparison is recorded. Exact novelty for P05/P06
cannot be assessed until their tuples are nominated. P01's external benchmark still needs an implementation specification matching
the now-inspected Appendix. P02 needs source scoring code/authoritative sign
clarification and the missing S2 locator before exact external-score reproduction.
Do not call those narrower audits complete or use them to block unrelated
Wagner source identity work. Recent uninspected leads from the earlier note
remain leads, including the periodontal alveolar-bone study (not lung alveoli).

Full articles and downloads remain ignored local source material under
`raw_data/wagner_literature_20261004/`; source hashes and recovery locations are
recorded in [the continuation handoff](HANDOFF_2026-10-04.md). No copyrighted
article body is added to Git. Reopen this pass when the actual comparison or
new primary evidence changes, rather than repeating the whole search.
