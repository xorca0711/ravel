# A21 exploratory methods

## Frozen scope and units

The [intake contract](config/intake_contract.json) preceded quantitative source
selection. The [exploratory contract](config/exploratory_v1.json) was frozen at
2026-09-30 04:08:57 UTC, after source narratives/metadata and before new gene
estimates. Original Nb2 associations and published biological narratives were
already exposed. This is descriptive follow-up, not a confirmatory functional test.

GSE211335 supplies 12 separately barcoded animals, three per condition. Samples
with the same replicate number across conditions are distinct animals.
Technical PoolA/B/C partitions are aggregated within each animal. The analysis
uses exactly the 5,423 deposited endothelial cells, source states, false doublet
flags and positive raw UMI totals. Eight author clusters map to five gCap states,
one aerocyte state, arterial and venous states. Independent identity genes
qualify that crosswalk; Fzd4/cycling did not define the reanalysis labels.

## Measurements

Raw nonnegative integer matrices supply all-gene library denominators.
Twenty-six requested genes map uniquely in every pool. Sum counts per animal/state,
calculate CPM and log2(CPM+1), and retain detection fractions separately.
The six-gene cycling panel averages log2(CPM+1) for Mki67, Top2a, Pcna, Cdk1,
Ccnb1 and Ccnb2. It measures selected cell-cycle RNA, not renewal.

The primary floor is 20 sampled cells per state/animal. Fixed 10/50-cell
sensitivities retain failed comparisons explicitly. Contrasts pair states within
an animal and are reported separately by condition:

- Aggregate gCap minus aerocyte.
- Author transitional state 1 minus major gCap state 0.
- Author cycling state 7 minus major gCap state 0.

Report all points, sample numbers, mean/median, observed range and signs.
Within-condition Spearman correlations relate Fzd4 CPM to the cycling panel
separately in aggregate gCap and state 0, only with at least three eligible animals
and variable inputs. No across-condition pooled correlation, P value, population
confidence interval, model-adjusted effect or trajectory fit is produced.

## Denominator discrepancy and amendment

An exact-match check stopped the first run before new gene estimates. Raw UMI
totals matched author nCount_RNA in 4,705 cells; 718 differed by 1–10 UMIs.
A per-pool gene-prevalence filter of at least three cells reconstructs 5,421
of 5,423 totals, with two one-UMI residual differences. Published code begins
from an existing object, so exact initial filtering remains unresolved.

The [recorded amendment](reports/denominator_amendment.json) retains every cell,
the frozen raw-count denominator and all comparisons. A sensitivity substitutes
the deposited author denominator while holding target counts fixed. It is not
an exact reproduction of author filtering. All 648 group-mean contrast directions
agree between these denominator choices. The [cell audit](tables/umi_denominator_audit.tsv)
and sensitivity table retain the discrepancies.

## Reused cohort evidence

Eight Nb2 day-42 CAP1 records join uniquely to round, reporter genotype, sex
and label-cohort identifiers. Sex fields agree. Previously reported pooled and
within-round coefficients are reconciled; no new adjustment or search for a
positive association is performed. These estimates remain reused evidence.

## Reproduction

From the repository root, with Python numpy/pandas/h5py/scipy/matplotlib and
a PDF renderer available:

    python RQ_Specified/A21_fzd4_capillary_function/scripts/00_fetch.py
    python RQ_Specified/A21_fzd4_capillary_function/scripts/umi_audit.py
    python RQ_Specified/A21_fzd4_capillary_function/scripts/01_analyze.py
    python RQ_Specified/A21_fzd4_capillary_function/scripts/02_figures.py
    python RQ_Specified/A21_fzd4_capillary_function/scripts/03_verify.py

The fetch script restores and hash-checks the three named H5 members used by
the denominator audit. Completed results must be preserved and versioned;
the analyzer refuses to overwrite a completed run.

Downloaded matrices, cell extracts and source payloads are ignored cache.
Tables, contracts, scripts, retrieval hashes, amendment and figure hashes are
tracked. Figures use 300-dpi PNG and vector PDF/SVG. No new biological acceptance,
claim grade or inferred Fzd4-dependent lineage effect is assigned.
