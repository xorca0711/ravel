# Checkpoint B: source metadata and remaining holds

31 October 2026, Asia/Seoul. Owner **Yd1-P01**. This return implements the
[reviewed B authorization](REVIEW_A.md) on integration
`dc908350a73a28714ec1df6456fafaf661db76b3`. Metadata execution is complete;
actual X3 state/retention recovery and X3/X5 expression remain held.
[Provisional X6 matrix](PROVISIONAL_X6_MATRIX.md) is a separate synthesis, not
scientific acceptance, a bench-ready package or final extension closeout.

## B1 / X3: author labels located; retained-cell metadata unresolved

Question: can the actual retained author states be joined to the twelve reported
mouse samples before any state/time expression comparison? The endpoint here is
source identity and metadata support, not RNA. Mistaking a code annotation vector
for the deposited object's cell identities is the principal validity threat.

The [publisher record](https://doi.org/10.1038/s41586-024-07660-1) links
[TatsuyaTsukui/AlveolarLineage](https://github.com/TatsuyaTsukui/AlveolarLineage/tree/0001f0329d5abdcd61635d17cf60e0cb5ba48586).
The complete, nontruncated tree at that revision contains a README and five R
scripts, with no retained-cell/state export. In
[2_integrate_by_MNN.R](https://github.com/TatsuyaTsukui/AlveolarLineage/blob/0001f0329d5abdcd61635d17cf60e0cb5ba48586/Rcodes/2_integrate_by_MNN.R):

| Exact source locator | Recovered meaning | Limit |
| --- | --- | --- |
| Lines 7–46 | Twelve objects receive sample, day and treatment metadata | Does not recover the deposited retained barcode list or donor identities |
| Line 60; lines 75–87 | An earlier `MG.rds` save precedes exclusions of clusters 17/18 and reclustering | Numeric cluster IDs do not supply names; these operations were not rerun |
| Lines 91–94 | Eleven annotation positions, ten unique names; labels are bound to `levels(MG)` before `RenameIdents` | The vector is author intent, not verified saved-object identity |
| Lines 95–106 | `MGcleaned.rds` saves and a `meta.txt` export of identities, sample and lineage | `meta.txt` is absent from this tree and the inspected GEO listings |

The code names are **Alveolar, Fibrotic, Inflammatory, Adventitial, Smooth muscle,
Peribronchial, Stress-activated, Proliferating, Mesothelial and Pericyte**;
Alveolar occurs twice in the vector. Proposed exact labels remain **Alveolar,
Inflammatory and Fibrotic**. Their actual object field and barcode assignments
are **unknown**; no guessed cluster-number mapping was made.

[Annotation vector](../../../analysis/research/runs/Yd1_extension_b1_v1/author_code_annotation_vector.csv)
and [code locators](../../../analysis/research/runs/Yd1_extension_b1_v1/author_code_locators.csv)
preserve the provenance.
The [36-row support request grid](../../../analysis/research/runs/Yd1_extension_b1_v1/requested_state_support_grid.csv)
reuses X0's 50,785 pre-filter barcodes across twelve sample/day labels and leaves
retained cells, state counts and demultiplex ambiguity **blank**. These blanks
mean unavailable, not zero. Actual occupancy for all author states, retained and
dropped barcode joins, and ambiguity fields remain unmeasured.

The authorized fallback is specifically
`GSM6428697_seurat_v4_obj.rds.gz`, listed at **1,553,376,346 compressed bytes**.
The resource check found C free space 3,508,690,944 bytes, X free space
138,724,839,424 bytes, and available RAM 1,858,854,912 bytes. No Rscript was found
on PATH or in the inspected standard R locations; the default Python lacks
rdata/pyreadr. The object's memory peak and a validated metadata-only reader are
unknown. X has storage, but that alone does not qualify deserialization. The
resource decision is precautionary qualification, not proof the object cannot
be processed on this machine.

**No RDS was downloaded or deserialized**, and no separate matrix/RAW archive or
expression values were accessed. The [metadata hold](../../../analysis/research/runs/Yd1_extension_b1_v1/metadata_hold.json)
contains exact resource observations. Reopen with the small author export or a
qualified reader/memory route for the authorized RDS. Then recover actual
retained/dropped barcodes, all sample/state occupancy, joins and ambiguity before
requesting expression review.

The [conditional X3 design](EXTERNAL_FEASIBILITY.md#one-bounded-conditional-design-for-review-not-execution)
remains unchanged: Il6 primary; P2rx4, Col1a1 and Acta2 companions; Day7−Day0
primary, Day14−Day0 and Day21−Day0 companions; equal reported-sample weighting,
no suffix pairing or population tests. Each compared day must retain all three
reported samples with nonempty nominated state. Verified absence means zero
composition and undefined expression; missing annotation means unknown.
No relabeling, reclustering or weakened support rule is permitted to repair a
missing baseline state.

## B2 / X5: source table recovered; expression prerequisites remain held

Question: which exact public studies and capture/overlap limits qualify a bounded
human comparison? The biological units would be independent donors, with samples
and cells nested; this pass recovers study metadata only. Source labels and
marginal tissue/condition counts cannot substitute for donor joins.

The [public FAQ](https://scahn.khatrilab.org/FAQ) opened through the normal browser
after automatic loading. The inspected Home/FAQ showed figure downloads but no
raw metadata download link. No expression page was opened, no target gene was
queried, and no atlas was downloaded. Direct HTTP 403 and failed web routes remain
recorded alongside the successful browser access.

The [primary article](https://doi.org/10.1038/s41590-026-02671-8) and its directly
linked [supplementary workbook](https://static-content.springer.com/esm/art%3A10.1038%2Fs41590-026-02671-8/MediaObjects/41590_2026_2671_MOESM3_ESM.xlsx)
were recovered. Only **Table S1** was extracted; other sheet values were not
extracted. The workbook is 196,987 bytes, SHA-256
`3eadd6386874f3464cec0eaabaf5d1349566add4a04c51ee1552493c3441af1a`,
retrieved 2026-10-31 01:26:25 UTC.

[All 40 source rows](../../../analysis/research/runs/Yd1_extension_b2_v1/scahn_source_table.csv)
sum to **1,053,128 cells and 781 reported samples**, matching the Home totals.
These are published metadata counts, not independent donors or new expression
summaries. Table S1 has study IDs, technology, DOI and tissue/group marginal
counts, but no accession, individual sample, donor or cell crosswalk.
[Thirty lung/blood source leads](../../../analysis/research/runs/Yd1_extension_b2_v1/lung_blood_source_screen.csv)
retain those limits. No new cohort was selected from them.

| Table S1 source row | Exact study lead | Source-reported context | Decision relevance |
| --- | --- | --- | --- |
| 8 | Gupta2020; DOI 10.1073/pnas.2003603117 | Seven peripheral-blood samples, all labeled healthy; 10x Chromium | Healthy blood lead; fresh whole-blood versus PBMC/preparation, donor IDs and gene measurement still unqualified |
| 33 | Wigerblad2022; DOI 10.4049/jimmunol.2200154 | Eighteen peripheral-blood samples, all labeled healthy; 10x Chromium 3′ | Same qualification need; not an independently qualified comparison cohort |
| 9 | Habermann2020; DOI 10.1126/sciadv.aba1972 | Nineteen lung samples: five healthy, thirteen other lung disease, one other disease | Direct overlap of study provenance with Ravel; broad disease labels do not identify exact IPF donors |
| 24 | Reyfman2019; DOI 10.1164/rccm.201712-2410OC | Six lung samples: five healthy and one other lung disease | Tissue lead; source/donor disease joins still absent |
| 25 | Salcher2022; DOI 10.1016/j.ccell.2022.10.008 | Twenty-nine lung-cancer samples, BD Rhapsody | Same publication lineage used in Yadav; actual selected donors/cells require a crosswalk |

The [overlap map](../../../analysis/research/runs/Yd1_extension_b2_v1/parent_overlap_map.csv)
confirms standalone Salcher and Habermann rows; no standalone Adams row appears.
Adams' possible indirect reuse through a parent atlas is unresolved, not excluded.
Salcher's row is specifically the reported BD Rhapsody lung-cancer subset: its
presence does not prove SCAHN contains every Salcher parent dataset or the same
cells selected by Yadav. Exact physical/donor overlap remains unknown. Tissue and
group fields are marginals; single-tissue rows constrain their group counts, but
individual sample/condition joins are still absent. The generic screen's
“joint unknown” field records this missing explicit crosswalk.

FAQ locators **gene availability/normalization, multiple datasets and low depth**
add three constraints:

- A gene unmeasured in a source dataset is encoded as zero in every source cell.
  Of 16,711 atlas genes, 11,490 are measured in all sources; 5,221 are absent from
  at least some. A source-by-gene measurement mask is needed before interpreting
  zeros or detection. These figures describe the app, not a target-gene query.
- App normalization uses log1p counts per 10,000 over the atlas gene set; means
  include nonexpressing cells. Such means cannot replace qualified raw donor/cell
  inputs or distinguish structural missingness from biological absence.
- Jardine2021, Salcher2022 and Schrepping2020 each split into a/b datasets:
  43 datasets are not 43 independent studies. The low-depth category is technical,
  not a biological neutrophil state.

The article Methods, **“Dataset collection, curation and integration”** (XML Sec11),
also selects samples with at least thirty retained neutrophils and applies
cell/capture filtering. This selection can affect source support and composition.
The [qualification record](../../../analysis/research/runs/Yd1_extension_b2_v1/source_qualification.json)
therefore holds X5 until exact source accession/version, sample-to-donor and
preparation joins, measurement masks, retained-cell denominators and suitable raw
counts qualify one reviewed comparison. The recovered source table supersedes
only the previous source-table access failure. It does not reopen expression.

## Verification, source access and remaining work

Both [B1](config/b1_contract_v1.json) and [B2](config/b2_contract_v1.json)
metadata contracts froze with code and specification at
`e7498beb8058f9fef5bc1e6cbe437f0a9104f07d`.
Their receipts are [B1](../../../analysis/research/runs/Yd1_extension_b1_v1/receipt.json)
and [B2](../../../analysis/research/runs/Yd1_extension_b2_v1/receipt.json).

An independent openpyxl read matched all **400 source fields across 40 Table S1
rows**, row locators and reported totals against the OOXML extraction. Explicit
source-code checks verified eleven annotation positions, exact code locators and
all 36 blank-support rows against X0. This is technical verification of reused
sources, not biological replication. Both metadata scripts completed without a
run failure; scientific acceptance remains unassessed.

The ignored `raw_data/Yd1_checkpoint_b_20261031/` cache is preserved. Contract
inputs bind source/export hashes, resource checks, FAQ transcription, GitHub
revision and retrieval receipts. Tsukui Europe PMC XML failed with HTTP 500;
PMC HTML routes returned challenge pages, not article text. SCAHN Europe PMC XML
succeeded, followed by publisher supplement discovery and direct XLSX retrieval.
No failed route is represented as successful reading.

X4 retains [its reviewed culture/native and early-stage source/design holds](REVIEW_A.md).
Both relevant assays are described as fixed-RNA, but exact donor, culture-file,
FFPE versus fixed-cell protocol/probe/normalization joins and early-IPF specimen
identity remain unqualified. No native-only substitute comparison was performed.
X6 is now the [provisional matrix](PROVISIONAL_X6_MATRIX.md); X3/X5 remain pending
where actual state support or expression would be needed. The
[ledger](EXECUTION_LEDGER.md) records final base, preservation and validation.
