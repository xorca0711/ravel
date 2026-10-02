# Nb4-P03: disease expression as identity, induction or composition

**Status: planned; existing disease sources require new contrast qualification.**
[Master contract](README.md) · [source ledger](SOURCES.md). S01 normal context;
S05 IPF discovery; S06 second-cohort transport. These are previously exposed
repository resources, not newly unseen validation data.

## Question and alternatives

In idiopathic pulmonary fibrosis, does a disease-associated expression pattern
reflect a population's normal identity, altered expression within a comparable
state, or a change in the captured population mixture? Start with **IPF and
alveolar/adventitial fibroblast context**, because Nb4 already has auditable
normal contrasts. Treat epithelial and immune expansion as separate secondary
branches, not a post hoc search for whichever compartment is significant.

The initial C3 result motivates a sentinel check, but broader complement
transfer was inconsistent. Freeze an independently sourced IPF-associated
gene panel with gene–disease evidence categories before fitting; the paper's
disease catalogue supplies localization context, not proof that every listed
gene causes IPF. Do not select this panel using the same IPF DE outcome.

## Measurement and units

Primary estimand: the IPF–control expression contrast within independently
defined, comparable fibroblast states, estimated by donor in each study.
IPF and control people are unpaired unless actual repeat sampling proves
otherwise. Retain tissue pieces and modalities nested within donor.

Decompose a standardized mixture contrast on the linear expression scale into
expression and captured-composition contributions using a frozen reference;
show the alternative decomposition order or a symmetric decomposition because
the attribution depends on the reference. This is descriptive accounting, not
a causal mediation model or tissue cell-abundance estimate.

## Ordered analysis

1. Requalify S05/S06 diagnosis, control definition, region, donor/patient IDs,
   count provenance, cell labels and previous exposure. Restrict primary
   comparisons to verified IPF; keep other fibrosis/COPD diagnoses separate.
2. Freeze a label crosswalk without C3, chemokine or tested disease-panel genes.
   Preserve disease-associated populations with no normal counterpart as
   unmatched states. Do not force them into a healthy cell class.
3. Build donor-state pseudobulks. Estimate within-state contrasts using a
   design-supported count model, with prespecified age/sex/smoking/region
   adjustments only where metadata and design support them. Display both
   unadjusted and adjusted results; do not fit an overparameterized design.
4. Contrast fixed-mixture expression with captured-mixture summaries; audit
   sorting, cellular/nuclear preparation, depth and state-definition sensitivity.
   An unmatched disease state is reported separately, not zero-filled in controls.
5. Freeze discovery results and transfer the same contrast/panel into S06.
   Rank-based GSEA/GO may contextualize genome-wide within-state effects using
   declared tested genes and gene-set versions. Validate any localization claim
   in independent pathology-labelled tissue if available.

## Decision, figures and next step

Retain a within-state disease-context RQ if it transfers across qualified
cohorts and survives independent state definitions. A mixture-only result
narrows the question to captured composition; an unmatched-state result narrows
it to state emergence. Neither establishes the cell of disease origin,
therapeutic target validity or an epithelial-to-fibroblast mechanism.

Planned panels: donor/diagnosis coverage, healthy identity dot plot,
within-state effect forest, mixture decomposition and independently labelled
spatial context. Caption focus: **“Fibrotic expression is resolved into its
cellular context and disease-associated changes within that context.”**

First deliverable: donor × diagnosis × state coverage and fixed disease-panel
provenance. If the resulting question is the same epithelial-input/chemokine
mechanism, merge into A22/A13 and preserve their existing unsuccessful or
conditional results. Disease mapping alone is not a new A-number.
