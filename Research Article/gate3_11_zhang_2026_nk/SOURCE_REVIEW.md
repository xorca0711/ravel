# Source inventory and reconciliation

Inspected 10 November 2026, Asia/Seoul. Repository base:
`1a6769fc3d808ccf6b27aed3ecedc71341026f33`.
This is a reading/source inspection; no matrix analysis or numerical run occurred.

## Sources and access

| Source | Verified identity / access | Permitted use and remaining work |
|---|---|---|
| Published article | [DOI](https://doi.org/10.1126/sciimmunol.adx4411), 10 April 2026; supplied 15-page PDF SHA-256 `05e9193c9ff71924063e6bfbadbbb826120c167a635aa7d1750ef1d3f8539273` | Paper text and Figures 4–7 inspected. Publisher web route returned 403; supplied PDF remains the reading source. |
| Earlier version | [bioRxiv 2025.06.26.661417 v1](https://www.biorxiv.org/content/10.1101/2025.06.26.661417v1) is linked by the code README | Version relationship, not a second study. Full version-to-version comparison remains unperformed. |
| GEO | [GSE287581](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE287581), [SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE287nnn/GSE287581/soft/GSE287581_family.soft.gz); saved SOFT last-update field 1 August 2025, compressed SHA-256 `eef0ae83d9f5843f405222265edeff80ccaf87da09504c8b4f382aa5af5ccdaa` | Nine sorted-NK GSM records, three named treatments across rep1–rep3. Existing saved metadata inspected; refresh/hash comparison and machine-checked joins belong to S0. |
| Released code | [Pinned tree](https://github.com/wagnerlab-berkeley/itdt_rna_seq_data/tree/61ac9a440ba3f9db754ff8b8ad5008b450e647c0), current main verified at this commit | README, file inventory, sample metadata, limma and both GSEA scripts inspected. Scripts were not executed. |
| RNA inputs/outputs | Pinned tree contains `input_files/NK_kallisto_tpm.csv`, `sample_info_NK.csv`, three differential-expression and two GSEA output CSVs | Existence and Git blob identities verified; full matrix bytes, feature semantics, dimensions and equivalence to GEO not yet qualified. |
| GEO supplementary matrix | `GSE287581_transposed_kallisto_NK_only.csv.gz` named in SOFT | Do not infer counts or TPM from filename alone. Need byte acquisition, header and provenance comparison. |
| Raw sequencing | SOFT links BioProject PRJNA1213767 and SRX records | Raw-read linkage is a lead; run accession, layout, reference/transcript annotation and complete count reconstruction are not verified. Raw remapping is not the default first job. |
| Figure source data | Article availability statement lists data files S1–S17; tables S1/S3 support RNA/enrichment discussion | Individual files were not acquired in this pass. Supplement/repository/version lookup is an S0 task. No claim of source-wide absence. |
| Other RNA studies in authors' tree | `gse164115_il18_vs_wt.csv`, `gse248977_nkstim_vs_wt.csv` | Published comparator inputs, not independent replication of the intratumoral intervention. Defer importing until a comparison-specific question justifies it. |

The article names “Zenodo (89)” in its availability text, while reference 89 is
the bioRxiv preprint. The targeted archive search did not identify a verified
Zenodo record. Record this as an unresolved locator, not proof no archive exists.

## Unit and sample mapping

The released metadata lists, in order, PBS, ITDT and ITDT_aCD4 for each of
rep1, rep2 and rep3. GEO titles identify GSM8748408–GSM8748416 in the same
treatment/replicate order. This is a provisional identity crosswalk; S0 must
verify a one-to-one matrix-column join rather than rely on positional order.

The paper describes experiments on different days and pooled tumor sorts.
Figure 3 and adjacent prose say three to four tumors; another methods sentence
and GEO say two to four mice. Exact pool membership and animal reuse are unknown.
The RNA observation is one sorted pooled preparation/library. Experimental day
is a blocking factor, not repeated measurement of a mouse across treatments.
Do not multiply the RNA sample size by the pool size. Pool-level inference is
conditional on distinct preparations and valid block assignment.

## Material discrepancies to preserve

| Item | Published paper / GEO | Released implementation at pinned commit | Consequence |
|---|---|---|---|
| Abundance and model | Paper: log-CPM, limma-voom; zero-only filter | `src/limma_nk.Rmd`: reads TPM, retains genes >1 in at least three samples, fits `log2(TPM + 0.5)` using `lmFit`, then `eBayes(trend=TRUE)`; no voom step | First replay must be called released-code reproduction. A count model requires qualified count inputs. A DGEList field named counts does not change TPM semantics. |
| Design | Paper: treatment plus experimental replicate; GEO: treatment-only formula | Code: `~0 + condition + replicate`, replicate sum contrasts | Preserve the source block design; verify rank and identity. GEO and publication are different versions of the method description. |
| Comparisons | Paper emphasizes two; GEO describes three | Code calculates all three, including ITDT+aCD4 minus PBS | Retain all released outputs for fidelity; name the two main biological contrasts prospectively. |
| Significance/display | Paper: BH <0.05 and absolute log2FC >1.5; GEO older threshold >1 | Code contains an intermediate >1 flag but volcano `fc_thr=1.5` | Trace which object feeds each figure/table; do not collapse these thresholds into a single undocumented rule. They are source conventions, not a meaningful biological effect margin. |
| GSEA ranking | Paper says BH-adjusted P value | Both scripts use `statistic = logFC`, after `AveExpr > 1`; comments incorrectly say signed -log10(P) | Replay executable expression. Any alternative ranking is a separate declared sensitivity, not an invisible correction. |
| Version/figure naming | Published Fig.3B/D volcanoes | Released filenames include `fig_3h.pdf` and `fig_3i.pdf`; README still names preprint | Build a panel-content crosswalk. Filename agreement is not figure reproduction. |
| Endpoint labels | Figure 5 caption reverses F/G; Figure 6J Tconv legend has a FOXP3-positive label | Rendered Figure 5 axes show F IFN-gamma, G CD107a | Preserve discrepancy and inspect source worksheets/gates before extracting numeric endpoints. |

## Execution feasibility

S0 metadata qualification is ready to specify. A released-code replay looks
feasible from the public file inventory, but input hashes and runtime/package
availability remain untested. Exact count-based reproduction, source-data
functional reanalysis and full supplemental review remain conditional.
These limits do not prevent completing the paper synthesis.
