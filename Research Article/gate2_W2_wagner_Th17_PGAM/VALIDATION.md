# Validation: what was actually checked in this pass

4 October 2026. This records checks that were performed, their outcome and their
limits. A passing check here is evidence about provenance and structure, never
about biology.

## Source documents

- The two owner-supplied PDFs were parsed and read end to end: 16 main pages
  including STAR Methods and the key resources table, and 9 supplemental pages.
  Both files were hashed; the values are in [Source manifest](SOURCE_MANIFEST.md).
- The supplement was searched for the Excel tables: it contains Figure S1–S5
  legends and Table S2 only. Tables S1 and S3–S6 are **absent**, which is recorded
  as a hold rather than worked around.
- Two documentation problems were found by reading, not by computation: the
  pathogenicity-score **sign** is stated one way in Results and the opposite way
  in STAR Methods, and the human cohort is described as five-versus-five while
  the deposit resolves to six donors per group. Both are recorded in
  [Evidence map](EVIDENCE_MAP.md#what-is-not-available) and
  [Datasets](DATASETS.md#human-reuse-cohort). Neither is resolved here.

## Deposits

- All three accessions were retrieved directly from GEO, not from the paper's
  text. Nine files were downloaded, byte-counted and SHA-256 hashed into
  `raw_data/wagner_pgam_w2_20261004/acquisition_v1.json`.
- An earlier download of the series records used a GEO view that returns the
  whole platform's sample list; those files were discarded and re-fetched with
  `targ=self` and `targ=gsm`, which is why the recorded sizes are kilobytes
  rather than tens of megabytes. Only the re-fetched copies are in the manifest.
- Two large inputs were deliberately **not** downloaded, because no stage is
  eligible to use them yet: the single-cell count matrices and
  `GSE138266_RAW.tar`.

<a id="dry-run-outside-the-runner"></a>
## Dry run outside the governed runner

[scripts/qualify_sources_v1.py](scripts/qualify_sources_v1.py) was executed once
against the recorded inputs **outside** `research_gate.py`, to check that it runs
and that its outputs are well formed. That execution produced no receipt and is
**not** the Wp-R0 result; the numbers quoted in [Datasets](DATASETS.md) come from
it and will be superseded by the governed run's `results.json`.

What the dry run confirmed:

- Every manifest entry re-hashed to its recorded value, and the script's
  stop-on-mismatch path was exercised by construction (it verifies before doing
  anything else).
- Single cell: 8 sample records, animal labels `Mo1` and `Mo2`, four condition
  combinations, **0** per-sample supplementary matrices, 19,203 barcodes of which
  19,203 are unique, 8 aggregation suffixes, 31,053 features all of type
  `Gene Expression`.
- Bulk: 79 sample records, 79 matrix columns, **0** unmatched joins in either
  direction, 20,465 gene rows, 16 design cells with five libraries each except
  Th17p/DMSO/Div.1 with four, and **no** animal field anywhere in the records.
- Human: 22 sample records resolving to 12 donor codes, 6 per disease group, 10
  with both CSF and blood. Donor identity comes from sample titles because the
  deposit declares no donor field; the script records that provenance in the
  output table rather than presenting it as a declared field.

## Not done

- **Nothing has run under the governed runner.** No receipt, no registered
  output, no results report. The contract
  [config/source_qualification_v1.json](config/source_qualification_v1.json) is
  frozen but its execution and registration are the next step in the
  [plan](ANALYSIS_TRIAL_PLAN.md#before-the-first-substantive-run).
- No expression value from any deposit has been read, so no statement in this
  package is a numerical reproduction of any published panel.
- Compass was not installed or run. Its current repository requires a Gurobi
  licence, which this environment does not have; `token.gurobi.com` was
  allowlisted but no academic credential is configured.
- No figure exists in this package, and no hypothesis schematic is registered.
  The [literature context](LITERATURE_CONTEXT.md#hypothesis-schematic) carries an
  explicit pending-figure note instead.
- The literature pass is bounded: six PubMed queries, title-and-abstract level,
  with citing-article chains for the two most recent sources not inspected. The
  log, including what was not inspected, is in
  [Literature context](LITERATURE_CONTEXT.md#next-literature-check). No novelty
  is claimed from it.
- No claim-register row, no A identifier, no owner retain/reject decision and no
  scientific acceptance was created.

## Interpretation limit for the package as a whole

Everything here is reanalysis planning for a paper whose results were read first.
The reproduction stages are reconstructions with declared substitutions, not
exact reproductions, because the frozen gene lists and the analysed cell set are
not deposited. The mouse deposits cannot reach population inference at all — one
animal per single-cell condition cell, no animal field in the bulk series — and
the human deposit is the only donor-level unit available.
