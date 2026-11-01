# Preserved Q4a v1 source-identity hold

1 November 2026. Freeze `4f1a8f662d9409355aa5065388621c2c54ac1d8e` executed as
`arz1_accessibility_description_v1`. [Receipt](../../analysis/research/runs/arz1_accessibility_description_v1/receipt.json)
verification passed. Four loci qualified with exact M33/source TSS-span agreement
and no basic-transcript fallback; all three RNA depth/QC reconstructions passed.
All three fragment sources then stopped at the v1 coordinate/barcode duplicate
check. **No paired RNA/accessibility endpoint was released**: all 64 fixed rows
are held. This is source-format qualification, not an unfavorable biological effect.

The [source-validation record](../../analysis/research/runs/arz1_accessibility_description_v1/source_validation.json)
retains partial traversal diagnostics. The files did not reach full gzip EOF/CRC
validation in v1. Do not describe the acquired full hashes or matched prefixes as
completed numerical source validation. The held figure placeholders and all other
v1 artifacts remain immutable; they are not substantive result figures.

## Targeted literal source inspection

Only the offending prefix records were reread after the hold. Each repeated
coordinate/barcode key is a pair of opposite-strand rows:

| Library | Physical lines | Chromosome / start / end / barcode | readSupport / strand |
|---|---|---|---|
| CTRL | 5009, 5010 | chr1 / 3867681 / 3867706 / CCTTTAGTCGATTTGA-1 | 1 / + ; 2 / − |
| KRT20 | 26860, 26861 | chr1 / 5240827 / 5240888 / GTAATAGCATTAAGTC-1 | 2 / + ; 1 / − |
| LGR5 | 19538, 19539 | chr1 / 4607993 / 4608048 / CGTTAAATCGACAAAG-1 | 1 / + ; 1 / − |

These rows are distinct in the sixth field; v1 treated them as the same key.
The [ARC 2.1 algorithm overview](https://www.10xgenomics.com/support/software/cell-ranger-arc/2.1/algorithms-overview/algorithms-overview)
describes duplicate marking by start/end/hashed barcode and motivated that check.
The [ARC 2.1 fragment specification](https://www.10xgenomics.com/support/software/cell-ranger-arc/2.1/analysis/outputs/fragments-file)
and release notes describe the added strand-origin field. The observed deposited
representation does not satisfy the stronger strand-discarding uniqueness
assumption. Neither that conflict nor these three prefix examples establish that
the files are corrupted, that every such pair is a separate physical molecule,
or that every later source record is valid.

## Concrete amendment proposed for originating review

Preserve v1 and use a new committed v2 contract/run. Define a unique **deposited
strand-labelled fragment record** by chromosome/start/end/barcode/strand. Count
each such source record once, retaining readSupport solely as a validated source
field. Reject repeated keys even if readSupport differs. Enumerate coordinate/
barcode collisions across opposite strands separately, both overall and among
allowed canonical records; do not silently merge or remove either row.

This would qualify the deposited row representation while narrowing the counting
claim: distinct strand-labelled source records are not independently certified
physical molecules. Keep every other field/order/gzip/barcode/region/denominator
check, fixed locus, paired selection, normalization and comparison unchanged.
The fixed-region endpoint counts overlapping fragment records, whereas ARC's
deposited Peaks matrix counts cut sites. Neither version is exact peak-matrix
replay; the source matrix must not be used as a numerically equivalent count check.
Add a known-answer opposite-strand pair test and retain a same-strand repeated-key
failure test. Freeze the amendment after originating review and before renewed
counting. No accessibility outcome has been inspected, so the change addresses
source semantics rather than a favorable result. Full-source traversal may still
produce local holds; no such future failure is pre-excused.
