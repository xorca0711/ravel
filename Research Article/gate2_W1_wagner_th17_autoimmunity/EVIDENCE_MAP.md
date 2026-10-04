# Published evidence and reproduction targets

Source: [Wagner 2021](https://doi.org/10.1016/j.cell.2021.05.045), supplied
40-page annotated PDF. PDF page numbers below include the cover. These are
published observations, not new repository findings. The local annotated PDF
and extracted full text are not redistributed.

| Source locator | Published measurement | Reproduction product | Interpretation limit |
|---|---|---|---|
| Fig. 1; PDF pp. 3-4; STAR Methods pp. 26-30 | Network-constrained transcriptome support for high reaction flux | Verify model, gene/reaction rules, score direction and smoothing configuration | Potential activity is neither observed flux nor enzyme activity |
| Fig. 2B-E; PDF pp. 5-6; Tables S1-S3 | Metabolic heterogeneity, reaction contrasts and RNA correlations in Th17p/n | Recreate 2C/2E using author's outputs, then assess metareaction/source fidelity | Published cell-wise statistics do not establish independent-mouse precision; RNA-derived signatures are not independent functional outcomes |
| Fig. 3; PDF pp. 7-9 | Extracellular flux measurements, metabolite abundance, isotope labeling and lipid-related measurements | Recompute contrasts only if numerical source values and replicate maps are recovered | Metabolite pool size, fractional label and metabolic flux are different quantities; selective inhibitor readouts have specificity limits |
| Fig. 4; PDF pp. 8-10 | Reaction predictions plus enzymes, polyamine-related abundance and labeling | Reconcile direction, compartment, metabolite identity and assay-specific denominators | Arginine/ornithine/polyamines cannot be collapsed into a uniformly directed pathway |
| Fig. 5 and S5; PDF pp. 10-12 | Pharmacological/genetic perturbation, cytokines, transcription factors and rescue | Audit agreement and differences across perturbations, viability/proliferation and rescue endpoints | A lower effector readout can reflect state, growth or selection; ODC1 and SAT1 are not interchangeable perturbations |
| Fig. 6A-C and S6; PDF pp. 11-13; S4-S6 | Bulk RNA response toward a Treg-like profile | Reproduce source-defined gene partitions and within-lineage DFMO contrasts | Bulk shifts do not demonstrate individual-cell conversion or stable suppressive function |
| Fig. 6D-F; PDF pp. 11-13; S7 | ATAC accessibility and enrichment of externally annotated binding regions/motifs | Reproduce accessibility partitions, coordinate joins and annotation enrichment | Accessibility is not a histone mark; enrichment is not direct binding or a JMJD3 sequence motif |
| Fig. 6G-H and S6E-F; PDF pp. 11-13, 38-39 | JMJD3/DFMO effects on selected functional readouts and transcriptome programs | Estimate genotype-by-treatment contrasts separately by lineage and endpoint | Endpoint-specific dependence does not establish one universal linear epistasis pathway |
| Fig. 7; PDF pp. 14-15 | EAE course, recall response and tissue T-cell phenotypes | Reanalyze only recovered animal-level longitudinal/source data | Systemic drug and T-cell deletion differ in scope; CNS autoimmunity is not lung repair |

Numerical supplement tables S1-S7 and raw assay-level data have not been
acquired. Supplemental figures/legends embedded in the supplied PDF are available;
their presence does not establish availability of underlying measurements.
Paper-level reproduction is partial unless every claimed panel has an exact
source, transform, unit map and auditable numerical comparison.

The author [demo](https://yoseflab.github.io/Compass/notebooks/Demo.html)
targets 2C/2E, but its default single-reaction analysis differs from the paper's
metareaction analysis. Passing the demo alone must be reported as tutorial
reproduction. Original-source concordance needs the metareaction definitions,
feature family, filtering and manual compartment choices from STAR Methods.
