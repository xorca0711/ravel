# Review of A16, A1, A10, A8 and A14 deliveries

**Date:** 29 September 2026

**Status:** Baseline review preserved; corrections applied 29 September 2026

**Reviewed revision:** 5d4619da3a3d7ebe8bfc38de71241b44a588751b (origin/main)


## Summary

The findings and line references below describe the reviewed baseline revision.
See [CORRECTIONS.md](CORRECTIONS.md) for their resolution and the current A1
execution decision. The acceptance table below is the original review verdict.

All five requested documentation packages exist. A10 meets its proposal's "Now" item.
A16, A1, A8 and A14 have delivered substantial organizing work, but the issues below
prevent accepting their current framing and decision rules without correction. These
deliveries establish documentation and evidence boundaries; they do not validate the
biological hypotheses or make the proposed primary tests executable.

The review covers the final merged state of [PR #111](https://github.com/xorca0711/scRNA_seq/pull/111),
[PR #112](https://github.com/xorca0711/scRNA_seq/pull/112),
[PR #113](https://github.com/xorca0711/scRNA_seq/pull/113) and
[PR #114](https://github.com/xorca0711/scRNA_seq/pull/114). All four are merged.
Overlapping files in the stacked PRs were reviewed once at the final revision.

| Question | What is established | Acceptance of the "Now" item |
|---|---|---|
| A16 | Dated amendment, supersession ledger, successive evidence states and two figures from tracked tables | Delivered; attribution wording still needs correction (R2) |
| A1 | Comparison matrix, 27-branch inventory and supporting roles | Partial: the nominated test lacks its required regulatory predictor (R1); shared inventory needs synchronization (R3) |
| A10 | Consolidated timing, units, plate/target dependence, preparation uncertainty and absolute/relative performance | Meets the documentation item; independent-preparation validation and prospective prediction remain unresolved |
| A8 | Own workspace, shared 29-record inventory and a sound explanation of why overlap motivates a measurement check | Delivered; inventory and timing gate need correction (R3–R4) |
| A14 | Separate H1/H2 populations, outcomes, rivals and decisions | Delivered; directional decision and evidence/design restrictions need correction (R5–R7) |

Acceptance is judged against the [proposal](../2026-09-28-rq-development-proposal/PROPOSAL.md),
not against completion of its later analyses.

## Findings

### R1 — P1: A1 nominates an RNA-to-outcome linkage as its regulatory primary test

[COMPARISON_MATRIX.md](../../../RQ_Specified/A1_transitional_epithelial_state_distinction/COMPARISON_MATRIX.md),
lines 59–81 and 134–135, specifies eight day-7 RiboTag RNA features, with a regulatory
feature entering only if subsequently measured. It nevertheless says that only
co-measurement is missing and changes the gate to early regulatory **or** RNA measurement.
The proposal asks whether a specified early regulatory feature adds information
beyond early RNA. The shared inventory itself preserves the stricter regulatory
**and** RNA gate and explicitly excludes RNA-only replacement (lines 179–186).

Linking those RNA features to day-14 AGER could support an RNA-to-outcome question.
It cannot, as currently specified, establish information from a distinct regulatory
measurement beyond RNA. No concrete regulatory predictor has been nominated, and
feasible linkage of the early and late measurements is not established by their
existence in separate cohorts.

**Correction:** name the regulatory measurement, its RNA comparator and a feasible
unit-level linkage before accepting this as the primary test. Otherwise retain
IRE1-alpha as a candidate supporting linkage and label the decisive regulatory
test as still unspecified. Restore "and" in the gate and remove "only co-measurement
is missing." Do not run a replacement RNA-only analysis.

### R2 — P2: A16 still turns attenuation into positional attribution

The amendment in [RATIONALE.md](../../../RQ_Specified/A16_cd177_state_attribution/RATIONALE.md),
line 201, concludes that "position as measured explains much, not all." Its own
boundary at lines 239–242 says attenuation is not an explained causal fraction and
substantial imbalance remains. At k = 10, the priming raw contrast changes from
1.2558 to 0.4098 and from 1.3318 to 0.3151, while maximum absolute PC imbalance
remains 0.6249 and 0.5210.

These establish attenuation under the recorded matching procedure. They do not
identify how much of the marginal association is biologically explained by
position. The amendment's conditional interpretations may remain hypotheses, but
the ledger's affirmative explanation is stronger than the corrected evidence.

**Correction:** describe the observed attenuation and unresolved attribution
consistently, including the rationale summary. Keep both positional and
non-positional explanations open. In the C3 figure, "most control genes" would
also be more precise than "best-powered"; control count is not a power analysis.
No new parameter sweep is required.

### R3 — P2: The shared inventory is not synchronized with evidence already recovered

[A1_A8_A14_OUTCOME_INVENTORY.md](../../../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/A1_A8_A14_OUTCOME_INVENTORY.md)
contains three consequential inconsistencies:

- **O12, line 44 and lines 110–115:** says the 22 HPCS source labels are not verified
  animals. [REGULATORY_FATE_REPORT.md](../../../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/REGULATORY_FATE_REPORT.md),
  lines 31–58, already resolves 22 distinct animals through Supplementary Table 4.
  Library/chase confounding and the missing current reporter remain; the identity
  hold does not.
- **O26, line 58 and lines 160–164:** remains a placeholder awaiting A10's timing
  statement even though that statement is delivered in the reviewed revision.
- **O27, lines 59 and 165–168:** describes the mature outcome measurement as entirely
  missing. O2 and O3 already record measured, non-RNA mature AT1 endpoints; what is
  missing is a compatible link to the required predictors. The stronger "missing
  entirely, not merely unlinked" wording also appears in the comparison matrix
  at line 111.

The 29 rows include unavailable requirements and non-mature readouts; they are not
29 measured mature-epithelial outcomes as the matrix introduction calls them.
Treating these distinctions as interchangeable can send A8/A14 sourcing toward
already solved problems or unnecessarily new measurements.

**Correction:** classify each row by measurement availability, biological-unit
verification, predictor linkage, timing and question-specific eligibility. Bind
O26 to the completed A10 statement; update O12 without removing its remaining
design limitations; describe O27 as missing an eligible linked dataset. Use
"29 inventory records" for the count. Lack of EdU/BrdU documentation should not
erase the genetic lineage-labelled endpoints explicitly present in O2/O3.

### R4 — P2: A8 silently narrows association-or-prediction to prospective prediction

[PLAN.md](../../../RQ_Specified/A8_maturation_component_at1_contribution/PLAN.md),
lines 46–65, requires the predictor to precede the endpoint and excludes every
concurrent design. However, the [A8 register card](../../../RESEARCH_QUESTIONS.md#a8),
lines 487–495, permits incremental **association or prediction**; the proposal
requires specified timing, not necessarily earlier timing. The new README says it
does not change that card.

A concurrent, independently measured mature endpoint could address incremental
association while being unable to address future prediction. The new rule
discards that legitimate branch without recording the scope change. This does
not make A10 automatically eligible: its size endpoint and unresolved preparation
identity remain separate limitations.

**Correction:** separate an association contract from a prospective-prediction
contract, or explicitly record a justified narrowing to the latter. Synchronize
the README, rationale, plan and JSON contract. Retain noncircular outcomes and
independent biological units in either branch.

### R5 — P2: A14's H1 decision accepts the opposite of its directional hypothesis

[RATIONALE.md](../../../RQ_Specified/A14_withdrawal_recovery_and_reception/RATIONALE.md),
lines 25–26, hypothesizes that longer exposure **reduces** mature recovery.
Lines 52–54 accept "a recovery difference" as support. The same rule is encoded in
[PLAN.md](../../../RQ_Specified/A14_withdrawal_recovery_and_reception/PLAN.md), line 42,
and [a14_question_contract.json](../../../RQ_Specified/A14_withdrawal_recovery_and_reception/config/a14_question_contract.json),
line 42.

As written, greater recovery after longer exposure would also be counted as
support, although it contradicts H1's stated direction.

**Correction:** make the decision direction-specific, explicitly classify a
reverse effect, and distinguish an imprecise estimate from a precise absence of
a meaningful decrement. If a nondirectional hypothesis is intended, amend the
hypothesis consistently instead. Preserve the viability, withdrawal and lineage
interpretation checks.

### R6 — P2: Separate A14 decisions do not require a blanket ban on joint designs

[RATIONALE.md](../../../RQ_Specified/A14_withdrawal_recovery_and_reception/RATIONALE.md),
lines 90–98, says a single factorial would confound the two questions.
The JSON contract, line 66, prohibits combining them into one experiment.

The example compares two arms that differ in both factors, which is confounded.
That is not a general property of a factorial design: separately varying and
adequately observing both factors can identify separate contrasts and their
interaction. Separate hypotheses, controls and decisions do not logically require
separate experiments.

**Correction:** prohibit inseparable exposure/reception contrasts, not every joint
design. Keep H1 and H2 independently interpretable and independently eligible;
assess any proposed joint design for its actual identifiability and replication.

### R7 — P2: A14 rules out existing data without establishing their absence

[README.md](../../../RQ_Specified/A14_withdrawal_recovery_and_reception/README.md),
lines 78–79, says the gap is not a dataset that might exist somewhere, and
[PLAN.md](../../../RQ_Specified/A14_withdrawal_recovery_and_reception/PLAN.md),
lines 112–114, makes the next step a capability question rather than a data-search
question. The same plan explicitly states that no public-archive search under the
eligibility conditions has been performed.

The need for a perturbation/withdrawal contrast specifies the required evidence.
It does not establish that suitable observations must be newly generated.

**Correction:** state that no eligible existing dataset has been identified in
the reviewed evidence. Allow a bounded search or author-provided data to satisfy
the same contract; consider new data generation only if that route remains
unresolved. Do not lower the endpoint or biological-unit requirements.

## Verification and limits

- Repository validation passed **4,427 checks**, including local Markdown links,
  tracked JSON parsing and selected numeric/claim bindings.
- All **10 recorded SHA-256 comparisons** passed: A16's script, three source
  tables and four image files; A10's script and source table.
- Both plotting scripts parsed successfully. Their selectors were inspected;
  the scripts were not rerun and the scientific models were not refitted.
- A16's k = 10 priming contrasts and maximum residual PC imbalance were checked
  directly against the corrected tables. Its C3 figure uses nine primary entries;
  control counts and displayed null fractions agree with the source table.
- A10's eight selected model/plate rows match every plotted RMSE and R-squared
  value in its run record. The larger model has lower RMSE on all four plates
  but negative held-out-mean R-squared on three; the four well counts sum to 885.
- The three PNG figures were visually inspected. The inventories contain
  27 branch IDs and 29 outcome/requirement records.
- No new external literature or dataset search, biological analysis or
  feasibility experiment was performed. Local evidence supports the identified
  document contradictions; it does not prove that suitable future datasets exist.

## Next steps

1. Correct A1's primary-test specification and synchronize the shared inventory.
2. Correct A16's attribution language, A8's timing scope and A14's decision/design
   rules across their prose and contracts.
3. Retain A10's completed documentation as the current timing/units reference.
4. Recheck only changed contracts, affected cross-links and numerical wording.
   These review findings do not require rerunning the existing scientific analyses.
