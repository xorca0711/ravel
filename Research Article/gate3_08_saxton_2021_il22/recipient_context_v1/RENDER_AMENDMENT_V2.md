# Rendering correction v2

31 October 2026 (Asia/Seoul). This is a post-exposure display correction, not a
new biological comparison or rerun of the numerical analysis.

The original contract/code were frozen at `5fbe78f` and executed successfully in
`sx22_e1a_recipient_description_v1`. Its one-decimal figure annotations round
some small positive values to `0.0`, including the day-14 non-contaminant Il22ra1
measurement. The originating reviewer raised the display risk, and inspection
of the executed figure confirmed it. The original code, contract, receipt,
tables and both figure formats remain unchanged.

The new rendering contract reads only the original stratum table. It preserves
the row order, denominators, endpoints, color transforms and scientific limits.
Only the display rule and its explanatory caption change: unavailable is `NA`,
exact zero is `0`, strictly positive values below 0.1 are `<0.1`, and other
values retain one decimal. Detection uses percentage units in this display;
abundance uses counts per million stratum counts. No numerical endpoint changes.

The separately frozen renderer emits new PNG/SVG files and a display-value audit
table into a fresh runner directory. The v2 gallery supersedes only the v1
figure presentation. Original numerical results remain authoritative. All
outcomes were exposed before this rendering amendment; no new target, stratum,
model, normalization or biological inference was selected.
