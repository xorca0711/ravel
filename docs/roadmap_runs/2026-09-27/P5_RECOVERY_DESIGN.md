# P5 — A discriminating recovery experiment

**Status: source-informed design completed; experimental execution requires new compatible data.** This package produces a concrete allocation, endpoint and contrast specification. It does not report an experiment that has not happened.

## What is already known, and what the extension would test

Choi's study already reports recovery of late AT1-marker expression after a 14-day IL1B exposure followed by 7 days of withdrawal. Repeating that marker observation would be a replication, not a new mechanism. The same work distinguishes early PDPN/HOPX expression from later markers such as CAV1. [Primary Results, Figure 7](https://pmc.ncbi.nlm.nih.gov/articles/PMC7487779/).

The proposed extension tests **fibroblast-specific IL1R1 reception during resolution**, using traced late-AT1 yield and survival instead of an RNA-score decline. Keeping the receptor intervention after entry prevents an effect on initial state formation from being mistaken for an effect on recovery. This requires measured intervention onset; a constitutive deletion would answer a different question.

## Allocation and independent units

Use a defined same-species AT2–fibroblast culture with lineage-labelled epithelium. Each independent preparation is allocated across all six arms, with randomized positions, matched handling and blinded scoring. Aliquots are technical wells, as P1's recovered protocol illustrates; they do not increase biological n.

| Exposure schedule | Fibroblast IL1R1 intact | Fibroblast IL1R1 selectively suppressed after entry |
|---|---|---|
| Exposed days 0–14; continued through day 21 | Continuous/intact | Continuous/suppressed |
| Same exposure days 0–14; withdrawal to day 21 | Withdrawal/intact | Withdrawal/suppressed |
| Unexposed through day 21 | Baseline/intact | Baseline/suppressed |

All arms receive matched handling/induction controls. Direct epithelial reception remains intact and is measured, not assumed unchanged. Record source identities, medium ligands, baseline support and viability. An intervention that cannot be restricted to fibroblasts or cannot act after entry fails this design's gate.

## Endpoint and the two decisions

The primary endpoint is viable traced **late-AT1 yield per initial labelled input** at day 21, with a prespecified independent AGER/CAV1 protein and morphology gate. Absolute surviving descendants and mature fraction among survivors are separate secondary measurements, because a fraction alone can increase through selective loss. This supports mature contribution; a functional-repair claim still needs a separate validated functional endpoint.

1. **Schedule effect:** withdrawal minus continued exposure in intact cultures.
2. **Recipient modification:** the withdrawal-minus-continuous contrast in recipient-suppressed cultures minus that contrast in intact cultures.

The second is a direct interaction, not a comparison of two p-values. Keep both in one declared multiplicity family if tested inferentially. Independent-unit variance and a useful effect/precision criterion must determine sample size before the main outcomes are compared; no arbitrary well count is substituted.

Measure the actual exposure after withdrawal and target engagement after intervention. A common harvest age and exposure history before day 14 make the schedule contrast interpretable, but it is still not a pure duration effect independent of cumulative dose or recency. The [machine-readable design](P5_withdrawal_design.json) records the remaining launch requirements.

## Related questions remain distinct

- **A3:** obtain age/harvest-matched injured and sham animals. Same-cell persistence additionally needs tracing; a late population comparison cannot supply it.
- **A4:** obtain validated signalling history and current activity, with washout and a later response. Co-detection is not a temporal switch.
- **A6:** define comparable macrophage states independently of the tested programme; keep composition and within-state contrasts separate. A nonsignificant contrast does not establish a composition-only explanation.

## Decision

Advance only when the selective post-entry intervention, independent preparations, withdrawal verification and independent late phenotype are available. Failed engagement or inadequate survival is inconclusive. A supported C1 does not establish C2. A supported C2 does not identify the downstream mediator. Neither supports function that was not measured.

This package closes the design ambiguity about induction versus resolution and distinguishes the extension from published withdrawal evidence. It does not close the biological gap without new data.
