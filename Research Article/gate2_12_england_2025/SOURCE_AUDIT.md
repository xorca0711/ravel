# Source and design audit, 27 September 2026

**Execution update, 28 September 2026:** the owner authorized the actual analysis after planning. The [first execution batch and four figures](RESULTS_BATCH1.md) are complete: 20 libraries, 44,196 source-QC cells, and 164,453 clonal measurements across 44 source-indexed mice. Numerical verification passed; exact source-state reproduction, independent pool identities and inferential spatial joins remain unresolved. The text below records the original planning/source-intake state.

**Completed:** local article and supplements read; selected main-figure and methods pages visually checked; owner-provided Notion text read; repository hierarchy and relevant historical outputs inspected; GEO SOFT sample fields and matrix dimensions inventoried; public Zenodo archive catalogue and MATLAB source inspected.
**Not completed:** new expression scoring, clone-array decoding, model fitting, author-label recovery, manuscript figure reproduction or any biological experiment. No source code from the archive was executed.

## Source ledger

| ID | Source | What it supports |
|---|---|---|
| P1 | [England 2025](https://doi.org/10.1016/j.stem.2025.01.011), supplied local main PDF, 26 pages | Study claims, figure definitions, methods and data accessions |
| P2 | Local mmc1.pdf, 19 pages | Figures S1-S7 and Tables S1-S3; clonal sampling and supporting phenotypes |
| P3 | Local mmc2.pdf, 9 pages | Methods S1: two-compartment model, conditional clone-size distributions, parameters and fit summaries |
| N1 | [Reading order](https://app.notion.com/p/Thesis_Reading_Order-3d7151616b448093a718e0dfe66d513d) | Gate 2C item 2, companion relationship and intended extracts |
| N2 | [Discussion notes](https://app.notion.com/p/Discussion-3e6151616b44806a98abc043ae5f5844) | Owner's scientific emphasis on growth heterogeneity, feedback, extra oncogenic hits and WT neighbors |
| N3 | [Result-body notes](https://app.notion.com/p/Result-Body-3e6151616b4480a48e4bc43043ab685f) | Figure-by-figure context and candidate questions |
| D1 | [GSE247505](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247505), existing local SOFT and deposited matrices | Twenty sample titles/genotypes, files and dimensions; no verified mouse/pool map |
| D2 | [Zenodo v1.1](https://zenodo.org/records/14673088) | Extracted clonal data and MATLAB analysis/simulation scripts; version and checksums recovered through public API |
| D3 | [Mendeley supporting figures](https://data.mendeley.com/datasets/ss6pb96pty/1) | Supporting-figure deposit; no assumption of full raw image availability |
| R1 | [Cardoso C0](../gate2_05_cardoso_2026/trials/c0_data_reality_check/c0_summary.md), [C3](../gate2_05_cardoso_2026/trials/c3_areg_state_specificity/c3_summary.md) | Prior exposure, measurements, annotation choices and unresolved metadata |

[Source hashes and access record](metadata/source_manifest.json) identify the local/public inputs. Notion pages were unverified working notes, not authoritative primary findings; raw notes and their embedded private image URLs are not copied here. Main PDF figure 3 (PDF p.7), figure 7 (p.13), and methods (p.23) were rendered and checked against extraction. Notes' embedded images were not separately fetched. Page references below use PDF page numbers, including the cover page.

## Sequencing design: keep experiments separate

| Experiment | Population | Time | Deposited libraries | Valid immediate reading |
|---|---|---|---:|---|
| 1 | Confetti RFP and YFP, both WT | 2 weeks per methods | 1 each | Reporter-sorted baseline libraries, not two independent control animals |
| 1 | Red2Kras RFP, mutant | 4 days; 2 weeks | 2 per time | Within-time mutant distributions; cross-sectional change |
| 1 | Red2Kras YFP, WT in oncogenic tissue | 4 days; 2 weeks | 2 per time | Matched-time contextual comparator; pairing remains provisional |
| 2 | Confetti RFP, WT | Baseline; exact time unresolved | 2 | Experiment-specific baseline, not the Il1r1 genotype control |
| 2 | Red2Kras RFP, Il1r1 heterozygous | 2 weeks; 12 weeks | 2 per time | Comparator for homozygous deletion within time |
| 2 | Red2Kras RFP, Il1r1 homozygous deletion | 2 weeks; 12 weeks | 2 per time | Recovered-cell genotype contrast; not a measurement of cell survival or absolute expansion |

P1, PDF p.23, explicitly states that at least two lungs were pooled for every sequencing sample. The analysis unit is therefore an independently prepared pool if independence can be verified; otherwise report libraries only. Individual animals cannot be reconstructed from pooled expression. Reporter libraries sorted from the same pool are related measurements. Equal r1/r2 suffixes are candidate pairings, not evidence of them.

The same paragraph says 13 libraries for the comparative experiment; GEO exposes 10 Experiment-1 samples. Determine whether this reflects merged/split batches, excluded libraries or another documented accounting before claiming an exact source reproduction. It is an unresolved reconciliation, not evidence that data are missing or that the paper is wrong.

The GEO family text also includes a SuperSeries description. Sample-level GSM titles and genotypes, rather than that generic series summary, support this table. The [manifest](metadata/geo_library_manifest.csv) keeps reported replicate tokens separate from unknown biological identities. Matrix header dimensions are an intake measurement, not a QC-passed cell count.

### Consequences for statistical design

- Do not concatenate 4 days, 2 weeks and 12 weeks into an ordinary-Kras time course: 12-week samples come from the Il1r1 experiment.
- Prefer the Experiment-2 het-versus-homozygous contrast at each time. Wild-type Confetti is a different comparison; heterozygous is not synonymous with intact Il1r1 dosage.
- Do not call RFP minus YFP a within-animal effect until the pool pairing is recovered. If unavailable, display unpaired library contrasts and explicitly limit attribution.
- With two reported replicates per arm and unverified independence, make sample-level distributions and effect sizes primary. Cells, bootstrap cell draws, clones within one mouse and technical libraries cannot supply biological replication.
- Changes among recovered epithelial cells cannot estimate total tumor burden, number of initiated clones, absolute AT1 production or organ-wide cellular composition.

## Reuse audit and prior exposure

C3 used Experiment 1 only, with its own QC/doublet and five-signature/modal-cluster annotation. It did not confidently resolve AT1-like clusters or explicitly reproduce England's primed AT2 category. C3's unassigned clusters and 33,217-cell total make it unsuitable as an unqualified six-state source reproduction.

The 4-day RFP DATP-like counts are 44/3,797 and 541/1,921; the existing rounded fractions are 1.16% and 28.16%. At 2 weeks they are 818/3,952 and 1,058/3,415 (20.70% and 30.98%). The new plan must distinguish a variable state fraction from variation in within-state RNA. C3's Areg direction agrees across the four libraries even though the state fractions do not agree closely. These are historical observations, not results produced by this plan.

Source paper QC (P1 p.23): exclude cells with mitochondrial fraction >15%, fewer than 1,000 detected genes, or more than 50,000 UMIs; remove mitochondrial genes and genes seen in fewer than three cells before clustering. Source clustering uses 5,000 HVGs and Louvain; source cross-study integration uses 2,000 anchors (p.24). Existing C3 uses a different MAD/Scrublet/Leiden workflow. Match the source for a labeled reproduction track; retain raw counts for a separately specified repository analysis. Do not tune either track to force the published cell count.

England/C3 and Choi data are already exposed. A future dated contract can make a new analysis reproducible but cannot turn these into untouched validation data. Areg/Itga2/Cd177-selected states require held-out genes or an explicit circularity label if those same genes become endpoints.

## Clone and spatial data availability

The 1,352,723-byte Zenodo archive has SHA-256 `404697263ca941b1b74dee9feb4c4680ff3077d9e20bb7105482d17f14e96a70`; its advertised MD5 matched. It contains `data_analysis.m`, `sim_two_pop_model.m`, 13 MAT files and saved MATLAB figures. The [archive inventory](metadata/zenodo_files.csv) records names, sizes and member hashes.

The analysis source describes `datasets`, `time_points`, `store_sections`, `chlbls`, `lobe_area_total`, `clone_sizes_total`, and `clone_sizes_SPC_pos`. It loops over mice and combines lobes/sections and reporter channels with genotype-specific rules. Distance inputs include `all_ds`, `all_nv_cent`, `all_nv_neigh`, and `all_nv_neigh_spc`: mutant-WT pair distances, central and neighboring clone sizes, and neighboring pro-Sftpc-positive counts. Thus proximity is not automatically blocked for the clonal branch even though it is absent from the RNA matrices.

**Still to verify:** internal array nesting and unique mouse/clone/section identities, distance units, repeated pair handling, area normalization, whether sizes are noninteger imaging estimates, missingness, and clone-merger censoring. Script variable names are not a validated relational schema. The archive contains processed measurements/model code; this audit did not find or validate the original intensity-based segmentation implementation or raw z-stacks. Do not equate `data_analysis.m` with the complete image segmentation pipeline.

Methods S1 conditions its proliferative clone analysis on size >=2, combines lobes within lung, and fits the cumulative tail. A long tail or two fitted components alone does not identify two immutable stem-cell types. One-population overdispersed alternatives and held-out mouse prediction are useful extensions. The original paper itself leaves a single hierarchy as a possibility (P1 p.14).

## Interpretation corrections to carry forward

1. The NF-kB genes in Fig.7I are **Nfkbia and Tonsl**, verified visually. Keep Tonsl as the paper's reported feature, not an interchangeable substitute for another feedback gene or a validated general NF-kB activity meter.
2. The paper reports CD177 induction in non-mutant cells under sustained inflammatory exposure (P1 p.12, S7). Therefore CD177 is neither a mutation assay nor a globally cancer-specific marker. The notes' oncogenesis-specific phrasing is conditional on the compared in-vivo datasets.
3. Faster/slower founder classes inferred from clone histories are distinct from rapidly interconverting transcriptional states after oncogenic reprogramming. No snapshot-based conversion between these labels is justified.
4. Ager/Pdpn RNA, loss of pro-Sftpc, flatter morphology, and functional mature AT1 fate are different readouts. Their agreement is informative; none should silently substitute for the others.
5. The growth-versus-distance and differentiation-versus-distance findings need a joint size-aware analysis. Repeating one significant test and one nonsignificant test does not establish that the two distance effects differ.
6. The old C0 pooling entry and C3 'within-animal' heading are historical wording now qualified by P1 and unresolved identities. Numerical outputs and historical claims are preserved; this audit adds a prospective interpretation correction rather than rewriting their run records.

## Execution readiness

No biological job is running. The bundled Python supports the read-only intake and documentation checks. The checkout's `.venv-x64` launcher currently points to an unavailable interpreter; MATLAB/scientific MAT decoding was not validated in this session. Resolve the analysis runtime before executing EN1 or EN6. This is an environment limitation, not a conclusion that the public data are unusable.
