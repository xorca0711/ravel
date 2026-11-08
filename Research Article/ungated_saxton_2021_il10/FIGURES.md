# IL-10 RNA figure gallery

[Results and limits](RESULTS.md) · [Source/assay map](SOURCE_EVIDENCE.md) ·
[Methods](METHODS_V1.md). These are adapted exposed source descriptions of
24-hour activated human CD8 RNA. No p-values or independent biological replication.

![All fixed target libraries and five contrasts](../../analysis/research/runs/sx10_description_v1/fixed_targets.png)

**1. Fixed Figure5A targets.** Left: all eight library values in published row
order, with the two source direction groups separated. Right: differences of
group mean log2(CPM+1), including both direct variant-WT comparisons. IL2 is
displayed with an asterisk but excluded from panel summaries by the fixed filter.
These are RNA abundances, not cytokine secretion. The source labels do not imply
every member has the same sign: IFNG WT-PBS is slightly negative here.
[PDF](../../analysis/research/runs/sx10_description_v1/fixed_targets.pdf) ·
[Values](../../analysis/research/runs/sx10_description_v1/target_library_values.csv).

![Two variant response patterns and background references](../../analysis/research/runs/sx10_description_v1/response_pattern.png)

**2. Response pattern.** Grey dots are 12,655 fixed eligible background rows,
excluding all Figure5 target matches. Colored points are eligible published up/down
targets. Green lines are descriptive through-origin background fits; dotted lines
mark equal responses. Both axes reuse PBS and are noisy. Genes are not replicate
subjects, and beta is not a fraction of biological response explained. Super-10's
mixed targets coexist with overall attenuation.
[PDF](../../analysis/research/runs/sx10_description_v1/response_pattern.pdf) ·
[Fits](../../analysis/research/runs/sx10_description_v1/amplitude_fits.csv).

![Fixed Figure5B direct contrasts and omission sensitivity](../../analysis/research/runs/sx10_description_v1/omission_sensitivity.png)

**3. Bounded sensitivity.** Full data are symbols; lines span the eight single-library
omissions, separately for CPM, median-ratio count-normalized CPM and deposited
FPKM. Each is log2(value+1); scales have distinct meanings. Ranges are not CIs.
CCL1's super-10-WT direction is unstable; this unfavorable uncertainty is retained.
For suppressed chemokines, positive 10-DE-WT is weaker suppression, not an overall
inflammatory score. Source suffixes do not establish donor pairing.
[PDF](../../analysis/research/runs/sx10_description_v1/omission_sensitivity.pdf) ·
[Exact ranges](../../analysis/research/runs/sx10_description_v1/target_ranges.csv).
