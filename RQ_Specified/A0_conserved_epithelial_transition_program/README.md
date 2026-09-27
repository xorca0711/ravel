# A0 — Conserved processes across epithelial transitions

Created: 2026-09-25. Updated: 2026-09-26.
Status: **Exploratory expression pilot executed. Decision: narrow; stop broad expansion of this candidate.**

Read the [current expression report](reports/EXPLORATORY_PILOT_REPORT.md).
A 50-gene repair program is positive against both endpoints in 9/9 held-out mice
and survives source depth and mixture checks. It is positive in one qualifying
developmental capture group, but lacks robust intermediate-specific transfer in
the two qualifying intestinal mice. A smaller pre-transfer variant is sensitive
to intestinal depth matching. These findings do not disprove a universal process.

## Biological question

Do epithelial cells reuse a conserved regulatory process when passing between
differentiation states, despite differences in tissue, starting identity and
destination identity?

The motivating hypothesis concerns a universal process. The executed amendment
tests a narrower prediction: **a program learned in lung repair also distinguishes
source-defined intermediates in normal lung development and intestine.** Source
annotations, small transfer cohorts and the developmental normalized assay limit
what this prediction can establish about conservation, specificity or causality.

## Read in this order

| File | Purpose |
|---|---|
| [Exploratory report](reports/EXPLORATORY_PILOT_REPORT.md) | Executed analyses, figures, limits and investment decision |
| [EXPLORATORY_PLAN.md](EXPLORATORY_PLAN.md) | Authorized repair-first amendment and stage gates |
| [Stage decisions](stage_decisions.json) | Review of whether each succeeding analysis was worthwhile |
| [PLAN.md](PLAN.md) | Historical original two-context discovery design; not completed |
| [DATASET_CANDIDATES.md](DATASET_CANDIDATES.md) | Three dataset roles, existing resources, eligibility and unresolved selections |
| [Historical feasibility report](reports/PILOT_REPORT.md) | Earlier metadata findings and replication gaps |
| [Readiness](readiness.json) | Current exploratory status and remaining original-design requirements |
| [Reproduction and input contract](REPRODUCING.md) | Commands, required metadata and unblocking conditions |
| [P0 eligibility report](reports/P0_ELIGIBILITY_REPORT.md) | Executed coverage audit, limitations and next selection steps |
| [Dataset audit](tables/dataset_audit.csv) | Candidate-level eligibility decisions |
| [Decisions](decisions.json) | Dated scope and interpretation decisions |
| [Expression source manifest](expression_source_manifest.json) | Expression input provenance and hashes |
| [Validation](exploratory_validation.json) | Numerical, alignment, freeze, artifact and figure checks |

## Executed scope

- Three settings: lung repair, normal lung development and differentiation in
  one other epithelium. Prefer one species for the first pass.
- One primary 50-gene program learned in nine repair mice, evaluated against
  both endpoints with leave-one-mouse-out gene selection.
- Source technical and generic-response challenges, then frozen descriptive
  transfer in development and intestine. Biological samples determine replication.
- A targeted post-transfer intestinal depth check, a report and three figures.
  Program and branch definitions were not retuned after transfer.

A positive pilot supports a transferable transcriptional association. It does
not establish universality, causal control, actual cell fate or transition rate.

## Relationship to existing work

A0 asks about conservation **across transitions and tissues**. The adjacent
[A1 workspace](../A1_transitional_epithelial_state_distinction/) concerns
transitional epithelial-state distinction. The existing
[ES1 analysis](../../Thesis/epithelial_state_specificity/README.md) supplies
signature provenance, overlap checks and measurement controls; its data and
previously inspected findings are not untouched validation.

The original design still requires adequately replicated developmental discovery
and independent tissue validation. Its gaps are preserved in
[feasibility_readiness.json](feasibility_readiness.json); the completed exploratory
amendment does not manufacture missing replication. Historical audit records and
their validation remain separate from the current expression execution record.
