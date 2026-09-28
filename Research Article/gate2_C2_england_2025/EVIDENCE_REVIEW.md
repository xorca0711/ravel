# England 2025: claims and current evidence

[Study overview](README.md) · [Complete figure gallery](FIGURES.md) ·
[Source/claim audit](../../docs/audits/2026-09-28-england-paper-rqs/REPORT.md)

**Current interpretation, 28 September 2026.** This page separates published
source findings from this repository's reanalysis and unresolved mechanisms.
It summarizes the source audit, A16 integration, corrected C1 and A17 source accounting; it does
not create a second graded claim register or regrade C1–C168.

<a id="state-and-maturation"></a>
## 1. Mixed epithelial identity and AT1 maturation

**Published evidence:** Figures 3–4 and S4–S5 support mixed mutant identities
and plasticity of sorted populations under the tested functional conditions.

**Our analysis:** EN1/EN2 and FU_B show that RNA occupancy depends on the gate.
The permissive AT1 marker rule includes many cells assigned to AT2 clusters.
FU_B calibrates an alternative AT1 score using the same reference cells on
which its sensitivity/specificity are reported.

**Conclusion and limit:** state assignment is sensitive to the classifier.
Its in-sample performance is not independent validation. Changing a custom RNA
gate does not refute protein-supported mixed states. Small cycling-score
differences do not demonstrate equivalent proliferative potential, and graph
connectivity or one-dimensional projection does not trace reversible fate.
[Relevant figures](FIGURES.md#state-and-maturation); [RNA topology panel](FIGURES.md#fu-f03).

<a id="cd177-attribution"></a>
## 2. CD177-associated priming

**Published evidence:** the source identifies a CD177-associated mixed state.
It does not establish CD177-specific necessity. Its WT inflammatory organoids
also express CD177, limiting claims of universal mutant exclusivity.

**Our analysis:** the original two library-specific transitional contrasts
show higher priming-associated RNA. FU_A's frozen depth-control result is
inconclusive. FU_C pools libraries and drops the original transition gate;
it is not the same population comparison conditioned on neighbourhood.
The source audit's fixed-population diagnostic retains two eligible strata
with different priming effects. A16 Stage 1 adds exploratory sensitivities,
but specificity remains inconclusive and the available panel cannot exclude
ambient RNA. Its four primary-library thinning comparisons fail the cell floor.
The later [corrected C1](../../RQ_Specified/A16_cd177_state_attribution/correction_20260928/reports/CORRECTED_C1_REPORT.md)
uses fixed per-library populations and excludes grouping/gate/outcome genes
before local matching. Primary priming raw differences attenuate from 1.2558
to 0.4098 and 1.3318 to 0.3151; appreciable PC imbalance remains. These are
exposed-data sensitivities, not independent biological confirmation.

**Conclusion and limit:** CD177-associated RNA is a lead, not established
cell-intrinsic function or a resolved composition/depth effect. Read the
[A16 current review](../../RQ_Specified/A16_cd177_state_attribution/reports/INTEGRATION_REVIEW.md)
before its historical report. [Relevant figures](FIGURES.md#cd177-attribution).

<a id="il1r1-and-nf-kb"></a>
## 3. Il1r1-dependent entry and NF-kB feedback

**Published evidence:** Figure 7 and S7 distinguish Il1r1-dependent entry into
mutant states from later changes after NF-kB inhibition in organoids/PCLS.

**Our analysis:** EN2 recovers genotype-associated RNA differences and lower
transition-state occupancy in the Il1r1 deletion context. It does not reproduce
the post-entry inhibition experiment. Nfkbia is an inducible inhibitor;
its RNA level alone measures neither pathway activity nor feedback competence.

**Conclusion and limit:** source functional results and repository RNA
associations are complementary, different observations. No AT1-score increase
in EN2 is not evidence against the source's later inhibition result, and marker
changes are not demonstrated durable alveolar repair. [Relevant figures](FIGURES.md#il1r1-and-nf-kb).

<a id="clone-growth"></a>
## 4. Clone growth and founder classes

**Published evidence:** Figures 1–2, lineage observations and Methods S1
support heterogeneous clone growth and a two-population model. The Discussion
also retains a single-hierarchy alternative.

**Our analysis:** mouse-indexed distributions support held-out comparisons
of statistical model families. EN6 confirms that the deposited slow-loss
branch cannot fire in the audited q=0.7 setting, changing simulated size
distributions. The corrected full stochastic refit has not run.

**Conclusion and limit:** an implementation defect affects reproducibility;
it does not by itself refute observed heterogeneity, the analytical source
fit or lineage evidence. [A17 raw-source accounting](../../docs/roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md)
now reproduces all 58 saved count rows and traces the code's fast/slow arguments
and 14-day switch. The primary input has 11 source-indexed mice. Printed-table
and manuscript/curve-provenance discrepancies remain; grid-wide switching,
common model scoring and a tail diagnostic still need a refit amendment.
Source-indexed mouse units exist in the nonspatial arrays, unlike the spatial pair exports. [Relevant figures](FIGURES.md#clone-growth).

<a id="wild-type-neighbours"></a>
## 5. WT expansion and loss of AT2 identity

**Published evidence:** Figures 5–6 show altered WT growth and identity in
oncogenic tissue. S6Q–V gives functional organoid motivation for SPP1/DLK1.

**Our analysis:** EN_F06/FU_W reproduce pooled distance profiles. The size
association and identity-loss proxy have different descriptive patterns,
but spatial rows omit mouse/clone IDs, may repeat neighbours and become sparse
at larger distances.

**Conclusion and limit:** a noisy identity-loss slope does not establish
distance independence or two causal mediators. AREG, SPP1/DLK1, relay signalling
and mechanics remain alternatives; RNA or ligand class does not assign spatial
range. Whether the WT response promotes or restrains tumour growth is open.
[Relevant figures](FIGURES.md#wild-type-neighbours).

<a id="repair-transfer"></a>
## 6. Repair-state comparison

**Published motivation:** mutant states reuse features observed during repair.

**Our analysis:** EN7 applies the frozen RNA panels to Choi and Niethamer
repair data, with the recorded time points and biological-unit coverage.
CD177-positive transitional cells are too sparse for the planned contrast.

**Conclusion and limit:** available repair-state distributions can be
described. Missing coverage leaves CD177 transfer unassessed; it does not show
that the marker cannot occur in repair or that the same cells reverse state.
[Relevant figure](FIGURES.md#repair-transfer).

## Historical claims, reports and proposed questions

| Record | What it owns |
|---|---|
| [Root claim register](../../CLAIMS.md) | Graded historical C claims; no grade is assigned by this page |
| [England claim crosswalk](../../docs/audits/2026-09-28-england-paper-rqs/REPORT.md#historical-claim-register-crosswalk) | C19, C31–C35, C105, C136–C137, C141 and C148–C150, with source-specific limits |
| [Batch 1](RESULTS_BATCH1.md), [continuation](RESULTS_CONTINUATION.md), [follow-up](RESULTS_FOLLOWUP.md) | Original executed outputs and numerical reports; stronger interpretations are bounded by the current reviews |
| [Source audit](../../docs/audits/2026-09-28-england-paper-rqs/REPORT.md), [A16 review](../../RQ_Specified/A16_cd177_state_attribution/reports/INTEGRATION_REVIEW.md) | Evidence for the current corrections |
| [A16–A18](../../RESEARCH_QUESTIONS.md#a16), [eight candidates](CANDIDATE_HYPOTHESES.md) | Proposed biological explanations, predictions and missing evidence |

Reading a table or rerunning a verifier establishes neither a new biological
mechanism nor independent replication. No outcome, threshold or claim grade
was changed by this documentation reorganization.
