# Nb5 extension feasibility before RQ derivation

3 October 2026. **Targeted extensions are plausible and useful before formal
RQ derivation.** Each extension still needs a bounded candidate question before
execution. This is a feasibility assessment, not a new biological result or an
authorization record for every proposed method. No extension below has run.

The current [results](RESULTS.md) already separate eight article-local branches.
The useful next analyses should distinguish their strongest remaining rivals
and identify what evidence a later RQ would need. Exhausting every branch or
finding a positive result is not a prerequisite for RQ development.

## Extensions supported by the current evidence

| Extension and branch | Question it could resolve | What is feasible now | Decision it informs |
|---|---|---|---|
| Mouse influence and capture sensitivity, P01/P05 | Does one animal or unequal captured-cell yield dominate a fixed contrast? | Leave one mouse out of the existing prespecified summaries; retain every deletion and undefined estimate. Conditional cell subsampling can assess capture-count sensitivity, but cannot simulate sequencing depth from normalized values. | Describe a stable observation, identify a fragile one, or require more independent animals. This is sensitivity analysis, not external validation. |
| Composition accounting on a common denominator, P01/P05 | How much of the observed RNA difference persists when comparing the same supported cell types? | Compute observed and standardized summaries on the same common-type cell universe, explicitly retain omitted cell mass, and inspect within-type mouse estimates. Preserve the same fixed genes and age contrast. | Distinguish a composition-related measurement question from a within-population candidate; neither establishes absolute abundance or causality. |
| Tissue-aware repertoire sampling, P06 | Could changing tissue contributions explain the older reconstructed repertoire's concentration? | Audit age-by-mouse-by-tissue support; then compare supported tissues with within-mouse clone identities and conditional common-depth calculations. Report missing strata and clone sharing across tissues. | Determine whether a tissue-mixture rival remains sufficient, or whether a bounded within-tissue concentration question merits an independent test. |
| Source identity and annotation bridges, P02/P08 | Are apparent states or missing renal populations consequences of release and annotation differences? | Reconcile cell IDs, original/reannotated labels and source processing versions. Preserve unmatched observations and missing lineage labels. | Establish a defensible population and expression scale before state or nonlinear-age modeling. This can end in an informative hold. |

Mouse-level inference matters because cells from one animal do not supply
independent biological replicates. This principle is supported by
[Squair et al., Nature Communications 2021](https://www.nature.com/articles/s41467-021-25960-2).
The existing normalized values are suitable for the stated descriptive
extensions; they must not be rounded or rebranded as raw counts for a count model.
Small mouse counts and sparse captured types remain precision limitations.

## Extensions that require another qualification step

- **P02 microglial state versus mixture:** first qualify all-age unintegrated
  expression, animal identities, brain sampling and processing differences.
  Exact published cluster correspondence is necessary for claiming that figure's
  reproduction. A separately defined state analysis could instead use its own
  frozen definitions once the source and scale are qualified. If model comparison
  is attempted, train transformations and definitions within training mice and
  assess held-out mice. Reused disease genes cannot serve as independent support
  for a state defined using those same genes. A new embedding alone does not
  resolve the state-versus-mixture question.
- **P03 injury context and P04 organ comparisons:** qualify compatible
  populations and independent study units before transport claims. A broad
  shared-age signature scan already has substantial prior art in
  [Zhang et al., eLife 2021](https://elifesciences.org/articles/62293) using the
  same atlas; an additional RQ needs a more specific unresolved discriminator.
- **P07 sex and P08 age shape:** the planned 3-versus-24-month sex interaction
  lacks old females. Some 3-versus-18-month strata contain both sexes, but that
  is a different estimand requiring a new design, not a replacement selected
  after inspecting effects. Renal annotation discontinuities and cross-sectional
  cohort/survival differences must be addressed before fitting an ageing curve.

These dependencies describe analysis readiness, not a ranking of biological
importance. All eight branches and every existing global RQ remain available.

## Transition into an RQ

1. Name the candidate decision, biological unit, endpoint and strongest rival.
   Review the specific primary-source precedent and the current source mismatch.
2. Freeze a small extension contract before numerical execution, retaining prior
   outcome exposure, exclusions and a stopping rule. No arbitrary effect margin
   or confirmatory sample size is inferred from the current small datasets.
3. Report the fixed results, mouse influence and remaining alternatives, including
   null outcomes and failed eligibility. Do not expand a failed analysis solely
   to obtain a positive result.
4. Write a short synthesis identifying the residual biological gap, a test that
   could oppose it, an independent evidence source and actual access/precision
   requirements. Propose one disposition: measurement check, existing-RQ
   refinement, distinct-RQ proposal or hold.
5. Follow the repository's recorded review and registration procedure. A new
   global ID, retain/reject decision or claim grade does not follow automatically
   from executing an extension. Evidence stays in this article package until
   accepted question-specific work belongs in `RQ_Specified/`.

The practical next scope is the supported sensitivity and denominator work,
alongside the microglial source-qualification step. Stop when the remaining gap
and an informative independent test are clear; a formal RQ should not be delayed
by an open-ended catalogue of scores or models. See the
[branch register](BRANCH_REGISTER.md) and
[research governance](../../docs/RESEARCH_GOVERNANCE.md) for ownership and gates.
