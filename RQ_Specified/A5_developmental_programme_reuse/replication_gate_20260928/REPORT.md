# A5 external replication recovery, 28 September 2026

**GSE303646 advanced from a title-level lead to an identified author-state and
library resource, but cannot yet support the unchanged A5 test. No expression
matrix, programme coverage, paired-arm eligibility count or score was produced.**
The recovery rules and original input hashes were committed before this extraction
at `f3950253ae229f062dbae94551b04a908a8e5ade`.

## What was recovered

| Evidence | Confirmed result | Remaining limitation |
|---|---|---|
| Author QC notebook output | 56 unique identifiers, all matched to GEO; age, day and treatment agree | Library identifiers do not establish individual mice |
| Author epithelial labels | `Krt8-ADI`, `AT2_activated`, and `AT2` are explicitly named in author code | No barcode-to-label map recovered |
| Fixed-window library inventory | 24 libraries: four per young/old x day 3/10/20 cell | These are libraries, not 24 verified eligible mice |
| One deposited DGE summary, GSM9131916 / muc26501 | Molecular-barcode output, `OUTPUT_READS_INSTEAD=false`; per-barcode transcript summaries | Full-cohort raw integer matrices and barcode alignment remain untested |

The [author QC table](GSE303646_author_qc_metadata.tsv) preserves the visible
sample fields from notebook cell 8, including its reported QC summaries. Its
retained-cell totals sum to 160,477. This extraction does not recompute counts.
The notebook display omits the epithelial count columns, so they cannot be used
to infer arm sizes. Author `n_counts` is not substituted for raw UMI depth.
[Library crosswalk](GSE303646_library_crosswalk.tsv) deliberately marks mouse
identity and the state map unresolved.

The [primary paper](https://www.biorxiv.org/content/10.1101/2025.07.24.666371v1)
describes 55 mice, canonical-marker annotation and preprocessing that includes
ambient correction and normalization. That 55-mouse statement needs reconciliation
with the 56 library identifiers; neither pooling nor a technical split is assumed.
The paper points to the public browser and author code. Its distinct study and
2021 processing evidence support, but do not prove, independence from the earlier
Strunz cohort. Existing A5 results and this study's published observations have
already been seen; any future test should not be described as blind validation.

## Exact enabling input

The pinned [author repository](https://github.com/schillerlab/2025_Aging_Bleo/tree/e52bede4d8a0f9a8a07cb88ceb557fe01455d0c0)
references **`230111_Bleo_Ageing_annotated_final.h5ad`**. Its code uses `identifier`
for sample grouping, `name` as a donor field, and `cell_type` / `meta_label` for
annotation. The necessary author export is its per-cell metadata, retaining raw
barcode, library identifier, biological mouse identity, treatment/day, and the
original state label. It also needs the author annotation method/version, pooling
or split reconciliation, and a match to deposited uncorrected raw UMI counts.
A full h5ad download is unnecessary if those fields can be exported separately.

The author state vocabulary makes the intended crosswalk plausible:
`Krt8-ADI` to the transitional arm and `AT2_activated` to the activated reference.
It is **not an executable state map**. Author assignment dependencies cannot yet
be audited, and no new classification using the Guo genes was performed.

## Sources checked and bounded stop

[Source ledger](source_ledger.json) records exact URLs, retrieval outcomes, bytes,
and SHA-256 hashes. Saved evidence includes the primary JATS article, GEO
filelist, one DGE summary, the complete non-truncated 2025 author repository tree,
its README / metadata-QC / NicheNet / scITD code, the same-cohort 2024 repository
tree, and the public browser entry page after cold start. These did not expose the
required annotated object or per-barcode export. The browser entry page offers
plots and communication views; this is not proof that no export exists elsewhere.
The attempted supplementary-material endpoint returned the article page without
a recovered supplementary metadata link. No authors were contacted.

GSE202325 is **not assessed under the frozen non-pathogen scope**, rather than
called biologically ineligible. Its prior broad-AT2 annotation limitation is
carried forward without new infection-data analysis. One source-led alternative,
[Hippo_LOX / Zenodo 14229565](https://zenodo.org/records/14229565), was stopped after
the [primary paper](https://www.nature.com/articles/s41467-025-61795-x) established
that the deposited single-nucleus data are human PCLS from two donor lungs. The
paper's separate mouse experiments do not convert those data into a mouse cohort.
No further candidate or matrix search was undertaken.

## Gate outcome and reproducibility

[Per-candidate verdicts](candidate_verdicts.json) distinguish confirmed fields,
access/identity blockers, failed scope, and unassessed measurement gates.
GSE303646 remains the actionable candidate, with precise missing metadata rather
than evidence that the desired cell states are absent.

Run `audit_recovery.py` with Python 3 from any directory to reproduce extraction,
source-hash checks and verdicts. [Verification](verification.json) passed: original
A5 files match the frozen hashes, modules remain 99/57/53, downloaded hashes match,
and all 56 author/GEO library identifiers and checked characteristics agree.
The original day 2-21, 500-UMI, 30-cells-per-arm, three-mouse and 70%-coverage gates
are unchanged. A candidate-specific committed contract is still required before
any future expression scoring; this report does not authorize scoring.
