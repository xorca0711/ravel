# E1a: observed receptor-transcript context in the retained Choi benchmark

**Publication update, 1 November 2026:** this reviewed extension and its current
v2 figure are included in [PR #155](https://github.com/xorca0711/ravel/pull/155)
at the owner's request. The original numerical run and superseded v1 figure
remain preserved. PR inclusion is separate from merge and scientific acceptance.

31 October 2026 (Asia/Seoul). Owner **Sx22-P01**. The owner requested further
extension analysis after the completed X1–X3 source audits. This prospective
scope follows [their reviewed results](../extensions_20261031/RESULTS.md).
It is a descriptive measurement extension, not a reproduction of a cytokine
intervention, an animal-level effect study or a new accepted canonical RQ.

## Current disposition

**C0–C3 completed locally, 31 October 2026.** [Results](RESULTS.md) ·
[Figure/table gallery](FIGURES.md) · [Source qualification](C0_QUALIFICATION.md) ·
[Validation and handoff](VALIDATION.md).
[Originating review](REVIEW.md) passed; the completed handoff is integrated locally.

| Step | Completed work and retained limit |
|---|---|
| C0 | Exact H5AD/source hashes, two unique symbols, all 11,683 ordered metadata joins and source composition qualified; original pooled-unit/label limits remain |
| C1 | New contract/code committed before one descriptive numerical run; all 78 fixed stratum/gene rows retained |
| C2 | All cell counts, denominators, count sums and sparsity bins independently checked; 18 empty rows remain unavailable. Il22ra1 has only two observed single counts; no biological absence or response conclusion |
| C3 | Tables and current static v2 figure complete. A separately frozen rendering amendment distinguishes small positives from exact zeros; original numerical output and v1 figure are preserved |

The original scope below remains the prospective record. Both transcripts retain
their fixed order. No new targets or cohorts were added after seeing sparse
capture. Original E1/R2/R3 and persistence/function holds remain unchanged.
Human scientific acceptance remains unassessed; local review is not publication.

## Question, purpose and interpretation

What Il22ra1 and Il10rb transcript measurements are observed within the retained
libraries and literal pipeline labels of the existing Choi P001 benchmark?
The purpose is to establish whether this particular saved dataset supplies
interpretable transcript context for discussing recipient state, and to expose
sparse coverage and label/denominator limits rather than infer responsiveness.

The measurement unit is the retained cell; reporting strata are the saved
library and pipeline label. Each library pools two mice, with one library per
condition. Animal-level variation and treatment/time effects are not estimable
from these strata. The output describes the observed cells only, with no cell
bootstrap, animal confidence intervals, significance tests or condition effects.

The endpoint is transcript detection and count-derived descriptive abundance.
Neither endpoint measures receptor protein, signaling, cytokine response,
intrinsic memory, lineage fate or repair. The consequential threats are sparse
capture, ambient signal, library/time confounding, cell selection and annotation
error. Non-detection cannot establish biological absence or inability to respond.
No molecular design, variant comparison, target ranking or intervention selection
is included. The original R2/R3 execution hold is unchanged, with no claim that
the service identified or cleared its triggering item.

## Why this is a narrower eligible question

The historical E1 question sought a state/response comparison with biological
units and relevant functional evidence. Its animal-level and response claims
remain held. The new user request permits a separately governed descriptive
question about measurements already present in a noninfectious injury dataset.
This does not retry the blocked engineered-cytokine analysis or convert pooled
libraries into replicates. Persistence and later-function analyses remain held:
the inspected sources still lack the necessary linked measurements.

The [Choi scientific review](../../gate1_02_choi_2020/weft_pilot_v1/SCIENTIFIC_REVIEW.md)
is the current authority. Its 11,683 retained cells include 1,284 labels designated
as contaminants by the pipeline; the non-contaminant denominator is 10,399.
The five published states were not recovered: pAT2 is absent, hAT2 is a pipeline
label, and the day-28 exclusion/label issue is substantial. Do not relabel,
recluster, repeat the historical pipeline or promote these labels to true states.
The owner retained this benchmark only at its recorded descriptive scope.

## Steps and prospective boundaries

| Step | Work | Completion rule |
|---|---|---|
| C0 | Qualify the exact published H5AD and saved label/library fields against the original receipt and source review; inspect schema and gene identity only | Verify exact bytes, unambiguous gene mapping, count layer, sample join and label provenance. Record any exposure before freeze. Missing or ambiguous required fields stop the affected endpoint; no invented alias/state recovery. |
| C1 | Freeze and run one descriptive contract for the two prespecified transcripts | Bind inputs/code/tests before execution. For each saved library and literal label report denominator, cells with positive count, detection fraction, count sum and summed-count/library-size abundance on a stated scale. Keep both genes in fixed order, without selecting targets by result. No condition contrasts, DE, pathway/program scores, joint-response score or population inference. |
| C2 | Check denominator and coverage interpretation using the same run | Retain all labels including contaminants/unassigned; also show the already-defined non-contaminant aggregate as a separate denominator. Missing state rows are explicitly empty rather than invented zeros. Do not drop small groups or add genes after seeing results. Cross-check aggregate arithmetic against the cell-level counts and saved composition. |
| C3 | Produce a compact descriptive figure/table gallery and review handoff | A dot/table panel may show detection and count-derived abundance with denominators and literal labels. No arrow implying trajectory, protection or responsiveness. Bind plotting code in the same contract or a separate render contract. Update this ledger, the article README and PROGRESS; return a clean local commit and required validation. |

Use `analysis/research/runs/p001_figure1_v1_f001_d56ee41e13cd4327/figure1_descriptive.h5ad`,
SHA-256 `6d2ab27a98543d3f03c941907729af69ca9ce22295e51cff67e329ce8c1644ca`.
It is present in the review checkout; the locked public-output restoration route
is documented in the [source publication](../../gate1_02_choi_2020/weft_pilot_v1/PUBLICATION.md).
Use exclusive hash-verified copies or matching existing files. Preserve the
original H5AD, receipt, scripts, labels and other frozen outputs. Do not rerun
preprocessing, clustering or legacy analysis. No new cohort acquisition is needed.

The original source and selected counts/labels have been exposed in prior reviews.
The new transcripts' values must be logged as exposed if inspected during C0;
this remains exploratory/descriptive regardless of when a contract is frozen.
Write exact normalization and missingness handling in the prospective contract;
an all-cell sum-normalized transcript abundance is a descriptive library statistic,
not a repaired animal-level design. No numerical effect margin is invented.

## Literature context and source lineage

The established premise is recipient-context dependence in
[Saxton et al. 2021](https://doi.org/10.1016/j.immuni.2021.03.008), main Figures 3–7,
read from the supplied final PDF. The repository's added evidence so far is QC
and source qualification, not a reproduced treatment effect. The
[2025 companion review](../extensions_20261031/X3_SOURCE_LINKAGE.md) distinguishes
a withdrawal transcript from later function. These published premises do not
establish lung receptor activity or novelty for this descriptive extension.

[Choi et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7487779/), Figure 1A–D
and scRNA-seq methods, supplies the source population and injury/time labels.
The repository benchmark is a method adaptation with the explicit discrepancies
above. Reusing its cells is shared-source reanalysis, not independent replication.
The conceptual gap is the distinction between a tissue-level receptor argument
and measurements within retained, imperfectly annotated cell populations.
Either sparse or distributed detection is informative about this measurement
source; neither decides which cells respond to IL-22 or whether response helps.

Search refresh on 31 October 2026 used web search for
`Choi 2020 GSE145031 IL22RA1 Il22ra1 lung alveolar injury receptor expression` and
`IL22RA1 alveolar epithelial injury single cell RNA sequencing receptor expression 2024 2025 2026`.
Choi's published PMC text was opened and its Fig. 1/source design rechecked.
The search identified the older lung epithelial-repair literature and the primary
paper *IL-22 Binding Protein Controls IL-22–Driven Bleomycin-Induced Lung Injury*
(PMC10913761); direct opening of the latter returned a browser challenge.
These hits are unqualified leads, not adopted mechanistic support or a reason
to add perturbation analyses. The already-read 2025 companion supplies the
contrary-context premise. No exhaustive citation tracing, new canonical
hypothesis or novelty clearance is claimed. This is a measurement/context
description with known source limits.

## Status and delivery

C0–C3 are prospective at plan creation. Technical execution must stop on a new
content restriction rather than retrying it through other sessions. Source/field
limitations, runtime failures and any service restriction must be recorded
separately. No publication, author contact, Notion write, bench work, governance
change or human scientific acceptance is part of the technical handoff.
The originating chat independently reviews outputs and figures before local
integration. Original X1–X3 and historical E1/R2/R3 dispositions remain intact.
