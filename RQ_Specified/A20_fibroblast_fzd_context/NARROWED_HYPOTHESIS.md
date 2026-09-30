# A20: focused hypothesis and biological decisions

30 September 2026 · scope_refinement_v1 · post-analysis design amendment.
The owner requested narrowing after the exploratory phase. This selects a
focused question; it does not record biological acceptance or validation.
[Analysis results](RESULTS.md) · [Extension evidence](extensions/extension_v1/RESULTS.md) ·
[Execution plan](PLAN.md) · [Current contract](config/question_contract.json).

## One primary question

**Does Fzd2 sustain AF1 fibroblast support of an AT2 pool capable of mature alveolar repair more strongly than Fzd1?**

**Directional hypothesis H1:** In a defined adult alveolar repair context,
comparable Fzd2 loss in prospectively identified AF1-like fibroblasts reduces
functional epithelial support and absolute mature AT2-descendant output more
than comparable Fzd1 loss.

This retains the original mature-output endpoint and receptor comparison.
The narrowing is one receiving fibroblast context, one receptor contrast and
one downstream repair outcome. It is a bounded contribution to functional
Fzd-family mapping; it does not map every receptor or compartment.

The focused mechanistic proposal is **maintenance of an AT2 pool capable of
later maturation**. A maturation-specific effect remains a competing explanation.
The available RNA data do not identify either mechanism. This mechanistic
proposal is a testable refinement of H1, not a second established result.

## Why this is the current scope

The prior mouse atlas places higher Fzd2 with selective support-ligand and
collagen RNA in AF1; the same atlas is reused, not independently replicated.
The human input-context extension shows that FZD2 or canonical-response RNA
can increase while selected support-ligand RNA decreases. Those findings
motivate functional discrimination and rule out using RNA rank as the answer;
they do not establish Fzd2 dependence.

The [source audit](SOURCES.md) supplies receptor-specific motivation and
Notch/lineage context, while the [extension audit](extensions/extension_v1/SOURCES.md)
separates functional support, matrix behavior and concurrent inputs. None supplies
the matched Fzd1/Fzd2 comparison needed for H1. No particular secreted mediator,
Fzd2–Notch interaction or beneficial matrix direction is selected.

## Endpoint hierarchy

| Role | Biological outcome | Interpretation boundary |
|---|---|---|
| Primary, retained from original H1 | Absolute lineage-linked mature epithelial output per starting epithelial population, with prospectively defined identity and functional criteria | A marker score or mature-cell percentage is not the endpoint |
| Required mechanistic companion | Functional epithelial support supplied by the defined fibroblast source | Must distinguish altered source activity from loss of viable support cells |
| Mechanistic discriminator | Supported AT2-descendant pool before the mature-output assessment, with survival and expansion distinguished | Pool size alone does not show maturation competence |
| Competing mechanism | Later fate/function of tracked descendants | A maturation-specific defect may occur despite preserved earlier pool size |
| Biological rival | Fibroblast survival/abundance and matrix deposition/mechanics | Neither post-treatment adjustment nor collagen RNA establishes mediation |

For the primary contrast, let E(r) be the receptor-loss minus matched-control
effect on the primary outcome in the same initial AF1-like context.
The prespecified direction is E(Fzd2) - E(Fzd1) < 0.
Useful-effect margins and uncertainty rules remain unset until an eligible
assay/source is selected, before its new outcomes are inspected.

## Outcomes that discriminate the biology

| Observed pattern under valid, comparable receptor perturbation | Consequence for A20 |
|---|---|
| Greater loss of functional support and mature output after Fzd2 loss, with independent evidence of altered support activity under comparable viable-source conditions | Supports receptor-selective H1; does not yet identify the mediator |
| The above plus a reduced earlier supported AT2 pool and no selective later maturation defect in a valid fate comparison | Compatible with the pool-maintenance proposal; not proof that the pool change mediates the effect |
| Earlier AT2 pool is preserved but later mature output is reduced | Favors maturation-specific support over the pool-maintenance proposal |
| Epithelial output tracks fibroblast depletion and no activity difference is demonstrated beyond depletion | Favors general niche persistence; activity-specific interpretation remains unsupported |
| Matrix function differs alongside output, without evidence separating matrix from other source activity | Receptor dependence may hold, but matrix-mediated versus other support remains unresolved |
| A precise absence of a useful Fzd2-over-Fzd1 decrement, or a reliable reverse direction | Weakens or contradicts receptor-selective H1; equal effects may retain a shared receptor role |
| Incomplete engagement, unequal perturbation validity, missing mature function or imprecise estimates | Inconclusive; not biological refutation |
| Only receptor, ligand, canonical-response or ECM RNA changes | Contextual evidence only; does not decide H1 |

Equal initial input alone does not exclude subsequent fibroblast loss. A
post-treatment count covariate, division by surviving AT2 cells or selection
of survivors cannot by itself distinguish depletion, activity and maturation.
Separate outcome trajectories and source/recipient attribution are necessary;
no mechanistic conclusion follows from a regression adjustment alone.

## Deferred scope and reopening rules

| Earlier branch | Current disposition | Reopen when |
|---|---|---|
| Original H2: receptor dependence differs between initial AF1 and AF2 | Retained, untested; deferred from the primary test | Independently defined subtypes and replicated functional receptor contrasts are available in a comparable context |
| Fzd2–Notch interaction | Biological possibility, not an inferred mechanism | Direct joint perturbation with valid source units and functional outcomes exists |
| Matrix mechanism and a particular secreted mediator | Rivals/secondary outcomes, not parallel discovery programs | Receptor-dependent functional support is established and suitable discriminating evidence exists |
| Other FZD members, neonatal/adult comparisons and chronic-disease generalization | Outside this focused test | A separate eligibility and replication case warrants expansion |

A13 and A15 retain their existing scopes. A19 and A21 remain separate receiving
compartments. The primary A20 context is not identified by a Fzd or support score;
source-defined AF1-like identity requires an independent biological crosswalk.

## Stop condition and next executable step

The current exploratory phase is closed. Further correlations in the same atlas
or gene panels do not resolve the decisive gap.

Next, assess a candidate source against the [functional eligibility gate](PLAN.md#functional-eligibility-gate):
comparable Fzd1/Fzd2 perturbation in the same adult AF1-like setting, verified
engagement, source/recipient identities and biological units, source viability,
and lineage-linked mature output. Only an eligible source justifies a new
functional fit. A source may test total H1 without resolving the pool mechanism;
its conclusion must then stay at that level. No eligible public dataset was
identified in the completed audits.

Original H1/H2 and pre-amendment documents remain in
[scope history](metadata/history/scope_refinement_v1/document_snapshots.json).
No new numerical estimate, figure, RQ ID or claim grade accompanies this amendment.
