# A36 — Current results and dependent holds

10 November 2026. Owner-authorized registration and the source/representation stage are complete. The exact-matrix recipient stage is frozen; cloud runtime restoration/execution is in progress. Later neuronal survival remains unestimated. [Plan](PLAN.md) · [Primary literature and access](LITERATURE_CONTEXT.md) · [Executor handoff](EXECUTOR_HANDOFF.md).

## What narrowed

The added question is broad-bin representation plus within-bin RNA, not discovery of a residual IFN pathway. Navarro Table S3 already reports engineered-IL-10 astrocyte/qNSC interferon-beta response enrichment (rows 104–105). Its three tabs contain treatment–control comparisons, with no direct engineered–WT table. S6A/B show clocks, C–E whole-niche PCA, and F DG STAT1 after behavior. The PDF graphic (p.21), legend (p.22), table labels and relevant source Methods were inspected. Enrichment terms do not measure IFN type or secretion.

The source explicitly could not separate astrocytes/qNSCs or aNSCs/NPCs. Fine NSC-specific attribution is therefore held. Original-bin description remains useful, with within-bin mixture retained as a limitation.

## Executed source and representation stage

Freeze: `6ce40d7`. [Contract](contracts/source_representation_v1.json) · [Immutable receipt](../../analysis/research/runs/a36_source_representation_v1/receipt.json) · [Input hashes](../../analysis/research/runs/a36_source_representation_v1/input_manifest.json) · [Source overlap](../../analysis/research/runs/a36_source_representation_v1/source_overlap.json) · [Complete published S3 rows](../../analysis/research/runs/a36_source_representation_v1/S3_source_rows.tsv).

All 96 original alias/bin recovery rows reconcile between the two retained metadata products and sum to 51,176 cells. The new comparisons use only Young, Control, WT5 and Mut5; eight-alias/six-library and dose/pool limitations remain. The published S3 values are archived with exact sheet/row coordinates; enrichment was not rerun.

| Original bin | Control cells / lineage fraction | WT5 cells / lineage fraction | Mut5 cells / lineage fraction | Mut5–WT5 lineage fraction |
|---|---:|---:|---:|---:|
| Astrocytes_qNSCs | 345 / 38.59% | 572 / 35.20% | 472 / 39.27% | +4.07 percentage points |
| aNSCs_NPCs | 123 / 13.76% | 407 / 25.05% | 285 / 23.71% | −1.34 percentage points |
| Neuroblasts | 426 / 47.65% | 646 / 39.75% | 445 / 37.02% | −2.73 percentage points |

The three-bin denominators are Control 894, WT5 1,625 and Mut5 1,202. The [complete table](../../analysis/research/runs/a36_source_representation_v1/representation.tsv) also retains all-recovered-cell denominators (3,365; 7,760; 6,162), Young context and every original bin. [All contrasts](../../analysis/research/runs/a36_source_representation_v1/representation_contrasts.tsv) retain both denominator definitions.

![Captured-cell representation with both denominators](../../analysis/research/runs/a36_source_representation_v1/representation.png)

Mut5 does not simply increase every captured lineage fraction over WT5. This weakens a uniform-restoration interpretation of these capture fractions and justifies keeping population representation and RNA response separate. It does not refute the independent histological endpoint, establish tissue abundance or estimate a mouse treatment effect. Recovery and tissue counts are different measurements.

Independent verification passed **156** recovery/denominator/rational-arithmetic checks and **4,160** workbook scalar comparisons against direct ZIP/OOXML, for **4,316 checks**. [Verification](../../analysis/research/runs/a36_source_representation_v1/independent_verification.json). The measured figure was visually inspected. Agreement across two reads of shared data is numerical verification, not biological replication.

## Exact-matrix stage and current executor state

The [recipient contract](contracts/recipient_screen_v1.json), [configuration](contracts/recipient_screen_v1.config.json), R extraction and independent Python decomposition were frozen at `0c8f133`. This preserves exposure to the preceding results. It uses original combined bins, four already-exposed IFN-associated markers and twelve identity/context markers, with no aggregate score, relabeling or population P values.

Local inspection found no Rscript and about 2.3 GB available memory, versus the prior 6.7 GB R peak. The existing cloud executor reverified the complete read-only RDS at its expected size/hash and a 16 GiB memory limit, but its temporary R runtime had expired and effective Git attribution had reverted to the host default. The owner authorized resuming that chat and then explicitly authorized the 22,932-byte specification archive transfer after automatic review required payload/destination approval. Runtime restoration and scoped identity correction precede execution. No RNA receipt or successful result is claimed yet.

## Later-output and age feasibility

The bounded primary/source search did not locate an eligible later post-withdrawal D25K/WT/vehicle birthdated neuronal-survival cohort. Inspected Navarro measurements are one-week snapshots; its public object listing concerns RNA. The [feasibility record](../../analysis/research/runs/a36_source_representation_v1/feasibility.json) and [search log](LITERATURE_CONTEXT.md#next-literature-check) specify coverage and limits. Absence of an inspected eligible source is not proof that none exists.

Held estimates require actual exposure cessation and later timing, birthdated survival/maturation measurements, and biological-unit/comparator linkage. A measurement plan is specified in [stage 5](PLAN.md#5-later-output-source-search-and-conditional-execution), with interval, dose, variance, meaningful effect and sample size explicitly unresolved. No unpaired group-average linkage or fabricated cohort is used.

Age modification remains conditional on matched young/old treatment contrasts. An aged-context treatment effect remains legitimate without that design. There is no measured lesion, so no injury-repair analysis is launched.

## Preserved interpretation and next decision

Nn26-P01's direct nonsignificant D25K–WT neural-marker comparisons, nonsignificant direct cognition tests, mixed-dose nesting, RNA exceptions and source discrepancies remain unchanged. A36 does not promote these results, replace the originating candidate, or merge A25/A26/A27/Sx10-P01. The next eligible computation is the exact frozen RNA decomposition; the organizing later-output hypothesis requires its own endpoint evidence. Execution and biological resolution remain separate. No human acceptance or claim-grade change is recorded.
