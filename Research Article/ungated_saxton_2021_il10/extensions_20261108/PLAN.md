# IL-10 extension plans: output transport and IL-18 co-input

8 November 2026. Owner-authorized planning and execution under **Sx10-P01**.
[Question rationale](../../../docs/research_reviews/2026-11-08-saxton-reading/RQ_DEVELOPMENT.md)
and [literature history](../../../docs/research_reviews/2026-11-08-saxton-reading/POST_RESULT_LITERATURE.md).
Prior Saxton outcomes and Gorby published findings are exposed; no confirmation
or new accepted RQ is claimed. Existing frozen analyses remain unchanged.

## Route 1: does the contrasting IFNG/GZMB/IL18RAP response transport?

**Purpose:** a specified context comparison, not an affinity mechanism estimate.
**Source:** Gorby et al. 2020, GSE146438, human CD8 cells, R5A11D versus WTD
at 0.1 and 50 nM, with unstimulated controls. Cells were activated/expanded over
six days with ligand exposure, unlike Saxton's post-activation 24-hour treatment.
Ligand identity, dose and timing change together across studies; their separate
contributions cannot be estimated by pooling the studies.

**Published premise:** [Gorby et al. (2020)](https://doi.org/10.1126/scisignal.abc0653),
Figs. 5–6, already reports stronger responses at subsaturating ligand doses.
Results pp. 11–13 and RNA methods pp. 24–26 of the
[author manuscript](https://discovery.dundee.ac.uk/ws/files/51987933/REF_Gorby_et_al_Text.pdf)
were inspected in primary indexed text. GEO describes normalized values as
RPKM and reports three human donors. The paper's WT-selected S2 is not used as
the gene universe. The full GEO workbook is the proposed source instead.

**Metadata stage:** freeze/run workbook schema, exact GSM-to-column joins,
duplicate-control equality across all rows, stable IDs, unique target mapping,
finite/nonnegative values and public treatment descriptions. Preserve conflicting
`biorep` labels; D85/D93/D36 are source block codes, not independently recovered
donor identities. Do not infer biological independence from distinct BioSamples.
Direct sample overlap with Saxton is unverified; different accessions alone do
not certify independent donors. Eligibility concerns finite source description.

**Numerical stage, conditional on qualification:** retain exactly IFNG, GZMB,
IL18RAP; no replacement after viewing results. For each dose describe R5A11D–WTD,
WTD–control and R5A11D–control using differences of log2(RPKM+1), showing every
source block. This is not a fitted population fold change. Prespecify sensitivity
to log2(RPKM+0.1), log2(RPKM) only where all required values are positive, and
single-block omissions. Display low abundance, missingness and disagreement.
Do not exclude an expressed target merely because it fails the original paper's
WT-significance filter. Do not fit p-values, EC50, a causal STAT model or a
cross-study pooled effect. Freeze the exact numerical contract after metadata.

**Main threat:** treatment history, source normalization, donor/block allocation
or state differences can explain transport failure. Agreement motivates a later
matched protein comparison; mixed/reversed responses narrow the context; missing
targets or uncertain matrix meaning hold the affected endpoint. RNA does not
measure IL-18 competence, IFNγ secretion or killing. Independent raw-input scalar
verification and figure inspection precede reporting.

## Route 2: does ligand choice alter the IL-18 response increment?

**Hypothesis:** super-10-associated IL18RAP RNA accompanies a greater incremental
IFNγ response to IL-18 than WT, without requiring higher GZMB. **Rival:** direct
IL-10 signaling, survival/state or receptor trafficking explains the RNA pattern
without changing IL-18 responsiveness. Freeman et al. (2012), Fig. 1, already
demonstrates context-dependent IL-10/IL-18 coactivation in mouse antiviral CD8
cells; generic synergy is not this proposal's discovery.

**Required comparison:** the same independent human donor preparations split
across no IL-10/WT/super-10/10-DE, each with and without IL-18, common activation
history and matched sampling. The estimand is each ligand's IL-18 increment
minus the WT IL-18 increment. Required endpoints are per-viable-cell IFNγ output
and receptor-component protein; GZMB is a separate output. A killing claim needs
a killing assay; IL18RAP mediation needs a justified receptor perturbation.
Dose, timing, model access, meaningful effect and precision remain unspecified.

**Run now:** a frozen public-source eligibility screen. Inspect GEO exact-variant
and broader co-input searches, all returned summaries, and full metadata for
plausible hits. GSE160332/GSE146438 without IL-18 cannot estimate this interaction.
Do not substitute coexpression, a pathway score or an unrelated macrophage study.
If no matching source qualifies, close computational intake with exact missing
arms/units/endpoints and preserve this conditional experiment plan. Search absence
does not establish novelty or absence of data everywhere.

**Informative outcomes of a qualified future comparison:** a larger increment
supports partner dependence, not mediation; no increment weakens this response
route; generalized survival/state shifts limit within-cell interpretation.

## Execution and source record

Work starts from `7bea99d`, fetched main `4318740`. Public acquisition manifests
retain URLs, date, byte counts and hashes. Initial sandbox DNS failures and an
institutional PDF 403 are retained; web-indexed primary passages remained readable.
GEO queries on 8 November use E-utilities `gds`, `gse[ETYP]`, retmax 20 and no
date filter: IL10/IL18/CD8 synonyms and exact super-10/10-DE/R5A11/Saxton terms.
The prior 2024–2026 literature scan is reused. No contact with authors, laboratory
execution, structural redesign or paid compute is implied by these plans.
