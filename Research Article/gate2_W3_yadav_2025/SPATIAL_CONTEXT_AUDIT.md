# Spatial source definitions and context availability audit

30 October 2026 (Asia/Seoul). Article-local Yd1-P01. This documentation audit
continues the technically reviewed d7e3dd7 checkpoint; it does not confer scientific
acceptance. The [first source audit](SOURCE_QUALIFICATION.md) and its seven hashed
inputs remain valid. New retrievals below are small source metadata, article XML,
supplemental tables and versioned library code, never new atlas expression scans.
The separate S1 marginal contract is exposed source description, not raw spatial
reconstruction.

## S1 availability and definitions

The supplied final article (Fig. 5B; Methods p.14; Data availability p.15) and
[public final text](https://www.jci.org/articles/view/188734) identify Xenium
centroids/counts, analyzer-derived boundaries, low-count filtering and marker
groups. A cell-boundary algorithm version, author AnnData object, segmentation
masks, transcript/centroid matrices, field transforms, patient/FOV-to-result join,
exact call arguments and analysis notebook are not provided by the article's
data-availability links. Its only new sequencing accession remains GSE242510,
already qualified as six coculture libraries, not spatial tissue inputs.
Generic toffy/ark links describe MIBI tooling and do not provide these Xenium inputs.
The bounded article/DOI/GitHub/Zenodo search found no additional paper-specific
spatial deposit; this is an availability result for the searched routes, not proof
that no unindexed or request-only deposit exists.

The [official supplemental tables](https://www.jci.org/articles/view/188734/sd/3)
were recovered from the linked XLSX. Table S1 A6:H14 lists anonymous IDs 1-9 with
Xenium as application; ID 1 is also marked MIBI, with MIBI additionally at IDs
10-13 (rows 15-18). This supplies a participant list and documents imaging overlap,
but no key connects these IDs to 5b!A2:B10, fields or saved statistic arrays.
Neither matching counts nor row order establishes that key. Table S3 lists
CTHRC1 at A78, COL1A1 A185, ARG1 A188 and IL6 A327; panel inclusion does not prove
detection sensitivity or resolve cell calls. No segmentation files accompany it.

The Methods text duplicates IL6-positive in fibroblast categories (b) and (c);
the Fig. 5B plot and official workbook headers distinguish IL6-positive and
IL6-negative fibroblasts. Keep the discrepancy unresolved for raw reconstruction.
The grouped Boolean rules, ARG1 exclusion and handling of other cell types must
come from explicit author definitions/code. The figure legend describes a paired
test and nine patients; the workbook lacks an explicit pairing key. Its separate
mean/SEM wording and the Methods' five half-cell subsample min/max bounds cannot
be silently equated to patient uncertainty. The previously recorded S3C legend
conflict also remains unchanged.

## Squidpy 1.5.0: inspected implementation, not a rerun

[Release notes](https://squidpy.readthedocs.io/en/stable/release/notes-1.5.0.html)
date version 1.5.0 to 27 May 2024 and link
[PR 816](https://github.com/scverse/squidpy/pull/816), merged that day.
The annotated tag resolves to commit
62cc97111fc743bcef0ce79ca1c3d0fb38cd0d90. The
[tagged source](https://github.com/scverse/squidpy/blob/62cc97111fc743bcef0ce79ca1c3d0fb38cd0d90/src/squidpy/gr/_ppatterns.py)
was inspected at _occur_count, _co_occurrence_helper and co_occurrence:

- The radius test includes distances greater than zero and less than or equal to
  the upper threshold; it is cumulative, not an annulus. Zero-distance coincident
  centroids are also excluded. Coordinates must have the intended physical units.
- Counts are accumulated by category pair. Row-normalized counts are divided by
  the neighbor-pair marginal. This weights neighbors through pair counts; it is
  not an explicit equal-weight average of each center's local fraction.
- An integer interval specifies a number of generated thresholds, not a distance
  in micrometres. Explicit thresholds are sorted; results correspond to upper
  thresholds after the first entry. The call/index used for 25 micrometres is missing.
- Multiple split combinations produce separately normalized ratios which are
  then averaged. n_splits can be chosen automatically; it therefore belongs in
  a faithful execution record, alongside the five subsample masks/seeds.

The paper's verbal per-center averaging and the tagged aggregation are not
silently reconciled here. No claim is made that the published values used an
incorrect implementation. Resolving the actual call, data subset, grouping,
distance/index and aggregation is required before a faithful raw reconstruction.
No Squidpy install, toy null, spatial simulation or result replay was run.

## S1 available marginal description and raw hold

**Useful bounded question:** what range and mean separation are present in the
two explicitly labeled columns of the published Fig. 5B statistic? This makes the
source magnitudes inspectable without pretending to reconstruct their statistic.
The workbook maps A1 to IL6+ fibroblast and B1 to IL6- fibroblast, with A2:A10 and
B2:B10 the nine source values each. All are already outcome-exposed.

Freeze a separate descriptive contract for all 18 values and their source
coordinates; report n, arithmetic mean, median, range and IL6+ minus IL6- mean
difference. Plot unlinked values and means with no tests, paired differences,
patient-effect intervals or invented IDs. A ratio-of-one guide describes the
published scale only. Do not regenerate probability ratios or spatial nulls.

**Raw reconstruction remains held.** Reopen only with (1) versioned raw/processed
Xenium counts, centroids and segmentation plus panel/analyzer details and coordinate
units; (2) explicit category Boolean definitions, handling of excluded/other cells
and resolution of the duplicated category; (3) patient, section and FOV identifiers,
field placement and table/result joins; (4) executable author call/version,
threshold/index, split behavior, aggregation and five subsample masks/seeds;
and (5) a separately frozen reconstruction design. A patient-effect estimate
additionally needs valid pairing and independent-patient qualification. No extra
marginal scoring can supply these missing objects.

## New access ledger and coverage

Actual service/date: web search and direct primary HTTPS retrievals,
30 October 2026. Targeted reads, not newly completed full-paper reviews.
Earlier supplied PDF/pixel inspection and GSE242510 recovery were reused.

Search queries actually issued: `"JCI188734" Xenium data code github`;
`"Yadav" "188734" spatial data zenodo`;
`"GSE70867" "GPL14550"`;
`"Salcher" "2022" "atlas" "zenodo" neutrophils`;
`Strunz 2020 alveolar regeneration Krt8 GSE141259`;
`Tsukui 2024 "Alveolar fibroblast lineage" "GSE"`;
`site:nature.com/articles/s41586-024-07660-1 "GSE"`;
`site:ncbi.nlm.nih.gov/geo "Tsukui" "Alveolar fibroblast lineage orchestrates"`;
`site:pmc.ncbi.nlm.nih.gov/articles/PMC9767679 "neutrophils" "Rhapsody"`.
No date filter; this is a source-identity audit, not an exhaustive literature or
novelty search. Incidental results were not added as new biological evidence.

JCI full text, supplemental landing pages, Squidpy release notes and
[Salcher's Zenodo version 2022.10.20](https://zenodo.org/records/7227571) were readable.
The stable Squidpy API page now documents a newer release, so it was not used as
evidence of 1.5.0 behavior. Browser routes challenged GEO/PMC, failed the Squidpy
API/PR and supplemental XLSX fetches, and returned Nature redirect/Cell 403
failures. Direct primary retrieval resolved the metadata/code/XLSX routes below.
Tsukui's Europe PMC XML request returned HTTP 500; its GEO design/README and
indexed primary data-availability section were inspected instead. Salcher and
Strunz targeted primary Results/Methods were read via Europe PMC XML. No external
account sign-in or author contact was attempted.

Retrieved records live in ignored raw_data/Yd1_context_audit_20261030. Exact URLs,
UTC attempts, status and hashes follow; HTTP success alone was followed by content
inspection. No raw count matrices or atlas archives were downloaded.

| Cached source | Primary URL | Attempt UTC / outcome | SHA-256 |
| --- | --- | --- | --- |
| supplement_tables.xlsx | [Source](https://dm5migu4zj3pb.cloudfront.net/manuscripts/188000/188734/JCI188734.sdt1-3.xlsx) | 2026-10-30T08:59:52.145248+00:00 / 200 | 7ddc52108bff769333e6b38a46daf91c9d0108dc06d91e30551c280186a62331 |
| GSE70867.txt | [Source](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE70867&targ=self&form=text&view=full) | 2026-10-30T08:59:52.147348+00:00 / 200 | 91eb5d0ddf1391c09e227209f404416bf379ea20495db97b2b907a9ced6d9f5f |
| GSE210341.txt | [Source](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE210341&targ=self&form=text&view=full) | 2026-10-30T08:59:52.149791+00:00 / 200 | 9af502e3f4d014d4d42ee0ecf6c6e19c0d1c3323758c34186afb6663c9cee324 |
| GSE141259.txt | [Source](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE141259&targ=self&form=text&view=full) | 2026-10-30T08:59:52.150536+00:00 / 200 | 491f2fb49340f798cd0982e280cc1ed17d16c4b23ea099f2c37fed0986482cdf |
| tsukui.xml | [Source](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12088911/fullTextXML) | 2026-10-30T08:59:54.651552+00:00 / HTTP Error 500:  | not retrieved |
| salcher.xml | [Source](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9767679/fullTextXML) | 2026-10-30T08:59:55.153051+00:00 / 200 | 8c6ed35cd679d729b19f5ffbf7cdd705fcf93000324239e5aa1726136676f15c |
| strunz.xml | [Source](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7366678/fullTextXML) | 2026-10-30T08:59:55.228014+00:00 / 200 | 9e83f2f631bfa19dfdc0cc9665e85eeb48e11bd5cf01dd23ae34fa440063fb28 |
| squidpy_v1.5.0_ppatterns.py | [Source](https://raw.githubusercontent.com/scverse/squidpy/v1.5.0/src/squidpy/gr/_ppatterns.py) | 2026-10-30T08:59:55.261593+00:00 / 200 | 04b54a5efa12fa566edeb7727bcb3fc37b77af735647b6fbc545ba1fe2d0e5e8 |
| squidpy_tag.json | [Source](https://api.github.com/repos/scverse/squidpy/git/ref/tags/v1.5.0) | 2026-10-30T08:59:57.372646+00:00 / 200 | b0618c2e0c57259a5315bd17f5d3caaa658665ab33780db4b0104ff32e7dc900 |
| squidpy_pr816.json | [Source](https://api.github.com/repos/scverse/squidpy/pulls/816) | 2026-10-30T08:59:58.663069+00:00 / 200 | 228797a319f1ae1171695a9b8bae668821daf14607b567777247ecdd3f230209 |
| GSE70866.txt | [Source](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE70866&targ=self&form=text&view=full) | 2026-10-30T09:02:59.084015+00:00 / 200 | 98c36f68319f95f0d40d4a9f0db9bac97c4f1fa448f2793cc93aa2d897c856c7 |
| GSE210341_README_demultiplexing.txt | [Source](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE210nnn/GSE210341/suppl/GSE210341_README_demultiplexing.txt) | 2026-10-30T09:02:59.658531+00:00 / 200 | 977a63984285b4cf06deece3fc7f863280ea2a1fe1bedfba58c755fe72a62c31 |
| squidpy_tag_object.json | [Source](https://api.github.com/repos/scverse/squidpy/git/tags/b8b8bea8190fb7f817e1b002d50e6959a165e78e) | 2026-10-30T09:03:01.375475+00:00 / 200 | 3f072d660311bac359d2afdeac516a8abfebc4b8bbe5d74486cb4e2e4eb0b93a |

## C1 source qualification locators

- BAL: [GSE70867](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE70867),
  subseries [GSE70866](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE70866),
  last updated 3 April 2019; Yadav Fig. 1D and Methods select GPL14550.
  The superseries includes other platforms/experiments; its total is not the
  selected contrast denominator.
- Strunz: [GSE141259](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE141259),
  last updated 17 May 2022; [primary paper](https://doi.org/10.1038/s41467-020-17358-3),
  Fig. 1 and whole-lung versus high-resolution Methods. Author code:
  [2019_Strunz](https://github.com/theislab/2019_Strunz).
- Tsukui: [GSE210341](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE210341),
  public 18 April 2024, updated 12 July 2024; PMID 38987592 /
  [Nature 2024](https://doi.org/10.1038/s41586-024-07660-1).
  GEO Overall design and the linked demultiplexing README distinguish 12 tagged
  source samples from four pooled sequencing lanes and the single GSM record.
- Salcher: [Cancer Cell 2022](https://doi.org/10.1016/j.ccell.2022.10.008),
  [primary XML route](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9767679/fullTextXML),
  Results first atlas section, neutrophil capture section, Fig. 1/S1,
  STAR Methods datasets and Data/code availability. Author code:
  [icbi-lab/luca](https://github.com/icbi-lab/luca); processed data
  [version 2022.10.20](https://zenodo.org/records/7227571), published concept
  DOI [10.5281/zenodo.6411867](https://doi.org/10.5281/zenodo.6411867).
  The model-only archive contains selected genes and is not automatically the
  expression input. No exact Yadav download filename/checksum is specified.
