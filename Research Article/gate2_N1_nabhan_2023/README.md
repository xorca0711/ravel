# Nabhan 2023: Nb2 receptor-selective regeneration analysis

**Gate 2N, item N1; stable paper ID 6; namespace Nb2.** The owner completed reading
on 29 September 2026. The supplied paper and three private context pages informed
an executed first pass through reproduction, biological exploration and open
hypothesis development. No claim grade changes.

| Start with | Contents |
|---|---|
| [RQ derivation from overall results](RQ_DERIVATION.md) | Three proposed RQs (A19–A21), branch disposition and next discriminating evidence |
| [Executed branch analysis and candidate interpretations](branch_analysis/README.md) | Seven focused branches plus the endogenous-Fzd6 companion; cross-study results, five figures, hypotheses and falsifiers |
| [Results and remaining questions](RESULTS.md) | Main findings, uncertainty and next evidence |
| [Figure gallery](FIGURES.md) | Six bulk and receptor-context figures |
| [Bulk report](trials/bulk_v1/REPORT.md) | All18 libraries, direct comparisons, source panels and enrichment sensitivity |
| [Atlas report](trials/atlas_v1/REPORT.md) | Human source reuse and mouse extension, unit/depth/coverage limits |
| [Published claims and Nabhan hypotheses](HYPOTHESIS_REGISTER.md) | Ten source propositions; Nb2-N1 through Nb2-N8 in the owner's order |
| [Focused extension branches](EXTENSION_BRANCHES.md) | Intermittent exposure, YAP/TAZ, starting state, compensation, signaling output, fibroblast Fzd1 and vascular Fzd4 |
| [Source audit](SOURCE_AUDIT.md) and [functional recovery](FUNCTIONAL_SOURCE_AUDIT.md) | Corrections, data units and unrecovered functional evidence |
| [Original analysis plan](ANALYSIS_TRIAL_PLAN.md) and [dataset map](DATASETS.md) | Three-track design and source/extension roles |
| [Execution and replay](EXECUTION.md) | Scripts, frozen contracts and reproducibility |
| [Current stage ledger](metadata/stage_status.tsv) | Completed measurements and unresolved gates |

The biological question is whether receptor-selective Wnt signaling expands
regenerative epithelial capacity while preserving later differentiation and
avoiding persistent stromal remodeling. This follows the repository's
[reading → reanalysis → question → specified test sequence](../../README.md).
Growth, AT2 identity, AT1 contribution and fibrosis remain separate endpoints.

[Nabhan et al., Cell 2023](https://doi.org/10.1016/j.cell.2023.05.022) combines
receptor maps, inhibition/deletion, organoid growth, bulk transcription, injury
outcomes and airway-derived organoids. GSE208770 is **bulk AT2-organoid RNA-seq**,
not a single-cell agonist-response atlas. Its18 deposited libraries support an
adapted transcriptional reconstruction, with unresolved preparation identity
and timing. Crim2 remains unresolved, and the published DEG totals are not
numerically reproduced by the frozen adaptation.

The measured findings refine the [Nabhan cards](HYPOTHESIS_REGISTER.md#nabhan-branch);
none is a validated new hypothesis. Exact healthy-atlas and functional source
reproduction still need unavailable source inputs. New question-specific tests
belong under the owning `RQ_Specified/` contract; the existing Axin2/Il1r1 question
stays with A4/Nb1. The subsequent [synthesis](RQ_DERIVATION.md) proposes A19–A21
with separate question plans; the original branch cards remain paper-local.

[Numerical verification](metadata/execution_validation.json) checks provenance and
independent table arithmetic. [Repository validation](metadata/repository_validation.json)
checks contracts and links. The earlier [planning validation](metadata/validation.json)
is retained as history. Raw inputs, full private notes and the annotated PDF are
not tracked; compact tables, figures, source hashes and scripts are retained.
