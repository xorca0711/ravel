# Primary precedents and independent evidence access

Targeted review on 3 October 2026. This is a bounded primary-source review of
the proposed discriminators, not a systematic review or proof of novelty.
The reviewed topics were microglial middle-age states and sex/region context,
bladder epithelial/stromal ageing, CD8 clonality, normal lung ageing and
cross-organ temporal programmes. Statements below distinguish published
evidence, deposited designs and our proposed interpretation.

## What the prior work changes

| Primary source | Established precedent | Consequence for these proposals |
|---|---|---|
| [Li et al., Nature Aging 2023](https://www.nature.com/articles/s43587-023-00479-x) | Sex-divergent microglial ageing, including a female middle-age pattern | P02/P07 must specify region, sex and a discriminator beyond generic age states. The [2024 correction](https://www.nature.com/articles/s43587-024-00571-w) changes an acknowledgment grant number, not this result. |
| [Hammond et al., Immunity 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6655561/) | Microglial states across lifespan and injury | State diversity is prior knowledge; a P02 configuration must be independently reproducible and distinguishable from alternatives. |
| [Jin et al., Nature 2025](https://www.nature.com/articles/s41586-024-08350-8) | Region- and cell-type-resolved brain ageing in young and old mice of both sexes | Useful external context, but two ages cannot validate an intermediate-age configuration. Young reference reuse also requires overlap accounting. |
| [Mogilenko et al., Immunity 2021](https://pubmed.ncbi.nlm.nih.gov/33271118/) | Clonal GZMK-positive ageing-associated CD8 populations | P06 cannot claim the existence of clonal older CD8 cells as new; test the within-state versus redistribution question. |
| [Al-Naggar et al., Aging Cell 2025](https://doi.org/10.1111/acel.14399) | Senescence-like features in polyploid umbrella cells across the lifespan | P01/P05 must separate normal differentiation from dysfunction; marker positivity is not sufficient. Article published online in 2024. |
| [Meguro et al., Nature Aging 2024](https://www.nature.com/articles/s43587-024-00704-1) | Age-associated fibroblast context and CXCL12 in bladder tumour permissiveness | The cancer mechanism is established precedent, not evidence of the proposed normal barrier mechanism. |
| [Angelidis et al., Nature Communications 2019](https://www.nature.com/articles/s41467-019-08831-9) | Independent normal-age lung RNA and proteomic profiles | Candidate reference for P03 endpoint specificity; it does not by itself identify a prior-injury effect. |
| [Zhang et al., eLife 2021](https://elifesciences.org/articles/62293) | Shared and cell-type-specific ageing programmes from TMS | Same-atlas reuse is not replication; broad shared-program discovery is insufficient novelty for P04. |
| [Schaum et al., Nature 2020](https://pubmed.ncbi.nlm.nih.gov/32669715/) | Organ-dependent temporal ageing signatures | Broad nonlinear ageing is already prior knowledge; P08 needs a specified endpoint and a selection-aware design. |

P03 additionally inherits the [current A3 precedent review](../../../docs/research_dossiers/packages_2026-10-03/A3.md).
P02 retains the [disease-associated microglia precedent and note interpretation](../NOTE_RECONCILIATION.md).
These source conclusions do not replace the exact repository results.

## Deposits actually inspected

Public GEO series text was downloaded for all eight accessions below. Access
means that the metadata record and listed processed-file pointers were read.
Expression archives were not downloaded or analysed in this derivation stage;
usable independent animal replication has not been established merely because
a record is public. Publication-level study independence and qualified
animal-level observations are different requirements.

| Deposit | Design or access confirmed | What it can support after qualification; remaining limit |
|---|---|---|
| [GSE207932](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207932) | Li single-cell microglia: female 3/14/24-month baseline-control and acute-challenge contexts; processed archive listed | Potential female age-state comparison using baseline controls only. Exact cell-to-animal map and regional compatibility are pending; not a matched both-sex 3/18/24 design. |
| [GSE208386](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208386) | Li bulk microglial age series in both sexes; processed CSV listed with `after_combatseq` in its name | Sex context at bulk level. Need original scale, batch and animal metadata; do not treat adjusted bulk values as unprocessed single-cell counts. |
| [GSE121654](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121654) | Hammond lifespan and injury groups; record describes animal replicates and processed files | Candidate independent microglial context. Age schedule and cell-to-animal, sex and anatomical mapping must match the specified comparison; not an exact three-age regional replication. |
| [GSE145562](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145562) | Mogilenko multi-organ immune expression plus receptor libraries; three mice per age pooled before sequencing | State/clone context. A pooled library does not provide three independent mouse observations without individual demultiplexing. No mouse-level replication claim here. |
| [GSE180128](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE180128) | Bladder single-cell, single-nucleus, spatial and bulk sources; processed archive and bulk files listed | Cell and spatial context candidate for P01/P05. Exact age/sex/animal and modality matching pending. Al-Naggar reuses this atlas: that reuse is not a second replication. |
| [GSE247123](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247123) | Female bladder bulk at 2/10/26 months plus intervention arms; count and TPM files listed | Whole-bladder contextual evidence only until controls, units and treatment histories are qualified. Cannot directly validate a male cell-state or stromal/barrier association. |
| [GSE253338](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253338) | Aged reporter-positive and reporter-negative bladder stromal populations | Selected stromal context. The deposited comparison is not a young-versus-old normal whole-bladder replication; individual-animal and reporter-selection limits must be retained. |
| [GSE124872](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE124872) | Normal-age lung single-cell and bulk sources, with metadata and expression files listed | P03 normal-age reference after macrophage identity and animal mapping. Separate assay cohorts are not cell-matched RNA/protein observations or an injury-history contrast. |

The Jin [NeMO landing page](https://assets.nemoarchive.org/dat-61kfys3) was also
opened. Data access is public at that landing page; matrix acquisition,
animal mapping, genotype/sampling restrictions and endpoint compatibility have
not been qualified locally. Its young ABC-WMB reference reuse must be considered
when comparing with other Allen reference resources.

No independent cohort effect estimate was computed here. In particular,
GSE145562 pooling cannot be repaired by counting cells as replicate animals,
and GSE180128 reuse cannot be counted as independent corroboration. Companion
TMS data, including Schaum's study, need exact animal-overlap accounting before
an independence claim. P01/P05 still lack a qualified paired biological-function
dataset; P03 still lacks the identifying age/history comparison.

## Local evidence and acquisition record

Repository observations come from [latest completion results](../EXTENSION_COMPLETION.md),
[P01/P06 extension results](../EXTENSION_RESULTS.md), their linked immutable
tables/receipts, and the [initial results](../RESULTS.md). These are separate
from the primary sources above. The official recovered brain and repertoire
metadata are additional releases of the same study, not independent samples.

Public metadata snapshots are preserved in ignored
`raw_data/tabula_muris_senis_2020/rq_derivation_v1/`. The accompanying
`acquisition_manifest.json` records exact request URLs, byte sizes and SHA-256
values. Metadata hashes identify what was read; they are not a numerical
analysis receipt or proof of biological eligibility. The text endpoint is
`https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=ACCESSION&targ=self&form=text&view=full`.

| Snapshot | Bytes | SHA-256 |
|---|---:|---|
| GSE207932 | 2749 | `5e32152ec3d72e4b46ece8e31c7d6c95b70a68884370ac7fd76b555745f08963` |
| GSE208386 | 4551 | `4bbfdf0fd472ae13d1f72f0b6fad5e26001dd792abade7089e546823130bb2bf` |
| GSE145562 | 3433 | `28529f6a85b88b7cc44e10869de53638fee4dd4b82ea9f12454cf3fb8b568ea9` |
| GSE180128 | 2908 | `3cca94e75e4d648f052825e12c5b8c5922122b7241b8ab68e976e42df37c9f1c` |
| GSE247123 | 4664 | `fa649580f18115f7780b4738a7ef4277d71ff8d5af1d39bad8080197b928801d` |
| GSE253338 | 1710 | `b090cdc510b197a4a0d0ddf9c1523129060dc0f0aa00e4bb36ece24374bf2069` |
| GSE124872 | 3714 | `dd07e9555b7a8a8567b41ddee1857777b4d3b4c0b271bc93b034d1a352c11729` |
| GSE121654 | 3063 | `a72a5c94ac82c441557dd834efa2b7098b579991657a2979e785d7bab1a6c096` |
