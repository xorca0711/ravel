# Prospective description of Gorby's reported CD8 response estimates

8 November 2026; Sx10-P01, exposed descriptive work. Read the
[source amendment](SOURCE_AMENDMENT_V2.md) first. The common expression matrix
failed qualification and stays held. This stage uses twelve author-deposited
comparison tables, not reconstructed raw-count effects or a pooled cross-study
estimate. V2 source qualification admits all 36 fixed target records.

Exactly IFNG/ENSG00000111537, GZMB/ENSG00000100453 and
IL18RAP/ENSG00000115607 are retained. Source codes D85/D93/D36 each have
WTD/R5A11D at 0.1/50 nM versus their labelled unstimulated control. Published
three-donor and within-donor analysis descriptions support that intended design;
the inconsistent biorep labels and unrecovered independent donor crosswalk remain.
No population inference, p-values, effect-margin decision or sample-size claim.

Primary quantity L is each table's deposited `log2foldchange`. For each target,
dose and source code, calculate L(R5A11D versus control) minus L(WTD versus
control). Call this a **difference of reported response estimates**, not the
direct log-fold change from a common expression matrix. Show all source values,
the arithmetic mean across the three source codes, and all three single-code
omission means. These omissions reuse data and are not confidence intervals.

Secondary quantity Q is log2(stimulated.value/control.value) only if both values
are finite and strictly positive. It is a separately labelled source-derived
ratio, not an assumed reproduction of the reported fit. Compute the corresponding
Q difference and means/omissions. If a required value is missing/zero, retain an
unsupported result; do not add a pseudocount or average the remaining codes into
the nominal complete-case result. Flag any supplied value below 1 without
changing target membership. No averaged/reused control vector is constructed.

Outputs: 36 source rows; 36 code/dose/quantity differences; 48 summaries
(3 targets × 2 doses × 2 quantities × full/3 omissions), complete missingness,
and a two-row figure showing reported responses and their differences. No EC50,
time-course model, gene-set screen, monomer contrast or post-result target addition.
Inference remains restricted to the specified six-day source context. Compare
directions to the existing Saxton result narratively; do not pool magnitudes.

Verification uses a separate script with direct raw-file parsing and Decimal
logarithms/arithmetic, no imports from production, at 1e-10 absolute tolerance.
It checks source identity/values, all contrasts and summaries. Inspect the PNG
for legibility and accurate labels before reporting. A later numerical amendment
would require another version; these outputs will remain immutable.
