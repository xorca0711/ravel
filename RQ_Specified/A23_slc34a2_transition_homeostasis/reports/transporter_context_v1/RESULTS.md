# A23 extension: alternative-transporter RNA and epithelial stress context

**1 October 2026.** A descriptive extension of the conditional compensation
candidate. [Contract](../../config/transporter_context_v1.json) |
[Receipt](../../metadata/transporter_context_v1/run_record.json) |
[Figure](../../FIGURES.md#figure-5-alternative-transporter-context).

## Finding

The PAM case has lower SLC20A1 and SLC20A2 RNA than the control across all five
fixed AT2 selections. Within the case, depth-conditional associations with KRT8
and CLU are small and mixed. These data do not support increased alternative-
transporter RNA as the explanation for the missing coherent transition-marker
pattern. They cannot test or rule out compensatory transport activity.

## Contract and population

The new readouts were frozen before inspection of their values. Exact archived
barcodes from marker-defined AT2 candidates (primary/strict QC) and the complete
published AT2 set (all/primary/strict QC) were recovered from the original raw
matrices. Total UMI and detected-gene counts match the archived selections.
All six readouts have unique symbol mappings with stable IDs recorded.
The previously reported SLC34A2/KRT8/SPRR1A/CLU summaries are recovered.

The primary comparison remains one PAM child (CD45-negative fraction) and one
adult control: 2,298 versus 185 primary AT2 candidates. The complete published
AT2 selection contains 2,742 versus 211 cells. PAM CD45-positive cells are a
separate fraction of the same subject and are reported only as context.
Annotation and ambient/doublet uncertainty remain; selections overlap and are
sensitivity analyses, not five independent confirmations.

## Expression and within-library results

| Primary AT2 candidates | PAM mean | Control mean | PAM − control | Detection PAM / control |
|---|---:|---:|---:|---:|
| SLC20A1 | 0.07832 | 0.25405 | −0.17573 | 11.18% / 31.35% |
| SLC20A2 | 0.08864 | 0.11611 | −0.02747 | 13.45% / 15.68% |

Means are natural log(1 + UMI per 10,000), not biological log-fold changes.
Across selections, SLC20A1 differences range from −0.18689 to −0.17107 and
SLC20A2 from −0.03015 to −0.02747. Detection and aggregate-count CPM are
reported separately in the [tables](../../tables/transporter_context_v1/summaries.tsv).
They do not supply per-cell transporter abundance or transport flux.

| Case association | Primary AT2 partial rank correlation | Complete published AT2 |
|---|---:|---:|
| SLC20A1–KRT8 | +0.0026 | +0.0002 |
| SLC20A1–CLU | +0.0246 | +0.0009 |
| SLC20A2–KRT8 | +0.0111 | +0.0021 |
| SLC20A2–CLU | −0.0106 | −0.0363 |

Both variables were residualized against ranked total UMI and detected-gene
count. Raw rank associations and each variable's depth dependence are retained.
Across all prespecified pairs, libraries and selections, 40/90 associations
pass the coverage gate; 30 fail because the CD45-positive fraction has fewer
than 50 selected cells, and the remaining 20 fail sparse SPRR1A coverage.
Unestimable associations are missing, not zero. There are no p-values,
cell-based biological intervals or population claims.

## Strict review of compensation and competing explanations

**Related to A23 H2/P3: compensation remains an untested functional candidate.**
The stronger RNA-surrogate explanation is unsupported here: neither higher
alternative-transporter RNA nor a consistent inverse transporter–stress
relationship is observed in the case. This is not a precise null for function,
and a case/control difference cannot identify what caused the epithelial state.

The earlier [mouse source-assay audit](../external_pilot_v2/RESULTS.md#p3-source-endpoints-and-linkage)
showed transporter-RNA responses under dietary phosphate restriction. Those
mouse observations are not linked to these human cells or subjects. The
[primary source](https://www.nature.com/articles/s41467-023-36810-8) motivates
phosphate-homeostasis context, not evidence that compensation buffered this case.

The narrowed RQ remains: **under what homeostatic and injury conditions does
SLC34A2 impairment produce transition-associated stress?** Direct epithelial
homeostatic disturbance, secondary mineral/inflammatory injury, and disease-stage
or cell-selection differences remain competing explanations. Temporal ordering
before identity loss and restoration of mature function remain untested.
A decisive extension needs replicated linked units with verified transport
status, compensatory flux, the relevant phosphate compartment, independent
state measures and injury context. More correlations in this same case cannot
supply those missing endpoints. No RQ ID, claim grade or owner acceptance changes.

## Reproduction

Run `scripts/07_transporter_context.py` only in a fresh copy without its output
directories. It requires the three exact hashed raw matrices recorded by the
preceding acquisition run and the scientific packages pinned in
`config/external_requirements.txt`. It refuses overwrites. From repository root,
`python analysis/scripts/verify_a22_a23_extensions.py` checks tracked receipts,
selection/summary arithmetic and missingness gates; `--with-raw` additionally
recomputes primary marker and depth-controlled association values independently.
The current layout-v2 figure moves a legend away from observations; initial
renders and both rendering receipts remain preserved.
