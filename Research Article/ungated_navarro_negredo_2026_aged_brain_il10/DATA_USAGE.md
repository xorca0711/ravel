# Data usage, source identity and access record

8 November 2026 (Asia/Seoul). Companion to the [fit assessment](README.md).
Counts below describe public metadata and author-reported designs, not a new
biological analysis. Outcomes were already exposed in the supplied paper.

Subsequent owner-requested inspection is recorded in the
[metadata follow-up](METADATA_FOLLOWUP.md): six BioSample attribute records,
four SRA experiment records, assay-specific methods and updated supplement
access attempts. The [current analysis plan](ANALYSIS_PLAN.md) uses that evidence.
This initial audit remains the record of its original source coverage.

## New versus reused data

| Source block | Usage and design | Reuse limit |
|---|---|---|
| Published SVZ atlases: Dulken 2019, Liu 2023, Buckley 2023 | Baseline age/composition and microglial expression context; Fig. 1A merges Dulken/Liu (7 young, 6 old mice); Fig. 1K/code also uses Buckley | These are reused source data, not newly independent replications in this paper. Exact source sample overlap remains to be qualified |
| Sun 2025 MERFISH | Fig. 1H/N and related supplementary panels reuse spatial aging data, including 5 young and 6 old mice for the stated T-cell comparison | No MERFISH D25K intervention dataset is generated here; spatial associations are not intervention or lineage evidence |
| Brain/lung CD8 scRNA/TCR | Old mice, 22–25 months, 11 mice pooled by organ; 3,724 brain and 4,976 lung T cells reported | Matched donor pool, not 11 individually linked mouse transcriptomes; old-only organ comparison |
| RIPR-PD1 scRNA/TCR | Old control versus RIPR, 1 week; cohort 1 pools 4 mice/condition, cohort 2 pools 3/condition | Two experimental cohorts, but cells/clones within a pool are not independent mice |
| Main IL-10 scRNA | 25-month old vehicle n=1; WT and D25K at 0.02/0.1 mg/mL each pool n=2; young vehicle, 3 months, pool n=2; 1 week | One observed library/pool per condition. No young treatment arms; no mouse-level D25K replication |
| Separate WT IL-10 scRNA | Independent old control/WT experiment, 3 mice pooled per condition (STAR Methods; S4L–Q described in Results) | Supports the WT experiment only; does not independently replicate D25K-versus-WT |
| FACS, imaging, ELISA, behavior | Separate animal/culture measurements; Figs. 3–7 and S4 statistics metadata | Do not join these to pooled RNA as matched individuals without an explicit crosswalk |

Primary locators: final PDF pp. 3–8 (Figs. 1–3), pp. 9–15 (Figs. 4–7),
STAR Methods pp. 25–29 and 31–33. PDF p. 25 specifies neonatal primary microglia
of both sexes and peripheral T cells from 12–29-month male mice. In-vivo aging
experiments are male-only. Some final-PDF reference numbers for clocks/baseline
datasets are inconsistent with the bibliography; the Methods, PMC manuscript
and author code identify **Buckley 2023**, not Mogilenko, for the SVZ clocks.

Reused sources:
[Dulken 2019](https://doi.org/10.1038/s41586-019-1362-5),
[Liu 2023](https://doi.org/10.1016/j.stem.2023.03.016),
[Buckley 2023](https://doi.org/10.1038/s43587-022-00335-4),
[Sun 2025](https://doi.org/10.1038/s41586-024-08334-8).
This review verifies their roles, not every underlying accession/sample join.

## Deposits that were actually checked

**Raw sequencing:** [BioProject PRJNA1365936](https://www.ebi.ac.uk/ena/browser/view/PRJNA1365936).
An ENA public `read_run` report returned **20 runs: 14 RNA-Seq and 6 AMPLICON
(TCR-labelled libraries), across six BioSample accessions**. BioSample IDs group
experiments and must not be interpreted as six independent animals.

The main IL-10 block maps to SAMN53298933:

| Run | Deposited library name |
|---|---|
| SRR36091747 | SVZ_IL10_young_control_GEX |
| SRR36091752 | SVZ_IL10_old_control_GEX |
| SRR36091749 | SVZ_IL10_WT_low_GEX |
| SRR36091748 | SVZ_IL10_Mut_low_GEX |
| SRR36091751 | SVZ_IL10_WT_high_GEX |
| SRR36091750 | SVZ_IL10_Mut_high_GEX |

SAMN53298934 maps the separate WT/control libraries (SRR36091745/46).
SAMN53298929/30 identify brain/lung blocks; SAMN53298931/32 identify RIPR
cohorts 1/2. These are library-level metadata mappings; neither hidden donor
identity nor numeric dose is inferred from the names alone. No FASTQ was fetched.

**Processed data:** [Zenodo 17594828](https://zenodo.org/records/17594828),
version v1, stated publication 22 December 2025; record created/modified
23 February 2026. The five listed Seurat objects total approximately 4.2 GB:

| Object | Listed size | Intended role |
|---|---:|---|
| IL10_svz_seurat.rds | 2.2 GB | Main WT/D25K dose comparison and young/old controls |
| WT_IL10_svz_seurat.rds | 402.9 MB | Independent WT experiment |
| RIPR1_svz_tcr_seurat.rds | 1.2 GB | RIPR cohort 1 |
| RIPR2_svz_tcr_seurat.rds | 91.6 MB | RIPR cohort 2 |
| Brain_lung_Tcells_seurat.rds | 358.7 MB | Old brain/lung T-cell comparison |

The landing page lists MD5 checksums and describes filtered high-quality
singlets. It still says GEO accession “XXX”; the article, GitHub README and
actual ENA record instead identify PRJNA1365936. The objects were **not
downloaded or opened**. Availability is verified at the manifest level, not as
validated readable matrices, complete metadata, or a successful reproduction.

**Code:** [GitHub](https://github.com/PalomaNavarro/TargetingImmuneCellsSVZ)
and frozen [Zenodo 18174039](https://doi.org/10.5281/zenodo.18174039), v1.0.0.
The downloaded 46,370-byte ZIP has 17 files, archive prefix commit `c08010b`,
and published MD5 `d34352f0ef77547f8f7f9180edeffd5d`. Source was read, not run.

Consequential code locators (line numbers in the inspected GitHub files):

- `IL10/1.Seurat.R:23–41`: condition-labelled inputs, not donor-labelled
  replicates. Lines 251–252 remove WT50/Mut50 from one plotting view. The code
  contains eight starting labels while the public main IL-10 run block has six;
  **S1 and object metadata must reconcile this**, rather than treating unused
  labels as additional deposited doses or silently dropping them.
- `IL10/2.Microglia.R:225–279`: cell-level `FindMarkers(..., test.use="MAST")`
  comparisons with up to 1,000 cells per identity; these calls do not supply
  independent animal replication.
- `IL10/5.Aging_clocks.R:34–98`: references external training/model objects
  `bootstrap_pseudocell_15.rds` and `models_all_bootstrap.rds`; they are not
  included in this small code ZIP. Pseudocell resampling does not add mice.
- `ImmuneCells/Microglia_FC.R:16–28`: names Liu, Dulken and Buckley inputs.

The scripts also refer to `IL10_svz_seurat_IL10.rds`, whereas the published
object filename omits the final `_IL10`. This requires reconciliation before
running anything; the script is not evidence of a turnkey reproducible pipeline.

**Supplements:** PMC manuscript XML (`PMC12927632.1`, NIHMS2138997) identifies:

- supplement 1 PDF: supplemental material;
- supplement 2 XLSX / **Table S1**: mouse metadata and annotation markers;
- supplement 3 XLSX / **Table S2**: microglial pathway enrichment;
- supplement 4 XLSX / **Table S3**: neural-lineage pathway enrichment;
- supplement 5 XLSX / **Table S4**: experiment details, individual data values
  and statistical tests.

The S1/S4 URLs returned HTML challenge pages rather than XLSX; Europe PMC's
supplementaryFiles endpoint returned XML rather than an archive. No false
download success is recorded. These tables exist in the article's source
manifest but **their cells were not inspected**. No public raw FCS, image stack
or behavioral-video archive was verified. S4's advertised numerical values
would be a useful next input before a complete functional-statistics audit.

## Limits that determine feasible reuse

1. **Pooling is the primary limit.** A pseudobulk sum per condition is possible,
   but one pool per condition cannot estimate between-animal treatment
   variance. Cell bootstraps, label permutations and downsampling cannot repair
   that design. Report finite-sample contrasts if qualified; do not use cell
   counts as biological n.
2. **Sparse control T cells.** Methods report only nine old-control T cells in
   the IL-10 experiment. The published signature test permutes cell labels
   10,000 times. This does not justify an animal-population interpretation.
   Fig. 3K plots only Gzmb-expressing T cells, requiring its conditional
   denominator to be retained.
3. **Readouts are partly selected on observed outcomes.** The inflammation
   signatures use treatment DE genes compared with age directions; they are
   not an independent functional validation. The young/old PCA procedure
   selects 98 PCs after searching 10–100 for maximal separation. Any reuse
   must disclose this selection and cannot label it an unexposed validation.
4. **State and tissue composition matter.** Astrocytes/qNSCs and aNSCs/NPCs
   are combined labels; ependymal recovery is poor. A niche-level shift may
   reflect composition and recovery as well as within-type expression.
5. **Treatment and physiology are not interchangeable.** Microglial IFN markers,
   cytokine release, newborn-neuron markers and behavior are distinct outcomes.
   Their agreement supports the biological argument but not complete mediation
   or a matched cell-to-animal prediction model.

## Search and access log

Search date: **8 November 2026**, Asia/Seoul. Services: live web search; public
NCBI E-utilities, ENA and Zenodo APIs; GitHub connector. Search scope: paper
identity/correction/data, direct Saxton link, related 2024–2026 work and older
contrary IL-10 findings. No date filter was imposed where it could hide older
precedents; explicit year terms supplied recent coverage. This is a bounded
fit review, not an exhaustive systematic search or novelty clearance.

Actual query families included:

- `"10.1016/j.immuni.2026.01.016"`; `"Targeting immune cells in the aged brain" GEO data`;
- `"PRJNA1365936"`; `"Targeting immune cells" "Table S1" Navarro`;
- `"IL-10" microglia aging engineered 2025 2026 D25K`;
- `"Chronic IL-10 overproduction disrupts" neurogenesis`;
- `"Microglia activation orchestrates CXCL10" 2025`; `"Granzyme K" "slow tauopathy" 2025`;
- title-based searches for Dulken, Liu, Buckley and Sun source/data identities.

| Source/version | Actual coverage | Use here |
|---|---|---|
| Navarro Negredo 2026, online 30 January; issue 10 February | Supplied final-format PDF: biological Results, Figs. 1–7 legends, relevant STAR Methods; visual inspection of Figs. 4–7; PMC accepted-manuscript XML | Main data/design/phenotype evidence; supplements separately marked unread |
| Correction, online 25 June; issue 14 July 2026, DOI 10.1016/j.immuni.2026.06.019 | Full correction text at [PMC13440024](https://pmc.ncbi.nlm.nih.gov/articles/PMC13440024/) | Fig. 2K labels and Fig. 4J image; authors report unchanged quantitative analysis |
| Saxton 2021 | Reused current repository source audit/results and same-day literature review | D25K is related to published functional assays, not a GSE160332 RNA arm |
| [Sanchez-Molina 2022](https://doi.org/10.1016/j.bbi.2021.12.026), online 3 January | [Institutional full PDF](https://ddd.uab.cat/pub/artpub/2022/257401/257401.pdf): abstract, animal methods, relevant Results and Figs. 3–4 behavioral legends | Chronic astrocytic WT IL-10 is a contrary context, not a direct D25K replication |
| [Groh 2025](https://doi.org/10.1038/s41593-025-01955-w), online 22 May | Indexed primary Results/Fig. 5–6 excerpts; publisher redirect and PDF size blocked full web retrieval | Context lead: microglial perturbation can increase CD8-associated degeneration; no full methods audit claimed |
| [Mason 2025](https://doi.org/10.1038/s41590-025-02198-4), July issue | Primary abstract/indexed record only; publisher redirect blocked full reading | Contrary-context lead: GZMK CD8 cells can be protective in tauopathy; not a universal harmful-state label |
| [Sun 2025](https://doi.org/10.1038/s41586-024-08334-8) | Primary indexed data-availability and dataset/figure descriptions | Reused MERFISH lineage; [processed source](https://doi.org/10.5281/zenodo.13883177) identified, not downloaded |

Backward references were followed from the supplied paper for the baseline
datasets and contrary IL-10 context. A citing-paper lead appeared in web search
but was not read or used as support; no systematic forward-citation review was
performed. The existing Saxton review's 2026 TYK2/modeling boundaries are reused
without claiming a new full-text audit. No retraction was identified in the
returned records; the explicit correction above was found and read.

## Reproducible retrieval and version notes

Public sequencing query:
`https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA1365936&result=read_run&fields=run_accession,sample_accession,experiment_accession,study_accession,sample_title,library_name,library_strategy,fastq_bytes&format=tsv`

Public full-text XML recovery:
`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=12927632`

Zenodo code metadata: `https://zenodo.org/api/records/18174039`.
Source snapshots are retained in this chat's local artifact directory; no
restricted PDF, raw dataset or credentials were copied into the repository.
SHA-256 identities:

| Source | SHA-256 |
|---|---|
| Owner-supplied 33-page PDF | `b67bc7499aeab877ac43bcdfa2f29ae994e53ee21ec3ff6b7a5dbf433040ef89` |
| Retrieved ENA TSV | `4bf8c10d285379bab4c9958dad887581ad3f0228ca4da502157c5577da3d5b31` |
| Retrieved PMC manuscript XML | `75c65f97aa3cd4c05d4b16d60f53a9fd570d65250a439faadf9ce4baf3b91037` |
| Frozen author code ZIP | `32a26233f686adc621fb8da27d68bb7935395ba44be0380cb27b3325277c1481` |

Public sources may change; these hashes identify the responses examined, not
permanent correctness. Network sandbox DNS initially failed; approved public
API reads recovered ENA, Zenodo and PMC XML. Direct PMC/NCBI browser access,
Europe PMC full-text and supplementary-file access remained incomplete.
