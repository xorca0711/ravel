# A12 cell configuration v1 — prospective exposed description

Frozen before new cell expression outcomes. The primary comparison is the
original twelve A12 patients (4,5,6,7,14,17,18,19,21,22,24,25), LUAD minus normal,
exact `AT2` transferred label, finest uncertainty <=0.2, >=50 pooled QC nuclei
per patient/histology. No extra source-macrophage eligibility is imposed on this
recipient description; the original recipient roster must be exactly recovered.
All 75 libraries are retained for broader, explicitly exposed context.

Read `review_gene_row_CSC_v1` by gene pointer; row indices are original cell
positions. Join only via `source_cell_index`, verify GSM:barcode, patient,
histology, totals, detected genes, mitochondrial percentage and the original QC
(>=500 genes, >=1000 counts, <20% mitochondrial). Annotations must exactly cover
the stored QC cells. Never treat this store as AnnData or zero-fill missing genes.
Hardlinks reuse source bytes; every input is hashed and opened read-only.

Ten fixed transcripts: IL1R1, IL1RAP, IL1R2, IL1RN, SIGIRR, MYD88, IRAK1,
IRAK4, NFKBIA, TNFAIP3. No new composite, prediction, ranking or response fit.
Primary pair IL1R1/IL1RAP; three descriptive pairs IL1R1 with IL1R2, IL1RN,
SIGIRR. Detection is raw count >0. Report all four joint categories, joint fraction,
and accessory/context detection conditional on detected IL1R1 (undefined if no
IL1R1-positive cell). These are barcode RNA co-detections, not protein complexes.

Per gene report fraction detected, mean count, mean log2(1+10000*count/full-library)
and conditional positive-cell mean of that same log quantity, plus summed-count
log2(1+CPM) for exact parity with the old component primitives. A measured zero is
undetected RNA, not receptor absence. Positive-only means with no detections are
missing, never zero. Repeated blocks are pooled within patient/histology; a second
view averages block statistics equally. Patients have equal weight in summaries.

Selection sensitivities use the same primary twelve patients and histologies:
AT2 uncertainty <=0.3; AT2 all QC (including low-confidence candidates); broad
`Epithelial` candidates at finest uncertainty <=0.2; broad Epithelial all QC.
No remapping. Preserve every transferred label/confidence category in an all-QC
inventory; non-epithelial and ambiguous candidates are not silently reassigned.
Broader all-patient/all-histology tables are description, not extra replication.

Depth sensitivity uses the primary population. Cross-classify full-library counts
at [1000,2000,4000,8000,infinity) and detected genes at
[500,1000,2000,4000,infinity). Retain only bins with >=5 nuclei in both histologies
of a patient; weights are their pooled frequencies, renormalized over common
support. Record retained mass, counts and missing support. This is a measurement
sensitivity, not a new biological population or a power threshold. Standardize
detection and joint fractions; no model-based imputation or threshold relaxation.

Show all individual paired deltas, equal-patient mean/median/range and leave-one-
patient-out mean range. The latter is influence sensitivity, not a confidence
interval. No independent-cell p-values, power margin or general-population null.
Verify all primary counts/detections/pairs by a separate sparse-reader arithmetic
implementation and compare all 240 primary summed-count gene values with the
frozen old component output. Failed identity/coverage/QC/parity stops execution;
invalid narrower sensitivity support is reported missing, not rescued.

[Context and search record](PUBLIC_DATA_CONTEXT.md). Author-dependent stages 3–6
remain held; WES/P7/mouse S5 ambiguities do not gate unrelated public RNA.
