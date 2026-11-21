# Qualified human-cell context — frozen descriptive scope

10 November 2026. The source-qualification stage executed at `557eb98` and
qualified GSE318914 (72 libraries) and GSE318915 (36 libraries), each with
19,984 deposited genes and explicit sample/library links. Each series reports
three donor labels; these are not assumed to identify the same people across
series. The question is the direction and donor consistency of a fixed RNA
panel under the four deposited treatments, in each observed context and time.

The [follow-up plan](PLAN.md) prespecified STAT3, SOCS3, TNF, IFNG and GZMB before
expression description. Every supplied condition, donor and time is retained.
Matched contrasts are IL-10–PBS, IL-10-Fc–PBS, agonist–PBS and agonist–IL-10.
Report raw counts, CPM over **all deposited gene rows**, log2(CPM+1), every
donor-paired difference, and the median/range and sign count across three
reported donors. Range is a description, not a confidence interval.

One figure shows all five markers and all contrasts as median-difference
heatmaps; a second displays every donor's IFNG/GZMB differences. The complete
tables retain all five genes. This display choice is frozen before the stage,
not selected from a favorable result. Both figures are saved as PNG and SVG.

Verification independently sums the matrices with NumPy against the earlier
streamed library totals, reconstructs normalized values with scalar math,
checks paired differences using a log-ratio identity, and checks medians by
ordered donor values. Any disagreement or incomplete pair stops execution.

No DE model, P value, interval, gene-set optimization, cross-series donor join
or comparison to mouse pool means is permitted. CPM is compositional and
depends on the deposited feature universe. PBMCs are a cell mixture; RNA cannot
identify secretion, microglial function, tissue repair or cognition. The new
agonist is not D25K. The study's published selectivity claim is already exposed;
this is a bounded description, not confirmation or independent reproduction of
Navarro's aged-brain intervention.
