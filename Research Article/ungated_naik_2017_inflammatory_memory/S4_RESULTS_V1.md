# S4 v1: recall RNA after accounting for the baseline offset

18 November 2026. Article-local `Nk17-P01`; exposed description of 12 deposited
libraries. The governed run and independent verification are complete. The
coordinator reviewed this report, numerical outputs and all figures without requesting a numerical
revision and authorized bounded S4B after preserving S4. This is agent review,
not human scientific acceptance; S3/S5 remain unstarted.

## What narrowed, stayed mixed and remains unestimated

The post-wound history/control difference is not uniformly larger than baseline:
its absolute magnitude exceeds baseline for 53.72% of the W6 union and 46.71% of
the W12 union. Subtracting baseline leaves continuous positive and negative
contrasts, but their typical magnitudes are small relative to the observed
library-combination spread. About 82% of adjusted ranges include zero, and
normalization changes the sign of 13.67% at W6 and 19.29% at W12. The same pattern
remains in the comparison-specific baseline expression intersections.

The exposed QC also identifies a consequential unresolved discrepancy: two
baseline libraries have near-zero Xist with hundreds to thousands of counts for
each of four Y-linked genes, although all 12 saved GEO records say `Sex: female`.
The other ten libraries have abundant Xist and at most two raw counts for any of
those Y markers. This is a source/marker consistency problem requiring
clarification, not a basis to assign sex, pair libraries, exclude samples or apply
batch correction. It further limits interpretation of baseline-adjusted effects.

The published premise of altered recall remains distinct from this shared-source
measurement. S2 motivated separating post-wound differences from baseline offsets;
S4 now supplies that decomposition and its limitations. It does not establish
uniform response amplification, faster kinetics, repair benefit, retained
chromatin or an intrinsic memory mechanism. It also does not refute the paper's
separate chromatin or functional evidence. No new candidate or claim grade is adopted.

## Comparison, normalization and provenance

The [method](S4_METHOD_V1.md) and
[contract](../../analysis/research/contracts/Nk17-P01.s4_recall_description_v1.json)
were frozen in `840bca34c2e943f532d523bdbe771dc1663c7026` before execution.
The [receipt](../../analysis/research/runs/naik2017_s4_recall_description_v1/receipt.json)
binds that revision, 17 inputs, five code/test/helper files and 16 outputs.
The unchanged S2 normalization/contrast helpers were reused; no S2 output changed.

| Phase | Control | Prior-inflammation history |
|---|---|---|
| B0: D30 unwounded baseline | GSM2440989–90 | GSM2440991–92 |
| W6: 6 hours after D30 wounding | GSM2440993–94 | GSM2440995–96 |
| W12: 12 hours after D30 wounding | GSM2440997–98 | GSM2440999–2441000 |

Every group has two deposited libraries. Source-reported duplicate pooled
preparations remain positive design evidence, with exact membership, batches and
overlap unverified. All 12 have HiSeq 2500/single metadata. This removes the
specific D6 platform/layout comparison from S4, while baseline versus wound-edge
compartment/selection, composition and preparation effects remain unresolved.
There is no established longitudinal pairing.

Joint median-of-ratios (MOR) factors use 15,589 genes positive in all 12 libraries
and are centered to geometric mean one. For arithmetic normalized group means,
`L_t = log2((H_t + 1)/(C_t + 1))` and `A_t = L_t − L_B0`. Each group's separate
wound/baseline log ratio and every component are retained. The common reference
scale makes the pseudocount comparable across phases. Joint total-count scaling
is the sole normalization sensitivity. S4 baseline numbers can differ from S2's
four-library reference, particularly for sparse genes; this is a different
prespecified normalization context, not a revision of S2.

All 47,729 exact gene IDs remain in
[gene_effects.tsv.gz](../../analysis/research/runs/naik2017_s4_recall_description_v1/gene_effects.tsv.gz)
and [gene_values.tsv.gz](../../analysis/research/runs/naik2017_s4_recall_description_v1/gene_values.tsv.gz).
The latter contains raw, MOR, total-scaled and CPM values for every library.
Exact M9 annotation matched 47,643 IDs; 86 unmatched IDs remain in the universe.
No population p-value, confidence interval, equivalence margin or biological
response class was calculated. Counts and normalization do not measure absolute RNA.

## Baseline, post-wound and adjusted effects

Expression qualification requires CPM ≥ 1 in at least two of four libraries in
a phase. Each primary union includes baseline or that wound phase; its
intersection requires both. Qualification is not expression in both history groups.

| Comparison/universe | Genes | Median absolute baseline L0 | Median absolute post-wound Lt | Median absolute adjusted At | Absolute Lt > absolute L0 |
|---|---:|---:|---:|---:|---:|
| W6, all deposited IDs | 47,729 | 0.023 | 0.048 | 0.115 | 29.79% |
| W6, comparison union | 12,857 | 0.144 | 0.165 | 0.238 | 6,907 / 12,857 (53.72%) |
| W6, baseline intersection | 11,732 | 0.134 | 0.155 | 0.225 | 6,334 / 11,732 (53.99%) |
| W12, all deposited IDs | 47,729 | 0.023 | 0.041 | 0.106 | 27.31% |
| W12, comparison union | 12,885 | 0.144 | 0.132 | 0.206 | 6,019 / 12,885 (46.71%) |
| W12, baseline intersection | 11,772 | 0.134 | 0.124 | 0.193 | 5,517 / 11,772 (46.87%) |

Effects are regularized log2 ratios/differences. `A_t` is a signed difference,
not `abs(L_t) − abs(L0)`, and a positive value is not necessarily induction in
the history group. Baseline adjustment reverses the sign of the unadjusted
post-wound effect for 20.62% of W6 and 25.33% of W12 union genes. Retaining both
components therefore changes the biological reading of some examples.

All-ID summaries contain many uninformative zeros: 40.78% at W6 and 40.46% at
W12 are zero across all eight involved libraries. In the unions, the low-group-
mean flag occurs for 45 W6 genes and 56 W12 genes; three genes in each union
are all-zero at baseline, and two W6/four W12 genes are all-zero after wounding.
Neither comparison's baseline intersection contains a group-zero or
group-mean-below-one case. Thus the intersection narrows zero-floor explanations,
but does not remove library variability or source composition uncertainty.

Each group's wound/baseline contrast is also present. In the W6 union, median
absolute contrasts are 0.540 for controls and 0.600 for history; at W12, 0.499
and 0.573. These feature distributions are not a test of an overall stronger
biological response and cannot distinguish compartment changes from within-cell
regulation. Exact quantiles/flags are in
[summary.json](../../analysis/research/runs/naik2017_s4_recall_description_v1/summary.json).

## Spread, normalization and shared-baseline correlation

| Diagnostic | W6 union | W6 baseline intersection | W12 union | W12 baseline intersection |
|---|---:|---:|---:|---:|
| Adjusted 16-combination range spans/touches zero | 82.07% | 81.66% | 82.72% | 82.62% |
| Median range width, log2 units | 1.077 | 1.005 | 0.920 | 0.857 |
| MOR/total-count adjusted sign changes | 13.67% | 14.36% | 19.29% | 20.55% |
| Median absolute normalization difference | 0.113 | 0.113 | 0.138 | 0.139 |

The 16 combinations enumerate two libraries in each of four groups. They are
neither independent replicate effects nor a confidence interval. Zero inclusion
does not establish no effect, equivalence or a failed population-level hypothesis.
Conversely, a range wholly on one side of zero supplies no population p-value.
The normalization sensitivity remains substantial relative to typical adjusted
magnitudes, even after expression qualification.

| Common universe | Genes | Unadjusted W6/W12 Pearson / Spearman | Adjusted W6/W12 Pearson / Spearman |
|---|---:|---:|---:|
| Global three-phase union | 12,998 | 0.641 / 0.573 | 0.805 / 0.783 |
| Qualified at all three phases | 11,647 | 0.656 / 0.602 | 0.805 / 0.801 |

Both adjusted profiles subtract the **same estimated baseline**. Baseline
variation/error can induce or strengthen their correlation; the higher adjusted
correlation is not independent temporal corroboration. This diagnostic does not
estimate how much correlation is biological versus shared-baseline arithmetic.
Opposite nonzero adjusted directions occur for 18.36% of the global union and
17.93% of the all-three subset. Neither concordance nor discordance across two
sampled hours establishes a response rate or accelerated repair.

## Marker QC: preserve the discrepancy without assigning identity

All five names map uniquely to exact M9 IDs in the input count universe; the
[annotation record](../../analysis/research/runs/naik2017_s4_recall_description_v1/annotation_coverage.json)
preserves IDs, gene types and chrX/chrY locations. Every one of the 60
marker/library records, including raw/MOR/total/CPM values and recorded sex, is in
[marker_qc.tsv](../../analysis/research/runs/naik2017_s4_recall_description_v1/marker_qc.tsv).

| Library | Xist raw | Ddx3y raw | Eif2s3y raw | Kdm5d raw | Uty raw |
|---|---:|---:|---:|---:|---:|
| GSM2440989, B0 C1 | 0 | 3,631 | 1,957 | 897 | 1,345 |
| GSM2440990, B0 C2 | 53,065 | 0 | 0 | 0 | 1 |
| GSM2440991, B0 H1 | 1 | 2,386 | 1,683 | 976 | 978 |
| GSM2440992, B0 H2 | 44,150 | 1 | 0 | 0 | 0 |
| Eight wound libraries, per-library range | 13,575–61,086 | 0–2 | 0–1 | 0–1 | 0–1 |

The contrast remains on the CPM scale: Ddx3y is 151.744/100.999 CPM in B0 C1/H1,
with Xist 0/0.042 CPM, compared with Xist 506.322–1,498.996 CPM in the other ten
libraries and near-zero Y-marker CPM. The saved source field is uniformly
`Sex: female`; it is not silently replaced by an expression-inferred label.
The finding is consistent with an unresolved source-composition/label or
measurement problem. Its cause, exact animal/pool sex, contamination status,
sample matching and any correction are **unassigned**. Both histories contain
the discrepant baseline profile, but that symmetry does not prove its effects
cancel under baseline adjustment.
Conversely, the balanced occurrence across baseline history groups means this
marker finding alone is not proof that every history contrast is biased.

This follow-up was selected because S2 exposed Xist heterogeneity. It is not an
independent validation cohort. A useful next clarification would establish
whether the recorded sex applies to these exact preparations and resolve their
provenance/measurement discrepancy. No new sample exclusion, sex classification,
matching, reanalysis or external inquiry was performed.

## Positive, negative and inconsistent examples

The frozen rules select signed extrema in each comparison's expression union,
an opposite-direction example in the all-three subset, and the widest adjusted
range. These are descriptive illustrations subject to selection/noise, not
validated targets or estimates of their prevalence.

| Example | Baseline L0 | W6 L6 / A6 | W12 L12 / A12 | Interpretation limit |
|---|---:|---:|---:|---|
| 2300005B03Rik, maximum W6 adjusted | −2.025 | 2.759 / 4.784 | 0.836 / 2.860 | W6 control wound/baseline is −4.056, history +0.728; positive adjustment partly reflects control decline. W6 range 1.426–6.775; W12 not expression-qualified. |
| Col1a2, minimum W6 adjusted | 5.395 | −3.527 / −8.922 | 1.311 / −4.084 | Baseline fails qualification and is dominated by one history library. W6 range −16.385–0.455, W12 −8.181–4.403. |
| Defb3, maximum W12 adjusted | −3.132 | 2.478 / 5.610 | 2.061 / 5.193 | Baseline history counts are zero; unregularized adjusted effects are undefined. It is outside the W6 comparison union, though the complete-table W6 value is shown. |
| Igfl3, minimum W12 adjusted | 4.669 | 1.432 / −3.238 | 0.475 / −4.194 | Baseline control mean is 0.571. Both groups rise at W12 (control +7.475, history +3.281), so negative adjustment does not mean repression in history. Both adjusted ranges include zero. |
| Iigp1, strongest opposite adjusted directions | 0.117 | −0.894 / −1.011 | 0.991 / 0.874 | Qualified at all phases; W6 range −2.580–0.155 and W12 −1.811–3.181 both include zero. No kinetic switch is established. |
| Xist, widest adjusted library range | −0.040 | −0.318 / −0.278 | −0.397 / −0.356 | W6 range −16.778–14.754 and W12 −16.549–14.287; near-zero means mask major baseline heterogeneity. See marker QC. |

Full IDs, selection ranks, per-group responses and flags are in
[selected_cases.tsv](../../analysis/research/runs/naik2017_s4_recall_description_v1/selected_cases.tsv).
No functional interpretation is inferred merely from an annotated gene name.

## Figures, validation and handoff

All three PNGs were visually reviewed; paired PDF exports are retained.

- [Figure 1: library and exposed marker QC](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig01_sample_marker_qc.png)
  ([PDF](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig01_sample_marker_qc.pdf)).
  Count totals/detections describe deposited tables, not raw-read QC. Totals span
  23.62–76.99 million; detected genes span 18,478–23,395. The heatmap uses
  log2(CPM + 1), preserves all libraries and assigns no sex or matching.
- [Figure 2: components and adjusted effects](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig02_recall_effects.png)
  ([PDF](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig02_recall_effects.pdf)).
  Hexagon colour denotes within-panel gene density on a log scale; panels do not
  share a colour scale. The correlation annotation and table above retain the
  shared-baseline caveat. The two sampled post-wound times supply no rate estimate.
- [Figure 3: all libraries in selected examples](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig03_library_examples.png)
  ([PDF](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig03_library_examples.pdf)).
  Dots show log2(library MOR + 1) relative to log2(B0 control mean + 1); bars
  transform arithmetic count-scale group means. No lines imply paired trajectories.

Input preflight, the governed run and receipt integrity verification passed.
The independently implemented standard-library verifier passed **7,255,847**
checks on the actual inputs, including all 60 marker rows, source/annotation
joins, numerical fields, example selection and core summary fractions/correlations.
Maximum scaled error was `1.0658e-14` at computational tolerance `1e-10`.
[verification.json](../../analysis/research/runs/naik2017_s4_recall_description_v1/verification.json)
records that arithmetic result, not biological replication or acceptance.
No real S4 run failed and no frozen S1M/S2/S4 input, code or output was overwritten.
The full research gate passed against refreshed main `d0429d0`, alongside
20,077 repository checks, 249 affected-document local links and whitespace.

**Authorized next bounded step:** after preserving S4, S4B will hold its
normalization, gene qualification and wound means fixed, and compare the primary
two-library/group baseline with GSM2440992/2440990 and GSM2440991/2440989 reference
ratios. These observed marker-profile references each use one library per history;
they are not verified sex strata, matched pairs, an exclusion/correction or a
preferred replacement. A separate prospective contract will assess continuous
reference dependence using the same universes and already-selected examples.
Return after S4B for coordinator review before S3/S5. S3 accessibility
qualification can remain informative without treating recall RNA as validated
intrinsic memory; S5 must retain unresolved source/unit and compartment limits.
No S4B/S3/S5 calculation or mechanistic extension has started. The restriction history
remains preserved; blocked broad methods extraction was not retried. No push,
PR, Notion edit, external inquiry or publication was performed.
