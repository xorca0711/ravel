# S5M v1: preserved execution with an aggregate-flag defect

18 November 2026. Owner `Nk17-P01`. Executed from frozen setup
`03d42af5d5eb0b5e259c35871988c802c819b73f` under the
[v1 method](S5M_METHOD_V1.md) and
[contract](../../analysis/research/contracts/Nk17-P01.s5m_molecular_integration_v1.json).
This version is **not accepted**: coordinator review identified a semantic error
in an aggregate warning. The [v2 amendment](S5M_AMENDMENT_V2.md) owns the bounded
correction; all v1 code, outputs and receipt are preserved unchanged.

## What ran and what failed review

The [receipt](../../analysis/research/runs/naik2017_s5m_molecular_integration_v1/receipt.json)
records successful execution. The exact-ID outer join retained 47,729 genes;
the frozen primary/all-mapped universes contain 11,007/21,775 genes and
11,005/21,760 unique anchors. All 312 coefficients and 96 covariance identities
were produced. The separate v1 verifier passed 18,810,969 arithmetic/copy checks,
with maximum scaled error `2.95025e-16` and covariance identity error
`2.77556e-17`. Receipt integrity passed. These checks did not establish the
correct semantics of every field.

`s5m_integrate_v1.prepare` selected every source field containing `zero` for
`rna_any_zero_flag`. That included S4's W6/W12
`adjustment_range_includes_zero`, which describes a contrast range, not an
expression count. The verifier independently recalculated values but repeated
the same field-name heuristic. Its pass therefore failed to detect this semantic
bug. The reported 9,966 primary genes and all five anchor flags must **not** be
read as count-zero prevalence. The v1 summary and anchor figure are historical
defective displays, not current interpretation.

Static data-flow inspection shows that this aggregate is used only for warning
summaries and anchor displays, not eligibility, weighting or coefficient
calculation. A bounded correction will prove that the full association/covariance
tables, ATAC table and Figure 1 are byte-identical, while checking every unchanged
gene/anchor source field. This report does not assume that the v2 verification
has already happened.

## Preserved evidence and limits

- [Full joined table](../../analysis/research/runs/naik2017_s5m_molecular_integration_v1/gene_join.tsv.gz)
  and [ATAC table](../../analysis/research/runs/naik2017_s5m_molecular_integration_v1/gene_atac.tsv.gz).
- [All associations](../../analysis/research/runs/naik2017_s5m_molecular_integration_v1/association_results.tsv)
  and [covariance components](../../analysis/research/runs/naik2017_s5m_molecular_integration_v1/covariance_identity.tsv).
- [Original summary](../../analysis/research/runs/naik2017_s5m_molecular_integration_v1/universe_summary.json),
  [anchor manifest](../../analysis/research/runs/naik2017_s5m_molecular_integration_v1/anchor_manifest.json),
  and [v1 verification](../../analysis/research/runs/naik2017_s5m_molecular_integration_v1/verification.json).

Entrypoint time was 174.344 seconds; all run files total 43,743,645 bytes.
There was no failed real execution. The failure was semantic review, and it
requires a versioned correction rather than editing the completed run. Source
analyses, source units, expression qualification, prior exposure and all
interpretation limits remain unchanged. Gene-feature association supplies no
same-cell regulation, independent replication, protein/activity endpoint or
causal chromatin-to-repair link. Return corrected actual outputs for coordinator
review before S5F; no scientific acceptance follows from this preservation.
