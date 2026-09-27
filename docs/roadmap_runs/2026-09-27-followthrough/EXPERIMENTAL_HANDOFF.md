# Experimental and data handoff

The remaining requirements are biological inputs and externally verifiable mappings. This packet makes them concrete; it does not claim experiments were performed or messages sent.

## Prioritized decisions

1. Validate the A12 epithelial signal in an independent cohort with the same source/recipient states, gene-disjoint response and TNF comparator. Retain assigned-source and identity assumptions. The current A13 programme lacks a predictive reason for expansion.
2. Resolve GSE303646/GSE202325 state and mouse mapping before another A5 score. Request exact barcode, sample, animal, age, injury day, author state, QC status and full-library UMI provenance. The state mapping must distinguish transitional from activated AT2 independently of the 99-gene instrument. Sample names and new clusters alone are insufficient.
3. Acquire a replicated early-regulatory/later-fate linkage or implement the existing [post-entry withdrawal design](../2026-09-27/P5_RECOVERY_DESIGN.md). Direct chromatin observations without linkage remain descriptions.

## P5 planning is now quantitative, without inventing variance

The six-arm design crosses exposure schedule and recipient IL1R1 status, with intervention after common entry. The two primary preparation-level contrasts remain withdrawal versus continuous exposure and its interaction with recipient status. [Calculated sample-size scenarios](P5_sample_size_scenarios.json) use noncentral-t power, two-sided alpha .025 per contrast for conservative two-comparison planning, independent normally distributed preparation contrasts and no attrition.

| Mean contrast / its biological SD | Preparations for 80% power | Preparations for 90% power |
|---|---:|---:|
| 0.3 | 109 | 141 |
| 0.5 | 41 | 53 |
| 0.8 | 18 | 23 |
| 1.0 | 13 | 16 |

These are **scenarios, not a selected sample size**. Use the SD of each actual paired/factorial contrast, not the spread between technical wells. Each independent preparation supplies six arms; technical repeats do not increase biological n. A biological minimum worthwhile effect, contrast variance, attrition and feasible independence structure must be chosen/measured before a launchable protocol can be completed. Existing three-mouse eligibility floors are not a substitute.

## Required collection fields and controls

[Collection template](experimental_unit_template.csv) separates source animal/donor, independent preparation, parent material, technical well and plate position. Record actual time of perturbation onset/withdrawal, medium/matrix lot, dose, measured residual exposure, lineage-label denominator, living descendants, mature AGER/CAV1/morphology counts and blinded scoring. Marker loss alone is not recovery; mature yield is per initial labelled input, with survival and fraction reported separately. Record an independent functional endpoint if claiming repair function.

Before outcome inference, establish intervention specificity and timing in fibroblasts, dynamic range, viable starting populations, and verified ligand withdrawal. Constitutive receptor loss cannot replace post-entry loss. Separate selective source supply, latent-ligand activation and receptor engagement for A2/A15; source/recipient production, EGF medium, latent matrix pool and rescue floors are required controls. Measure active and total TGF-beta with calibrated readouts and an active-ligand bypass where interpretable.

A3 needs sham and injury cohorts at the same age/harvest schedules; A4 needs a validated activity-history recorder/pulse-chase; A7 needs independent genotype units; A8 needs mature lineage/function endpoints; A9 requires receptor protein/engagement. A12-S1 requires independent annotation and ambient/doublet adjudication for unassigned cells, with processing/secretion measured separately. Reanalysing the same reference-conditioned RNA labels cannot supply those missing measurements.

## Stop/reopen rules

Keep the computational queue closed for the currently inspected contracts. Reopen only when a named missing input arrives, an externally validated population map is available, or a separately justified estimand is declared. A new exploratory score is not a substitute for a failed design gate. The [remaining-work ledger](remaining_work.json) records every question, its current result and the exact reopening condition; no scientific gap is marked solved by drafting this packet.
