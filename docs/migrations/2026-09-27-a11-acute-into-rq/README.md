# Migration: the A11 acute-injury assay moves into the question hierarchy

27 September 2026. The assay was executed under the computational research pipeline and its outputs
were written under `docs/research_pipeline/`, which is process scaffolding rather than the question
hierarchy. `RQ_Specified/README.md` states that question-specific plans, workflows, metadata and
tables belong under `RQ_Specified/`. This move puts them there. **No number changed and no file was
deleted.**

## What moved

Fifty-six tracked files, all with `git mv` so history follows them.

| From | To |
|---|---|
| `docs/research_pipeline/config/a11_acute_injury_contract.json` | `config/gse198864_acute_injury_contract.json` |
| `docs/research_pipeline/scripts/*` | `scripts/05` to `scripts/15`, continuing the folder's numbering |
| `.../2026-09-27-execution/c1/` | `tables/acute_injury_gse198864/intake/` |
| `.../c3/` | `tables/acute_injury_gse198864/gate/` |
| `.../c4/` | `tables/acute_injury_gse198864/scores/` |
| `.../c5/` | `tables/acute_injury_gse198864/diagnostics/` |
| `.../c6/` and `.../c7/` | `tables/acute_injury_gse198864/concordant_identity/` |
| `c1/REPORT.md`, `c1/ENVIRONMENT_GATE.md`, `c5/REPORT.md` | `reports/ACUTE_INJURY_INTAKE.md`, `ACUTE_INJURY_ENVIRONMENT_GATE.md`, `ACUTE_INJURY_RESULTS.md` |

All destinations are under `RQ_Specified/A11_lesion_programme_addition/`.

The scripts were renumbered rather than renamed in place, because this folder already numbers its
instruments 00 to 04 for the Kim test and a second assay continuing that sequence is what the
hierarchy expects. The stage letters C1 to C7 survive only in the pipeline queue, which is where the
process record belongs.

## What did not move

`docs/research_pipeline/queue.json` stays. It tracks tasks across A5, A11 and A12, so it is not
question-specific, and its artefact pointers were rewritten to the new locations.
`docs/COMPUTATIONAL_RESEARCH_PIPELINE.md` and the handoff under `docs/handoffs/` likewise stay and
were repointed.

The retrieved 6.5 GB object and the derived caches were never tracked and are untouched under
`raw_data/`, which `.gitignore` excludes.

## How the record was kept honest

Every run record under the new tree carries a `relocated_2026_09_27` field naming this note, because
its `script` and output path strings were rewritten to point at the new locations. The alternative,
leaving the old strings, would have left every record pointing at paths that no longer exist. The
numbers in those records are untouched.

Three reports had relative links that the move broke; all fifteen were repointed and a link check
reports none remaining. One moved script was re-run into a scratch directory and reproduced its
recorded figures exactly, which is the check that the relocation did not break execution:
`13_virus_table.py` returns the same 46 viral features and the same per-arm detection counts.

## Where the assay is now registered

It was previously reachable only from the pipeline queue and the handoff. It now appears in the A11
folder README, in the A11 register card, and in the `RQ_Specified` index. That gap is the reason for
the move: an assay that answers a register question should be findable from the register.
