# Zh26-P01: stepwise analysis plan, version 1

10 November 2026. **Reviewed planning specification, not a frozen execution
contract.** No numerical run or scientific acceptance is recorded.
[Source review](SOURCE_REVIEW.md) · [paper review](PAPER_REVIEW.md) ·
[literature context](LITERATURE_CONTEXT.md) · [handoff](REVIEW_AND_HANDOFF.md).

## Purpose, comparison and exposure

The biological purpose is to understand the evidence for local immune
regulation of NK antitumor responses. The immediate measurement question is:
which of the paper's reported NK RNA contrasts can be reconstructed, and how
much does the conclusion depend on the discrepancy between methods and code?

Two main contrasts are ITDT minus PBS and ITDT+aCD4 minus ITDT in sorted tumor
NK preparations at the paper's RNA collection time. Released-code reproduction
also retains ITDT+aCD4 minus PBS because the source exports it.
The endpoint is a source-model difference in transcript abundance.
The unit is a pooled preparation/library, with reported experimental replicate
as a block. Neither constituent mice nor genes increase biological replication.

Exposure is explicit: the owner read the paper, and the planning agents inspected
reported outcomes, figures, methods, source code and neighboring results.
Source-derived gene panels and pathways are exposed choices. Future freezing
preserves implementation choices but cannot make this independent confirmation.

The chief technical threat is that different inputs/versions yield superficially
similar plots. Selection and recovered NK-state composition limit biological
interpretation even after a successful replay. The informative outcomes are
reproduced, method-sensitive, numerically discordant or not estimable from the
qualified inputs. All remain reportable; none triggers an automatic search for
a favorable gene or a new dataset.

## S0 — source identity, input qualification and runtime

**Type:** metadata recovery. Register a versioned Zh26-P01 contract before
scripted qualification. The source inventory is a starting list, not a passed
preflight.

1. Acquire immutable author files at commit
   `61ac9a440ba3f9db754ff8b8ad5008b450e647c0`; save URLs, retrieval dates,
   exact bytes and SHA-256 hashes in ignored raw data. Preserve originals.
2. Refresh GEO SOFT, compare with the saved snapshot, and inspect the deposited
   supplementary matrix. Verify GEO/GitHub identity and abundance semantics;
   do not infer counts from a filename or construct counts by rounding TPM.
3. Build and verify a one-to-one GSM/sample/condition/replicate crosswalk.
   Inspect missing/duplicate identifiers, finite nonnegative values, feature
   names and orientation. Establish whether raw inputs, published tables and
   displayed panels refer to the same analysis version.
4. Record pooling, experimental-day structure, potential shared animals and
   unknown metadata separately. No unverified pairing or animal identity.
5. Locate the article supplements/data files and any archive identifier using
   publisher, repository and version records. Record each access outcome.
   Review discrepancy rows; do not contact authors without explicit instruction.
6. Inspect available R/Python runtimes and the README's package versions.
   Preserve package/gene-set versions; test needed dependencies and the source
   API surface before declaring replay feasible.

**Deliverables:** source manifest, sample crosswalk, discrepancy ledger,
runtime report and source-qualified stage dispositions under the repository
runner. **Decision:** allow S1/S2 for a qualified TPM source; allow a count
sensitivity only with qualified counts and annotation. Unknown animal membership
does not prevent metadata work. Ambiguous sample mapping blocks dependent
contrasts, not the literature review.

## S1 — reproduce the released RNA implementation

**Type:** exposed reproduction. Freeze a separate contract and hash-bound
entrypoint before calculation. Use the actual TPM filter, transformation,
block design, contrasts and limma-trend implementation identified in S0.
Retain every included/excluded feature and source reason.

Check sample-name joins and design rank explicitly. Inspect per-library profiles,
PCA and block/treatment balance as diagnostics; PCA separation is not a
hypothesis test. Recreate differential-expression output tables before styling
figures. Check all shared genes against the authors' deposited output values
using a numerical tolerance justified by serialization and runtime precision,
declared before comparing outputs. Record missing/excess genes and maximum
discrepancies instead of selecting matching examples.

Reconstruct the fixed published marker/granzyme panels with their actual
gene membership, replicate correction and scaling. Keep individual pooled
preparations visible alongside any source group averages. Map figure filenames
to final paper panels by content. Log exact package versions and all adaptation
needed to replace IDE-only paths or output locations.

**Deliverables:** all three contrast tables, inclusion report, sample diagnostics,
panel crosswalk, output-comparison report and figures.
**Decision:** concordance establishes released-code reproduction only.
Disagreement requires tracing input/filter/design/version differences before
advancing a claim. No source output is overwritten.

## S2 — reproduce the released enrichment analysis

**Type:** exposed reproduction; depends on qualified S1 output.
Pin the source gene sets and both scripts. Preserve executable logFC ranking,
AveExpr restriction, identifier case rules, universe, seed and pathway-size
settings; distinguish misleading comments from executed code.
Check duplicates introduced by identifier conversion and record pathway coverage.

Compare the authors' exported enrichment results and leading edges, retaining
the full tested pathway family and its multiplicity correction.
Display IL-2/STAT5, TNF/NF-kappaB and IFN-gamma panels because the source selected
them, not because a new screen ranked them favorably.

**Decision:** reproduction supports a transcript-set association, not direct
IL-2 secretion or STAT5 activity. Those claims rely on separate paper assays.
A gene-set-version failure is an exact-replay limitation; a current-version
rerun must be labeled an adaptation.

## S3 — bounded robustness after source reconciliation

**Type:** exposed sensitivity analysis; use a new frozen contract with decisions
made before inspecting sensitivity outputs.

- Examine leave-one-experimental-block-out stability of effect directions and
  magnitudes. These few-block diagnostics are not population confidence
  intervals or a basis for a new significance threshold.
- Assess a prespecified alternative enrichment ranking based on the signed
  moderated statistic, retaining the same qualified universe where possible.
  State why the alternative answers a ranking-dependence question.
- Only if S0 qualifies count-scale inputs and their annotation/length treatment,
  specify an appropriate count-based model separately. Do not call an inferred
  approximation exact published-method reproduction.

Report the two main contrasts and all fixed source panels, including discordant
or null patterns. Do not interpret correlation between the two contrasts as
independent replication: they share the ITDT group. Opposite signs or a return
toward PBS are descriptive response patterns, not formal proof of rescue or
mediation.

**Decision:** stable, mixed or sensitive outcomes narrow measurement confidence.
No arbitrary robustness percentage, effect margin or sample-size claim is
invented. Stop if further alternatives cannot change a stated interpretation.

## S4 — connect RNA to functional evidence

**Type:** source-grounded synthesis; can proceed without S3 or numerical
functional reanalysis. Keep RNA, protein, signaling, lysis, tumor volume and
toxicity as separate endpoints in the existing evidence map.

If S0 recovers relevant data files, qualify assay units and cross-panel cohort
reuse before specifying any numerical reconstruction. Tumor measurements across
days remain within mouse; assay triplicates remain technical; pooled sorts stay
pooled. The available RNA is not a paired multilevel mediator dataset.

Inspect actual Figure 5 endpoint labels and Figure 6J gating ambiguity before
extracting values. Preserve the CD107a non-increase and the separate functional
killing result. Missing raw FCS or worksheet identities limits the dependent
reanalysis; it does not erase the source-grounded discussion.

## S5 — synthesis and next-question decision

Deliver a compact result/figure guide with one disposition per stage, exact
receipt/contract links, all discrepancies and negative findings. Explain what
the work changed about confidence in the RNA evidence and what remains supported
only by the source experiments.

Revisit the local literature context only if the comparison changes.
A new biological question needs a specified unresolved link and an informative
comparison beyond the published circuit. There is no automatic target ranking,
canonical RQ allocation, wet-lab package or portfolio-wide extension.
Retain A33–A35 and all prior evidence unchanged.

## Execution and validation requirements

Follow the current research governance: register the article owner and contract;
preflight exact inputs; freeze and commit the contract and code; run through
`analysis/scripts/research_gate.py`; verify the receipt; then interpret.
Metadata, reproduction and sensitivity stages retain their distinct exposure
and inference limits. The technical chat may make necessary local freeze commits
after checking author and committer identity. Publication/merge is not part of
this handoff.

Independent numerical checks must verify joins, contrast arithmetic and output
comparisons; they are not biological replication. Run repository-required
tests/checks and base-aware governance against refreshed origin/main.
Keep raw sources and prior results immutable; update PROGRESS with exact next
steps and access/runtime settings. No governance or validator weakening is allowed.
