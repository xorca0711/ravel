# Osmr RNA: completed finite-library description

8 November 2026. **Sx22-P01; exposed shared-source reanalysis.** Osmr RNA is
lower under 22-B3 than WT in these deposited whole-colon libraries. WT is above
PBS on all specified scales/omissions; B3 is slightly below PBS in full data,
but its CPM and FPKM omission ranges cross zero. Thus this acute source does
not show a stable B3-associated Osmr induction. The result narrows the motivation
from this dataset for a retained-Osmr explanation; it neither tests OSM response
nor contradicts the published epithelial IL-22/STAT3/OSMR circuit in other settings.

The sole preselected target uniquely maps to ENSMUSG00000022146 and passes the
unchanged existing threshold (CPM >=1 in all six libraries; >=2 required).
All six libraries are retained. Original animal/preparation identities remain
unverified. Full-data means of log2(CPM+1) are contrasted below; these are not
population log-fold changes. Ranges are the six observed omissions, not CIs.

| Scale | WT-PBS: full [omission range] | B3-PBS | B3-WT |
|---|---:|---:|---:|
| CPM | +0.200 [+0.063, +0.337] | -0.183 [-0.389, +0.023] | -0.383 [-0.589, -0.177] |
| TMM | +0.162 [+0.026, +0.309] | -0.174 [-0.349, -0.018] | -0.336 [-0.516, -0.180] |
| Deposited FPKM | +0.143 [+0.044, +0.242] | -0.121 [-0.258, +0.016] | -0.264 [-0.401, -0.127] |

The direct B3-WT direction persists in all 21 scale/view cases. The smaller
B3-PBS difference is sensitive to the individual library and normalization.
Whole-colon composition, general attenuation and unmeasured preparation effects
remain unresolved. No epithelial localization, receptor protein, OSM sensitivity,
protection, chronic risk or persistence endpoint was measured. Il6st was not
needed for this fixed question; no replacement target or receptor screen was run.

[Figure gallery](FIGURES.md) · [Methods and prospective rationale](METHODS.md) ·
[Exact ranges](../../../analysis/research/runs/sx22_osmr_v1/ranges.csv) ·
[All library values](../../../analysis/research/runs/sx22_osmr_v1/library_values.csv) ·
[All contrasts](../../../analysis/research/runs/sx22_osmr_v1/contrasts.csv).
The [previous IFN/barrier description](../reassessment_v1/RESULTS.md) remains
unchanged: selected IFN attenuation and broader response reduction coexist.
It is reused context, not a new independent comparator or replication.

## Provenance and verification

The [contract](contract_v1.json), methods and scripts were committed at
`d5530f7` before the [runner execution](../../../analysis/research/runs/sx22_osmr_v1/receipt.json).
All prior output hashes were checked; source counts/FPKM were copied only after
matching archived SHA-256 values. No historical analysis was replayed.
The receipt verified successfully. The [independent verifier](verify_v1.py)
uses raw matrices and scalar arithmetic without production imports: unique join,
108 library-scale-view values, 63 contrasts and nine plotted ranges passed at
1e-12 tolerance. TMM factors are reused verified outputs, not a new independent
implementation. PNG inspection confirmed readable labels, all six dots, full
values and signed omission ranges without clipping. No frozen output was edited.

Completed: mapping, committed freeze, description, bounded sensitivity, arithmetic
and figure review. Held: population inference needs animal/preparation and
allocation keys; epithelial OSM-response claims need matched receptor protein and
an OSM challenge response, with verified units. Not needed: generic scoring,
Il6st, a new atlas, raw-read or structural reprocessing. Parent review and human
scientific acceptance are distinct; no acceptance or claim promotion is recorded.
