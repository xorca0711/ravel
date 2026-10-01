# A23 external analysis: results and hypothesis review

**1 October 2026.** P2 descriptive analysis and P3 source-assay audit executed.
P4 timing and P5 epithelial restoration/function remain untested. This is an
exploratory case comparison and source reproduction, not independent causal
validation. [Figures](../../FIGURES.md) | [Run receipt](../../metadata/external_pilot_v2/run_record.json) |
[Contracts](../../config/external_pilot_v2.json).

## Main finding

The external PAM case does not show the coordinated KRT8/SPRR1A/CLU increase
seen after Slc34a2 targeting in Nb3. Lower SLC34A2 RNA is present, but it is
insufficient to identify that state response. Source biochemical measurements
motivate a conditional compensation hypothesis; they do not establish a linked
phosphate-to-state mechanism or epithelial recovery.

## P2: human case context

Three filtered matrices contain 13,346 cells and 32,738 features each. PAM CD45−
and CD45+ are fractions of one reported subject; D071 is one adult control.
Disease, donor, age and sampling are inseparable. Absolute cell yields are
coverage measures, not tissue composition or independent replication.

| Primary QC | PAM CD45− | PAM CD45+ | Control D071 |
|---|---:|---:|---:|
| Filtered cells | 5,090 | 4,603 | 3,653 |
| QC cells | 4,971 | 4,533 | 3,528 |
| Epithelial candidates | 2,315 | 33 | 221 |
| AT2 candidates | 2,298 | 29 | 185 |
| AT2 candidates with published AT2 label | 1,821 | 20 | 134 |

The comparison uses PAM CD45− and D071. CD45+ remains a separate coverage/context
fraction. Candidate annotation uses features disjoint from every reported
readout. These are marker-defined candidates with co-lineage exclusions,
not a validated whole-lung cell taxonomy. Ambient RNA and residual doublets
remain limitations; no decontamination model or integration was used.

PECAM1 and its current stable ID are absent from the feature list. The initial
attempt stopped before outcome calculation. The documented pre-scoring v2
amendment conservatively excludes cells detecting either VWF or EMCN. It does
not treat the missing feature as zero or claim an equivalent endothelial panel.
NCBI's official orthologue service verifies the three selected human markers;
Ensembl requests failed and are retained in the acquisition record.

| Readout in AT2 candidates | PAM mean | Control mean | Difference | Detected PAM / control |
|---|---:|---:|---:|---|
| KRT8 | 1.1264 | 1.2481 | −0.1216 | 1,895/2,298; 160/185 |
| SPRR1A | 0.00144 | 0 | +0.00144 | 4/2,298; 0/185 |
| CLU | 0.5266 | 0.5815 | −0.0549 | 1,114/2,298; 91/185 |
| SLC34A2 | 0.5174 | 2.1859 | −1.6686 | 1,266/2,298; 165/185 |

Means are natural-log(1 + UMI per 10,000) averaged over candidate cells;
differences are PAM minus control, not log-fold changes of biological replicates.
There are no population p-values or biological confidence intervals.

KRT8 and CLU remain lower under stricter QC and in the published-AT2 intersection.
SPRR1A is undetected in both published-AT2 intersections. The three-marker signal
therefore does not transfer coherently to this case under these definitions.
This does not refute an acute perturbation hypothesis: genotype, transport,
time, disease stage, dissociation and sampling are not matched to Nb3.

Identity interpretation is especially sensitive to cell selection: SFTPA1,
SFTPA2 and LAMP3 differences change sign in the published-AT2 intersection.
Do not convert the primary positive surfactant-marker contrasts into preserved
identity. Target RNA decrease also does not measure transport activity.

The published annotation contains 14,210 cells. Exact library-plus-barcode
matching finds 12,363 in the deposited filtered matrices; 1,847 published cells
are absent and 983 filtered cells lack published labels. All missing published
cells are in the PAM fractions. No barcodes were silently recovered from raw
matrices, and this pilot is not an exact reproduction of the article's cell set.
[Coverage](../../tables/external_pilot_v2/annotation_coverage.tsv) and
[crosswalk](../../tables/external_pilot_v2/published_annotation_crosswalk.tsv)
retain that distinction.

## Source-completeness sensitivity

Because omission was differential by case status, a separately recorded,
post-pilot [contract](../../config/published_cell_audit_v1.json) tested the complete
published cell set using raw matrices already present in the downloaded archive.
All 14,210 published cells match exactly. Published AT2 counts are 2,742 in
PAM CD45−, 49 in PAM CD45+, and 211 in D071. The fractions remain separate.

In all published AT2 cells from PAM CD45− versus D071, mean log-normalized
KRT8 differs by −0.0434, CLU by −0.0476 and SLC34A2 by −2.0625. SPRR1A is
undetected in both. The fixed primary and strict QC sensitivities retain those
directions. Thus the missing filtered PAM cells do not explain the lack of a
coherent three-marker increase under published AT2 annotation. This is a
post-pilot sensitivity of the same case, not a second validation cohort.

Published annotation has not been independently revalidated and can select on
identity-related RNA. This check resolves barcode completeness, not annotation
bias, ambient RNA, disease-stage confounding or biological replication.
[Tables](../../tables/published_cell_audit_v1/marker_differences.tsv) |
[Source-completeness receipt](../../metadata/published_cell_audit_v1/run_record.json) |
[Supplementary figure](../../FIGURES.md#supplementary-figure-1-complete-published-cell-set).

## P3: source endpoints and linkage

The [Uehara et al. source workbook](https://www.nature.com/articles/s41467-023-36810-8)
was retrieved and hashed. Fifty-three sheets were inventoried; eight biochemical
or mineral-burden sheets were re-extracted with exact cell coordinates. This
is the same study as GSE199329, not another independent study.

Within Npt2b−/− groups, the LPD/RD ratio of means is 0.393 for BALF phosphate,
0.600 for serum phosphate, 2.009 for isolated-AT2 Slc20a1 RNA and 1.977 for
Slc20a2 RNA. They have different units, sampling and n (6, 6, 3 and 3 per group).
BALF is lavage fluid, not intracellular phosphate or undiluted lining fluid.
RNA abundance is not transporter flux. The corresponding wild-type BALF
phosphate ratio is 1.600; a uniform decrease across genotypes is unsupported.

All four source-paired LPD mineral-burden observations decrease between D0 and
D56 (24.2–68.3%). This is mineral clearance, not restoration of epithelial state.
Figure 6's mineral series and biochemical series differ in age, duration and
LPD formulation; the HPD mineral cohort is younger than the LPD/RD cohorts.
They cannot be pooled into one dose-response or temporal epithelial experiment.

BALF osteoprotegerin means under LPD and RD in Npt2b−/− groups are similar
(ratio 1.013), whereas HPD is higher. The LPD/RD mean and median summaries differ
because of skew. This source endpoint does not support a simple mean decrease
from RD to LPD or by itself explain the epithelial state comparison.

No explicit shared animal identifiers are supplied for these biochemical sheets.
Rows identify source positions, not cross-assay subjects. Pairing for mineral
burden follows the source's paired design and row layout; subject IDs remain
unknown. The retrieved annotations link to human RNA barcodes but not to the
mouse biochemical subjects. The inspected endpoints do not provide linked
transport-flux, transition-state, time and restoration measurements.
[Endpoint ledger](../../tables/external_pilot_v2/endpoint_linkage.tsv).

## Strict review of the A23 hypothesis

| Prediction | Decision from this batch |
|---|---|
| H1: disruption changes epithelial state | Original screen remains motivating; coherent marker transfer is not observed in the external case. Population causal effect untested |
| H2: relevant homeostasis contributes beyond secondary injury | New biochemical context supports a plausible compensation branch; mediation and direct epithelial flux untested |
| H3: state response precedes identity loss | Not tested. Neither simultaneous human RNA nor a mineral-burden time series establishes epithelial ordering |
| H4: restoration reverses state and permits mature recovery | Not tested. Diet-associated mineral clearance is not transporter restoration, state reversal or mature AT1 function |

**Conditional candidate: compensation of phosphate handling, related to P3/H2.**
Compensatory phosphate handling may buffer the epithelial response to SLC34A2
loss. The compensatory-transporter RNA response in the source biochemical data,
together with the lack of a coherent transition-marker pattern in this PAM
case, makes this a plausible discriminator rather than an accepted explanation.
The two observations are unlinked and cannot show that compensation caused the
case pattern. The rival is secondary mineral/inflammatory injury, or selection
and disease-stage differences, accounting for apparent state differences.

A discriminating dataset must link verified SLC34A2/transport status, measured
compensatory flux, relevant phosphate compartment and an independent epithelial
state endpoint in replicated biological units. It should test whether state
response differs with compensation at comparable perturbation and injury,
without adjusting away downstream variables as if that proved mediation.
A precise unchanged state response despite valid differences in compensation
would weaken this branch. Slc20a1/2 RNA alone cannot pass the gate.

**Rejected in this review:** low SLC34A2 alone defines the transition state;
positive primary surfactant markers prove retained identity; diet rescues AT1
function; or the biochemical assays and human RNA constitute a measured causal
chain. No new RQ ID, hypothesis acceptance or claim-grade promotion follows.

## Remaining work

1. Published-cell recovery is complete. Independent cell annotation and
   ambient/doublet assessment remain relevant before interpreting finer states;
   both filtered and complete published-cell sensitivities remain archived.
2. Seek a replicated source linking transport/compensation and epithelial state,
   with real times and unit IDs. Additional unrelated atlas scoring cannot test
   H2/H3. P4 remains blocked on this data requirement.
3. P5 needs verified restoration plus linked state and mature output. The current
   dietary/mineral dataset cannot supply that conclusion.

Commands and dependencies are in [REPRODUCE.md](REPRODUCE.md). Tables and figures
retain immutable hashes; v1's failed feature gate and F3's superseded layout are
preserved. The main README remains general.
