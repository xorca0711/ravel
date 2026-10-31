# Independent review of the saved Sx22 R1 metadata/QC run

31 October 2026. Review purpose: determine whether the saved metadata/QC evidence
agrees with its declared files, without repeating the biological analysis sequence.
Owner: Sx22-P01. Comparison: source bytes and source-derived technical quantities
versus the frozen outputs. The observational items are library records and gene
rows; the intended biological unit remains the source-reported colon sample,
whose separate animal identity is unknown. Main validity threat: confusing file,
library or BioSample identity with animal independence. No effect estimand or
significance test belongs to this review.

## Authorities and preservation

- [Frozen v2 contract](config/r1_contract_v2.json),
  [original receipt](../../analysis/research/runs/sx22_r1_v2/receipt.json),
  [summary](../../analysis/research/runs/sx22_r1_v2/summary.json).
- [Original source audit](SOURCE_AUDIT.md), qualified by the
  [documentary correction](SOURCE_CORRECTION_2026-10-31.md).
- [v1 failure and v2 amendment](AMENDMENTS.md): the prior CRLF preflight/runner
  rejection is retained. No failed record was overwritten or rerun.

The v2 receipt reports successful execution at `ff09fab3fb37fd4bf915845e5cd59effaa386210`.
Its contract hash is `3cb8e486e1d2b9d41e393defb3fd9ba8c66f61a9fbf018a666f1d9b8e2aaf9ba`.
The review compared all eight saved run files in this checkout to both preserved
source checkouts. This includes receipt, stdout and stderr beyond the five
receipt-declared outputs. Every byte comparison passed. All declared code and
output hashes passed; input/code manifests and expected output names agree with
the contract. The contract and both code blobs at the recorded execution commit
also match their receipt hashes. `scientific_acceptance=not_assessed` and `verification=pending`
remain original receipt facts, not editable review statuses.

| Declared raw file | SHA-256, verified in both source caches and new copy |
|---|---|
| GSE160217_family.soft.gz | `dd5c728e3a8a4128d3c64674ff56b54a24ed3585e3bc9707f33245dbe6a0b273` |
| GSE160217_060120_22_readcount_genename.xls.gz | `26a63db90cbb1c65614205b05a1a957b37f0783b67df72ad4801b48c5bc0646d` |
| GSE160217_060120_22_fpkm_genename.xls.gz | `69dd439dc048fe6ff0e4d343d403e2fe277ea004beb4bc10b80c2f0daa7027f1` |

Only these three inputs were copied into ignored `raw_data/Sx22/`, after both
source hashes were verified. Exclusive creation refused overwriting different
existing files. The supplied PDF was read in the original cache, not copied.
Source checkout paths and exact command history are recorded in [VALIDATION](VALIDATION.md).

## Independent method and findings

A separate temporary Python 3.12 standard-library checker, without importing or
calling `r1_audit_v1.py`, performed the following checks. The checker SHA-256 was
`a3a78b1c5b508bf66d7bbd35f680d9a4f8fd751460bc22e35b2631971dabf55f`;
its session-local path is recorded in VALIDATION. It wrote no scientific outputs.

| Check | Independent method | Finding |
|---|---|---|
| File format and shape | Decompress gzip, parse tabs with DictReader, reject malformed/duplicate headers and missing fields | Both `.xls.gz` files are text, not Excel; 35,275 rows, six libraries, nine annotation columns |
| Annotation join | Compare every non-sample field at every row between tables | Identical geneID, Gene_name, Chrom, Strand, Start, End, GeneLength, Gene_type and Description values/order |
| Count/FPKM validity | Decimal finite/nonnegative/integral checks for counts; finite/nonnegative float checks for FPKM | All 211,650 entries in each matrix pass; six nonempty and distinct count vectors |
| Library summaries | Integer sums, nonzero counts, heap-based largest-ten fraction; compare every saved value | All six rows agree; fractions agree within absolute tolerance 1e-15 |
| Gene diagnostics | Independent ID/symbol counters and all-library zero flags; compare every gene_qc field | No duplicate Ensembl IDs; zero empty symbol rows; 52 repeated labels cover 122 rows; 12,935 all-zero rows |
| Sample joins | Streaming SOFT record parser; exact GSM/title/treatment/BioSample joins and cardinalities | Six one-to-one joins; two library records per treatment; no sample exclusions |
| Timing/source labels | Read deposited tissue/strain/treatment and treatment-protocol fields | Colon, C57BL/6 and six-hour treatment; timing is a source annotation, not a cessation measurement |

The deposited sample map is the frozen [samples.csv](../../analysis/research/runs/sx22_r1_v2/samples.csv).
GSM4869228/29 map to PBS_1/2, GSM4869230/31 to LH5_1/2 (WT IL-22), and
GSM4869232/33 to LH30_1/2 (22-B3), from GEO attributes rather than expression.
The six BioSample accessions also agree exactly with the source audit.

| Library | Total counts | Nonzero gene rows | Largest-ten count fraction |
|---|---:|---:|---:|
| PBS_1 | 19,329,695 | 19,498 | 0.0692959200856506 |
| PBS_2 | 19,744,956 | 19,001 | 0.08647530032480194 |
| LH5_1 | 20,740,041 | 19,298 | 0.055729060516322024 |
| LH5_2 | 22,081,904 | 19,365 | 0.057730891321690375 |
| LH30_1 | 17,428,528 | 19,062 | 0.056717928215165386 |
| LH30_2 | 19,022,869 | 19,281 | 0.06798627483583049 |

These transcribe the unchanged [library_qc.csv](../../analysis/research/runs/sx22_r1_v2/library_qc.csv).
They are technical library summaries, not group summaries or biological effects.

## Interpretation corrections

`duplicate_nonempty_symbols` counts **distinct nonempty symbol labels occurring
more than once**. It is neither the number of affected gene rows (122) nor the
number of extra rows beyond one per repeated label (70). No IDs were collapsed
or annotation release inferred. The recovery-scope wording about 52 duplicated
entries should be read with this clarification; its historical bytes are retained.

The frozen `samples.csv` value `paired=no` was supplied by the audit script, not
recovered from an animal crosswalk. It means no pairing was established or used.
Neither unpaired animals nor distinct mice can be certified from this metadata.
The supplied PDF p. 23/e9 reports two independent biological RNA replicates;
this source report remains distinct from independent verification of those units.
Mouse IDs, allocation, sex, batch and exact annotation release remain unqualified.
Technical qPCR triplicates and the FPKM representation add no biological units.

The receipt summary's conditional model eligibility is a historical data-QC
statement, not permission to resume R2/R3. Those stages remain on the
[platform-policy execution hold](COMPLETION_LEDGER.md).
