# T1-B verification and preservation

31 October 2026. Numerical specifications/code were frozen at
`53a5f8f3cee36ed67eb87afdbf53017324ee6c74`; the layout-only amendment was
frozen at `a89b42c3b3c6a66adb71a327d3dea94e0d77b32e`.
[T1-B results](T1B_RESULTS.md) links all three receipts and expected outputs.

## Numerical checks

Both input preflights and code compilation passed before execution. Fifteen
synthetic endpoint checks passed: a valid channel with a missing neighbor;
invalid/missing target and no partial-n mean; explicit four versus three labels;
percent-domain versus area-domain distinction; no rescaling of 0.5%; unchanged
failed closure with separately describable valid channels; header holds;
complete zero vectors; negative and formula handling. Prior unchanged parser
and T1-A tests were reused, not replayed as another biological analysis.

The frozen [independent verifier](scripts/verify_t1b_v1.py) passed **17,841
checks** using openpyxl source reads and `math.fsum/min/max`, separately from
the execution parser's XLSX XML reads and Decimal arithmetic. It checks exact
source-cell membership, literal unit/isotope/sample maps, percent domains,
full supplied counts, all summary/difference arithmetic and missing-target holds.
It independently checks complete sums/residuals versus explicitly incomplete
subtotals and the unchanged numerical tolerance. All 120 original R1 QC records
are equal to their retained v1 records, including every failed closure; the
original QC file hash matches. No old hold was recomputed away.

| Run | Source cells | Summaries | Held summaries | Vector QC rows |
| --- | ---: | ---: | ---: | ---: |
| R1 companion | 720 | 180 | 20 | 120 |
| R2 | 2,072 | 548 | 84 | 94 |

Results are saved as `t1b_independent_verification.json` in
`C:/Users/dream/.codex/visualizations/2026/10/30/01a18ba9-2ee9-72d0-a6f0-2c77bf838a75/`.
The checks independently verify arithmetic on the same source; they do not
create independent biological replication, validate correction/normalization,
or establish population uncertainty.

## Figure QA and correction

All initial PNGs were inspected. Crowded R2 titles and edge-positioned held
marks justified a versioned layout correction. The original successful runs,
figures, numerical code and verification are retained. The v2 plot script uses
only source/summary/vector CSVs and stored endpoints; no workbook access or new
mean/difference calculation occurs. Nine table references across three figures
(six unique tables) remain SHA-256 identical to their numerical runs.

All three v2 PDFs were independently rendered with pypdfium2 and inspected;
each is one 1296×1368-point page. Panel labels/units are separated, held crosses
fit within padded x limits, counts are outside data regions, and legends and
interpretation captions are present. PDF text extraction also confirmed each
UT/TGF-beta legend. The figures remain unstacked and do not assert normalized
composition. This correction supersedes presentation only.

## Integration checks

Required receipt, repository/current-main and preservation results are recorded
in the [execution ledger](EXECUTION_LEDGER.md). No governance, validator,
canonical question/guide, claim grade or old scientific output changed.
The actual source gaps and missing-value outcomes are retained as results.
No original Yadav, reviewed R1 areas/B1 or T2/Atg5 analysis was rerun.
