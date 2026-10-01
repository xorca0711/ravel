# Nb3: additional analyses before question derivation

Declared 1 October 2026 after viewing v1 results. The owner requested execution
of the additional analyses followed by hypothesis-based RQ derivation. This is
a source-informed follow-up, not a preregistration on unseen data. The frozen
[follow-up contract](../config/Nb3_followup_v1.json) records inputs and choices
before the new computations. Existing A10/A2 fits and Nb3 v1 outputs are retained.

## Minimum additional batch to run now

| Stage | Why this can change a question | Analysis and deliverable | Interpretation rule |
|---|---|---|---|
| B1: panel dependence | A small marker list can be driven by one gene, reference type or well | For the same 16 focal targets and 13 non-receptor panels: recover v1 scores/effects; compare TIGIT-only and tdTomato-only references, omit each panel gene and each target well; retain every eligible result and interval | Sign/size variation is a diagnostic, not biological replication; a one-gene sentinel cannot pass gene-omission testing |
| B2: paired-depth sensitivity | Both compartments have score–depth associations; different QC populations can change contrasts | Refit the two already-nominated association endpoints (mouse AT2 and human chemokines) for all targets on the 771 paired wells, with and without both log read depths; compare target-level associations and the focal 16 contrasts | Depth may be downstream of perturbation. An adjusted coefficient is not a direct causal effect; retain paired unadjusted and original estimates separately |
| B3: broader transcriptional context | Figure marker panels do not establish pathways | Rank-based cameraPR on saved whole-transcriptome moderated t statistics for both species and the existing 16 targets, using all 50 species-appropriate MSigDB Hallmark 2024.1 sets; audit coverage and duplicate-symbol handling | Competitive RNA enrichment is exploratory. Global BH is across all eligible species × target × set tests within each correlation specification; repeat at fixed intergene correlation 0.05 after primary 0.01 |
| B4: perturbation and evidence audit | Transcript targeting, lineage switching and measured function are distinct | Extract each focal target's exact S2 stable-ID row from the saved mouse DE results; connect prior primary literature to the patterns; preserve target/plate and independent-preparation holds | Transcript change does not verify protein editing; CTNNB1 is an activating edit. References motivate hypotheses, not validation of this screen |
| B5: question derivation | Follow-ups should resolve biological alternatives rather than rename diagnostics | Compare with A0–A18; derive only distinct evidence-supported question cards, with context, directional prediction, rival explanation, discriminating outcome and readiness | Proposed post-analysis hypotheses receive no inherited claim grade; feasibility and supporting observations are reported separately |

The exact same 16 targets were selected in v1, before these diagnostics. No
target, gene or pathway is removed because its effect is inconvenient. No
automatic “robust” threshold is invented from the resulting ranges. This batch
reuses normalized counts and saved DE statistics; rerunning all 395 gene models
would add cost without addressing the identified uncertainty.

## Branch-specific work that remains conditional

| Requirement | Current evidence / stopping condition | Consequence for RQs |
|---|---|---|
| Reconcile human S5 numeric contrasts | Existing audit found 8,987 internal sign conflicts. Corrected source table, generating code or a verified mapping is needed; do not permute labels to maximize agreement | Count-derived human observations can motivate a provisional question; exact human source reproduction stays failed |
| Identify biological units and valid perturbations | Split wells, target/position/guide confounding and missing independent preparations remain unresolved; RNA is not editing efficiency | No confirmatory causal or biological-population inference from this screen |
| Exact cPCA/JADE and original component stability | Source input/scaling, cPCA settings and JADE implementation are not recovered | Necessary for an exact embedding/component reproduction claim; not necessary to formulate a question from independently defined marker contrasts |
| Independent within-state, donor/time validation | Source-reused GSE215824 is not independent; GSE122960 author annotations and biological-unit eligibility remain unresolved | Required before claiming persistence, fate, state independence or validation; candidate cohorts remain candidates |
| Spatial heterogeneity and paracrine locality | Reconcile GSE307128 treatment, animal identities and grid definition before modelling; bins are not animals | E7/locality remains untested; do not make a spatial figure from incompatible metadata |
| EGFR/HER2/HER3 recipient function and DepMap | Recover the exact source release, assay and 93-versus-96 line denominator for reproduction; normal epithelial function needs its own evidence | Expression/growth motivate receptor questions but do not establish dispensability, AT2 origin of cancer lines or drug-induced fibrosis |
| Lung-specific fibroblast programme | PLIN2 alone is insufficient; requires a prespecified multi-gene, multi-tissue comparison | E8 is currently paired with E1 as a niche-response question; no lung-specific identity claim |

These are not all prerequisites to *formulating* an RQ. They are prerequisites
to the particular stronger answer that the RQ would seek. The executable batch
above narrows hypotheses now; unavailable causal and independent-validation
evidence must be named in the resulting plans.

Method basis: [camera, Wu and Smyth 2012](https://doi.org/10.1093/nar/gks461)
and [Hallmark collection, Liberzon et al. 2015](https://doi.org/10.1016/j.cels.2015.12.004).
The original paper's enrichment settings are not being claimed recovered by
this new, explicitly versioned analysis.
