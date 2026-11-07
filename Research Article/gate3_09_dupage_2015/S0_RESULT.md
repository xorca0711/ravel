# Dp1-S0: source qualification

7 November 2026; exposed metadata work. **Executed and independently checked.**
[Contract](contracts/Dp1.S0.source_qualification_v1.json) ·
[Receipt](../../analysis/research/runs/dupage_s0_qualification_v1/receipt.json) ·
[Full qualification](../../analysis/research/runs/dupage_s0_qualification_v1/qualification.json) ·
[Sample manifest](../../analysis/research/runs/dupage_s0_qualification_v1/sample_manifest.tsv) ·
[File QC](../../analysis/research/runs/dupage_s0_qualification_v1/file_qc.tsv)

## Measured result and permitted route

All 12 deposited files contain 23,846 rows. There are 250 duplicated gene labels;
their 744 rows are excluded rather than summed or merged by symbol. The remaining
**23,102 unique gene-labelled mm10 spans agree exactly across all 12 libraries**.
Of these, **22,997 have OK status in all 11 retained libraries**. There are no
negative or nonfinite FPKM values. This qualifies a descriptive comparison of
compatible gene-labelled loci; exact annotation-release and exon-model identity
remain unverified. It does not qualify transcript-level inference.

The published exclusion is preserved: GSM1423627, HET/high replicate 3. The
retained design is **HET/high 2, HET/low 3, KO/high 3, KO/low 3**. The excluded
library has only **927 reads** across its linked ENA runs. Each library links to
two runs: **24 runs are not 24 biological replicates**. All SRX/BioSample joins
agree. ENA lists 348,803,897 reads and 16,551,370,115 compressed FASTQ bytes
across the deposited study. These are archive metadata, not measured alignment
depth or a completed read-integrity audit.

The merged file has 23,235 group-level rows. Only **19,526** have an unambiguous
exact symbol-and-span match to the common per-library features. Its XLOC IDs
must not be joined to sample IDs by their number. Keep merged estimates separate
from arithmetic averages of the library FPKM; confidence bounds are not animal
SEM. [Exact crosswalk](../../analysis/research/runs/dupage_s0_qualification_v1/merged_crosswalk.tsv).

Unknown individual mouse IDs, pool membership, cross-state pairing, age and batch
remain unknown. No count matrix or supported transcript-import input was found
in the deposited supplementary products. **Count/population inference is held**;
descriptive per-library FPKM and separately labelled four-estimate reconstruction
are eligible. No counts are fabricated from FPKM or coverage.

## Source recovery and access

Cached GEO input hashes agree with [SOURCE_REVIEW](SOURCE_REVIEW.md). Exact
inputs and hashes are bound in the contract. New ENA query, retrieved 7 November:
[PRJNA254138 run report](https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA254138&result=read_run&fields=run_accession,experiment_accession,sample_accession,secondary_sample_accession,read_count,base_count,library_layout,fastq_ftp,fastq_bytes&format=tsv).

The [NCBI PMC efetch endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=4347854)
recovered the full article XML (133,444 bytes; SHA-256
`d998434d7a925a11ceaad80585e8d4575930e657c150999d429ef2dafdebafd3`).
It identifies exact supplement names `NIHMS659668-supplement-1.xlsx`,
`NIHMS659668-supplement-2.docx`, and `NIHMS659668-supplement-3.pdf`.
The files themselves are **not recovered**: PMC returned HTML download challenges
despite HTTP 200; Europe PMC's exact-file route returned 403. Its supplementary
API returned a non-open-access error XML, not a ZIP. The publisher article and
candidate CDN supplement returned 403; Europe PMC full-text XML returned 500;
the OA query returned 404; publisher/PMC HTML were browser challenges. The
eScholarship web route also failed. These are route-specific failures, not proof
that the supplements or functional source data do not exist. Access responses
and request URLs remain in ignored `raw_data/dupage_20261107/access_attempts_v*.json`.
The initial sandbox DNS failure was resolved using authorized public retrieval.

## Independent verification

Receipt verification passed. A separate parser indexed each original archive
member by gene ID, required exactly one row, and compared symbol, span, FPKM
string and status for **277,224 matrix cells (23,102 × 12)**: all matched.
It independently reconciled all 24 run accessions and read/FASTQ byte totals
against the saved ENA table. This is arithmetic/source verification, not biological
replication. No expression contrasts, PCA or enrichment have run in S0.

## Checkpoint and next comparison

The mistaken-feature/replicate threat is narrowed sufficiently for a bounded RNA
reconstruction. Unknown biological nesting and selection into the surviving
Foxp3-positive gate remain the leading limits. **S1 is justified** to determine
whether stronger low-state divergence is visible across retained libraries,
rather than merely in four merged estimates. Freeze its transform, eligibility,
PCA and contrast definitions before numerical execution. This is an adapted
descriptive reconstruction, not an exact Figure 6 replay.

Raw-read reprocessing is not needed for that decision. A later proposal would
first qualify mouse/pool provenance, then download/check the listed ~16.55 GB
compressed FASTQs, pin mouse reference/annotation and quantifier, quantify each
library with its two runs combined, and specify storage/runtime and count-model
design under a new contract. Raw reprocessing alone cannot recover missing animal
identities. No such job has started.
