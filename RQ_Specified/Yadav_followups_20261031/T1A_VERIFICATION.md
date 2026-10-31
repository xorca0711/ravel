# T1-A verification record

31 October 2026. Both runner receipts record successful execution from frozen
commit `5e1d7dbbfac8ae3ba41046b1b3542e1cec5d716c`, with all 13 expected outputs
across the two runs. See [results and receipts](T1A_RESULTS.md).

Before freeze, both input preflights and Python compilation passed. Ten
synthetic checks exercised fraction/percent scaling, failed closure, zero
total, retained negative/NaN/formula values, no partial-n summary, and arithmetic
means/ranges. Fixtures contained no newly observed source outcomes.

The frozen [independent verifier](scripts/verify_t1a_v1.py) completed **6,306
checks, all passing**, after execution. It used bundled openpyxl 3.1.5 rather
than the runner's ZIP/XML parser, and `math.fsum/min/max` rather than Decimal.
It checked the exact authorized cell set, source values/types/headers, four
suffix observations, summary counts and arithmetic, independently evaluated
fraction closure/scale and holds, and checked all eligible R1 differences.
B1 checks retain the unresolved native-label condition key. Source SHA-256
matched. This is independent numerical verification of the same source, not
independent biological replication.

| Run | Literal cells | Summaries | Held summaries |
| --- | ---: | ---: | ---: |
| R1 | 1,440 | 360 | 95 |
| B1 | 144 | 36 | 0 |

The saved machine-readable verifier result is
`t1a_independent_verification.json` in the local staging directory
`C:/Users/dream/.codex/visualizations/2026/10/30/01a18ba9-2ee9-72d0-a6f0-2c77bf838a75/`.
It records `ok: true`, the check count, table counts and method. The verifier
is bound as code by both contracts; it does not write into either frozen run.

Both PNGs were inspected, and both PDF files were independently rendered with
pypdfium2 and inspected. Each PDF has one page (R1 864×1008 points, B1 864×648).
Axes, units, condition labels, points/ranges and held-panel notices are visible
without clipping or overlap. Source panels/metabolites were not removed to
improve apparent results. The R1 caption explains its conservative whole-panel
display hold for the partly qualified 4D argininosuccinate block.

Repository/current-main checks and preservation results are recorded in the
[execution ledger](EXECUTION_LEDGER.md). Unchanged prior tests were reused;
no historical biological analysis was rerun. Missing cells and strict closure
failures are retained analysis outcomes, not verification failures.
