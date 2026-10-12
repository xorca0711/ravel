# Weft intake

This is Ravel's collection of reviewed handoff packages from
[Weft](https://github.com/xorca0711/weft). Start here to find a paper's gate
assessments, review, limitations, disposition and exact evidence locations.
This is an ongoing trial integration, currently represented by the exposed Choi
pilot. Ravel remains the paper-driven omics research repository; Weft remains
the automation project. The collection does not replace article workspaces or
the research registry. Choi's scientific dossier has moved here from Weft; frozen
analysis evidence keeps its original location.

## Packages

| Package | Reviewed scope | Evidence status | Ravel disposition |
|---|---|---|---|
| [Choi 2020 / P001 / v1](choi-2020-p001/v1/README.md) | Previously read, exposed descriptive Figure 1 benchmark | Outputs published and hash-locked; four recovered labels, pAT2 absent | Owner retained the bounded discrepancy record; [#149 merged](https://github.com/xorca0711/ravel/pull/149); no new RQ or claim promotion |

No fresh-discovery candidate has completed the figure, supplement and dataset-use
review needed for a research handoff. Weft's held B4 candidate is not imported.

## What belongs here

Use `weft_intake/<paper-id>/<handoff-version>/` for a reviewed, public handoff:

- `README.md`: source identity, intended use, gate-by-gate assessment, unresolved
  limits, review authority and links to the canonical evidence.
- `manifest.json`: package identity, dated assessment, provenance, file hashes and
  locations. The first package is a documentary manifest, not an automated importer.
- Any additional public, redistribution-permitted review attachments, with their
  source, version, rights and hashes recorded. Link to restricted materials.

“Gate passed” always names the gate and permitted use. Reading priority alone
stays in Weft's decision buffer. A reviewed package can still have later gates
held or unperformed; arrival here does not authorize execution, accept a claim
or allocate an RQ. Scientific disposition and repository integration remain
separate, recorded decisions under the existing [research governance](../docs/RESEARCH_GOVERNANCE.md).
No new gate semantics, automatic transfer or scheduling is implemented here.

## Storage and preservation

| Content | Authoritative location |
|---|---|
| Weft handoff and evidence inventory | This folder, one versioned package per handoff |
| Published-source synthesis and study-specific analysis | `Research Article/<paper>/` |
| Execution receipts and materialized outputs | `analysis/research/runs/<run-id>/` |
| Public output download identity and member hashes | `analysis/research/published_outputs/` and the linked release asset |
| Registered questions, contracts and receipts | `analysis/research/registry.json` |
| Private screening stores and recovery checkpoints | Weft's private run storage and owner-only Drive backups |

Keep existing outputs in their original contract-bound paths. The handoff gathers
their locators and hashes rather than duplicating large matrices or moving frozen
evidence. Preserve earlier handoff versions; a correction or later review gets a
new version with a supersession reference. Repository-relative paths resolve from
the particular checkout root, which may be a worktree.
