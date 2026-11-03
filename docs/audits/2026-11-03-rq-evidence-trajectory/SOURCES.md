# Evidence coverage and review limits

3 November 2026. Companion to the [all-question assessment](README.md).

## Repository state and method

- Fetched `origin/main`; verified merge `115f3c5` and tree
  `5ae127987a15c188ebba0122e5393405475ef767`. It matches the reviewed PR #160
  branch's tree. The initial working tree was clean.
- Created `codex/rq-evidence-trajectory-audit-20261103` from that base.
- Read the current agent entry, progress and research governance; used
  `analysis/research/registry.json`, its 33 question records and their current
  dossiers/evidence locators. The NGS results-review skill supplied endpoint,
  unit, lifecycle and interpretation checks. These are repository runs, not
  newly registered NGS Workbench executions.
- Read the biological problem, repository evidence, working hypothesis and
  maturity sections for **every A0–A32 dossier**; inspected current source
  amendments and grouped result reports before recovering earlier wording.
- Recovered the earliest headed A0–A32 entries by traversing the Git history
  of `RESEARCH_QUESTIONS.md` in chronological log order. Reviewed the original
  question headings/claims and the particularly consequential older A1–A5,
  A15–A18 and A24–A30 wording. [ORIGINS](ORIGINS.md) links immutable versions.
  This is the earliest registration located in that file, not proof of the
  earliest private idea or a full transcript reconstruction.

## Current result authorities inspected

The [report's individual entries](README.md#each-question-origin-present-evidence-and-justified-next-decision)
link the question-specific records. These cross-question authorities were also
read and supply the coverage/hold summaries for the whole portfolio:

| Authority | Coverage and role |
|---|---|
| [G1 audit](../../portfolio_extensions/2026-10-07/g1_epithelial/AUDIT.md) and [results](../../portfolio_extensions/2026-10-07/g1_epithelial/RESULTS.md) | Epithelial questions, source units, A11 capacity diagnostic and A17 denominator calculation. |
| [G2 audit](../../portfolio_extensions/2026-10-07/g2_niche/AUDIT.md) and [results](../../portfolio_extensions/2026-10-07/g2_niche/RESULTS.md) | Niche/source/receptor questions, later corrections, fixed Nb4-P09 expression comparison. |
| [G3 ledger](../../portfolio_extensions/2026-10-07/g3_immune/STATUS_LEDGER.md), [A25](../../portfolio_extensions/2026-10-07/g3_immune/A25_RESULTS.md), [A30](../../portfolio_extensions/2026-10-07/g3_immune/A30_RESULTS.md) | A24–A30, source units, state/region/sex and observed-support restrictions. |
| [Wp corrections](../../../Research%20Article/gate2_W2_wagner_Th17_PGAM/CORRECTIONS_2026-10-07.md) | Supersedes old Compass sign, human-score denominator and regulatory-equivalence interpretations. |
| [A1 comparison matrix](../../../RQ_Specified/A1_transitional_epithelial_state_distinction/COMPARISON_MATRIX.md) | Distinguishes supporting branch measurements from the missing primary regulatory/outcome comparison; also documents shared A8/A14 gaps. |
| [DY1-P02 current results/ledger](../../../Research%20Article/gate2_DY1_damani_yokota_2026/rq_discordance/README.md) | Recent baseline measurement/reference/synthetic and human-panel work. Its central discrepancy is bulk RNA versus separate bulk ATAC; scRNA adds composition evidence. These extensions do not identify the NAM regulatory mechanism. |
| [Arozamena RQ connections](../../../Research%20Article/ungated_arozamena_2026_inflammatory_memory/RQ_CONNECTIONS.md) | Four-locus region/count/QC sensitivity and paired barcodes do not supply qualified within-state labels or early-to-later function joins. The indirect Saxton connection does not upgrade an A-series result. |
| [Yd1-P02 T0](../../../RQ_Specified/Yadav_followups_20261031/T0_RESULTS.md) and [T2](../../../RQ_Specified/Yadav_followups_20261031/T2_DISPOSITION.md) | Separates matrix, substrate and mature epithelial endpoints; no qualified joint source-ARG1 effect dataset or confirmed host model. A32 is an unexecuted extension, not a relabelled completed run. |

Question-specific reads additionally included A0's pilot, A2's interpretation
amendment, A5/A11's revised result, ES1's measured summary, A10's follow-up,
A12's pilot, A13's coverage report, A15's rival-only report, A16's corrected
matching report, A19's context results, A20's narrowing amendment, A21's
independent expression results and A22/A23's current extension results.
Some long files were read in relevant sections rather than in full; no complete
raw-data, source-code or all-supplements audit is claimed.

## Saved numerical evidence spot checks

Read the saved tables themselves to check the selected headline values against
the prose. These are **inspection checks**, not new inference, raw-matrix
recomputation or independently replicated experiments:

| Evidence inspected | Values used in this assessment |
|---|---|
| [A5 inference](../../../RQ_Specified/A5_developmental_programme_reuse/tables/test_v1/inference.tsv) | 24 primary mice, +0.735466 pp; fixed exclusions +0.557463/+0.602406 pp. |
| [A12 model metrics](../../roadmap_runs/2026-09-27-followthrough/A12_model_metrics.csv) | Primary AT2 source+TNF versus joint RMSE 0.427139/0.324373; the report preserves the opposite fibroblast result. |
| [A11 paired comparisons](../../../analysis/research/runs/g1_a11_paired_prediction_v1/comparisons.tsv) and [capacity comparisons](../../../analysis/research/runs/g1_a11_capacity_qualification_v1/capacity_comparisons.tsv) | Primary lesion mean loss 0.191987 versus 0.190882 for a duplicated p53 feature; the duplicate adds no predictor information. |
| [A30 saved summary](../../../analysis/research/runs/a30_common_support_v1/summary.csv) | Activation-standardized floor-20 median +0.038105 in seven donors; floor-five interval −0.003083 to +0.044199. |
| [Nb4-P09 summary](../../../analysis/research/runs/nb4_p09_expression_specificity_v1_20261007/summary.json) | External cell GRIA1 contrast positive in 4/4 donors; mean +3.600340 log2(CPM+1) difference. This is not an unregularized log-fold change or an effect of GRIA1 perturbation. |

Other numerical details are transcribed from the linked current reports and
are identified as their findings. Prior receipt/arithmetic checks are reused;
they were not rerun simply to repeat a passing result. The review's N/L/Q
assignments and counts are editorial judgments, not a biological statistical
analysis.

## Targeted primary-source checks on 3 November 2026

Purpose: check whether selected apparent target discoveries or contradictions
actually extend published findings. This was **not** a systematic review,
recent-literature clearance for all 33 questions or a fresh search for datasets.

Queries actually used included:

- `"s41467-020-17358-3" "development"`
- `"s42003-024-06111-x" "GRIA1"`
- `"s41588-022-01243-4" "SCN7A"`
- `"Strunz" "2020" "developmental" "correlation" Krt8`
- `"Wang" "PGAM" "2025" "PEP" Th17`

| Source/version and access | Exact checked locator | Consequence for the audit |
|---|---|---|
| [Strunz et al., 2020, published article in PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7366678/) | Discussion paragraph comparing published developmental signatures with Krt8 ADI. Publisher direct access failed; PMC full text was accessible. | The paper reports poor overall correspondence. A5's positive fixed-subset average is compatible with that observation and does not establish global developmental identity. |
| [Jia et al., 2024, Communications Biology](https://www.nature.com/articles/s42003-024-06111-x) | Results “Phenotypic changes of fibroblasts during development and aging,” Fig. 4a,b/Supplementary Fig. 6a. Search-indexed publisher/PDF text identifies an SCN7A/GRIA1 subgroup; direct publisher access failed. | GRIA1/SCN7A expression is a precedent, not a new discovery by A31. The indexed sensory wording does not supply a direct response assay. No full-methods review is claimed. |
| [Madissoon et al., 2023, Nature Genetics](https://www.nature.com/articles/s41588-022-01243-4) | Results “Four distinct cell types in airway peripheral nerves”; Extended Data Fig. 5a,j. Search-indexed publisher text, author PDF text and PubMed figure text were accessible; direct publisher open failed. | SCN7A-positive nonmyelinating Schwann cells are a real specificity rival. This does not prove fibroblast contamination; repeated assays/donors still cannot be counted as independent studies. |
| [Wang et al., 2025, author manuscript in PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12443480/) | Fig. 1E legend/result and Discussion on stress/TGF-beta/serine. PMC text accessible. | The PEP result is a labeled-carbon fraction, not an absolute PEP-pool measurement. The Discussion leaves stress/serine connections for further study. A29's transcript pattern does not choose among those mechanisms. |

Primary-paper support and repository reanalysis are deliberately cited
separately. The audit does not transfer a paper's functional findings to a
repository RNA score, count reused source data as replication, or infer novelty
from the absence of a search result.

## Remaining uncertainty

No new access to private notes/Notion, full chat archives, laboratory resources
or raw molecular assays was established in this pass. Historical statements
about unavailable data are reported as current repository qualifications, not
proof that no new deposit exists elsewhere. An updated source acquisition could
change an eligibility decision; this task did not reopen those analyses.

The review establishes documented claim/evidence mismatches and corrected
framing. It cannot estimate what proportion of the portfolio was “caused by AI,”
infer the author's intent or supply human scientific acceptance. No question
was retired and no unfavorable result was removed.
