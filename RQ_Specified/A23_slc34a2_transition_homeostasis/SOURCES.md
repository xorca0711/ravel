# A23 source eligibility and acquisition priorities

**1 October 2026 update.** Processed matrices and the source workbook are now
analyzed in the [external results](reports/external_pilot_v2/RESULTS.md). The
immutable initial registry and intake gates below record the earlier search state. [Source registry](config/source_registry.json) |
[Generated gates](tables/intake_v1/source_gates.tsv) | [Pipeline](PIPELINE.md).

| Source | Role and next step | Limitation |
|---|---|---|
| [GSE307112](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307112) | Preserve Nb3 discovery and audit exact subsets | Bulk technical wells; not independent validation |
| [GSE199329](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE199329) | First external processed-count and epithelial-coverage audit for P2 | Disease-case context with sampling/age/donor confounding; no replicated causal effect |
| [Uehara 2023 source data](https://doi.org/10.1038/s41467-023-36810-8) | Audit biochemical endpoints and per-subject links for P3 | Same study as GSE199329; workbook retrieved in the execution batch; no explicit cross-assay subject IDs in selected biochemical sheets |
| [GSE141259](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE141259) | Reuse [A1's state/time source audit](../A1_transitional_epithelial_state_distinction/STUDY_MAP.md) | Repair reference, not an SLC34A2 intervention or independent validation of its mechanism |
| [GSE215824](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215824) | Source-reused NKX2-1 comparison context only | Different perturbation; no routine new numerical fit proposed |

## Newly verified metadata

The official [GEO SOFT family file](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE199nnn/GSE199329/soft/GSE199329_family.soft.gz)
was retrieved and hashed. It contains three samples: CD45-negative PAM1,
CD45-positive PAM2 and control D071, labeled as a 24-year-old normal donor.
GEO advertises processed raw/filtered feature-barcode HDF5 matrices. Three filtered matrices and their epithelial coverage are now inspected. See the
[parsed record](metadata/external_source_v1/GSE199329_metadata.json) and
[sample roles](metadata/external_source_v1/SAMPLE_ROLES.md).

The [primary article](https://doi.org/10.1038/s41467-023-36810-8) describes one
PAM child explant and one control. Its focus on myeloid/mineral biology provides
a secondary-injury alternative, not a tested epithelial state sequence.
The two PAM libraries must not become two patients. Fraction-enriched sampling
and the unmatched disease/age comparison limit any future RNA summary to
case context; batch correction does not resolve that design.

## Biological context and search boundaries

[Saito et al. 2015](https://doi.org/10.1126/scitranslmed.aac8577) grounds the
transport/homeostasis model already cited in [RATIONALE.md](RATIONALE.md).
Its model-level evidence is not a newly analyzed independent A23 state dataset.
The 2023 study supplies a source-data lead for separating biochemical compartments
and mineral/inflammatory responses. Neither source is assumed to contain a
linked transport-state-time-restoration experiment.

Searches used SLC34A2/Slc34a2, Npt2b, pulmonary alveolar microlithiasis, GEO,
RNA-seq and single-cell terms. Tumour fusion, non-lung and generic marker hits
were not admitted as SLC34A2-loss validation. Discovery of GSE199329 changes the
next feasible step from an unspecified cohort search to the now-completed coverage
audit; it does not close the temporal or functional gates. The search was
bounded, not a systematic claim that other data are absent.

Existing Nb3 [dataset roles](../../Research%20Article/gate2_N2_nabhan_2026/DATASETS.md)
and [context audit](../../Research%20Article/gate2_N2_nabhan_2026/reports/CONTEXT_ELIGIBILITY.md)
remain authoritative for source reuse. No new raw sequencing, large image
bundle, patient contact or experimental intervention is part of this intake.
