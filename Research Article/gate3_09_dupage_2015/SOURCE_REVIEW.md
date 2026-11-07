# DuPage 2015 source and reading review

Review date: **7 November 2026 (Asia/Seoul)**. Scope: documentation and
deposited-file inspection; no expression model, enrichment or biological rerun.
Base: `dcee4b63e11abd27fe2bbc679993b288e913565e` (fetched main).

## Sources actually inspected

- Owner-supplied annotated published PDF, 13 PDF pages including the graphical
  abstract; journal pages 227-238. SHA-256:
  `a2eab6ab2e3a5a82ce11e66385576676b807d2f41ceb4ee432b5d469248ef0e9`.
  Text extracted; all ten annotated pages (PDF 2-11) visually inspected.
  There are 171 annotation objects and no nonempty text-comment fields.
  Highlights/underlines emphasize activation, mosaic controls, RNA/chromatin
  comparisons, tissue loss and the indirect-effect caveat. No claim is made
  that highlighting equals endorsement of every causal interpretation.
- The owner's main Notion paper note, linked Results subpage and Discussion
  subpage were fetched. These are private reading evidence, not public data or
  instructions. Their personal ancestry and full note contents are not copied
  into this repository. The detailed reconciliation below paraphrases only the
  scientific points needed for planning. No Notion content was edited.
- [Publication record](https://pubmed.ncbi.nlm.nih.gov/25680271/),
  [GEO series](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE58998),
  sample metadata and full SOFT response; the two GEO supplementary downloads
  were retrieved and their archive members/headers inspected.
- Current repository instructions, registry, article roadmap, relevant current
  summaries and the 4 November biological-screening workflow were read. The old
  root checkout at `78320a1` has unrelated `PROGRESS.md` edits; it was preserved.
  This package is in `codex/dupage-stepwise-plan-20261107` from current main.

Access limits: the Cell full-text endpoint returned 403; PMC and eScholarship
returned browser checks; the Europe PMC full-text API returned 500. The supplied
PDF provided the full main paper. The separate 2015 supplement (seven figures,
one table and detailed procedures) was **not recovered**. References to S1-S7
below are from the main text, not a claim to have inspected those supplemental
panels. These access failures do not establish that the supplement or raw
functional measurements are absent from all sources.

## Paper logic, evidence and note reconciliation

| Link / exact locator | What was measured | Consequence for the plan |
|---|---|---|
| Figure 1A-D; journal p.228 / PDF p.3 | Human naive CD4 microarray co-stimulation comparison, mouse Treg Ezh2 RNA/protein and H3K27me3 flow measurements | The upstream CD28 premise spans assays/species. GSE58998 is not a CD28 perturbation experiment. |
| Figure 2F; p.229 / PDF p.4 | Suppression by sorted CD62L-high Tregs in a short in-vitro assay | "Functioning properly" is limited to this assay/population; it is not preserved activated-tissue function. |
| Figures 3-4; pp.229-231 / PDF pp.4-6 | Systemic phenotype; WT-cell depletion in mosaic adult mice; T-cell activation and Foxp3 expression | Healthy mosaic controls reduce the systemic-inflammation alternative. They do not identify every downstream mechanism. |
| Figure 5 and main-text discussion of S4F-H; pp.230-232 / PDF pp.5-7 | Foxp3-reporter/lineage-reporter frequencies across tissues and activation strata | Identity retention and abundance are distinct endpoints. Reporter history alone does not specify the exact timing of destabilization. |
| Figure 6A-B; pp.231-233 / PDF pp.6-8 | Sorted Foxp3-positive Treg RNA from spleen/LN of healthy mosaic females | This is a selected surviving population. Figure 6A plots four group averages, not the individual biological samples. |
| Figure 6C-F; pp.231-233 / PDF pp.6-8 | RNA comparison with Arvey H3K27me3, Gavin Foxp3-loss and Samstein Foxp3-binding evidence | External chromatin overlap supports consistency; it is not matched KO H3K27me3 loss or mediation. |
| Figure 7A-H and main-text account of S7; pp.232-235 / PDF pp.7-10 | EAE severity/remission, antigen-specific Treg frequencies/Foxp3; similar early division and increased later apoptosis reported | Preserve survival and identity loss as potentially coexisting explanations. Tissue paucity alone cannot establish impaired homing. |
| Discussion; pp.235-236 / PDF pp.10-11 | Proposed lymphoid activation → effector differentiation → tissue migration/function sequence | Keep this as the organizing model, with each unmeasured connecting arrow explicit. The authors themselves request KO-cell chromatin measurement. |

Specific clarifications for the reading notes:

1. The RNA comparator is **Ezh2 HET (conditional one-allele deletion) versus KO**,
   not ordinary WT versus KO. WT Tregs in mosaic animals help preserve the
   environment, but they are not the sequenced HET comparator group.
2. The notation is **PRC2**, not PCR2. The tetramer uses **MOG38-49**; EAE
   immunization and the 2D2 specificity are described with **MOG35-55**.
3. CD62L-high/low sorting is an activation-associated state comparison, not an
   experimental activation time course. Foxp3-positive sorting does not prove
   that every profiled cell will later lose Foxp3.
4. The conclusion "via H3K27me3" must retain the authors' p.236 caveat: direct
   chromatin effects were not measured in the knockout samples. An indirect or
   noncanonical contribution remains possible.
5. Initial proliferation and short-term suppression can remain intact while
   later survival, identity retention and in-vivo control fail. These are the
   biological distinctions to preserve through the hypothesis sequence.

## Deposited data: verified structure

[GSE58998](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE58998)
is linked by the paper's accession statement (p.237 / PDF p.12).
Published 9 February 2015; metadata last updated 15 May 2019. It links
BioProject **PRJNA254138**, SRA **SRP044008**, platform **GPL17021**.
Sequencing is single-end 50 bp Illumina HiSeq 2500; the source pipeline uses
mm10, TopHat and Cufflinks 2.1.1.

| Group | GEO samples | Deposited libraries | Retained in publication |
|---|---|---:|---:|
| HET, CD62L-high | GSM1423625-1423627 | 3 | 2 |
| HET, CD62L-low | GSM1423628-1423630 | 3 | 3 |
| KO, CD62L-high | GSM1423631-1423633 | 3 | 3 |
| KO, CD62L-low | GSM1423634-1423636 | 3 | 3 |

**GSM1423627** is explicitly excluded for low read counts in GEO processing
metadata and its sample description. Figure 6A and the main methods agree with
2/3/3/3 biological samples. Preserve the excluded library as source evidence;
do not reintroduce it silently to balance the design.

Samples are female C57BL/6, spleen and lymph-node Tregs from
Foxp3YFP-Cre/Foxp3WT;Ezh2fl/+ or Ezh2fl/fl animals. The main paper gives the RNA
sort as CD4+CD25+YFP+RFP+, subdivided by CD62L. It calls the replicates biological
samples. The inspected deposit does **not** give a per-mouse/pool crosswalk,
state-pairing keys, sequencing batch, exact sample ages or a complete allocation
record. Do not infer pairing from "rep1" shared across group names or equate
BioSample accession uniqueness with independent animals.

| Download | Inspected contents and usable role |
|---|---|
| `GSE58998_FPKM_all_samples_merged.txt.gz` (1,369,392 bytes) | Feature metadata plus **Het_hi, Het_lo, KO_hi, KO_lo FPKM**, confidence limits and status. Four condition estimates, not twelve sample columns. Suitable for source display once feature/aggregation semantics are qualified. Confidence limits are not between-animal SEM. |
| `GSE58998_RAW.tar` (9,205,760 bytes) | Twelve compressed `GSM...FPKM...txt.gz` files, including the excluded library. Headers contain tracking/reference/gene/TSS/locus fields, coverage, FPKM, confidence limits and status. "RAW" is the archive name; the contents inspected are processed expression estimates. |
| Full GEO SOFT response (11,181,750 bytes) | Series, platform and all sample metadata; sample data-row counts are zero. Metadata are not an additional expression matrix. |
| SRA linkage | Raw sequencing is advertised. Run-level joins, read integrity and a count-quantification workflow have not been qualified or downloaded in this review. |

Retrieve from the [GEO supplementary directory](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE58nnn/GSE58998/suppl/).
File SHA-256 values at this retrieval:

```text
GSE58998_RAW.tar
87eb8b660d7b83c501040c984db62b9501acbe24c8fb7d9f91a531835fa78e6f
GSE58998_FPKM_all_samples_merged.txt.gz
b5ef0d73b19e21c2cee6c89d306e6d99affc8d4e48b5c0ba8205c1151fa8aa51
GSE58998 full SOFT response
b667cc7b64e7161be6edfc9ff6005811e8cc011b37474113a7638cbfc6fa4ece
```

The downloaded source files and private PDF extraction remain outside tracked
research evidence. A future execution must place its exact qualified inputs in
the declared input location and bind these or newly documented hashes. This
header/archive inspection is not a numerical research run or a receipt.

## External sources that must remain separate

- Arvey et al. 2014 supplies activation-associated H3K27me3 context; Gavin et al.
  2007 supplies Foxp3-loss expression; Samstein et al. 2012 supplies binding;
  Hill et al. 2007 supplies Treg-signature context. Exact supplemental versions,
  sample selections and feature mapping remain S0/S3 qualification tasks.
- GSE55705 is identified as Arvey's **microarray** series; do not mislabel it as
  the H3K27me3 sequencing deposit without following and verifying the assay links.
- Peeters et al. 2024 reports RNA-seq **GSE262130** and CUT&RUN **GSE262129**.
  He et al. 2026 reports **GSE291449**. These are publication-verified leads;
  their actual downloadable assay/sample crosswalks were not recovered here.
- No raw FCS, per-mouse EAE trajectories or matched knockout H3K27me3 assay was
  found in the inspected GSE58998 supplement listing. This is a listing-level
  limit, not a source-wide claim of nonexistence.

## Exposure and next action

The owner and reviewing agent have read the published outcomes; the agent also
inspected file headers and literature results. This is exposed reproduction /
exploratory planning. A later freeze cannot make it confirmatory. Next: execute
the bounded source/feature qualification specified in [Dp1-S0](ANALYSIS_PLAN.md#dp1-s0--qualify-the-observation-before-fitting-a-model)
under its own contract, then choose the permitted descriptive or inferential route.


## Execution-era source update

The review above records initial planning access. [S0](S0_RESULT.md) adds the
ENA run crosswalk and article XML; [S3](S3_RESULT.md) records recovered Arvey
sources and annotation. The separate 2015 supplement remains unrecovered.
Current results are in [RESULTS](RESULTS.md); originals/private material were
preserved.
