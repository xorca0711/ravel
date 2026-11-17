# Naik 2017: from inflammatory history to epithelial recall

18 November 2026. Article-local research package, informed by the owner's
Naik Results/Discussion notes. It follows Ravel's established paper-driven
biological research workflow across tissues, organisms and molecular layers.
Inflammatory memory is this paper's topic, not a change to the project's identity.
This source sits outside the ordered roadmap; existing gates and RQs retain
their status. S1M qualification, S2 baseline RNA and S4 recall RNA descriptions
and S4B reference sensitivity are complete; no global RQ is allocated or scientific acceptance implied.

**Current result:** [S4B v1](S4B_RESULTS_V1.md) holds S4 normalization, wound means
and qualification fixed while changing only the observed baseline reference.
Adjusted signs change for about 15% of the W6 union and 17% of the W12 union;
similar sensitivity remains in baseline-expression intersections. Col1a2's W12
adjustment changes direction under one reference. Neither alternative is a
preferred correction, verified sex stratum or matched sample comparison.

The preserved [S4 v1](S4_RESULTS_V1.md) separates post-wound history/control
RNA differences from the D30 baseline offset on one common 12-library scale.
Absolute post-wound differences exceed baseline for 53.72% of the W6 and 46.71%
of the W12 expression unions; about 82% of adjusted library-combination ranges
include zero. Normalization changes 13.67%/19.29% of adjusted signs. Similar
findings remain in baseline expression intersections. This is a mixed relative
RNA description, with no inference of uniform amplification, kinetics or repair.

Prespecified marker QC identifies two baseline libraries with near-zero Xist
and substantial counts for four Y-linked genes despite uniform recorded female
metadata. Both baseline histories contain this profile; the discrepancy limits
interpretation but alone does not prove every history contrast biased. No sex
assignment, pairing, exclusion or correction was made. S4B now demonstrates
numerical baseline-reference dependence without identifying its biological cause.

The preceding [S2 result](S2_RESULTS_V1.md) found smaller absolute D30 differences
for 82.58% of 13,452 union-qualified genes and 83.65% of 12,052 both-time-qualified
genes. Those source measurements remain unchanged; the new baseline QC adds a
further limitation to their biological interpretation, not a resolved/persistent
gene classification. All 47,729 deposited gene IDs remain in both stages.

[S1M](S1M_RESULTS_V2.md) owns the accession/unit qualification. D6 is **acute
inflamed**, not recovered baseline; D30 is recovered-baseline history. Within-time
comparisons share platform/layout, while cross-time technical differences and
exact pool/pairing uncertainty remain. Owner `Nk17-P01`, contracts and receipts
are registered. Incomplete S1M v1 parsing, its [amendment](S1M_AMENDMENT_V2.md)
and the earlier service/recovery history remain preserved.

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

S4B ran from frozen setup `d547951`; 3,938,436 independent arithmetic checks and
receipt integrity passed. The coordinator reviewed its [result](S4B_RESULTS_V1.md)
and all four panels without numerical revision and authorized S3 preparation and
source qualification. S3 biological comparison and S5 integration have not run. All original and
alternative outcomes remain side by side, with unchanged example selection.
The original eight D6/D30 tracks and a tested supported project-local reader are
[prepared](S3_RUNTIME_V1.md). [S3Q metadata qualification](S3Q_METHOD_V1.md) has
passed input preflight and awaits setup freeze/execution. Return its source/header,
scale and region findings with a concrete S3 estimand for review before biological
execution. Installation and source transfer supply no chromatin comparison.

Execution was authorized through a separate technical session. That service
returned an automatic content restriction during source qualification; a narrower
host-cell/non-infectious-repair continuation also failed before execution. The
[checkpoint](STAGE_STATUS.md) records the incomplete stages and exact next work.
No numerical result or scientific stopping conclusion follows from this failure.

S0 has an initial evidence map. Broader S1 source/functional qualification and
S3/S5/S6 remain unfinished. The separately authorized molecular work did not retry
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
