# Nb3 follow-up: findings before RQ derivation

**Completed 1 October 2026.** The focal marker patterns withstand the tested
local sensitivity checks, but broader pathway significance is strongly
dependent on the assumed intergene correlation. This supports two provisional
biological questions, not a validated signalling mechanism or repair trajectory.
Read the [RQ derivation](RQ_DERIVATION.md) and [figure gallery](../FIGURES.md).

The owner authorized this batch after its proposal. The
[plan](PRE_RQ_ANALYSIS_PLAN.md), [frozen contract](../config/Nb3_followup_v1.json),
[execution receipt](../runs/followup_v1/run_record.json) and
[scripts](../scripts/14_followup_analysis.py) separate new analyses from v1.
All choices followed exposure to v1: none is a retrospective preregistration.

## What ran

| Stage | Completed work | Boundary |
|---|---|---|
| B1 | 2,292 panel specifications: 2,250 estimable, 16 one-gene omission cases untestable, 26 target-well omissions below original eligibility gates; 832 individual-marker contrasts | Same 16 targets and 13 panels; no well/control/gene was selected for favourable effects |
| B2 | 804 paired baseline/depth model attempts for AT2 and chemokine panels; 195 targets jointly estimable in both specifications | Same 771 paired wells; RNA depths are sensitivity covariates, not a causal correction |
| B3 | 1,600 species × target × Hallmark combinations assessed; 1,486 eligible, each at two fixed correlation assumptions (2,972 results) | Rank-based cameraPR of saved moderated t values; no new whole-transcriptome DE fits |
| B4 | All 16 focal targeted stable-ID rows recovered from mouse DE; literature and prior design holds reviewed | Target-transcript change is not protein editing efficiency |
| Recovery | 416 numerical comparisons pass: 13 score matrices, 208 focal contrasts and 195 paired human contrasts | Input hashes were verified before and after execution |

## NKX21: a reproducible local RNA pattern, with a modest general association

The original effect is −2.072 for the mouse AT2 panel, −3.357 for human
chemokines and +1.468 for human wound markers, in mean log2(TMM CPM + 0.5)
contrast units. Reference substitution and every eligible marker/well omission
retain these three directions.

| NKX21 endpoint | TIGIT-only / tdTomato-only | Omit one marker: range | Omit one target well: range |
|---|---:|---:|---:|
| Mouse AT2 | −2.047 / −2.141 | −2.415 to −1.399 | −2.114 to −2.002 |
| Human chemokines | −3.305 / −3.480 | −3.706 to −2.872 | −3.750 to −3.026 |
| Human wound markers | +1.417 / +1.588 | +1.389 to +1.578 | +1.422 to +1.517 |

These ranges are sensitivity ranges, **not confidence intervals**. Four NKX21
target wells share the source preparation structure. All seven individual
chemokines have negative technical contrasts; CCL2 is −1.769 (technical 95%
interval −2.355 to −1.183). This is a plausible starting point for a secretion/
recipient-function question, not a measurement of immune-cell recruitment.

On the paired population, NKX21 AT2 changes from −2.094 to −1.837 after both
log read depths enter the model; chemokines change from −3.357 to −3.238.
Across all 195 common targets, AT2–chemokine rho changes **0.210 to 0.151**;
without NKX21, **0.198 to 0.138**. The older v1 rho 0.182 used species-specific
QC populations, so it is a different estimand from the paired baseline.
RNA depth may reflect real abundance or state changes. Persistence under this
adjustment does not establish a direct identity effect; attenuation does not
prove a technical artefact.

Data: [panel summary](../runs/followup_v1/panel_sensitivity_summary.tsv),
[individual markers](../runs/followup_v1/individual_marker_effects.tsv),
[paired-depth effects](../runs/followup_v1/paired_depth_effects.tsv) and
[paired associations](../runs/followup_v1/paired_depth_associations.tsv).

## SLC34A2: transition-marker induction with a smaller identity change

The transition-panel effect is +0.524: +0.490 with TIGIT-only references,
+0.624 with tdTomato-only references, +0.437 to +0.568 under marker omission,
and +0.488 to +0.567 under target-well omission. All three markers contribute:
Krt8 +0.436, Sprr1a +0.438 and Clu +0.698. There are eight target wells and 32
mouse references on plate 4, not eight demonstrated independent preparations.

AT2 is −0.110 and AT1 +0.062 in the original analysis, both with intervals
crossing zero. One AT1 marker omission reverses its near-zero sign. The paired
AT2 contrast becomes −0.219 after depth adjustment (technical interval −0.375
to −0.062). Therefore **“no identity loss” is too strong**; the evidence is a
transition-associated pattern with much smaller identity attenuation than
NKX21, within the limitations of bulk averages. It does not identify the
sequence of states, irreversibility or recovery.

The exact targeted Slc34a2 row decreases (logFC −0.870, gene-DE q = 1.20e−8),
which is transcript-level consistency only. Slc34a2 is excluded from the
transition/AT2 panels, so the state observation is not the target transcript
being used as its own outcome.

## ELOVL1/ATP6V0E: retain the phenotype, withhold the Wnt mechanism

Both AT1 marker contrasts stay negative across control substitutions and all
gene/well omissions. ELOVL1 marker-omission effects range −0.919 to −0.570;
ATP6V0E ranges −1.120 to −0.908. The small positive Wnt-panel estimates keep
their signs across these diagnostics, but their primary technical intervals
still include zero. A narrow positive marker mean is not a pathway result.

Whole-set mouse Wnt/beta-catenin enrichment is unconvincing: global q is 0.395
for ELOVL1 and 0.927 for ATP6V0E under the primary correlation assumption.
The CTNNB1 activating-edit comparator also fails this Hallmark readout
(q = 0.762), despite its strong source-marker Wnt contrast. This limits the
readout's calibration: it cannot establish either Wnt activation or Wnt
independence in the candidate perturbations. Elovl1 RNA does not decrease
(logFC +0.155, q approximately 1); Atp6v0e does (−2.044, q = 1.25e−6).
Neither observation alone measures editing or protein function.

## Broader pathway context is assumption-sensitive

Species-appropriate MSigDB Hallmark 2024.1 sets were assessed against all
expressed, fitted genes (AveExpr > 1.5), retaining one row per symbol by highest
average expression then stable ID. Coverage required at least 15 mapped genes
and at least half of the set. Of 1,600 planned comparisons, 114 fail coverage;
these remain documented rather than receiving a null p-value.

At intergene correlation 0.01, **251/1,486** tests have global BH q < 0.05.
At 0.05, **6/1,486** do. All rank directions agree, but statistical strength
does not. The six retained entries are mouse IFN-alpha response for KEAP1
(down), CSNK2A1 (up), ATP6V0E (down), FZD5 (down), ERBB3 (down), and IFN-gamma
response for CSNK2A1 (up). This is agreement across two declared assumptions,
not proof that either equals the true residual correlation.

NKX21 human TNF/NF-kB, interferon-gamma and inflammatory sets rank downward
under the primary model, but none retains global q < 0.05 at correlation 0.05.
SLC34A2 mouse interferon and TNF/NF-kB context is likewise sensitive.
These **do not identify the causal pathway** underlying the marker phenotype.
With independent units unresolved, even the six retained entries remain
exploratory competitive RNA results. The cameraPR implementation uses a fixed
correlation; it does not estimate set-specific correlation from expression.

Data: [all tests](../runs/followup_v1/hallmark_camera.tsv),
[coverage](../runs/followup_v1/hallmark_coverage.tsv),
[gene universes](../runs/followup_v1/hallmark_universes.tsv).
Method references: [Wu and Smyth](https://doi.org/10.1093/nar/gks461),
[Liberzon et al.](https://doi.org/10.1016/j.cels.2015.12.004).

## Source and functional limits remain

Human S5 still has 8,987 internal sign conflicts and near-zero numeric
concordance. The new results reuse Nb3's verified count-derived fits; they do
not repair that source table. The source reports NKX2-1 protein loss despite
increased Nkx2-1 RNA; our +1.194 transcript contrast must not be used to negate
the reported protein result. Other target-specific editing cannot be certified
from transcript reduction, and EGFR/ERBB4 have low fitted average expression.
See the [target checks](../runs/followup_v1/target_transcript_checks.tsv).

The [conditional-work register](PRE_RQ_ANALYSIS_PLAN.md#branch-specific-work-that-remains-conditional)
still governs exact embeddings, spatial design, independent validation,
DepMap and lung-specific fibroblast identity. No new animal/donor experiment,
secretion assay, fate measurement, clinical outcome or claim-grade promotion
has occurred. The two derived questions are proposed in the existing register
format with explicit rivals and discriminating outcomes.
