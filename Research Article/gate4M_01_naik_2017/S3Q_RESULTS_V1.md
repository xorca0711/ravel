# S3Q v1: original ATAC input qualification

18 November 2026. `Nk17-P01`; metadata qualification complete and coordinator-
reviewed. All eight original D6/D30 files are acquired and readable through the
supported reader. Core chromosome lengths are qualified, while deposited signal
units and the original retained-region universe remain unresolved. No biological
accessibility comparison was run by S3Q. Coordinator review is not human scientific
acceptance.

## Confirmed source and reader findings

The [method](S3Q_METHOD_V1.md) and
[contract](../../analysis/research/contracts/Nk17-P01.s3q_track_qualification_v1.json)
were frozen at `230b3548e9775b2d638ca386045a6cf0620d2343`. The
[receipt](../../analysis/research/runs/naik2017_s3q_track_qualification_v1/receipt.json)
binds 19 inputs, three scripts and six outputs. Input preflight, execution and
receipt integrity passed; the independent verifier passed **1,789 checks**.
No real S3Q run failed or frozen S1M/S2/S4/S4B artifact changed.
Final checks passed against freshly fetched main `d0429d0`: the research gate,
all 20,125 repository checks including tracked local links, and whitespace.
GitHub CLI identity is verified `xorca0711`; commits retain Xorca attribution.

GSM2441001–1008 join exactly to their saved GEO supplementary URLs and frozen
S1M records: two control/history libraries at D6 and at D30. Their 6,679,503,736
bytes have preserved local SHA-256 records. The
[source table](../../analysis/research/runs/naik2017_s3q_track_qualification_v1/source_identity.tsv)
retains every URL, hash, label and processing statement. This verifies accession/
file joins, not the identity of the underlying animals. S1M records all eight as
HiSeq 4000/paired; pooled-preparation membership and assay pairing remain unknown.
The original paper's biological-replicate/pooling statements remain positive
design evidence and are not erased by missing individual-animal identifiers.

All eight BigWigs use the same 66-entry chromosome dictionary, totaling
2,730,871,774 bases. **Chr1–19, X, Y and M match the UCSC mm10 names and lengths
exactly.** The other 44 entries use accession-style names such as `GL456210.1`
rather than UCSC-style noncanonical names. Their aliases were not mapped or
silently renamed. Thus the literal all-name compatibility flag is false, while
the core chromosomes are qualified; this is not evidence that the whole genome
build is wrong. Every original entry remains in the
[dictionary table](../../analysis/research/runs/naik2017_s3q_track_qualification_v1/chromosome_dictionary.tsv).

Each stored `basesCovered` equals the entire declared dictionary length. The
prespecified chr1:10,000,000–10,000,100 query returned 100 finite values and no
missing values in every file. Only query shape/missingness counts were retained.
This is bounded readability evidence, not an independent decode of every block.
The supported reader also passed the separate upstream toy-file checks recorded
in the [runtime/acquisition note](S3_RUNTIME_V1.md).

## Deposited scale is still unassigned

| Library | Condition | Stored mean | Stored standard deviation | Stored maximum |
|---|---|---:|---:|---:|
| GSM2441001 | D6 C1 | 1.308 | 18.088 | 11,325 |
| GSM2441002 | D6 C2 | 1.216 | 18.380 | 11,339 |
| GSM2441003 | D6 H1 | 1.569 | 19.017 | 12,910 |
| GSM2441004 | D6 H2 | 1.069 | 15.374 | 10,624 |
| GSM2441005 | D30 C1 | 0.879 | 22.993 | 15,420 |
| GSM2441006 | D30 C2 | 0.846 | 24.001 | 16,831 |
| GSM2441007 | D30 H1 | 1.009 | 21.179 | 13,926 |
| GSM2441008 | D30 H2 | 0.985 | 20.020 | 13,144 |

Every stored minimum is zero. These are
[stored header summaries](../../analysis/research/runs/naik2017_s3q_track_qualification_v1/header_metadata.json),
not biological effect estimates. They do not certify raw coverage, RPM or the
paper's Z-score representation. The full encoded universe is not represented
with mean zero/unit variance, but a header cannot recover transformations,
filtering, clipping or the precise background used elsewhere in the analysis.
GEO processing metadata states mm10 alignment and `.bw` format without a unit.
The coordinator's bounded paper-method note describes per-base genome-wide Z
scores excluding MT/Y, 500-bp bins and peak analyses; it does not establish the
deposited file scale. No between-track normalization is inferred from file size,
means, chromosome presence or the ability to read them.

## Original coordinates and next measured endpoint

The coordinator's original-source review found MOESM9 Figure 3 source data
contains pathway binomial p-values and an empty sheet, not peak coordinates.
Targeted reporting-PDF headings supplied no identified coordinate table. These
are bounded findings, not proof that coordinates never exist. The later Cowley
domain set uses Larsen GSE171596 for D6/D30 and cannot replace the Naik universe;
its source/version/access limitations are retained in [literature context](LITERATURE_CONTEXT.md).
No duplicate workbook scan or rejected broad extraction was attempted here.

Exact Naik retained-region reproduction remains unresolved. The coordinator
reviewed S3Q and explicitly approved a **new, narrower prospective adaptation**:
within-library relative ordering of signal near annotation-defined protein-coding
gene 5′ boundaries, with a fixed universe and explicit processing assumptions.
This is a different measured endpoint, not acceptance of absolute accessibility
comparability or recovery of the original distal domains. The historical plan
and S3Q evidence remain unchanged. A separate amendment, frozen method/contract,
artificial tests, exact-read verification and visual review must precede its
completion. S5/S6 remain later stages; local preservation is not completion of
the overall research sequence.
