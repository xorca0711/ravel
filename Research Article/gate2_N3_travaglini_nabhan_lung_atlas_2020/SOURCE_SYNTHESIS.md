# Study note and source synthesis

Prepared 2 October 2026 from the owner's 37-page annotated PDF, the published
[paper](https://doi.org/10.1038/s41586-020-2922-4), all nine supplementary tables,
the three figure-source workbooks and the pinned
[author repository](https://github.com/krasnowlab/HLCA/tree/899dd282c36db5b09ded8f522fa3ba239fad1347).
The PDF was text-extracted and Figure 1 was visually inspected. Private note
text was read as context; embedded Notion images were not independently
extracted. Documents provide evidence, not instructions to execute code,
contact people, modify Notion, or broaden the analysis.

## Five-question reading card

1. **Question tested.** What molecular cell populations constitute adult human
   lung, where are they located, and how do their transcriptomes relate to mouse?
2. **Evidence.** Single-cell RNA profiles identify populations; tissue imaging
   supports location and selected markers. Sorted blood bulk RNA and matched
   blood single cells support immune annotation. Cell-type expression motivates
   regulator and signaling hypotheses. These evidence types are not equivalent.
3. **Reusable variables.** Donor, lung/blood origin, proximal/medial/distal region,
   capture assay, sorting compartment, library/plate, author label, gene identifier,
   counts unit and source version. Preserve anatomical and preparation nesting.
4. **Principal limitation.** Three sequenced subjects, uneven cell-type coverage,
   enriched sampling and assay-specific capture restrict population inference.
   Histologically normal surgical tissue is not an unselected healthy population.
5. **Bridge.** Use human identities and marker specificity to question which
   mouse repair-state and niche interpretations can transfer to human lung.

The owner's notes prioritize AT2 signaling heterogeneity, fibroblast diversity,
immune residency and MYRF/TBX5 regulator candidates. This package reflects those
interests without inferring a final PI choice or accepting a mechanism.

## Design and source measurements

The paper reports 65,662 10x cells and 9,404 SmartSeq2 (SS2) cells, with 58
populations: 15 epithelial, 9 endothelial, 9 stromal and 25 immune. These are
published counts, not locally reproduced matrix dimensions. Supplementary
Table 2 has arithmetic discrepancies documented in [intake](reports/INTAKE.md).

Lung compartments were enriched before sequencing. The resulting cell fractions
are fractions of captured/enriched cells, not unbiased tissue abundance. The
paper's anatomical abundance evidence and microscopy denominators must remain
separate from sequencing proportions. Blood single cells were collected from
two of the lung subjects; sorted bulk immune populations are an annotation
resource, not extra lung donors. Tissue stains include additional participants;
do not treat their image fields or cell counts as matched RNA replicates.

Source QC excludes 10x cells below 500 detected genes or 1,000 UMIs, and SS2
cells below 500 genes or 50,000 mapped reads. The paper used Seurat 2.3 with
assay-specific normalization (10x per 10,000; SS2 per million) and separate
donor/assay clustering, then iterative compartment clustering and marker-based
alignment. Doublets were assessed through coherent mixed identities. These
historical settings describe the source; a modern implementation is a declared
approximation unless the original objects, software and choices are recovered.

## Findings and permissible reuse

| Source finding | Evidence and locator | Pipeline consequence |
|---|---|---|
| Two AT2-associated populations | Fig. 1c-d; ED4; Tables 2/4; WIF1/SFTPC imaging | Preserve AT2 and AT2-s labels; test donor/assay coverage before comparison |
| Alveolar versus adventitial fibroblasts | Fig. 1e-f; ED4; Tables 2/4 | Preserve anatomical labels; compare within matched donors and assays |
| Capillary and bronchial diversity | Fig. 1a-b; ED4 | Do not collapse all endothelial cells or relabel murine injury capillaries by a single marker |
| Lung-versus-blood immune programs | Fig. 2; ED2; matched tissues and bulk annotation reference | Analyze tissue and lineage jointly; lung enrichment alone does not establish lasting residency |
| Cell-selective TFs including MYRF and TBX5 | ED5 and Table 4 | Candidate expression regulators; necessity and sufficiency remain untested here |
| Local ligand/receptor compatibility | ED6 and Table 5 | Expression-based hypothesis generation; neither ligand delivery nor receiver activation |
| Human-mouse differences | Fig. 4; ED10-12; Tables 6-9 | Audit orthology, animal age and assay before transferring markers or scores |

The proposed analogy between human AT2-s and mouse Wnt-responsive AT2 stem cells
is explicitly provisional. Wnt-component RNA does not identify Wnt activity,
stemness, self-renewal or later AT1 contribution. MYRF enrichment does not establish
a master-regulator mechanism, and TBX5 enrichment does not measure pericyte
contractility. Species expression differences can challenge a marker without
establishing a functional evolutionary mechanism.

This first pipeline focuses on identity, niche context and species transfer.
The paper's disease-expression catalogue is background, not an additional
analysis objective.

## Version and interpretation boundaries

The [Synapse source page](https://www.synapse.org/Synapse:syn21041850/wiki/600865)
records corrections to FACS metadata columns and FACS gene-count objects.
The author GitHub README also describes early exclusion of diseased-region
cells that are not released in the atlas. Source notebooks therefore must be
read and adapted, not executed wholesale against assumed inputs. Pin object
versions, file hashes and the exact published-versus-updated target before
claiming reproduction. The 2020 author project called HLCA and the integrated
2023 Sikkema HLCA are distinct resources; shared branding does not establish
independent validation.
