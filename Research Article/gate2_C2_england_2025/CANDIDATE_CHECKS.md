# Supporting checks for the eight England candidates

**28 September 2026. Proposed checks, not newly executed tests or frozen protocols.**
Read the [biological hypotheses](CANDIDATE_HYPOTHESES.md) first. These checks
support decisions in the shared question register; they are not eight further
biological discoveries. Freeze units, contrasts, margins and validation splits
in the relevant `RQ_Specified/` plan before a new fit. Existing data have been
inspected, so subsequent analyses require that exposure to be declared.

## E-N1: clone composition and tissue weighting

Use the deposited nonspatial hierarchy and existing
ignored `processed/batch1/clones/clone_measurements.csv.gz` and tracked
`trials/batch1/clones/clone_summary_by_mouse.csv`.
Reconcile [Table S1 with the archive](../../docs/audits/2026-09-28-england-paper-rqs/table_s1_reconciliation.csv)
first. Compare clone-weighted and cell-weighted summaries within mouse and
reporter, then standardize to a prespecified common clone-size distribution.
Keep within-time relationships separate from differences between time points.
Check singlets and noninteger image-derived cell estimates. Do not define fast
founders by size and then test their size. Standardization is descriptive:
clone size could itself mediate biological change, so adjustment is not a
causal estimate of identity loss independent of growth.

## E-N2: paired mutant and WT burden

Verify same-mouse RFP/YFP indexing and lobe-area accounting. Compare labelled
mutant burden per sampled area with WT clone/cell density and WT
pro-Sftpc-negative fraction. Show every mouse within each time point. Check
labelling density, shared injury and the fact that YFP labels a subset of WT
cells. The small mouse count supports descriptive contrasts. These nonspatial
arrays cannot repair A18's missing spatial mouse/clone identifiers.

## E-N3: survival and conditioning in A17

After repairing the parameter/switch-schedule specification, distinguish initial
founder fractions, fractions among surviving expanded clones, and fractions of
all contributed cells. Map extinction, singlets and expanded-clone retention
under each model and the actual sampling rule. An analytical birth-death
calculation can check a correctly specified simulator, but cannot silently
replace the literal deposited implementation. Compare held-out models under
the same bins, folds and objective; preserve an insufficient-discrimination
outcome. See the [A17 audit](../../docs/audits/2026-09-28-england-paper-rqs/REPORT.md).

## E-N4: coordinated epithelial output

Freeze a small source-derived panel and control genes. Analyse each eligible
library separately; define neighbourhoods without the tested genes and keep
depth/cycling comparisons fixed. Separate state prevalence from within-state
expression. Report EGFR-ligand and SPP1/DLK1 axes separately; do not construct a
favourable composite after inspecting results. Check shared coverage without
relaxing the eligibility gate. Unknown biological pools prevent animal-level
RNA inference. Co-expression is neither secretion nor recipient activation.

## E-N5: incomplete maturation versus classification

Separate AT2 retention, transition and late-AT1 features with disjoint scoring
genes. Match effective depth and retain uncertain classifications. Calibration
and evaluation must use different biological units or studies: FU_B's
in-sample sensitivity/specificity is calibration evidence. Benchmark against
independent protein, morphology or fate when available. A threshold-dependent
RNA mixed state cannot refute the source's protein-supported mixed identity.

## E-N6: genotype and cross-study transfer

Audit preparation identities, genotype, time and culture before opening an
expression pilot. [GSE253461](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253461)
has 39 entries spanning WT and Kras/p53-deficient cells, organoids and
mesenchyme; this is not 39 independent mice. [GSE227719](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227719)
has four assay/condition entries spanning RNA and ATAC, not four independent
biological replicates. Neither metadata record establishes a matched Kras-only
versus Kras/p53 causal comparison. Any eligible A16 transfer must preserve the
same compartment, separate libraries and frozen genes. Cross-study subtraction
cannot isolate the p53 effect.

## E-N7: feedback dynamics

Distinguish pathway activity, endogenous feedback induction and later
maturation. Nfkbia is an inducible inhibitor; transcript abundance alone is not
feedback competence or activity. Tonsl is a source-reported feature, not an
interchangeable validated activity meter. Regulatory associations can nominate
mechanisms. They do not distinguish failed feedback from overwhelming input
without linked temporal/activity evidence. Keep state-entry suppression,
post-entry maturation and viable mature-cell yield separate.

## E-N8: signal interaction

The non-interacting expectation depends on the prespecified response scale;
a combined effect smaller than either alone is motivation, not a complete
mechanistic test. Independent preparations, recipient engagement and separate
formation, size, cell-number and maturation outcomes are needed to distinguish
interference, saturation and toxicity. Source necessity and spatial range are
additional questions. [GSE316244](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE316244)
is an Areg-genotype study with separate epithelial/niche sorts from pooled
mice. Its four libraries are neither a SPP1-by-DLK1 experiment nor spatial
validation. AREG-mediated fibroblast effects remain a competing indirect route.

## Other biological gaps retained from the original sweep

- **Founder-specific mature AT1 subtypes:** requires founder-to-descendant
  linkage and mature subtype endpoints; inferred size classes cannot supply it.
- **WT elimination of small mutant clones:** remote apoptosis motivates the
  question, but local WT fitness and longitudinal mutant loss are not jointly
  measured by the public arrays.
- **Durable alveolar recovery after NF-kB inhibition:** organoid/PCLS markers
  and morphology do not provide the missing in-vivo functional endpoint.
- **Reversibility from RNA velocity:** re-quantification could permit a
  model-dependent directional estimate, not lineage ground truth.

The [original candidate wording](../../docs/audits/2026-09-28-england-paper-rqs/history/RQ_CANDIDATES.original.md)
is preserved as history. The source audit and its numeric artefacts remain in
the dated audit folder; current paper-specific hypotheses and checks live here.
