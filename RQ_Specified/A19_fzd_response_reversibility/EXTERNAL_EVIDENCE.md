# A19 external evidence and implications for the extension

**Primary-source review, 30 September 2026.** This bounded web review informs
[the extension pipeline](EXTENSION_PIPELINE.md); it is not a systematic review,
a new numerical analysis or an upgrade of H1–H3. Published results, our inference
and dataset eligibility are separated below. The original paper and already
analyzed human-organoid study are labelled reused evidence.

## What the literature changes

External results support the plausibility of competing epithelial fates and
show that ending a growth-maintenance input can be insufficient without a
permissive differentiation environment. They also constrain the proposed scope:
an airway-associated state must not be presumed irreversible, and a reduction
in SFTPC must not be called successful AT1 maturation. This is our synthesis
of the studies below, not an effect estimated across their incompatible models.

The focused A19 hypothesis should therefore ask whether **pre-withdrawal lineage
state modifies the probability of productive maturation under a specified
maturation environment and input**, while retaining absolute mature output and
AT2 reserve as functional criteria. State acquisition, missing maturation cues,
selection and receptor/input context are competing explanations. New mediator
screens are not necessary to distinguish these possibilities at the first stage.

## Evidence map

| Reference and inspected evidence | Published result relevant to A19 | What it supports or challenges | Boundary and pipeline role |
|---|---|---|---|
| **Kathiriya et al., 2022**, [Nature Cell Biology](https://www.nature.com/articles/s41556-021-00809-4); Results, Figs. 2 and 6, data availability | Purified human AT2 cultures yield alveolar–basal intermediates and basal progeny in a mesenchymal context; graft-origin labelling supports conversion capacity in injured mouse hosts | Supports a biological competing-fate route, beyond disagreement between marker scores | Not endogenous human genetic lineage tracing or a Fzd withdrawal experiment. Reference states/time course for P1; source/output linkage audit for P3. Already reviewed in [A1's lineage audit](../A1_transitional_epithelial_state_distinction/LINEAGE_AUDIT.md) |
| **Burgess et al., 2024**, [Cell Stem Cell](https://pmc.ncbi.nlm.nih.gov/articles/PMC11147407/); Results, Figs. 5–7 and Supplementary Fig. 3 | In human iPSC-derived alveolar cells, removing CHIR/KGF alone produces little AGER reporter induction; a LATS-inhibition context promotes AT1-like identity. The study separately demonstrates epithelial barrier capacity and cue-dependent reversibility | Strong constraint on “withdrawal alone is sufficient”; provides an independently measured functional benchmark and warns against treating induced identity as permanently fixed | Combined input changes and iPSC context; no intermittent Fzd regimen with preserved reserve. P3 maturation reference; not proof that A19 is mediated by YAP |
| **Li et al., 2024**, [American Journal of Physiology](https://journals.physiology.org/doi/full/10.1152/ajplung.00191.2023); Results/Discussion and data statement | Human AT2 spheroids and distal-lung organoids acquire AT1-associated molecular/morphological features under coordinated BMP, Wnt, TGF-beta and growth-factor changes | Supports environmental control of differentiation; challenges attributing a multi-factor medium effect to one receptor or input | Not a traced schedule-plus-reserve test. P3 co-intervention inventory; public supplements do not establish recovery of all unit-level outcomes |
| **Rational engineering of lung alveolar epithelium, 2023**, [npj Regenerative Medicine](https://www.nature.com/articles/s41536-023-00295-2); Figs. 6–7, cached full text | CHIR/KGF removal gives a modest AEC1 response in engineered rat tissue; adding cyclic strain strengthens differentiation-associated output | Adds a mechanical-context explanation for incomplete differentiation after withdrawal | Reused study, with Fig. 7 newly considered here. Combined intervention and species differences remain; individual Fig. 6/7 values were not recovered. P3 source candidate, not a new replication |
| **Patel et al., 2024**, [Respiratory Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985870/); article results | A broad FZD-binding WNT mimetic expands alveolar organoids and improves lung function while reducing fibrosis in a mouse injury model | Shows that receptor-directed stimulation can accompany a functional tissue benefit | Whole-lung, multi-cell effects do not identify lineage-derived AT1 output, a verified off-period or later AT2 reserve. Functional context for H1/H3; no direct schedule test |
| **Lin et al., 2026**, [Advanced Science](https://pmc.ncbi.nlm.nih.gov/articles/PMC13334660/); Results, Figs. 5 and 7, data statement | Human organoid progenitors generate pathological basal states; CHIR and NRG1–ERBB4 perturbations constrain basal conversion and preserve source identity | Supports modifiable lineage stability and an alternative explanation for CHIR-associated identity effects | Prevention of conversion is not reversal of an established state or proof of AT1 maturation. Some reference transcriptomes reuse Kathiriya data. Context for P1/P2; new ERBB4 mediation is deferred |
| **Nabhan et al., 2023**, [Cell](https://pubmed.ncbi.nlm.nih.gov/37321220/); parent-paper results | Fzd5 and Fzd6 agonists stimulate alveolar stem-cell activity, while the Fzd6 agonist additionally promotes alveolar fate in airway-derived progenitors | Constrains any universal claim that airway origin permanently excludes alveolar fate; motivates input-dependent plasticity | Parent evidence already exposed. It does not show reversal of every established basal state or settle the intermittent-dosing question |
| **Hoffmann et al., 2022**, [Communications Biology](https://pmc.ncbi.nlm.nih.gov/articles/PMC9409623/); existing A19 source analysis | Alveolar-derived organoids show context-dependent identity; airway-derived cultures show transient SFTPC induction | Motivates the cellular-state question and supplies the immediate P1 controls | Same study as exploratory_v1. Reanalysis and a new figure are not independent biological replication |

## Public data triage

These are candidates for specified roles, not newly executed datasets. Publication
of a functional result does not guarantee that the RNA and functional endpoint
can be joined in the same independent units.

| Resource | Confirmed source description | Appropriate next use and limitation |
|---|---|---|
| [GSE197949](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE197949) | Existing A19 source; control organoids with candidate AO15/AO16/AO22 origin matches | Primary P1 eligibility audit; resolve actual donor/preparation identity and origin/medium confounding |
| [GSE150068](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE150068) | GEO series describes human AT2/mesenchyme organoid sampling at days 7, 14 and 21, with freshly sorted cells among the samples | Candidate external reference for the basal route. Six samples do not mean six paired donors; timepoint-to-donor continuity needs audit. If used to define states, it is not an independent validation of those definitions |
| [GSE246243](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE246243) | One named iPSC line; baseline and 24/48/72-hour sampling after a combined medium change; four GEO samples | Candidate AT1 differentiation reference. Four time points are not four donors; no isolated Fzd withdrawal or demonstrated link of every sequenced unit to function/reserve |
| [GSE221343](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE221343) | Three source conditions in one named iPSC clone: AT2 medium, an AT1 differentiation medium and nuclear-YAP context | Optional input-context reference. GEO explicitly records a **20 May 2024 correction of two sample titles and processed-file names**; use the corrected identity mapping. No population-level replication implied |
| [GSE178405](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178405) | Engineered-lung transcriptomic deposition | Do not assume it contains the individual withdrawal/strain outcomes from Figs. 6–7; that linkage remains unverified |
| [Li supplementary tables](https://zenodo.org/records/10023167) and [figures](https://zenodo.org/records/10023177) | Public supplemental material; source states other data are available on reasonable request | Audit endpoint/unit metadata first. No author outreach or assumed availability of raw paired functional values |
| Lin 2026: HRA009633, reported at [GSA-Human](https://ngdc.cncb.ac.cn/gsa-human) | New sequencing accession named in the paper; it also reuses GSE150068/GSE150247 and selected SRA records | Secondary candidate. Access terms, subject mapping and usable counts remain unaudited; do not count reused references as new replication |

## Changes incorporated into the pipeline

1. Keep P1 focused on cellular organization and competing identities. Add an
   optional external state-reference comparison only after primary source
   identity/coverage is established; do not merge adult, fetal/iPSC and rodent
   systems into a common causal contrast.
2. Keep P2 bounded to existing GSK3B-by-CHIR effects. Record whether apparent
   differentiation/growth separation survives gene-level inspection, while
   acknowledging that differently scaled RNA panels cannot establish selective
   biological action. Neither EGF/FOXM1 expression nor the ERBB4 literature
   identifies the mediator of the existing A19 response.
3. Expand P3 metadata to include maturation-promoting co-interventions, mechanics,
   developmental model and the timing of state measurement. A missing cue is a
   rival to intrinsic fate restriction. Record withdrawal-only and combined-cue
   comparisons separately when genuinely available.
4. Preserve H1's reserve requirement and distinguish a clinical/tissue-function
   improvement from traced epithelial mature output. No inspected study joins
   the complete Fzd schedule, state, functional descendant yield and later
   reserve question in the required units. This is an inventory finding about
   these inspected records, not a universal claim that such evidence does not exist.

## Search and provenance

Searches on 30 September 2026 covered human alveolar-to-basal conversion,
Wnt/Fzd withdrawal and AT1 differentiation, receptor agonists with functional
outcomes, and public datasets cited by those primary studies. Current 2026
results were included. Publisher articles, PubMed/PMC and source GEO/Zenodo
records supply the evidence; reviews, vendor pages, ResearchGate and search
aggregators were not used as evidentiary authorities. A surfaced Burgess
preprint was superseded by the 2024 peer-reviewed article for this review.

[external_evidence_intake.json](metadata/external_evidence_intake.json) records
retrieved XML/SOFT URLs and SHA256 hashes and preserves failed XML attempts.
Kathiriya and Li full-text XML requests returned HTTP 500; the publisher/PMC
indexed article sections and source data statements were readable through web
search. Some direct browser requests encountered recaptcha/redirect failures;
these do not imply missing studies. Cached payloads remain ignored; this report
and [structured reference map](metadata/external_reference_map.json) are deposited.

All conclusions in the evidence map are reported findings or explicitly bounded
inferences. No new effect size, meta-analysis, biological acceptance or claim
grade has been generated by this reference review.
