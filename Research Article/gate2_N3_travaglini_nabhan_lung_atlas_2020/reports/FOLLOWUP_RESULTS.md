# Nb4: sensitivity branches and external pilot

**Executed 2 October 2026.** Choices were source-informed and frozen in
[followup_v1.json](../config/followup_v1.json) before the additional estimates.
The sequence follows Nb1, England and Nb3 precedents: units, sensitivity,
then separate-cohort transfer. No population-level biological p-values were used.

## Internal branches

| Branch | Result | Consequence |
|---|---|---|
| Floors 10/20/30/50; leave-one-donor-out | Source distal P2 enters the fibroblast contrast only at floor 10 (15 adventitial cells). C3 stays negative in all three 10x donors; CXCL2 and IL32 become positive in P2. | Keep the fixed primary floor; no uniform immune-panel direction. |
| Matched donor/region cross-assay | C3 stays negative. CCL2 is positive in two primary 10x donors but negative in their SS2 samples. | Assays are not independent donor replications. |
| Exact 1,000-UMI detection expectation | C3 remains negative (−0.608 to −0.507), MYRF AT1–AT2 positive (+0.035 to +0.115), TBX5 pericyte–alveolar fibroblast positive (+0.181 to +0.267). CCL2 is mixed. | Selected directions survive this depth diagnostic. |
| Alternative comparators | MYRF is higher in AT1 than AT2, Club and other epithelium across three distal donors per assay. TBX5 is higher in pericytes than alveolar fibroblasts/other stroma across three donors; vascular-muscle comparisons have two. | Reference context, not regulator function. |

Depth adjustment is the exact hypergeometric probability of detecting at least
one molecule after sampling without replacement. Only 10x cells with at least
1,000 assigned molecules are eligible. It is not SS2 read-to-UMI conversion.
[Floors](../runs/followup_v1/floor_and_donor_sensitivity.tsv),
[assay pairs](../runs/followup_v1/matched_assay_directions.tsv),
[depth effects](../runs/followup_v1/depth_standardized_detection.tsv),
[comparators](../runs/followup_v1/alternative_comparators.tsv).

## Independent atlas

The fibroblast subset of
[Madissoon et al., Nature Genetics 2023](https://www.nature.com/articles/s41588-022-01243-4)
contains 20,515 cells/nuclei from ten donor labels in a distinct organ-donor
study. Ten labels do not imply ten eligible pairs. Normal single cells from
explicit left-lobe sites were matched on donor, anatomy, assay and preparation
protocol. Mixed sites, airways, other subtypes and strata below 20 cells per arm
were excluded. Eligible stratum effects are averaged equally within donor;
cells and nuclei stay separate. [Frozen pilot](../config/external_pilot_v1.json).

Four primary single-cell donors and two nuclear donors remain. Floor 10 adds
no donors. Related markers inform the author subtype labels, so independent
recruitment does not mean independent annotation validation.

| Alveolar minus adventitial | External cell mean | Donor range | Directions |
|---|---:|---|---|
| C3 | −1.86 | −2.77 to −0.27 | 4/4 negative |
| CXCL2 | −2.47 | −2.96 to −1.98 | 4/4 negative |
| IL32 | −0.48 | −0.91 to −0.09 | 4/4 negative |
| CCL2 | −0.32 | −0.87 to +0.23 | 3 negative, 1 positive |
| CXCL12 | −0.27 | −0.87 to +0.18 | 3 negative, 1 positive |

GPC3 is positive in all four donors; PI16/SFRP2 negative in all four; SPINT2
positive in three and zero in one. These checks are annotation-exposed.
[Donor results](../runs/external_pilot_v1/donor_effects.tsv) and
[matched strata](../runs/external_pilot_v1/stratum_effects.tsv).

Nuclear C3 stays negative in both donors (−3.37, −3.28), but CXCL2 reverses to
positive (+1.40, +3.51), and IL32 is mixed. Donor/protocol differences prevent
attributing the discrepancy to nuclear capture alone. They also prevent a
claim of uniform transfer. [All summaries](../runs/external_pilot_v1/summary.tsv).

## Decision

Retain C3 as a subtype-associated RNA observation in this bounded comparison.
Secreted complement, pathway activation, recruitment and injury responses
remain unmeasured. Ambient RNA, handling, label dependence and subtype
composition remain rivals. The [genome-wide analysis](EXTENDED_VISUAL_ANALYSIS.md)
does not support generalizing C3 to the whole complement set.
[RQ derivation](RQ_DERIVATION.md).
