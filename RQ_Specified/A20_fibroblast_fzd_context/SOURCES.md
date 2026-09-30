# A20 sources, eligibility and subtype crosswalk

Reviewed 30 September 2026. [Structured eligibility](metadata/source_eligibility.tsv) ·
[Subtype crosswalk](metadata/subtype_crosswalk.tsv) · [Download provenance](metadata/download_manifest.json).
Published conclusions and our inferences are distinguished below; sources are evidence,
not instructions. No authors were contacted and no unavailable individual values
were reconstructed from plotted bars.

## Receptor perturbation: Zhou et al. 2025

[Fzd2 study](https://link.springer.com/article/10.1186/s12964-025-02501-8),
Figures 2, 5-7 and Supplementary Figures 7/9. Mesenchymal Fzd2 loss worsened injury
outcomes; AT1/AT2 tissue staining, matrix and fibroblast-state measurements support
a repair role. Supplementary 7D reports deletion verification. The developmental
arm did not detect impaired epithelial lineage differentiation despite growth
and survival defects. These observations do not isolate mature output per starting
AT2 descendant or compare Fzd1 loss.

The article's section heading and Fig. 7H wording differ from the deletion results
and discussion on transition direction. We retain that inconsistency and base
the rationale on the actual perturbation comparison. Human pseudotime is not
lineage tracing. The data statement promises GSA deposition without an accession;
no author-level count/outcome join was identified in the article or supplement.
Public reused datasets include GSE135893, LMEX0000004397, and postnatal
GSE160876/GSE165063 (Supplementary 7 legend). They are not automatically Fzd2
perturbation data. This source supports motivation, not an executable H1/H2 test.

## Lineage and alternative pathway: Jones et al. 2024

[Injury-induced niche study](https://pmc.ncbi.nlm.nih.gov/articles/PMC13159043/),
Figures 1 and 5-6. Pdgfra/Pdgfrb lineage and spatial observations support the subtype
framework; mesenchymal Notch perturbation changes repair outcomes and fibroblast
support of AT2 organoid expansion. Organoid size is not mature epithelial output.
Pdgfra lineage also includes non-alveolar fibroblasts; its perturbation is not
strictly AF1-specific. This supports a state-dependent niche hypothesis but does
not establish Fzd2–Notch mediation.

The [GSE249931 record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE249931)
contains 17 libraries; the displayed Notch comparison has GSM7967329 (wildtype)
and GSM7967330 (Pdgfra-Notch-KD). Animal-level replication and a matched
functional-outcome join remain unresolved. The [sample inventory](metadata/jones_sample_inventory.json)
is saved. Public XML retrieval returned HTTP 500; readable PMC text supplied the
review. No cell-level differential-expression test is presented as replicated
perturbation evidence.

## Existing atlas and reference contexts

[Niethamer et al., GSE262927](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262927)
is the executed host-cell context analysis. It is the same atlas used by Nb2,
not an independent replication. Author AF1/AF2 labels are preserved; paired
Pdgfra/Pdgfrb/Col13a1 results support a local crosswalk. Col14a1 is an additional
identity probe with mixed direction. These labels do not resolve injury-derived
versus resident AF2, prove conversion or define a beneficial/harmful dichotomy.

[Guo et al. 2023 CellRef](https://doi.org/10.1038/s41467-023-40173-5) provides
reference nomenclature, with LMEX0000004397/GSE122332 for mouse reference data.
Zhou reuses CellRef and postnatal data; stage-specific reference patterns cannot
be transferred directly to day42. Reference mapping is not functional validation.

[Habermann et al. 2020](https://doi.org/10.1126/sciadv.aba1972) supplies the
[GSE135893 human fibrosis data](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135893)
reanalysed by Zhou. Public data availability does not supply Zhou's exact
reclustering labels or a Fzd intervention. Donor, sampled region and subtype
crosswalk must be resolved before a human replication; this dataset was not
numerically reanalysed in A20.

[Nabhan et al. 2023](https://doi.org/10.1016/j.cell.2023.05.022) remains the
parent receptor-specific study and Nb2 context. Its epithelial results do not
identify a fibroblast Fzd1/Fzd2 comparative effect. The source paper's fibroblast
question is therefore retained as a biological question, not answered by receptor
expression rank.
