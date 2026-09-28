# A16: does CD177 identify a priming phenotype within comparable mutant cells?

**Current status, 28 September 2026: proposed; partly measured and inconclusive.**
The [shared question card](../../RESEARCH_QUESTIONS.md#a16) owns the hypothesis.
Read the [integration review](reports/INTEGRATION_REVIEW.md) before the original
Stage 1 report. Publication of these results does not establish a mechanism or
change a historical claim grade.

## Biological question

Within comparable transitional mutant cells, CD177 may identify a
priming-associated phenotype beyond the local mixture of epithelial states.
Neighbourhood association and a stable intrinsic programme can coexist. RNA
alone cannot establish persistence or functional growth potential.

## What has run

C3/C4 and then C1/C2/C5 ran on previously exposed England data. The population
amendment distinguishes the transition gate per library from FU_C's original
pooled, all-cell subclusters. The latter is a diagnostic of the old result,
not a within-transition, per-library contrast. C1 used UMAP as a declared
substitute for the frozen integrated space.

Matched-gene specificity is inconclusive: seven of nine descriptive entries
have fewer than 40 control genes. Remaining effects under the neutrophil-panel
adjustment do not exclude ambient contamination. Full-depth cutoff stability
does not replace thinning: all four primary-library thinning rows fail the
cell floor. The original report's stronger exclusions are superseded.

## What remains open

The corrected same-population attribution test needs a prospective amendment
if pursued. Independent marker/outcome linkage is required for a stable,
functionally distinct phenotype. Existing external candidates have not become
matched validation simply because Stage 1 ran. No new biological analysis was
executed during branch integration.

| Record | Role |
|---|---|
| [Current integration review](reports/INTEGRATION_REVIEW.md) | Current interpretation and unresolved comparisons |
| [Original Stage 1 results](reports/STAGE1_RESULTS.md) | Historical numerical report; stronger interpretations superseded |
| [Population erratum](reports/STAGE1_ERRATUM.md) | Pre-execution two-arm amendment |
| [Original rationale](RATIONALE.md), [plan](PLAN.md), [contract](config/a16_question_contract.json) | Preserved planning history; original premises/status are not the current verdict |
| [Public-data search](reports/PUBLIC_DATA_SEARCH.md) | Dated search boundaries |
| [Verification record](reports/INTEGRATION_VALIDATION.json), [verifier](scripts/verify_stage1_evidence.py) | Lightweight provenance and table checks; no raw-data replay |

Run the verifier from a clean clone with standard-library Python:

```bash
python RQ_Specified/A16_cd177_state_attribution/scripts/verify_stage1_evidence.py
```

Keep cell thresholds, exposure history and missing biological-unit identities
explicit. Do not pool libraries to claim independent replication or substitute
cycling RNA for a measured outcome. Original execution scripts overwrite
outputs; they must not be replayed over the archived evidence.
