# Nb3 context eligibility, 1 October 2026

The GEO family records were downloaded and hashed by
[09_context_metadata.py](../scripts/09_context_metadata.py). This is an eligibility
audit; no spatial genotype effect or external cell-state contrast has been fitted.

| Dataset | Confirmed deposition | Eligible use and unresolved issue |
|---|---|---|
| [GSE307128](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307128) | Four spatial libraries: WT blocks 8/16 and Nkx2.1 KO blocks 10/15; every sample says bleomycin, batch 25036. Processing specifies 8-micron SpatialData bins. | Source Fig. 5 comparison held. The article/SI describes an AAV perturbation; no deposited animal identifier or explicit bridge between those treatments is supplied. The series-level design mistakenly describes the organoid bulk experiment. |
| [GSE215824](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215824) | Five RNA and three ATAC libraries. RNA includes WT days 14/21/28 and day-28 AAV control/Nkx2-1 KO. | Toth et al. source context recovered. One deposited library per condition does not establish independent replication. These are already used by Nabhan, so any reuse is source reconstruction, not independent validation. |
| [GSE122960](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122960) | Eight donor lungs, eight fibrotic explants (four IPF, one HP, two SSc-ILD, one myositis-ILD), plus one separate IPF cryobiopsy. Processed filtered matrices are public. | Reyfman et al. is identified in Fig. S6. The eight-plus-eight source cohort can be distinguished from the cryobiopsy, but the exact source PCA, author cell labels and AT2 subset assignment have not been recovered. No new trajectory or disease-specific inference is reported. |

Exact retrieved records: [spatial](../runs/R5_v1/GSE307128_metadata.json),
[Toth](../runs/R5_v1/GSE215824_metadata.json),
[Reyfman](../runs/R5_v1/GSE122960_metadata.json).
Cached original SOFT files remain under ignored `raw_data/Nb3_context_metadata/`.

The spatial report requires a sample-to-animal map, treatment/time-point
reconciliation and the relationship between the article's reported grid and the
8-micron deposited bins. Two animals per group, as reported by the paper, cannot
be expanded into independent observations by counting bins. Large spatial image
archives were not downloaded because they cannot resolve the current design
ambiguity by themselves.

For the human reference, the next concrete inputs are the original author cell
annotations/PCA and a fixed donor-aware analysis contract. Public processed
matrices are sufficient for expression work; controlled-access FASTQs are not
needed for this stage. E2 state comparisons and E5 receptor localization remain
separate from clinical toxicity or causal repair claims.

The paper's DepMap comparison also remains unreproduced: body and caption use
different line counts (93 versus 96), and the release, assay and line-selection
list are unspecified. A contemporary DepMap release would be a separately dated
extension, not an exact reconstruction of that comparison.
