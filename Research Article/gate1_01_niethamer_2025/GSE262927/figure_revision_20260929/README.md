# Figure presentation corrections — 2026-09-29

These figures replay saved tables. The original figures and trial records remain
historical outputs. No clustering, scoring, pseudotime fitting or biological test
was rerun. [The rendering script](../plot_presentation_20260929.py) and
[hash manifest](figure_run.json) identify the complete inputs and outputs.

| Current figure | Correction |
|---|---|
| [Lineage composition](lineage_composition_by_dpi.png) | Names the categorical day spacing; lines summarize different animals at each day rather than elapsed-time slopes or individual trajectories. |
| [Proliferation by lineage](proliferation_by_lineage.png) | Names categorical spacing in both rows and distinguishes cross-sectional animals from repeated measurements. |
| [Trace at a common harvest](traced_fraction_at_common_harvest_by_window.png) | Names categorical window spacing and identifies lines as 42-dpi group medians. Each dot remains one animal. |
| [Program ordering](trajectory_alveolar_programmes.png) | Replaces “independent check” with annotation comparison. Deposited labels and fitted ordering share cells/RNA, even though those labels were not used to fit the ordering. Violins show cells, not animal uncertainty. |

Per-animal values are read from the three tracked `phase_timecourse/tables/`
summaries. The last figure uses saved `regeneration_focus/tables/alveolar_cell_metadata.csv`
scores and DPT coordinates, retaining the existing rolling-window rule and original
float32 coordinate precision. These are descriptive RNA orderings, not fate
measurements. A read-only comparison with the available original H5AD confirmed
5,694 matched rows, score differences below 5e-16 and coordinate differences below
3e-8 due to CSV serialization.
