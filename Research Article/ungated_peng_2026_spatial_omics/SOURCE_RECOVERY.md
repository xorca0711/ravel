# Source and annotation recovery — 8 November 2026

This is the retained planning-stage source-reading/access record. The subsequent
[completed metadata qualification](RESULTS.md) provides the frozen crosswalk,
source ledger, filename conflicts and exact remaining holds through the
[research contract and runner](../../docs/RESEARCH_GOVERNANCE.md). All source
outcomes already inspected, including earlier C3 results, are outcome-exposed.
The later Figure 5 code retrieval and publisher HTTP 403 route are recorded in
its source manifest; Tables S1–S4 and annotation exports remain unrecovered.

## Recovered sources and remaining access limits

| Source | Observed availability | Permitted use |
|---|---|---|
| [GSE307534](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307534) | Family SOFT recovered; human Visium. Existing C3 report inventories 56 sections / 25 patient labels. Series supplementary directory lists a 9.4 GB archive and file list. | Accession/library identities and existing archive inventory; no new whole-archive download needed. |
| [GSE308103](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308103) | Family SOFT recovered; human snRNA-seq. Existing C3 report documents 75 libraries / 23 patient labels. | RNA library/demographic cross-check and existing local count cache. |
| [GSE307529](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307529) | Family SOFT recovered. This is **human WES, not Xenium**; sample supplementary links name VCF files. | Genomic sample metadata; not a source of Xenium cell coordinates. Reconcile deposit coverage with the paper's reported WES sample count before using it. |
| [Human-data concept 15670280](https://zenodo.org/records/15670280) | Public API resolves to version [18851077](https://zenodo.org/records/18851077), title matches the paper; `access_right=restricted`, public `files=[]`. | Record/version identity. An empty public list does not establish that the authors have no data. |
| [Code record 17172149](https://zenodo.org/records/17172149) | Public metadata recovered; restricted files. | Source identity only. |
| [Author GitHub](https://github.com/FuduanPeng/LungPCA_Code) | Public tree contains figure scripts and README, no Data directory or annotation files. Figure 1 loads processed RDA/RDS objects; Figure 5 also depends on processed objects and Xenium Explorer panels. | Figure provenance and expected object names, not an executable annotation pipeline. |
| README DOI 17148540 | Zenodo API returned 404 in the recorded attempt. | Unresolved identifier; do not alias silently to either published DOI. |
| [PMC supplementary material](https://pmc.ncbi.nlm.nih.gov/articles/PMC12980502/#supplementary-material1) | Table S1 = supplement-2.xlsx, S2 = -3.xlsx, S3 = -4.xlsx, S4 = -5.xlsx. PMC returned HTML, Europe PMC routes returned non-ZIP/403, and browser download timed out. | Table titles/locators only; spreadsheet contents are **not read or recovered**. |

Local public-source snapshots and per-request UTC timestamps, URLs, hashes and
failures are in ignored `raw_data/peng_spatial_20261108/` in this worktree.
`acquisition_v1.json` through `acquisition_v4.json` preserve the attempted routes.
The tree snapshot is `author_repository_tree.json`, tree SHA
`fba87dbee8dbae497b15b81a4b0fa79edccd17b2` (a tree identity, not a commit).
`author_Figure_1.R` corresponds to Git blob
`e0a22a0b123d3ce0c6282dd066b15d8fd7dc0ef6`; it was read, not executed.
It names `Data/Figure 1B.rda` and `Data/Figure 1C.downsample_25_percent.rds`,
with a `Pathology` plotting field. These identify requested processed products;
they do not establish that a full barcode-level annotation table is available.
Do not bypass restricted Zenodo access or infer file access from its thumbnails.

## Author pathology and ROI definitions recovered from methods

Source locators: STAR Methods, **Histopathological processing of tissues**,
**Visium CytAssist ST profiling/data analysis**, **Xenium data generation/data
analysis**; main Figs. 1B, 2C, 5F–L and S3. These are operational definitions;
the corresponding row-level annotation exports remain missing.

| Layer | Author procedure | Consequence for reuse |
|---|---|---|
| Case/ROI selection | Three pathologists assessed archived H&E. HALO supported pathology annotation; 11 × 11 mm ROIs were marked on whole-slide SVS images using the Aperio square tool. | Recover slide identity, ROI square, coordinate units and image version. A cropped tissue image is not the original ROI export. |
| Lesion selection | LUAD required at least 50% invasive adenocarcinoma in the ST ROI and an adjacent-normal interface. AAH/AIS required a complete precursor lesion and an adjacent-normal interface. Extensive necrosis and selected normal-tissue inflammatory/fibrotic changes were exclusions. | Selected resection ROIs are not an unbiased sample of all early lesions or at-risk lungs. Do not generalize prevalence directly. |
| Histology | The methods distinguish small atypical AAH, non-invasive lepidic AIS and MIA with a limited invasive component; RPII denotes reactive/hyperplastic non-neoplastic pneumocyte morphology. | Retain exact author category and review version. RPII is not a molecular KAC label or proof of future malignancy. |
| Visium spot pathology | Loupe 7.1 annotation of Space Ranger cloupe files against same-section H&E. A spot with at least one tumor cell could be called tumor; normal-epithelial spots should contain none. Non-epithelial structural categories exclude epithelium. | Tumor-labelled spots can be mixed. An annotation is not a purified cell state. Keep pathological annotation distinct from transferred RNA annotation. |
| Visium exclusions/support | Space, foreign-body and artifact categories excluded. snRNA epithelial annotations were transferred; iStar expression alignment corroborated annotations. | Morphology and molecular support are not wholly independent labels. Audit which genes informed labels before using the same genes as an endpoint. |
| Whole-tissue Xenium ROI | The same selected 11 × 11 mm tissue region was used on an additional section. Post-Xenium H&E was converted to OME.TIFF and aligned in Xenium Explorer with at least 30 manually placed landmarks. | Same selected ROI does not mean identical cells across serial sections. Recover transform and section identities, not just patient names. |
| Xenium lesion/RPII regions | Freehand polygons were drawn around lesions and RPII groups; cell barcodes inside them were exported. | Need polygons, coordinate frame, and the cell-ID export. Representative figure images cannot reconstruct all assignments. |
| Neighborhood | Surrounding cell centroids within 80 micrometers of the center define its neighborhood; cell-state counts form the composition matrix. | Recover handling of the center itself, tissue edges and segmentation/QC. Counts depend on density; overlapping neighborhoods are not independent observations. |
| TMA | A separately described cohort of 36 lesions / 19 patients yielded 188 retained cores across eight TMAs; a smaller gene panel was used. | Require core→lesion→patient and cohort identifiers plus the exact panel. Do not join similarly numbered patients to the discovery cohort. |

The sampling sequence was DNA scrolls → 5-micrometer Visium section → two
25-micrometer snRNA scrolls → an additional 5-micrometer Xenium section for selected
samples. If no separate normal block existed, adjacent normal could substitute.
This supports matched regional provenance, not co-measurement of the same cells.
Paper Results also revise one putative precursor in P7 to a second LUAD; preserve
original GEO labels and record the revised interpretation with its source.

## Existing join evidence to reuse

The [C3 spatial report](../gate2_C3_yu_lee_choi_min_2026/trials/u5_spatial_context/REPORT.md)
already documents demographic consistency for all 23 RNA patient labels in the
25-patient spatial cohort. Its `RNA_spatial_demographic_crosswalk.csv` and
`RNA_spatial_crosswalk_validation.json` are existing evidence, not a new result.
Its `deposited_member_inventory.csv` lists the inspected spatial archive members;
`possible_pathology_annotation_members.csv` contains no candidate rows. That
bounded archive inspection did not recover independent spot-level pathology.

The next crosswalk must distinguish **patient match**, **author library alias**,
**lesion match**, **serial-section relationship**, and **same-section barcode
match**. Preserve suffixes such as `-1`; never collapse separate lesions by
patient plus histology. Match fields from explicit metadata first and label
filename-derived fields as parsed, with unresolved conflicts retained.

## Missing-data request specification — draft, not sent

1. Table S1 and a discovery sample manifest: cohort, patient, tissue block, lesion,
   original/revised diagnosis, section, platform, GSM and library aliases.
2. Visium cloupe/annotation export keyed by sample and barcode, full category
   dictionary, excluded-spot/QC flags, and author state/clone labels with provenance.
3. Whole-slide images or approved image references, 11 mm ROI squares, Xenium
   lesion/RPII polygons, coordinate units/orientation, H&E registration transforms,
   and polygon-to-cell-ID exports.
4. Xenium cell annotations, centroids/boundaries, counts/transcripts, section/slide
   manifest and TMA core→lesion→patient map. Clarify the discovery cell-count
   difference between Results and Methods instead of selecting one silently.
5. Tables S2–S4, exact base/add-on panels and the processed Figure 1/2/5 objects.
   Specify QC, center inclusion, edge handling and cluster-label mapping used for
   neighborhood plots. Published C15/C16 and TMA C4 names are dataset-specific.

No author message, data-access request or external account change has been sent.
