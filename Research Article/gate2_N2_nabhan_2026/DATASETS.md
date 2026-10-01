# Dataset roles and acquisition boundaries

Inventory updated 1 October 2026 for Nb3 execution. The initial
[manifest](config/source_manifest.json) preserves the intake paths and hashes;
the [acquisition record](reports/Nb3_acquisition.json) records the recovered inputs.
Historical run records establish prior use, not that ignored files accompany
a clone. Keep downloaded matrices, source workbooks, images and private note
snapshots out of git.

| Resource | Role and present evidence | Next required check |
|---|---|---|
| [GSE307351](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307351) | Parent of organoid and spatial subseries; 890 listed libraries, not 890 biological replicates | Use subseries-specific readers; do not combine modalities into one sample table |
| [GSE307112](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307112) | 886 bulk libraries, two species, 203 deposited labels = 201 targets plus TIGIT and tdTomato. P1 crosswalk and A10 runs are tracked | Target labels do not imply 201 independently randomized mechanisms |
| `GSE307112_gene_counts.xlsx` | Recovered to ignored `raw_data/GSE307112/`; 303,511,372 bytes and recorded SHA-256 match. 52,636 mouse and 58,302 human gene rows; 886 libraries each. Every library total exactly matches archived A10 totals | Nb3 keeps 850 mouse and 771 human libraries under the declared detected-gene definition; all 771 human-passing libraries also pass mouse QC |
| Plate design and imaging tables | Small files exist in P1 `inputs/`; original hashes match A10's audit record | Reuse one-to-one joins; retain missing day-14 record and missing tdTomato guide rows |
| Xenome statistics | Recovered exact hash; all 886 library/target/plate joins match and every partition sums to input reads | Retain host/graft labels where their species mapping is undocumented; RNA fractions are not cell abundance |
| Supplement archive | Already available locally under `tmp/rq-audit/sources/`; no redownload needed | Extract only required members to ignored storage; preserve archive/member checksums |
| Datasets S1/S2 | S1 is the plate layout; S2 contains four plate sheets with gene identifiers and guide-design columns | Resolve target aliases and reference controls; guide pools are not independent guide experiments |
| Dataset S3 | Two budding comparison sheets: `buddingmorpho_vs_TigitTdTom` and `buddingmorpho_vs_othersWithIm` | Distinguish both reference groups and recover statistical-column semantics |
| Datasets S4/S5 | Mouse/human wide differential-expression summaries, respectively; sheet names indicate adjusted-p-value filtering | These selected summaries cannot replace the full gene universe or raw count workbook for a new DE fit |
| Dataset S6 | Target-by-component CSV with 20 ICA columns; first row labels include Met, Glis3 and Trp53 | Target activities are distinct from gene projections; recover scaling and match components |
| Dataset S7 | Twenty ICA sheets with gene annotation and `gene_zscoreOfProj` | Gene projections are available; this is not simply an enrichment-results workbook. Freeze module extraction/sign rules before scoring |
| [GSE307128](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307128) | Four spatial samples: blocks 8/16 WT, 10/15 NKX2.1 KO; processed ZARR, SpaceRanger and image assets | Establish animal/block identity, treatment, region/bin mapping and RCTD outputs before downloading large objects |

All seven datasets were extracted unchanged from the existing archive into
ignored local storage. [Schema inventory](reports/supplement_schema.json)
records hashes, sheet names and representative headers. S4/S5 contain 5,136/7,195
selected genes and 200/195 target columns. S6 supplies 200 target activities and
S7 supplies 10,589 gene projections for each of 20 components. Their original
component signs and identities are retained in Nb3 source-table reconstruction.

The spatial series bundle is listed at roughly 12.7 GB. Prefer metadata and
selected processed objects after feasibility; no FASTQ rebuilding is needed
for this scaffold. SpaceRanger processing in inspected sample metadata is
3.0.1, whereas the supplement says 3.0. Preserve the version distinction.

## Existing comparators, not newly independent validation

- **Toth 2023**, [DOI](https://doi.org/10.1038/s41467-023-44184-0),
  **GSE215824**: five RNA and three ATAC libraries; RNA includes a day-28
  AAV control/KO pair. The source paper already uses this dataset. It is a source
  reproduction arm, not an untouched independent validation dataset.
- **Strunz/Tsukui reference data:** already used to construct the paper's spatial
  reference. Their use for annotation cannot also count as independent support
  for a state signature learned from that reference.
- **Niethamer GSE262927, Choi GSE145031 and existing A1/A8 packages:** possible
  state/time comparisons. Audit biological units and earlier exposure; do not
  merge all atlases as the default first step.
- **Healthy/ILD AT2 comparison in Fig. S6:** Reyfman 2019, **GSE122960**.
  Eight donors and eight fibrotic explants can be separated from the additional
  cryobiopsy sample. Exact source PCA and author AT2 annotations remain needed.
- **DepMap:** release and assay underlying Fig. 2J remain unresolved. A modern
  release would be a versioned extension, not an exact reproduction.

The [context eligibility audit](reports/CONTEXT_ELIGIBILITY.md) links the retrieved
GEO records and distinguishes confirmed design facts from missing source mappings.

**S5 consistency warning:** the completed source comparison found numeric
logFC/direction-list conflicts. Preserve both fields and their hashes;
[the concordance audit](reports/CONCORDANCE_AUDIT.md) explains why numeric human
DE reproduction remains failed despite directional support for inspected targets.

## Required schemas before numerical work

Organoid joins: `library_id -> GSM -> target_label -> resolved_gene_id -> plate
-> repeat_label -> well_position -> preparation_id (unknown allowed)`; include
separate mouse-isolation and fibroblast donor/lot fields. Imaging has one row
per well/day/segmentation method; RNA has one row per gene/library/species.
Retain raw and normalized values separately. Species-specific QC may produce
different eligible well sets; paired analyses use their declared intersection.

Spatial joins: `GSM -> library -> block -> section -> animal -> genotype ->
treatment -> timing`, then bin coordinates, physical scale, transcript count,
reference labels/weights and region definition. Unknown animal IDs remain
unknown; neither a block name nor a filename is automatically an animal ID.

## External E5 addition, 1 October 2026

[GSE306184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE306184) was
downloaded to ignored `raw_data/GSE306184`: fourteen read-count workbooks and
the complete SOFT metadata. The [manifest and source fields](runs/E5_metadata_v1/sample_manifest.tsv)
and [descriptive pilot](reports/E5_EXTERNAL_FEASIBILITY.md) retain fourteen
libraries in seven groups. This is a separate external epithelial-response
dataset, with protocol conflicts, unknown donor independence, sparse AT2
markers and no uninjured receptor-knockdown group. It is not a replacement for
the original source screen, DepMap cohort or a functional AT2-renewal assay.
The report also specifies GSE97053 expression context and the unexecuted,
release-specific DepMap branch.
