# Wang public-data stages and review checkpoints

12 November 2026, Asia/Seoul. The owner's selected endpoint is public-data
analysis plus an analysis-ready measurement plan. The
[original plan](ANALYSIS_PLAN.md), [S2–S3 amendment](EXECUTION_AMENDMENT_V1.md)
and [S4 amendment](CONTEXT_AMENDMENT_V1.md) record the prospective decisions.

## Stage status

| Stage | Delivered scope and disposition |
|---|---|
| S0 | Published evidence ledger completed for RNA, lineage, recovery proxies and function. Figure 7 addresses residual deficient Tregs versus its particular depletion comparator. [Evidence ledger](RESULTS_V1.md#s5--what-the-rna-changes-add-to-the-functional-evidence). |
| S1 | Nine deposited libraries linked across count columns, GEO, ENA and BioSample. The source documents mixed control alleles. Mouse/pool and block identity remain unresolved. [Qualification](SOURCE_QUALIFICATION.md). |
| S2 | Adapted finite-library RNA contrast completed with pooled and strict +/+ controls. Exact normalization and S3C library-to-dot mapping remain unavailable. [Day-four results](RESULTS_V1.md#s1s2--the-released-counts-reproduce-the-published-anchor-directions). |
| S3 | Adapted modern mouse Hallmark scores, coverage and sensitivity completed. The published S3B directions were recovered under the adapted ranking. [Breadth results](RESULTS_V1.md#s3--inflammatory-ranks-rise-alongside-opposing-culture-state-patterns). |
| S4 | Five exposed mouse context genes compared across frozen source scales. The human tissue association branch closed because it cannot discriminate recovery, composition or genotype effects in the cultured mouse comparison. [Context results](RESULTS_V1.md#s4--five-exposed-genes-across-separate-activation-contexts). |
| S5 | Published functional evidence integrated with the limits of the RNA measurement. Numerical functional reconstruction needs panel-linked per-animal flow and/or longitudinal tumor records. [Functional evidence](RESULTS_V1.md#s5--what-the-rna-changes-add-to-the-functional-evidence). |
| F1 | Documentary source recovery completed. SRA adds a facility filename lead and the supplement identifies Signal2Noise. The original sample and analysis records remain input-dependent. [F1 source audit](F1_SOURCE_AUDIT_20261112.md). |
| F2 | Frozen Signal2Noise adaptation executed and reviewed. It strengthens the specific inflammatory result and narrows full-collection robustness. [F2 results](F2_RESULTS_V1.md). |
| F3 | Literature-grounded recovery, composition and within-observed-state RNA specification completed and agent-reviewed. Data collection and future contract freeze depend on the design and assay inputs stated in the plan. [Measurement plan](F3_MEASUREMENT_PLAN_V1.md) · [Literature addendum](F3_LITERATURE_ADDENDUM_20261112.md). |

## Checkpoints

- **F1, agent source review passed at `9d9d241`.** The coordinating agent
  independently inspected all nine SRA sample-attribute and original
  filename records and rendered supplement p. 5. The Signal2Noise label,
  phenotype orientation and rank 5609 zero crossing were confirmed.
  Agreement among archive fields comes from a shared submission. [F1 review in the F2 method](F2_METHOD_V1.md#f1-review-checkpoint).
- **F2, agent review passed at `0d92c36`.** The coordinating agent reviewed
  the method, code, report, figure and saved table. Its independent table
  check confirmed all 50 sets scored. Glycolysis, heme metabolism and
  WNT/β-catenin signaling reversed under both control definitions.
  Pooled omissions preserved all directions. Strict +/+ omissions crossed
  zero for bile acid metabolism, heme metabolism and spermatogenesis.
  The 950-score arithmetic verification, receipt and passed provenance
  gate from the technical execution were reused. [F2 verification](F2_RESULTS_V1.md#verification).
- **F3, agent specification review passed at `5f8caee`.** The coordinating
  agent reviewed the comparison, biological units and nested samples, stable
  joins, ancestry/current-FOXP3 distinction, recovery denominators, exposed
  Il10 anchor, estimands, missingness and stop rules, literature attribution
  and remaining input requirements. No blocking issue was identified for an
  analysis specification. The FOXP3-positive compartment can contain finer
  state mixtures; its RNA contrast is conditional, not a direct genotype
  effect. Precision, assay feasibility and collection remain unqualified.
  The technical stage's repository/provenance checks were reused; no numerical
  analysis was repeated for this review. These checkpoints carry no human
  scientific acceptance or certification of laboratory readiness.

After recording the final checkpoint, repository validation passed 19,428
checks and `git diff --check` found no whitespace errors. The review changed
documentation only; frozen numerical evidence was preserved.

## Held dependencies and next decision

| Question | Specific input needed |
|---|---|
| Population inference from GSE114298 | A verified library-to-mouse or disjoint-pool crosswalk, actual control alleles and processing assignments, followed by an estimability and precision check. |
| Exact S3B–C replay | Original expression input, phenotypes, mapping and run settings for S3B, and panel membership, library-to-dot mapping and normalization for S3C. |
| Recovery/composition versus observed-state RNA | Same-preparation viable input and absolute recovered counts, stable ancestry and validated current FOXP3 state, and matched total-lineage and state-specific RNA. A technical crosswalk alone does not supply these measurements. |
| Numerical functional reconstruction | Panel-linked raw flow and gates/denominators or individual tumor trajectories and cohort/treatment assignments, depending on the published endpoint. |

The assessed public sources provide counts or separate functional
measurements without the required linkage. Another calculation on the
existing bulk counts cannot recover viable cell numbers or state-specific
RNA. The [local unsent author request](F1_AUTHOR_REQUEST_DRAFT.md) remains
available if recovery of original records is pursued. Functional,
mediator and recipient assays are conditional options for different
questions. The selected public-data analysis and measurement-plan scope is
complete and reviewed. Reopen a dependent stage only when its specified inputs
become available or the owner chooses a different scientific comparison.

## Subsequent public-gap and tumor review

The [12 November public-gap review](PUBLIC_GAP_REVIEW_20261112.md) and [Bockman full-main-paper read](BOCKMAN_FULL_READ_20261112.md) update A33–A35 and the conditional tumor extension. They qualify published model/assay precedents and delimit missing measurements; no new functional estimate or numerical run was qualified. S1–S5/F1–F3 dispositions above are unchanged.
