# Return checklist — approximately 21 October 2026

This is a saved handoff, not a scheduled task. Read current Git/PR state on return;
the dates and commit references here are checkpoints, not a claim about future main.

## 1. Establish the current checkout and integration state

The audit branch is `codex/repo-readiness-audit-20261007`. Its local worktree is
`X:\GitHub\scRNA_seq\.worktrees\ravel-rename-20261007`. The primary path remains
`X:\GitHub\scRNA_seq`, also reachable through `X:\GitHub\ravel`.
PR #145 was merged into main at `cc5ce7e09bc03df49a982569236d572407ecb195`;
PR #140 is closed as superseded. This audit is a subsequent change.

```powershell
git status --short
git branch --show-current
git fetch origin
git log -1 --oneline
git log -1 --oneline origin/main
git worktree list
```

Use the merged audit if its PR has landed; otherwise inspect the audit branch/PR.
Preserve local changes. Do not restart work from an old plan merely because it is
open in the editor. Read [PROGRESS](../../../PROGRESS.md),
[AI_CONTEXT](../../../AI_CONTEXT.md), the [registry](../../../analysis/research/registry.json),
and the selected question's **current result/amendment before its plan**.

## 2. Select the work by the owner's question

All A0–A30 remain available. The [review ledger](QUESTION_REVIEW.md) lists their
current evidence and concrete qualification needs. There is no automatic next
RQ, preferred paper or instruction to obtain a positive result.

For continued Wang/Wagner 2025 work, read the
[current correction report](../../../Research%20Article/gate2_W2_wagner_Th17_PGAM/CORRECTIONS_2026-10-07.md).
Do not reuse old Compass negative-sign or subset-denominator human summaries.
For A30, use its [extension baseline](../../../RQ_Specified/A30_csf_compartment_effector_state/EXTENSION_BASELINE_V2.md):
qualify barcode/QC sensitivity, a justified null universe and common-state support
before stronger compartment claims. A29 needs an absolute metabolite/functional
discriminator; A28 needs a protein-level endpoint for competence. Reading and
design work can proceed without pretending these measurements exist.

For a new paper, establish source identity, accessible raw/supplementary data,
biological units, paper-local candidate, relation to existing RQs, exposed outcomes
and the decision the analysis could change. Follow the existing governance rather
than copying a previous paper's thresholds or forcing its biological rationale.

## 3. Check data and runtime before a new numerical run

Host runtime verified on 7 October:
`X:\GitHub\scRNA_seq\.venv\Scripts\python.exe` (ARM64 Python 3.12.10;
NumPy, pandas, SciPy, Matplotlib and openpyxl). The x64 virtualenv has a missing
base interpreter and was not used. The generic bundled Python lacks SciPy.
These are local observations, not portable environment guarantees.

The 21-file Wp cache is under
`X:\GitHub\scRNA_seq\raw_data\wagner_pgam_w2_20261004`.
The audit worktree exposes the same files with hard links (about 508 MB logical
size, no duplicate content allocation). Treat raw inputs as immutable: writing
through a hard link changes the same underlying file. No raw content was edited.
Other historical raw inputs are not all present in this audit checkout. Their
absence is an availability hold, not evidence of lost data or a license to fabricate it.

```powershell
& 'X:\GitHub\scRNA_seq\.venv\Scripts\python.exe' analysis/scripts/research_gate.py preflight 'path/to/new-contract.json' --inputs
```

Use a **new** analysis ID, versioned outputs, exact input/code hashes and an
honest exposure record. Freeze and commit before the runner. Never rerun a frozen
historical script onto its old outputs. A missing unit, endpoint or precision
justification restricts the permissible analysis; it need not block reading or
metadata recovery. Do not repair the gate by weakening it.

## 4. Verify and hand off

Run the exact checks in `.github/workflows/repository-checks.yml` and
`.github/workflows/research-governance.yml`; the [reproducibility guide](../../../REPRODUCIBILITY.md)
links their scope. Raw data are not needed for the ordinary tracked-file checks.
On this host, if sandbox temporary files fail, set `TEMP` and `TMP` to an existing
task-local `tmp` directory for the test process only.

For new analyses, verify units, joins, denominators, arithmetic and endpoint
interpretation independently of the generating code. Inspect measured figures
visually. Record failures and supersession, then update PROGRESS and the specific
paper/RQ indexes. Fetch main again before delivery. Open a scoped PR; a passed
run or CI job is not a human scientific acceptance or authorization to merge.
