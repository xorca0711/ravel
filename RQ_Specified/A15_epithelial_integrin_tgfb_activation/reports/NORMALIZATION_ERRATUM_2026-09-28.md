# A15 rival-2 normalization erratum, 28 September 2026

**The original median-of-ratios sensitivity is invalid and is replaced by the versioned correction below.** The corrected sensitivity remains non-separating for both original epithelial panels, so it does not add a sensitivity downgrade. The original primary results and the historical `weak_bound_on_rival_2` algorithmic label are unchanged. Epithelial mediation remains unresolved, the parent A15 test remains blocked, registration remains pending, and no claim or grade changes.

The [correction specification](NORMALIZATION_CORRECTION_SPEC_V1.md) and [machine-readable contract](../config/a15_rival2_normalization_correction_v1.json) were committed at **`f3950253ae229f062dbae94551b04a908a8e5ade` before corrected outcomes were computed**. The original v3 freeze, execution script, tables and [results report](RIVAL2_RESULTS.md) are preserved unchanged. The [27 September interpretation clarification](INTERPRETATION_AUDIT_2026-09-27.md) continues to govern the biological reading.

## Defect and repair

The original script estimated raw-count median ratios from its targeted gene union, then divided each count by both its factor and its library total. The factor already contains a depth component. On identical compositions with library B exactly twice A, correct count/factor values are identical; the original extra total denominator instead makes B half A. Consequently, the original report's statement that both declared sensitivities agreed relied on an invalid alternative-normalization calculation and is withdrawn as evidence. The separately computed CPM primary was not affected by this defect.

The new calculation uses **15,174 reference genes** from all 42,548 matrix rows: positive in all eight original epithelial libraries, excluding the seven scored panel genes and `Itgb6`. No treatment-label, effect, p-value or variability filter selects these genes. It takes the arithmetic median of raw-count/geometric-gene-mean ratios, then centers the eight factors to geometric mean 1. Each panel score is the equal-weight mean of `log2(count / factor + 1)` over the unchanged original measurable genes (5/5 transitional and 2/2 identity). Size factors range from 0.7488 to 1.3262. Library total is not divided out again.

These are **unstandardized log2 normalized-count scores**, with a +1 normalized-count pseudocount. They are not CPM or standardized scores. The numerical differences between normalization rows below combine the repaired estimator, broader reference and explicit score scale; they must not be read as a common-unit effect change. The point-estimate sign for identity changes from negative to positive, while every epithelial panel decision remains non-separating.

## Numerical and gate consequences

Every contrast retains the original four case mice (218, 219, 226R, 228) versus four references (204, 206, 208R, 225), epithelial compartment, bleomycin exposure and S151 batch. The exact two-sided rank-sum test enumerates all 70 assignments; the gate is p <= 2/70. No saline or new exploratory contrast was added.

| Version and score units | Panel | Case minus reference mean | Exact two-sided p | Separates |
|---|---|--:|--:|---|
| Preserved primary, standardized log2 CPM | Transitional | -0.3599 | 0.885714 | No |
| Preserved primary, standardized log2 CPM | Identity | -0.2107 | 0.685714 | No |
| Preserved unstandardized log2 CPM sensitivity | Transitional | -0.1563 | 0.685714 | No |
| Preserved unstandardized log2 CPM sensitivity | Identity | -0.0497 | 0.685714 | No |
| Withdrawn defective normalization, historical scale | Transitional | -0.1491 | 0.342857 | No |
| Withdrawn defective normalization, historical scale | Identity | -0.0425 | 0.885714 | No |
| Corrected log2 normalized counts | Transitional | **-0.085856** | **0.685714** | **No** |
| Corrected log2 normalized counts | Identity | **+0.021399** | **0.885714** | **No** |

| Corrected panel | Hodges-Lehmann shift | Pairwise-shift interval |
|---|--:|---|
| Transitional | -0.048786 | [-0.523072, +0.456674] |
| Identity | +0.102947 | [-1.005967, +0.683664] |

Intervals span the full range of the 16 case-minus-reference differences. Their attained coverage is 68/70 = 97.142857% under a continuous common-shift, exchangeable model; they are not asserted to have that interpretation under arbitrary distribution or composition changes. All eight scores, reference IDs, factors and pairwise shifts are retained in [the new output directory](../tables/rival2_normalization_correction_v1/) and [run record](../tables/rival2_normalization_correction_v1/correction_run.json).

Neither corrected panel disagrees with its actual saved standardized CPM primary separation decision. Holding engagement, omnibus, composition, handling and other gates at their original values leaves **no downgrade reasons** and leaves the historical algorithmic label unchanged. This is a valid replacement sensitivity under its assumptions, not retrospective validation of the original code. Non-separation does not establish equivalent epithelium, absent epithelial response, exclusion of mediation, or evidence for or against the A15 mechanism.

## Verification and provenance

All seven regression tests passed (the initial six, then one added gate test). They check the defining proportional-library invariance, explicitly demonstrate failure of the old denominator, and check positive-reference exclusions, arithmetic median convention, insufficient-reference refusal, exact/tied ranks, overwrite protection and sensitivity-disagreement downgrading without mutating the saved decision. The independent [NumPy/SciPy verifier](../scripts/05_rival2_normalization_verify.py) re-reads the deposited counts without importing either execution script: **62 checks passed, zero failed**. It re-derives reference membership, all eight factors and scores, effects, ranks, all pairwise shifts, intervals and gates. It also reproduces the actual preserved standardized and unstandardized CPM primary scores, effects and p values, rather than comparing against a newly invented baseline. Its [verification record](../tables/rival2_normalization_correction_v1/independent_verification.json) pins the source and output hashes.

Both original cache hashes matched before execution and remain recorded in the output:

- Counts: `X:/GitHub/scRNA_seq/RQ_Specified/A1_transitional_epithelial_state_distinction/cache/inputs/GSE190821/GSE190821_counts.csv.gz`, SHA-256 `2c8a21fd68c355330bfee2e5e63ca3d415d7f4677a3b783669d9acb0a595d1f7`.
- Symbol map: `X:/GitHub/scRNA_seq/.claude/worktrees/sharp-margulis-5e858e/RQ_Specified/A15_epithelial_integrin_tgfb_activation/cache/ensembl_symbol_lookup.json`, SHA-256 `0a8da7c1ad99c3f7cd1cde806d49b853c03c91a0b60c7eee08ac3b892133fe7b`.

The symbol map was found in the preserved source worktree because the current main A15 cache directory is absent. It was accepted only because its bytes match the original run; no genes were remapped and no raw source was written. The original join, freeze, run and execution script hashes are also pinned and checked.

Exact execution commands, run from `C:/Users/dream/.codex/worktrees/rq-gap-fill/scRNA_seq`:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'analysis/tests/test_a15_normalization_correction.py'
& 'C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'analysis/tests/test_a15_normalization_correction.py' NormalizationCorrectionTests.test_sensitivity_disagreement_adds_only_its_downgrade
& 'C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'RQ_Specified/A15_epithelial_integrin_tgfb_activation/scripts/04_rival2_normalization_correction.py' --data-root 'X:/GitHub/scRNA_seq' --output-dir 'C:/Users/dream/.codex/worktrees/rq-gap-fill/scRNA_seq/RQ_Specified/A15_epithelial_integrin_tgfb_activation/tables/rival2_normalization_correction_v1' --freeze-commit 'f3950253ae229f062dbae94551b04a908a8e5ade'
& 'C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'analysis/scripts/run_with_environment.py' --site-packages 'X:/GitHub/scRNA_seq/.venv-x64/Lib/site-packages' 'RQ_Specified/A15_epithelial_integrin_tgfb_activation/scripts/05_rival2_normalization_verify.py' --data-root 'X:/GitHub/scRNA_seq' --output-dir 'C:/Users/dream/.codex/worktrees/rq-gap-fill/scRNA_seq/RQ_Specified/A15_epithelial_integrin_tgfb_activation/tables/rival2_normalization_correction_v1'
```

Execution refuses any existing output directory. Verification refuses an existing verification file. A future rerun needs a different output directory and the same committed specification; it must not overwrite this evidence.

## Remaining limits

The broad-reference estimator assumes typical reference-gene relative abundance is stable or changes are balanced. Positivity selects broadly detected genes; it does not prove biological invariance. Without an absolute RNA reference, global abundance changes remain unidentified. The raw-count score scale and +1 convention are fixed in the correction specification, not tuned to match the primary.

Four mice per arm, unestablished allocation randomization, an enriched epithelial translatome rather than a pure isolated state, possible subtype/composition changes and lack of a mediation-identifying design remain. The corrected sensitivity repairs an analysis error; it does not supply new biological units or measurements and cannot resolve the parent mechanism.
