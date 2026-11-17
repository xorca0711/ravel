# Naik 2017: from inflammatory history to epithelial recall

17 November 2026. Article-local research planning package, informed by the owner's
Naik Results/Discussion notes. It follows Ravel's established paper-driven
biological research workflow across tissues, organisms and molecular layers.
Inflammatory memory is this paper's topic, not a change to the project's identity.
This source sits outside the ordered roadmap; existing gates and RQs retain
their status. S1M molecular metadata qualification is complete; no gene-effect
comparison has run, no global RQ is allocated, and no scientific acceptance is implied.

**18 November S1M result:** the [current qualification and S2 handoff](S1M_RESULTS_V2.md)
joins 28 molecular libraries and qualifies 16 count tables with 47,729 common
versioned gene IDs. Within-time RNA history contrasts are structurally supported;
cross-time platform/layout differences and exact pool/pairing uncertainty limit
interpretation. Article-local owner `Nk17-P01`, both contracts and receipts are
registered. V1's incomplete title parsing and the [v2 amendment](S1M_AMENDMENT_V2.md)
remain preserved, together with the earlier service restrictions and recovery record.

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

- The annotated version-of-record PDF includes a correction to Figure 2g.
  Figure 3 reports pooled ATAC preparations; Figure 4 and the final RNA Methods
  report four animals per condition in duplicate. Manuscript wording differs.
  Biological units must therefore be qualified by assay and source version.
- The inspected GEO metadata snapshot lists 16 RNA and 12 ATAC libraries.
  It offers RNA at D6, unwounded D30 and 6/12 hours after wounding, and ATAC at
  D6/D30/D180. It does not list wound ATAC or D180 RNA-seq. Separate assays are
  not established same-animal or same-cell pairs.
- Published outcomes and some D6 RNA profiles have already been inspected.
  That exposure is retained honestly; it supplies neither a Ravel result nor
  a required preprocessing method or starting artifact.
- Larsen 2021 already investigates establishment, maintenance and recall in this
  system. Rediscovering AP-1 enrichment or proposing that homeostatic factors
  maintain accessible regions is not, by itself, a new mechanistic contribution.

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

The coordinator completed S1M review without a revision and the owner authorized
the [S2 finite-library method](S2_METHOD_V1.md). Its contract/code are prepared
and input preflight has passed; S2 execution follows the setup commit. D6 is
the acute inflamed condition, and D30 the recovered-baseline history comparison.

Execution was authorized through a separate technical session. That service
returned an automatic content restriction during source qualification; a narrower
host-cell/non-infectious-repair continuation also failed before execution. The
[checkpoint](STAGE_STATUS.md) records the incomplete stages and exact next work.
No numerical result or scientific stopping conclusion follows from this failure.

S0 has an initial evidence map. S1M now supplies the molecular accession/run
crosswalk and processed-count qualification, with exact pool membership and
cross-assay pairing unresolved. Broader S1 source/functional qualification and
S2–S6 remain unfinished. Next is the authorized S2 execution: D6 acute inflamed
and D30 prior-inflammation versus their respective controls, using separate
descriptive library-level comparisons. This stage makes no population inference;
a separately justified inferential reproduction remains possible. The separate bioinformatics study
session supplies no task dependencies or execution restrictions here. Any S2
execution requires its own prospective contract and stage authorization.

Remote inspection on 17 November found main at
[`d0429d0`](https://github.com/xorca0711/ravel/commit/d0429d0205fab3e079ea949d0cb0b3a0c1a4a4be),
no open PRs, and passing
[repository checks](https://github.com/xorca0711/ravel/actions/runs/43393470127) and
[research governance](https://github.com/xorca0711/ravel/actions/runs/43393470288).
The older PROGRESS entry saying PR #182 awaits merge is historical; the main
commit verifies that it merged. This planning package preserves that record.
