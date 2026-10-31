# Checkpoint C: two-source qualification and a held X5 design

31 October 2026, Asia/Seoul. Owner **Yd1-P01**. Implemented the
[bounded C authorization](REVIEW_B.md) after adopting reviewed integration
`0c24535344e214f888405dcb2755b0f7faa5699d`.
**Metadata qualification executed; neither source currently qualifies the
state-specific expression comparison.** Gupta remains the preferred conditional
source. Wigerblad is the sole checked fallback. Selection did not use target
outcomes, and the state requirement was not silently removed.

## Source identity, preparation and unit joins

| Source | Verified identity/version and preparation | What the unit map does and does not establish |
| --- | --- | --- |
| **Gupta2020**, [primary DOI](https://doi.org/10.1073/pnas.2003603117) | [GSE145231](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145231) explicitly lists GSE145230 as a subseries, and [GSE145230](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145230) reciprocally names the parent. Both records last updated 18 November 2025. The seven single-cell records are GSM4308702–GSM4308708, whole-blood leukocytes after RBC depletion, not PBMCs or purified-neutrophil capture. GEO specifies Cell Ranger 3.0.0/3.0.2, raw feature/barcode matrices, Seurat 3.0 and GRCh38. | Seven GEO samples join to seven BioSample, experiment and run records. Source metadata give three male and four female sample labels plus experimental/lab IDs; individual ages and explicit participant crosswalk are absent. Source-record dates and embedded lab-ID strings are not collection/processing timestamps. GSE145033, identified by the paper as cohort 2, was not substituted for the single-cell source. |
| **Wigerblad2022**, [primary DOI](https://doi.org/10.4049/jimmunol.2200154) | [GSE188288](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE188288), last updated 30 September 2026, contains nineteen sample records, GSM5676972–GSM5676990. The map retains granulocyte-gradient, immunomagnetically purified-neutrophil and RBC-depleted whole-blood contexts. GEO specifies 10x 3′ 3.1 chemistry, Cell Ranger 4.0, Seurat 4.0 and GRCh38. | Nineteen samples join to nineteen BioSample, experiment and run records, with supplied sex/age attributes. Repeated title tokens such as F1 or M3 are unverified cross-preparation donor clues, not established pairing. The publication reports seven unrelated donors for its purified-neutrophil analysis; the HC1–HC7-to-GSM and across-preparation participant crosswalk is still unavailable. |

Exact [series relations](../../../analysis/research/runs/Yd1_extension_c_v1/series_relations.csv),
[sample/library/preparation map](../../../analysis/research/runs/Yd1_extension_c_v1/sample_library_map.csv),
[BioSample attributes](../../../analysis/research/runs/Yd1_extension_c_v1/biosample_attributes.csv)
and [SRA run map](../../../analysis/research/runs/Yd1_extension_c_v1/sequencing_run_map.csv)
preserve the individual identifiers and supplied fields. **Fresh/frozen handling,
collection time and elapsed processing time are not explicitly supplied in the
inspected sample/BioSample fields**. No assumption of fresh material was added.

The [Gupta primary indexed Results](https://pmc.ncbi.nlm.nih.gov/articles/PMC7368314/),
“Enhanced Type I IFN Signature…” / Fig. 2 and “IFN Signature…Distinct Subset” /
Fig. 3, identify seven whole-blood volunteers and neutrophil subsets numbered
0–3. Sex-prefixed presentations do not resolve the actual deposited barcode/state
field or establish a cross-sex label mapping.

The [Wigerblad primary indexed Methods/Results](https://pmc.ncbi.nlm.nih.gov/articles/PMC9712146/),
“Cell purification,” “A modified analysis pipeline…” and Fig. 2E–F, distinguish
raw from called cells and report Nh0–Nh3 in purified neutrophils. Those names are
publication provenance only. They were not transferred to granulocyte or
whole-blood libraries, aligned with Gupta states, or treated as measured lineage.

## Feature coverage, file sizes and the missing denominator

The [complete file inventory](../../../analysis/research/runs/Yd1_extension_c_v1/file_inventory.csv)
records **42 listed files/archives**, their exact bytes and acquisition status.
Only the seven separate Gupta gene-feature files were acquired: 270,606 bytes
for each listed male file and 270,608 bytes for each listed female file.
The Gupta archive is 319,293,440 bytes; Wigerblad's is 1,003,325,440 bytes.
Neither archive, any expression matrix/H5, raw sequencing read or large raw
barcode list was downloaded. The 19 Wigerblad H5 file sizes are retained in the
inventory; they were not opened even for embedded feature metadata.

[Target feature support](../../../analysis/research/runs/Yd1_extension_c_v1/target_feature_support.csv)
shows, in each of seven **33,538-feature** Gupta references:

| Target | Exact reference entry | One-based feature row | Meaning |
| --- | --- | ---: | --- |
| ARG1 | ENSG00000118520, Gene Expression | 11,428 | One reference entry; no transcript values inspected |
| IL6R | ENSG00000160712, Gene Expression | 1,971 | One reference entry; no transcript values inspected |

This addresses reference membership only. It does not establish detection,
biological absence, protein abundance or equivalent sensitivity across sources.
Wigerblad target coverage remains unknown because no separate small feature
export was found in its inspected GEO listing.

The [26-row retention/state/denominator ledger](../../../analysis/research/runs/Yd1_extension_c_v1/state_denominator_coverage.csv)
preserves unknown fields as blank:

- **Gupta:** GEO explicitly describes raw feature/barcode matrices. The large raw
  barcode lists are not evidence of author-retained cells. No recovered export
  assigns retained neutrophils, exclusions or subset labels to barcodes, so
  neither an all-neutrophil nor a within-state target-zero denominator is known.
- **Wigerblad:** H5 matrices and publication state names do not supply an accessible
  retained-cell/state export. The paper's cell-calling distinction makes it
  especially unsafe to assume that default filtered barcodes reproduce the
  author's neutrophil population. No classifier or QC reconstruction was run.

No small cell/state export was identified in the **inspected GEO listings and
retrieved primary passages**. Complete paper/supplement access was unsuccessful;
absence from every possible author resource is not claimed. A marker table or
aggregate figure count would not replace a barcode-level export.

## Overlap and transport limits

The frozen metadata check found no shared BioSample, SRA-experiment or SRA-run
accession between these two deposits. **That does not establish distinct
participants or independent replication.** Gupta lab identifiers include F4/F5/M4,
while Wigerblad includes oF4/oF5/oM4 title tokens; these naming clues are retained
for a future crosswalk, not asserted to be the same people. Repeated tokens
within Wigerblad likewise do not establish paired preparations.

Both publications already contribute to SCAHN. Its Table S1 reports eighteen
Wigerblad samples, whereas GEO lists nineteen libraries; the actual inclusion
join is unresolved. The apparent count difference cannot identify an excluded
library. SCAHN-retained cells and its dataset-by-gene measurement mask remain
unjoined. No pooled study effect or independent atlas replication is proposed.

Gupta's RBC-depleted leukocyte context is closer to the nominated whole-blood
description than purified-cell capture, but processing and selection still
restrict transport. A Wigerblad purified-neutrophil fallback would describe that
specific isolation context, not whole-blood capture, IPF tissue neutrophils or
the nominated source–recipient coculture's function.

## One conditional Gupta description returned for review

The following is frozen as a **review proposal**, not an executable expression
contract. It remains held on the missing source qualifications above.
The unchanged question is how ARG1 and IL6R RNA descriptions vary across
author-defined neutrophil states within the qualified healthy-blood source.

| Design element | Exact proposal / hold |
| --- | --- |
| Unit and population | The seven reported source volunteers, with GSM/library/run nesting after the donor crosswalk is qualified. All author-retained neutrophils from RBC-depleted whole-blood leukocytes; no target-positive preselection. Without participant mapping, any reduced GSM-only description would require explicit review and could not be called an equally weighted donor analysis. |
| States | Author subsets 0, 1, 2, 3 only after actual retained-barcode/state-field and sex-label joins. Numbers are coding labels, not a maturation order; subset 0 is a reporting reference, not assumed biological rest. No new classifier, label transfer or merging with Nh/SCAHN labels. |
| Denominator | Every verified retained cell in a sample/state, including ARG1-zero and IL6R-zero cells. Preserve author exclusions and unmatched/ambiguous cells. Zero cells in a verified state means zero composition but undefined expression; missing metadata or feature support means unavailable. |
| Endpoints | ARG1 and IL6R separately: nonzero raw-count fraction and mean cell-level log1p counts per 10,000, retaining raw target counts and total RNA counts for audit. No protein/functional endpoint is inferred. |
| Normalization | For each retained cell, log1p(10,000 × raw target UMI / total UMI across all original RNA features). No restriction to the SCAHN gene set, imputation, integration or new expression-dependent filtering. Positive total counts must follow from the qualified retained-cell definition. |
| Comparisons and weighting | Per-donor state 1–0, 2–0 and 3–0 descriptions, separately by target/metric. Equal donor weights only with all seven mapped donors supporting both states; otherwise retain every available donor summary and hold the combined contrast. No cell weighting, tests or confidence intervals. The complete-support rule is a reporting rule, not a precision/power claim. |
| Sex, time and preparation | Retain supplied sex as annotation; no new inferential sex effect or adjustment model. Unknown freshness/timing remains explicit. No cross-preparation contrast without actual paired-donor evidence. |
| Exposure/independence | Published source outcomes and state descriptions, prior Yadav/SCAHN evidence and current metadata are exposed. No target-expression values were queried or calculated in C. Reuse is not replication; do not pool Gupta with the fallback. |
| Interpretation | Observational RNA/state/capture descriptions only; no secretion, receptor competence, suppressive function, lineage equivalence, source ARG1 activity or IPF repair claim. |

A reduced **unstratified** neutrophil question is not adopted. It would still need
an author-retained neutrophil list and a complete target-zero denominator, then
explicit scope review. Mixed whole-blood cell averages would answer a different
question. Thus dropping states alone does not remove the present hold.

## Exact reopening requirements and verification

**Gupta:** recover a small barcode → retained/excluded → neutrophil identity →
author-state export, with source sample and state/sex mappings; qualify the
participant/GSM and preparation/timing context; then freeze a reviewed numerical
design and resource plan. Original feature identities are now qualified.

**Wigerblad fallback:** recover a separate feature reference and exact
retained-cell/state/sample export, HC/GSM and cross-preparation donor joins, plus
the SCAHN subset inclusion if atlas comparison is intended. Name the chosen
purified, granulocyte or whole-blood context explicitly. No source was selected
because of an ARG1/IL6R outcome.

[Contract](config/c_contract_v1.json), [specification](config/checkpoint_c_spec_v1.json)
and code froze at `68bbfe582039d9bb1007cc4a78b106ef40355379`.
The [receipt](../../../analysis/research/runs/Yd1_extension_c_v1/receipt.json)
records execution and all eight output hashes.
Independent verification checked all 26 sample joins, 26 sequencing-run rows,
52 target-support rows (14 with source feature files), 42 listed file sizes and
preservation of unknown denominators. No scientific acceptance is implied.

The preserved ignored cache `raw_data/Yd1_checkpoint_c_20261031/` contains all
53 hash-bound inputs, direct retrieval receipts and exact source-access/query
scope. PMC web routes challenged; Wigerblad's publisher PDF route returned a
loading page; BioC returned an error page for Gupta and HTTP 429 for Wigerblad.
No challenge was bypassed or failed content called a complete paper read.
Primary indexed sections were read; unrelated search hits were discarded.
No other atlas study, expression input, raw read, new classifier or outreach was
used. [Literature context](LITERATURE_CONTEXT.md) and the
[execution ledger](EXECUTION_LEDGER.md) distinguish these reads from unresolved
source work.

X0–X2 remain reviewed complete in their descriptive scope. X3's author-object
reader/state hold and X4's culture/native/stage holds remain unchanged. X5 now has
specific two-lead eligibility holds; the [X6 matrix](PROVISIONAL_X6_MATRIX.md) is
updated only with that source status and remains provisional. Checkpoint C is
returned for technical review, not final scientific or extension acceptance.
