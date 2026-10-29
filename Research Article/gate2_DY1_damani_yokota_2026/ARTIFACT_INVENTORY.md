# Saved artifacts at documentation close-out

The canonical article package is `Research Article/gate2_DY1_damani_yokota_2026/`.
Worktree: `C:/Users/dream/.codex/worktrees/nam-memory-execution-20261029/ravel`.
Branch: `codex/nam-memory-execution-20261029`.
Reviewed starting commit: `a0e7472e1fb24f4892a6084f486e9bef9e973b08`.
Frozen source checkpoint: `a2ae09e12f604e4926dc9b510558c3442cdc9445`.

## Committed evidence

| Artifact | Purpose |
|---|---|
| [source_v1 contract](config/source_v1.json) | Frozen exposed metadata specification and exact input/code hashes |
| [qualification script](scripts/qualify_sources_v1.py) | Historical executed parser; known label/interpretation limitations retained |
| [receipt](../../analysis/research/runs/DY1_source_v1/receipt.json) | Successful metadata execution at a2ae09e; acceptance not assessed |
| [sample map](../../analysis/research/runs/DY1_source_v1/sample_map.tsv) | 22 source sample records; animal/pool mapping explicitly unknown |
| [structural qualification](../../analysis/research/runs/DY1_source_v1/source_qualification.json) | Matrix dimensions, feature types, exon-bin identifiers and CMO references; read with the correction note |
| [retrieval manifest](../../analysis/research/runs/DY1_source_v1/retrieval_manifest.json) | Processed-file URLs, retrieval times, byte counts and SHA-256 values |
| [access recovery](../../analysis/research/runs/DY1_source_v1/access_recovery.json) | Public access attempts, including Code Ocean 403 and publisher challenge described in the correction |
| [superseding note](SOURCE_QUALIFICATION_CORRECTION.md) | Documentary correction; preserves v1 bytes and does not imply a v2 execution |

The run directory also retains its original stdout and empty stderr logs.
Its receipt's original `verification: pending` field is unchanged; subsequent
hash verification is documented in [CLOSEOUT](CLOSEOUT.md), not edited into history.

## Ignored local inputs and preparation

- `raw_data/nam_memory_2026/`: cached public GEO records, four small CMO
  references, eight narrowPeak files, six exon-count files, four matrix/feature/
  barcode triplets, compressed source CMO references and retrieval/access logs.
  Exact frozen inputs are enumerated in source_v1 and its receipt.
- The same ignored folder contains subsequent preparation only: two BioSample
  records, an SRA record, publisher client-challenge response, reused mm10 RefGene
  annotation and public literature lookup/BioC files. These were not inputs to a
  later executed run or qualified regulatory target set.
- `raw_data/GSE136831/`: four existing public atlas files copied from Ravel's
  established local cache to satisfy the runner's repository-relative input
  boundary. No repeat download or human analysis occurred; original cache unchanged.
- Supplied private paper/slides and pre-existing review extracts remain in their
  original private locations. No supplied full-text document or private PI,
  Notion, placement or identity content is included in tracked outputs.

No stage 1-8 contract, biological effect table, enrichment, regulatory network,
human contrast or measured figure exists. No new A-series ID or RQ output was
created. Existing RQ folders retain their canonical work unchanged. The execution
worktree and ignored inputs are preserved; no cleanup, archive or deletion ran.
