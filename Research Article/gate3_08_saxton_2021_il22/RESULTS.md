# Saxton saved-evidence recovery results

31 October 2026 (Asia/Seoul). **The bounded recovery is complete; the original
biological sequence is not.** This is a documentation and data-integrity review
of article-local **Sx22-P01**, governed by [RECOVERY_SCOPE](RECOVERY_SCOPE_2026-10-31.md).
[Stage dispositions](COMPLETION_LEDGER.md) · [R1 verification](R1_REVIEW.md) ·
[Source corrections](SOURCE_CORRECTION_2026-10-31.md) ·
[E1/E2 source feasibility](SOURCE_FEASIBILITY.md) · [Evidence index](FIGURES.md) ·
[Checks and handoff](VALIDATION.md).

## What was verified

The immutable R1 metadata/QC run at `ff09fab3fb37fd4bf915845e5cd59effaa386210`
passes independent input/code/output hashing, format, dimensions, annotation,
identifier, per-library arithmetic and sample-join checks. All eight run files
match the original technical and review checkouts byte-for-byte. The three raw
inputs match the receipt in both source caches and the new exclusive copies.
No original analysis entrypoint was rerun.

The count and FPKM tables each contain **35,275 gene rows and six sample columns**,
with nine matching annotation columns. Counts are nonnegative integers; all FPKM
values are finite and nonnegative. There are no duplicate deposited Ensembl IDs,
**52 distinct repeated nonempty symbol labels spanning 122 gene rows**, and
**12,935 rows with zero counts in every library**. These are technical diagnostics;
no treatment effect, biological program score, exclusion or biological outlier
judgment was calculated.

GEO titles, treatment attributes and BioSample links agree with all six saved
sample records. Source methods report two independent biological RNA samples per
group, but the deposit supplies no separate animal key or batch map. Distinct
BioSamples and distinct count vectors do not verify distinct animals. The saved
`paired=no` is interpreted as **no pairing established or used**, not evidence
that the animals are proven unpaired. The exact annotation release remains unknown.
The receipt's original `verification=pending` and `scientific_acceptance=not_assessed`
fields remain unchanged; this separate report records the later mechanical review.

## Documentary findings and remaining limits

The supplied final PDF places receptor qPCR in **Figure 5H**; **5F/G** are labeled
HepG2 immunoblots and **5I** is the receptor-expression comparison by immunoblot.
The caption's F and G/H references conflict with those visible panels. In Figure 7,
the image and main text identify **G as liver and H as skin**, while the continued
caption reverses them. These source-location findings supersede the corresponding
entries of the unchanged [historical audit](SOURCE_AUDIT.md). They do not resolve
raw sample identities or authorize numerical reconstruction.

E1's selected existing injury cohort has pooled libraries and time labels, without
an animal-resolved IL-22 response or linked functional endpoint. E2's published
withdrawal precedent supplies a source-level receptor-transcript observation;
its uninspected supplements and datasets are **not assessed**, not declared absent.
Existing A14/A19 linkage holds remain specific to their documented questions.

R0/R1 and the permitted source portions of R4/R5/E1/E2 are reviewed. R2/R3 have a
**platform-policy execution hold**, despite recovered counts. R4/R5 numerical work
also retains raw-value, replicate/nesting and panel-identity qualifications.
D1's results, evidence index and complete disposition ledger are delivered for the
originating chat's independent review. No canonical RQ, hypothesis, claim grade,
human acceptance, governance rule or external setting is changed.
