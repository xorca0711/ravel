# Source, design and reading-note audit

29 September 2026. This is the source-grounded intake record; subsequent execution is
reported separately in [RESULTS.md](RESULTS.md). PDF page numbers include the graphical-abstract cover.

## Sources inspected

| ID | Source | Use and scope |
|---|---|---|
| P1 | Owner-supplied annotated PDF of [Nabhan 2023](https://doi.org/10.1016/j.cell.2023.05.022), 34 pages | Results, Discussion, limitations, methods and included Figures S1–S6; figure 4 (PDF p.8), Discussion (p.14) and RNA methods (p.24) visually checked |
| D1 | [GSE208770 public SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE208nnn/GSE208770/soft/GSE208770_family.soft.gz) | Retrieved 18 sample records and six treatment labels; all count files subsequently audited and analyzed in bulk_v1 |
| N1 | [Result-body notes](https://app.notion.com/p/3e9151616b448042b032e6f60e4d6dc4) | Owner's experimental logic and biological emphasis; last edited 2026-09-29T09:33:01.927Z |
| N2 | [Discussion notes](https://app.notion.com/p/3e9151616b4480f3ace6e61b3044e155) | Owner's unresolved questions; last edited 2026-09-29T03:56:03.678Z |
| N3 | [Research-theme candidates, Nabhan branch](https://app.notion.com/p/3e0151616b44807ba675e28eeb4db751) | Seven ordered themes plus the Fzd6-ligand question; also the earlier Axin2/Il1r1 theme; last edited 2026-09-29T07:32:00.198Z |
| R1 | [Main purpose](../../README.md), [structure](../../docs/REPOSITORY_STRUCTURE.md), [architecture](../../docs/RESEARCH_ARCHITECTURE.md) | Paper evidence → biological questions → specified tests → cross-question synthesis |
| R2 | [Nabhan 2018/Nb1](../gate1_03_nabhan_2018/README.md), [Axin2/Il1r1 work](../gate1_02_choi_2020/axin2_il1r1/README.md) | Existing exposure, source candidates and interpretation ceilings; avoid duplicate analyses |

All Notion pages were available as text, marked unverified by Notion, with no
reported truncation. They are the owner's working context, not primary evidence.
Only the scientific synthesis and links are retained here. Private annotations,
personal context and full PDF text are not copied into the package. The PDF hash,
source date and metadata hash are in [source_manifest.json](metadata/source_manifest.json).
The PDF includes supplementary figures, but separate underlying numeric tables,
raw images and source code have not been recovered. The paper reports no original code.

## Assays and units

| Evidence | What the paper measures | Reanalysis ceiling |
|---|---|---|
| Figure 1/S1 | Fzd RNA across compartments, diseases and species; smISH confirmation | Donor/animal summaries for scRNA; cells/puncta cannot replace animal replication |
| Figure 2/S2 | Receptor-family inhibition and individual gene deletion in AT2 cultures; fibroblast response | Organoids nested within independent cultures/animals; no individual-Fzd1 necessity conclusion from a Fzd1/2/7 inhibitor |
| Figure 3/S3 | AT2 growth and reporter responses to agonists, with receptor controls | Reporter activity and growth are distinct endpoints; Fzd6 synthetic sufficiency does not establish endogenous necessity |
| Figure 4 | Bulk AT2-organoid transcription, qPCR and gene-set displays | Figure legend: three biological replicates per condition. Methods define biological replicates as different animals **or** independent cultures. GEO does not identify their preparations or cross-condition pairing |
| Figure 5/S4 | Mixed-culture growth, AT1 markers and in vivo AT2 EdU | Growth, differentiation and proliferation must be analyzed separately |
| Figure 6/S5 | Injury, survival, matrix deposition and histopathology | Preventative and delayed-treatment experiments differ; survivor selection affects injury/physiology comparisons |
| Figure 7/S6 | Airway pSftpC, reverse-lineage organoids, Lysotracker and airway markers | Supports an airway-to-alveolar interpretation; does not uniquely identify the founding airway subtype or demonstrate complete mature function |

## Corrections and unresolved source differences

1. **Bulk versus single-cell.** N1 describes the agonist transcriptomics as scRNA-seq.
   P1 pp.9/24 and D1 instead support bulk RNA-seq. Use single-cell methods only for
   the reused atlas arm. Do not fit cell-state proportions to these 18 libraries.
2. **Timing is not fully reconciled.** Figure 4/methods describe two weeks of
   expansion and 48-hour replacement treatments; D1's series design says 19 days,
   and its common treatment text says 8–12 hours while also listing 24/48-hour
   withdrawals. Preserve all descriptions. Withdrawal labels are usable as labels;
   an exact kinetic or scheduling inference remains unavailable.
3. **DE thresholds differ across descriptions.** Results p.9 says more than
   twofold; methods p.24 states absolute log2 fold-change >2 with FDR <0.05;
   Figure 4C's caption uses p<0.001 for highlighted genes. These may encode different
   reporting/highlighting rules. Reproduce each explicitly; do not tune until the
   published gene totals match. Figure 4D dots represent genes, not independent cultures.
4. **No detected difference is not equivalence.** P1 reports no significant AT2
   transcriptomic difference between Fzd5 and Fzd6 agonists. Precision and a
   biologically useful equivalence margin are needed to support similarity of effects.
5. **Editing versus blockade.** P1 p.6 reports a 65% Fzd5 knockout score, and p.14
   identifies incomplete deletion before proposing compensation. Neither explanation
   has been isolated by the deposited agonist bulk data. The antibody blocks Fzd5/8,
   so target scope also differs from individual Fzd5 deletion.
6. **Hippo terminology.** Cyr61/Ccn1, Ctgf/Ccn2, Amotl2 and Crim2 are the Figure 4D
   response panel. Their RNA is a Hippo/YAP-associated transcriptional readout, not a
   direct assay of Hippo kinase activity or proof of a bipotent cell. The figure's
   gene names need release-aware aliases, and Ki67 maps to mouse Mki67.
7. **Airway lineage sentence.** In P1 p.11, the fast-growing lineage-negative
   organoids initially lack Lysotracker incorporation; the notes' abbreviated
   placement could assign this to lineage-positive cells. Keep the groups distinct.
8. **Therapeutic scope.** P1 p.15 explicitly limits the fibrosis assessment to
   preventative dosing, reports survival bias in physiology/gas exchange, and leaves
   other injury contexts open. Delayed-treatment survival is not delayed-treatment
   antifibrotic efficacy. N2's broad IPF-benefit wording is a proposal, not a clinical result.
9. **Endogenous Fzd6 ligand.** P1 p.7 says an endogenous ligand, **if one exists**,
   remains unidentified in this context. This does not claim that Fzd6 has no
   noncanonical ligand biology, or that an atlas can discover binding specificity.

## Repository state and exposure

Remote `main` was fetched to `17c0859`; planning starts there on
`codex/nabhan-2023-plan` in a managed worktree. The original checkout at `33b27cf`
contains unrelated local audit material and was preserved. The owner has read the
paper and the source results are known: this is a prospective analysis plan on
exposed hypotheses, not a blinded preregistration. Existing Nb1, A4 and other atlas
results remain exposed evidence. No matrix fitting, candidate validation, new
biological finding or claim-register promotion occurred in this intake.
