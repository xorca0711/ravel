# Zh26-P01: literature context

Review date: **10 November 2026 (Asia/Seoul)**.
Repository base `1a6769fc3d808ccf6b27aed3ecedc71341026f33`.
Purpose: source reproduction and contextual interpretation of Zhang 2026.
This bounded update reuses the [7 November DuPage review](../gate3_09_dupage_2015/LITERATURE_CONTEXT.md);
it does not certify novelty or laboratory readiness.

## Published starting point

| Primary source / version | Exact locator and access | Role in this comparison |
|---|---|---|
| [Zhang 2026](https://doi.org/10.1126/sciimmunol.adx4411), final article, 10 April | Supplied PDF; Figures 3–7 and RNA/data-availability methods; Figures 4–7 visually inspected | The local cDC2/CD4/IL-2-associated NK mechanism is already published. Its RNA reproducibility is the present measurement question. |
| [Gasteiger et al., JEM 2013](https://doi.org/10.1084/jem.20122462) | Saved primary PMC XML re-read, especially Figure 1, Figures 3–4 and 5–6; live PMC route challenged | Treg limitation of CD4/IL-2 help and missing-self recognition predates Zhang. Its splenic/systemic setting differs from local tumor control; response to activating ligands was not uniformly increased. |
| [Wang et al., Cell Reports 2018](https://doi.org/10.1016/j.celrep.2018.05.050) | Primary abstract and indexed Results, including Figures 2D/E; full supplementary audit not performed | Tumor Treg functional reprogramming provides a related, distinct comparison to removal. GSE114298 is a source lead, not a matched NK replication cohort. |
| [DuPage 2015](https://doi.org/10.1016/j.immuni.2015.01.007) and [Peeters 2024](https://doi.org/10.1016/j.celrep.2024.114724) | Reused qualified repository review: DuPage Figure 6 and Peeters Figures 6H/7/S7F–I; see linked review for access limits | Identity regulation and context-dependent gain/loss comparisons inform the neighboring-paper discussion. Peeters S7H already reports a reciprocal comparison. |
| [Sharma et al., Clinical Cancer Research 2019; online 2018](https://pubmed.ncbi.nlm.nih.gov/30054281/) | Primary abstract Results; indexed methods; live PMC full-text route challenged | Their human tumor samples did not show depletion of total FOXP3-positive cells following the studied CTLA-4 therapies. This restricts mouse-to-human generalization, not all future subsets or regimens. |
| [Tselikas et al., Nature 2026; online 29 April](https://doi.org/10.1038/s41586-026-10341-w) | [PMC Results and legends](https://pmc.ncbi.nlm.nih.gov/articles/PMC13323097/), Figure 5e–i and Extended Data 7d–g; no raw reanalysis | Activated CD4/CD25/CD39 subset proportions decreased in patients with durable benefit while total-Treg readouts behaved differently. This qualifies a blanket “human depletion never occurs” account. It is observational mechanistic context within a clinical study, not replication of Zhang's NK-dependent circuit. |
| [Jiang et al., 2025; online 4 September](https://pubmed.ncbi.nlm.nih.gov/40914375/) | Primary abstract Results only; full figures not inspected | In another mouse treatment context, NK depletion improved the combination response and CD8 involvement differed. This is a boundary lead against universally beneficial NK activation, not a refutation of Zhang. |
| [Pedde et al., 2024](https://pubmed.ncbi.nlm.nih.gov/39541209/) | Primary indexed abstract only; live PubMed body unavailable | A tumor-derived PGE2-associated NK dysfunction route supplies a contextual alternative. The lung-metastatic setting is not an exact intervention match; no panel-level claim is made. |

The final Zhang article and its preprint are one source lineage. Published
source-code replay and sensitivity calculations also remain one data lineage.
No paper count is treated as a count of independent replications.

## Repository observation

[SOURCE_REVIEW.md](SOURCE_REVIEW.md) records disagreement among the published
RNA methods, older GEO description and executable code. The subsequent
[released-code reproduction and sensitivities](RESULTS.md) reconstruct all
three RNA tables, preserve fixed-panel directions under block omission, and
identify ranking-sensitive IFN-gamma enrichment. Zhang et al. Figure 3 already
reports the corresponding transcript pattern; Figures 6–7 supply separate
functional/signaling premises. This is shared-source reproduction, not a new
mechanism or independent support. The comparison has not changed, so the
completed literature search below was not rerun. Existing [DuPage results](../gate3_09_dupage_2015/RESULTS.md)
and [candidate follow-up](../gate3_09_dupage_2015/CANDIDATE_ANALYSIS_RESULT_V1.md)
retain mixed context dependence and unit limits; they are not Zhang predictions.

## What this question could add

A transparent, version-specific reconstruction can establish which released
measurements are reproducible and which depend on input/model/ranking choices.
That is a useful reproduction and measurement-validation contribution.
A new mechanism, target, independent replication or functional extension is
not presently claimed.

## Current hypothesis and rival

For this reproduction task, the estimands are the source-model contrasts in
sorted NK transcript abundance: ITDT minus PBS and ITDT+aCD4 minus ITDT.
The model/tissue is the paper's mouse tumor context, RNA timing is day 6,
and the unit is a pooled sorted preparation within a reported experimental day.
Exact pool membership remains unknown.

The chief validity threats are mismatched sample identities, unqualified matrix
semantics, source-version mismatch and unstable block estimates. NK-state mixture
and selection remain biological explanations for bulk RNA patterns; this dataset
cannot separate them from within-state change.

## What the comparison would teach

Agreement supports reconstruction of the published RNA evidence. Numerical
disagreement points to an unresolved pipeline/version issue. Method-sensitive
directions restrict transcript-level claims. Weak or mixed results are retained.
An unqualified count source leaves count-based inference unestimated while a
qualified TPM replay may still proceed. None of these dispositions establishes
cytokine flux, cellular fate, killing or clinical benefit.

## Hypothesis schematic

The [README](README.md#literature-context-and-visual-argument) contains a
qualitative Mermaid map of the published premise, measurement comparison,
validity threat and decisions. This article-local candidate has no canonical
question-guide image; no new measured figure is claimed.

## Next literature check

Actual service: live web search plus primary-page opens, 10 November 2026.
Recent coverage used 2024–2026 year terms alongside unrestricted older searches;
no hard publication-date filter or systematic citation export was used.
Queries included:

- `"Intratumoral T reg cell ablation elicits" Zhang 2026`
- `"regulatory T cells" "NK" "IL-2" tumor 2024 2025 2026`
- `"Anti-CTLA-4 immunotherapy does not deplete" human cancers`
- `"Gasteiger" "2013" "IL-2-dependent" natural killer regulatory`
- `"Safety and efficacy of intratumoural anti-CTLA4" "2026" figure`
- `"Tissue-colonizing disseminated tumor cells" prostaglandin 2024 NK`
- `"Intratumoral" "adx4411" correction erratum`
- `"adx4411" "supplementary" "Zenodo"`
- `"Targeting Ezh2 reprograms intratumoral regulatory T cells" Wang 2018`

Backward references were followed from Zhang to Gasteiger and the supplied
DuPage neighbors; relationship searches supplied recent boundary papers.
The correction query returned no verified correction record in this bounded
pass; this is not complete correction clearance. Publisher and some PMC/PubMed
routes failed; access levels above distinguish saved full text, indexed Results
and abstract-only reads.

Stop this pass at the reproducibility question. Reopen if source reconciliation
changes the estimand or a concrete proposed biological extension needs a closer
precedent. Jiang/Pedde full figures and complete Zhang supplements remain
specific follow-up reading, not completed reads.
