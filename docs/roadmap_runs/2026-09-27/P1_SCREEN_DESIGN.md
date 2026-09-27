# P1 — Screen design recovered far enough to set its inference ceiling

**Status: completed.** This package reconstructs the library crosswalk and recovers the previously unread supplementary methods. It supports a stricter interpretation of replication and identifies an additional culture-ligand rival; no new expression model was fitted.

## Recovered design

The [library crosswalk](P1_library_crosswalk.tsv) links 886 libraries to GEO samples, deposited repeats, position, imaging and guide-pool hashes. All 203 targets are retained. Thirty tdTomato libraries lack guide-design rows and remain explicit unknowns. Only four targets cross plates. Each of AREG, EGFR, ERBB2, ERBB3, ERBB4 and ITGB6 has four library records but one position and one guide pool. [Calculated checks](P1_crosswalk_checks.json); [target table](P1_target_identifiability.tsv).

The primary article's appendix was retrieved from the public [Europe PMC supplementary archive](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13367804/supplementaryFiles); PDF `pnas.2606113123.sapp.pdf`, pages 2–3 and 11. Retrieval hashes, locators and visual checks are in the [source record](P1_source_recovery.json).

| Newly recovered fact | Consequence |
|---|---|
| Four replicate Transwells receive aliquots of a common cell–Matrigel mixture | Do not count the four repeat labels as four independently prepared cultures. |
| Same-patient passage-3 fibroblasts are specified | This provides a protocol-level restriction, not a sample-level donor/lot crosswalk. |
| Matrigel and MTEC/Plus are specified; Fig. S5 documents recombinant EGF in regular medium | The AREG null has an additional unremoved ligand rival. Neither recipient AREG RNA nor this fact quantifies compensation. |
| Day-7/day-14 imaging, day-14 RNA and SAM processing are described | A10 RNA remains concurrent with the later area endpoint. Physical calibration and the deposited statistic's transformation remain unresolved. |
| Coverage is derived from bounding-box unions | The earlier area/count/coverage arithmetic is not itself proof of inconsistent area units. |

## Decision

A2 remains a within-screen perturbation-associated measurement, with shared-mixture wells and target–position/guide confounding. Independent biological uncertainty cannot be recovered by treating wells as mice or using a more elaborate model. A10's concurrent associations and held-out plate results remain valid as their stated calculations; new-preparation prediction and functional repair are not established. A15 still lacks its selective activation-route design.

No further screen-fitting cycle is opened. Stronger evidence requires a target/guide/position design with independent preparations and measured ligand/activation conditions. This is a completed design audit with a named ceiling, not a claim that all missing fields are unknowable.

The source discovery supersedes older *current* statements that the four groups' replication is wholly unknown or that nothing is known about medium composition. Frozen reports remain historical. The unresolved crosswalk and quantitative medium details must still be stated.
