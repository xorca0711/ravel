# Bounded external human RNA description

29 October 2026; prospective specification before new external effect fits.
Article-local DY1-P01, exposed descriptive transport question. The primary
GSE136831 Macrophage20 result remains primary; its AllMacrophages50 analysis is
an already declared sensitivity comparator. No new canonical question is created.

## Qualification and amendment

GSE135893, Habermann et al., is a published separate collection from the Adams
source, with different annotation and processing. This supports external context,
not a direct patient-identity audit. Metadata contain 30 donors: 12 IPF, 10
Control and eight other fibrotic diagnoses. The 43 distinct `orig.ident` labels
are source metadata identifiers, not proof of 43 independent biological libraries;
they also differ from the 34 GEO sample records. Sample_Name is the donor unit.

[Qualification v1](../../analysis/research/runs/DY1_external_human_qualification_v1/receipt.json)
failed before raw reading because the current preparation script hash differed
from its historical record. Git blob `02ff8b6:analysis/corrections/statistics/prepare_counts.py`
exactly matches SHA-256 `01b44d4aa5dd977c1a997a49e03edd8a227860b7b18cb65bcdf2add66e83271c`;
the later `8d6990f` diff changes only repository directory paths. V1 is preserved.
[V2](../../analysis/research/runs/DY1_external_human_qualification_v2/receipt.json)
binds that historical blob as read-only evidence and never executes it.

V2 read all 338,061,955 raw sparse entries. All 85 cached donor/annotation units
match current raw all-gene totals and source nCount_RNA; they do not all match
nCount_SCT. NPZ and CSV serializations, historical totals, donor/diagnosis/cell
joins and the 29 exactly mapped selected genes match. The original raw matrix
lacked a historical hash; current hashing and reaggregation do not retroactively
create one. Of 220,213 raw columns, 114,396 have deposited filtered annotations;
105,817 unannotated columns do not enter donor aggregates.

The full 30-symbol qualification retains a hold: SELENOP has no exact symbol
match. No alias is substituted and absence is not biological zero. It is an
identity marker, not one of the nine already proposed outcome genes. All nine
genes for the two panels plus ARG1 map uniquely and pass direct raw parity, so
this restricted comparison is supported. No external proxy/NAM analysis is run.

## Frozen comparison

Use all 21 eligible donors: 12 IPF and nine Control. The historical cache first
required 50 macrophage-compartment cells per donor; one of ten source controls
is not retained. Keep that floor and selection limitation. Aggregate exact
`Macrophages` + `Proliferating Macrophages` as the external union, with
`Macrophages` alone as an annotation sensitivity; neither is renamed as NAM or
assumed equivalent to the primary label. Sum raw gene counts and all-gene totals
across annotations **before** logCPM. No monocytes are included.

The outcomes are FABP4 panel (ATP10A/FABP4/SERPING1/SVIL), matrix macrophage panel
(MMP9/LGMN/PLA2G7/RGS1), and ARG1 log2(CPM+1), using the primary formula. For each
annotation, report all IPF−Control donor mean differences and 2,000-resample
pointwise bootstrap intervals. Report within-IPF and within-Control panel
Spearman rho with 1,000 paired bootstrap draws, the fixed eight-donor minimum,
varying outcomes and at least 95% defined resamples. Seed: 20261029. No p-values,
effect margin, power claim or multiplicity-controlled discovery.

Source imbalance is explicit: IPF comprises seven Vanderbilt and five NTI
donors; eligible Control comprises six Vanderbilt and three DNA source labels.
The exact common-source sensitivity is `Sample_Source == Vanderbilt`, seven
IPF/six Control. Its contrasts are supported, but both within-group correlations
fail the existing eight-donor rule and remain unestimated. Donor IDs, diagnoses,
source labels and selection sets are frozen in the numerical contract. External
age/sex, smoking, treatment and clinical variables are unqualified; no clinical
adjustment is claimed. Source restriction does not remove all confounding.

Cached fibroblast support is seven IPF/three Control, below the same fixed
correlation minimum. No within-disease recipient association is fitted or rescued
by lowering the rule. No COPD comparison, exact author-model reproduction,
enzyme/function inference or new cohort search is added to rescue results.

## Exposure and interpretation

Prior Ravel GSE135893 analyses and the primary atlas findings are exposed.
This is a transport/robustness description in a separate collection, not
unexposed confirmation. Different annotation, source-site composition, captured
cell mixture, cache selection and unmeasured clinical variables are consequential
alternatives. All supported, unfavorable and non-estimable results remain saved.

Primary-source discovery, actual queries, access restrictions and source locators
are retained in [external literature discovery](HUMAN_EXTERNAL_SOURCES.md).
The source counts are independently recalculated from the current raw assay;
outcome arithmetic is checked against those direct aggregates and SciPy ranks.
Execution completion and technical review confer no scientific acceptance.
