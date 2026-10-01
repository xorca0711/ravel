# Nb3 — Nabhan 2026: alveolar stem-cell identity and the fibroblast niche

*Mapping the dialogue: Decoding alveolar stem–niche interactions.* Nabhan et al.,
PNAS 123, e2606113123. [Paper](https://doi.org/10.1073/pnas.2606113123).
Gate **2N, item 2**; stable roadmap paper **14**; analysis ID **Nb3**.
The owner completed reading and authorized reproduction and extensions.
The corrected folder label is `gate2_N2_nabhan_2026`.

The paper asks how changes in AT2 epithelial identity and growth reshape the
fibroblast niche. Imaging and species-separated bulk RNA from mixed organoids
connect epithelial perturbations to both compartments. The reproduction tests
selected growth, identity and niche responses; the extensions ask which
patterns justify hypotheses about repair and communication.

**Updated 1 October 2026: partial reproduction, descriptive extensions and
follow-up complete.** Eleven original figures plus one external E5 pilot figure
are available. Two RQs are proposed as **A22/A23**; all eight annotated candidates
have explicit framings. Human S5 numeric reproduction remains unresolved.
Technical wells do not establish independent biological replication. Exact
embeddings, spatial interpretation and the paper's DepMap comparison remain
incomplete. The E5 pilot is a separate external analysis.

## Read this study

| To understand | Read |
|---|---|
| What was reproduced, what failed and what remains open | [Reproduction review](reports/REPRODUCTION_REVIEW.md); [S5 audit](reports/CONCORDANCE_AUDIT.md) |
| Results for the eight annotated extension questions | [Extension review](reports/EXTENSION_REVIEW.md); [completed follow-up](reports/FOLLOWUP_RESULTS.md) |
| Generated plots, units, source tables and captions | [Figure gallery](#figure-gallery); [all figures](FIGURES.md) |
| Hypotheses, rivals and decisive outcomes | [Eight candidate cards](CANDIDATE_HYPOTHESES.md); [A22/A23 derivation](reports/RQ_DERIVATION.md) |
| Contributions to earlier RQs after strict review | [Integration review](reports/RQ_INTEGRATION_REVIEW.md); [cross-article review](../../docs/audits/2026-10-01-cross-article-rq-review/README.md) |
| E5 public datasets, executed pilot and refined candidate | [External feasibility and results](reports/E5_EXTERNAL_FEASIBILITY.md) |
| Source paper, annotations and original plan | [Source synthesis](SOURCE_SYNTHESIS.md); [analysis plan](ANALYSIS_TRIAL_PLAN.md); [repository context](REPOSITORY_CONTEXT.md) |
| Data, environments, run order and verification | [Datasets](DATASETS.md); [execution guide](EXECUTION.md) |

## Findings at a glance

| Biological topic | Current reading | Evidence / limit |
|---|---|---|
| Growth and source reconstruction | Imaging and selected source tables are recovered; DE agreement differs by species | Mouse S4 agrees broadly; numeric human S5 does not |
| NKX2.1 and niche response | Lower AT2 and fibroblast chemokine markers, higher wound markers retain direction under local sensitivities | Motivates A22; secretion, immune recruitment and causal mediator remain unmeasured |
| Transitional state | Different IFN/hypoxia-associated bulk responses | No demonstrated trajectories or productive versus arrested fate |
| ELOVL1 / ATP6V0E | Lower AT1-marker patterns persist; Wnt interpretation remains uncertain | Lipid/acidification mechanisms are candidates; no calibrated Wnt-independence test |
| SLC34A2 | Three transition markers rise with smaller identity attenuation than NKX21 | Motivates A23; phosphate mediation and temporal order remain open |
| Receptor function / E5 | External ERBB3 and EGFR knockdown show different inflammatory RNA responses under irradiation | Cultured-epithelial context; sparse AT2 markers preclude a normal AT2 renewal conclusion |

The [follow-up report](reports/FOLLOWUP_RESULTS.md) owns detailed numerical
interpretation. RNA programmes do not independently reproduce the paper's
functional experiments.

## Data and biological units

| Material | Available measurements | Unit and limitation |
|---|---|---|
| Mixed-species organoid screen | Imaging and 886 RNA libraries per species; 771 wells retained in the paired analysis | Species-separated **bulk** wells, not single cells. Preparation identities unresolved; target, guide and plate position confounded |
| Deposited S1–S7 | Design, imaging, source DE, components and marker definitions | Source-derived results remain separate from newly fitted results; S5 has internal sign conflicts |
| Spatial / cancer context | Public metadata and source descriptions | Treatment/animal/grid reconciliation and original DepMap release/cohort unresolved |
| External GSE306184 | 14 human epithelial libraries in seven groups; downloaded count tables | Two libraries per group do not establish two donors. Protocol fields conflict and uninjured knockdown groups are absent |

Source PDFs, supplementary workbooks and private annotation snapshots remain
in the ignored local data cache. Compact results, provenance and generated
figures are deposited here. Existing A10/A2 fits retain their original ownership.

## Figure gallery

The [complete gallery](FIGURES.md) gives every panel's unit, source table and
interpretation. PNG exports are 300 dpi, with PDF and SVG companions. The
[original 11-page atlas](figures/Nb3_complete_figure_atlas_v2.pdf) remains unchanged;
the [external E5 figure](figures/E5_external_v2/Nb3_F09_E5_external_pilot.pdf)
is a separate addition.

| Browse by biological question | Figures |
|---|---|
| [Growth and reconstruction](FIGURES.md#figure-1-imaging-reconstruction-across-focal-perturbations) | F01 imaging; F02 concordance; S01 QC |
| [Epithelial identity and niche response](FIGURES.md#figure-4-epithelial-identity-and-paired-fibroblast-responses) | F03 panels; F04 paired niche; F07 sensitivity; S03 depth/influence |
| [Transition, homeostasis and pathways](FIGURES.md#figure-5-candidate-state-patterns-and-component-activities) | F05 candidates; F08 Hallmarks; S02 source components |
| [Receptor context](FIGURES.md#figure-6-receptor-expression-and-growth-context) | F06 expression and growth |
| [External E5 epithelial-response pilot](FIGURES.md#figure-9-external-e5-epithelial-response-pilot) | F09 receptor response, inflammatory genes and AT2 coverage |

## Analysis stages

Stages reuse the source screen; they are not independent replication cohorts.
The external E5 deposit is a different study with its own design limits.

| Order | What ran | Report / contract |
|---|---|---|
| Intake | Paper, supplementary data, annotations, joins and design inventory | [Source synthesis](SOURCE_SYNTHESIS.md); [historical intake](reports/INTAKE.md) |
| Reproduction | Imaging, species QC, 395 target DE fits, panels and source comparison | [Review](reports/REPRODUCTION_REVIEW.md); [v1 contract](config/Nb3_execution_v1.json) |
| Concordance audit | Internal S5 consistency, source directions and independent count XML checks | [Audit](reports/CONCORDANCE_AUDIT.md) |
| Initial extensions | Eight questions assessed with descriptive results and feasibility limits | [Extension review](reports/EXTENSION_REVIEW.md) |
| Follow-up | Marker/control/well/depth sensitivities, target-transcript checks and Hallmarks | [Results](reports/FOLLOWUP_RESULTS.md); [contract](config/Nb3_followup_v1.json) |
| RQ review | A22/A23 derivation and strict integration into earlier RQs | [Derivation](reports/RQ_DERIVATION.md); [integration review](reports/RQ_INTEGRATION_REVIEW.md) |
| External E5 | Metadata audit and four-contrast receptor/context pilot | [Results and candidate](reports/E5_EXTERNAL_FEASIBILITY.md); [contract](config/Nb3_E5_external_v1.json) |

## Questions and next decisions

[A22](../../RQ_Specified/A22_epithelial_identity_niche_response/README.md)
asks whether epithelial identity maintains fibroblast chemokine competence
beyond epithelial amount.
[A23](../../RQ_Specified/A23_slc34a2_transition_homeostasis/README.md)
asks whether phosphate homeostasis constrains transition-associated stress.
Both remain proposed, without claim-grade promotion. Main owns A19–A21 for
Nb2/Fzd; the [ID correction](reports/RQ_ID_CORRECTION_2026-10-01.json) records
the relabelling.

The [candidate cards](CANDIDATE_HYPOTHESES.md) retain broader questions.
E5 now has a distinct epithelial-function candidate and public-data pilot.
Functional engagement, independent units, state/lineage linkage, secretion
and recipient outcomes remain decisive. The
[pre-RQ plan](reports/PRE_RQ_ANALYSIS_PLAN.md) identifies outstanding source,
spatial and cancer-data requirements. Study-specific results stay here;
question-specific execution belongs in `RQ_Specified/`.

## Identifier guide

| Label | Meaning |
|---|---|
| Nb3 | This Nabhan 2026 reproduction/extension package |
| Paper Figure / Table S1–S7 | Published source evidence |
| Nb3 F01–F09 / S01–S03 | Repository figures; F09 is the external E5 pilot |
| E1–E8 | Paper-local annotated candidates |
| A22/A23 | Proposed global RQs |

For commands and checks use the [execution guide](EXECUTION.md). Original runs,
frozen configurations and superseded figure exports are retained.
