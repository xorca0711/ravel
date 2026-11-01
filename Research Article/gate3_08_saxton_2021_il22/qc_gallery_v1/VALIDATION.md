# QC gallery validation and local handoff

1 November 2026 (Asia/Seoul). Scope: two render-only technical QC figures under
Sx22-P01, using already-reviewed immutable summaries. No biological analysis rerun.

- Worktree: `C:/Users/dream/.codex/worktrees/saxton-metadata-recovery-20261031/ravel`.
- Branch: `codex/saxton-qc-gallery-20261101`, created after confirming clean state.
- Requested merged base: `41dc12716e1c09d288fd38847ce899ad381d926b`.
- Prospective plan/code/contract freeze: `05fa2ffa5af8bb28bbbe8db9bd3336c106dfa99c`.
- New immutable run: `analysis/research/runs/sx22_qc_gallery_render_v1`.

## Execution and verification

All source quantities were already exposed. Eight synthetic tests passed before
freeze, covering source order/coverage, exact value projection, invalid fractions/
denominators, overlapping metadata dimensions, source-summary disagreement,
duplicate records, SVG normalization and refusal to overwrite outputs. Synthetic
PNG previews were visually inspected before committing the code. Both input
preflight and the one runner execution passed; the receipt verification passed.
Python 3.12.10 ARM64 and existing Matplotlib 3.11.1 were used; no new dependency
installation or external retrieval was needed.

```text
python -m unittest discover -s "Research Article/gate3_08_saxton_2021_il22/qc_gallery_v1/tests" -q
python analysis/scripts/research_gate.py preflight "Research Article/gate3_08_saxton_2021_il22/qc_gallery_v1/config/render_contract_v1.json" --inputs
python analysis/scripts/research_gate.py run "Research Article/gate3_08_saxton_2021_il22/qc_gallery_v1/config/render_contract_v1.json" --run-id sx22_qc_gallery_render_v1
python analysis/scripts/research_gate.py verify analysis/research/runs/sx22_qc_gallery_render_v1/receipt.json
```

A separate read-only checker imported no rendering code. It verified all 15
input/code/output bindings plus the contract hash; all 18 R1 values, exact source
order and display strings; and all nine X1 category values/denominators against
the frozen summary. A separate count of the repeated-symbol metadata agreed on
the 52-label/122-row total and six overlapping dimension cardinalities. This was
source-to-figure verification, not a repeat of raw-source analysis.

Both actual PNGs were visually inspected: all six library labels, exact values,
axis units, zero category, shared X1 denominator and overlapping-category warning
are readable, with no clipped text. Both SVGs parse as XML and contain every
plotted value label. Trailing whitespace was normalized in memory before the
first write as specified prospectively; neither generated SVG needs an exception
or post-execution edit. Frozen sources and outputs remain unchanged.

The originating reviewer independently passed all 16 receipt/contract bindings,
all 18 library measurements and nine annotation category values/denominators.
Its review of the rendering code and both actual PNGs found no amendment needed;
both SVG XML/whitespace checks also passed. This technical review does not imply
human scientific acceptance or biological replication.

## Repository checks

Checks use freshly fetched `origin/main` at `41dc12716e1c09d288fd38847ce899ad381d926b`.

| Command | Outcome |
|---|---|
| `python analysis/scripts/validate_repository.py` | 12,782 checks passed |
| `python analysis/scripts/research_gate.py check --base origin/main` | Passed: `ok=true`, no errors |
| `python -m unittest discover -s analysis/tests -q` | 158 tests; two Windows symlink skips; passed |
| `python -m compileall -q -x '[/\\]\.tools[/\\]' analysis "Research Article" RQ_Specified` | Passed |
| `python analysis/scripts/claim_contract.py --check` | 18 numeric bindings verified |
| `python "Research Article/gate1_03_nabhan_2018/nb1/verify_outputs.py"` | 17 output hashes and provenance checks passed |
| `python "Research Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/scripts/verify_archive.py"` | 20 run records and 164 output hashes passed |
| `python RQ_Specified/A16_cd177_state_attribution/scripts/verify_stage1_evidence.py` | Passed |
| `python RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/08_verify_external_current.py` | Passed |
| `python analysis/scripts/verify_a22_a23_extensions.py` | Passed |

Logs are retained locally in `.tools/sx22_qc_gallery_validation/`. Mechanical
scope verification passed for all 16 changed paths: this package, the new run
and the registry only. Removing one new contract and one new receipt recovers
the original registry object exactly. Code/tests/contract remain byte-identical
to the pre-execution commit. Full `git diff --check 41dc127` passed without
excluding generated files; no whitespace exception is needed for this package.

## Ownership and remaining limits

Changes are confined to this new package, its one new run and the registry's
required contract/receipt additions. The root and paper READMEs, article FIGURES,
E1a gallery and PROGRESS belong to the parent for this request and are untouched.
This explicit ownership instruction supersedes the usual local PROGRESS update.
The original attributes, validators, canonical RQs, source reviews, contracts and
outputs are preserved. No push, PR creation, publication or external setting
change occurred here.

These figures add visibility to reviewed QC, not extra biological findings.
Libraries remain technical records with unknown animal IDs/independence; X1
dimensions overlap and annotation release remains unknown. Original R2/R3 and
all biological execution holds remain in force. Next: parent independent review,
navigation/status integration and its separately authorized publication follow-up.
No human scientific acceptance is inferred from execution or mechanical checks.
