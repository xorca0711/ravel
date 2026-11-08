# Metadata v3 amendment — 8 November 2026

V2 parsed and retained all file/description differences but failed the independent
check expecting the five snRNA discrepancies exposed after v1. The complete audit
identified a sixth discrepancy: **GSM9226083**, GSE307529 WES, has explicit Library
name `P6_AAH` and a deposited title identifying AAH, while its supplementary VCF
filename is `GSM9226083_P6_AIS.WES.PASS.recode.vcf.gz`.

Unlike the five snRNA punctuation differences, this changes a histology token.
V3 must retain both labels and flag a **file identity hold** for this WES record
and its two cross-platform alias correspondences. It does not choose between
AAH and AIS, rename the VCF, infer lesion identity or use genomic content to
settle the dispute. Author/source clarification is required before interpreting
that VCF or using it in a tissue-level join. Other metadata records remain eligible.

The independently implemented verifier now requires all six disagreements,
exact verbatim strings, complete issue reporting, the five separate punctuation
flags, the P6-specific hold and propagation of that hold to the affected joins.
The previously verified raw counts, fields, C3 coverage and unknown-ID checks
remain. This is a prospective amendment after new metadata exposure, not a
relaxation of repository governance or an assertion of source consistency.

V1 and v2 remain failed. V3 declares byte-identical archives of every file from
both attempts, including their failed receipts and partial outputs. Originals
stay local, unmodified; only after archive verification may their original paths
be ignored. Frozen contracts and scripts remain registered and unchanged.

The metadata purpose, biological unit and interpretation boundaries are unchanged.
No author contact, new scientific acceptance or downstream A12 estimate is implied.
