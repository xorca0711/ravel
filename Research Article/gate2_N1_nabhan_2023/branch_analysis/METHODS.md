# Measurement specification and source roles

The immutable [contract](trials/extension_v1/contract.json) embeds
[config/extension_v1.json](config/extension_v1.json). This analysis was requested
after prior Nb2 results were known, so new freezes preserve an exploratory design
and exposure history; they do not create untouched validation data.

| Input | Role and unit | Limitation |
|---|---|---|
| GSE208770, Nb2 bulk_v1 | Existing TMM-voom normalized 18 libraries; 6 source arms | Independent culture/animal preparation and pairing map unverified; source timing unreconciled |
| GSE327565 | Newly downloaded 955,094-byte processed count file, 49,671 input genes, 14 libraries | Source Figure8 reports mice; identities across media unresolved; reuses existing A1 catalog, not its multiome series |
| GSE262927 processed final_clustered.h5ad | Existing raw integer layer; 162,175 cells, 32,228 genes, source sample/state units | 107,626 cells with known author state/condition; predicted doublets removed in primary; day/round/tracing/genotype/sex confounding |
| Nb2 atlas_v1 | Independent previous count extraction and expected detection at500 UMIs | Same underlying mouse study; never additional replication |
| Mouse Hallmark v2024.1 | E2F/G2M list overlap control | Excluding list overlap does not remove all cycling biology |

GSE327565 is distinct from Gaona mouse multiome GSE327686 and human GSE326359.
No paired interpretation is borrowed from replicate suffixes. The mouse bulk
fits are separate genotype comparisons within each medium; filtering keeps genes
with count>=10 in>=3 of all14 libraries, then TMM/voom/limma is fitted separately
within each medium. BH is per contrast across the filtered genes. This is an
adaptation of the source DESeq2 analysis, not an exact reproduction.

Bulk scores are mean mapped-gene log2CPM; a signed reference score subtracts the
down-list mean from the up-list mean. A panel needs>=60% membership and>=2 genes;
each reference direction also needs>=5. Ambiguous duplicate symbols are excluded;
Cyr61/Ctgf aliases are mapped explicitly, and every missing member is recorded.
The reference selection is fixed using Gaona only, before Nb2 projection. Its
training-set separation is selection-conditioned, not validation. Medium comparison
is internal sensitivity, with possible overlapping source animals.

Bulk intervals use Welch variance across libraries, **conditional on independence**,
with no multiplicity correction; they are descriptive diagnostics, not a family
of confirmatory discoveries. All182 program contrasts are retained. Six
single-library and nine leave-one-per-arm omissions in each Nb2 3v3 comparison
reuse normalization: they assess score influence, not refitted whole-pipeline
uncertainty. Genes are not the replicate unit. No point estimate or omission
range is an equivalence test, and no omnibus interaction is inferred from
separate significance statements.

Atlas counts are summed within source sample/state. CPM uses every gene actually
present in the raw layer; scores use mean log2(CPM+1), so their scale differs from
bulk log2CPM. All comparisons stay within their study/measurement. Floors20/50/100
and retained-doublet sensitivity are separate views of the same samples. Cohort
patterns require>=3 source units; prespecified day42 within-state Spearman summaries
require>=5. There are30 primary associations (180 including all sensitivity views),
with no population p-values. No exposure-response model, pseudotime fate claim,
integration or inferred cell lineage is fitted.

CAP1/CAP2 crosswalks use Aplnr/Gpihbp1/Kit and Car4/Ednrb/Apln, consistent with
[Niethamer's source framework](../../../docs/scRNAseq_workflow_Niethamer2025.md) and
[Gillich et al.](https://www.nature.com/articles/s41586-020-2822-7). General-capillary
lineage behavior in the latter does not transfer as an observed fate for every
cell in this atlas. CAP1 injury substates are not resolved by these coarse labels.

The small epithelial, stress, ligand, ECM and junction panels are **analyst-defined
descriptive panels**, chosen before new outputs, not validated classifiers.
Membership is explicit in the config. The AT1 panel is not A8's mature-outcome
instrument; the transition panel cannot distinguish successful versus persistent
transition. Support-ligand RNA is not niche support measured by epithelial output;
ECM RNA is not deposited collagen; junction RNA is not vascular permeability.

“Hippo activation” is not used as a synonym for YAP/TAZ output: active MST/LATS
kinases restrain YAP/TAZ. [Park et al.](https://pubmed.ncbi.nlm.nih.gov/26276632/)
provides an alternative-Wnt signaling precedent, while
[Gaona et al.](https://insight.jci.org/articles/view/198113) supplies the tested
Stk3/4-loss context. Neither supplies a Fzd-specific mechanism in these cultures.

The [targeted audit contract](trials/extension_v1/targeted_audit_contract.json)
was written **after** seeing CAP1's positive correlation. Its round/depth checks
are labeled post hoc and include both favorable and unfavorable outcomes.
