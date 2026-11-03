# Full primary and moderate biological screening follow-through

3 November 2026, Asia/Seoul. Owner-requested scope: all 14 grouped rows in the
earlier primary/moderate recommendation, covering **21 canonical RQs plus
Wg-P06**. The owner additionally requires a structured screening sequence,
rationale and biological implications for each before actual execution.
This does not add other portfolio questions or authorize their retirement.

The follow-up branch is `codex/full-priority-screening-20261103`, starting at
`f54ad29`. The earlier [PR #162](https://github.com/xorca0711/ravel/pull/162)
is preserved separately; the follow-up is [PR #163](https://github.com/xorca0711/ravel/pull/163),
stacked on #162. Fetched main is `445a0ca`. Existing results, exposed
outcomes and failed comparisons remain authoritative. Execution and independent
review are recorded below; planning completion is not biological acceptance.

## Sequence applied to each question

1. Read the current result/amendment, canonical question and closest published
   precedent. Identify what the requested target screen actually asks; an
   adjacent reference result does not complete a different biological screen.
2. State the biological decision, named target or fixed candidate set,
   comparison, measured endpoint, biological unit, exposure and strongest
   alternative. Refresh primary literature only where the new comparison or
   insufficient existing context requires it.
3. Specify ordered steps and what a supportive, null/mixed or inconclusive
   result would mean. Define support/stop rules before target outcomes. Keep
   a descriptive screen distinct from the later causal or functional test.
4. The coordinator reviews the plan's rationale, actual inputs, novelty limits
   and outcome-to-decision mapping **before** numerical execution. A missing
   functional assay need not prohibit an informative RNA screen, but RNA must
   not be presented as the missing function.
5. Freeze the reviewed code, configuration dependencies and contract; execute
   through the repository runner. Reuse valid completed work rather than
   repeatedly calculating the same result. Do not lower an existing threshold
   or add targets to obtain a preferred result.
6. Verify units, arithmetic and receipts; inspect measured figures; reconcile
   the result with the hypothesis and alternatives. Update the owning RQ or
   article README/context and this ledger. Retain all unfavorable outcomes.

Each owner has its own plan and disposition even when related questions share
data. A completed screen, a completed limited reference, and an unresolved
biological comparison are different outcomes. Missing measurements receive a
specific hold and reopening condition; they are not marked as answered.

## Full requested coverage

| Tier | Owner | Requested biological focus | Current coordination status |
|---|---|---|---|
| Primary | A31 / Nb4-P09 | GRIA1-associated machinery and fibroblast-state specificity; SCN7A contextual | Nine-gene screen executed and reviewed; GRIA1 enrichment persists, partners are heterogeneous |
| Primary | A5 | Regulatory/effector subsets within the already-defined developmental component | All99-member attribution executed and reviewed; heterogeneous contributions, partial role annotation |
| Primary | A12 | Epithelial receptor, inhibitory/decoy and downstream recipient context | Original IL-1 component screen executed and reviewed; mixed component directions, no causal attribution |
| Primary | A3 / DY1-P02 | Induction/maintenance versus continuing input/composition; ARG1 separate effector | Fixed-target repeat-source view executed and reviewed; target responses differ, maintenance unmeasured |
| Primary | A32 | Myeloid ARG1, matrix and epithelial outcomes that may diverge | Completed bounded RNA screen reused; joint functional question unresolved |
| Primary | Wg-P06 | Substrate supply, routing and signaling alternatives | Completed source channels reused; availability/routing/signaling map integrated |
| Moderate | A1 | A regulatory feature distinguishing maturation competence beyond RNA state | Completed screen/context review; source-specific candidate map and missing outcome linkage |
| Moderate | A8 | Frozen maturation component versus shared transition and later output | Selected-panel attribution executed and reviewed; opposing member signals and seed-sensitive totals, later fate unmeasured |
| Moderate | A14 | Exposure duration and recovery after cessation; fibroblast reception separate | [Source intake complete](A14_SOURCE_MANIFEST.md); exact qPCR values and preparation/experiment map unavailable in checked attachments |
| Moderate | A4 | Wnt history versus current activity and later inflammatory response | Completed screen/context review; current RNA/accessibility do not recover historical lineage |
| Moderate | A7 | Starting state dependence beyond broad CEBPA identity loss | Completed screen/context review; baseline interaction unidentifiable in pooled post-treatment samples |
| Moderate | A19 | Starting state/history, maturation and retained reserve | Completed screen/context review; Fzd-specific reversibility and functional reserve unmeasured |
| Moderate | A9 | AREG recipient competence beyond ligand availability | Six-gene screen executed and reviewed; EGFR/ERRFI1 lower in all19 supported Myofibroblast comparisons, function unmeasured |
| Moderate | A15 | ITGB6-associated active TGF-beta versus total ligand | Completed screen/context review; direct ligand-activity measurement absent |
| Moderate | A20 | Fzd2 versus Fzd1 fibroblast support and early-pool/later-output distinction | Completed screen/context review; direct receptor/functional-output comparison absent |
| Moderate | A21 | Fzd4 vascular maintenance, survival and regeneration | Completed reuse/source refresh; receptor-specific adult-repair endpoints absent |
| Moderate | A22 | Focal NKX2-1-dependent extracellular output | Completed screen/context review; seven focal RNA effects already available, protein output absent |
| Moderate | A23 | SLC34A2-associated entry versus persistence | Completed screen/context review; static measurements cannot separate rates |
| Moderate | A18 | Neighbor expansion versus identity before molecular-channel nomination | Completed screen/context review; linked spatial biological units absent |
| Moderate | A27 | CD8 state concentration versus redistribution and receptor ascertainment | State/source-representation screen executed and reviewed; all four main naive/effector age contrasts unsupported |
| Moderate | A28 | Regulatory versus inflammatory Th17 arms | Completed screen/context review; distinct functional outputs remain unmeasured |
| Moderate | A29 | PEP, stress and biosynthetic-demand alternatives around PGAM | Completed screen/context review; discriminating metabolite/signaling measurements absent |

The existing technical chat prepares the [per-owner plans](PLANS.md); the
[coordinator review](COORDINATOR_REVIEW.md) precedes numerical dispatch. The
[technical ledger](TECHNICAL_LEDGER.md) records actual readiness/execution.
The bounded [A21 recent-source refresh](A21_SOURCE_REFRESH.md) distinguishes
new endothelial-repair precedents from the missing Fzd4-specific comparison.
The [A12 target-source review](A12_TARGET_SOURCE_REVIEW.md) fixes descriptive
roles for the five added transcripts without inferring pathway activity.
The [A9 receptor-context review](A9_TARGET_SOURCE_REVIEW.md) distinguishes
potential partners and feedback-associated transcripts from measured competence.
No author contact, controlled
access, paid compute, new plugin installation, model redesign or policy change
is included merely because a tool supports it.

## Completion and biological implications

All 22 owners have a reviewed sequence and a final disposition: seven new
numerical screens, fourteen reused completed screens, and one bounded source
intake (A14). All seven new runs passed independent result review. This completes
the eligible screening work, not the missing functional or causal comparisons.

- A31 retains a focused GRIA1-associated fibroblast context without a uniform
  receptor-partner programme. A9 separates recipient RNA contexts but does not
  measure AREG responsiveness.
- A5 retains a heterogeneous developmental component; partial role annotation
  does not support calling the full component a coherent regulatory programme.
- A3 separates target-specific repeat responses; A12 separates opposing IL-1
  index components. Neither screen identifies a persistence-maintaining mechanism
  or causal recipient competence.
- A8 exposes opposing member contributions and seed-sensitive late-panel totals.
  A27 cannot estimate the main naive/effector state comparison under its fixed
  mouse-support rule; mixed/indeterminate estimates do not attribute redistribution.

Exact missing measurements and reopening conditions remain with each owner in
[the plans](PLANS.md) and [technical ledger](TECHNICAL_LEDGER.md). No thresholds
were relaxed, failed result replaced, or human retain/reject decision invented.

[Integration validation](VALIDATION.md) records the required checks and exact
base revisions; all passed, with the host-specific symlink test left to Linux CI.

## Tools checked for this task

Connected NGS Analysis Workbench returned 12 workflow definitions, including
RNA-seq, ATAC-seq, CUT&RUN/ChIP-seq and STARsolo counting. It lists one local
compute target; runtime readiness was not assessed in this capability check.
Processed-data jobs should keep the existing repository runner and required
contracts; raw-read workflows are considered only for an actual analysis need.

Locally available NCBI Entrez/GEO, CELLxGENE and BioStudies skills can support
source recovery. Literature/citation skills support bounded primary-source
reviews; Scanpy and NGS design/result skills support appropriate cell-state and
replicate-aware analyses. Notion/GitHub tools can reconcile notes and source
code. BioRender is a presentation aid, not a source of quantitative evidence.

Plugin searches on 3 November for `PubMed`, `CELLxGENE` and `bioinformatics`
returned no dedicated matches. A broader combined search returned unrelated
services; none was recommended or installed. Existing tools are sufficient to
continue. Tool availability does not establish valid input identities, runtime
readiness or functional measurements.
