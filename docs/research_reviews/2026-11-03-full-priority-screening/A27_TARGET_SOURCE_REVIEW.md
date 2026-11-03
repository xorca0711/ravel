# A27: source rationale for the fixed operational CD8 labels

3 November 2026. Bounded pre-run marker review; no local marker effects,
age separation or clone support inspected to choose the rule. This supplements
the [A27 sequence](PLANS.md#a27--cd8-repertoire-concentration-versus-state-redistribution).
It does not validate a new cell taxonomy or change the nine nominated genes.

## Marker rationale and contrary context

[He et al. 2025](https://doi.org/10.1073/pnas.2425992122), Results sections
on CD8 clusters and age-associated Gzmk populations, Fig1D and Fig6A, provide
a directly relevant mouse splenic RNA reference. The first group below is
shared with memory/stem-like contexts; it is not specific to naive cells.

| Prespecified genes | Narrow source support | Limit for the local annotation |
|---|---|---|
| Tcf7, Lef1, Ccr7 | Naive/stem-like clusters; Ccr7 also in central memory | A detected transcript is not an antigen-history certificate |
| Il7r | Also expressed by effector-memory and tissue-resident memory populations | Retain as context, not a naive-specific marker |
| Nkg7, Ccl5, Gzmk, Gzmb, Prf1 | RNA associated with Gzmk-positive CD8 populations and cytolytic/inflammatory context (Fig6A) | Not direct killing, cytokine secretion or one homogeneous terminal state |

Consequently, the proposed labels must remain **naive-associated RNA**,
**effector-associated RNA**, mixed and indeterminate. The fixed detection rule
is an analyst-defined conservative partition, not a classifier published or
validated by He et al. Missing features must not become biological zeros.
Dropout, RNA depth, memory overlap and recovery differences can change category
membership; label names must remain qualified in tables and figures.

## Closest precedents and recent extension

[Ahmed 2009](https://pubmed.ncbi.nlm.nih.gov/19124721/), abstract and PubMed
Fig1 description, reports age-associated repertoire restriction within purified
naive CD8 cells. [Mogilenko 2021](https://pubmed.ncbi.nlm.nih.gov/33271118/),
abstract, reports highly clonal GZMK-positive ageing-associated cells distinct
from conventional effector memory. Neither establishes the nine-gene rule here.
These already-published within-state phenomena rule out claiming their first
discovery from the local screen.

[Shchukina 2026](https://pubmed.ncbi.nlm.nih.gov/42030157/), published abstract,
adds cell-extrinsic, aged-tissue context to the development of GZMK-positive
populations. This is the published successor of the 2025 preprint, not a second
independent study. Only its abstract and publication/update metadata were read;
no figure-level mechanism was independently reviewed. It reinforces that local
RNA/repertoire associations cannot isolate cell-intrinsic ageing from host
environment. No new experiment or mechanistic inference is added to this run.

## Access and search record

Actual search date: 3 November 2026. Queries:

- `"Tcf7" "Lef1" "Ccr7" "Il7r" "Nkg7" "Prf1" mouse CD8 single cell 2025`
- `"Mogilenko" "2021" "Lef1" "Gzmb"`
- `"CD8" "aging" "Gzmk" "2025" single cell naive`

The search included recent primary studies and relevant older precedents,
including findings that contradict naive-specific or homogeneous-effector
interpretations. Other tumor/human/primate hits were not used to define the
mouse rule. This is not a systematic review or novelty certification.

He et al. full article XML was retrieved from the public
[Europe PMC endpoint](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12002302/fullTextXML)
after PMC web access returned a browser challenge. Read: the relevant Results
paragraphs and Fig1/Fig6 legends. Supplementary figures were not independently
visually audited. The role table relies on RNA results, not ATAC-derived gene
activity relabelled as RNA. Ignored cache:
`raw_data/full_priority_20261103/A27/mouse_aging_2025.xml`, SHA256
`52bcf65bf9552d4eba3532e237a21e65e9980ad2924581286a629d93fa507fa1`.
PMID40163732, DOI10.1073/pnas.2425992122, published31March2025.
Ahmed/Mogilenko/Shchukina access was through their primary-paper PubMed records
at the levels stated above; no full-text claim is made for them.

## Pre-run decision

The fixed panel is suitable for a **qualified descriptive RNA partition**.
Use all annotated CD8 cells for the observed receptor-recovered fraction,
preserve clone IDs across states, retain failed animal/state support and use
the inherited depth-five endpoint only where eligible. The two marker groups
need not be mutually exclusive biologically. Neither weaker within-state
differences nor changed category proportions alone quantify how redistribution
explains pooled repetition. Keep that attribution unestimated unless a distinct
supported estimator is specified and reviewed before exposure.
