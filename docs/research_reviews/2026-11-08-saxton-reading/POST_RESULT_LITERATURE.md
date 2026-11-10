# Saxton results in the literature through 8 November 2026

8 November 2026, Asia/Seoul. Documentation/source review at local result revision
`16627aa`, against fetched main `4318740`. Author: Codex, at the owner's request.
This dated addendum supplements the [earlier review](LITERATURE_CONTEXT.md).
It does not change frozen outcomes, complete the pending parent technical audit,
register another RQ, or imply human scientific acceptance.

## Published starting point

**Same-day execution addendum:** [three extension plans and completed source work](EXTENSION_EXECUTION.md)
now follow this review. Gorby coverage was extended to indexed primary Results
around Figs. 5–6 (author-manuscript pp. 11–13), RNA methods pp. 24–26 and S7
legend pp. 45–46. Its CD8 RNA comparison used a six-day culture with ligand during
activation/expansion, distinct from Saxton's post-activation 24-hour treatment.
GEO SOFT and twelve per-comparison tables were inspected; a failed common-matrix
qualification and the narrower estimate endpoint are preserved in the new report.
The table below records the earlier reading checkpoint, supplemented here.

GEO E-utilities source searches on 8 November used `gds`, `gse[ETYP]`, retmax 20,
no date filter: IL10/IL18/CD8 synonyms; super-10/10-DE/R5A11/Saxton with IL18;
IL22 with IFNA/priming; and exact 22-B3 terms. Actual translated queries, all
returned records, counts and warnings are bound to the source-screen receipts.
The exact IL10 search dropped an unrecognized R5A11 phrase. All returned summaries
and sample-title lists were read; full SOFT was additionally read for GSE248984,
GSE162791, GSE307526, GSE89610 and GSE214633. Neither interaction qualified.
These are source screens, not a new systematic literature or novelty review.
The earlier recent-primary scan and its full-text access gaps remain applicable.

| Primary source / version | Actual read and exact locator | What is already specified |
|---|---|---|
| [Saxton et al., 2021, IL-10](https://doi.org/10.1126/science.abc8433), supplied final PDF | Reuse completed Results/Figs. 3–5 and CD8/RNA-methods reading; Fig. 5 visually inspected. | Weaker 10-DE and heterogeneous super-10 transcription were already reported in Fig. 5. The repository checks the same source data; it does not discover these patterns or independently validate the paper. |
| [Gorby et al., 2020](https://doi.org/10.1126/scisignal.abc0653), peer-reviewed author manuscript | [Institutional PDF](https://discovery.dundee.ac.uk/ws/files/51987933/REF_Gorby_et_al_Text.pdf), Results around Figs. 3–4; cell-culture and RNA methods; S1/S2 descriptions p. 47. Text read, not a complete Fig. 5–6/data audit. | Affinity/stoichiometry and dose-dependent IL-10 responses were studied before Saxton. GSE146438 supplies monocyte and CD8 comparisons; R5A11 is not super-10. Author-selected supplements filter on WT response, so they are not an unbiased target universe. |
| [Freeman et al., 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3382521/) and [2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4054413/) | Indexed primary 2012 Results/Fig. 1 legend: LCMV-experienced mouse CD8 cells, 6-hour cytokine challenge. 2014 Abstract/Introduction only. Direct PMC opens returned challenges. | The 2012 experiment already shows IL-10/IL-18 coactivation; the 2014 study reports inhibition of other cytokine-driven IFNγ responses and resistance of peptide-driven responses. Partner dependence is a published premise, not an IL18RAP discovery here. Different species/activation histories limit transfer. |
| [Saxton et al., 2021, IL-22](https://doi.org/10.1016/j.immuni.2021.03.008), final PDF | Reuse visually inspected Figs. 3–7 and relevant Results/methods. | STAT recruitment and tissue-dependent 22-B3 activity are already established. The six-hour bulk-colon description cannot localize the response or measure repair. |
| [Bachmann et al., 2013](https://pubmed.ncbi.nlm.nih.gov/23153456/), online 12 November 2012 | Primary PubMed abstract re-read; full figure/method access remains unresolved. | IFNα priming changes IL-22-associated STAT1/target responses in epithelial models. A generic claim that priming changes IL-22 signaling is already covered; the B3-versus-WT boundary requires a more exact comparison. |
| [Cineus, Luo et al., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12133592/), version of record 30 May | Reused Figs. 3–4 and prior S5e audit; re-read Fig. 6d–f and adjacent Results. | Epithelial IL-22/STAT3-dependent OSMR induction and inflammatory OSM signaling are published mechanisms. Sorted epithelial Osmr-deficient versus control colitis RNA is distinct from healthy B3-treated bulk colon. Withdrawal evidence does not establish autonomous persistence. |
| [Expòsit et al., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12632830/), bioRxiv v1, 13 October | Reused Fig. 3C–G Results/legends; current PubMed/PMC still label the accessed work a preprint. No later article established by this search. | Geometry-based IL-10 decoupling and type-III-interferon agonists are already reported in this preprint. "IFN-λ is an untested extension" is too broad. This does not settle every affinity-detuning proposal. |
| [Engineered TYK2 dependence…, 2026](https://www.nature.com/articles/s41586-026-11176-1), Nature, version of record 14 October | Indexed primary Figs. 1, 2, 4 and receptor-copy/CRISPR/phosphoflow methods read. Direct publisher open redirects; figures/supplement/data access not fully audited. | Receptor geometry, kinase dependence and receptor abundance already support engineered myeloid selectivity. Both receptor subunits matter in the reported manipulations. These findings do not retroactively identify the mechanism of Saxton's muteins. |
| [Martí-Baena et al., 2026](https://doi.org/10.64898/2026.06.02.729479), preprint lead | Manuscript v1 still HTTP 403. Primary author code/README inspected at commit `f7daaa8c0b067c775878868fe836240722626856` (2 September). Exact locators below. | Public code explicitly analyzes GSE160332 and gene-specific STAT thresholds. Reusing it is not independent validation. This closes the earlier uncertainty about dataset reuse, not the full manuscript/methods review. |

## Repository observation

The [IL-10 result](../../../Research%20Article/gate3_07_saxton_2021_il10/RESULTS.md)
reports super-10 above WT for IFNG/IL18RAP and below WT for GZMB/IL22/SOCS3
through all prespecified scale/omission cases. 10-DE is broadly closer to PBS;
CCL1's super-10 contrast is unstable. These were exposed, published targets.
Two libraries per group have unresolved donor/preparation joins. There is no
matched signaling/secretion experiment or causal STAT estimate in this deposit.

The [IL-22 Osmr result](../../../Research%20Article/gate3_08_saxton_2021_il22/osmr_v1/RESULTS.md)
is consistently lower under B3 than WT; B3–PBS is small and sensitive. It does
not supply positive evidence for retained Osmr induction in this acute setting.
The earlier [panel reassessment](../../../Research%20Article/gate3_08_saxton_2021_il22/reassessment_v1/RESULTS.md)
also retained overall attenuation and panel sensitivity. These negatives remain.

Thus the appropriate attribution is **"the mixed IL-10 pattern was already
reported by Saxton et al. (2021), Fig. 5, using these data"**, not "a new
mechanism was discovered." The OSMR literature supplies a relevant comparison,
not an explanation demonstrated in the B3 samples.

## What this question could add

The [development dossier](RQ_DEVELOPMENT.md) separates a distinct-study
transportability screen, an IL-10 co-input boundary, and an IL-22 priming boundary.
Their contribution would be measurement validation or a specified context test.
Generic decoupling, receptor-density explanations, IL-22→OSMR and gene-threshold
modeling are already represented in the inspected literature.

## Current hypothesis and rival

Organizing question: **under which recipient/exposure conditions does engineered
cytokine selectivity persist for a specified output?** It is not an adopted global
hypothesis. Amplitude, timing, cell mixture, survival and partner inputs can all
contribute. The dossier supplies separate comparison tuples; the existing data
cannot decide between these explanations. Source reuse is a major validity threat.

## What the comparison would teach

Agreement in a distinct study could support transport of a descriptive pattern;
failure would narrow its ligand/dose/state boundary. Only matched protein and
functional measurements could connect transcription to response. Neither an
unqualified external source nor repeated analysis of GSE160332 resolves this.

## Hypothesis schematic

See the qualitative [dossier diagram](RQ_DEVELOPMENT.md#qualitative-decision-map).
It marks proposed comparisons and missing measurements, not measured arrows.
Article-local discussion only; no registered scientific illustration is replaced.

## Technical section: resolved modeling-source overlap

The author's [README](https://github.com/Quim98/IL10_model_publication/blob/f7daaa8c0b067c775878868fe836240722626856/README.md)
names baseline, receptor-memory and proofreading alternatives and maps downstream
analysis to Fig. 4/EV4. In [Plots_genome_regulation.ipynb](https://github.com/Quim98/IL10_model_publication/blob/f7daaa8c0b067c775878868fe836240722626856/Plots_genome_regulation.ipynb),
zero-based cells 42/45 name/load GSE160332; 46 uses a condition-only DE design;
60/62/67 use Gorby monocyte data, including GSE146438. Notebook blob:
`ee23ef0764d980074042e417868bc2d7f20e0d66`.
No code was executed. The README's current Zenodo DOI is
[10.5281/zenodo.22257307](https://doi.org/10.5281/zenodo.22257307), replacing an
older discovery-index link; both direct record opens failed here. No payload
qualification, donor recovery or model-validation judgment follows from this read.

## Next literature check

Actual service: web search/open/find plus GitHub connector reads, 8 November
2026. Unrestricted foundational/title queries and a stated 2024–2026 recent
window were used; no PI restriction. Representative actual queries:

- `"Engineered TYK2 dependence enables myeloid-selective IL-10 receptor agonism"`
- `"Mechanistic pathway modeling reveals how IL-10 generates pleiotropic immune responses"`
- `"Mechanistic pathway modeling" IL-10 zenodo github`
- `"10.64898/2026.06.02.729479" published version`
- `IL-10 IL18RAP IL-18 CD8 T cells interferon gamma STAT1 Saxton`
- `"IL-10" "IL-18" "Regulation of innate CD8" Freeman 2012`
- `"IL-10" "R5A11D" monocyte`
- `"Bachmann" "IL-22" "2013" IFN alpha`
- `IL-22 partial agonist B3 priming interferon 2024 2025 2026`
- `"IL-22" "partial agonist" "priming"`
- `"Geometric Tuning of Cytokine Receptor Association Modulates Synthetic Agonist Signaling" 2026`
- Exact title searches with `correction retraction` for Bachmann, Cineus/Luo and
  the TYK2 study; no linked notice found in returned primary records. This is
  bounded notice checking, not clearance.

Followed backward source links from the modeling notebook to Gorby, and from
Saxton/prior local context to priming/OSMR studies. Keyword searches supplied
later studies; no systematic forward-citation graph or exhaustive search was run.
Earlier Saxton Crossref checks and IL-22 withdrawal/source audit are reused at
their recorded coverage. Search summaries and reviews were discovery aids only.

Stop here for choosing a research direction. Reopen before a numerical/experimental
contract to inspect the complete closest paper, qualify the specific units and
inputs, and refresh versions. Bachmann full methods, Freeman 2014 full Results,
the modeling manuscript, and the TYK2 source dataset remain specific access/read
gaps. Newly surfaced IL-10/IL-18 hyperinflammation and bystander-regulation papers
are uninspected leads, not evidence supporting a new mechanistic claim.
