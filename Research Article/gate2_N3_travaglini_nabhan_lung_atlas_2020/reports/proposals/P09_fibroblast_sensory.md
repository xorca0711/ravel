# Nb4-P09: SCN7A/GRIA1-associated fibroblast phenotype

**7 October execution:** the [first expression-specificity/transport stage](../../../../docs/portfolio_extensions/2026-10-07/g2_niche/RESULTS.md) is complete. Its separate genes and assay-sensitive joint detection motivate proposed [A31](../../../../RQ_Specified/A31_gria1_fibroblast_response/README.md); functional sensory response remains unmeasured. This article-local proposal retains the source evidence and its remaining stages.

**Status: planned; functional interpretation requires additional evidence.**
[Master contract](README.md) · [source ledger](SOURCES.md).
S01 source discovery; the existing S03 fibroblast subset can support a
newly frozen expression check. Spatial and functional inputs remain unqualified.

## Question and alternatives

Do SCN7A and GRIA1 mark a reproducible fibroblast phenotype that motivates
a sensory-response question, or do sparse transcripts reflect ambient RNA,
mixed identities or incidental expression? Verify the exact **GRIA1** gene;
the abbreviated “GRIA” note is not an analyzable gene identifier.

The first hypothesis is expression specificity and reproducibility. A
sensory-response mechanism is a later question. Neither a channel/receptor
name nor RNA coexpression demonstrates membrane localization, excitability,
sodium sensing or a response to neurotransmission.

## Measurement and units

Primary quantities are donor-level detection fractions and expression
contrasts in independently labelled alveolar/adventitial and other eligible
fibroblasts, with assay-specific treatment of UMI and read counts. Examine
SCN7A and GRIA1 separately before any joint phenotype; report joint detection
and depth dependence rather than hiding discordance in a summed score.

Labels must exclude both genes. Include available neural/glial, mural and
other mesenchymal comparators to assess specificity; if those populations
are absent from the cached subset, return to the full source release.
Distinguish within-cell coexpression from a mixture of expressing populations.

## Ordered analysis

1. Confirm stable gene IDs, coverage and count-layer semantics. Audit source
   and external donor/assay distributions without selecting only positive
   donors. Record cell/nucleus preparation separately.
2. Estimate fibroblast subtype contrasts and detection patterns at the donor
   level. Compare with full-compartment expression where available.
   Respect existing depth floors and freeze any new floor before effect fitting.
3. Assess ambient and doublet explanations using available raw droplets,
   source QC and mixed-lineage features. If raw background is unavailable,
   report that ambient correction is unvalidated; absence of a flagged
   doublet is not proof of pure identity.
4. Freeze the source definition and test it in the S03 fibroblast cohort.
   Show single-cell and nuclear assays separately. Gene omission cannot
   validate a two-gene biological program; demonstrate each component directly.
5. Seek independently annotated cell-resolved spatial coexpression or protein
   localization before advancing to a functional phenotype. Spots mixing
   nerves and fibroblasts do not establish fibroblast receptor expression.

## Decision, figures and next step

Retain an expression-phenotype candidate if it is donor/study reproducible
and specificity/contamination rivals are reasonably resolved. Narrow to one
gene or one fibroblast subtype when joint evidence fails. Hold the mechanistic
branch without localization and an independent response measurement.

A future response study would need a defined biological stimulus, a direct
cellular response and a receptor/channel-specific causal comparison; this
plan does not infer those results or prescribe an experimental protocol.
If the outcome instead concerns fibroblast support or epithelial chemokine
coupling, map it to A20/A13/A22.

Planned panels: full-compartment specificity dot plot; donor detection and
expression; joint-expression/depth diagnostics; independent-cohort contrasts;
cell-resolved localization if obtained. Caption focus: **“Candidate sensory
components are tested for reproducible and cell-specific fibroblast expression.”**

First deliverable: a gene-ID and full-compartment specificity table. Give this
branch lower execution priority than P01/P03/P04 because its mechanistic
interpretation needs measurements that the current transcriptomic cache
does not provide. Interesting biology and immediate feasibility remain
separate judgments.
