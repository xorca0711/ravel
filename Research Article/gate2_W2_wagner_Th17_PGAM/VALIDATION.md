# Validation: what was actually checked in this pass

**Current execution and interpretation — 7 October 2026:** see [corrections](CORRECTIONS_2026-10-07.md) and [the current README](README.md). Dated stage plans, intake states and derivation counts below remain historical. A28–A30 are now registered; the full portfolio is A0–A30.

4 October 2026. This records checks that were performed, their outcome and their
limits. A passing check here is evidence about provenance and structure, never
about biology.

## Source documents

- The two owner-supplied PDFs were parsed and read end to end: 16 main pages
  including STAR Methods and the key resources table, and 9 supplemental pages.
  Both files were hashed; the values are in [Source manifest](SOURCE_MANIFEST.md).
- The supplement was searched for the Excel tables: it contains Figure S1–S5
  legends and Table S2 only. Tables S1 and S3–S6 were then **recovered** on
  4 October 2026 from the NIH PMC Cloud open-data package `PMC12443480.1`, after
  two routes were declined rather than circumvented (PMC's viewer gates `bin/`
  downloads behind an anti-bot challenge; `ars.els-cdn.com` returns 403 to
  non-browser clients). Two checks confirm identity: `supplement-1.pdf` is
  byte-identical to the owner-supplied supplement PDF, and Table S1's `is_HVG`
  flags count 63 pro-inflammatory and 30 pro-regulatory genes out of 116 and 68 —
  the exact numbers the paper states were scored. Recorded under a separate
  `acquisition_v2_supplements.json`, because the frozen Wp-R0 contract hash-binds
  `acquisition_v1.json`.
- Two documentation problems were found by reading, not by computation: the
  pathogenicity-score **sign** is stated one way in Results and the opposite way
  in STAR Methods, and the reused human deposit's own overall-design field claims
  a five-versus-five cohort while its sample records resolve to six donors per
  group. Both are recorded in
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

- **Only Wp-R0 has run under the governed runner**, on 4 October 2026: contract
  frozen and committed, receipt verified with no errors, outputs and receipt
  registered, and every endpoint recomputed by a second route with all twelve
  comparisons agreeing. See the [result](R0_RESULTS.md).
- **Wp-R3, Wp-R1 and Wp-R4 have since executed and verified** (receipts
  `wp_bulk_contrasts_v1`, `wp_singlecell_reproduction_v1`,
  `wp_human_signature_transfer_v1` and the v2 amendment). Each has an independent
  arithmetic check computed from a different output file than the one being
  checked: Wp-R3 recomputed one contrast's log2FC from the TPM matrix with the
  library annotation re-parsed from the GEO SOFT records (max deviation
  4.4e-16 over 11,181 genes, BH count identical); Wp-R1 recomputed library means
  from the per-cell table and animal-paired differences from the library means
  (2.8e-8 and 3.2e-8, CSV rounding); Wp-R4 recomputed donor means from the
  per-cell table (9.8e-17) and reproduced the v2 null to the digit.
- Wp-R2 is frozen and running as a **declared version-and-input sensitivity**.
  Its result may not be described as a reproduction of Figure 1.
- Wp-R5 is **closed, not executed**: the owner declined author contact and figure
  digitisation on 4 October 2026.
- Expression values have now been read for Wp-R1, Wp-R3 and Wp-R4, so those three
  stages are numerical reproductions of published panels, within their stated
  limits. Wp-R5's panels remain cited evidence only.
- Compass 1.0.0 (the authors' wagnerlab-berkeley fork) is now installed and runs
  with the Gurobi WLS licence the owner supplied on 4 October 2026 (licence
  verified by solving a test LP to its exact known optimum). Two execution facts
  are recorded: Compass's own kNN micropooling did not complete on this host
  within 35 minutes of CPU on 8,711 cells, and `multiprocessing.Pool` is denied
  by the sandbox (`CreateNamedPipe`, WinError 5), so the run uses a declared
  serial pool shim and self-computed micropools.
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
The reproduction stages now bind the authors' own gene lists, so the module and
signature definitions are exact; what remains substituted is the embedding and the
cell set, because the analysed 5,192-cell object and the fitted scVI model are not
deposited. The mouse deposits cannot reach population inference at all — one
animal per single-cell condition cell, no animal field in the bulk series — and
the human deposit is the only donor-level unit available.
