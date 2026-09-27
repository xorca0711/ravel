# A13 coverage: the gate is not met, and the reason is definitional

27 September 2026. Counts only, under
[`config/a13_triad_coverage_spec.json`](../config/a13_triad_coverage_spec.json). Nothing is
fitted, no association is estimated and no claim row is added. Every number comes from
[`tables/`](../tables/) and the [run record](../tables/a13_coverage_run.json).

## Verdict

**Zero patients in the Kim lung adenocarcinoma cohort hold a complete paired triad at the
declared floor, against a ten-patient requirement, and the cause is that the deposit labels
no tumour-sample epithelium as type 2 at all.** Under a wider epithelial definition the count
is three, still far below the floor, and the binding constraint moves to fibroblast capture.

## The instrument reproduces

The script reproduces all 240 per-donor flags the earlier trial recorded, across both IPF
cohorts and all three floors, before reporting anything new. At the 50-cell floor it recovers
the numbers the A13 card quotes: GSE136831 gives two IPF and four control donors, GSE135893
gives two IPF and one control, which are the six and three the card names.

Getting there required recovering a rule the earlier artefact did not state. The first run
assumed a compartment met the floor when its labels summed to it, reproduced 230 of 240 flags
and refused to report any new count. Every disagreement ran one way, and the pattern gave the
rule away: a donor with 26 Fibroblast and 14 Myofibroblast cells fails a 30-cell floor in the
earlier trial but passes when pooled. **The earlier gate required one single cell label to
reach the floor.** That rule reproduces all 240 flags, so it is the primary here, and pooling
is reported beside it as a sensitivity. The refused attempt is preserved in
[`tables/attempt1_refused_pooled_rule/`](../tables/attempt1_refused_pooled_rule/).

## The Kim cohort, counted for the first time

Twenty-two lung samples, eleven tumour and eleven normal, giving ten patients with both. Per
sample, at the 50-cell floor, under the type 2 epithelial definition the two IPF cohorts use:

| Compartment | Median cells per sample | Samples at or above 50 |
|---|--:|--:|
| Type 2 epithelium | 36 | 11 of 22 |
| Largest fibroblast label | 32.5 | 10 of 22 |
| Largest macrophage label | 723 | 22 of 22 |

| Epithelial definition | Rule | Complete paired triads at floors 30, 50, 100 |
|---|---|---|
| Type 2 only, primary | single label | 0, 0, 0 |
| Type 2 only, primary | pooled | 0, 0, 0 |
| Type 2 plus tumour states, sensitivity | single label | 4, 3, 1 |
| Type 2 plus tumour states, sensitivity | pooled | 4, 3, 1 |

## Why the primary count is zero, and why that matters

**Every one of the eleven tumour samples holds exactly zero cells labelled type 2.** The
deposit annotates tumour-sample epithelium as its tumour states instead. So under an
epithelial compartment defined as type 2, a tumour sample can never hold an epithelial
compartment, and no patient can ever hold a complete paired triad. The zero is a property of
the annotation, not a shortage of cells.

That is worth stating plainly because it is the kind of result a power calculation would miss.
A13's paired contrast and a type 2 epithelial compartment are incompatible in this deposit,
whatever the cohort size. Any future attempt has to choose: keep the type 2 definition and
abandon the paired tumour-versus-normal contrast, or keep the contrast and define the
epithelial compartment to include the tumour states, which is no longer the same compartment
the two IPF cohorts used and so is not comparable with the six and three the gate quotes.

## Under the wider definition, fibroblasts bind

Admitting the tumour states lifts the count to three patients at the 50-cell floor. The limit
is then fibroblast capture: the largest fibroblast label reaches 50 cells in only ten of
twenty-two samples, with a median of 32.5. Pooling the three fibroblast labels does not change
the count, so this is scarcity rather than label fragmentation.

**This generalises beyond the cohort, and it is the useful part of the pass.** A13's gate is
bound by how many fibroblasts a lung single-cell library recovers per patient, which is a
property of the assay rather than of the cohort. A deposit with more patients does not help
if fibroblasts remain a low single-digit percentage of recovered cells. The two candidates the
[register gate audit](../../../docs/audits/2026-09-27-register-gate-audit/REPORT.md) named for
A13, GSE233844 and GSE122960, are larger but face the same constraint, and counting them would
need their per-patient annotation rather than a sample count.

## What this establishes and what it does not

**Establishes.** That the Kim cohort supplies no complete paired triad under the definition
consistent with the gate, and three under a wider one, both far below the ten-patient floor.
That the reason for the zero is definitional. And that the earlier trial's triad rule is
label-level, now reconstructed and reproduced exactly.

**Does not establish.** Anything about whether fibroblast programmes carry information beyond
macrophage interleukin-1 beta. No model was fitted and none should be, on this coverage.

**Does not change A13's grade or add a row.** The card already says coverage is next and not
mediation fitting, and this is that coverage.

## Proposed wording, not graded here

1. **Not established, with the constraint named.** In GSE131907, zero of ten
   tumour-normal patient pairs hold a complete macrophage, fibroblast and type 2 epithelial
   triad at a 50-cell floor, because no tumour sample carries a type 2 label; admitting the
   tumour epithelial states gives three, against a ten-patient joint-model floor.
2. **Descriptive, and reusable.** A13's coverage is bound by fibroblast recovery per patient,
   with the largest fibroblast label reaching 50 cells in 10 of 22 lung samples and a median
   of 32, so cohort size alone does not open the gate.

## What would open the gate

A cohort with deliberate mesenchymal enrichment, or a sorted fibroblast fraction paired with
unsorted myeloid and epithelial fractions from the same patients. Failing that, A13 should be
re-specified around a contrast that does not need all three compartments at depth in the same
patient, or retired. That is the owner's decision, not this pass.
