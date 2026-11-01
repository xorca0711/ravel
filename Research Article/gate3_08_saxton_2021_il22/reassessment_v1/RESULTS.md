# Finite-library program description: results and dispositions

1 November 2026. **Sx22-P01; exposed shared-source reanalysis.** The published
IFN-versus-tissue-protection panel distinction is visible in this deposit and
persists through the specified sensitivities. Broader IFN memberships show
substantially smaller median contrasts and residuals. A broad amplitude reduction
also accompanies the panel pattern. These observations do not establish causal
STAT selectivity, preserved function, equivalence or population generalizability.

[Question and literature framing](README.md) · [Literature context](LITERATURE_CONTEXT.md) ·
[Exact methods](METHODS.md) · [Illustrated results](FIGURES.md) · [Validation](VALIDATION.md).
Primary repository evidence is the immutable
[run](../../../analysis/research/runs/sx22_program_description_v1/receipt.json)
under [contract v2](config/description_contract_v2.json), frozen at
`404d23673194abbb388668a2aa74e2ff09399579` before execution. This is an adapted
description of the published WT IL-22/engineered 22-B3 six-hour colon RNA data,
not an exact replay of the authors' undocumented processing.

## Coverage and primary comparison

All 35,275 deposited stable-ID rows and six libraries are retained. The fixed
CPM threshold admits 14,483 rows; 228 rows match the tested membership union,
217 of which are eligible. Excluding that union leaves 14,266 eligible background
rows. All 31 unique author target symbols map uniquely; Cxcl1 alone falls below
the threshold and remains visible but excluded from the Figure 6E target median.

External IFN-alpha has 94 source members, 92 unique exact mappings and 89 eligible
members. IFN-gamma has 188, 184 and 175 respectively. No tested symbol is ambiguous.
Missing exact tokens are Tent5a/Wars1 (alpha) and Marchf1/Rigi/Tmt1b/Wars1 (gamma);
none is replaced by a guessed alias or numerical zero. The two sets overlap in
73 source symbols, 72 unique mapped rows and **70 eligible rows**. Their matching
primary medians are not independent confirmation. See
[mapping](../../../analysis/research/runs/sx22_program_description_v1/member_mapping.csv),
[overlap](../../../analysis/research/runs/sx22_program_description_v1/membership_overlap.csv)
and [inventory](../../../analysis/research/runs/sx22_program_description_v1/gene_inventory.csv).

Primary values below are medians of eligible gene-wise differences of group
means of **log2(CPM+1)**. They are not fitted animal-level log-fold changes.
The last column is median(y-beta*x), with x=WT-PBS and y=B3-PBS. A median of
differences need not equal a difference of medians in the preceding columns.
Exact unrounded values and every case are in
[panel_set_summaries.csv](../../../analysis/research/runs/sx22_program_description_v1/panel_set_summaries.csv).

| Fixed membership | Eligible/source | WT-PBS | B3-PBS | B3-WT | Amplitude residual |
|---|---:|---:|---:|---:|---:|
| 6B tissue protection | 6/6 | +2.246 | +1.897 | -0.459 | +0.278 |
| 6B DNA-damage response | 7/7 | +1.910 | +1.331 | -0.374 | +0.318 |
| 6B anti-inflammatory | 4/4 | +1.956 | +1.535 | -0.772 | -0.157 |
| 6D interferon response | 7/7 | +1.490 | +0.101 | -1.345 | -0.760 |
| 6D TNF/Trail | 5/5 | +1.391 | +0.454 | -0.952 | -0.531 |
| 6D Il1rn | 1/1 | -0.930 | -0.198 | +0.732 | +0.358 |
| 6C qPCR targets (RNA) | 3/3 | +6.592 | +4.229 | -2.166 | +0.286 |
| 6E qPCR targets (RNA) | 3/4 | +1.183 | +0.213 | -0.952 | -0.484 |
| Hallmark IFN-alpha | 89/94 | +0.321 | +0.077 | -0.163 | -0.081 |
| Hallmark IFN-gamma | 175/188 | +0.199 | +0.050 | -0.163 | -0.081 |

The six-member tissue-protection panel decreases in the direct B3-WT contrast
(-0.459); its positive amplitude residual (+0.278) means only that its pattern
lies above the chosen global reference. It does not mean no loss of expression
or preserved biological protection. The seven-member selected IFN panel has a
more negative direct contrast (-1.345) and residual (-0.760). The broader IFN
sets have much smaller corresponding medians (-0.163 and -0.081 for each under
primary CPM), narrowing how far the conspicuous selected-panel pattern extends.
The source's anti-inflammatory panel also has a negative residual, so category
names should not be treated as a clean mechanistic partition.

## Overall amplitude and bounded sensitivities

The background through-origin coefficient is **0.598013** for primary CPM,
0.605400 for TMM and 0.599988 for deposited FPKM. This is a descriptive reference
to noisy axes with shared PBS, not a fraction of response explained, a causal
parameter or a test that excludes broad attenuation. CPM omission coefficients
range from 0.450747 to 0.745279; the full-data result remains primary.
[All 21 fits](../../../analysis/research/runs/sx22_program_description_v1/amplitude_fits.csv)
retain the same gene universe and background.

Across the full-data and all six omission cases on each of CPM, TMM and FPKM,
the tissue-protection panel's direct median remains negative and its residual
positive. The selected IFN panel and both broad IFN sets retain negative direct
medians and residuals. The table gives full-data values followed by observed
six-omission minima/maxima; these are **not confidence intervals**. No extra gene
set, filter, pseudocount or library exclusion was sought after viewing outcomes.

| Membership | Scale | Direct B3-WT: full [omission min, max] | Residual: full [omission min, max] |
|---|---|---:|---:|
| 6B tissue protection | CPM | -0.459 [-0.565, -0.229] | +0.278 [+0.227, +0.764] |
| 6B tissue protection | TMM | -0.407 [-0.521, -0.233] | +0.282 [+0.225, +0.792] |
| 6B tissue protection | FPKM | -0.447 [-0.603, -0.220] | +0.304 [+0.220, +0.725] |
| 6D interferon | CPM | -1.345 [-1.476, -1.214] | -0.760 [-0.843, -0.616] |
| 6D interferon | TMM | -1.296 [-1.401, -1.217] | -0.737 [-0.853, -0.602] |
| 6D interferon | FPKM | -1.147 [-1.306, -0.965] | -0.666 [-0.778, -0.466] |
| Hallmark IFN-alpha | CPM | -0.163 [-0.296, -0.131] | -0.081 [-0.136, -0.023] |
| Hallmark IFN-alpha | TMM | -0.111 [-0.218, -0.111] | -0.049 [-0.084, -0.019] |
| Hallmark IFN-alpha | FPKM | -0.157 [-0.275, -0.124] | -0.071 [-0.129, -0.017] |
| Hallmark IFN-gamma | CPM | -0.163 [-0.298, -0.083] | -0.081 [-0.149, -0.018] |
| Hallmark IFN-gamma | TMM | -0.111 [-0.219, -0.087] | -0.048 [-0.090, -0.014] |
| Hallmark IFN-gamma | FPKM | -0.138 [-0.261, -0.078] | -0.071 [-0.136, -0.020] |

The Figure 6C subset (Reg3b/Reg3g/Muc1, RNA values only) is an unfavorable
sensitivity result that remains in the figures and tables. Its CPM direct median
is -2.166, with omission range -3.973 to -0.626; its residual is +0.286 but ranges
from -1.734 to +2.995. TMM and FPKM residual ranges also cross zero. This selected
three-gene subset is therefore less stable under library omission than the
six-member tissue-protection median. It neither reconstructs qPCR nor warrants
post hoc sample removal. All 120 ranges are retained in
[sensitivity_ranges.csv](../../../analysis/research/runs/sx22_program_description_v1/sensitivity_ranges.csv).

## Interpretation limits

The prediction receives bounded descriptive support for the fixed panel
distinction in these six records, together with smaller effects for the external
memberships and clear individual-library sensitivity in the three-target subset.
The broader response reduction and selected-panel difference can coexist; this
analysis does not determine their causal relationship. External membership is
another selection rule applied to the same data, not biological replication.
Whole-colon composition, allocation/batches and measurement noise remain
unresolved. No functional, protein-signaling or time-persistence endpoint was
measured here. Source-reported biological replicates remain recorded, while
individual mouse/preparation identity remains unverified. No human scientific
retain/reject decision or claim-grade promotion is inferred from completion.

## Final job dispositions

| Job | Disposition | Evidence or exact unresolved requirement |
|---|---|---|
| Q0 / R0-R1 reuse | Completed source/runtime eligibility review | [Eligibility](TECHNICAL_ELIGIBILITY.md); prior R1/X1/X2 audits reused without re-execution |
| Q1 / R2a | Completed finite-library description | All source rows, six per-library CPM/log values and three contrasts in the new run; no inference tests |
| Q2 / R3a | Completed exact-membership adapted description | Frozen Figure 6B/D and separately labelled 6C/E target lists; coverage and Cxcl1 exclusion explicit; not author preprocessing replay |
| Q3 / R3b | Completed for two qualified external IFN memberships only | Versioned public mouse GMT, exact mapping, coverage, medians and overlap; no additional STAT3 or protective set |
| Q4 / R3c | Completed all specified components | Three scales × seven views; 36 TMM factors; 21 amplitude fits; 210 membership cases; 4,788 tested-gene cases; all ranges and figures |
| Q5 / R2b | Held: biological-unit/design evidence | Verified independent animal/preparation units and allocation/nesting keys needed before population p-values, FDR or uncertainty; no gate weakened |
| Q6 / exact Figure 6 replay | Held: author-method evidence | Original gene universe, transformation, aggregation/filtering/zero handling and correlation choices remain unrecovered |
| Q7 / R4-R5 signaling/function | Held: raw data and panel identity | Raw measurements, replicate/nesting keys and unresolved Figure 5/7 identities remain unqualified; RNA output cannot substitute |
| Q8 / E1-E2 recipient/persistence | Held beyond completed E1a/X3 scope | Pooled Choi observations, sparse capture and missing animal-resolved exposure/cessation/later-function joins; no unrelated atlas expansion |
| Q9 / D1 | Technical package complete; parent integration remains | Numerical verification, figures, unfavorable results and this disposition table delivered; originating review and parent-owned navigation/PROGRESS integration remain separate |

No current service content refusal occurred during this run. The original two
generic prompt-level failures remain historical evidence with unidentified
triggering jobs; completion here does not assert unrestricted service clearance.
The local pre-execution registration failure and temp-file sandbox issue were
resolved transparently as described in [validation](VALIDATION.md).
