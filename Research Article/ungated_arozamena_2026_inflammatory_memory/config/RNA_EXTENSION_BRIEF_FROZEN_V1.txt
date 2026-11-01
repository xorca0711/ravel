# Arz1-P01: prospective deposited-library RNA extension

1 November 2026. Originating review of source checkpoint `fe719b1` authorizes
Q3a and Q5a below after a separate committed numerical contract and tests. The
original within-state Q3 remains held. Published outcomes and metadata have been
read; no new expression contrast has been inspected. This is an outcome-exposed,
shared-source descriptive reproduction, not independent replication or a new
canonical RQ. [Source qualification](SOURCE_QUALIFICATION.md) and
[literature context](LITERATURE_CONTEXT.md) govern interpretation.

## Biological question and competing explanations

Do the paper's reported inflammatory RNA directions recur in each deposited
post-injury/control comparison, and how much do barcode-depth weighting and
source-derived RNA-only QC change that description? The observational unit is a
deposited library, describing its finite sampled barcodes. Sorting, lineage,
genotype, cell composition and processing can explain apparent differences;
agreement cannot distinguish these from persistent within-state expression.
No cell-based p-values, FDR, confidence intervals, donor inference or population
replication counts are authorized. No RNA score identifies signaling or memory.

## Fixed comparisons and feature mapping

Keep four contrasts separate: GSE302685 irradiated minus its control;
GSE302687 irradiated minus its control; GSE329778 LGR5 minus CTRL; and GSE329778
KRT20 minus CTRL. Label accession and deposited lineage context. Preserve the
article/GEO run-number and sorting disagreements. The latter two contrasts reuse
one control and are not independent replications. Do not average across controls.

Report all 31,950 shared stable RNA IDs. Map symbols explicitly from all seven
sources; any inconsistent/ambiguous selected-symbol match is a local hold, not a
guessed alias. The source-selected panel is Cd74, Reg3g, Reg3b, H2-D1, App, Lgals9,
Mif and Ifitm3, from Results Sec5 / Figure 3j (Reg3 gamma/beta translated to the
canonical mouse symbols only if source feature records agree). These targets were
selected by the paper, not by new outcomes. Do not infer a pathway-wide response
from the panel. No extra gene-set expansion is required for this bounded question.

## Endpoint and bounded sensitivity family

For each library and barcode, RNA depth is the sum over **all its source RNA
features**, including genes outside the common reporting universe. ATAC entries
never enter RNA denominators. Detection is the number of RNA features with a
positive count. Zero-depth barcodes have undefined relative expression; enumerate
them and exclude them only where normalization requires positive RNA depth.

Primary: all deposited filtered-matrix barcodes, positive RNA depth. For gene g,
pooled CPM = 1e6 * sum(count_g) / sum(all RNA counts), then log2(CPM + 1).
Equal-barcode sensitivity: average [1e6 * count_g / barcode RNA depth] over the
same barcodes, then log2(mean CPM + 1). This changes depth weighting while keeping
the transformation and units fixed. A log2(CPM+1) difference is a descriptive
transformed-expression contrast, not an unqualified fold change.

Second sensitivity: apply the RNA subset of Methods Sec26 QC to the same deposited
barcodes: 200 <= detected RNA genes <= 2500, RNA counts >= 500, mitochondrial
fraction <= 0.40. Use all source RNA features for these quantities. Verify source
mitochondrial annotation before using it; if only a naming convention is available,
report that operational definition explicitly and its limit. If annotation is
ambiguous, retain the unfiltered two weighting cases and hold this QC sensitivity
with the precise reason. Apply both pooled and equal-barcode summaries to the
RNA-QC subset, giving at most four fixed cases. Empty retained sets yield undefined
endpoints and a local hold. This is an RNA-only adaptation, not the author's full
joint ATAC/RNA QC, integrated Seurat pipeline or ISC-specific analysis.

Retain complete gene/contrast/case tables, panel mappings, each library's barcode
counts and depth/QC summaries, denominators, undefined values and source hashes.
Describe selected-panel medians and direction counts by contrast and case;
report zero changes explicitly. Do not aggregate the four contrasts into one
effect or treat retained cells as independent animals. Retain negative/mixed
results. No outcome-adaptive thresholds, targets or extra cases.

## Implementation, review and figures

Use existing sparse/streaming Python runtime. Do not materialize a dense full
multiome matrix. Freeze code, input hashes, this brief and contract before execution
through the research runner. Tests must discriminate all-source denominators from
common-gene denominators, weighting effects from log-transform effects, QC boundary
behavior, zero-depth/empty subsets, explicit mappings and sparse accumulation.
Preserve prior metadata/source bytes and runs. Corrections use a new version.

Produce at most two substantive figure families: four accession-specific selected
target contrasts, and their weighting/RNA-QC sensitivity. Use signed changes and
clear unit/case labels; no significance markers. Save numerical plotting inputs
and PNG/SVG outputs. Actual files receive originating numerical and visual review
before gallery integration. Technical execution is not scientific acceptance.

## Separate Q4a feasibility assessment

GSE329778 has three linked fragment files, about 1.71 GB compressed in total.
Assess their source metadata, coordinate/reference and barcode correspondence,
existing annotation availability, disk/runtime budget and a streamed common-feature
counting option. Source qualification may proceed alongside RNA work. Do not
perform a biological accessibility comparison or large download under this RNA
contract. A fixed-region, third-deposit-only extension would need a separate
reviewed estimand, source-qualified coordinates and freeze. Do not dismiss it
merely because all-seven-library Q4 is held; do not call it within-state analysis
or reconstruct missing first/second-deposit fragments. Report the concrete
feasibility decision and remaining evidence, without manufacturing a resource hold.
