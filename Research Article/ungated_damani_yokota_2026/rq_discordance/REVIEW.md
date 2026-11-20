# DY1-P02 coordinating review

30 October 2026. The owner authorized external source qualification and execution
of every eligible E1-E6 extension through the existing analysis chat. Starting
reviewed revision: `a6559e4`. Integration base last fetched:
`78320a186b6f52426e7c7c5349a2f26492b718b7`. Technical review is separate from human
scientific acceptance; every receipt retains `scientific_acceptance: not_assessed`.

## Prospective review and corrections

- Published biological-replicate wording supports group-local meaning. Repeated
  labels do not recover across-condition preparation reuse or cross-assay pairing.
  Preserve timing (24h/25h), batch, overlap and annotation-version unknowns.
- E2 numerical code, contract, parameters and five targeted tests were reviewed
  before freeze. All eligible deposited ATAC regions receive effects; annotation
  restricts only cross-assay joins. This corrected the initial annotated-only
  implementation before any production result was exposed.
- E2 uses separate compositional logCPM contrasts, two fixed offsets and explicit
  mappings. Welch/full-pairing envelopes are conditional sensitivity views, not
  recovered identities or unconditional population CIs. The nearest-TSS distance
  can refer to a different gene from the source Ensembl assignment. Repeated genes
  make mapped-row proportions dependent descriptions, not independent trials.
- E3's five fixed independent-normal scenarios and analytic verifier were reviewed
  before freeze. Detection, sign, coverage and interval width are distinct. No
  biological calibration or effect margin was supplied.
- E6 literature/source review separated muscle injury, repeated-stimulation RNA
  and assay-specific early/late coverage. RNA-only source-average arithmetic was
  reviewed before freeze with three targeted tests. It does not reconstruct
  individual responses, variance, effective n or a matched chromatin trajectory.

## Completed result and integrity review

| Run | Frozen revision | Frozen/current entries; inputs; outputs checked | Numerical review |
|---|---|---|---|
| E1 reference source | `7361a174c8b174eadb931919b716e40a45e84a84` | 3; 9; 7 | 259 structural checks; every sample-column join and 71,942 annotation-coordinate matches |
| E2 reference benchmark | `3c1bc105b8f3904fe398d129205e1798977f10e6` | 5; 6; 11 | 1,608 scalar/category checks, eligibility/mapping tables and figure reviewed |
| E3 synthetic diagnostic | `48292daaa8482f4de701db4469350e428853ce91` | 5; 1; 6 | All 75 independent analytic checks and saved figure reviewed |
| E6 temporal source | `3c1bc105b8f3904fe398d129205e1798977f10e6` | 4; 11; 8 | 34 source-table checks; 278 occurrences deduplicated to 217 GSM records without conflicting shared records |
| E6 source-average RNA | `218f063d6dcd7d9deffbbd99246ef968db6644ac` | 4; 4; 5 | All 187,360 scalar ratio checks, four partitions, mixed results and saved figure reviewed |

Total: **21 frozen/current contract-code entries, 31 input hashes and 37 output
hashes** independently verified. These are entry counts, not necessarily unique
files. Contract/code bytes match both receipt hashes and frozen Git blobs. Each
receipt records successful execution. Internal arithmetic verification reuses the
same data/specification; it is not biological replication. The reviewer inspected
all three figures and the displayed result/qualification tables.

| Run | Receipt SHA-256 |
|---|---|
| E1 | `d3f222ef7f94c4997f552eabd317d2249e35edd7137ed234347b94ecec203294` |
| E2 | `42725cff6cdc824dde71839dee1c64c4102b18f367b946bbe8e692229c42f16f` |
| E3 | `3f3fc4b4e72a0b48645596dcaf7e5fcc186a0bad3345ae7bfe515952e6344552` |
| E6 metadata | `5e6a742cd1fb2e2c36b757fee1c391574671b6a132951e8554bc629b193496e9` |
| E6 RNA | `ef923d292eaaffae2b9f65de6914d29844225583bb6c8676755f2f0b3df3bd78` |

## Interpretation and hold review

The [README](README.md) retains mixed directions and exact denominators. E2 full
mapped rows show about 56% matching signs versus about 63% in the nearest-TSS
subset. These are neither a population agreement test nor NAM replication. The
raw source flag contingency is also retained: every annotated region has
`filtered=True`; 598 further True and 71,871 False regions lack annotation. A flag
name or the earlier numerical difference does not establish retained/dropped
semantics.

E3 equal truths yield substantial detection-label mismatch; opposite truths can
yield a similar mismatch fraction. Significance labels alone cannot identify
biological agreement. E6 source-average responses remain mixed, and their
magnitude depends on offset. Neither result identifies a NAM mechanism.

E4/E5 remain held on their original count/processing/unit/assignment/state and
regulatory-resource prerequisites. E6's biological precision and matched temporal
claims remain held for absent replicate values and appropriate time/assay/source
linkage. External descriptions do not supply NAM occupancy, activity or linked
ARG1 mediation. See [source-method limits](SOURCE_METHODS_2026-10-30.md),
[temporal inputs](TEMPORAL_INPUTS_2026-10-30.md) and
[primary temporal coverage](E6_SOURCE_REVIEW.md).

## Integration validation

Stable handoff `ebedcde8e2d7de1906f41b30dade3a4f178f93ec` is integrated. Source
validation passed 19 targeted tests, 161 repository tests (one skip), required
evidence verifiers and 11,618 repository checks. The integrated README/review
state passed 11,647 repository checks and the research gate against freshly
fetched unchanged main. A trailing-blank-line formatting finding was corrected.
All 32 canonical questions/guides and infrastructure match main; no protected
or RQ path changed in this pass. Frozen outputs, prior failures and negative
findings remain intact. No biological analysis was rerun for README integration.
