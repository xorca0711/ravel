# A16 Stage 1: integration review, 28 September 2026

**Current interpretation.** Stage 1 produced useful exploratory sensitivity
analyses, but does not establish CD177-specific, position-independent biology
or exclude ambient RNA and depth/detection effects. The full frozen comparison
remains incomplete. This review supersedes stronger prose in the original
[results](STAGE1_RESULTS.md), while retaining its tables, scripts, contract,
[pre-execution population amendment](STAGE1_ERRATUM.md) and correction to the
control-gene count unchanged.

## What is retained and what it establishes

| Analysis | Retained result | Appropriate interpretation |
|---|---|---|
| C3 matched-gene comparison | 4/9 descriptive entries exceed every sampled control; 7/9 have fewer than 40 controls | Heterogeneous, limited reference-gene evidence; no general specificity conclusion |
| C4 neutrophil-panel adjustment | Priming associations remain after the available panel adjustment | The chosen panel does not remove the association; contamination is unresolved |
| C1 UMAP matching | Positive raw matched differences in 8/9 entries at k=10 | Descriptive residuals in the available embedding, with a declared change from the frozen space |
| C2 resolution sensitivity | Three persisted resolutions give non-monotone weighted effects | No observed monotone decay on this short ladder; a non-positional component is not established |
| C5 marker thresholds | Full-depth effects in eligible rows generally keep their direction across 1/2/3-UMI cuts | Bounded cutoff sensitivity; all four thinned-depth rows in the two primary libraries fail the 30-positive-cell floor |

The nine entries combine two library-specific marginal contrasts and seven
experiment-pooled subclusters. They are neither nine independent biological
replicates nor repeated estimates of a single common population.

## Corrections needed before interpreting the original report

1. **C4 does not exclude ambient RNA.** The frozen contract itself states that
   filtered matrices and a within-cell panel cannot do so. A low panel
   correlation or a remaining adjusted effect does not test every source of
   contamination. The script's `cd177_umi_here` is a binary detection indicator;
   `spearman_cd177_umi_vs_neutro` therefore measures detection versus panel, not
   UMI abundance versus panel. Ratios of standardized effects are not fractions
   of biological signal retained because residualization changes the scale.
2. **C5 does not exclude detection/depth artefacts.** Its thinning changes the
   marker call while outcome scores remain full-depth. Both primary libraries
   fall below the floor under both saved thinning seeds. Robust directions at
   three full-depth cutoffs are narrower evidence than complete depth control.
3. **C1 is not the frozen neighbourhood test.** It uses UMAP coordinates from
   the previously fitted embedding, not an independently fitted, gene-excluded
   integrated space. Matched controls may recur; no library restriction is
   imposed in the pooled arm. Matching alone does not restore independent units
   or prove removal of composition. The C3 null uses unadjusted SMDs, whereas C1
   reports matched raw differences and paired-difference-standardized effects;
   those scales cannot be directly compared to apply a common null threshold.
4. **C2 changes more than resolution.** Eligibility, represented populations
   and weights change across resolutions. Pooled-library and gene-reuse issues
   remain. A short apparent plateau is not a specific test of intrinsic biology.
5. **C3 control abundance is not biological power.** More matched genes improve
   description of that selected reference set, but do not add independent mice.
   The median control SMD is not an additive decomposition of the CD177 effect;
   the report's claim that it accounts for most of the effect is unsupported.
   Zero sampled controls exceeding an estimate is not a zero p-value.
6. **The two-arm amendment does not repair the original population mismatch.**
   Arm A is marginal within the transition gate; Arm B keeps FU_C's all-cell,
   pooled-library population. Comparing those arms is not conditioning one
   fixed population. C1/C5 also use the round-2 labelled subset, while C3/C4
   assemble Arm A from the cell table; their eligible counts differ slightly.
   The same-population diagnostic in the
   [earlier audit](../../../docs/audits/2026-09-28-england-paper-rqs/REPORT.md)
   and this Stage 1 therefore answer different, exposed-data sensitivity questions.

## Readiness and next decision

Retain A16 as proposed and **partly measured, inconclusive**, with no claim-grade
change. The corrected same-compartment, separate-library comparison still needs
an amended specification and independent neighbourhood construction if pursued.
Repeating the existing matrices under new settings would remain exploratory.
A stable or functional CD177-associated phenotype requires independent
surface-marker/outcome evidence. No author was contacted, and the previously
recorded public-data search is not a claim of permanent data absence.

## Evidence verification and reproducibility limits

[verify_stage1_evidence.py](../scripts/verify_stage1_evidence.py) checks the
original scripts, contract, erratum and all six output hashes, then recomputes
C3 reference-set summaries from the saved per-gene table and checks the central
C1/C4/C5 summaries. [Verification record](INTEGRATION_VALIDATION.json).
The England continuation contract digest matches its LF Git blob; only its
Windows checkout line endings differ. A16's own hashed files are byte-preserved.

This is table/provenance validation, not a raw-data rerun. C3/C4 directly load
count matrices and barcode arrays that their run record does not hash; the
record therefore does not independently identify every direct input. The
original scripts also overwrite their output directory. Preserve them as run
evidence and use an isolated output location for any future replay; do not
execute them over the archived Stage 1 files.
