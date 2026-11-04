# A12: literature context and current argument

[Question home](README.md) · [Scientific dossier](../../docs/research_dossiers/A12.md).

Synthesis updated 4 November 2026 using the recorded source reviews and current
results. No fresh literature search or biological calculation was performed for
this documentation batch. Published premises and reused-data observations remain
separate evidence types.

## Published starting point

IL-1-dependent epithelial transitions and fibroblast exposure effects already show that responding compartments matter.

| Primary source | Inspected locator and access record |
|---|---|
| [Choi 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7487779/) | Fig. 7 and Discussion. [Access / prior review](../../docs/research_dossiers/NOVELTY_SPECIFICITY_APPLICATION_2026-10-03.md) |
| [Ciminieri 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC12042164/) | Fig. 1 and Results; fibroblast pre-exposure and organoid growth. [Access / prior review](../../docs/research_dossiers/NOVELTY_SPECIFICITY_APPLICATION_2026-10-03.md) |

Sources above reuse the named review unless the update ledger explicitly records a fresh inspection. Published-source evidence and reanalysis of the same material are not independent replication.

The [3 November ERBB source record](../../RQ_Specified/A12_recipient_context/reports/ERBB_SORTED_SPEC_V1.md)
and [Lin read](../../RQ_Specified/A12_recipient_context/reports/LIN_REFERENCE_READ_V1.md)
are adjacent receptor/identity context, not a new IL-1 validation lineage.
The close Gomez/Koyama 2026 report (DOI
[10.1093/ajrccm/aamaf106](https://doi.org/10.1093/ajrccm/aamaf106), Fig. 2A and
supplementary Figs. 2/3) cautions that HTII-280 sorting need not yield homogeneous
AT2 cells; its GSE150068 reanalysis shares the sorted source. The resulting
ERBB4/ERBB2 RNA detection in one preparation is described separately in the
[completed report](../../RQ_Specified/A12_recipient_context/reports/ERBB_SORTED_RESULTS_V1.md).
A usable between-state map and Lin replicate/preparation values remain
unrecovered. None of these observations transfers a functional mechanism into
the current human IL-1 prediction.

## Repository observation

The [original pilot](../../docs/roadmap_runs/2026-09-27-followthrough/A12_PILOT.md)
uses **12 matched patients and 48 patient/histology/recipient units** in GSE308103.
All features and outcomes are LUAD-minus-normal within patient. The outcome is a
gene-disjoint TNF/NFkB inflammatory RNA score, not an IL-1-specific activity assay.
The fixed comparison adds recipient context to the same source/mixture model
already containing TNF; patients are held out from fitting.

| Recipient | Source + TNF RMSE | With recipient index | Interpretation |
|---|---:|---:|---|
| AT2 candidate label | 0.4271 | 0.3244 | Lower prediction error; 7/12 patients improve. |
| Alveolar fibroblast candidate label | 0.2098 | 0.2283 | Worse primary prediction; direction changes in sensitivity analyses. |

Cross-validation training sets overlap, so these are exploratory prediction
results without fold-based significance claims. Healthy-reference labels do not
independently establish malignant identity. The [ten-gene attribution](../../RQ_Specified/A12_recipient_context/reports/IL1_COMPONENTS_V1_RESULTS.md)
reuses the same 12 patients: 24 patient/recipient paired contrasts, not new donors.
In epithelium, IL1RAP increases while IL1R1 decreases; lower IL1R2/SIGIRR contributes
positively to the signed index, while higher IL1RN contributes negatively.
The index is therefore not uniform receptor activation or uniform inhibitor loss.
MYD88/IRAK1/IRAK4 add RNA context, not activation measurements.
**NFKBIA and TNFAIP3 overlap the old response**, so they cannot independently
validate it.

The [A12-S1 source map](../../RQ_Specified/A12_recipient_context/reports/A12_S1_SOURCE_IDENTITY_MAP.md)
reports **median patient-level unassigned fractions of recovered IL1B counts
of roughly 52-72% across histologies** under the recorded assignments. These are
not pooled tissue fractions or secretion measurements. The source term describes
assigned macrophages; it cannot assign all active ligand to macrophages.

## Does the evidence warrant the narrowing?

**Rationale verdict: supported exploratory predictive narrowing, with an
incomplete causal interpretation.** Published recipient-context effects make the
question plausible; the actual support is lower held-out inflammatory-RNA error
in 12 epithelial patient pairs and an unfavorable fibroblast comparison. This
warrants prioritizing epithelial prediction for independent validation. It does
not select a causal receptor configuration, establish IL-1 specificity or show
that the fibroblast biology is absent.

The [pilot exposure record](../../docs/roadmap_runs/2026-09-27-followthrough/A12_PILOT.md)
distinguishes a comparison specified before its new scores/fits from exposure to
earlier results and coverage. Epithelial prioritization followed those outcomes;
the later component display reuses the same patients. Candidate-label transfer,
composition, shared normalization and general inflammation remain alternatives.
Mixed receptor/inhibitor directions and the unfavorable fibroblast result are
part of the evidence, not grounds to choose a favorable subset. The next
informative decision is whether the fixed epithelial prediction transports to a
qualified independent context. Current evidence cannot determine how much of
the gain is biological versus technical or sampling variation.

## What this question could add

The computational contribution is recipient-specific predictive narrowing and
interpretation of the original signed index. Epithelial association is useful
without proving reception. The unchanged registered hypothesis below remains a
functional proposal: an epithelial lead has been prioritized, but the mechanistic
receptor/inhibitory contrast and consequence are still unqualified.

## Current hypothesis and rival

IL-1 receptor and inhibitory context in recipient epithelial cells or fibroblasts may explain an IL-1-dependent response beyond ligand RNA abundance. Those are separate recipient questions; the current portfolio has not fixed one compartment, receptor/inhibitory contrast and biological consequence for a mechanistic experiment. General NF-kB or inflammation scores cannot establish IL-1 specificity.

**Strongest rival:** The index tracks general inflammatory state, cell composition or another stimulus rather than specific IL-1 reception.

## What the comparison would teach

The epithelial result motivates separating receptor/accessory/inhibitory
configuration from population mixture and general inflammation. The current
same-patient component display supports that question but cannot distinguish all
three explanations. Independent epithelial validation would test predictive
transport; a qualified IL-1-dependent response would test the stronger reception
claim. A generic response without IL-1 dependence would leave a useful
inflammatory predictor while weakening the specific functional interpretation.
Source uncertainty prevents a macrophage-only transmission conclusion.

The 23-patient CSC intake is source work in the same study, not 23 new validation
patients. Its healthy-reference labels use some candidate genes and retain
cross-lineage/retention uncertainty. [Exact intake and limitations](../../docs/research_reviews/2026-11-03-tool-assisted-screening-review/A12_SOURCE_INTAKE.md).

## Reading the registered illustration

The retained illustration depicts the registered proposal. The
[measured figure in the question home](README.md#evidence-analyses-and-next-steps)
has a separate evidence-display purpose; no registered asset is replaced.

## Hypothesis schematic

![A12: reviewed matte qualitative illustration](schematics/A12_gpt_matte_v1.png)

GPT-generated matte illustration, 3 November 2026. Proposed relationships and cell counts are qualitative; the owning context defines the comparison and interpretation limits. [Editorial review](../../docs/audits/2026-11-02-rq-schematic-review/MATTE_PUBLICATION_2026-11-03.md) · [Selected edit prompt](schematics/A12_gpt_matte_v1.prompt.txt). Earlier SVG files are retained as history.

Epithelial and fibroblast reception are separate developing questions. The current RNA predictor behaves differently between compartments and ligand-source attribution remains uncertain. Biological units and model need qualification; generic inflammatory RNA cannot identify IL-1 dependence or the active source.

Class-level glyphs and qualitative geometry are not molecular structures, organelle measurements or evidence of functional assembly. Neutral epithelial/stromal shapes do not assert subtype identity or organelle loss, and icon counts are illustrative. Read locally labelled solid premises/references separately from dashed proposed comparisons; no complete mechanism follows from their juxtaposition.

## Next literature check

This synthesis reuses the recorded 3 October primary review and the bounded
3 November adjacent-reference/source records above; no fresh search was performed.
The earlier planned IL-1 recipient query remains a possible future check, not an
executed search. Refresh exact epithelial input, receptor context and
IL-1-dependent endpoint precedents if a new comparison is specified.
[Independent-source qualification](../../docs/audits/2026-11-03-rq-evidence-trajectory/A12_TECHNICAL_RESULT.md)
does not confer novelty or laboratory readiness.

[Current evidence and history](README.md#evidence-and-planning-records) ·
[Research governance](../../docs/RESEARCH_GOVERNANCE.md).
