# Human continuation validation and handoff

29 October 2026. Completed scope: the separately permitted, exposed human
observational continuation and its bounded external RNA comparison. Execution
and technical review are complete; scientific acceptance is not assessed.

## Frozen execution

| Stage | Freeze | Actual disposition |
|---|---|---|
| Primary donor/assay qualification | `952ea40` | Executed;78donors,107nested libraries, exact barcode order |
| Public age/recorded-sex supplement | `8ddc8e0` | Executed; exact joins for all78donors |
| Primary donor-aware RNA | `aad1d86` | Executed;692,789,348raw entries, every cell's UMI/detection parity;27,545independent arithmetic checks |
| External qualification v1 | `c431f1e` | Failed before raw reading; historical preparation-code hash mismatch, no outputs fabricated |
| External qualification v2 | `9982774` | Executed;338,061,955raw entries,85cached units;29mapped genes and all-gene totals match current raw RNA, not SCT; SELENOP exact-map hold retained |
| External nine-gene description | `d4ee3cb` | Executed;12IPF/9Control donors,12contrasts,4estimated and4non-estimable correlations;184independent checks |
| Diagnostic/source preservation | `4683a36` | Executed;7files copied byte-for-byte; original qualification stays failed |

[Primary receipt](../../analysis/research/runs/DY1_human_observational_v1/receipt.json),
[external receipt](../../analysis/research/runs/DY1_external_human_observational_v1/receipt.json)
and [preservation mapping](../../analysis/research/runs/DY1_human_evidence_preservation_v1/preservation.json)
record exact code, inputs, outputs and hashes. All previous source-v1/v2 evidence
is unchanged. The independent coordinating reviewer checked frozen contract/code
blobs and declared output hashes for both numerical runs and inspected all three
figures. Its review found no blocking scientific-interpretation issue. This is
technical review on the same data, not independent biological replication.

## Required checks

- Repository unit suite: **161 tests, one skipped**, pass.
- Targeted human synthetic tests:27passed across donor qualification(5), clinical
  joins(4), primary statistics/aggregation(11), external qualificationv1/v2(2each)
  and external aggregation/missing-gene/identity cases(3). Valid prior checks
  were reused; no biological analysis was rerun for documentation edits.
- Repository compile check passed; added preservation script separately compiled.
- Claim contract:18numeric bindings passed.
- Nb1 output, Nb4 archive, A16 stage1, A23 external and A22/A23 extension evidence
  verifiers all passed.
- Repository validator: **11,432 checks passed** on the final artifact set.
- Base-aware research gate: **passed** against freshly fetched
  `origin/main` = `78320a186b6f52426e7c7c5349a2f26492b718b7`.
- Git diff whitespace check passed for edits. Two trailing tab fields in the
  frozen primary donor-context TSV represent legitimate missing final values;
  that receipt-bound file was preserved exactly rather than trimmed.
- All32canonical questions remain registered and unchanged in this analysis
  worktree. No existing frozen scientific code/result, claim grade, validator,
  schema, governance or root `.gitignore` changed.

## Failures and corrections retained

The external qualification v1 stderr reports `Historical preparation code
changed`; the runner also records missing expected output because execution
stopped before writing tables. The exact historical Git blob at `02ff8b6`
matches the preparation record. The subsequent `8d6990f` change only migrated
repository paths. V2 binds the historical blob as evidence without executing it;
the original failure and its contract remain preserved.

Draft preflight failures were corrected before numerical execution: missing
amendment fields, non-schema embedded selection/source manifests, and missing
discovery/validation role bindings. The final schema-compatible manifests and
explicit source units passed preflight; no validator was relaxed. A mistyped
preflight file path did not execute any analysis. Tool records preserve these
draft-check responses; successful frozen execution receipts are authoritative.

The first final repository check found two old README anchors broken by a heading
change. Restoring the historical heading fixed them without editing the archived
reports. The first base-aware gate rejected a failed receipt in the success-only
registry and an unregistered copied discovery JSON. The existing Nb5 failed-run
preservation pattern resolved both: a new metadata-only run copies every byte,
records original→archive mappings, and registers success of **preservation only**.
The [archived failed receipt](../../analysis/research/runs/DY1_human_evidence_preservation_v1/failed_receipt.json)
still says `execution_failed`. No failed result was relabeled successful.

## Preservation and local settings

Original failed files remain locally and at commit `9982774`; original discovery
copies remain locally and at `d4ee3cb`. Canonical diagnostic/source copies are now
tracked, receipt-bound outputs in `DY1_human_evidence_preservation_v1`. Only these
newly created duplicate index entries were removed after verifying archive hashes.
All original local bytes were checked again after index removal.

The reviewer approved two exact **local** Git excludes in
`X:/GitHub/ravel/.git/info/exclude`:

```text
/analysis/research/runs/DY1_external_human_qualification_v1/
/Research Article/gate2_DY1_damani_yokota_2026/source_metadata/external_human_v1/independent_human_candidates.json
```

No broad ignore rule or tracked `.gitignore` change was made. Ignored primary
source hardlinks remain immutable; external public inputs remain copies. No
checkout, raw input, unrelated staged/untracked work or history was removed.
No external publication, service write or remote setting changed.

## Remaining scope and next step

The [primary report](HUMAN_RESULTS.md), [external report](HUMAN_EXTERNAL_RESULTS.md)
and current [article ledger](README.md) separate completed measured RNA findings
from remaining holds. Exact author NAM clusters/model are unavailable; the full
external requested gene set has a SELENOP identity-marker mapping hold. External
Vanderbilt and recipient correlations below the fixed donor minimum stay
unestimated. Clinical covariates remain only partly qualified. None of these
limits turns RNA into activity, secretion, fate or a causal recipient effect.

The original mouse/infection numerical stages remain unexecuted under the
platform restriction, and full mechanistic stage8 integration remains incomplete.
No restricted rerun, extra cohort search or threshold relaxation is queued.
The owner-authorized coordinating review will integrate this stable handoff with
its six reviewed RQ-local context notes and review navigation, then validate
those documentation changes without biological reruns. Existing hypotheses,
unfavorable evidence and human scientific-decision authority remain unchanged.
