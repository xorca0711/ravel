# Execution, verification and local handoff

1 November 2026. Scope: Sx22-P01 Q1-Q4 exposed finite-library description under
the parent-reviewed amendment. [Results and dispositions](RESULTS.md) ·
[Figures](FIGURES.md) · [Prospective methods](METHODS.md).

- Branch: `codex/saxton-program-description-20261101`.
- Local integration before implementation: `cf7586723af7f844505773c2dd6517798f1bd458`,
  incorporating the parent plan at `07c8752706eac10f6cc9a2f895f702a49c0d6d60`
  and eligibility commit `c9e9405b7ee6b3aeb8e691222ab57fc142a10d2c`.
- First, unexecuted v1 freeze: `ae4a3b4`.
- Executed v2 freeze: **`404d23673194abbb388668a2aa74e2ff09399579`**.
- One run: [sx22_program_description_v1](../../../analysis/research/runs/sx22_program_description_v1/receipt.json).
  Its `analysis_id` is `Sx22.program_description_v2`; run directory and contract
  versions intentionally differ after the pre-execution registration amendment.

## Pre-execution checks and corrections

Seven synthetic tests passed: full-library denominators and filter boundary;
mean-log contrasts/omission; missing/ambiguous symbol handling; unclamped beta
and empty/zero-denominator local holds; empty summaries; TMM identical-composition
library scaling; and three figure/XML/whitespace/no-overwrite checks. All three
synthetic previews were visually inspected before execution. The first attempt
encountered Windows sandbox temp-file PermissionError in two tests; the unchanged
suite passed using approved filesystem/runtime access. This was not a content
restriction and did not involve real source endpoints.

Initial input preflight passed, but the base-aware changed-asset gate reported:
`Unregistered scientific asset change: Research Article/gate3_08_saxton_2021_il22/reassessment_v1/sources/memberships_v1.json`.
The existing gate requires the authored membership configuration to be bound as
an execution dependency, not solely as an input. Contract v2 adds that binding
and the independent verifier, preserving the analysis methods and production
code. No validator, governance rule or infrastructure allowlist was changed.
No runner invocation or real endpoint calculation occurred under v1.

The first freeze's v1 contract had CRLF bytes that trigger the default whitespace
check. They were temporarily normalized to LF before v2 execution. At originating
review, the **exact original v1 blob was restored** from `ae4a3b4`, SHA-256
`0c47c9873e48a06c6f650e6840e0a6372928784de5846e75990ee3b037a2ac47`.
V1 is only the v2 amendment predecessor, not an input/code/output hash binding of
the executed receipt. Its restoration changes none of v2's bindings. V2's
amendment reason remains untouched as a historical record of the pre-run
normalization; this paragraph records the later restoration. No numerical output
was rerun or modified. Root `.gitattributes` is unchanged. The original v1 CRLF
contract is retained with a narrow whitespace exception. The two frozen R
capture logs have the additional line-ending issue described below; all other
changed files pass without an exception.

V2 input preflight and the base-aware gate passed before execution. All source
memberships, source values, methods, production code, tests and verifier were
committed before the one actual run. Prior paper/source exposure is explicitly
recorded; committing a new specification does not remove it.

## Numerical and visual verification

The runner executed successfully and recorded all 19 declared artifacts. The
receipt verification passed. Python 3.12.10 ARM64, NumPy 2.5.1, Matplotlib 3.11.1,
portable R 4.6.1 and edgeR 4.10.5 were used. No dependency installation occurred.
The 36 TMM factors cover all seven views; their exact values and versions are
saved in [normalization_factors.csv](../../../analysis/research/runs/sx22_program_description_v1/normalization_factors.csv).
R emitted the informational message `calcNormFactors has been renamed to normLibSizes`
once per view; exit status was zero and all factor checks passed. The original
stderr capture is retained. Child-process locale C does not change machine settings.

After staging the new run, the final whitespace check detected CRCRLF line
endings in `tmm_stdout.log` (37 lines) and `tmm_stderr.log` (seven lines): the
Windows R output was decoded then written by Python's newline-translating text
writer. The parsed factor table has exactly 36 records and the independently
verified values are unaffected. These already hash-bound capture logs are
preserved byte-for-byte. This corrects the earlier pre-staging whitespace check,
which did not include untracked run files. The final exception covers exactly
these two logs and the 143 CRLF lines of the original v1 contract, not a general
attribute or validator exemption. No numerical rerun or output cleanup occurred.

The frozen [independent verifier](scripts/verify_v1.py) imports no production
analysis or rendering code. It independently reconstructs source joins,
denominators, log-expression and group means, using `math.fsum` for amplitude
terms and `statistics.median` for memberships. It passed:

- All 30 input/code/output bindings, plus the executed contract hash.
- Every one of 35,275 source IDs, annotations, count-copy rows and primary values.
- All 319 exact membership mappings and all 100 overlap pairs.
- All 21 amplitude cases, 210 membership cases and 4,788 tested-gene cases.
- All 120 full-data/omission range records and fixed-universe checks.
- Direct contrast identity at maximum absolute error `8.881784197001252e-16`.
- All three SVG XML parses and prospective trailing-whitespace normalization.

Recorded TMM factors are checked for coverage, package version, positive
normalization and denominator consistency; this is not an independent
implementation of edgeR's TMM algorithm. The synthetic proportional-library
test provides a separate known-answer check. These are numerical checks of the
same source, not biological replication or human scientific acceptance.

All three actual PNGs were visually inspected. The 31 target labels, Cxcl1
asterisk, scale labels, background count/beta, ten membership labels and full-data
dots/omission ranges are readable without clipping. The wide Figure 6C sensitivity
is retained. No post-run figure edit or output rewrite was needed. Result tables
are mechanically transcribed from the immutable CSV values, with rounding limited
to display. Exact outputs remain available through the figure and result links.

```text
python -m unittest discover -s "Research Article/gate3_08_saxton_2021_il22/reassessment_v1/tests" -q
python analysis/scripts/research_gate.py preflight "Research Article/gate3_08_saxton_2021_il22/reassessment_v1/config/description_contract_v2.json" --inputs
python analysis/scripts/research_gate.py run "Research Article/gate3_08_saxton_2021_il22/reassessment_v1/config/description_contract_v2.json" --run-id sx22_program_description_v1
python analysis/scripts/research_gate.py verify analysis/research/runs/sx22_program_description_v1/receipt.json
python "Research Article/gate3_08_saxton_2021_il22/reassessment_v1/scripts/verify_v1.py" analysis/research/runs/sx22_program_description_v1
```

## Repository checks and ownership

Required checks are recorded below after final package integration.

Freshly fetched `origin/main` remained
`51d3b930b3805c616e67e414390ecf060647d090`. All checks below passed against that
integration base; no remote update required reconciliation.

| Check | Outcome |
|---|---|
| `analysis/scripts/validate_repository.py` | 12,911 checks passed |
| `analysis/scripts/research_gate.py check --base origin/main` | `ok=true`, no errors |
| `python -m unittest discover -s analysis/tests -q` | 158 tests passed; two expected Windows symlink skips |
| Python compile across analysis, Research Article and RQ_Specified | Passed |
| `analysis/scripts/claim_contract.py --check` | 18 numeric bindings passed |
| Nb1 archive verifier | 17 output hashes and provenance checks passed |
| Nb4 archive verifier | 20 run records and 164 output hashes passed |
| A16 Stage 1 evidence verifier | Passed |
| A23 external-current verifier | Passed |
| A22/A23 extension verifier | Passed |
| Scope/registry preservation | 37 changed paths; removing only two new contracts and one new receipt recovers the original registry object exactly |
| Original v1 and executed bindings | Exact first-freeze v1 blob restored; every v2 input/code/output binding unchanged |
| Report validation | 54 local links and reported all-view direction statements checked against frozen ranges |
| Whitespace after staging | Passed outside exactly three preserved artifacts: original v1 contract (143 CRLF lines), TMM stdout (37 CRCRLF lines), TMM stderr (seven CRCRLF lines) |

Logs are retained locally in `.tools/sx22_program_description_validation/`.
Required archive checks verified existing outputs; no old biological analysis
was re-executed. The seven targeted synthetic tests had already passed before
freeze and were not repeated after documentation-only changes.

The originating reviewer communicated a separate passing review in parent chat
`01a18687-3e55-7b51-b514-52f5f55a210b`: all 31 bound files including the contract,
all 35,275 primary rows, 21 cases, 210 membership summaries, overlap and omission
ranges. Its scratch verifier imports no production code and likewise checks
recorded TMM factors rather than independently implementing edgeR. It inspected
all three actual PNGs and confirmed readable, unclipped figures, retained wide
6C sensitivity and interpretation consistent with the outputs. This is technical
originating review, not a human scientific retain/reject decision.

Own changes are confined to the reassessment package, the one new run and two
contract/one receipt additions to the registry. Parent-owned README, literature
note, PROGRESS and top-level navigation are not modified by this execution task;
their integration is the parent's next step under the explicit scope allocation.
The earlier eligibility-note correction attributes the historical service error
to the parent's read of the original chat and quotes the exact excerpt.

All original analyses, root attributes, validators, canonical RQs, prior
contracts and archived runs remain preserved. No push, PR, external write,
publication, package installation or external account-setting change occurred.
Q5-Q8 retain the precise evidence/design holds in RESULTS. No current content
refusal occurred and no refused job was disguised or routed to a replacement
session. Next: originating review and parent-owned navigation/status integration;
additional scientific execution requires the corresponding missing evidence and
its own prospective scope. No acceptance or claim grade is promoted here.
