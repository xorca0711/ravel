# Nk17-P01: S1M molecular source qualification

17 November 2026. Prospective metadata stage; no gene effects are estimated here.
This stage implements the molecular branch of [S1](ANALYSIS_PLAN.md), not a new
global RQ or a replacement for the remaining stages.

## Purpose and relationship to existing questions

The published premise is that inflammation can leave a lasting epithelial
response state after overt inflammation resolves. The current repository
observation is a saved set of molecular inputs with verified bytes but an
unfinished library/unit crosswalk; no Naik numerical result yet exists at this
freeze. The remaining decision is whether author-provided counts can support
time-matched history comparisons without mistaking runs or replicate labels for
independent animals or paired assays.

`Nk17-P01` owns this paper-specific reproduction/description sequence. It shares
the distinction between regulatory context and later functional output with
[A1](../../RQ_Specified/A1_transitional_epithelial_state_distinction/README.md),
but does not supply A1's registered early-feature/later-output test. It uses
[Arz1-P01](../ungated_arozamena_2026_inflammatory_memory/README.md) as a neighboring
example of source-qualified RNA/accessibility interpretation; intestinal and
epidermal libraries are not interchangeable or independent replication of a
shared dataset. Existing IDs, grades and questions are retained.

## Bounded comparison and measured endpoint

S1M compares identifiers and selected fields across the already saved GEO,
SRA, ENA and BioSample records, then checks the 16 saved processed count tables
for column structure, nonnegative integer representation, gene identifier form,
duplicate identifiers and coverage. It reports library/run/assay/history/time/
platform/reference relations and source disagreements. The endpoint is source
qualification, not gene expression, differential effects, repair or memory.

Biological units would be independently prepared mouse pools if their mapping
is established. This stage starts with unit status unknown and reports deposited
libraries; runs, genes, BioSample IDs and R1/R2 labels are not automatic biological
replicates. The principal validity threat is an incorrect source/library join or
unjustified unit assignment. Only explicit accession links are used. Metadata
fields and filename hints retain their different provenance.

The [existing paper review](PAPER_REVIEW.md#source-version-and-unit-audit) attributes
three pooled mice in duplicate to the final ATAC Figure 3 legend and four pooled
animals in duplicate to the final RNA Figure 4c legend/Methods, while retaining
the author-manuscript 3–4 discrepancy. These are attributed assay-level design
claims, not an animal roster or proof of the exact pool-to-library crosswalk.
The same review attributes STAR/mm10/GENCODE M9 processing and single-end RNA
reads to the paper. S1M checks deposited metadata against those recorded claims
without re-extracting the paper, PDFs, HTML, source workbooks or methods.

## Exposure, exclusions and decision rules

Published figures, selected loci and D6 profiles were previously inspected;
earlier interrupted turns inspected some metadata/source snippets. The recovery
audit examined bytes and filenames. This is exposed metadata qualification,
not confirmation, and a new freeze does not remove prior exposure.

Inputs are the saved GEO SOFT, SRA experiment XML, ENA run TSV, BioSample XML,
16 compressed count files, acquisition JSON records and the existing paper
review as an attributed context source. Code reads only selected metadata
fields and count structure. It does not retrieve new sources or parse paper/
PDF/HTML content, workbooks, raw sequencing reads or experimental procedures.

All declared files and samples are retained. Ambiguous joins, noninteger values,
duplicate gene IDs or incompatible feature universes become explicit scoped
holds; samples are not removed based on effects. No normalization, model fit,
p-value, effect margin or equivalence classification is performed. Library
identity/structure can support descriptive S2 planning while biological-unit
uncertainty continues to limit inference. A platform/time association qualifies
cross-time interpretation without automatically disqualifying within-time
comparisons. A read-layout discrepancy holds exact raw replay, not automatically
the existing processed-count route. No suffix-based cross-time or cross-assay
pairing is permitted.

## Execution and service history

The owner authorized this independently bounded molecular metadata stage and
the local commits needed by the existing runner. The prior service restrictions
and [recovery checkpoint](RECOVERY_CHECKPOINT.md) remain historical evidence;
this authorization does not claim that the restriction was resolved. If this
bounded stage is explicitly rejected, stop and report it without another route.
Freeze and commit the registered contract/code before reading the inputs through
the research runner. Use a new version and retain any failed run if amendment
becomes necessary. Verify/register the receipt, assess the source evidence, and
hand off the exact proposed S2 comparison for parent review before continuing.
