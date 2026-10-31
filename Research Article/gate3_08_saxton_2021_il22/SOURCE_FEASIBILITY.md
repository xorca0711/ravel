# E1/E2 source-only feasibility closeout

31 October 2026. Owner: Sx22-P01. Purpose: inventory identifiers, time/cessation
labels and endpoint linkage available in already-qualified sources. Comparison:
source fields against the historical E1/E2 documentation requirements, not a
comparison of biological responses. Biological units are animals/donors and nested
preparations; libraries/cells are not substituted. Main validity threat: joining
independent assays or pooled preparations by a common condition name. No new RQ,
receptor score, treatment model, functional estimate or experiment package is made.

## E1: selected existing injury/recovery source

Choi 2020 is the bounded first candidate because the repository already qualifies
its epithelial injury/recovery libraries and withdrawal precedent. This is a
scope choice, not a biological ranking or evidence that lung and colon responses
are interchangeable. No alternative atlas was downloaded or scored.

| Existing source | Available keys and labels | Missing or unqualified bridge | Source-only disposition |
|---|---|---|---|
| Choi GSE145031 | Six GSM/title mappings in D0: PBS, Day14 and Day28, each Tomato-positive/negative; the later reviewed pilot uses the three positive libraries | One library per condition, each positive library pooling two mice; no animal-resolved cell map. Time since injury is not verified cytokine cessation. No matched IL-22 input or linked functional response in these matrices | Library-level source context is available; animal-level recipient-state comparison and IL-22 functional response are not qualified |
| Choi GSE144468, same existing package | Two GSM/title mappings, Control_Organoids and Il1b_Organoids | No within-group library replication in D0. These deposited expression groups are not a withdrawal series linked to the paper's Fig. 7 recovery assay | Context only; cannot manufacture a cessation/recovery join by assigning cells or conditions to separate figures |
| Saxton GSE160217 | Six libraries, treatment labels and six-hour annotation, all reviewed in R1 | Bulk colon lacks resolved epithelial states and separate mouse/batch keys; no later functional endpoint joined to these RNA samples | Retain original RNA source as metadata-qualified; it does not itself instantiate E1 |

Exact repository evidence: [D0 deposited design](../gate1_02_choi_2020/trials/d0_data_reality_check/d0_deposited_design.csv),
[D0 library/replication audit](../gate1_02_choi_2020/trials/d0_data_reality_check/d0_summary.md),
and the newer [12 October pilot review](../gate1_02_choi_2020/weft_pilot_v1/SCIENTIFIC_REVIEW.md),
which retains the pooled-unit limit and incomplete state recovery. Published source:
[Choi et al. 2020](https://doi.org/10.1016/j.stem.2020.06.020), Fig. 1 and separate
Fig. 7 withdrawal evidence. These are reused reviews, not new source replication.
Receptor-gene coverage and per-state response scoring were **not assessed** in
this recovery; they are not reported as absent or silently inferred from D0's
checks of other marker panels.

E1 source assessment is complete. Numerical work remains unexecuted and outside
recovery scope. A future source intake would need an explicit cell/library-to-
animal/preparation map, state provenance, condition/time annotations and the
endpoint relevant to its claim. Recovering an ID cannot create an unmeasured
IL-22 response or functional outcome.

## E2: cessation and functional-endpoint linkage

| Source / reviewed locator | Sample/time/cessation evidence | Linked functional endpoint and limits | Status |
|---|---|---|---|
| Saxton Figs. 5–7; R1 metadata | Acute tissue/source labels and assay timing; no post-cessation series in the reviewed RNA records | Fig. 7 has metabolic viability, crypt and serum endpoints, but no qualified join from the six RNA libraries to later recovery units | Acute endpoints documented; persistence/recovery linkage not qualified |
| Cineus, Luo et al. 2025, main text citing Supplementary Fig. 5e; Fig. 4f–h | Text describes IL-22 removal followed by Osmr measurement; Fig. 4 addresses receptor-transcript regulation | The reviewed passage does not join withdrawal observations to a later functional-recovery endpoint. Individual-unit keys and precise cessation/acquisition labels in supporting files were not inspected | Published withdrawal premise confirmed; raw linkage **not assessed**, not demonstrated absent |
| Bachmann et al. 2013, PubMed abstract | Epithelial preconditioning/context precedent | Abstract alone does not qualify individual sample keys, cessation labels or linked recovery | Abstract-read context only; full text/data **not assessed** |
| A14 Choi outcome audit, O28 / closeout M10 | Published withdrawal-associated recovery; existing audit distinguishes removal from measured cessation | No inspected export links compartment exposure/reception history, viability and traced mature output | Preserve exact existing linkage hold; do not relabel acute RNA as persistent memory |
| A19 human-organoid source and closeout M11 | Donor-coded qPCR; eight bulk libraries in two source blocks with incomplete donor linkage; present/absent input labels | Marker/preparation data do not jointly establish receptor-specific cessation, mature descendants and retained reserve | Preserve current source limitations; no A19 analysis rerun |
| Existing Rochelle qualification, GSE306194/GSE306714 | Nine donor/stage libraries (UC/P0/P2) and three scaffold GSM records | No documented alias/preparation/time bridge to later function. Culture stages are not elapsed cessation times; donor names alone do not establish cross-assay pairing | Informative existing metadata, not an eligible linked withdrawal/recovery cohort |

Repository authorities: [A14/A19 outcome-linkage review](../../docs/research_dossiers/followup_2026-10-03/OUTCOMES.md),
[current closeout M10/M11](../../docs/research_dossiers/source_mapping_closeout_2026-10-03/README.md),
[A19 current result/limitations](../../RQ_Specified/A19_fzd_response_reversibility/RESULTS.md),
[Rochelle source qualification](../../docs/research_dossiers/continuation_2026-10-03/SOURCE_LINKAGE.md).
Current dossiers and question identities were located through the registry and
remain unchanged. The existing [A22 source-map limits](../../docs/research_dossiers/followup_2026-10-03/METADATA.md)
are also retained; separate well/plate labels do not supply animal/preparation
replication or protein output.

## Primary-source access record and completion boundary

No new literature search was conducted. The [31 October reading review](../../docs/research_reviews/2026-10-31-saxton-il22/README.md)
owns the earlier actual search queries and read-versus-unread coverage. This pass
used its documented sources plus direct opens on 31 October 2026:

- [Cineus, Luo et al., published PMC text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12133592/),
  DOI 10.1038/s41590-025-02149-z: inspected the removal passage immediately before
  the Fig. 4 section, Fig. 4 caption and Data availability/Associated Data.
  Source-data and supplement links are advertised, including Supplementary
  Methods/Figs. 1–7. Their contents, raw keys and figure-to-GEO mapping were not
  newly audited. No claim that raw data are unavailable follows from that limit.
- [Bachmann et al., PubMed PMID 23153456](https://pubmed.ncbi.nlm.nih.gov/23153456/),
  DOI 10.1016/j.bcp.2012.11.004: abstract-level access retained; no full-text or
  supplement read claimed. No broad search or novelty clearance was attempted.

E2 source assessment is complete at this coverage. Empirical persistence/recovery
work remains unexecuted; no inspected source is promoted to a linked functional
comparison. A future intake must distinguish absent fields in inspected exports
from uninspected supporting material, and record actual unit, exposure/cessation,
acquisition and endpoint joins. This is a data-qualification boundary, not a
bench protocol or permission to resume blocked execution. Closed Yadav/DY1 work,
canonical hypotheses, scientific acceptance and claim grades remain untouched.
