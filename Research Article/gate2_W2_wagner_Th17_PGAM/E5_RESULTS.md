# Wp-E5 result: candidate datasets exist, and none is yet admissible

Executed 5 October 2026 under the governed runner. Contract
[config/e5_external_screen_v1.json](config/e5_external_screen_v1.json),
entrypoint [scripts/e5_external_screen_v1.py](scripts/e5_external_screen_v1.py),
receipt
[analysis/research/runs/wp_e5_external_screen_v1/receipt.json](../../analysis/research/runs/wp_e5_external_screen_v1/receipt.json).
`verify` returned `{"ok": true, "errors": []}`.

**This is an eligibility screen, not an analysis.** No expression value was
read. The branch card requires the inclusion rule to be written before any
candidate is opened, so the rule is in the entrypoint docstring and in the
contract, and the screen defers rather than passes.

## What it would test

[Wp-R1](R1_RESULTS.md)'s strongest reproduced finding — the pro-regulatory arm
falls at low glucose, 4 of 4 animal-paired comparisons — rests on **two mice**.
That is the result most in need of an independent dataset, and the least able to
support one on its own.

## The frozen rule

| | Requirement |
|---|---|
| R1 | CD4 T cells polarised toward Th17, or a Th17-containing CD4 population, mouse or human |
| R2 | An explicit **nutrient** contrast within the experiment — a drug-only perturbation does not count, because the Wp-R1 finding is about nutrient level |
| R3 | Deposited expression values, not a figure or summary table only |
| R4 | At least two biological units per arm (animal, donor or verified independent culture) |
| R5 | The nutrient contrast crossed with, or held constant across, the Th17 polarisation condition |
| R6 | Independent of GSE289733, GSE290297 and GSE138266 |

Only R1, R2, R6 and a weak sample-count form of R4 can be decided from a GEO
summary. R3, R5 and the biological-unit form of R4 need the sample records and
the file list, so surviving candidates are marked `needs_record_inspection` —
**never passed**. A screen that guesses is worse than one that defers.

## Result

Six fixed queries over GEO DataSets returned **114 unique series**. 64 failed a
record-level rule; **50 survive to record inspection**, and none passes.

A limitation of the frozen term list was visible in the output and is reported
rather than fixed, because the rule was frozen: `media` and `medium` are generic
culture words that match any Methods sentence. Stratifying the shortlist on that
basis — a declared post-hoc split, not a rule change — 11 of the 50 matched only
those generic words and are almost certainly false positives. The strongest
remaining candidates, by closeness to the Wp-R1 design:

| Accession | Organism | Samples | Why it is a candidate |
|---|---|---|---|
| **GSE166430** | mouse | 6 | "TH17 cells cultured in the presence or absence of glutamine" — a nutrient contrast in the polarised population, the closest design match found |
| GSE143320 / GSE143321 | mouse | 6 each | methionine restriction shaping T helper responses; nutrient restriction, but methionine not glucose |
| GSE129028 | mouse | 24 | glycosylation and IL-2 signalling in Th17 differentiation, with 2-deoxyglucose |
| GSE222878 / GSE222880 / GSE222881 | mouse | 10 / 6 / 16 | pyruvate dehydrogenase and the citrate pool in Th17; metabolic but likely genetic rather than nutrient |
| GSE156742 / GSE207601 / GSE207602 | mouse | 8 / 12 / 6 | LKB1–mitochondria axis in Th17 effector function |
| GSE185478 | mouse | 6 | OXPHOS and persistence in Th17 cells, glutamine mentioned |
| GSE127768 | mouse | 20 | glycolysis inhibition in pathogenic Th17 via miR-21 |

Two notes on what these are likely to fail. Several are **drug or genetic**
perturbations of metabolism rather than nutrient contrasts, which fails R2 — the
distinction matters because the Wp-R1 result is about nutrient level, and an
inhibitor contrast is the design Wp-R3 already covers. And most are six to
twelve samples across several conditions, so R4's two-biological-units-per-arm
requirement will be tight.

GSE166430 is the one whose title states a nutrient contrast in the polarised
population directly. It is a six-sample microarray series, so R3 and R4 decide
it, and neither is decidable from the summary.

## What this settles

The route is **open but not yet usable**. Before any external comparison,
a successor contract must inspect the records of the named candidates against
R3, R4 and R5 and record the outcome — including the outcome that none
qualifies. Until then the Wp-R1 glucose finding stands on two mice, and must be
described that way.

## Limits

- A metadata screen over GEO summaries. It cannot establish that an admissible
  dataset exists, only that candidates do or do not survive record-level rules.
- The search is not exhaustive: six declared queries, not the archive.
- A summary that omits a nutrient contrast does not prove the experiment lacked
  one, so the 64 record-level failures include an unknown number of false
  negatives.
- The generic-term stratification is post-hoc and is labelled as such.
- No candidate may enter the Wp-R1 comparison on the strength of this screen.
