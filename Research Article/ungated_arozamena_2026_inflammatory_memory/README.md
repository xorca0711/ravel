# Arozamena 2026: deposited RNA and accessibility comparisons

1 November 2026. Article-local candidate **Arz1-P01**, proposed and outcome-exposed.
The owner requested source qualification through the existing technical chat,
every eligible extension, originating review and updates to PR #157. This package
owns the new paper's evidence; the [Saxton connection note](../gate3_08_saxton_2021_il22/reassessment_v1/RQ_CONNECTIONS.md)
owns its motivation. Neither a new canonical RQ nor human scientific acceptance
is created. [Literature/source context](LITERATURE_CONTEXT.md).

**Reviewed RNA result:** the eight selected targets show mixed accession-specific
directions. GSE329778 LGR5 changes from a -0.506 panel median before RNA QC to
+0.556 after RNA QC; retention is 635 of 6,921 barcodes. This is selection
sensitivity, not a recovered true direction or a test of the paper's ISC-specific
claim. [Results](RNA_RESULTS.md) · [Figure gallery](FIGURES.md) ·
[Originating review](ORIGINATING_REVIEW.md) · [Existing-RQ context](RQ_CONNECTIONS.md).

**Reviewed paired result:** all 128 four-locus RNA/fragment cases completed in
GSE329778. LGR5 Tiam1 has negative TSS-window but positive gene-body differences
under every fixed QC/weight choice. Some RNA directions also change with selection.
The two explicit fragment-count definitions change the largest contrast by
0.00270523 log2(CPM+1), with no sign changes in their 64 paired comparisons;
this does not establish biological equivalence or physical molecule identities.
[Accessibility results](ACCESSIBILITY_RESULTS.md). Four reviewed figure plates
are available. These finite-library measurements leave within-state regulation
and later function unresolved.

## Question, source and intended contribution

**In the deposited intestinal data, can the reported post-injury RNA/accessibility
pattern be attributed descriptively to differences within comparable epithelial
states, separately from changes in their abundance?** A separate conditional
question is whether early molecular measurements actually join later measured
regeneration at the appropriate biological-unit level.

The source is [Arozamena et al., Nature Communications 2026](https://doi.org/10.1038/s41467-026-79014-6),
*Inflammatory memory primes the intestine for enhanced regenerative potential*,
version of record 27 October 2026. This is a non-infectious intestinal injury/history
study. Its published molecular-memory/regeneration interpretation is an exposed
premise, not a new discovery proposed here. The contribution sought is source
qualification, transparent shared-source reproduction and bounded measurement/model
discrimination, with explicit failure and eligibility outcomes.

The [completed source checkpoint](SOURCE_QUALIFICATION.md) qualifies six accessions,
44 sample/BioSample records and seven processed multiome matrices. Their shared
RNA universe is 31,950 IDs; no exact peak ID is common to all seven. Full text and
supplements were recovered from public Europe PMC after direct publisher-route
failures. State/donor annotations and a validated mouse/pool crosswalk were not
located in the documented source coverage. Cohorts remain non-interchangeable.

Plan amendment: run a [narrower four-contrast RNA description](RNA_EXTENSION_BRIEF.md)
because matched gene IDs and accession-specific controls are available. This
Q3a/Q5a extension does not complete the held within-state Q3. The subsequent
[Q4a assessment](Q4A_FEASIBILITY.md) found GRCm39/ARC 2.1 fragment headers that
conflict with the article/GEO mm10/ARC 2.0.2 description. A streamed four-locus
adaptation is feasible on the deposited reference; the
[prospective accessibility brief](ACCESSIBILITY_EXTENSION_BRIEF.md) fixes common
M33 TSS-proximal windows and gene-body sensitivity before counting. This is not
exact author replay or a substitute for missing cell-state annotations.

Accessibility execution amendment: [v1 stopped on opposite-strand repeated
coordinate/barcode keys](ACCESSIBILITY_V1_HOLD.md), before any accessibility
endpoint was released. The held run is preserved. The prospectively frozen
[v2 amendment](config/ACCESSIBILITY_AMENDMENT_V2.md) counts strand-labelled records
and explicit coordinate-collapsed sensitivity with consistent denominators,
keeping the other comparisons fixed. Both definitions completed and passed
independent raw-source review. Neither certifies physical molecule identities;
all mixed and unfavorable outcomes are retained.

## Comparison and interpretation limits

The tissue is intestinal epithelium. Source-qualified accession/condition records
define four separate RNA contrasts; two third-deposit contrasts reuse CTRL for
paired RNA/fragments. Deposited barcodes are nested observations, and the finite
library is the descriptive unit. Reported pooling does not establish independent
mouse/preparation identities. Run numbering, sorting/genotype and reference
metadata contradictions remain recorded in the source reports.

Primary candidate measurements are source-qualified state proportions and
within-state RNA/accessibility summaries. The main alternatives are composition,
lineage selection/survival, library/processing effects, mismatched assays and
continued niche input. These can coexist with within-state differences. Gene
expression is not signal activity; accessibility is not occupancy or memory;
cell-level pairing is not independent biological replication. Later functional
outcomes require actual sample/animal/preparation joins, not shared group names.

The completed adaptations use post-minus-control log2(CPM+1) differences under
separately frozen RNA and accessibility contracts. RNA uses all-source gene depth;
fragments use canonical nuclear source-record depth under the same counting
definition as each numerator. TSS windows are annotation-defined proxies, not
validated promoters or the author's consensus peaks. RNA-only QC omits ATAC QC.
Unknown independent units restrict interpretation to finite-library description.
No population p-values/FDR or certainty claims are supplied by a large cell count.

## Stepwise disposition ledger

| Job | Scope and decision | Current disposition / exact reopening evidence |
|---|---|---|
| Q0 | Verify paper/version/accessions and retrieve legitimate public source records; record hashes/access failures | Completed within documented coverage; full XML and four supplements recovered |
| Q1 | Reconcile sample/preparation/animal identities, pooling, history/time/lineage, assay pairing and annotations | Source map completed with explicit run-number/sorting contradictions; independent mouse/pool identities unvalidated |
| Q2 | Contracted metadata/input QC: formats, dimensions, identifiers, barcode overlap, coverage and available state mapping | Completed v1/v2; counted-empty-record adapter resolved three parser holds without changing sources |
| Q3 | Describe within-state versus state-abundance contributions for a source-supported comparison | Held: author barcode-state map not located in inspected deposits/supplements; requires that map or separately reviewed operational state annotation |
| Q4 | Describe paired RNA/accessibility relationships within the same qualified state and assay units | Held: no common recounted matrix across seven libraries, first/second-deposit fragments not located, state map absent, and actual third-deposit reference conflicts with paper metadata |
| Q5 | Bounded sensitivity to source-supported normalization, library omission and state/feature mapping choices | Eligible RNA QC/weighting and Q4a region/count-definition families completed. Original state sensitivity needs Q3's map. Library omission is undefined for singleton post/control pairs with no pooled cross-accession estimate; cells are not substitute libraries |
| Q6 | Evaluate early molecular information against later measured regeneration/fate/function | Held: no actual early-molecular/later-function animal or preparation join located; group labels cannot supply it |
| Q7 | Originating numerical/source/visual review, figure gallery, README/RQ connections and PR #157 update | Source, raw numerical and four-figure review completed; this reviewed package and context are delivered through PR #157. Execution is not scientific acceptance |
| Q3a/Q5a | Four accession-specific whole-library RNA contrasts and fixed weighting/RNA-only QC sensitivities | Completed and independently reviewed: 31,950 genes, 16 cases, 128 selected-target contrasts; no execution/mapping/empty-subset holds |
| Q4a | Third-deposit-only four-locus common-region accessibility and paired RNA | Completed and independently reviewed: 152,186,923 source records, 19,981 paired barcodes, four loci, 128 paired cases and 64 count-definition deltas; no endpoint/locus/subset holds. V1 hold remains preserved |

The remaining restrictions are **data/design limitations**, not a current
content-policy refusal or external account-setting blocker. Population inference
needs qualified independent pools/preparations and their condition mapping.
Exact author replay additionally needs reconciliation of processing/reference
versions, the custom reference/annotation and the final author QC/state object.
Q3/Q4 can reopen with a provenance-qualified author map, or a separately reviewed
operational annotation design that is explicitly an adaptation. Q6 needs actual
timed molecular-to-functional unit links; matching group labels cannot supply them.
Missing records are reported only for the inspected coverage, not declared absent
from every possible source.

## Reproducibility and current evidence

Metadata v1/v2, RNA v1, held accessibility v1, completed accessibility v2 and the
render-only primary correction have separate frozen contracts and receipts.
[Originating review](ORIGINATING_REVIEW.md) records independent audits and their
limits. The [gallery](FIGURES.md) uses the corrected primary rendering without
overwriting the original figure or changing any measurement.

Raw inputs remain ignored under `raw_data/Arz1` in the technical worktree
`C:/Users/dream/.codex/worktrees/saxton-metadata-recovery-20261031/ravel`.
They were not duplicated into the review checkout. Public source URLs, versions,
byte sizes and hashes are recorded in [intake](sources/intake_v1.json), the
source reports and versioned contracts. A new checkout must reacquire or otherwise
provide those exact inputs and pass input preflight before any new versioned run;
do not replay a historical run over its frozen outputs.

## Execution and ownership

Existing technical chat: `01a191d5-e0e2-70d2-92e0-97272f85ce11`. It owns source
records/manifests, qualification reports, scripts/tests/contracts and new immutable
runs/results/figures. The originating reviewer owns this README, literature
context, parent navigation/PROGRESS and final integration. Each consequential
scientific specification is reviewed before execution. No new chat chain is needed.

Source reading can proceed immediately. Metadata analysis needs its own committed
contract and runner; biological endpoint work follows a reviewed numerical brief
and a separate freeze. Preserve all earlier Saxton and other article evidence.
Do not change validators, root attributes, governance, canonical hypotheses or
claim grades. No ligand engineering, pathogen analysis, laboratory protocol or
intervention optimization is part of this task.

Use qualified processed inputs where adequate. Inspect file sizes, disk, memory
and existing runtime before acquisition; no gratuitous raw-read processing or
package installation. Access failures are not proof of absent data. A current
content refusal, if any, is recorded verbatim and stops its dependent work; no
context masking, access-control bypass or replacement-chat workaround is allowed.
Continue independent permissible work and document the exact evidence needed
to reopen held steps. Execution completion is not scientific acceptance.

## Relation to existing RQs

This can supply a bounded epithelial measurement reference relevant to
[A1](../../docs/research_dossiers/A1.md) and the assay/composition problem in
[DY1-P02](../gate2_DY1_damani_yokota_2026/rq_discordance/README.md). Its potential
history/output connection is relevant to [A14](../../docs/research_dossiers/A14.md)
and [A8](../../docs/research_dossiers/A8.md), conditional on actual linkage.
It does not establish an IL-22 mechanism, alveolar repair, or the NAM
STAT6–EGR2–PPARγ/RXRA/ARG1 pathway. Canonical RQ cards retain their distinct
organisms, inputs, populations and functional endpoints.
