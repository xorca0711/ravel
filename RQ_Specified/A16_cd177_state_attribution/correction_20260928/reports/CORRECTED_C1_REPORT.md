# A16 corrected C1 comparison, 28 September 2026

**Executed exploratory correction; the priming difference attenuates but remains positive in both libraries. Matching leaves appreciable positional imbalance, so neither attenuation nor persistence establishes marker-specific or intrinsic biology.** No claim grade, biological status or original Stage1 artifact changed.

The [amended specification](../config/corrected_c1_specification.json), [660 excluded genes](../config/excluded_genes.tsv) and readiness record were committed at `e1d46b4f68453eedde9166f11b772576462a9f6d` before corrected outcomes were calculated. This is a bounded C1 computation on fully exposed data, not independent confirmation. [Effects](../tables/corrected_c1/effects.csv), [matching quality](../tables/corrected_c1/matching_quality.csv), [run record](../tables/corrected_c1/run_record.json), [verification](../tables/correction_verification.json).

## Primary result on one fixed population per library

| Library | Fixed Cd177+ / negative cells | Marginal raw difference | Matched raw difference, k=10 | Marginal / matched fixed-population standardized difference |
|---|---:|---:|---:|---:|
| GSM7890835 | 79 / 797 | 1.255829 | 0.409807 | 1.455332 / 0.474909 |
| GSM7890836 | 60 / 596 | 1.331844 | 0.315110 | 1.839246 / 0.435159 |

The outcome is the unchanged mean log1p(full-library CP10k) of Lcn2, Lrg1, Retnla and Ptgs1. Raw differences are in that score's units. Both effects in a library use the same outcome SD across **all fixed cells**: 0.862916 and 0.724125 respectively. These standardized values are not the original Stage1 pooled-group SMDs or its matched-pair SD units, and cannot be compared with its C3 reference-gene band. The change between marginal and matched differences is not a fraction of signal explained.

Every original `primary_include=True` and `gate_transition=True` cell in each primary library is retained, with the unchanged at-least-two-of-Cldn4/Ndrg1/Sox9 detection gate. The original verified cell table yields 876 and 656 cells. The founding prose's 878 and 658 counts do not override these actual inclusion flags. No round-2 label requirement, pooled subcluster population, new doublet call or remade gate enters this comparison.

The predeclared k sensitivity is descriptive:

| Library | k=5 matched raw difference | k=10, primary | k=20 |
|---|---:|---:|---:|
| GSM7890835 | 0.316339 | 0.409807 | 0.469867 |
| GSM7890836 | 0.227578 | 0.315110 | 0.486227 |

All fixed positive cells were matched at all three k values. No result was used to choose k, latent dimensions, feature set or eligible cells.

## Matching support and residual imbalance

| Primary k=10 diagnostic | GSM7890835 | GSM7890836 |
|---|---:|---:|
| Positives matched / fixed positives | 79 / 79 | 60 / 60 |
| Unique negative controls used | 254 | 151 |
| Control-weight effective sample size | 124.67 | 77.69 |
| Largest reuse count for a negative | 17 | 17 |
| Largest negative weight | 0.02152 | 0.02833 |
| Mean / 95th-percentile neighbour distance | 9.777 / 13.282 | 9.714 / 13.466 |
| Maximum absolute PC standardized imbalance, before | 1.30154 | 1.59559 |
| Maximum absolute PC standardized imbalance, after | **0.62495** | **0.52100** |

Every depth quartile has candidates for every fixed positive, and all six library/k comparisons clear the required 30-positive/30-distinct-negative floors. Availability does not establish good common support. No distance caliper was specified; all positives are retained, some neighbours are distant, and the strongest PC imbalance remains substantial. Distances are local PCA units and have no external acceptability threshold. The [20-PC balance table](../tables/corrected_c1/PC_balance.csv), coordinates and [edge list](../tables/corrected_c1/matched_edges.csv) preserve the diagnostics. Reused controls, graph edges and effective sample sizes do not create independent animals or donors.

## Secondary outcomes, k=10

These endpoints are retained for consistency, with no promotion based on their direction.

| Endpoint | GSM7890835 marginal -> matched raw | GSM7890836 marginal -> matched raw |
|---|---:|---:|
| AT2 identity | 0.695824 -> 0.112045 | 0.997005 -> -0.042701 |
| AT1 identity | 0.252855 -> 0.006614 | 0.155498 -> -0.025310 |
| Itga2 | -0.397238 -> -0.030124 | -0.651080 -> -0.004508 |
| Cycling | -0.015371 -> -0.009126 | 0.125699 -> -0.068290 |
| Shared disjoint remodelling | -0.261051 -> -0.128004 | -0.487182 -> 0.002880 |
| Lesion disjoint remodelling | -0.088645 -> -0.021806 | -0.097601 -> 0.000997 |

Cycling RNA is not measured proliferation. There are no p values, confidence intervals, pooled estimates, cell-based biological inference or old-C3 null comparisons.

## What was corrected and what remains unresolved

The space was fitted separately within each library's fixed transition population. All 660 frozen grouping, gate, module, individual and inclusion-panel genes, plus mitochondrial features, were excluded **before normalization and the depth denominator**. Thus those genes cannot enter through the normalized library size. The algorithm selects up to 2,000 remaining variable features using no group/outcome labels and fits a centered, unscaled, deterministic 20-PC space with one BLAS thread. Feature ties use symbol then original feature-row index, so duplicated symbols do not make selection ambiguous. Full SVD signs are canonicalized. This local PCA is an explicit amendment to the unavailable original integrated embedding, not a reconstruction of the author embedding.

Cd177-negative neighbours come only from the same library and depth quartile. Matching uses replacement across positive cells, preserves every fixed positive, and uses one common effect scale for marginal and matched comparisons. These changes repair the computational population/scale mismatch identified in the integration review. They do not establish that the selected coordinates remove all relevant position.

Gene exclusion removes **direct** reuse; correlated remaining genes may still encode the response, and conditioning on them can overadjust real biological state. The RNA-based transition gate and Cd177 detection groups retain selection, depth and detection dependence. Outcome scores still share a full-library normalization denominator. Ambient RNA, unknown source/handling variation and incomplete matching support remain unresolved. The two libraries have no deposited independent animal identities. Attenuation or persistence therefore cannot be read as a causal decomposition, marker specificity, cell-intrinsic function or an exclusion of contamination.

## Provenance, checks and execution

The first main-checkout cache inventory found missing processed inputs; that [initial record](../tables/readiness_main_only.json) is preserved. The earlier `england-analysis-plan` checkout then supplied read-only historical caches. The [resolved readiness record](../tables/readiness.json) verifies the original cell table, both batch1 QC files and six raw input files against saved historical hashes. No historical checkout or main cache was modified.

The runner reads the original raw matrix/feature/barcode triplets and selects the verified fixed barcodes directly, avoiding Stage1's unhashed matrix/barcode caches. Reconstructed full-library totals, detected features, Cd177 UMIs and transition calls agree exactly. All 14 library/endpoint score comparisons agree with the original cache to at most **4.44e-16**, below the frozen 1e-8 stop tolerance. [Instrument parity](../tables/corrected_c1/instrument_parity.csv).

Six synthetic dependency-free tests passed for gene-exclusion isolation, population/depth rules, whole-comparison rejection when a positive lacks candidates, distinct-control floors and the common effect scale. A separate standard-library verifier passed ten checks, recomputed actual nearest neighbours and all 42 effects from saved coordinates/cell scores/edges, and confirmed every original Stage1 hash. Maximum effect recomputation error was **4.44e-16**. The scientific runner needs the existing NumPy/SciPy/Pandas stack; the tests and saved-evidence verifier do not add dependencies to CI.

Executed from the managed checkout:

```powershell
$python = 'C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$base = 'RQ_Specified/A16_cd177_state_attribution/correction_20260928'
& $python "$base/scripts/test_invariants.py"
& $python analysis/scripts/run_with_environment.py --site-packages X:/GitHub/scRNA_seq/.venv-x64/Lib/site-packages "$base/scripts/02_run_corrected_c1.py" --spec-commit e1d46b4f68453eedde9166f11b772576462a9f6d
& $python "$base/scripts/03_verify_corrected_c1.py"
```

The runner refuses to overwrite completed output. The saved-evidence verifier can be rerun directly. A raw rerun requires a separate output-free copy; preserve this run and original Stage1 first. The current correction is complete within its computational scope; biological attribution remains inconclusive.
