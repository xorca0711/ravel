# Extension execution, validation and handoff

31 October 2026 (Asia/Seoul).

- Worktree reused only after confirming clean state:
  `C:/Users/dream/.codex/worktrees/saxton-metadata-recovery-20261031/ravel`.
- New branch: `codex/saxton-source-audit-20261031`.
- Requested plan/base: `162493af485e7160d84feebb73818d1b5daa09e2`.
- Frozen metadata specification commit: `1f7b0d54a66e821039ff09ef103d2c1fab04af60`.
- Integration base checked by fetch: `4df267d3f5035b249df2e587c70a8b9e9253b049`.
- Python 3.12.10 ARM64, standard-library metadata scripts. No scientific package,
  expression model, external annotation mapper or sequence download was needed.

The clean completed recovery branch remains at its original commit. No primary,
review or original execution checkout was edited. Raw inputs and the newly
retrieved source documents are retained in ignored caches; their exact locators,
hashes and access outcomes are in [SOURCE_MANIFEST](SOURCE_MANIFEST.md).

## Freeze and execution

Both contracts were input-preflighted, committed with exact code/tests and
registered before either runner invocation. Prior paper/R1 exposure, schema
inspection and raw metadata retrieval are explicitly recorded. Freezing did not
make this unexposed confirmation. Each runner produced a new directory and
successful immutable receipt; `scientific_acceptance=not_assessed` is unchanged.

```text
python -m unittest discover -s "Research Article/gate3_08_saxton_2021_il22/extensions_20261031/tests" -q
python analysis/scripts/research_gate.py preflight "Research Article/gate3_08_saxton_2021_il22/extensions_20261031/config/x1_contract_v1.json" --inputs
python analysis/scripts/research_gate.py preflight "Research Article/gate3_08_saxton_2021_il22/extensions_20261031/config/x2_contract_v1.json" --inputs
python analysis/scripts/research_gate.py run "Research Article/gate3_08_saxton_2021_il22/extensions_20261031/config/x1_contract_v1.json" --run-id sx22_x1_annotation_v1
python analysis/scripts/research_gate.py run "Research Article/gate3_08_saxton_2021_il22/extensions_20261031/config/x2_contract_v1.json" --run-id sx22_x2_provenance_v1
python analysis/scripts/research_gate.py verify analysis/research/runs/sx22_x1_annotation_v1/receipt.json
python analysis/scripts/research_gate.py verify analysis/research/runs/sx22_x2_provenance_v1/receipt.json
```

All commands passed: eight targeted tests, both preflights, both executions and
both receipt verifications. Synthetic tests reject wrong/missing metadata links,
duplicate experiments, missing annotation headers and annotation disagreement;
they demonstrate that nonnumeric expression strings are not parsed and that
version diagnostics, sequencing pairing and candidate animal fields do not
collapse records or certify biological independence.

## Independent checks and review

A separate temporary verifier, without importing either frozen analysis script,
checked all bound input/code/output hashes and contract hashes, every annotation
row against both original tables, every repeated-symbol group, all six source
chains and all retrieved-file hashes. It also compared R1 contracts/run bytes
and root `.gitattributes` to the plan base. All checks passed. Session-local
checker: `C:/Users/dream/AppData/Local/Temp/sx22_extensions_verify.py`.

The originating reviewer separately reported agreement on 20 bound
input/code/output hashes, both contract hashes, all 35,275 projected annotation
rows, 52 symbol summaries and six sample/run chains. It also independently checked
Figure S5e/caption and the distinction from S5c/d's mouse counts. No code or run
output changed after that review. Final integration review remains separate.

For X3, Poppler rendered supplement PDF pp. 23–24 for visual review; pypdf supplied
the caption and reporting-summary text. The workbook's sheet/index structure and
leading rows were read as OOXML without recalculation or modification. These
checks document labels and source scope, not a biological effect or human acceptance.

## Required repository checks

All required checks passed against fetched `origin/main` at `4df267d3f5035b249df2e587c70a8b9e9253b049`:

| Command | Result |
|---|---|
| `python analysis/scripts/validate_repository.py` | 12,687 checks passed |
| `python analysis/scripts/research_gate.py check --base origin/main` | `ok=true`, no errors |
| `python -m unittest discover -s analysis/tests -q` | 158 tests passed; two Windows symlink skips |
| `python -m compileall -q -x '[/\\]\.tools[/\\]' analysis "Research Article" RQ_Specified` | Passed |
| `python analysis/scripts/claim_contract.py --check` | 18 numeric bindings verified |
| `python "Research Article/gate1_03_nabhan_2018/nb1/verify_outputs.py"` | 17 output hashes and required provenance checks passed |
| `python "Research Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/scripts/verify_archive.py"` | 20 run records and 164 output hashes passed |
| `python RQ_Specified/A16_cd177_state_attribution/scripts/verify_stage1_evidence.py` | 1,867 checks passed |
| `python RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/08_verify_external_current.py` | Passed |
| `python analysis/scripts/verify_a22_a23_extensions.py` | Passed |

Older unchanged archive evidence was verified without running biological analyses.
Final preservation checks confirmed the bounded 27-file diff, byte-identical
historical article README after removing its new navigation paragraph, unchanged
root attributes/R1 contracts and unchanged registry state after removing the two
new contracts, two receipts and one evidence link. R1 run bytes were also verified
in the independent check above. The freeze wording was corrected to distinguish
pre-execution contracts/code from post-execution run outputs/receipts.

The initial final-check output was unavailable after context compaction, so the
mechanical checks were repeated with saved logs. No scientific run was repeated.
Session-local logs: `C:/Users/dream/AppData/Local/Temp/sx22-validation-final/`.

## Failures and remaining state

The first synthetic-test invocation failed on two sandbox temporary-file
permissions; the identical tests passed under approved execution. No code was
weakened and no scientific run was attempted before freeze. The first sandbox
PDF render produced no usable images; the ordinary approved Poppler invocation
succeeded. Source-access failures and successful ordinary mirror retrievals are
retained separately in the manifest. No new biological-content restriction was
reported during these metadata/documentary jobs; the original restriction is
not claimed lifted.

Next: originating chat reviews the complete local handoff and any integration.
X1 annotation-release ambiguity, X2 biological-unit unknowns and X3 endpoint-link
limits remain explicit in [RESULTS](RESULTS.md). R2/R3 and all excluded biological
work remain held. No push, PR mutation, merge, author contact, Notion write,
bench work, external setting change or scientific acceptance occurred here.
