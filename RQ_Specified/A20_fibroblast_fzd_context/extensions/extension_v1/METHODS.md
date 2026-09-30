# A20 extension methods

## Source and frozen scope

The [publisher-linked figshare deposit](https://doi.org/10.6084/m9.figshare.7740071.v1)
contains integer nonnegative counts for 32,734 genes from four human fibroblast
donors, each with vehicle, CHIR, TGF-beta and combined treatment.
The [intake contract](config/intake_contract.json) predates dataset selection;
the [analysis contract](config/analysis_contract.json) was frozen at
2026-09-30 02:19:04 UTC after source narratives, labels and count integrity checks,
before new gene estimates. Prior A20/A19 findings were already exposed.
This is exploratory, not independent Fzd-mechanism confirmation.

Forty-five genes were requested using a recorded human Ensembl mapping.
FZD10 was absent; the mapping gate failed before outcomes. An explicit amendment
retains it as missing and executes 44 genes without replacement or panel change.
FZD3/5/8/9 and HEYL fall below the descriptive detection rule
(>=10 counts in >=4 libraries).

## Normalization and estimands

edgeR TMM effective library sizes use the entire supplied matrix, followed by
log2(CPM+1). This is an adaptation, not reproduction of the source publication's
differential-expression filter or significance testing.

For each donor, compute CHIR minus vehicle, combined minus TGF, TGF minus
vehicle, combined minus CHIR, and the direct interaction
combined - TGF - CHIR + vehicle. Fixed panels average gene log2(CPM+1) before
contrasts. Their genes are all present and adequately detected:

- Canonical response: AXIN2/NKD1/NOTUM/TCF7/LEF1.
- Support: WNT2/FGF7/FGF10/HGF.
- Collagen: COL1A1/COL1A2/COL3A1/COL5A1/COL5A2/COL6A1/COL6A2/COL6A3.
- TGF response: SERPINE1/PMEPA1/TGFBI.

No receptor belongs to these panels. Summaries retain every donor, mean, median,
range, signs and the range of all four leave-one-donor means under fixed
normalization. Library-total
CPM is the frozen normalization sensitivity. No P values, population intervals,
post-treatment mediator regression or genome-wide discovery is performed.

## Source-unit audit

Jones GEO and NCBI BioSample records agree on genotype/accession but do not
resolve animal/pool membership. Riccetti metadata retains 18 libraries
(3 per exposure at P4/P7/P10); functional wells/slides cannot be assigned as
independent animals. No new RNA model uses those sources. Ng RNA and functional
cohorts differ, preventing a matched donor-level function join.

## Reproduction

From the repository root, with the Python scientific environment and R edgeR:

    python RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1/scripts/00_fetch.py
    Rscript RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1/scripts/01_normalize.R RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1
    python RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1/scripts/02_analyze.py
    python RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1/scripts/03_figures.py
    python RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1/scripts/04_verify.py

The analyzer refuses to overwrite completed results; preserve/version first.
The standard-library verifier checks count denominators, donor pairing,
transformations, panels, interactions, missingness, figures and preserved prior
files independently of pandas/edgeR. Payloads and full intermediate matrices stay
in ignored cache. Frozen mapping records are tracked, so numerical reproduction
does not require a live gene lookup.
