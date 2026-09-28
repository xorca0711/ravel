# England review: architecture and revision record

**28 September 2026. Landing base: main at `27e281a`; scientific audit snapshots:
`bbfa4e7` / `d485507`.** The review incorporates the owner's request to rewrite
eight candidates, correct the repository structure where necessary, open a PR
and merge after checks. Publication authorization is not acceptance of a
scientific hypothesis or a new claim grade.

## Placement decisions

| Material | Current location and reason |
|---|---|
| Global question identities and current A16–A18 interpretation | `RESEARCH_QUESTIONS.md`; one canonical register, with a link to paper-local candidates |
| E-N1–E-N8 biological cards and supporting checks | `Research Article/gate2_C2_england_2025/CANDIDATE_HYPOTHESES.md` and `CANDIDATE_CHECKS.md`; paper-specific proposals with links to existing A questions |
| Performed audit and diagnostic evidence | This dated folder; source snapshots, saved numerical results and reproduction script stay together |
| Original candidate wording | `history/RQ_CANDIDATES.original.md`; preserved bytes, explicitly superseded |
| Future executable specifications | Relevant `RQ_Specified/A<id>_<topic>/` workspace only when a test is specified; no eight empty workspaces or duplicate global register |
| Current state and authority | Root `PROGRESS.md`, `AI_CONTEXT.md`, and appended `DEVELOPMENT.md` decision/revision records |

All four universal documents exist. Revisions add the missing top README claims
summary using existing status vocabulary and evidence, label the no-data
verification entrypoint, restore the standing progress-update rule at the top,
and correct the structure contract's stale A0–A14 limit to A0–A18 with proposal
status explicit. The full historical claim ledger remains canonical; the README
summary does not regrade it. Earlier dated handoffs are preserved below a current
notice so an unexecuted old checkpoint cannot override completed results.

## Scientific corrections carried into current documents

- A16: remove categorical depth-independence and consistent residual-priming
  claims. FU_A's frozen verdict is inconclusive; FU_C changed both population
  and pooling. The post-hoc same-population diagnostic retains two strata, with
  different priming results. Intrinsic biology and neighbourhood composition
  are not mutually exclusive.
- A17: state the biological founder-versus-continuum question before its
  simulator check. Preserve the confirmed code defect but separate it from
  source analytical fits and lineage evidence. Reconcile manuscript/archive
  units, parameters and switching schedule before the prospective refit.
- A18: keep the separate-control hypothesis conditional; pooled distance
  profiles cannot identify two mechanisms. Include the source's SPP1/DLK1 lead;
  RNA abundance and ligand class do not identify in-vivo range.
- E-N1: source Figure 4A already reports no detected size–composition relation.
  The rewritten hypothesis asks about broadly distributed identity loss and
  the contribution of tissue weighting; it does not advertise preferential
  expansion of altered clones as an established positive lead.
- E-N3/E-N5: model sampling and classification are enabling checks. A
  biological survival or maturation hypothesis can motivate each without
  calling the technical correction itself a new biological discovery.

Frozen contracts, result tables, original result reports and C-register grades
are preserved. The current opportunities ledger and paper README direct readers
to these corrections. The separately observed A16 Stage 0 worktree was not part
of the landing base and is not silently imported. No new atlas, stochastic
refit or external expression pilot was executed for this rewrite.

## Verification scope

The audit's previously executed numerical diagnostic is documented in
[evidence.json](evidence.json). [revision_manifest.json](revision_manifest.json)
records hashes of the preserved audit files and original candidate wording.
Landing checks cover Python compilation, the repository's evidence/provenance
unit tests, the generated claim contract, tracked Nb1 evidence and repository
artefact/link validation. These checks validate the documentation and evidence
contract; they do not validate the eight proposed mechanisms.

[Local validation results](VALIDATION.json): 53 tests (one existing skip), 18 numeric claim bindings, Nb1 provenance, compilation and repository validation passed. All eight preserved audit files match their recorded hashes. A scoped Git attribute preserves those bytes on checkout.
