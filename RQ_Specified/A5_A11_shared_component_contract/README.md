# Shared epithelial component contract (A5 and A11)

**Current development framing:** [A5 development dossier](../../docs/research_dossiers/A5.md) and [A11 development dossier](../../docs/research_dossiers/A11.md). Read its evidence, rival explanation and experimental bridge alongside the historical plan and current results below.

## Organizing biological questions

This shared workspace supports two questions:

- **A5:** Does adult alveolar repair reuse part of a developmental epithelial programme?
- **A11:** Which lesion-associated programmes add to a shared epithelial plasticity component?

Both questions need an explicit account of what the selected developmental,
injury and lesion-associated gene lists share. Otherwise, overlapping genes can
make a context-associated score appear to identify a distinct biological process.

This folder defines the source-list partition, exclusions and measurement
contracts used by the two analyses. It is enabling work with two owning questions,
not a new A-number or a single combined biological test. Each question keeps its
own units, comparison and decision.

**Read first:** [A5 card](../../RESEARCH_QUESTIONS.md#a5),
[A11 card](../../RESEARCH_QUESTIONS.md#a11), [biological logic](BIOLOGICAL_LOGIC.md),
[plan](PLAN.md), [revised results](reports/REVISED_TEST_RESULTS.md).

**Current figure presentation:** [paired-estimate forest plot with biological units](figures/revision_20260929/a5_a11_results.png) labels A5 as 24/26 mice and A11 as eight patient pairs. This 29 September presentation revision reads the saved estimates and intervals; the [original figure](figures/a5_a11_results.png) and analysis records remain unchanged. [Render provenance](figures/revision_20260929/render_record.json).

## Evidence and analysis history

**Status: contract and revised A5/A11 tests complete; PR #77 merged.** The owner
retained the original partition on 25 September 2026 (DEVELOPMENT decision 37).
It remains a provenance reference. The revised A5 primary instead uses additional
external Guo modules because the original Strunz-filtered variants are descriptive.
Results live in [A5's folder](../A5_developmental_programme_reuse/README.md) and
[A11's folder](../A11_lesion_programme_addition/README.md); their interpretation and
verification are collected here. Historical claim grades are unchanged.

Start with [the biological logic and revised analysis sequence](BIOLOGICAL_LOGIC.md)
and [the completed results](reports/REVISED_TEST_RESULTS.md). A5 supports partial
external-signature recruitment after the planned exclusions. A11 replicates lesion
association, while its beyond-shared comparison remains unresolved.

- **A11:** eight eligible Kim patient pairs; the original 23 are discovery.
  Its amended plan separates lesion association from relative activation.
- **A5:** an external Guo gene set avoids Strunz-derived filtering for the primary
  test. The old 94/51-gene variants remain descriptive in Strunz.
- **Shared:** 5 development–injury and 7 injury–lesion genes, with no three-way
  intersection. Biological unrelatedness is not established by limited overlap.

## What this is

Enabling work owned jointly by [A5](../../RESEARCH_QUESTIONS.md#a5) and
[A11](../../RESEARCH_QUESTIONS.md#a11). One source-list partition makes overlap and
exclusions traceable across both questions. It contains two disjoint pairwise
overlaps, not a common programme demonstrated across all three contexts. Each
question retains its own biological reference and test. The labels
`development_specific` and `lesion_specific` mean exclusive within these selected
lists; they do not establish specificity in biology.

## What this is not

- **Not a new research question.** It takes no new register identifier. Its
  status matches the enabling source-identity question A12-S1.
- **Not a merge of A5 and A11.** The two keep separate species arms, biological
  units, contexts, multiplicity families and decisions. The register's merge rule
  requires a shared test and a shared decision, which these do not have.
- **Not a result.** Passing this contract licenses two later tests. It
  establishes no mechanism, cell identity, ancestry or fate.

## Stage 1 outcome

The missing developmental input is now sourced. The existing
[specificity module](../../Research%20Article/epithelial_state_specificity/README.md)
recorded that no independent developmental signature was available locally. Seven
external candidates were examined and one selected: the author-defined signature
of a mixed type 1 and type 2 population in normal mouse lung at postnatal day 1,
from Guo et al. 2019. The audit records why the other six were not used, and that
the selection is partly by accessibility.

## Layout

| Path | Contents |
|---|---|
| [PLAN.md](PLAN.md) | Prospective plan, stages, species and unit rules, prohibited readings |
| [config/shared_component.json](config/shared_component.json) | Reviewable specification: sources, exclusions, partition rule, gates |
| `config/README.md` | What the specification fixes and what stays open |
| [reports/STAGE1_SOURCE_AUDIT.md](reports/STAGE1_SOURCE_AUDIT.md) | Every candidate examined, the doublet check and the limitations |
| [reports/STAGE2_3_REPORT.md](reports/STAGE2_3_REPORT.md) | Frozen modules, eligibility per question, limitations and stage 4 decisions |
| [scripts/README.md](scripts/README.md) | How to rerun the freeze and the coverage report |
| `tables/` | Frozen modules, membership, overlap, coverage, unit floors and run records |
| [tables/stage3_attempt1_refused/](tables/stage3_attempt1_refused/README.md) | The first coverage attempt, refused by its own precedent check |
| `sources/README.md` | Identity of the untracked cached source spreadsheet |

The layout follows the question-specific pattern in the
[structure contract](../../docs/REPOSITORY_STRUCTURE.md).

## Historical evidence at contract creation

Every number below is read from existing tracked evidence, not recomputed here.

| Fact | Value | Source |
|---|---|---|
| Assayed source fraction gate | 0.7 | Completed human specificity trial |
| Complete-unit floor per paired contrast | 3 | Same trial |
| Lists already failing the fraction gate | 0.641 and 0.667 | Same trial |
| Lists already passing it | 0.780 and 0.791 | Same trial |
| ADI holdout ortholog fraction, which a mapping-only gate would pass | 0.859 | Same trial |
| A11 paired patients, lesion contrast | 23 | Same trial |
| A5 animals passing both group floors | 1 of 25 | Specificity module |
| Local human developmental lung deposits | none found | Scan of local GEO family records |
