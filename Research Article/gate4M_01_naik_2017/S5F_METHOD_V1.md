# S5F v1: separate reconstruction of published functional-source endpoints

19 November 2026. Owner `Nk17-P01`. S5M v2 was coordinator-reviewed without
numerical/figure revision and preserved at `7051b45`. The coordinator authorized
this exact S5F scope, including the previously qualified F4h and F5a/b/c additions.
The 18–19 November usage-limit interruption did not change that authorization;
it is separate from the older content restriction. No earlier molecular analysis
is rerun. Original source values, fitted summaries and paper findings are exposed.

## Purpose and permitted inference

Naik et al. (2017) links inflammatory history, epithelial molecular states and
enhanced wound repair. The current [S5M result](S5M_RESULTS_V2.md) finds larger
acute than recovered/recall RNA–TSS-proxy association, with shared-baseline
coupling and mixed anchor patterns. It does not measure repair, protein or activity.
This step asks what the separately supplied **functional and molecular-source
measurements** actually show in their own groups and units. Concordant, weak,
opposite and perturbation-dependent finite contrasts are all informative; no
combined memory score, new mechanism or chromatin-to-repair mediation is fitted.

The paper captions provide positive evidence that n denotes biologically
independent animals. F1g also labels source rows as biological replicates.
Nevertheless, exact animal IDs, cross-panel overlap, some technical aggregation
and several source/caption N discrepancies remain unresolved. Those limitations
do not erase the qualified finite comparisons. No cross-condition pairing,
biological-unit count from repeated cells, population test, equivalence claim,
confidence interval, source p-value reproduction or scientific acceptance is made.
Genetic/pharmacological repair contrasts do not identify chromatin-memory
establishment/maintenance; loss of a history advantage is not loss of all repair.

## Exact source and group map

[S5F_SOURCE_MAP_V1.json](S5F_SOURCE_MAP_V1.json) is the complete frozen specification:
35 endpoint records, 83 groups (57 source-record groups and 26 reported-summary
groups), all exact cells including intended blank slots, source labels/header
guards, endpoint units, time context, source N, caption N and all 38 contrast
coefficient vectors. Three original MOESM7/10/11 XLSX files and the existing
owner-supplied final-PDF text are input-hashed. The 19 November bounded check
read only assigned sheets/cells and Figure 1/4/5 captions; it made no broad source
retry or operational protocol extraction. Relevant caption text locators are
338–366, 895–923 and 1153–1181 in the saved `final_pdf_fitz_text.txt`.

| Panel | Source locator and endpoint | Source N and caption qualification |
|---|---|---|
| F1b daily area | Ctrl B3:W13; D30 PI B19:R29; days from column A; mm² | 11 days, sparse records; daily cell counts are not animal N; caption D30 n=17 is context only |
| F1b fitted rate | A35:F35 (D30), A41:F41 (D180), Mean/SE/N blocks | 22/17 versus caption 17; 6/5 versus caption 5 |
| F1e tongue | Days 1/3/5, rows 3:5; Ctrl B:G, PI H:M; micrometers | 5/4, 4/4, 6/6 versus caption n=4 |
| F1e EdU | Days 1/3/5, rows 11:13; Ctrl B:E, PI F:I; percentages | 4/4, 3/2, 2/2; caption n≥2. Caption denominator: K14+ EdU+ / K17+ cells; raw numerator/denominator counts are absent |
| F1g outgrowth | A3:A25/B3:B16; mm; day 10 | 23/14, compatible with caption n≥14; rows labelled biological replicates |
| F4g fitted rate | A4:L4 | Reference Ctrl/PI and Aim2KO Ctrl/PI: 6/5/2/3, caption n≥2; do not relabel reference as verified WT |
| F4h expression | A3:B4, RFP−/RFP+; normalized Aim2 arbitrary units | 2/2; all RFP− values 1 are normalization references, not measured zero variance |
| F4h fitted rate | A9:F9, Ctrl/Aim2OE | 3/2 versus caption n=2; separate from the expression records and F5g blockade |
| F5a qPCR/activity | A3:B5 Casp1; A9:A14/B9:B13 CASP1 activity in U/g total protein | qPCR 3/3 and reference controls 1; activity 6/5 versus caption n=3; caption specifies 12 h after wounding |
| F5b activity/rate | A3:D4 activity; A12:L12 Mean/SE/N | Activity 2 each, caption 2; rate 5/5/4/6 versus caption 5; retain source `Sd. Error` label, with no conversion to SD |
| F5c qPCR | Il18 B3:D3/E3:G3; Il1b B4:C4/E4:F4 | 3/3 and 2/2, matching endpoint-specific caption Ns; all Ctrl values 1 are references |
| F5c protein | IL18 B8:E8/F8:I8; IL1beta B9:D9/F9:H9; pg/g total protein | 4/4 and 3/3, matching endpoint-specific caption Ns; separate from qPCR/activity |
| F5d/F5e fitted rates | Each A4:L4, WT and KO Ctrl/PI | Il18KO 3/3/3/3, caption 3; Il1r1KO 3/2/6/5 versus caption 4 |
| F5f outgrowth | A3:C5 Ctrl/IL18/IL1beta; mm; day 5 | Three source records each. Caption n=3 animals, three technical replicates/mouse; averaging/IDs/matching undocumented, never N=9 |
| F5g fitted rates | A4:L4: Ctrl+Ig, Ctrl+anti, Aim2OE+Ig, Aim2OE+anti | 3/3/4/4 versus caption 3; OE by IL1R1 blockade, not history by genotype |

Daily area Ctrl Ns are 5,13,11,22,8,19,3,15,4,4,10 and PI Ns are
5,13,11,16,8,14,5,11,5,5,4 for days 0–10. Blank cells remain blank; true zeros
remain observations. No source-column label is promoted to an animal ID.
Fitted-rate workbooks state `Rate Constant` without an explicit unit, but the
supplied final-PDF axes explicitly give **day^-1** (Fig1 text lines 185/329;
Fig4 803/894; Fig5 1059/1150–1152). The coordinator qualified these axes and the
technical session verified their exact text before freeze. Use day^-1 with this
PDF-axis provenance while retaining the workbook omission. These reported
one-phase wound-area decay summaries are not instantaneous migration speed.
Exact original fit constraints are not
fully specified, so no trajectories or individual fitted rates are reconstructed.

## Statistics and all declared contrasts

For each source-record group, save every numeric/blank cell and its coordinate;
report N, arithmetic mean, median, source minimum/maximum and sample SD when
n>1. SD describes the finite source values, not uncertainty of an animal effect.
For the four explicitly designated all-1 qPCR/expression reference groups, retain
the source constants and reference mean but set empirical SD to NA with an
explicit normalization-reference reason. No reference dot cloud suggests measured
zero biological variance. Do not infer pairing from workbook rows.

For each reported-summary group, retain its exact Mean/SE/N and source label.
Median, source range and SD are NA. Do not infer individual rates, convert SE to
SD, combine SEs across groups or construct a contrast interval. Source/caption
N discrepancies remain explicit in tables and plots; do not force a common N.

The map declares **20 record-based contrasts** and **18 reported-rate contrasts**.
All are linear combinations of group means using the fixed coefficients; record
contrasts also retain the same combination of group medians as a descriptive
sensitivity. No ratios across unlike units, significance selection or pooling.

- F1e: PI−Ctrl at each of three days for tongue length and EdU percentage;
  F1g: PI−Ctrl at day 10. F1b daily area is observation/mean/missingness display
  only, with no new longitudinal contrast or fit.
- F4h expression: RFP+ minus its fixed RFP− normalization reference;
  F5a qPCR/activity and all four F5c endpoints: PI−Ctrl in their own units.
- F5f day-5 outgrowth: IL18−Ctrl, IL1beta−Ctrl and direct IL1beta−IL18;
  the first two share a control and are not independent comparisons.
- F5b activity: PI−Ctrl without and with YVAD, then the latter minus the former.
- F1b D30/D180 fitted summaries: PI−Ctrl separately; F4h fitted rate: Aim2OE−Ctrl.
- F4g/F5d/F5e rates: PI−Ctrl within each reference/KO background, then KO effect
  minus reference effect. F5b rate uses the same history-by-inhibition structure.
- F5g: Aim2OE−Ctrl **within control-Ig and within anti-IL1R1**, then anti-minus-Ig
  difference of OE effects. Equality of OE+anti to Ctrl+Ig alone does not establish
  complete removal of OE effect because blockade also changes the control.

For each record-based contrast, remove each nonreference source record once from
one contributing group, only if that group remains nonempty. Retain every
deletion's coordinate, recomputed mean contrast and change from the full contrast,
plus the minimum/maximum of these values. Normalization reference constants are
fixed and not deleted. A singleton supplies no eligible deletion from that group;
if none are eligible, the range is NA with a reason. This is source-record
influence, not an animal jackknife, confidence interval or robustness threshold.
Summary-only rate data have no deletion diagnostics.

## Displays and independent verification

Five PNG/PDF figures retain the complete assigned scope: F1e tongue/EdU panels;
separate day-10/day-5 outgrowth panels; four normalized-expression, two activity
and two protein panels; all eight reported-rate panels; and sparse daily
F1b wound-area observations. Use deterministic horizontal offsets, all observations,
group means and labelled source Ns. Rate bars are reported source SE only.
No lines join animals, days or molecular layers; no population interval, p-value,
significance star, equivalence notation or composite score is displayed.

The main reader uses read-only openpyxl and never saves a source workbook. Reject
unexpected labels, formulas, nonfinite/non-numeric outcome cells, invalid Ns or
reference constants. Independent verification uses a separate standard-library
ZIP/XML XLSX reader and Decimal arithmetic, without importing the main reader,
statistics or contrast helpers. Reconstruct every requested cell including blanks,
all header guards, group summaries, N comparisons, coefficients, medians and
individual deletion contrasts. Compare finite numbers at scaled `1e-10` tolerance;
labels, cell identities, booleans, Ns, NA reasons and group memberships are exact.
This verifies source/arithmetic, not independent biological replication.

Artificial tests must distinguish a blank from a true zero, unpaired unequal
groups, singleton deletion limits, fixed normalization references, summary-only
SE/N, and the F5g baseline-blockade counterexample. Wrong Ns/headers/formulas and
tampered source/contrast outputs must fail. Freeze tested code, this map/method
and the exposed contract before calculation. Preserve failures and use a new
version for scientific corrections; no overwrite of frozen artifacts.

Return actual verified S5F outputs and visually reviewed figures for coordinator
review. S6 and any justified extension follow that review. No global RQ/claim
promotion, external publication or human scientific decision is created here.

## Pre-freeze artificial verification

The final artificial fixture has four endpoints, ten groups, six contrasts,
38 independently parsed source cells and seven deletion rows. Four tests passed,
including all 700 ZIP/XML/Decimal checks (maximum scaled error `8.16485e-17`),
formula rejection by both readers, reference/blank/N checks and output tamper
rejection. The blockade example has OE+anti equal to Ctrl+Ig while the OE effect
within anti remains positive; the implementation retains that distinction.
The initial formula-rejection test exposed an unclosed workbook handle on the
error path. The bounded sheet stream now completes before semantic checks, with
workbook closing in `finally`; the final rerun passed. No real S5F calculation
was performed during these artificial tests.
