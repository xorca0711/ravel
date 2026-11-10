# Integrated execution validation — 8 November 2026

**Later validation:** the [10 November follow-up record](followup_20261110/VALIDATION.md)
covers the three additional stages, public human-cell data and organized gallery.
The original integration record below remains historical.

The [seven-stage ledger](STAGE_STATUS.md) records the completed authorized scope
and scientific holds. The cloud run is imported into the isolated desktop branch
`codex/navarro-aging-fit-20261108`; this is local integration, not publication or
integration into main. Current base: `471d0c2f8b3b5fef287aea5173325436901fceac`,
freshly fetched before delivery. Parent pre-import revision: `1785daf`.

## Transfer and provenance

- Cloud HEAD: `cdf71c0881748f4e7560b561c1f4044662774ada`; eight cloud commits
  retain the pre-execution metadata, amendment, review and descriptive freezes.
- Git bundle: 3,519,447 bytes; SHA-256
  `b633fae1b7bf3eaae32ae31d2f43c38c21188217f58843de9d6f03d3ba735077`.
  All 287 transport pieces and the reconstructed bundle were hash-verified.
  `git bundle verify` confirmed its prerequisite and branch head before import.
- All **nine successful Navarro receipts verify locally**: three earlier source/
  animal stages and six cloud stages. The failed first metadata execution remains
  failed in its byte-preserved archive; the successful archive receipt does not
  convert it into successful analysis.
- All **101 unique receipt-bound contracts, code/config files and outputs**
  match their recorded SHA-256 in both the working tree and staged Git blobs.
  [Portability correction](PORTABILITY.md) preserves the original executed
  source-contract bytes across Windows/Linux. No frozen result was edited.
- Registry integration preserves all **36 canonical questions and 41 article
  candidates**, existing contracts/receipts and the Peng work from current main.
  The four source JSONs imported to the cloud match the existing desktop evidence.

## Validation and review

Repository validation and the base-aware research gate passed after the full
cloud import. Eight package Python scripts parse successfully. The required
repository test suite already passed against this same integrated main base:
**167 tests, two skips**. No validator, test implementation or infrastructure
changed during cloud import, so that valid test run was reused.

The RNA execution independently checked **4,245 scalar values** using R/Python
calculations, retaining 11,920 cell denominators and 195,506 selected sparse
entries. The parent additionally checked **90 displayed table values/denominators**
against frozen summary rows. This corrected the WT5 Bst2 prose rounding from
1.8226 to 1.8225 (full value 1.82254995208773); the numerical output is unchanged.
All four frozen SVGs were rendered and inspected in the cloud.

Documentation whitespace checks pass. Raw `git diff --check` also reports
whitespace in immutable source/run files, including original CRLF bytes and R
session formatting; these files retain their receipt-matching bytes. No cleanup
was applied to frozen evidence. The 33 unrelated historical working-tree status
paths were preserved; they remain byte-identical to their pre-import revision.

The large RDS and isolated R runtime remain in the cloud, with exact acquisition
and restoration instructions in the [transfer guide](CLOUD_TRANSFER.md). Local
receipt verification uses retained output/code hashes; it does not imply that
the RDS was loaded again on this Windows machine. No optional biological object,
new method, scientific acceptance, push, PR, author contact or network-policy
change was introduced by this delivery.
