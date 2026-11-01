# E1a execution and handoff

31 October 2026 (Asia/Seoul).

- Worktree: `C:/Users/dream/.codex/worktrees/saxton-metadata-recovery-20261031/ravel`.
- Scoped branch: `codex/saxton-recipient-description-20261031`, created from
  plan commit `19b6a9c` after confirming a clean working tree.
- Numerical freeze: `5fbe78ff44d096b173394e8bdae314e7268d3c60`.
- Numerical results preservation and rendering freeze:
  `56da56e18ef8304a16c3153ad136c36b13dca7dd`.
- Fresh integration base: `4df267d3f5035b249df2e587c70a8b9e9253b049`.

## Source, exposure and execution

[C0](C0_QUALIFICATION.md) qualifies exact bytes, fields, symbols and label/source
joins. No count values were read during C0. Historical source outcomes and labels
were already exposed. Both contracts are descriptive, with scientific acceptance
not assessed. No independent animal-level design was inferred from pooled cells.

Ten synthetic endpoint/provenance/plot tests passed before the numerical freeze.
Synthetic visual review found color bars shortening two panels; this was fixed
before freeze and a vertical-alignment assertion added. The affected plot test
passed again, and the corrected synthetic figure was visually inspected.
Two additional display-rule tests passed before the separate render-v2 freeze.
The original source pipeline and X1–X3 were not rerun.

Both input preflights, both runner executions and both receipt verifications
passed. Each run used a fresh directory and exact committed code/contract hashes:

```text
python analysis/scripts/research_gate.py preflight "Research Article/gate3_08_saxton_2021_il22/recipient_context_v1/config/description_contract_v1.json" --inputs
python analysis/scripts/research_gate.py run "Research Article/gate3_08_saxton_2021_il22/recipient_context_v1/config/description_contract_v1.json" --run-id sx22_e1a_recipient_description_v1
python analysis/scripts/research_gate.py verify analysis/research/runs/sx22_e1a_recipient_description_v1/receipt.json
python analysis/scripts/research_gate.py preflight "Research Article/gate3_08_saxton_2021_il22/recipient_context_v1/config/render_contract_v2.json" --inputs
python analysis/scripts/research_gate.py run "Research Article/gate3_08_saxton_2021_il22/recipient_context_v1/config/render_contract_v2.json" --run-id sx22_e1a_render_v2
python analysis/scripts/research_gate.py verify analysis/research/runs/sx22_e1a_render_v2/receipt.json
```

Execution used Python 3.12.10 ARM64, h5py 3.16.0, NumPy 2.5.1, SciPy 1.18.0
and Matplotlib 3.11.1. The isolated h5py location was supplied through process-local
`PYTHONPATH=.tools/sx22_e1a_runtime`; no global Python installation was modified.
The scripts otherwise use ordinary imports and record package versions.

## Independent numerical and presentation checks

A separate read-only verifier imported neither frozen entrypoint nor its helper
functions. It checked 12 numerical-run input/code/output hashes plus the contract,
read the HDF5 CSR buffers directly, and compared all 23,366 selected cell counts
and all 11,683 cell totals with the emitted audit CSV. Original ordered cell IDs,
library/label joins and all 24 observed composition strata agreed. Separate
integer aggregation reconciled every endpoint/count bin in all 78 stratum/gene
rows, including all 18 empty rows and the overlapping aggregate denominators.
Local checker: `.tools/sx22_e1a_verify.py`. These are arithmetic checks, not a new
biological analysis or replication.

The originating reviewer independently reported the same hash, raw-CSR, cell-total,
78-row and 18-empty-row agreement. It also reviewed the code's count formulas,
label retention, missingness and source joins. Its separate v2 review passed the
contract/bound hashes, all 78 display rows, the four small-positive annotations,
SVG XML and visual legibility/alignment. Final handoff review/integration remains
separate from human scientific acceptance.

The actual v1 and corrected v2 figures were visually inspected. V2 preserves row
alignment, literal labels and explicit denominators, and distinguishes four
small-positive annotations from exact zeros. A separate display audit compared
all 156 measurement annotations in 78 rows against the unchanged numerical CSV.
Both SVGs parse as XML and match their receipt hashes; all five embedded matrix/
color-scale images are byte-identical across versions. Only annotation/caption
presentation changed. The [amendment](RENDER_AMENDMENT_V2.md) records exposure
and supersession without overwriting the original run.

## Required repository checks

Checks against freshly fetched `origin/main` at the revision above:

| Command | Result |
|---|---|
| `python analysis/scripts/validate_repository.py` | 12,752 checks passed |
| `python analysis/scripts/research_gate.py check --base origin/main` | Passed: `ok=true`, no errors |
| `python -m unittest discover -s analysis/tests -q` | 158 tests; two Windows symlink skips; passed |
| `python -m compileall -q -x '[/\\]\.tools[/\\]' analysis "Research Article" RQ_Specified` | Passed |
| `python analysis/scripts/claim_contract.py --check` | 18 numeric bindings passed |
| `python "Research Article/gate1_03_nabhan_2018/nb1/verify_outputs.py"` | 17 output hashes and provenance checks passed |
| `python "Research Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/scripts/verify_archive.py"` | 20 run records and 164 output hashes passed |
| `python RQ_Specified/A16_cd177_state_attribution/scripts/verify_stage1_evidence.py` | 1,867 checks passed |
| `python RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/08_verify_external_current.py` | Passed |
| `python analysis/scripts/verify_a22_a23_extensions.py` | Passed |

No biological analysis was rerun for these checks. Logs are retained locally in
`.tools/sx22_e1a_validation/`. A mechanical scope check verified the 30 changed
paths against plan commit `19b6a9c`: only the new E1a package/runs and the three
authorized navigation/registry files changed. Removing the added navigation
paragraph/section recovers the original article README and E1a plan bytes exactly.
Removing the two new contracts, two receipts and one evidence link recovers the
original registry object. Frozen E1a code, contracts, tests and numerical run
remain identical to their committed versions. Authored-file whitespace checks
passed with the named generated-SVG exception below.

## Exceptions and retained limitations

The C0 temporary reader's CSV field-name mismatch was corrected before completing
the join; source data did not change. The initial Python environment lacked
h5py; an ordinary isolated binary-wheel installation resolved it. No new content
restriction occurred, and the original service restriction is not claimed lifted.

An unfiltered `git diff --check` reports 54 trailing-space lines in each generated
SVG: `analysis/research/runs/sx22_e1a_recipient_description_v1/recipient_transcripts.svg`
and `analysis/research/runs/sx22_e1a_render_v2/recipient_transcripts_v2.svg`.
These are Matplotlib path-formatting bytes. The originating reviewer explicitly
approved preserving them and checking authored files separately, excluding only
these two named generated artifacts. XML and receipt checks passed. Root
attributes, validators and governance are unchanged; no check was weakened.

All source reviews, old contracts/output bytes, X1–X3, canonical RQs and hypotheses
remain preserved. Original Saxton WT/variant work, R2/R3 holds and unqualified
persistence/function joins remain held. No push, PR mutation, main merge, author
contact, Notion edit, new cohort search or human scientific acceptance occurred.
Next: originating review and any authorized local integration of this bounded
descriptive result. There is no queued expansion to obtain a positive pattern.
