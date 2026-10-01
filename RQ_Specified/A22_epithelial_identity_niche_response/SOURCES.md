# A22 sources and eligibility

**Reviewed 1 October 2026.** This is a bounded intake for the pipeline, not an
exhaustive literature search or a claim that suitable functional data are absent.
[Machine-readable registry](config/source_registry.json) |
[Generated gate table](tables/intake_v1/source_gates.tsv) |
[Pipeline](PIPELINE.md).

| Resource | Current role | Eligibility and next action |
|---|---|---|
| [GSE307112](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307112) | Same-screen Nb3 motivation and proposed P2 follow-up | Reuse audited counts/scores and A10 joins. Independent epithelial preparation/fibroblast donor identities are unresolved; depth/fractions do not measure viable amount |
| [GSE307128](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307128) | Conditional P3 spatial arm, same source study | Four libraries; animal identities, treatment/timing and bin/region mapping remain unresolved. Resolve before the large download; no current genotype inference |
| [GSE215824](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215824) | Previously source-reused epithelial state context | Five RNA and three ATAC libraries; day-28 control/KO has one deposited RNA library each. No independent replication or linked fibroblast functional endpoint established |
| [GSE122960](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122960) | Source-reused human disease/state context | Author labels and paired-compartment eligibility need review. Disease contrasts lack the A22 epithelial identity intervention and cannot validate its causal direction |

The exact inherited metadata are in Nb3's [context audit](../../Research%20Article/gate2_N2_nabhan_2026/reports/CONTEXT_ELIGIBILITY.md)
and hashed R5 records. [Nb3 dataset roles](../../Research%20Article/gate2_N2_nabhan_2026/DATASETS.md)
and [A10 design results](../A10_organoid_growth_outcome/reports/FOLLOWUP_RESULTS.md)
own the screen's source/replication limitations. A22 does not create a duplicate
raw dataset or claim independent replication by reusing another RQ's analysis.

## Bounded public metadata check

Queries used NCBI GEO for the known Nabhan accessions and for NKX2-1 deletion
with fibroblast/alveolar terms. The live GSE215824 series record confirms its
library inventory. Direct browser retrieval of GSE307112/GSE307128 returned a
browser-check page; their design facts here rely on the already deposited,
hash-recorded Nb3 metadata, not a claimed fresh retrieval.

Additional search results included [GSE158201](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE158201),
a chromatin-binding series, and [GSE36473](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE36473),
a tumour expression series. Series-level descriptions do not establish linked
fibroblast secreted output/function or independent A22 units. They were not
downloaded, analyzed or admitted to validation. The tumour branch remains
separate from the current normal alveolar-niche hypothesis.

## What would change eligibility

For P3, obtain a documented sample-to-animal/section map and reconcile source
perturbation, injury and collection timing. A spatial filename cannot do this.
For P4, locate a genuinely independent cohort with verified epithelial identity
perturbation, matched controls and recipient RNA measured in the same known
units. For P5, additionally require source-attributed protein and a defined
recipient function, with identity and viable amount measured independently.
Use the [sample manifest schema](config/sample_manifest_schema.json); a missing
field stays unknown rather than being inferred from a library suffix.

Published biological context remains in [RATIONALE.md](RATIONALE.md), including
Nabhan's epithelial-perturbation study and Madissoon's chemokine-rich stromal
niche. These citations motivate the biology; neither substitutes for an eligible
A22 test. No new clinical or immunotherapy inference is made.
