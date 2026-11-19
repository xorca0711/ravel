# S2 v1: acute and recovered-baseline RNA differences

18 November 2026. Article-local owner `Nk17-P01`; exposed, finite-library
description of the deposited public data. Execution is complete. The coordinator
reviewed this report, summary/verification outputs and all three figures without
requesting a numerical revision, and authorized bounded S4 next. This is agent
review; no human scientific acceptance or global RQ promotion is implied.

## What the result changes

In these libraries, recovered-baseline D30 history/control RNA differences are
usually smaller than D6 acute-inflamed/control differences. This remains true
when restricting the comparison to genes expression-qualified at **both** times,
so genes with low or zero D30 counts in the union cannot alone explain the broad
pattern. Individual D30 directions remain much less consistent across libraries
than the group means suggest. These are relative RNA measurements, not evidence
that particular genes or cells have biologically resolved, nor a test of retained
chromatin, absolute RNA abundance or repair competence.

The published premise is that regulatory memory and altered recall can remain
after inflammation subsides. [S1M](S1M_RESULTS_V2.md) qualified the saved counts
and within-time comparisons. S2 now supplies a source-specific observation of
smaller baseline RNA contrasts, with heterogeneous residual differences. The
remaining informative RNA question is whether later wound-associated history
differences exceed these baseline offsets. That question motivates the proposed
bounded S4 comparison below; it does not follow from availability of an assay.

## Comparison and evidence

The [prospective method](S2_METHOD_V1.md) and
[contract](../../analysis/research/contracts/Nk17-P01.s2_rna_description_v1.json)
were committed at `d4bf26d4a3307486c9a8462ca5266221117d9ca1` before execution.
The [receipt](../../analysis/research/runs/naik2017_s2_rna_description_v1/receipt.json)
records that exact revision, 12 input hashes, four code/test files and 15 outputs.

| Contrast | Exposed libraries | Controls | Endpoint and unit |
|---|---|---|---|
| D6 acute inflamed/control | GSM2440987–88 | GSM2440985–86 | Relative gene-count log2 ratio; two libraries per group |
| D30 recovered-baseline history/control | GSM2440991–92 | GSM2440989–90 | Same endpoint; two libraries per group |

Median-of-ratios (MOR) factors were estimated separately within each timepoint.
The effect is `log2((mean_exposed + 1)/(mean_control + 1))`, using arithmetic
means of normalized counts. Total-count normalization on a comparable reference
count scale is the prespecified sensitivity. All 47,729 versioned gene IDs remain
in [gene_effects.tsv](../../analysis/research/runs/naik2017_s2_rna_description_v1/gene_effects.tsv)
and the per-library
[gene_values.tsv.gz](../../analysis/research/runs/naik2017_s2_rna_description_v1/gene_values.tsv.gz).
Exact GENCODE M9 annotation matched 47,643 IDs; 86 unmatched IDs were retained
with explicit missing labels. Annotation did not select genes.

The paper's duplicate pooled preparations remain positive design evidence.
This descriptive analysis uses libraries without inventing mouse-level sample
sizes, pairing, pool membership or batch equivalence. D6 uses HiSeq 4000/paired
reads; D30 uses HiSeq 2500/single reads. Each within-time contrast shares
platform/layout, but their cross-time difference cannot isolate recovery from
technical differences. The reanalysis is shared-source evidence, not independent
biological replication.

## Continuous effects and expression qualification

Qualification means CPM ≥ 1 in at least two of four libraries at a timepoint.
It does not require both history groups to be expressed. The union includes
13,452 genes, of which 12,052 qualify at both times, 1,144 only at D6 and 256 only
at D30. No acute-effect ranking selects these summary universes.

| Gene universe | Genes | Median absolute D6 effect | Median absolute D30 effect | Smaller absolute D30 effect |
|---|---:|---:|---:|---:|
| All deposited IDs | 47,729 | 0.147 | 0.020 | 20,412 / 47,729 (42.77%) |
| Qualified at either time (primary display) | 13,452 | 0.538 | 0.146 | 11,108 / 13,452 (82.58%) |
| Qualified at both times (sensitivity) | 12,052 | 0.504 | 0.134 | 10,082 / 12,052 (83.65%) |

All effects are regularized log2 ratios. Across all deposited IDs, 18,967
absolute-effect ties (39.74%) and many all-zero rows make the first row a poor
stand-alone biological summary. The complete universe is retained nevertheless.
Within the union, 27 genes have all four D30 counts zero and 150 have at least one
normalized group mean below one. Their D30 effects can be pulled toward zero by
the added one; an all-zero contrast is exactly zero. In the both-time subset,
neither D30 condition occurs. The similar smaller-effect fraction in that subset
narrows this particular artifact explanation, while retaining the cross-time,
expression-selection and finite-sample limitations.

The D6/D30 effect profiles have weak feature-level correspondence: Pearson
`r = 0.071` and Spearman `rho = -0.069` in the union (`0.032` and `-0.107` in the
both-time subset). These summarize gene features without treating genes as
biological replicates or attaching inferential p-values. Smaller magnitude does
not require preservation of direction or a scaled copy of the acute profile.
Exact distributions and counts are in
[summary.json](../../analysis/research/runs/naik2017_s2_rna_description_v1/summary.json).

## Library spread and normalization sensitivity

| Union-qualified genes | D6 | D30 |
|---|---:|---:|
| Median absolute MOR versus total-count effect difference | 0.102 | 0.057 |
| Normalization sign changes | 715 / 13,452 (5.32%) | 1,581 / 13,452 (11.75%) |
| Four-library-combination range spans or touches zero | 3,851 / 13,452 (28.63%) | 9,911 / 13,452 (73.68%) |
| Median width of that log2-effect range | 0.548 | 0.575 |

The range covers all four exposed-versus-control library combinations; none is
an established matched pair, independent effect estimate or confidence interval.
In the both-time subset, ranges span/touch zero for 27.90% at D6 and 73.92% at
D30, and normalization changes the sign for 5.59% and 12.75%, respectively.
Thus expression qualification does not eliminate the D30 direction uncertainty.
Even modest normalization shifts matter near zero; maximum absolute differences
in the union are 0.175 at D6 and 0.110 at D30. The two normalization assumptions
do not establish absolute RNA abundance or remove composition/batch effects.

Count totals range from 23.62 to 49.54 million and detected IDs from 18,478 to
24,041 across the eight libraries. These are sums/detections in deposited gene
tables, not raw sequencing-read QC. Sample correlation is calculated over the
union-qualified genes and is descriptive. Neither profile correlation nor the
two libraries per group resolves exact pool composition or preparation effects.
See [sample_qc.tsv](../../analysis/research/runs/naik2017_s2_rna_description_v1/sample_qc.tsv).

## Selected examples and figures

The six examples were selected by the frozen rank rules within the union.
They illustrate extremes and diagnostics, not biological classes. Acute-selected
examples invite selection bias and regression to the mean; the global fractions
above were not calculated from those examples.

| Example and selection | D6 effect | D30 effect | Consequential qualification |
|---|---:|---:|---|
| S100a9; maximum D6 signed effect | 11.005 | 0.282 | D30 four-combination range −2.997 to 2.888 despite the much smaller mean contrast |
| Mrgprb11-ps; minimum D6 signed effect | −8.476 | −0.367 | D30 range −0.738 to 0.087; annotation is an unprocessed pseudogene |
| Col1a2; maximum D30 signed effect | −0.873 | 5.374 | D30 range −1.887 to 7.309; one high history library dominates, and D30 fails the two-library expression criterion |
| Defb3; minimum D30 signed effect | 5.686 | −2.634 | Both D30 history counts are zero; unregularized D30 effect is undefined and D30 is not expression-qualified |
| Scand1; greatest normalization discrepancy | 0.119 | 0.609 | D6 changes from 0.119 under MOR to −0.056 under total-count scaling; D6 range is −3.769 to 3.595 |
| Xist; widest library effect range | −1.214 | −0.030 | D30 range −14.182 to 15.282 despite near-zero group contrast; source of heterogeneity is unassigned |

Exact IDs, selection reasons and diagnostics are in
[selected_cases.tsv](../../analysis/research/runs/naik2017_s2_rna_description_v1/selected_cases.tsv).
The Xist observation is a QC lead, not evidence assigning sex, pool composition
or a history mechanism to any library. No candidate is promoted from these ranks.

All three 300-dpi PNGs were visually reviewed for legible labels, displayed values
and the absence of implied longitudinal pairing; matching PDFs are available.

- [Figure 1: library diagnostics](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig01_sample_qc.png)
  ([PDF](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig01_sample_qc.pdf)).
- [Figure 2: continuous effects and normalization](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig02_effect_profiles.png)
  ([PDF](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig02_effect_profiles.pdf)).
- [Figure 3: finite-library examples](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig03_library_examples.png)
  ([PDF](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig03_library_examples.pdf)).
  Each dot is `log2(library MOR count + 1) − log2(time-specific control mean + 1)`;
  bars use the arithmetic count-scale group means before log transformation.
  They are not means of the plotted log values or trajectories between times.

## Validation and next decision

Input preflight and the governed runner completed successfully. An independently
implemented standard-library verifier reread the eight input tables and passed
3,006,967 numeric/flag/join checks; maximum scaled arithmetic error was
`7.1054e-15` at tolerance `1e-10`. This verifies implementation, not a biological
claim. [verification.json](../../analysis/research/runs/naik2017_s2_rna_description_v1/verification.json)
contains the result. The receipt integrity command returned `ok: true`; the
receipt itself remains the immutable runner record. Synthetic checks and the
pre-freeze floating-point tie correction remain documented in the method.
No real S2 run failed, and no frozen input, code or output was overwritten.
The full research gate against refreshed main `d0429d0`, 20,041 repository
validation checks, 237 affected-document local links and whitespace checks passed.

**Next bounded stage, authorized after coordinator review:** S4 recall RNA,
qualifying the saved D30 baseline and 6/12-hour wound libraries together before a
separate prospective contract. Compare each post-wound history/control log-ratio
with the baseline history/control log-ratio, retaining library spread,
normalization sensitivity and discordant genes. A remaining contrast could
describe history-dependent transcription beyond a baseline offset; disappearance
after adjustment or inconsistent library directions would narrow that account.
Before calculation, freeze a common normalization/reference scale across the
12 libraries, expression-based comparison universes, independent arithmetic
checks and exposed marker QC motivated by S2's Xist heterogeneity. No sex
assignment, exclusions, matching or batch correction follows from that QC.
Shared HiSeq 2500/single-read metadata avoids the known D6 platform/layout
contrast but does not establish equal processing batches or longitudinal pairs.

S3 ATAC remains independently eligible for later source/region qualification;
it has not run and is not presumed necessary to begin a justified recall RNA
description. S5 integration and S6 extension remain unstarted. No result here
proves or disproves epigenetic memory or wound repair. The earlier restricted
method extraction was not retried, and its failures remain in the
[recovery record](RECOVERY_CHECKPOINT.md). No push, PR, external publication or
account/protection setting changed.
