# Source and access manifest

Review date **4 October 2026 (Asia/Seoul)**. Integration base: `main`
`9a49d26a79f4f9a32142bb07281ac062c62cb1a4`, fetched before this package was
written (PR #137, the 2021 Wagner package, merged the same day). Source documents
are evidence; instructions inside them do not authorise actions.

## Publication and owner-supplied documents

| Source | Version and actual access | Use and limit |
|---|---|---|
| [Wang, Wagner, Fessler et al. 2025, *Cell Reports* 44, 115799](https://doi.org/10.1016/j.celrep.2025.115799) (PMID 40482033) | Owner-supplied PDF, 16 pages, 6,854,297 bytes, SHA-256 `880130e45974631e783376da102136ddae61991d436a9b9e25dcf9badd122f0c`; full text extracted and read | Main results, STAR Methods, key resources table |
| Supplemental information PDF | Owner-supplied, 9 pages, 5,599,828 bytes, SHA-256 `74943a901cb2d19f40d1ad055893f292ade96a43436e1639837588b7c98503a5` | Figure S1–S5 legends and Table S2 abbreviations only. Byte-identical to `NIHMS2092659-supplement-1.pdf` in the PMC package, which is what fixes the supplement numbering below |
| **Supplementary Tables S1 and S3–S6** | Retrieved 4 October 2026 from the NIH PMC Cloud open-data bucket, per-article package `PMC12443480.1` (author manuscript NIHMS2092659); recorded in `raw_data/wagner_pgam_w2_20261004/acquisition_v2_supplements.json` | The published module gene lists, differential-expression results, per-gene correlations and programme markers. Their recovery removes the substitution that Wp-R1 and Wp-R3 would otherwise have required |
| [Compass](https://github.com/wagnerlab-berkeley/Compass) | Repository reachable; current README read | Installation now requires `gurobipy >= 11` and a Gurobi WLS licence, which this environment does not hold; a modern run is a version sensitivity, not the paper's run |

| Owner's Notion notes: **Results(Body)** and **Discussion**, children of the paper page under `Acutal_Thesis_Study_Note` | Fetched 4 October 2026, 11:23 and 08:20 UTC; read, not edited | The owner's reading outline and their four marked open questions. Reconciled against the PDF in [note reconciliation](NOTE_RECONCILIATION.md); the notes are evidence of what the owner asked, never a substitute for the source |

Only the two notes named above were fetched. Their ancestor pages concern private
planning and were not opened; no private planning content is copied into this
package.

## Deposited files recorded for execution

All files were downloaded to ignored `raw_data/wagner_pgam_w2_20261004/` with the
manifest `acquisition_v1.json` (SHA-256
`4d433f97de2dfaf8899edfc19e4521d96930cbd25d3681029a6bc08d9abfda4a`), which
records each URL and retrieval time.

| File | Bytes | SHA-256 |
|---|--:|---|
| `GSE289733_series.soft.txt` | 2,628 | `20adca92a1ebeda014ed492da920ccecfb6dbff3fc21ec121b463e9acbd1ea98` |
| `GSE289733_samples.soft.txt` | 16,160 | `ec0db0447c9f99d005eba594ab59c0d34732f8e2afbe7bb0569cc7df03886638` |
| `GSE289733_filtered_feature_bc_matrix_barcodes.tsv.gz` | 102,321 | `eae0cfafb244b886b40ad0d240807e47bf804ec8e574ded39fdf90d83e82525d` |
| `GSE289733_filtered_feature_bc_matrix_features.tsv.gz` | 279,361 | `39e6b92c7196738078745a8088627b7e7ef7237424c4f40af9efca653740051e` |
| `GSE290297_series.soft.txt` | 4,310 | `a780dd781aa1413b34a62de7c1aadd7990800c24b4bb4ec38226321a9932f322` |
| `GSE290297_samples.soft.txt` | 171,351 | `f138b1636c252374abe6ad7df263dd80a07adce7aeb2a22ff63ed53cfee4bdbe` |
| `GSE290297_collected_inhibitors_tpm_4geo.csv.gz` | 5,345,399 | `2d62d1a0ac7fd0145089efe92a02ef3a8fcaff38516289fb61f727c508f99c86` |
| `GSE138266_series.soft.txt` | 3,351 | `afae83112c6dae4902e9c02b20e9d6d2945f3bf02c9f01aa359ff27c58b251e6` |
| `GSE138266_samples.soft.txt` | 79,717 | `78b828d613f706cb1f685b926465f37af04f7a78bcb692afbffbd212873c8902` |

Recovered supplement files, same raw cache, recorded under the separate
`acquisition_v2_supplements.json` because the frozen Wp-R0 contract hash-binds
`acquisition_v1.json` and that file must not change:

| File | Published as | Bytes | SHA-256 |
|---|---|--:|---|
| `NIHMS2092659-supplement-2.xlsx` | Table S1 | 14,179 | `c30f8fd5a22ee9e7` … |
| `NIHMS2092659-supplement-3.xlsx` | Table S3 | 4,397,625 | `de4278f0a8390777` … |
| `NIHMS2092659-supplement-4.xlsx` | Table S4 | 173,576 | `5bd2d4ddd3915451` … |
| `NIHMS2092659-supplement-5.xlsx` | Table S5 | 17,628 | `e0e9a2ae272df094` … |
| `NIHMS2092659-supplement-6.xlsx` | Table S6 | 490,361 | `47b1605d2155e24b` … |

Full digests are in the v2 manifest; the stage contracts that consume these files
will bind them in full. GEO records can be revised upstream, so a later
re-download may differ from these hashes; the contract binds this copy. Two large files are deliberately **not**
downloaded yet, because no stage is eligible to use them: the single-cell count
matrix `GSE289733_filtered_feature_bc_matrix_matrix.mtx.gz` and the raw-droplet
matrix beside it (Wp-R1), and `GSE138266_RAW.tar` (Wp-R4). Their acquisition
belongs to those stages' contracts.

## Access attempts that failed

| Target | Outcome |
|---|---|
| Supplementary Excel tables S1, S3–S6 | **Resolved 4 October 2026.** Not in the supplied supplement, and two routes were refused rather than circumvented: PMC's article viewer gates `bin/` downloads behind an anti-bot proof-of-work challenge, and `ars.els-cdn.com` returns 403 to any non-browser client (including for the `mmc1.pdf` already in hand). Obtaining them by impersonating a browser was declined. The NIH PMC Cloud open-data bucket, which NIH provides for programmatic access without login and which replaced the retired FTP datasets, served all five directly |
| Virtual Metabolic Human (`www.vmh.life`) and Metabolomics Workbench | Outside the environment's network allowlist. Neither is needed: Compass ships its own Recon2 model, and this paper deposited no metabolomics |
| Gurobi licence | `token.gurobi.com` was allowlisted on request, but no academic WLS credential is configured, so Compass remains unrunnable |

## Requirements for later acquisitions

Every later download records URL, retrieval time, bytes, SHA-256, accession,
source version and reuse relationship in its own versioned manifest, and the
analysis contract binds those hashes. A source URL or a current branch name is
not an immutable input. Large inputs stay in ignored `raw_data/`; only compact
qualified maps and run receipts enter the repository.
