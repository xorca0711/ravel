# Exact tied-rank diagnostic — 8 November 2026

After the frozen v1 animal run, 12 reported comparisons differed by more than
0.001 from the predeclared primary calculation. Most involve ties; the
untied WT/control IFITM3 result also differs. The four chance t tests reproduce.
All v1 values, code, contract and figures remain unchanged.

The paper Methods P104 names R 4.2.2 and GraphPad Prism 10.2.0 without identifying
every panel's options. [GraphPad's official tie FAQ](https://www.graphpad.com/support/faq/for-a-mann-whitney-u-test-how-does-prism-handle-ties/)
explains its exact label-permutation calculation with tied ranks. The
[Prism 6 guide](https://cdn.graphpad.com/docs/prism/6/Prism-6-Statistics-Guide.pdf)
already documents exact treatment of ties; this is not assumed to be a new
Prism 11 feature. Documentation was read on 8 November 2026 after v1 results.

The v2 contract freezes a narrow arithmetic diagnostic across **all reported
direct comparisons**, not only discrepancies. It uses the same v1 source
observations and contrasts, with no exclusions, rounding changes or relabeling.
Integer dynamic programming counts all fixed-size label allocations of doubled
pooled average ranks. Report twice the smaller inclusive tail, capped at one,
and the alternative absolute-distance tail. These are explicitly distinguished.
Validate small allocations by full enumeration and SciPy's separate permutation
implementation. No Monte Carlo approximation or seed selection is required.

Agreement explains an implementation difference; disagreement remains an
unresolved source/test discrepancy. This is numerical verification using the
same exposed values, not new evidence, a new family of discoveries or biological
replication. The v1 source mean discrepancies and physical-unit limits remain.
