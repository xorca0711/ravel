# Naik 2017: from inflammatory history to epithelial recall

18 November 2026. Article-local research package, informed by the owner's
Naik Results/Discussion notes. It follows Ravel's established paper-driven
biological research workflow across tissues, organisms and molecular layers.
Inflammatory memory is this paper's topic, not a change to the project's identity.
This source sits outside the ordered roadmap; existing gates and RQs retain
their status. S1M metadata qualification and S2 descriptive RNA analysis are
complete; no global RQ is allocated or scientific acceptance implied.

**Current result:** [S2 v1](S2_RESULTS_V1.md) describes eight D6/D30 libraries over
all 47,729 deposited gene IDs. Among 13,452 genes qualified at either time,
82.58% have a smaller absolute D30 history/control effect; the fraction is
83.65% among 12,052 genes qualified at both times. Median absolute log2 effects
are 0.538 at D6 versus 0.146 at D30 in the union, and 0.504 versus 0.134 in the
both-time subset. The broad pattern therefore survives this low/zero-count
qualification sensitivity. It does not classify genes as biologically resolved.
D30 directions remain uncertain: 73.68% of union genes have a four-library-
combination range spanning/touching zero, and 11.75% change sign with normalization.

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

![D6 and D30 continuous RNA effects and normalization sensitivity](../../analysis/research/runs/naik2017_s2_rna_description_v1/fig02_effect_profiles.png)

Figure 2 shows the union-qualified gene universe. D6 and D30 are separate
cross-sectional contrasts, with two deposited libraries per group. The
[result table](S2_RESULTS_V1.md#continuous-effects-and-expression-qualification)
also displays all genes and the both-time sensitivity: union-only zero/low D30
counts can mechanically reduce regularized effects, and qualification is not
proof of reliable expression in each history group. No gene-based p-values,
confidence intervals or longitudinal pairing are used.

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

The coordinator reviewed S1M and the prospective S2 method without requesting a
revision. S2 ran from frozen setup commit `d4bf26d`; its independent arithmetic
verification and receipt integrity check passed. The coordinator then reviewed
the result and all three figures without requesting numerical changes. This
agent review supplies no human scientific acceptance.

The authorized next bounded stage is S4 recall RNA: qualify the saved D30 baseline
and 6/12-hour wound libraries together, then specify history/control differences
after accounting for the baseline offset. The smaller yet heterogeneous S2
baseline effects make that distinction informative. Shared post-D6 platform/layout
metadata does not establish equal preparation batches or pairing. S3 ATAC source/
region qualification remains a separate later comparison. Neither stage has run;
each requires its own reviewed scope and prospective contract. S4 will include
prespecified exposed Xist/Y-linked marker QC without assigning sex or pairing.

Execution was authorized through a separate technical session. That service
returned an automatic content restriction during source qualification; a narrower
host-cell/non-infectious-repair continuation also failed before execution. The
[checkpoint](STAGE_STATUS.md) records the incomplete stages and exact next work.
No numerical result or scientific stopping conclusion follows from this failure.

S0 has an initial evidence map. Broader S1 source/functional qualification and
S3–S6 remain unfinished. The separately authorized S1M and S2 work did not retry
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
