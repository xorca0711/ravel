# Data sources and qualification requirements

**Newly qualified source:** the [completion audit](EXTENSION_COMPLETION.md)
adds the official S3 brain object and full/raw atlas metadata. Its count-valued
brain layer differs from the earlier normalized Figshare objects described below.

**Current execution:** see [results and amendments](RESULTS.md), [figures](FIGURES.md)
and [execution ledger](EXECUTION_VALIDATION.md). The planning text below records
pre-execution choices and is retained; it does not override current evidence.

Checked 3 October 2026. These are source-directory observations for planning,
not a qualified biological metadata analysis. No expression matrices were
downloaded and no sample counts or independent-animal counts were calculated.

## Verified source pointers

| Source | Confirmed identity and intended role |
|---|---|
| [Figshare release 8273102 version 2](https://figshare.com/articles/dataset/Processed_files_to_use_with_scanpy_/8273102/2) | Paper-cited processed release, DOI 10.6084/m9.figshare.8273102.v2. Its API lists tissue-specific H5AD files; internal count layers and annotation version remain unverified. |
| [GSE132042](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE132042) | Current SuperSeries includes GSE132040, GSE109774, GSE149590 and GSE193093. Do not treat it as one homogeneous ageing cohort. |
| [GSE149590](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE149590) | Titled Tabula Muris Senis; its summary says 18 tissues and points to public raw data. Reconcile that scope with the paper and Figshare rather than silently replacing the paper's tissue count. |
| [GSE132040](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE132040) | Bulk sequencing of 17 organs, with a separate metadata file. Optional tissue-level context; pairing and overlap with single-cell animals are unverified. |
| [Author code](https://github.com/czbiohub-sf/tabula-muris-senis) | Ingest, atlas and ageing-signature code is listed. Pin a commit and identify the panel-specific implementation before reuse. |

The original Tabula Muris contribution is documented in the source manuscript
linked from [the note reconciliation](NOTE_RECONCILIATION.md). Audit reused
animals and cells before using that resource as a validation dataset.

## Bounded matrix acquisition candidates

Observed through the [versioned Figshare API](https://api.figshare.com/v2/articles/8273102/versions/2).
Sizes are server metadata, not completed downloads. No matrix SHA-256 is known.

| File | File ID | Bytes | Candidate use |
|---|---|---:|---|
| `Lung_facs.h5ad` | 15467765 | 134756411 | Within-lung assay sensitivity |
| `Lung_droplet.h5ad` | 15467792 | 608112140 | Lung coverage and count eligibility |
| `Brain_Myeloid_facs.h5ad` | 15468251 | 273601725 | Owner's microglial candidate |
| `Kidney_droplet.h5ad` | 15467990 | 728334161 | Optional source immune-state comparator |
| `Bladder_droplet.h5ad` | 15468203 | 430253430 | Optional composition reproduction anchor |

Start with source tables and metadata. Download only files required by the
chosen stage; a whole-atlas or FASTQ download is not needed for planning.
Processed objects must not be assumed to contain raw counts merely because
they have an `.h5ad` extension. A normalized-only release permits a documented
source-scale description, not an invented count-based model.

## Required metadata evidence

Before numerical use, record the source location and join cardinality for
each field: stable cell ID, original mouse ID, tissue/region, age, sex, assay,
library/plate/run, processing batch, source release, annotation and count
layer. Retain original labels alongside any harmonized fields.

Produce an animal-by-tissue-by-assay-by-age coverage table with unique animals
separate from cells and libraries. Check cross-assay and cross-tissue mouse
reuse, original Tabula Muris overlap, duplicate barcodes, pooling and missing
IDs. Never replace a missing mouse ID with a plate or sample name without
source evidence. A tissue missing from a mouse is missing, not zero abundance.

Age, sex and batch overlap and model rank must be examined before selecting
comparisons. The source age schedule does not guarantee lung or microglial
replication. The oldest group may carry survivor/cohort selection; the youngest
group should not be silently combined with adult baseline when asking an adult
ageing question. Exact unit counts, QC thresholds, usable genes, gene-set
versions and precision remain unknown until qualification.

## Source record preservation

Small public API/text responses were cached locally during reading. Their
scientific role is limited to the deposit descriptions above. Before the first
metadata run, acquire immutable source copies under ignored
`raw_data/tabula_muris_senis_2020/`, hash their exact bytes, and bind them to the
metadata contract. Do not use private Notion exports as public raw data.
