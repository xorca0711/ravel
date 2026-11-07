# Candidate follow-up source qualification

7 November 2026. Reading/metadata record for Dp1-P01. This separates source
qualification from the subsequent [numerical plan](../CANDIDATE_ANALYSIS_PLAN_V1.md).
Published findings, repository observations and proposed effects are different
evidence categories. All original DuPage outcomes were already inspected.

## TIGIT source identity: a material discrepancy

The [2025 TIGIT paper](https://doi.org/10.1038/s41590-025-02300-w), Data availability,
names E-MTAB-8861 for its WT/Tigit-KO single-cell experiment. Live
[BioStudies metadata](https://www.ebi.ac.uk/biostudies/api/v1/studies/E-MTAB-8861)
and its SDRF instead describe bulk poly-A RNA-seq of Foxp3-GFP reporter Treg/Tconv
populations with/without LCMV WE, associated with older publications. The metadata
reports 19 samples; that is not an animal count. The SDRF also explicitly points
some samples to E-MTAB-6156, so reuse must not be counted as replication.

[Zenodo 14041419](https://doi.org/10.5281/zenodo.14041419) matches the paper's
WT/Tigit-KO, spleen/lung, naive/infected description. Record updated 19 August
2025; deposited dataset date 5 November 2024. Only record metadata and the first
8,192 returned bytes of cell metadata were inspected. Fields include `sample`,
`sample_id`, `Genotype`, `Tissue`, `Condition` and cell annotations; no verified
animal identifier or complete sample map has been established here. The paper's
Methods, "Single-cell RNA sequencing", additionally describes transferred T cells,
sorted-cell remixing and hashtag pooling. These require explicit reconciliation.

Disposition: **matching processed-data lead, not qualified animal-level analysis**.
Do not silently substitute either accession, interpret cells as independent mice,
or label a repair score functional repair. No matrix or RDS was downloaded.
GSE79339/GSE121838 are previously published Blimp-1 sources cited by the same
paper, not new independent validation obtained in this pass.

## EZH2 gain source: qualified for a limited numerical follow-up

[Peeters et al., 2024](https://pubmed.ncbi.nlm.nih.gov/39264807/), STAR Methods
"RNA-sequencing"/"RNA-seq analysis", Figure 7F–G and S7H, and
[GSE262130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262130) were checked.
The series is public from 10 September 2024, last updated 11 December 2024.
RNA-seq compares CD62L-positive sorted Tregs carrying Ezh2 Y641F or WT, directly
after sorting or following four days of CD3/CD28 stimulation with IL-2. GEO
describes three replicate libraries per group (12 GSM records), but does not
establish individual-mouse identities, pool composition or cross-state pairing.

The supplementary DESeq2 tables contain only genes passing the authors' adjusted
p < 0.05 criterion. Their rlog matrix contains the union selected across six
pairwise comparisons; it is **not an unfiltered transcriptome or a raw count matrix**.
The header identifies all twelve genotype/state/replicate columns directly.
Candidate outcomes were not inspected during this header/methods qualification.
Gene IDs and gene names are present. Missing candidate rows will mean unavailable
in this selected release, not no expression or a null effect.

Disposition: eligible for fixed-candidate descriptive rlog contrasts and omission
sensitivity under a new frozen contract. No DESeq2 refit, new FDR, population
intervals or claim of independent external validation. The mutation, culture and
comparator differ from DuPage; gain cannot be assumed to invert loss. S7H already
reuses DuPage for a broad comparison. The new increment is the specified candidate
profile and its measurement limits, not rediscovery of that published broad result.

## Primary evidence and access log

| Source/version and exact locator | Read in this continuation; consequence |
|---|---|
| Panetti 2025, Figures 5–6, Extended Data 8, stimulation and single-cell Methods, Data availability | Retrieved primary BioC text; response depends on context. Source identity issue above remains unresolved. |
| [Zhan, online 11 December 2018 / February 2020 issue](https://doi.org/10.1038/s41423-018-0187-8), Results and Figures 5–6 | Indexed primary Results/legends read. Mixed-cell inflammatory response, purified-cell and ligand-alone limitations narrow the fitness assay. Figure 5 includes replicate wells; Figure 6C–D identifies individual chimeric mice. Direct PMC/Nature and Europe PMC full text failed; no full supplement audit. |
| [DiToro, April 2020](https://doi.org/10.1016/j.immuni.2020.03.013), Results after Figure 1, Figures 2/4 and 6D–F | Full primary page, relevant Results/legends read. desIGF1 bypasses binding-protein regulation; the sequenced cells in Figure 6 are sorted IL-17a-positive/Foxp3-negative Th17. |
| [Karino, online 7 September 2025 / December issue](https://doi.org/10.1002/art.43313), author manuscript available April 2026, Figure 3G–I, in-vitro differentiation Methods | Primary Results/legend/methods read. Polarization context and cleavage make cell source and intact-protein specificity necessary. Supplementary culture recipes not audited. |
| [Miyagawa, online 19 July 2017 / September issue](https://doi.org/10.4049/jimmunol.1600230), abstract | Primary abstract retrieved through Europe PMC PMID28724578. IGFBP4 neutralization in human MSC-conditioned medium increased Treg numbers; source is MSC, not proof of a mature Treg-autonomous mediator. No exact figure or full-method claim. |
| [Shapiro 2023](https://doi.org/10.4049/jimmunol.2200651), Figures 2–3, corresponding Results | Primary text/legends read. IGF plus IL-2 response in NOD splenocytes and expansion context constrain cytokine choice; this is not the Ezh2/IGFBP4 experiment. |
| [TCF1-deficient Tregs, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8428683/), Figure 4B/Extended Data 5H | Indexed primary expression passage only; additional Igfbp4 context lead. Direct full text blocked. Not used as functional proof. |

The same-day [literature context](../LITERATURE_CONTEXT.md) supplies older foundational
sources and the 2024 intestinal microniche context. No study count is treated as
independent support. Not all supplements or citation trees have been read.

## Actual search coverage

Live web search on 7 November 2026, unrestricted older precedents plus explicit
2024–2026 terms, outside the existing PI bibliography:

- `"TIGIT" "PRDM1" "EZH2" Treg 2025 2026`
- `"CCR2" "regulatory T cells" CD25 2024 2025 2026`
- `"IGFBP4" "regulatory T cells" 2024 2025 2026`
- `"CCR2 enhances CD25" "doi"`; `"CCR2 enhances CD25 expression" "CpG"`;
  `"CCR2 enhances CD25 expression" "purified"`
- `"Hyperactivating EZH2" "GSE"`; `"14041419" "TIGIT"`
- `Miyagawa 2017 IGFBP4 regulatory T cells IGF mesenchymal stem cells`;
  `"IGFBP4" "Treg" "Miyagawa"`

DOI-fragment searches for correction/retraction were also attempted for the
2025 TIGIT, CCR2, IGF2020 and ADAM9 papers. They did not identify a relevant notice
in returned results; several queries returned irrelevant hits, so this is not a
complete correction-status clearance. Backward references from DiToro and the
new IGFBP4 lead led to Miyagawa; forward-topic searches found Shapiro and Karino.
No comprehensive citation-index traversal was performed. Computational regulon
and deconvolution hits were not used as perturbation evidence.

## Saved metadata provenance

Public full texts and metadata remain in ignored `raw_data`, not redistributed
in the PR. SHA-256 values refer to the locally saved representations; the
BioStudies helper can serialize text/JSON rather than preserve HTTP wire bytes.
Retrieval date: 7 November 2026.

| Local file under `raw_data/dupage_target_screen_20261107/` | SHA-256 |
|---|---|
| E-MTAB-8861.json | `e2345573ed700551c67d7e8a15162b53558dace00b17816bdbb1e99dd50d1339` |
| E-MTAB-8861.sdrf.txt | `d4e5ef678474dd4732dab93934c961f6d9dd437927830f46e3d77c03bc38f116` |
| zenodo14041419.json | `c96b5477cc6a00fb98ac072606b844a88a7697bca4e746a7d0b695f6b4285a43` |
| zenodo_cell_metadata_preview.txt (incomplete, 8,192 bytes) | `fb0a5fbbd7965c88d882f4ae57decf19ec539ba848b550f096816456be7948b3` |
| GSE262130_series.txt | `0817a415931cc6c2d0191947ca362696a505a96242015a607655b61ea70e4cd7` |

The numerical plan/contract binds the independently downloaded GEO family SOFT,
selected rlog matrix and existing DuPage table exactly. A later successful run
does not remove any of the source or interpretation limits recorded here.
The public downloads are the [GEO family SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE262nnn/GSE262130/soft/GSE262130_family.soft.gz)
and [selected rlog matrix](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE262nnn/GSE262130/suppl/GSE262130_rld_sig_up.txt.gz).
