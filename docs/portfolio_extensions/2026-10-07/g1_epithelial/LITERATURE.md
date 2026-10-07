# G1 targeted literature refresh

Search date: **7 October 2026**. This refresh concerns the two new bounded
comparisons below. The unchanged premises for all twelve RQs retain their
registry-linked 3 October context notes. This is not a systematic review or
novelty clearance. The numerical outputs remain exposed exploratory work.

## Search and access record

Service: live web search and primary-publisher/PMC/arXiv opens. No date filter;
recent coverage explicitly sought 2024–2026 alongside older closest precedents.
Queries executed verbatim:

- `epithelial high plasticity cell state regeneration lung cancer lineage 2025 2026 Chan s41586-025-09985-x`
- `lung cancer regenerative epithelial plasticity stress signature nonmalignant injury Marjanovic 2020 HPCS`
- `England 2025 sustained NF-kB mutant alveolar stem cells clone two population model`
- `Gunnarsson Foo Leder 2023 identifiability birth death switching cell state 111497`

Primary indexed text of Chan 2026 supplied Results and Fig. 2/5 and Extended
Data 5/6 locators. Direct Nature open subsequently hit its authentication
redirect. PMC Marjanovic full-text open hit a browser check; indexed primary
text and PubMed abstract were accessible. England PubMed was opened; the
repository's earlier source/code audit supplies the detailed model provenance.
Gunnarsson arXiv abstract was accessible; the attempted v2 HTML returned 404.
Wu 2024 PLOS full text was accessible, including Methods, Linear birth-death
process, End-point experiments and Live-cell imaging techniques. Figure images,
new supplementary files and full forward/backward citation searches were not
inspected. Related-paper discovery found Li 2025 organoid modelling; it is an
unread lead, not supporting evidence. No correction notice appeared on the
accessible source pages; inaccessible publisher records were not independently
cleared for corrections/retractions.

## A11: published finding to fit-for-purpose comparison

| Primary source / version | Exact inspected locator and finding | Consequence |
|---|---|---|
| [Marjanovic et al., Cancer Cell 2020](https://pubmed.ncbi.nlm.nih.gov/32707077/), DOI 10.1016/j.ccell.2020.06.012 | Primary abstract and indexed Results, HPCS/cluster 5; high plasticity, growth and treatment-resistance associations | HPCS biology is an established premise. A set subtraction does not identify a new cell state. |
| [Chan et al., Nature 2026](https://doi.org/10.1038/s41586-025-09985-x), version of record 21 January 2026, issue 5 March 2026 | Indexed Results and Fig. 2 lineage tracing, Extended Data 5/6; Fig. 5c–d regeneration contexts | Direct functional plasticity evidence and regeneration overlap already exist. This is close prior work and counterevidence to equating an HPCS-related RNA score with malignancy. |

Repository observation: the fixed lesion-associated module rose in eight
paired Kim patients; the original beyond-shared criterion remained unresolved
(BH q=0.0547). The separate three-donor injury assay did not establish
specificity. Exact authority:
`RQ_Specified/A5_A11_shared_component_contract/reports/REVISED_TEST_RESULTS.md`
and `RQ_Specified/A11_lesion_programme_addition/reports/ACUTE_INJURY_RESULTS.md`.

Remaining question: does the frozen residual add **paired tissue-discrimination
information** beyond the fixed shared-remodelling and three stress modules?
The existing signed-rank contrast is not this conditional predictive test;
the original `PLAN.md` explicitly excludes incremental prediction from its
interpretation. Eight patients, each with normal-AT2 and author-labelled tumour
epithelium, are the units. We retain the exact selected cells and gene lists,
reconstruct pseudobulks and use per-library full-count log2(CPM+1). This changes
the measurement scale transparently to avoid reusing all-patient TMM in a
nominally held-out pipeline. Training-only feature scaling and conditional
logistic coefficients are learned in seven patients; the eighth pair supplies
log loss. A fixed penalty avoids tuning on eight patients. A stress-excluded
residual and two additional fixed penalties are sensitivity analyses.

Feature-discovery audit: the original A11 README and shared contract record
the 23 GSE308103 patients as discovery, with the Kim/GSE131907 eight-patient
test scored subsequently. Source module membership and its frozen human
mapping are reused unchanged. This run does not discover features in its folds,
and cannot validate the entire historical feature-discovery procedure. More
importantly, the Kim outcomes and previous test results have already been
inspected before choosing this model comparison. Patient holdouts therefore
estimate conditional internal reuse performance, not untouched confirmation.

An improvement supports internal measurement utility in these paired
populations; no improvement limits the proposed residual. Both outcomes are
informative. Unknown malignant identity, changed epithelial composition,
previous outcome exposure and the absence of matched non-neoplastic injury
prevent diagnostic, causal, prospective-fate or cancer-specific interpretation.
Contribution: **measurement qualification of existing A11**, not a new RQ.

### Prospective amendment after the first predictive result

The executed first comparison improved paired log loss, while both baseline
and augmented models already ordered every pair correctly. Before interpreting
this as additional information, a concrete modelling alternative needs testing:
duplicating a baseline feature leaves the linear predictor space unchanged but
lets ridge regression distribute one coefficient over two penalized columns.
For a fixed combined coefficient, equal splitting halves that coordinate's
penalty. A gain can therefore arise from regularization geometry alone.

A separately exposed amendment duplicates each of the four fixed baseline
features one at a time under all three already declared penalties and folds.
It uses the saved per-library scores, introduces no gene, changes no population,
and reports all controls without tuning. Comparable gains from an unchanged
predictor space would limit the biological-information reading; better residual
performance than those controls would still only support the bounded internal
measurement comparison. This mathematical control is not a new RQ, new
biological hypothesis or literature-novelty claim. Its script and synthetic
penalty-equivalence test are frozen separately before those controls are run.

## A17: published finding to fit-for-purpose comparison

| Primary source / version | Exact inspected locator and finding | Consequence |
|---|---|---|
| [England et al., Cell Stem Cell 2025](https://pubmed.ncbi.nlm.nih.gov/39978341/), 6 March 2025 | Primary abstract; repository full-source audit of Fig. 1–2, model source `sim_two_pop_model.m`, mutant RFP block lines 53–65 | The paper motivates founder heterogeneity. The saved source parameters and published-curve provenance remain distinct; a code defect does not refute the biology. |
| [Gunnarsson, Foo and Leder 2023](https://arxiv.org/abs/2306.08096), arXiv abstract, DOI 10.1016/j.jtbi.2023.111497 | Abstract: different information in phenotype fractions and cell counts | Model identifiability depends on observation type. Results from sorted cultures cannot be imported into truncated, cross-sectional total-clone sizes. |
| [Wu et al., PLOS Computational Biology 2024](https://doi.org/10.1371/journal.pcbi.1011888), published 6 March 2024 | Methods, Linear birth-death process and endpoint versus live-cell likelihoods, equations 4–12; Fig. 1 caption | Growth, loss, sampling and longitudinal correlation require explicit models. These cell-count experiments do not validate A17's unobserved founder/detection denominator. |

Repository observation: source accounting retains 11 source-indexed mutant
mice at weeks 1/2/4, but only size>=2 clones enter the primary comparison.
The validated stochastic kernel has not established a fitted biological
observation model. Exact authority:
`docs/roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md`, its
`mutant_parameter_trace.json`, and
`docs/research_dossiers/continuation_2026-10-03/A17_MODEL_SPEC.md`.

Remaining question: under the **source-script parameters**, how different are
the starting fast fraction, its share of retained clones and its share of
living/retained cells? Exact no-switching birth-death laws permit this without
fitting the cohort or inventing a molecular identity. The primary parameters
are 0.08 fast founders, renewal 0.7, early net rates 3.1/0.9 per week, later
0.5/0.01 after week 2. We keep alternative 0.16 founder and 1.1 early slow-rate
transcriptions as named sensitivities, never as a selectable reproduction.
Size floors 1/2/5 characterize observation selection; floor 2 is primary.

Large separations between those fractions make ascertainment a concrete
interpretation issue. Similarity would narrow this particular concern.
Neither result chooses founder versus switching biology. Independent backward
probability-generating-function coefficient ODEs verify probabilities and
truncated first moments; this is arithmetic verification, not replication.
Contribution: **A17 observation-model qualification**, not a new growth theory,
new RQ, cohort fit or claim about actual extinction.
