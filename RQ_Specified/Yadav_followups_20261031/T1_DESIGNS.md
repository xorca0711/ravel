# Exact next-stage designs and holds after T0

31 October 2026. **For review, not execution.** These are post-exposure designs
under the existing Wg-P06 and proposed Yd1-P02 questions. T0 has stopped.
Any approved numerical job needs a new frozen contract bound to the exact
source hashes and design. [T0 evidence](T0_RESULTS.md) owns source qualification.

## Wg-P06: first feasible processed-tracing description

**T1-R1, eligible for review:** describe the deposited isotope fractions and
processed peak areas in Hamanaka's unambiguous Fig. 3B,3D,3H and 4D blocks.
The decision is whether their reported precursor/product labeling patterns
can be recovered from the published processed values, and which routes those
measurements can support. This is source reconstruction, not independent
raw-MS validation, confirmation or a population-level treatment test.

| Fixed sheet and rows | Identity columns | Corrected peak-area columns | Fraction columns |
| --- | --- | --- | --- |
| Figure 3B, Arg rows 4–11; Orn rows 15–22; Cit rows 26–33; argininosuccinate rows 37–44; dimethylarginine rows 48–55 | A=sample; B=metabolite except final block C=metabolite; Group header changes with block | D:J; D:I; D:J; D:N; D:L respectively | K:Q; J:O; K:Q; O:Y; M:U respectively |
| Figure 3D, Arg rows 3–10; argininosuccinate rows 12–19; Cit rows 21–28 | A=sample, B=group, C=metabolite | E:I | J:N |
| Figure 3H, Orn rows 3–10; Cit rows 13–20; Pro rows 23–30; putrescine rows 33–40 | A=sample, B=group, C=metabolite | E:I | J:N |
| Figure 4D, Arg rows 3–10; argininosuccinate rows 13–20; Cit rows 23–30 | A=sample, B=group, C=metabolite | E:I | J:N |

The table uses shortened figure labels; actual sheet names contain a space,
for example `Figure 3B`. Input is the exact Figshare v1 workbook verified in
T0. All metabolites/conditions in these blocks are retained. Four suffix labels
per condition are deposited observations; donor, culture and preparation
independence remain unknown. Do not pair UT/TGF by matching suffix. The same
sample repeated across metabolites is not another replicate.

Before calculations, validate each frozen coordinate/header against the T0
layout, preserve original values and establish whether stored fraction units
are 0–1 or 0–100. The sum of complete isotope channels and the published percent
axis can inform this check; ambiguous scaling, nonnumeric entries, negative
corrected values or missing channels require an explicit source issue, not
clipping, zero fill or forced renormalization. Headers identify the source's
claimed correction; do not redo correction without raw data and settings.

Report all deposited observations, observed sample-label counts, unweighted
means and ranges within each panel/condition, with no donor confidence interval
or biological p-value. A UT/TGF descriptive difference may be shown explicitly
conditional on these source observations. Keep media/tracers separate. Retain
low/no downstream labeling and all precursor pools; do not convert a plotted
near-zero into an assay detection limit or exact absence.

Main-figure relative-abundance normalization is insufficiently specified for
an exact replay. A new stated normalization would be a new exposed descriptive
analysis, requiring explicit review; it must not be called the author method.
Do not compare arbitrary peak-area units across metabolites, instruments or
studies. No rate, time constant, calibrated concentration, collagen flux,
necessity or quantitative contribution to fibrosis follows.

The source can distinguish observed labeling of recipient intracellular
products from a purely unlabelled-pool account in this culture context. It
cannot establish source-cell delivery, route necessity or the collagen effect
of source ARG1 restriction. Even complete source reconstruction leaves those
biological questions open.

## Other Wg-P06 jobs and exact stopping conditions

| Job | Current status | Required evidence/design before execution |
| --- | --- | --- |
| T1-R2, remaining tracer blocks | Held outside the first whitelist | Fig. 3F argininosuccinate duplicate fraction headers need an explicit isotope map; Fig. 4B putrescine needs its own isotope-column map. Unaffected 3F/4B metabolites could be separately frozen without repairing held blocks. Fig. 4F can only describe its three supplied labels, with the n/error-bar disagreement explicit; exact published reproduction requires reconciled source version. |
| T1-B1, Fig. 6D/F processed intracellular pools | Conditional source-value description; not yet approved | Freeze explicit sample-prefix-to-condition mapping as an inference supported by figure/context, or obtain the author key. Confirm peak-area units and missing/invalid values. Retain all five 6D and all three 6F groups, UT/TGF, and four supplied labels. Summaries only; no donor pairing, calibration, viability-normalized synthesis or source-ARG1 effect. |
| T1-B2, collagen protein/qPCR contrast reconstruction | Held | Numerical Fig. 5/6 blot/qPCR source values, correct normalization, culture/preparation/donor/well identities, and source-version reconciliation. Digitizing blots or bars is not an authorized substitute. Existing Yadav reconstructions remain available without a rerun. |
| T1-R3, raw-MS/correction or kinetic flux | Held | Actual raw instrument files, processing/correction settings and standards, isotope purity, tracer timing, precursor enrichment trajectory, calibrated pools and validated kinetic/compartment assumptions; resource and design review. Deposited peak areas/fractions do not supply these. |
| GEO expression analysis | Outside T0 and not needed for the immediate tracer question | A separately justified RNA question, actual donor/preparation/clone design, normalization and analysis contract; GEO is not a flux source. No matrix acquisition merely because it exists. |
| Lee quantitative reconstruction | Held | Exact numeric source values and replicate/unit/timing/denominator keys. Published MRC5 and mouse results may inform the competing route, but cannot be pooled with Hamanaka/Yadav as matched measurements. |

These jobs are independent where their inputs and endpoints are independent.
The missing collagen table does not block T1-R1. A header problem in one block
does not license repairing it from favorable results or discarding an entire
negative medium. T1-R1 completion would not itself release a later job.

## Yd1-P02: exact endpoint hold and bounded next work

**T1-E numerical joint-effect analysis is held.** Atg5 Fig. 2 and 6 lack an
individual preparation/animal-to-endpoint join, source values and the proposed
absolute mature functional endpoint. The perturbation is mesenchymal Atg5,
not myeloid ARG1. Source organoid formation, diameter, T1alpha RNA and marker
ratios cannot be substituted for the planned mature-output endpoint. Distinct
reported n values do not establish a repeated-measures design. Neither a
cross-paper correlation nor a new classifier resolves these gaps.

An independent T1-E source/capability qualification job could proceed after
review without numerical effect estimation. Its concrete output would be an
actual model/source inventory and endpoint feasibility record, including AT2
provenance, fibroblast preparation, source-cell perturbation validity, temporal
sampling and the matrix/epithelial linkage. If a numerical Atg5 source table
becomes available, a separately scoped description may reproduce its measured
endpoints, while keeping this joint ARG1 question held. No outreach is currently
authorized or required to declare the hold.

## Capability inventory and minimal future comparison

| Capability | Confirmed here | Required qualification before new biological work |
| --- | --- | --- |
| Small-source acquisition and metadata parsing | Primary JATS, supplements/figures, processed workbook and GEO headers cached with hashes; stdlib parser and independent bundled openpyxl/PDF reader work | Preserve versions; no large data required for T1-R1 |
| Processed LC-MS description | Source includes peak areas and isotope fractions | Units/scaling, exact block map and descriptive contract; no claim of raw-data validation |
| Source human neutrophils and primary lung fibroblasts | Published precedent only | Actual access, independent donor identity/crossing, source handling, validated source ARG1 restriction and recipient exposure/viability measurements |
| Quantitative metabolites and collagen | Published assays only | Actual laboratory/instrument access, calibrated Arg/Orn exposure measurement, qualified new/deposited collagen assay, separate viable-recipient exposure denominator and assay precision |
| Route/signaling discrimination | Hamanaka intracellular tracer and Lee PRODH/MitoSOX precedents | Access and sensitivity for recipient product and collagen labeling if a transfer claim is intended; signaling measurements/perturbations and specificity as required by that claim; actual timing/enrichment and standards |
| AT2–fibroblast organoids/lineage/function | Atg5 published mouse system; repository endpoint constraints | Actual compatible model, AT2 origin and lineage tracking, mature identity/function criteria, early survival/expansion and later mature-output timing, retained functional AT2 reserve when relevant |
| Precision and experimental oversight | No new values established | Biological-unit variance, meaningful effect or preservation margin, feasible allocation and institutional oversight; no sample size or laboratory readiness is inferred |

For Wg-P06, the minimal effect question remains **validated source ARG1
restriction versus its appropriate control**, with measured recipient Arg/Orn
exposure and collagen output in the actual accessible coculture. Independent
source and recipient donors, and their real crossing, define the units. Wells
and repeated measurements nest within them. Recipient arginine context must
be independently characterized to test effect modification; no threshold,
artificial-starvation regime or additional factorial arm is assumed. Source
survival, cytokines, recipient survival and nutrient alternatives limit the
interpretation. Rescue or extra perturbations are justified only by a stronger
mechanistic claim.

For Yd1-P02, the corresponding effect comparison must link matrix output and
**absolute lineage-linked mature epithelial output per starting epithelial
input** in a qualified source–fibroblast–epithelial system. Measurements may
use matched parallel aliquots if their preparation identity is explicit and
the assay requires destructive sampling. They are not independent replications.
Record early AT2 survival/expansion separately from later mature output. Validate
direct recipient exposure and niche-cell survival before attributing an effect
to altered fibroblast support; adjusting a post-treatment cell count does not
establish mediation. The exact functional assay and collection time remain
unknown until an actual model is qualified.

Lower collagen accompanied by better, unchanged-but-imprecise, or worse mature
output are all informative. A precise preservation claim needs a justified
margin and precision plan; NS is insufficient. A substrate result without the
joint epithelial endpoint leaves Yd1-P02 unresolved. This is a proposed context
extension/effect question, not a novelty claim, mechanistic conclusion or
permission to start bench work.

## Preserved work and next checkpoint

T0 retains every A0–A31 question/guide, all original Yadav and X0–X6 evidence,
the separate human-context companion, and old spatial/X3–X5 holds. The Atg5 read
does not reopen A13/A22 proxy fits or change A20/A8/A19 hypotheses. Review should
select an exact eligible job and its inference limit before another contract
or numerical run. T0 completion is not that authorization.
