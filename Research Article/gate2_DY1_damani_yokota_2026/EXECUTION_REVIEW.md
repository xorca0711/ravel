# NAM execution checkpoint review

**Date:** 29 October 2026
**Status:** source checkpoint reviewed; requested biological analyses remain unfinished

## Summary

The owner-authorized execution chat `01a18767-874c-7680-a521-69f6a59757ee`
(**Execute NAM memory paper analyses**) started from review commit `a0e7472`.
It froze source contract `DY1-P01.source_v1` at `a2ae09e` and executed a metadata
audit. Its first turn then ended with a platform biology-content restriction,
recorded as `systemError` / failed turn. This was neither a numerical result nor
a demonstrated data limitation. The reviewer requested documentation-only
close-out, with no retry of the restricted analysis.

## Scope and independent checks

- Read the frozen source script and its saved qualification output, retrieval
  record, contract interpretation fields and receipt provenance. This checkpoint
  estimates no biological effect and establishes no mechanism.
- Compared parsed registry objects at `a0e7472` and `a2ae09e`: the only semantic
  additions were article candidate `DY1-P01` and its source contract. Existing
  canonical questions and contracts were unchanged; much of the textual diff
  was formatting.
- Independently inspected the four compressed CMO reference files and the
  non-expression feature rows in all four expression feature tables. This was
  source-label verification, not a new expression analysis or replication.
- Confirmed the two corrections below and sent them to the execution chat before
  close-out. Frozen outputs and scripts must remain intact, with the corrections
  documented as superseding their affected interpretations.

## Corrections and limits

1. **Blank naive CMO labels are a parser artifact.** The naive reference column is
   `multiplexed_sample `, with a trailing space. The v1 parser looks up the
   untrimmed name `multiplexed_sample`, producing blank labels. Reading the actual
   source shows CMO301-303 labelled naive. CMO304-306 in the trained baseline
   reference carry the trained label. This correction does not establish whether
   each tag represents a mouse or a pool.
2. **Baseline condition/library confounding is unresolved.** Both baseline
   expression feature tables contain CMO301-306. Feature presence alone cannot
   distinguish mixed-condition cells from ambient tags or unused feature rows.
   The source_v1 assertion of one condition per expression library must therefore
   be superseded by an unresolved assignment statement. The planned tag-count
   audit was not executed. Reused challenge tag identifiers are library-specific
   and cannot identify the same animals across libraries.
3. **ATAC processing versions differ.** GEO describes an edgeR-based workflow;
   the paper describes DiffBind/DESeq2. Deposited narrowPeak intervals are not
   consensus read counts. Neither a peak-presence comparison nor a metadata audit
   reproduces the paper's differential-accessibility analysis.
4. **Bulk RNA files contain exon-bin identifiers.** Summation by gene prefix
   cannot silently be called unique gene-fragment counting. Exact counting
   semantics and the author pipeline need recovery or an explicitly qualified
   alternative before interpretation.
5. **Animal/pool identity remains unverified.** GSM identifiers, CMO names and
   nominal replicate numbers do not by themselves establish independent animals.
   Code Ocean returned HTTP 403; inaccessible code is a source-access limit,
   not evidence that a particular biological result is false.

## Completion and ownership

Only the source-metadata checkpoint ran. Stage 0 has unresolved source identity
and unit questions. Numerical components of stages 1-7 were not executed after
the platform restriction; stage 8 cannot provide results-based integration.
Completed source-reading and design-audit components remain credited as review
work, including the ARG1 comparator audit and regulatory precedents. Planned
comparisons must not be marked completed or converted wholesale into data
limitations. The article README owns the current stage ledger.
No TF activity, causal ARG1 mediation, memory maintenance, human disease effect
or mature epithelial repair result was generated.

The paper package belongs under `Research Article/gate2_DY1_damani_yokota_2026/`.
No new results exist to place under existing RQ folders. The reviewed links to
A1/A2/A8/A14/A19/A22 remain proposed connections and preserve their current
hypotheses, negative findings and decision authorities. The original review and
literature context remain the scientific plan; this note reports execution status.

## Next steps

- Preserve the execution checkout and ignored source cache with the committed
  source receipt; do not retire the checkout while it holds needed inputs.
- Use the documented CMO corrections when assessing source eligibility; do not
  treat library titles or tag names as a verified animal/condition map.
- Keep remaining numerical steps explicitly unexecuted. Source/measurement
  limitations and the platform execution restriction have different causes and
  must remain separately visible.
- Human scientific acceptance remains unassessed. Repository validation checks
  provenance and consistency; it cannot establish a biological mechanism.
