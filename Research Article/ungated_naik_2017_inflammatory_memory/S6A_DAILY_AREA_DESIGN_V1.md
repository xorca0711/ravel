# S6A prospective design: all supplied daily wound-area comparisons

19 November 2026. Owner `Nk17-P01`. **Coordinator-approved for implementation
and governed execution; a committed frozen contract is still required.** The completed
[S5F result](S5F_RESULTS_V1.md) and [S6 assessment](S6_DECISION_V1.md) motivate
this exposed descriptive extension. No new daily-area mean or contrast has been
calculated. Existing paper curves, S5F summaries and group/day occupancy are
exposed; this specification does not make the work confirmatory.

## Purpose, unit and primary comparison

The paper reports inflammatory-history and Aim2-dependent repair effects. S5F
finds a positive reported OE contrast within anti-IL1R1 despite OE+anti equalling
Ctrl+Ig. The unresolved finite-source question is whether the corresponding
area comparisons persist, attenuate, reverse or depend on starting area and
changing coverage across the complete published day grid. All six assigned
panels are included so the interpretation is not chosen from F5g or one day.

The endpoint is remaining wound area in mm². A positive treatment/history-minus-
control area contrast means larger remaining area, the opposite direction to
the paper's positive fitted decay-rate advantage. The computational unit is a
numeric spreadsheet area record within one panel/group/day. Captions identify
animals as biological units, but exact identities, column trajectories and
aggregation/matching are unqualified. Days and panels are not independent animals.
The leading validity threats are starting-area offsets, changing observed
coverage, unknown record/animal relationships and source-label/N discrepancies.

## Exact source scope

Use original public source files saved in `raw_data/naik2017_s6_preparation/`:

| File | Bytes | SHA-256 |
|---|---:|---|
| `41586_2017_BFnature24271_MOESM16_ESM.xlsx` | 51,968 | `58b52d4b5ee1f097a21a684d20d3d01393d20005f5d862889f11147a44ae1bec` |
| `41586_2017_BFnature24271_MOESM17_ESM.xlsx` | 57,515 | `196ca23b612207b032a497022fdd8292aa58e5b206d005bcfa27aa6d3fba2fe4` |

Published links: [MOESM16](https://static-content.springer.com/esm/art%3A10.1038%2Fnature24271/MediaObjects/41586_2017_BFnature24271_MOESM16_ESM.xlsx),
[MOESM17](https://static-content.springer.com/esm/art%3A10.1038%2Fnature24271/MediaObjects/41586_2017_BFnature24271_MOESM17_ESM.xlsx).
The coordinator acquired them on 19 November around 03:39 UTC; local copied
bytes match. Saved publisher link titles misnumber the extended figures as
10/11, while worksheet names and final-PDF captions identify EDF5/6. Preserve
that provenance discrepancy rather than relabel the actual sheets.

Use exact A1 unit/header text (`Wound Area (mm^2)`, including the trailing
space in EDF6f/g), A2 `Day`, group-start labels in row 2, and every day-cell
value. The source map must bind each expected numeric/blank slot and retain the
full listed column ranges, including entirely blank columns. No sorted numeric
compaction, inferred animal ID or cross-condition pairing is permitted.

| Sheet / related main panel | Exact rows and days | Group ranges in source order | Numeric source counts by day |
|---|---|---|---|
| EDF5e / F4g | Rows 3:13; days 0:10 | WT Ctrl B:G; WT PI H:L; Aim2KO Ctrl M:N; Aim2KO PI O:Q | 6/5/2/3 on days 0–7; 6/5/1/3 on days 8–9; 3/3/1/3 on day 10 |
| EDF5f / F4h | Rows 3:12; days 0:9 | Ctrl B:D; Aim2OE E:G | 3/2 every day; E:G has three slots despite two numeric values |
| EDF6d / F5b | Rows 3:11; days 0:8 | Ctrl B:F; PI G:K; Ctrl+YVAD L:O; PI+YVAD P:V | 5/5/4/6 every day; P:V has seven slots despite six numeric values |
| EDF6e / F5d | Rows 3:12; days 0:9 | WT Ctrl B:D; WT PI E:G; Il18 KO Ctrl H:J; Il18 KO PI K:M | 3/3/3/3 every day; row 13 has no day and is outside the observed day grid |
| EDF6f / F5e | Rows 3:13; days 0:10 | WT Ctrl B:D; WT PI E:F; Il1r1 KO Ctrl G:L; Il1r1 KO PI M:Q | 3/2/6/5 on days 0–5; 3/2/6/4 on days 6–9; 0/0/4/3 on day 10 |
| EDF6g / F5g | Rows 3:13; days 0:10 | Ctrl + Control Ig B:D; Ctrl + Anti-IL1R1 E:H; Aim2OE + Control Ig I:K; Aim2OE + Anti-IL1R1 L:O | 3/4/3/4 every day |

This fixes 62 panel/day endpoints and 228 group/day records. Verify all counts
and day labels before interpreting any comparison. Blank slots remain missing;
true zero areas remain measured zeros. Do not fill unobserved days or carry
forward values. Missing a group's entire day makes its mean/median/SD NA.
Preserve the absent-day versus observed-day/all-blank distinction.

## Caption and reported-summary Ns remain separate

The supplied final PDF's EDF5 caption is at saved text lines 2644–2662, EDF6
at 2755–2771. They specify biologically independent animals and also contain
panel-specific Ns that must not replace the worksheet record counts:

| Sheet | Extended-data caption N | Related main caption N | Main rate-summary Ns, source order |
|---|---:|---:|---|
| EDF5e | 3 | ≥2 | 6/5/2/3 |
| EDF5f | 4 | 2 | 3/2 |
| EDF6d | 3 | 5 | 5/5/4/6 |
| EDF6e | 3 | 3 | 3/3/3/3 |
| EDF6f | 4 | 4 | 3/2/6/5 |
| EDF6g | 4 | 3 | 3/3/4/4 |

Report differences to both caption sources and the reported-summary Ns without
resolving them by assumption. EDF5e explicitly labels its area reference groups
WT; retain that label in this new source while preserving S5F's separate
qualification of the main-sheet reference labels. Shared paper provenance does
not establish which area records entered each fitted summary.

## Statistics and all prespecified contrasts

For every group/day, retain all numeric and blank cells with coordinates, number
of slots, observed N, missing N, mean, median, minimum, maximum and sample SD.
SD is finite-source dispersion; n=1 has SD NA, and n=0 has all summaries NA.
These area records have no fixed normalization-reference groups. A genuinely
all-zero measured group may have SD zero. No SE or population interval is added.

Primary estimands are linear contrasts of **unadjusted group means at each day**:

- EDF5e, EDF6e and EDF6f: PI−Ctrl within WT and within KO, then KO history
  effect minus WT history effect.
- EDF6d: PI−Ctrl without YVAD and with YVAD, then with-minus-without YVAD
  history-effect difference.
- EDF5f: Aim2OE−Ctrl.
- EDF6g: Aim2OE−Ctrl within control-Ig and within anti-IL1R1, then anti-minus-Ig
  difference of OE effects. Never substitute OE+anti versus Ctrl+Ig for the
  within-anti comparison.

Apply these same fixed vectors to group medians as a full-grid descriptive
sensitivity to the small groups' value distribution. Neither statistic is chosen
as a winner. This gives 166 prespecified contrast/day rows, including rows that
must remain NA when a contributing group lacks records. Do not count these as
166 independent experiments or select a day from its effect size.

Secondary, prespecified day-0 decomposition uses the same available group means:
for group g, save `M_g(d)`, `M_g(0)` and `M_g(d) − M_g(0)`. For every contrast
vector c, save the raw contrast `C(d) = sum_g c_g M_g(d)`, its baseline
`C(0)`, and `A(d) = C(d) − C(0)`. For an effect-difference vector this same
formula retains both within-condition components and their day-0 components.
Also retain the analogous median contrast and baseline subtraction.

These are differences of observed group summaries, **not within-animal changes,
ANCOVA-adjusted effects or corrected kinetics**. Each later day reuses the same
estimated baseline, so adjusted contrasts share baseline error. Counts can
change between day 0 and day d; apparent changes can reflect coverage, not
healing of a fixed cohort. Day-0 adjusted values are exactly zero by construction
and provide no evidence of biological equivalence. If any required current or
baseline group is missing, retain NA and the exact missing-group reason.

In particular, EDF6f day 10 has no WT data: its WT history contrast and
KO-minus-WT contrast, raw and baseline-adjusted, must be NA. The KO contrast
may still be described. Do not drop the entire endpoint or fill WT with zero.
No ratio to baseline, percentage closure, interpolated day, closure time, fitted
k, individual trajectory, p-value, equivalence margin or independence claim is
introduced. No panel/day pooling or significance-based selection is permitted.

## Displays, verification and preservation

Predeclare four PNG/PDF figures: all source area records with group means for
the six panels; every raw mean/median contrast; every day-0-adjusted contrast
with its raw/baseline components available; and group/day observed-N/missingness
coverage. Use consistent contrast colours and units across the complete day
grids. Any connected mean/contrast lines describe group summaries, never animals.
Missing contrasts remain visibly missing; the absence of a day is distinct from
a labelled day with zero records. Show all EDF6g comparisons and do not crop to
one favorable day. Source SD, if displayed, is labelled dispersion, not a CI.

Save source-cell and observation tables, all group summaries, all contrast and
baseline-component tables, count/caption/source metadata, runtime and independent
verification. The exact output list, code/config hashes and immutable evidence
inputs will be bound in the post-review contract. Preserve the existing S5F and
S3/S4/S5M artifacts; this stage writes to a new run directory only.

The independent verifier should use stdlib ZIP/XML with Decimal arithmetic,
separate from the main read-only openpyxl implementation. It must reconstruct
every selected source cell and blank, day/group membership, Ns, summary, fixed
coefficient vector, raw/median contrast and baseline component. Check the
identity `A(d) = C(d) − C(0)` and exact NA reasons, including EDF6f day 10.
Numerical scaled tolerance 1e-10 is computational only; labels, occupancy,
identities and missingness are exact. Input/output hashes and runner receipt
are separate preservation checks, not scientific acceptance.

Artificial tests must cover unequal/missing daily groups, a real zero versus
blank, singleton SD, constant measured zeros, missing day-0, source-order
group labels, changing coverage, a nonzero starting-area offset, and the
OE+anti=Ctrl+Ig counterexample with a nonzero within-anti OE contrast. Test
rejection of unexpected headers/day maps, formulas, nonfinite values, count
drift and tampered contrasts/components. No artificial test may inspect the real
area effects before freeze. Review actual figures after the governed run.

Stop on source identity/header/hash/unit disagreement or incorrect day/group
mapping. An expected all-blank group/day is retained as missing rather than
failing all panels. An unexpected occupancy mismatch is investigated before
execution; do not silently relax the declared count map. Preserve unfavorable,
mixed and unsupported outcomes. Coordinator design review is complete; implement/test,
register, preflight and freeze a separate exposed contract before numerical work.
The [literature context](LITERATURE_CONTEXT.md#s6-targeted-literature-refresh--19-november-2026)
and S6 assessment must be evidence references in that contract.
