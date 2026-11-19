# Naik 2017: from inflammatory history to epithelial recall

19 November 2026. Article-local research package, informed by the owner's
Naik Results/Discussion notes. This source sits outside the ordered roadmap;
existing gates and RQs retain their status. Owner `Nk17-P01` follows Ravel's
paper-driven workflow. Execution and coordinator review confer no human
scientific acceptance.

**Current result:** [S5F v1](S5F_RESULTS_V1.md) reconstructs 35 functional/source
endpoints and all 38 declared contrasts. PI epithelial tongues and day-10
outgrowth are larger in the supplied records; EdU differences vary by day.
Reported history advantages change with Aim2, CASP1 and IL1R1 perturbations,
while the Il18KO contrast remains positive. In the separate F5g comparison,
Aim2 OE effects are +0.30 under Ig and +0.16 under anti-IL1R1 (difference −0.14
day^-1). Equality of OE+anti to Ctrl+Ig does not demonstrate complete blockade.
Source/caption N discrepancies and normalized reference semantics remain
explicit. All 13,821 independent checks passed; all five figures were inspected.
Coordinator stage review of the complete report, figures and numbers requested
no further revision; S5F is preserved at `2514379`. The [S6 assessment](S6_DECISION_V1.md)
now proposes the [all-panel daily-area design](S6A_DAILY_AREA_DESIGN_V1.md) first,
with fixed D6 marker QC and D180 proxy durability retained as separate candidates.
The design is coordinator-approved for implementation and governed execution;
no extension effects have been calculated.

[S5M v2](S5M_RESULTS_V2.md) preserves the 312 RNA–ATAC associations and 96
covariance records while correcting its count-zero warnings. Primary ±1 kb MOR
Pearson is 0.425 at D6 and 0.144 at D30; small negative adjusted associations
reflect subtraction of a larger positive baseline covariance. They do not show
chromatin repression. The [S3 result](S3_RESULTS_V1.md) describes relative ranks
near 21,760 boundary proxies; original retained domains and absolute opening
remain unestimated.

The [S2 baseline](S2_RESULTS_V1.md), [S4 recall](S4_RESULTS_V1.md) and
[S4B sensitivity](S4B_RESULTS_V1.md) retain mixed relative RNA effects and
baseline-reference dependence. Recorded female metadata and Xist/Y-marker
profiles disagree for two baseline libraries; no sex assignment, correction or
pairing was made. [S1M](S1M_RESULTS_V2.md) owns assay-specific units: D6 is acute
inflammation, D30 recovered-baseline history. RNA cross-time technical differences
must not be transferred to ATAC, whose eight D6/D30 tracks share platform/layout.
Exact pool/animal and cross-assay membership remain unresolved.

**Organizing question:** after inflammation resolves, what remains in epithelial
stem cells, and how does that history alter a subsequent tissue-damage response?

Naik's published result connects persistent accessibility with altered wound
response in mouse epidermis. The first computational purpose here is exposed
reproduction and qualification of that connection: distinguish acute RNA,
recovery-stage RNA, persistent accessibility and wound-induced transcription.
These are different measurements. Population selection, continuing local input,
sampling and processing can coexist with intrinsic regulatory persistence.

[Stepwise plan](ANALYSIS_PLAN.md) · [Paper evidence and corrections](PAPER_REVIEW.md)
· [Literature context and search record](LITERATURE_CONTEXT.md)
· [Execution checkpoint](STAGE_STATUS.md)

The published biological argument is that inflammation leaves regulatory
changes in long-lived epithelial populations, which can alter a later response
and repair outcome. The RNA, chromatin and functional experiments support
different parts of that argument. Ravel's analysis will reconstruct the eligible
comparisons, examine their robustness and use any remaining discrepancy to
develop a specific follow-up. The [stage table](ANALYSIS_PLAN.md#stage-sequence-and-decisions)
describes computational order, not a cellular trajectory or established causal chain.

## What the current evidence changes

- S5F supplies distinct measured functional/source endpoints. Tongue length,
  EdU, outgrowth, expression, activity, protein and reported decay constants
  cannot substitute for one another or identify memory storage. The residual
  within-blockade F5g contrast motivates qualifying the separate daily-area
  sources before proposing a bounded extension; no new numerical extension has
  run. Naik Fig. 5c already supplies the transcript/protein distinction.
- S5M connects the measured RNA and TSS-proxy descriptions: acute alignment is
  larger than recovered/recall alignment, with baseline subtraction shaping the
  small adjusted associations. Shared libraries, baseline coupling and differing
  biological layers remain limits. S5F now describes the separate source
  functional endpoints without a combined memory score. Naik Fig5c
  already reports IL-1beta protein without an Il1b transcript increase.
- S3 adds a qualified relative-ordering measurement in a protein-coding boundary
  universe. Smaller aggregate D30 displacement survives the two widths, while
  individual signs/magnitudes and library support can vary. Aim2's positive D30
  average has a cross-library range including zero; Iigp1 is width-sensitive.
  None reconstructs the published distal retained-domain classification.
- The S2 distribution supports smaller recovered-baseline relative RNA contrasts
  within this source, including the both-time expression-qualified subset.
  Residual gene differences are heterogeneous and sometimes driven by one
  library or zeros. Neither attenuation nor a small group mean establishes
  equivalence, absolute RNA recovery, intrinsic regulatory memory or repair.
- S4 decomposes baseline and post-wound contrasts and exposes a source/marker
  discrepancy. Adjusted W6/W12 correlations share baseline estimation error:
  global-union Pearson correlation rises from 0.641 unadjusted to 0.805 adjusted,
  which is not independent temporal corroboration. Negative adjusted effects can
  coexist with increases in both histories; component contrasts remain essential.
- S4B adds reference dependence: median absolute shifts of about 0.11 log2 units
  accompany 15–17% union sign changes. Two one-library references diagnose
  sensitivity without correcting source identity or replacing the primary result.
  The shift is identical at W6/W12 for each gene by construction, not replication.
- The annotated version-of-record PDF includes a correction to Figure 2g.
  Figure 3 reports pooled ATAC preparations; Figure 4 and the final RNA Methods
  report four animals per condition in duplicate. Manuscript wording differs.
  Biological units must therefore be qualified by assay and source version.
- The inspected GEO metadata snapshot lists 16 RNA and 12 ATAC libraries.
  It offers RNA at D6, unwounded D30 and 6/12 hours after wounding, and ATAC at
  D6/D30/D180. It does not list wound ATAC or D180 RNA-seq. Separate assays are
  not established same-animal or same-cell pairs.
- Published outcomes and some D6 RNA profiles were inspected before the S2
  specification. S2 is exposed shared-source description; its later freeze
  does not turn the work into independent confirmation or biological replication.
- Larsen 2021 already investigates establishment, maintenance and recall in this
  system. Rediscovering AP-1 enrichment or proposing that homeostatic factors
  maintain accessible regions is not, by itself, a new mechanistic contribution.

## Measured functional-source evidence

![Reported functional-rate comparisons](../../analysis/research/runs/naik2017_s5f_functional_sources_v1/fig04_reported_rates.png)

[S5F results and all five figures](S5F_RESULTS_V1.md) retain every assigned
comparison, including unfavorable and mixed results. Points and bars above are
reported rate means and SEs, not reconstructed animal rates or contrast intervals.
Source Ns and caption Ns remain separate. The normalized-reference labels in
Figure 3 count spreadsheet entries, not biological cells.

## Measured RNA–ATAC integration

![All finite RNA–ATAC associations](../../analysis/research/runs/naik2017_s5m_molecular_integration_v2/fig01_associations.png)

All widths, universes, normalization contexts, statistics and baseline references
remain on one fixed coefficient scale. Gene features are dependent, and shared
source libraries are not replication. [S5M result and covariance components](S5M_RESULTS_V2.md)
and [corrected fixed-anchor figure](../../analysis/research/runs/naik2017_s5m_molecular_integration_v2/fig02_published_anchors.png)
retain the distinct RNA, ATAC, count-zero and range-inclusion meanings.

## Measured TSS-proxy evidence

![S3 continuous rank contrasts and window-width sensitivity](../../analysis/research/runs/naik2017_s3_tss_rank_v1/fig01_relative_rank_overview.png)

[S3 result and captions](S3_RESULTS_V1.md) ·
[Overview PDF](../../analysis/research/runs/naik2017_s3_tss_rank_v1/fig01_relative_rank_overview.pdf) ·
[All fixed example libraries](../../analysis/research/runs/naik2017_s3_tss_rank_v1/fig02_fixed_examples.png) ·
[Examples PDF](../../analysis/research/runs/naik2017_s3_tss_rank_v1/fig02_fixed_examples.pdf).
Colours show within-panel log counts with separate scales. Ranks describe relative
ordering; every library's mean rank is fixed. Xist is explicitly unassayed in this
protein-coding universe. Both widths, all libraries and original means remain saved.

## Measured RNA evidence

![S4B observed baseline-reference sensitivity](../../analysis/research/runs/naik2017_s4b_baseline_reference_v1/fig01_baseline_reference.png)

[S4B result and caption](S4B_RESULTS_V1.md) ·
[PDF](../../analysis/research/runs/naik2017_s4b_baseline_reference_v1/fig01_baseline_reference.pdf).
All four panels retain the primary result and frozen gene universes. Colours show
within-panel log density; axis and colour ranges differ between panels. The two
alternative references each have one library per history and assign no sex or matching.

![S4 baseline components, adjusted recall effects and normalization sensitivity](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig02_recall_effects.png)

S4 Figure 2 retains baseline/post-wound components and the comparison-specific
union/intersection sensitivities. Both adjusted profiles subtract the same
estimated baseline; the figure and [result](S4_RESULTS_V1.md) retain that
correlation limitation. With two libraries/group, all-combination ranges remain
spread diagnostics, not confidence intervals or paired trajectories. Expression
qualification is not reliable expression in each history group or identity validation.

| S4 measured figure | What to inspect | Export |
|---|---|---|
| [1. Library and marker QC](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig01_sample_marker_qc.png) | The two baseline Xist/Y profiles, preserved source labels and common normalization | [PDF](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig01_sample_marker_qc.pdf) |
| [2. Recall components](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig02_recall_effects.png) | Baseline offsets, mixed adjusted effects, shared-baseline correlation and normalization sensitivity | [PDF](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig02_recall_effects.pdf) |
| [3. Selected library examples](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig03_library_examples.png) | Positive/negative adjustments, sparse baselines, Iigp1 direction discordance and Xist spread | [PDF](../../analysis/research/runs/naik2017_s4_recall_description_v1/fig03_library_examples.pdf) |

S4's complete [marker table](../../analysis/research/runs/naik2017_s4_recall_description_v1/marker_qc.tsv)
and [verification](../../analysis/research/runs/naik2017_s4_recall_description_v1/verification.json)
support the readout; validation supplies no biological acceptance. Earlier S2
figures remain available below, with their original method and receipt.

| Measured figure | What to inspect | Export |
|---|---|---|
| [1. Library diagnostics](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig01_sample_qc.png) | Deposited count totals, detection, normalization and union-gene profile correlation; not raw-read QC | [PDF](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig01_sample_qc.pdf) |
| [2. Continuous effects](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig02_effect_profiles.png) | Smaller D30 magnitudes, weak direction correspondence and normalization sensitivity | [PDF](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig02_effect_profiles.pdf) |
| [3. Selected library examples](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig03_library_examples.png) | Every library shown; Col1a2's single-library influence, Defb3's zeros, Scand1's normalization sign change and Xist's large spread | [PDF](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig03_library_examples.pdf) |

Figure 3's six extremes follow the frozen rank rules within the union; they are
illustrations, not biological classes or the basis of the aggregate fractions.
Points are control-relative log counts within each timepoint; bars transform
the arithmetic count-scale group means. See the
[method](S2_METHOD_V1.md), [complete results and limits](S2_RESULTS_V1.md),
[independent arithmetic verification](../../analysis/research/runs/naik2017_s2_rna_description_v1/verification.json)
and [run receipt](../../analysis/research/runs/naik2017_s2_rna_description_v1/receipt.json).

## How neighboring Ravel work informs the pipeline

| Owning evidence inspected at main `d0429d0` | Consequence for this package |
|---|---|
| [Arozamena current synthesis](../ungated_arozamena_2026_inflammatory_memory/README.md), RNA/accessibility results and v2 amendment | Carry forward separate units, source-reference checks, explicit region definitions and unfavorable QC-sensitive results. Its intestinal libraries are not skin replication. |
| [DuPage S0–S6 results](../gate3_09_dupage_2015/RESULTS.md) and [AM01](../gate3_09_dupage_2015/ANALYSIS_AMENDMENT_V2.md) | Read current results before plans; label adapted reconstructions; permit a justified stop when another analysis would add no information. |
| [Wang results](../gate3_10_wang_2018_ezh2/RESULTS_V1.md), [execution amendment](../gate3_10_wang_2018_ezh2/EXECUTION_AMENDMENT_V1.md) and [original plan](../gate3_10_wang_2018_ezh2/ANALYSIS_PLAN.md) | Separate library-level RNA, robustness, biological synthesis and genuinely measured functional outcomes. |
| [A1 current interpretation](../../RQ_Specified/A1_transitional_epithelial_state_distinction/README.md) | Regulatory context and later function remain distinct; Naik is conceptual context, not automatic evidence for the registered early-feature/later-output question. |

The reusable sequence is source reading → sample/assay qualification → bounded
reproduction → informative sensitivity → biological interpretation → literature-
qualified follow-up. Each stage may finish with a negative, mixed or held result.
As in DuPage and Wang, the next comparison follows from what the preceding
evidence changes, rather than from a requirement to complete every available method.

## Current disposition and immediate next step

S1M and S2 are coordinator-reviewed and committed. S4 ran from frozen setup
`840bca3`; independent verification passed 7,255,847 checks, including all marker
rows and shared-baseline correlation diagnostics. The coordinator reviewed its
numerical/visual outputs without requesting numerical revision and authorized
bounded S4B after preserving S4. This agent review supplies no human scientific
acceptance.

S4B ran from frozen setup `d547951`; 3,938,436 independent checks and receipt
integrity passed. Coordinator review authorized S3 preparation. S3Q at `6f4fdf0`
qualified core chromosomes while leaving 44 noncanonical aliases and deposited
scale/original-region semantics unresolved. The separately approved
[amendment](S3_AMENDMENT_V1.md) and [method](S3_METHOD_V1.md) were frozen at
`28a62d9`; the adapted [S3 result](S3_RESULTS_V1.md) is now executed, independently
verified and registered, with all prior evidence preserved. The research gate,
20,170 repository checks and 380 local links passed. S3 is preserved at
`8ada940`; coordinator review requested no numerical or figure revision.

The [S5 proposal](S5_PROPOSAL_V1.md) was prepared during extraction under separate
coordinator authorization. It retains source reuse, shared-baseline coupling and
separate functional units, including the F1e source/caption count discrepancy.
[S5M v1](S5M_RESULTS_V1.md) ran from `03d42af`; coordinator review identified
an aggregate zero-flag semantic defect. The authorized [v2 amendment](S5M_AMENDMENT_V2.md)
was frozen at `26d23e8` and has now executed with raw-count semantic verification.
All coefficients, covariance records, ATAC values and Figure 1 are byte-identical;
corrected Figure 2 was visually inspected. [Actual v2 results](S5M_RESULTS_V2.md)
were reviewed without numerical/figure revision; S5F is authorized after local
preservation at `7051b45`. S5F ran from frozen setup `ff0ed97`, with 35 endpoints,
83 groups and 38 contrasts. [Actual results](S5F_RESULTS_V1.md), 18 outputs and the
receipt are registered; 13,821 independent ZIP/XML/Decimal checks passed. All
five figures were reviewed by the technical session and coordinator without a
revision request; final report review is complete. The research gate, 20,267
repository checks and 308 local links passed. The [S6 assessment](S6_DECISION_V1.md)
and [approved S6A design](S6A_DAILY_AREA_DESIGN_V1.md) now specify the first
extension, all source days and missingness rules. Implement/test and freeze the
separate contract before governed execution.
The three candidates to assess are recovered EDF5/6 daily areas, fixed five-marker
D6 RNA QC, and the frozen S3 endpoint at D180. Preserve ATAC zero flags because
other windows/tie mass can change the rank even of a constant local zero.

Execution was authorized through a separate technical session. That service
returned an automatic content restriction during source qualification; a narrower
host-cell/non-infectious-repair continuation also failed before execution. The
[checkpoint](STAGE_STATUS.md) records the incomplete stages and exact next work.
No numerical result or scientific stopping conclusion follows from this failure.

S0 has an initial evidence map. Broader S1 source/functional qualification and
the original retained-region reproduction and S6 remain unfinished. S5F has executed
and has completed coordinator stage review. The separately authorized molecular work did not retry
the restricted extraction. S2 makes no population inference; a separately
justified inferential reproduction remains possible. The independent
bioinformatics study supplies no task dependencies or execution restrictions here.

Remote inspection on 17 November found main at
[`d0429d0`](https://github.com/xorca0711/ravel/commit/d0429d0205fab3e079ea949d0cb0b3a0c1a4a4be),
no open PRs, and passing
[repository checks](https://github.com/xorca0711/ravel/actions/runs/43393470127) and
[research governance](https://github.com/xorca0711/ravel/actions/runs/43393470288).
The older PROGRESS entry saying PR #182 awaits merge is historical; the main
commit verifies that it merged. This planning package preserves that record.
