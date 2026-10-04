# R1 source-score analysis specification

**4 October 2026; exposed descriptive analysis, Wg-R01, supporting Wg-P02.**
This specification follows the executed R0 result. Author plots, paper outcomes
and source algorithms were already viewed. A freeze does not make this confirmatory.

**Question and decision:** can the pinned author output reconstruct the tutorial
reaction contrasts and the documented metareaction procedure, and which pathway
summaries conceal opposite source-condition associations? The result determines
the defensible reproduction label and whether a reaction-resolved readout is
needed. The strongest rival is incorrect mapping/orientation, duplicated members,
grouping or near-constant profiles rather than informative heterogeneity.

**Population/unit:** exactly 139 Th17p and 151 Th17n source cells. Independent
animals/preparations are unknown; cells are nested observations. No new population
inference, flux measurement, pathogenicity test or independent replication is claimed.

## Frozen numerical choices

1. Reuse the pinned author penalties, metadata, reaction annotations and R0 joins.
   Stop on identity changes, duplicates, nonfinite/negative penalties or unmapped
   reactions. No cells are removed. No new gene signature is selected.
2. Tutorial route: negative log1p penalties, retain rows with range at least 0.001,
   then a global minimum shift. Cohen's d uses pooled sample variance and the
   sign Th17p minus Th17n. Two-sided Mann–Whitney U uses asymptotic tie correction
   and continuity correction; BH includes every retained reaction before core
   filtering. These cell-level p/q values reconstruct a source convention.
3. Metareaction route: average ranks of raw penalties, Spearman distance 1-rho,
   complete-link clustering at distance 0.02. Exactly constant profiles have
   undefined correlation: exclude them from clustering and retain their IDs in
   the exclusion table. This explicit guard is absent from the tutorial helper;
   do not conceal it as exact historical execution. Numerical distance excursions
   of at most 1e-12 are clipped to [0,2]; larger excursions stop the run.
4. Average raw penalties within each group, then apply the same transform/range
   filter. Test all retained groups once and apply BH across them; copy group
   statistics to members only for annotation/display. No new tests arise from
   expanding a group. Zero pooled variance gives an undefined standardized effect,
   retained as missing rather than an invented finite value.
5. Retain core annotations at confidence 0 or 4 with a nonmissing EC number.
   Confidence 0 is unevaluated. Preserve full reaction direction/compartment IDs.
   Apply the tutorial's mitochondrial TCA rule; no post-result manual curation.
6. Pathway displays follow the source exclusions (Miscellaneous, Unassigned,
   Other, Transport and Exchange) and more than five core reaction members.
   For aggregation sensitivity, count unique groups per pathway; report their
   median d, member-weighted median, range and positive/negative groups at the
   source q < 0.1. The median is a descriptive summary, not measured pathway activity.
   A group may belong to multiple pathways; pathway counts are not independent.
7. Fourteen named reactions are fixed from the source helper before the run:
   PGM_neg, LDH_L_neg, TPI_neg, PDHm_pos, ACONTm_pos, ICDHyrm_pos, SUCD1m_pos,
   C160CPT1_pos, CSNATr_neg, ARGN_pos, ARGDCm_pos, AGMTm_pos, SPMDOX_pos,
   r0281_neg. Keep missing or discordant results visible.

## Verification and figures

Independent scalar arithmetic recomputes every tested d and U, normal-tail
probability with ties/continuity, and BH using a separate algorithm. Tolerances
are absolute 1e-11/relative 1e-9 for d/U/p, absolute 1e-10 for BH, and 1e-12
for group expansion. Check within-group maximum distance <= 0.020000000001,
identities, pathway deduplication and the source's reported 1,911 total/784 core
groups. Those published counts are comparison targets, not tuning targets.
Disagreement produces a discrepancy record, not a threshold change.

Figures receive a separate frozen rendering contract after the tables exist.
Planned article-style plates: central metabolic contrasts; pathway heterogeneity;
selected reaction distributions; grouping/source-batch diagnostics. Use actual
cell counts, source q labels, complete axes and captions; show all prespecified
pathways/selected reactions, including weak or contrary effects. No cell-bootstrap
confidence interval or significance star may imply animal-level precision.
Provide vector PDF/SVG and high-resolution PNG; inspect rendered PDFs before delivery.

The source supplies plotted outcomes but no recovered exact numerical manuscript
reference table. Numeric reproducibility of the declared algorithm and qualitative
manuscript concordance therefore remain separate. Full Compass, bulk RNA, ATAC,
functional assays and the conditional lung extensions retain their distinct gates.

Primary algorithm evidence: pinned `Demo.ipynb`/`compass_analysis.py`, and Wagner
STAR Methods “Grouping reactions”/differential activity (supplied PDF).
[Literature boundaries](PRECEDENT_REVIEW.md) and [current source result](RESULTS.md)
remain authoritative. No governance, validator, claim grade or human acceptance changes.
