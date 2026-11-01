# Source-readiness extension results

31 October 2026 (Asia/Seoul). **X1/X2 executed and independently checked; X3
documentary qualification completed at the inspected coverage.** The owner remains
Sx22-P01. These exposed metadata/source reviews do not estimate treatment effects,
qualify a new biological experiment or lift any prior execution hold.
[Plan and dispositions](README.md) · [Source/access manifest](SOURCE_MANIFEST.md) ·
[Companion endpoint review](X3_SOURCE_LINKAGE.md) · [Validation](VALIDATION.md).

## X1: deposited annotation ambiguity

Purpose: characterize the identifier ambiguity counted by R1. Unit: deposited
annotation row, not an animal. Endpoint: identity/multiplicity and annotation-field
consistency. Main validity threat: equating a shared symbol with a single gene
record. The [frozen X1 contract](config/x1_contract_v1.json) was committed at
`1f7b0d54a66e821039ff09ef103d2c1fab04af60` before the
[immutable run](../../../analysis/research/runs/sx22_x1_annotation_v1/receipt.json).

The script projects **only nine annotation fields**; it does not select, convert,
sum or score expression columns. The [annotation output](../../../analysis/research/runs/sx22_x1_annotation_v1/annotations.csv)
retains all 35,275 source rows in their original order. All selected values agree
between the read-count and FPKM representations. There are no empty selected
fields, repeated deposited/stable IDs, version-suffixed IDs, nonstandard ID forms,
or detected coordinate/strand syntax issues. These checks establish internal
consistency, not annotation accuracy against a current external genome release.

The [52 repeated symbols](../../../analysis/research/runs/sx22_x1_annotation_v1/repeated_symbols.csv)
span 122 rows: 48 labels occur twice, three occur three times, and one occurs
17 times. Every repeated label maps to multiple distinct stable IDs. Within each
label, all rows share a chromosome; 51 labels have more than one deposited
chromosome/strand/start/end tuple, four span strand labels, 18 span biotypes and
23 span descriptions. These categories overlap and are not alternative bins.
The table is alphabetically ordered as an identifier inventory, not a priority list.
Full definitions and counts are in the [summary](../../../analysis/research/runs/sx22_x1_annotation_v1/summary.json).

**Implication:** a symbol alone is not a unique row key in this deposit. Version
suffix removal cannot resolve these particular collisions because no suffixes
are present. No symbol was collapsed, representative row selected or mapping
guessed. The source's mm10 label does not identify the exact annotation release;
external annotation reconciliation remains unassessed. No biological target,
receptor response or expression effect follows from these metadata findings.

## X2: all-six-sample source provenance

Purpose: determine whether the previously uninspected sample records add unit or
technical-run keys. Unit: public metadata record; the animal/preparation remains
source-reported and unverified. Main threat: treating database identifiers as
independent animals. The [frozen X2 contract](config/x2_contract_v1.json) used the
same pre-execution commit and has its own [receipt](../../../analysis/research/runs/sx22_x2_provenance_v1/receipt.json).

| GEO / column | BioSample | SRA sample | Experiment | Run |
|---|---|---|---|---|
| GSM4869228 / PBS_1 | SAMN16563502 | SRS7594489 | SRX9372917 | SRR12908235 |
| GSM4869229 / PBS_2 | SAMN16563631 | SRS7594490 | SRX9372918 | SRR12908236 |
| GSM4869230 / LH5_1 | SAMN16563630 | SRS7594491 | SRX9372919 | SRR12908237 |
| GSM4869231 / LH5_2 | SAMN16563629 | SRS7594492 | SRX9372920 | SRR12908238 |
| GSM4869232 / LH30_1 | SAMN16563628 | SRS7594493 | SRX9372921 | SRR12908239 |
| GSM4869233 / LH30_2 | SAMN16563627 | SRS7594494 | SRX9372922 | SRR12908240 |

All forward/reverse sample, experiment, run and member links agree with the reused
GEO SOFT records. Treatment/title attributes agree as well. Every sample has one
public run in the returned packages. [Exact crosswalk](../../../analysis/research/runs/sx22_x2_provenance_v1/sample_provenance.csv),
[field inventory](../../../analysis/research/runs/sx22_x2_provenance_v1/field_inventory.csv),
[record metadata](../../../analysis/research/runs/sx22_x2_provenance_v1/record_metadata.json)
and [access metadata](../../../analysis/research/runs/sx22_x2_provenance_v1/source_access.json)
retain the evidence.

BioSample and SRA sample attributes contain source name, tissue, strain and
treatment. They add no explicit animal ID, preparation, pool composition, batch,
sex or allocation key. SRA experiment attributes identify GEO accessions;
design-description fields are empty and run-attribute lists contain no added
unit fields. The same instrument/model and submission are technical provenance,
not a biological or processing-batch map. An AI documentary check of the linked
titles, descriptions and protocol/processing fields found no additional unit
crosswalk. This is distinct from human source verification or scientific acceptance;
the automated summary's caution about narrative review remains visible.

`PAIRED` is the **sequencing layout**, not paired animals. SRA `Pool/Member`
contains one database sample member per run here; it establishes neither pooled
animals nor the absence of animal pooling. The aliases ending `_r1` are run labels,
not additional biological replicates. No sequence/read files were requested or
downloaded by X2. The paper's n=2/group report remains a source statement; animal
independence, pairing, allocation and batch remain unknown.

## X3: withdrawal-source linkage

The advertised supplement is now directly inspected at **PDF pp. 23–24,
Figure S5e and its caption**. The figure supplies time-after-withdrawal labels
and a normalized qPCR transcript endpoint, while the caption reports two
independent experiments. It does not identify a mouse/preparation per observation,
the biological versus technical replication at each time, or a join to later
functional recovery. The separate six-mice-per-genotype statement for S5c/d
must not be assigned to S5e.

The [detailed source review](X3_SOURCE_LINKAGE.md) records the nominal cessation
and passaging labels, endpoint scale, missing keys, reporting-summary coverage,
workbook index and uninspected items. No point values, effects, decay rates or
functional estimates were extracted. The earlier "supplement not assessed"
status is superseded only for these named materials and locators.

## What these extensions change

Annotation and public-record identity are more explicit, and the companion's
withdrawal panel can now be located and described directly. They do not establish
independent replication, treatment selectivity, persistent memory or repair.
These findings support precise source-readiness decisions: retain record-level
annotation keys, retain unknown animal relationships, and keep transcript time
labels separate from measured cessation and linked function. They do not nominate
new targets or experimental conditions.

R2/R3 retain their **platform-policy execution holds** despite available counts.
Numerical R4/R5 and E1/E2 also remain outside this task, with their existing
source/design limits. No canonical RQ, hypothesis, claim grade, governance rule,
root attribute or R1 artifact changed. The original recovery ledger remains
historical. Technical completion here does not create human acceptance.
