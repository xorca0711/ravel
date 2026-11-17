# S5 proposal: connect molecular descriptions with functional evidence

18 November 2026. **S5M is coordinator-reviewed and authorized after S3 finalization;
S5F remains prepared for later review/assignment after the S5M result.**
Prepared while the frozen S3 run was extracting signals, without viewing partial
S3 effects or selecting integration results. The coordinator subsequently reviewed
completed S3 and this proposal without numerical revision. Freeze S5M code/contract
after preserving S3; do not execute S5F before S5M result review. Owner remains `Nk17-P01`.
This uses the coordinator's bounded 18 November source/caption review and supplied
S5 framing, not a new broad literature or workbook search.

## Purpose and decisions

Naik's published argument connects inflammatory history, regulatory persistence,
recall and repair. S2/S4/S4B provide mixed relative RNA evidence and a baseline
reference limitation. The approved S3 endpoint measures relative ordering near
protein-coding gene boundaries, with distal regions and original memory domains
unassayed. S5 should assess how those qualified descriptions align and reconstruct
separate functional measurements at their own biological units. Concordance would
support a source-specific association; weak or reference-sensitive alignment
would narrow it. Neither outcome identifies a causal chromatin-to-repair path.
Use two separate exposed contracts, S5M and S5F, with review of each result.
Naik Figure 5c reports increased IL-1beta protein without increased Il1b
transcript (coordinator bounded source read); weak RNA alignment alone therefore
does not refute that published protein/functional premise. RNA, protein/activity
and function remain distinct endpoints.

## S5M: frozen molecular endpoints together

Join immutable S2 `gene_effects.tsv`, S3 gene/window mapping and effects, S4
`gene_effects.tsv.gz`, and S4B `reference_effects.tsv.gz` by exact versioned M9 IDs.
Retain a complete mapping/eligibility table, including absent, unassayed and
noncoding entries. Preserve every RNA low/zero flag and ATAC encoded-zero/zero-mean
flag. Even a constant local zero can change rank when universe/tie mass changes;
retain this interpretation through all displays and associations. Do not assign
nearest enhancers, impute missing ATAC values,
reproduce the original 73/140 overlap, or combine RNA log effects and ATAC
percentile points into a memory score.

Proposed primary display/statistic universe: mapped genes with finite required
RNA values and both frozen S2 time qualifications and S4 `all_three_qualified`.
Use the unchanged frozen thresholds; this exposed RNA qualification is not a
claim of reliable expression in every history group. Preserve the all-mapped,
finite-RNA universe as a separately labelled sensitivity. Each universe stays
fixed across both window widths, all baseline references and normalization
sensitivities; never select on an ATAC contrast. Report its exact genes/anchors
before interpreting a correlation.

Within each universe, describe D6 RNA versus D6 rank contrast and D30 RNA versus
D30 rank contrast. Compare D30 rank contrast with S4 B0, unadjusted W6/W12, and
baseline-adjusted W6/W12 under the primary and both S4B references. Primary RNA
scale is each stage's frozen MOR; retain its frozen total-count sensitivity.
No refitting, cross-context subtraction or preferred-width/reference selection.
S2 D30 and S4 B0 reuse GSM2440989–992 under different normalization contexts;
label them separately and never count them as replication.

Use descriptive gene-feature Pearson/Spearman associations with no p-values,
confidence intervals or biological replicate count. All gene mappings remain in
the display/statistic, so shared TSS proxies can repeat an ATAC value. Report that
multiplicity; prespecify inverse-multiplicity weighted Pearson sensitivity, giving
each anchor total weight one within the same eligible universe. Neither weighting
removes dependence among nearby/overlapping genomic features.

Always display baseline and unadjusted associations beside adjustments. For a
fixed universe/weighting, verify `cov(X, A_t)=cov(X, L_t)-cov(X, L0)`; correlations
themselves are not subtracted. Both times share L0, so two adjusted associations
are not independent corroboration and may arise through the baseline term.
Retain the source/marker discrepancy and low/zero flags; do not assign sex or
correct the primary libraries.

Proposed figures: one compact association/component display across all frozen
sensitivities, plus separate-axis examples for the paper-selected Aim2, Casp1,
Il1b, Il1r1 and Il18 anchors. Resolve exact M9 IDs prospectively and retain
unassayed/unqualified panels; no replacement winners or implied paired cells.

## S5F: separate functional-source reconstruction

Saved sources are `raw_data/naik2017_s01_sources/` workbooks named
`41586_2017_BFnature24271_MOESM{7,10,11}_ESM.xlsx`. Freeze exact hashes and source
cell locators in the eventual contract. The following is the coordinator's
bounded source map; individual measurements/effects have not been recalculated.

| Source cells | Endpoint/unit evidence | Proposed bounded treatment |
|---|---|---|
| MOESM7 F1g, Ctrl A3:A25; PI B3:B16; headers A2/B2 and replicate note D2 | Day-10 explant outgrowth distance in mm; 23 Ctrl/14 PI biological-replicate rows; supplied final PDF Fig. 1 caption, page 2, defines n as animals | Unpaired finite-sample mean/median differences and all observations; no individual-cell migration-speed or omics pairing claim |
| MOESM7 F1e, rows 3:5, days 1/3/5; Ctrl B:G, PI H:M | Epithelial tongue length, micrometers; source Ctrl/PI counts 5/4, 4/4, 6/6 at days 1/3/5 | Retain these cell counts and all values; caption n=4 is discrepant; no forced four or cross-day matching |
| MOESM7 F1e, rows 11:13; Ctrl B:E, PI F:I | Source proliferating/EdU-positive percentages; counts 4/4, 3/2, 2/2 at days 1/3/5 | Describe percentage-point contrasts; labeling is not a measured division rate and nonsignificance is not equivalence |
| MOESM7 F1b, area rows 3:13 Ctrl/19:29 PI; fitted-rate summary rows 35/41 | Incomplete per-day observations without verified animal-column IDs; reported D30 N=22/17 and D180 N=6/5 | Preserve per-day measurements/missingness with counts labelled observations; no invented trajectories, animal-specific baseline or refitting. Keep rate summaries separate |
| MOESM11 F5f, A1 unit; A2:C2 Ctrl/IL18/IL1beta; rows 3:5 | Day-5 K14+ outgrowth distance in mm; three source records per condition; caption n=3 animals with three technical replicates per mouse | Describe all three groups, both treatment-minus-common-control mean contrasts and IL1beta-minus-IL18; no inferred nine records or matching |
| MOESM10 F4g; MOESM11 F5d/e/g, labels row 2, Mean/SE/N row 3, rate row 4; blocks A:C, D:F, G:I, J:L | Reported fitted rate summaries only; panels have distinct backgrounds/perturbations | Preserve each Mean/SE/N and its own panel; describe within-background differences and differences of those differences |

For F1g/F1e, proposed primary contrasts are PI minus Ctrl means in their measured
units, accompanied by medians, ranges and observed N. A prespecified one-observation
leave-out range removes each source observation once from either group (only when both
remaining groups are nonempty); it measures sample leverage, not a confidence
interval. Missing cells remain missing. Before a contract, verify F1e denominators,
F1b units/time labels and each source block against the saved cells; never fill
these from caption shorthand or invent an N. The coordinator's additional bounded
read found F1e tongue counts 5/4, 4/4 and 6/6 despite caption n=4; preserve both
records. The caption's animal-unit statement is positive design evidence, while
this unresolved reporting discrepancy limits inference and supplies no sample IDs.
F1g's 23/14 counts are compatible with its n>=14 caption. Do not edit sources or
frozen results to reconcile the labels.

For fitted rates, retain the coordinator-read group-specific Ns: F4g 6/5/2/3;
F5d 3/3/3/3; F5e 3/2/6/5; F5g 3/3/4/4, in workbook block order. F4g compares
Ctrl/PI in the reference background and Aim2KO; F5d in WT and Il18KO; F5e in
WT and Il1r1KO. F5g is
Ctrl/Aim2OE by Control-Ig/Anti-IL1R1, not inflammatory history by genotype:
compare the OE effect within each blockade background, then their difference.
Do not compare only with untreated Ctrl, which mixes baseline blockade and OE
effects. F5e caption n=4 differs from source Ns 3/2/6/5; F5g caption n=3
differs from 3/3/4/4. Preserve those discrepancies and actual source Ns.
Preserve reported SE as source SE; infer no raw fitted rates, distribution,
confidence interval, cross-panel independence, pooling or meta-analysis.

Proposed figures: raw animal/observation dots and means in separate F1g/F1e panels;
reported fitted-rate means/SE in distinct source panels with explicit N and
within-background contrasts. F1b sparse daily values retain a separate table and
qualified observation-count display. No figure links animals across assays/days.
The coordinator's targeted F5f read found exactly three source values per
condition, compatible with the caption's three-animal summaries, but averaging,
animal IDs and cross-condition matching are undocumented. Include only those
three source records per group; no raw technical values or N=9 may be fabricated.
Any influence diagnostic deletes a source record, not an identified animal.
The two treatment-minus-control contrasts share Ctrl; their direct comparison is
IL1beta minus IL18. Keep this day-5 endpoint separate from F1g day-10, with no
cross-panel pooling, IL18-equivalence claim or population test.

Functional perturbation evidence concerns repair responses, not proof of chromatin
memory establishment/maintenance. Loss of a history advantage is not loss of every
repair component. Ex vivo outgrowth, tongue length, labeling percentage, wound
area and a fitted decay parameter remain different measured endpoints.

## Before execution and delivery

After S3 preservation: implement and test the approved S5M specification, freeze
its code/contract, and return the actual result for review before S5F. For later
S5F, qualify only the exact remaining source fields, implement edge-case tests and
freeze its separate code/contract. Both stages require
preflight and execute through the runner. Independently verify all joins, source
cells, denominators, contrasts, covariance identity and leverage calculations;
inspect the actual figures. Preserve mixed/negative outcomes and source limits.
Keep current README/context/status/PROGRESS aligned. S6 follows these reviewed
results; no new RQ, external publication or scientific acceptance is implied.
