# Song C2 source provenance

The analysis plan and literature context were transferred privately from source revision
`b8eddf8a569866e1faa45bfb310501c67abf013c`. That commit was unavailable from the
published remote. The branch was created from `0d32085fa0e307f3a26b67592450bb8633e7700a`.
The observed on-disk Git blobs, computed before the run, were
`6bc426e06f0a8719b00e7773973532e62d7580be` (plan) and
`c1ddce2af6516bf488e00fe1960e27cb5c6d74fc` (literature context).
Both matched the supplied hashes. The opening comparison is young WT versus Cd38 KO after cytokines,
using recovered HSC number, BrdU incorporation and 7-AAD staining in Fig. 1a–c.

Inputs were retrieved on 26 November 2026 and saved under ignored `raw_data/song_v1/`.
Each contract records SHA-256 digests. The GEO `geo` and `soft` files are the
[raw archive](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE268nnn/GSE268310/suppl/GSE268310_RAW.tar)
and [family SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE268nnn/GSE268310/soft/GSE268310_family.soft.gz).
Files named `mN.xlsx` are publisher assets `43587_2024_670_MOESMN_ESM.xlsx` for
Supplementary Table 1 (N=2), main Figures 1–4 (N=3–6) and Extended Data Figures 1,
4–7, 9–10 (N=7, 10–13, 15–16). Links are available from the [publisher](https://doi.org/10.1038/s43587-024-00670-8).
The `article` file is the [PMC manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC11565225/?report=xml).
Workbook labels and cell coordinates are panel-local. Blank values stay blank.

The Hallmark adaptation uses the versioned [mouse Hallmark GMT](https://data.broadinstitute.org/gsea-msigdb/msigdb/release/2025.1.Mm/mh.all.v2025.1.Mm.symbols.gmt). Replays used Python with openpyxl 3.1.5 and matplotlib 3.10.8.
