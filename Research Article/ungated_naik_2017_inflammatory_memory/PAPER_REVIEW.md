# Naik 2017: claim-to-measurement review

17 November 2026. Source: [Naik et al., Nature 550, 475–480](https://doi.org/10.1038/nature24271),
online 18 October 2017, issue 26 October. The owner's annotated 21-page PDF
contains the final article, Methods, extended data/reporting material and the
[4 July 2018 correction](https://doi.org/10.1038/s41586-018-0229-5).
Its SHA-256 is `e02a6f7b2bcc4c3e1338e13bac313ef8a919c0e47e5d778ca3093fa53aabf036`.
The PDF remains private. Main text and relevant legends/Methods were inspected;
PDF pages 3–5 (Figures 2–5) were also viewed as images. This is a focused
interpretation review, not reconstruction of every source-data panel.

## Published findings and their limits

| Claim | Exact source | Measured support | Limit that matters for the plan |
|---|---|---|---|
| Prior inflammation changes later repair | Fig. 1b–g; Extended Data Fig. 2 | Wound-area dynamics, re-epithelialization, splinted wounds and explant outgrowth | Wound closure, migration and proliferation are distinct; do not infer a general increase in every repair function. |
| Long-lived epithelial populations carry prior exposure | Extended Data Fig. 1b–e | Krt14/Krt10 lineage-label persistence | Population tracing does not show that every surviving cell retains the same regulatory change or exclude clonal selection. |
| The repair advantage is local and survives tested immune-cell interventions | Fig. 2a–h; Extended Data Fig. 3 | Local/distal comparison, macrophage/RORC-positive-cell depletion and Rag2-null comparison | These tests support an epithelial contribution; they do not exclude every niche contribution or establish that immune signals never help establish memory. |
| Some accessibility persists after recovery | Fig. 3a–e; Extended Data Fig. 4 | Bulk ATAC in sorted EpSC preparations at D6/D30/D180 | Accessible-region persistence is not continuous transcription, direct TF binding, or same-cell longitudinal tracking. |
| Retained regions and recall RNA are associated | Fig. 4a–e; Extended Data Fig. 5 | Reporter activity, RNA contrasts, and the reported overlap of 73 of 140 upregulated wound-response genes with retained-region-associated genes | Region-to-gene assignment and background matter. Reporter responsiveness does not prove endogenous necessity of each element. |
| AIM2 and downstream signaling contribute to enhanced repair | Fig. 4f–h and Fig. 5a–h | Sustained Aim2 RNA, loss/gain-of-function repair comparisons, CASP1 activity, cytokine/receptor tests | A repair phenotype does not establish which factor stores or maintains the chromatin change. Aim2 is a sustained-expression exception to the predominantly latent pattern. |

These are published findings. None is a new Ravel observation. The general
chromatin mechanism, its endogenous elements and organism-level disease risks
are not all established by any one panel.

## Corrections and qualifications for reading notes

- **D30, not “d330”**: the recovery-stage accessibility comparison is D30;
  some regions were additionally examined at D180 (Fig. 3).
- **Il18-null, not Il17-null**: Figure 5d/e compares Il18 and Il1r1 loss.
  IL-18 was dispensable for the reported repair advantage; IL-1R1 was required.
- **Loss of enhanced repair is not proof of erased chromatin memory.** Keep
  establishment, maintenance and execution as separate questions when interpreting
  AIM2/CASP1/IL-1 signaling perturbations.
- **“Immune independent” needs a defined scope.** The tested macrophage/T-cell
  routes were dispensable for the relative recall advantage under these designs;
  no universal exclusion of immune or stromal contributions follows.
- **Baseline recovery is not equivalence.** Few significant D30 RNA differences
  do not establish that all RNA returned to an identical state. Retain effect
  sizes, uncertainty and the limited number of pooled preparations.
- **A later high value is not a response rate.** Separate baseline differences,
  change after challenge and kinetics. The deposited 6-hour libraries may add
  temporal description, but cannot by themselves identify a precise onset/rate.
- **Figure 2g was corrected.** The original D30 IMQ image duplicated D6 Ctrl.
  The appended correction explicitly replaces it; use corrected publisher
  material for any future panel reproduction, rather than assume an older PDF
  image has been updated merely because the correction is appended.

## Source-version and unit audit

The final PDF Figure 3 legend (p. 4) reports three pooled mice per group in
duplicate for ATAC. Figure 4c's legend (p. 4) and RNA Methods (p. 8) report four
pooled animals per condition in duplicate. The
[PMC author manuscript, RNA-seq Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC5808576/)
says 3–4 pooled animals per condition. Prefer the final publication when quoting
its design, retain the version discrepancy, and qualify each library's actual
pool/experiment mapping. Neither four pooled animals nor two sequencing runs
automatically supply four or two independent biological observations.

Both Methods and GEO describe 50-base RNA reads, with the paper specifying
single-end sequencing. A preliminary SRA/ENA inspection identified paired reads
for SRR5133553; independently qualify that mapping in S1 and preserve the
unresolved mismatch. It affects exact raw-read replay; it does not automatically
invalidate the author-provided gene-count route. The paper's processing reference
is STAR/mm10/GENCODE M9.

Bulk ATAC and RNA use separately sorted preparations. Identical R1/R2 labels
across assays do not establish pairing. Whole-skin unwounded sorting and
wound-edge sorting may also differ in captured populations. This is an explicit
validity threat to a simple history-by-wounding interpretation.
