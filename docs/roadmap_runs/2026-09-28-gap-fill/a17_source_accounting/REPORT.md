# A17 source accounting completed

Fresh decoding of the hash-identified Zenodo v1.1 MAT files reproduces all **58 mouse/analysis-channel counts** in batch1. The source contains 44 mouse-indexed arrays across 13 datasets; both raw channels were decoded separately before matching the original Confetti combination. This closes deterministic input accounting, not published-fit provenance or the future FU_S comparison.

The unchanged primary input is RFP, `kras1w` / `kras2w` / `kras4w`, clone size >=2: **11 source-indexed mice and 16,113 clone measurements**. It has four, four and three mice respectively. [Primary manifest](primary_cohort_manifest.csv) retains source coordinates, vector hashes and equal-mouse weights; [size frequencies](primary_clone_size_frequencies.csv) preserve the complete observed size distribution without tail trimming. Stable IDs such as `kras1w:m1` identify nested source entries, not newly recovered animal names. No spatial mouse identity is inferred.

## Table S1 reconciliation

[Fresh reconciliation](table_s1_reconciliation.csv) reproduces all eight prior audit archive-count rows. Five printed table rows remain discrepant:

- At 1 and 2 weeks, both channels print three mouse entries while the archive holds four. The omitted fourth-mouse counts are 1,107 / 851 at 1 week and 4,815 / 2,739 at 2 weeks (YFP / RFP).
- The 2-week YFP third entry prints 1,142; the archive contains 1,152.
- The 4-day RFP entries and archive sum to 922, but the printed total is 10,464.

The transcription and archive values remain separate. The prior visually checked table transcription is a hashed reference; the raw MAT arrays, rather than the prior decoded summary, supply the new counts. [Discrepancy ledger](discrepancy_ledger.json) preserves every affected row and its comparisons.

## Mutant parameter and schedule trace

Positional arguments in the archived RFP call establish **main `sigma_s` -> function `sigma_f` -> fast process** and **main `sigma_p` -> function `sigma_s` -> slow process**. Likewise, `tausigma_s` feeds late fast rates, `tausigma_p` late slow rates, and `fs` feeds `prop_f`. [Machine-readable trace](mutant_parameter_trace.json) includes source line numbers and all units.

| Phase, by event-start time | Fast nominal net expansion | Slow nominal net expansion | Renewal probabilities |
|---|---:|---:|---|
| t < 14 days | 3.1/week | 0.9/week | r=q=0.7 |
| t >= 14 days | 0.5/week | 0.01/week | r=q=0.7 |

These are rates of the intended birth-death law, not the realised drift of the defective event selector. The literal code chooses rates before drawing its waiting time, so an event crossing 14 days retains the old rates. It also applies an event after advancing beyond an observation time before checking the loop again. The repeated slow-loss cumulative term remains documented and unmodified.

The archive's nominal `fs=0.08` allocates fast founders; its zero-based `rep <= prop_f*nclones` boundary gives 81 fast founders per 1,000. Methods S1 Table 3 was previously transcribed as `f_S=0.16` and early slow expansion 1.1/week. Both manuscript values are preserved; manuscript-symbol correspondence and the parameters that produced published curves remain unresolved.

## Executed checks and boundary

[Run record](run_record.json) hashes the archive, consumed MAT/source members, references, executing script and all outputs. Checks passed for nested dimensions, channel order, integer support, lobe pairing, full batch1 count parity, Table S1 archive-count parity, primary frequency totals, argument mapping and arithmetic rate conversion. Completed outputs cannot be overwritten by this script.

No fits, stochastic simulations or model rankings were run. A future exploratory FU_S contract still needs source variants, grid-wide rate switching, tail diagnostics, unobserved-bin likelihood handling and common comparator folds/bins/weights. These exposed data cannot become an independent validation set through this reconciliation.

To reproduce in a new authorized output location, preserve the script and its archive hash and change the explicit output confinement deliberately; the completed audited run is immutable. Runtime: Python 3.12.14, NumPy 2.4.6, SciPy 1.18.0.
