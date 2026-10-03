# Nb5 prospective analysis development plan

Draft dated 3 October 2026. This is an exposed-data planning document, not a
frozen executable contract. [Source context](NOTE_RECONCILIATION.md),
[data gates](DATASETS.md) and [repository context](REPOSITORY_CONTEXT.md)
are part of its interpretation. No numerical stage has run.

## Scientific candidates and decisions

Use the [eight-branch register](BRANCH_REGISTER.md) and individual cards for
questions, rivals, units, endpoints, decisions and possible RQ development.
P02 retains the owner's microglial direction; the other branches broaden
the source-informed analysis frames. [Source reproduction](REPRODUCTION_SCOPE.md)
is a separate track. No branch is preselected for global RQ promotion.

## Ordered task pipeline

| Stage | Work and planned output | Eligibility and exit decision |
|---|---|---|
| D0 source and note review | This package; reconcile paper, note, deposit identities and current evidence | Done at the documented reading scope; supplement contents and code settings remain open |
| M0 source qualification | Source manifest, input hashes, ID joins, count-layer audit, animal coverage and stage-by-stage eligibility report | New metadata contract and committed code first. Unknown units permit metadata reporting only. |
| R1 bounded source reproduction | Coverage/annotation concordance; one declared marker or composition source panel; one immune-state panel relevant to P02 | Recover exact panel inputs and methods. Compare to a source table using a tolerance justified by rounding, not a desired outcome. |
| E1 composition and expression | Nb5-P01 animal-level estimates and standardization sensitivities | Common cell-type support, known measurement scale and estimable age comparison |
| E2 microglial state assessment | Nb5-P02 per-mouse state/mixture diagnostics and a separate disease-transfer feasibility report | Verified microglia, region and animal identities; no treatment inference |
| E3 lung context | Nb5-P03 fixed-endpoint within-study comparison, or an explicit hold report | Qualified endpoint, population correspondence, ages and independent study/sample identity |
| E4 additional branch qualification and exploration | P04 cross-organ, P05 measurement, P06 clonality, P07 sex and P08 age-shape outputs under separate contracts | Candidate-specific dependencies in the branch register; these are alternative frames, not a required exhaustive scan |
| S1 synthesis | Evidence table linking results to rivals, unfavorable outcomes and next biological discriminator | Verify outputs first. Proposals remain article-local unless the owner records further scientific decisions. |

R1 is intentionally partial. Proposed panel families are coverage (Figure 1),
composition/marker measurement (Figure 2) and immune-state diversity (Figure 4).
Freeze exact panels and source versions before execution. Supplement-only
arithmetic checks are not cell-level reproduction. A lung-only extension cannot
be presented as whole-atlas reproduction. Mutation calling, raw receptor assembly,
whole-atlas reclustering, ageing clocks and bench intervention are outside this
initial queue; each would need its own question, inputs and contract.

E1, E2 and E4 share qualification dependencies but need not wait for a positive
result in each other. E3 and each companion-data comparison are conditional. Missing inputs narrow or stop a stage;
they do not justify choosing the tissue, threshold or score with the best signal.

## Statistical specification to complete after metadata qualification

- Keep technologies separate initially. For eligible raw counts, aggregate
  by mouse, type and assay and use an appropriate count model with library
  normalization. Preserve source-scale reproduction separately. Do not infer
  differential expression from batch-corrected embeddings or integrated values.
- Proposed adult comparison: 3 versus 24 months where both are eligible;
  intermediate ages describe shape, and youngest/oldest groups are distinct
  sensitivity contexts. This choice is not frozen. Qualification may require
  a documented change before outcomes, not silent pooling into young/old.
- Covariates require cross-classified support and a full-rank design. Show
  age-by-sex-by-batch coverage and animal influence. FACS and droplet from a
  shared animal are repeated assays, not independent replications.
- Show all independent-unit points and effect intervals when estimable. Resample
  or split whole animals, including all their tissues and assays together.
  An isolated cell-level p-value does not support population inference.
- Freeze gene filtering, denominator, QC, missingness, minimum cells per unit,
  annotation uncertainty and sensitivity variants with source or measurement
  justification. Insufficient units restrict estimates to description; a
  convenient minimum animal count is not a power calculation.
- Declare separate multiplicity families for genome-wide type-specific tests,
  composition endpoints and disease-signature comparisons. Use an appropriate
  correction within each declared family; bounded marker descriptions remain
  descriptive. No unbounded gene-set search after unfavorable results.
- Meaningful effect margins, independent-unit variance and sample-size/precision
  justification are unresolved. Confirmation cannot begin until these and an
  unexposed outcome source are established. Failure to reject is inconclusive
  unless a separately justified equivalence design exists.

## Prospective contracts and evidence

For M0, copy the repository [contract template](../../analysis/research/contract.template.json)
into a new versioned `config/` path owned by a registered Nb5 candidate. Use
`metadata` as the analysis type, as required by the
[schema](../../analysis/research/contract.schema.json).
Complete source hashes, biological units or explicit unknowns, joins, decision,
rival, exclusions, code hashes, outputs, inference limit and stop rule.
Do not populate unknown fields with placeholder identities or invented counts.

Record `prior_outcome_exposure` as exposed: owner reading, note and agent source
inspection precede these choices. Commit the completed frozen contract and
hash-bound code, register it, then use `research_gate.py preflight`, `run` and
`verify` as documented in [governance](../../docs/RESEARCH_GOVERNANCE.md).
Each later stage needs its own version and explicit exposure record. Design
changes receive a new analysis ID and amendment link; old evidence is retained.

Independent numerical checks must verify ID cardinalities, denominators,
unit counts and one primary endpoint before interpretation. Register receipts
and link compact result tables and figures to them. A successful receipt
records execution, not scientific acceptance or biological replication.

## Planned review artifacts and immediate next steps

Planned figures: animal/age/assay coverage; source-panel concordance;
composition versus within-type effects; microglial state/mixture diagnostics;
a conditional lung-context comparison; and branch-specific displays defined
in the cards. Captions must name units,
denominators, data reuse and interpretation limits. No figure gallery exists yet.

1. Acquire exact supplementary tables and pin the source code version; resolve
   note gene spellings and the GEO/processed-release scope mismatch.
2. Prepare and freeze the metadata contract, acquisition manifest and bounded
   qualification code. Determine which candidate-specific inputs are needed.
3. Run M0 through the governance runner and independently check joins and units.
4. Use the eligibility report to complete the source-reproduction and eligible
   branch contracts. Keep unsupported comparisons on hold. Review primary
   precedents around each exact discriminator before claiming novelty.
5. After execution, synthesize each branch through the RQ-development criteria
   in the branch register; do not allocate a new global question automatically.

The order is dependency-driven, not a commitment to execute every branch.
Owner scientific acceptance, actual experimental access and qualified
functional outcomes remain open.
