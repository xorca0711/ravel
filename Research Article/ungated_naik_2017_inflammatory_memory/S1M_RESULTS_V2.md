<a id="s1m-molecular-source-qualification-and-s2-handoff"></a>

# S1M molecular sources and S2 eligibility

18 November 2026. **Molecular metadata qualification completed with the limits
below; S2 has not run.** This stage qualifies deposited libraries and count-table
structure. It estimates no gene effect, recovery equivalence, chromatin effect
or functional output. The published biological premise and the
[original analysis plan](ANALYSIS_PLAN.md) remain unchanged.

## Execution and current evidence

Owner: `Nk17-P01`. The current [frozen contract](../../analysis/research/contracts/Nk17-P01.s1m_metadata_v2.json)
and [code](scripts/qualify_s1m_v2.py) were committed before execution at
`399ef62def8e09d9c6599a414eecd2734c7567e4`. The
[v2 receipt](../../analysis/research/runs/naik2017_s1m_metadata_v2/receipt.json)
is verified and registered. The run completed on 17 November at 23:57:57 KST;
this interpretation/handoff was prepared on 18 November.

- [Library crosswalk](../../analysis/research/runs/naik2017_s1m_metadata_v2/library_crosswalk.tsv):
  accession, assay, history/time labels, replicate label, platform/reference,
  source compartment, characteristics, pooling claim and unresolved unit mapping.
- [Run crosswalk](../../analysis/research/runs/naik2017_s1m_metadata_v2/run_crosswalk.tsv):
  experiment/run/BioSample joins and SRA/ENA layout/instrument concordance.
- [Selected source fields](../../analysis/research/runs/naik2017_s1m_metadata_v2/source_fields.json):
  GEO line numbers, SRA accession locators, ENA row numbers, BioSample attributes
  and acquisition URLs/timestamps/hashes. The saved records are the source version
  used here; no fresh public-source retrieval or literature search was performed.
- [Count structure](../../analysis/research/runs/naik2017_s1m_metadata_v2/count_structure.tsv),
  [identifier coverage](../../analysis/research/runs/naik2017_s1m_metadata_v2/identifier_coverage.json),
  [qualification summary](../../analysis/research/runs/naik2017_s1m_metadata_v2/qualification.json)
  and [runner report](../../analysis/research/runs/naik2017_s1m_metadata_v2/S1M_REPORT.md).

The [v1 receipt](../../analysis/research/runs/naik2017_s1m_metadata_v1/receipt.json)
records the first successful execution from `b5f96ecfce41b60fe09061720824ecdadacc4afb`.
V1 correctly joined accessions and checked counts, but left compact GEO titles
unclassified. [V2's amendment](S1M_AMENDMENT_V2.md) preserves that limitation and
the pre-execution refusal of uncommitted v2 code. Both versions remain registered
and byte-preserved; v2 supersedes the incomplete grouping. No failed biological
result was hidden or rerun to obtain a favorable effect.

## Source-qualified observations

All **28 GEO libraries** join to 28 SRA experiments, 28 ENA runs and 28 distinct
saved BioSample records. Each deposited library has one matched experiment/run
in this snapshot. No source join, selected SRA/ENA field, condition/time label
or count-structure conflict was detected. Distinct accessions establish record
identity; they do not establish independent animals.

| Deposited group | Libraries | Instrument / layout | Qualified reference |
|---|---:|---|---|
| D6 RNA, control and prior inflammation | 2 per history | HiSeq 4000 / paired | GEO: STAR, mm10, GENCODE M9 |
| D30 RNA, baseline labels, both histories | 2 per history | HiSeq 2500 / single | Same stated RNA reference |
| D30 RNA, 6-hour wound labels, both histories | 2 per history | HiSeq 2500 / single | Same stated RNA reference |
| D30 RNA, 12-hour wound labels, both histories | 2 per history | HiSeq 2500 / single | Same stated RNA reference |
| D6 and D30 ATAC, both histories | 2 per history at each time | HiSeq 4000 / paired | GEO: bowtie, mm10 |
| D180 ATAC, both histories | 2 per history | HiSeq 2500 / paired | GEO: bowtie, mm10 |

The deposited RNA platform IDs are `GPL21103` for D6 and `GPL17021` for D30/recall.
Within each RNA timepoint, both history groups share the instrument/layout.
Time and instrument/layout are associated across D6 versus D30; a biological
time effect or history-by-time interaction cannot simply be separated from
technical differences using these records. The same qualification applies to
D180 versus earlier ATAC. This does not automatically invalidate within-time
history contrasts.

RNA D6 paired-end deposition is confirmed for `SRR5133553`–`SRR5133556` in both
SRA and ENA. The other 12 RNA runs are single-end. The discrepancy with the
paper's single-end statement retained in [PAPER_REVIEW](PAPER_REVIEW.md#source-version-and-unit-audit)
therefore specifically affects exact D6 raw-read replay. It does not establish
that the deposited processed counts are unusable.

The samples are described as female C57BL/6 adult skin epithelia. Age in weeks,
animal membership and preparation batch are not established by the selected
attributes. D6/D30 and recall history labels are corroborated by deposited
characteristics. Recall characteristics explicitly specify a day-30 wound and
6-/12-hour harvest labels. D180 time/history labels come from titles; selected
D180 characteristics omit treatment/time. Retain that weaker D180 qualification.
No suffix-based longitudinal or cross-assay pairing was assigned.

Exact source examples in the decompressed GEO SOFT are GSM2440985 title line 89,
characteristics 99–103, processing 110–112, and relations 125–126; GSM2440989
corresponding lines 257, 267–271, 278–280 and 293–294; GSM2440993's recall
characteristic is line 439. GSM2652413's title is line 1097, with only the selected
sex/strain/cell/sort characteristics at 1107–1110. These locators and values are
retained in `source_fields.json` without reading paper/PDF/HTML methods.

## Count semantics and biological-unit limits

All 16 processed RNA tables have **47,729 rows and two fields per row**: a
versioned mouse Ensembl gene ID and one nonnegative integer count. There are no
duplicate IDs, malformed numeric fields, STAR summary rows or differing gene-ID
orders. The intersection and union are both 47,729 IDs. GEO explicitly describes
`GENE_ID, Counts`, with counts generated from STAR GeneCounts output.

S2 can use the sole deposited count column, retaining exact versioned IDs. These
files do not expose the original three-column STAR strand outputs, and the
chosen strand convention cannot be established from their structure alone.
Annotation remapping, feature filtering and normalization remain prospective S2
choices. This audit did not inspect gene effects or classify genes as persistent
or resolved.

The existing paper review attributes three pooled mice in duplicate to ATAC
and four pooled animals in duplicate to RNA in the final publication; it retains
the manuscript's RNA 3–4 wording. These are positive source claims supporting a
pooled duplicate-preparation design, not evidence that replication is absent.
The deposited R1/R2 labels are consistent with that design. However, the selected
records provide no animal roster, explicit pool membership/overlap, preparation
batch or RNA-to-ATAC pairing map. Distinct BioSamples and runs do not supply that
information. Missing individual IDs alone does not refute the reported design.

For a formal population model, explicitly assess and record whether the
author-reported duplicate preparations sufficiently qualify independent pools
for the intended comparison. Until that decision, the permitted S2 description
uses two deposited libraries per history, without treating pooled mice, genes
or sequencing runs as additional replicates. No single-mouse variance or paired
design is established here.

## Exact proposed S2 comparison for parent review

Use eight author-provided baseline-label RNA tables and estimate the two
**separate within-time prior-inflammation versus control contrasts**:

| Contrast direction | Prior-inflammation libraries | Time-matched controls |
|---|---|---|
| D6 history minus control | GSM2440987, GSM2440988 | GSM2440985, GSM2440986 |
| D30 history minus control | GSM2440991, GSM2440992 | GSM2440989, GSM2440990 |

The measured endpoint would be library-level normalized gene-count differences
and descriptive history/control effects within each time, showing both library
values. Begin with the common 47,729 exact gene IDs; freeze filtering,
normalization, zero handling and effect reporting in the separate S2 contract
before calculation. The source joins and count structure support this scope.
An inferential model is conditional on the explicit pool-independence assessment
above; no such model or population p-values are authorized by this handoff.

Compare the two effect profiles only with the cross-time platform/layout
qualification, without claiming a batch-separated recovery effect, equivalence,
longitudinal pairing or a resolved/persistent class from non-significance.
The RNA result could later narrow whether acute patterns attenuate or remain
mixed, but this metadata stage does not answer that biological question.
The 6-/12-hour recall libraries remain for S4 and ATAC libraries for S3; they are
not additional replicates for S2. Functional workbooks and source-method
qualification remain outside S1M and were not resumed.

<a id="validation-and-handoff-boundary"></a>

## Validation and analytical scope

Both contracts passed input preflight; both receipts passed verification and
registration. Synthetic tests covered count structure, explicit accession joins,
compact labels and label contradictions. Independent checks, written separately
from the execution parser, matched all 28 literal GEO sample/experiment links,
all 28 ENA run/experiment/BioSample/layout tuples, and all GEO BioSample pointers
to the saved BioSample records. A separate count reader reproduced the 16
47,729-by-two tables, unique gene counts and identical ordered identifier hashes.
This is source/arithmetic verification using shared inputs, not replication.

The coordinator's 18 November review also reported that GSM2440985, GSM2440993
and GSM2441005 source spot-checks supported the title/characteristic labels and
identified no source-join revision. This is coordinating-agent review evidence,
not independent human scientific acceptance.

Final checks passed: the full research gate against refreshed `origin/main`
(`d0429d0205fab3e079ea949d0cb0b3a0c1a4a4be`), 19,994 repository validation checks,
and 53 local links plus whitespace/conflict checks across affected documentation.
The registry comparison confirms that only Nk17-P01 and its contracts/receipts
were added. Valid unchanged framework and historical scientific checks were
reused; historical analyses were not rerun. The two local setup commits retain
verified Xorca author/committer attribution. Current v2 outputs, receipt
registration and interpretation updates remain uncommitted for parent review.

The 28 empty final `disagreements` cells in each run crosswalk are valid TSV
fields. The generic Git whitespace check flags their trailing separators; uniform
12-field rows were checked and frozen bytes preserved. Other affected text is
checked separately. No validator, safeguard, claim grade or governance rule was
changed. The three earlier service failures and recovery checkpoint remain
preserved; S1M's execution does not certify that those restrictions were resolved.

This handoff stops at parent review of S1M and the proposed S2 scope. The broader
analysis plan remains unfinished. No push, PR, merge, external message or
scientific acceptance is implied.
