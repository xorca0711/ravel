# Numerical verification amendment: R1 v3

4 October 2026. Supersedes the execution attempts v1 and v2 without overwriting
their frozen contracts, code, receipts or output. The analysis is outcome-exposed.

The v1 run stopped at a pandas merge: SciPy supplied 32-bit integer cluster
labels on Windows, while the join expected 64-bit labels. Version 2 explicitly
casts identifiers to int64; this does not change grouping or statistical rules.

Version 2 then stopped at independent verification. The verifier incorrectly
assumed that a common translation preserved ties in finite-precision scores.
Recalculating an unshifted log and group mean with different arithmetic changed
U for 20/6,373 individual reactions and 8/1,722 metareactions. Maximum U
discrepancy was 683; maximum p and q discrepancies were 0.470431 and 0.478412.
Maximum standardized-effect discrepancy was 3.60e-11. The discrepancy is retained;
negligible effect-size error does not imply negligible rank-test error.

Version 3 preserves the exact float64 arrays submitted to the production tests.
The independent checker separately verifies the log transformation and common
shift to absolute 1e-11, then computes scalar pooled variance, rank-sum U,
tie/continuity correction, normal-tail p and BH on those exact arrays. The
original effect/U/p/q, expansion and clustering tolerances remain unchanged.
This corrects the target of verification; no failed tolerance is enlarged.
The old unshifted comparison is retained as a diagnostic in verification.json.

No production contrast, feature selection, clustering threshold, multiplicity
family or pathway rule changes between v2 and v3. Before this amendment, v2
summaries exposed 1,912 formed groups, 1,722 tested groups, 784 core groups and
20 pathways with both source-significant directions. These observations remain
exploratory. Unknown biological nesting and the difference from the manuscript's
1,911 total groups still restrict interpretation; a passed numerical checker
cannot establish exact manuscript reproduction or independent replication.
