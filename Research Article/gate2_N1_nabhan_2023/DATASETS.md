# Dataset roles and feasibility

This inventory distinguishes the source deposit from the atlases reanalyzed by
the paper, and those from repository extensions. A reused atlas is not independent
confirmation of its own Figure 1/S1 result. Verify donor/study overlap before
calling any HLCA transfer independent.

## Source treatment experiment: GSE208770

Public [GEO metadata](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208770)
and [the recovered sample manifest](metadata/samples.tsv) contain:

| Condition, as deposited | GSM range | Libraries | Intended use |
|---|---|---|---|
| LGK974_WNT | GSM6369132–GSM6369134 | 3 | Recombinant Wnt comparator |
| 48hourwithdrawal | GSM6369135–GSM6369137 | 3 | Primary withdrawal reference |
| 24hourwithdrawal | GSM6369138–GSM6369140 | 3 | Withdrawal-stage description |
| LGK_CHIR99201 | GSM6369141–GSM6369143 | 3 | Downstream pathway activation reference |
| LGK974_FZD6_Agonist | GSM6369144–GSM6369146 | 3 | Fzd6 response |
| LGK974_FZD5_Agonist | GSM6369147–GSM6369149 | 3 | Fzd5 response |

Mouse AT2-organoid **bulk** RNA-seq, GRCm38. GEO advertises per-sample exonic
count/RPKM text files, not barcode matrices. The study reports three biological
replicates, but exact animals, independent preparations, shared culture blocks and
pairing remain unresolved. Never pair conditions because each has a `rep1` label.
Keep CHIR99201 as the source spelling; do not silently substitute a reagent identity.
Read the [timing/threshold discrepancies](SOURCE_AUDIT.md#corrections-and-unresolved-source-differences)
before analysis. Neither receptor knockout/blockade RNA, airway-response RNA,
stromal-response RNA nor in vivo treated single-cell RNA is represented by these
18 sample titles. Published functional panels are a separate source-data recovery task.

## Atlas and complementary routes

| Role | Source/resource | Paper link and repo use | Admission gate |
|---|---|---|---|
| Exact receptor-map reconstruction | Travaglini/Nabhan 2020 human/mouse lung atlas | P1 reference 36, Figure 1; [publication](https://doi.org/10.1038/s41586-020-2922-4) | Recover original matrices, annotations and donor units; not yet downloaded for this package |
| Exact integrated map | HLCA release cited as the 2022 preprint | P1 ref.37; existing [Sikkema branch](../gate1_04_sikkema_2023_hlca/README.md) | Pin the source release. A newer reference atlas is an adaptation; check reused donors/studies |
| Fibrotic epithelial/stromal context | Habermann 2020, GSE135893 | P1 ref.41/Figure S1E; existing Cardoso E3 | Recover diagnosis and donor/state crosswalk, including rare basaloid cells; no universal cell floor borrowed from another question |
| Fibrotic stromal context | Tsukui 2020, GSE132771 | P1 ref.45/Figure S1F; existing Cardoso E4 | Verified animal IDs and fibroblast subtypes; collagen enrichment changes the sampled population |
| Cross-tissue stromal selectivity | Buechler 2021 fibroblast atlas | P1 ref.44/Figure S1G; [publication](https://doi.org/10.1038/s41586-021-03549-5) | Dataset/version/accession recovery pending; optional after lung analysis |
| Other original single-cell inputs | Riemondy 2019, DePianto 2021, Reyfman 2019 | P1 refs.81/109/110; methods p.24 | Recover exact figure-to-study map first; do not silently substitute a familiar lung atlas |
| Repository injury extension | GSE262927, Niethamer; GSE141259, Strunz | Existing [Nb1](../gate1_03_nabhan_2018/nb1/README.md), A4/A5 context | Reuse audited per-animal artifacts; receptor/state screens only, no claim that untreated viral/bleomycin time courses measure agonist efficacy |
| Additional human context | GSE136831, Adams; GSE178360, Murthy | Existing Cardoso/HLCA branches | Both are already exposed in the repo; define new contrasts and disease/state eligibility before use |
| Vascular extension | Gillich 2020 capillary specialization | P1 ref.97; [publication](https://doi.org/10.1038/s41586-020-2822-7) | Recover relevant endothelial states and outcomes; bulk AT2 data cannot answer Fzd4 function |
| Regulatory extension | A1-accessible RNA/ATAC/histone datasets | Existing [A1 workspace](../../RQ_Specified/A1_transitional_epithelial_state_distinction/README.md) | Compatible state, unit and measured regulatory layer; motif enrichment is not TF binding or linked future fate |

## Initial intake requirements and execution update

1. Inspect all 18 advertised processed-file headers, gene identifiers, integer
   count columns and consistent gene universes; hash files and separate counts/RPKM.
2. Resolve independence, animal/preparation identity and any valid blocks; log
   unresolved fields rather than inferring sample identities from replicate suffixes.
3. Recover normalization and figure-specific gene/statistic definitions; preserve
   source discrepancies as alternative reproduction settings.
4. Recover the original atlas versions and functional source tables. Missing
   endpoints limit a reproduction, not the owner's eligibility to ask the question.

No multi-GB FASTQ download or full-atlas integration is needed for this planning
step. Reuse counts and audited existing artifacts first. Generated RNA results will
go to versioned trials; large inputs and processed objects remain ignored.


The [bulk run](trials/bulk_v1/REPORT.md) now includes all 18 processed-count files
and a pinned GRCm38.102 annotation, with source hashes. All18 BioSample records
were checked; independent preparation/animal identity and pairing remain unresolved.
The [atlas run](trials/atlas_v1/REPORT.md) uses Habermann author-labeled cells
and the existing Niethamer author-annotated counts layer. Its contracts pin
original inputs and distinguish source reuse from the exposed mouse extension.
Travaglini processed data were located as Synapse syn21560510 v1; metadata
syn21560409 downloads returned403. Functional numeric/image tables were not
recovered; see [the recovery audit](FUNCTIONAL_SOURCE_AUDIT.md).
