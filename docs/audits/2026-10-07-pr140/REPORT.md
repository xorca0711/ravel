# PR140: scientific code, saved artifacts and A30 framing audit

7 October 2026. Requested scope: Wp analysis QC, relation to A30 and the source
paper; subsequently A30 schematic and repository-wide agent framing.

**Recommendation: resolve the Compass orientation defect before accepting its
biological interpretation.** A30 v3's saved calculations are internally consistent,
but do not establish activation independence, regulatory equivalence or a causal
CSF effect. Documentation changes in this branch correct those overstatements;
no frozen numerical run is edited or replayed.

## Revisions and verification boundary

- Audited [PR140](https://github.com/xorca0711/ravel/pull/140) at
  `74d6bd6b1c0ee411c929efbf473b5fd39dcce243`; its original base is
  `744996d0c7302fd497699c5915926137d9e3d432`.
- Integrated current main `32174c9` in isolated branch
  `codex/pr140-artifact-audit-20261007`, merge `48ad937`. The registry conflict was
  formatting plus additive entries: all four PR140 contracts/receipts and main's
  two approved infrastructure paths were retained.
- [Checker](check_saved_evidence.py) and [machine-readable results](verification.json):
  **24 Wp receipts verify; 85 saved-table arithmetic checks pass.** The checker
  recomputes donor contrasts, signs, Wilcoxon p-values, primary BH, support counts,
  both decompositions and named-gene floor invariance. These are numerical
  verification on shared data, not biological replication or new model fitting.
- Raw matrices, raw Compass reaction penalties, original barcode QC and individual
  random-null draws were not replayed. Receipt checks validate recorded code and
  output hashes, not independent re-verification of every raw input or scientific
  assumption. The null summary CSV cannot reconstruct all empirical tail counts.

## Findings and required disposition

### P1 — Wp-R2 interprets penalties with the wrong direction

[`compass_sensitivity_v2.py`, lines 200–212](../../../Research%20Article/gate2_W2_wagner_Th17_PGAM/scripts/compass_sensitivity_v2.py)
reads `reactions.tsv`, labels its values negative-log penalties in a comment,
and passes them unchanged to Spearman correlation. The serial runner changes
pool execution only and performs no score transformation. The official
[Compass tutorial](https://yoseflab.github.io/Compass/notebooks/Demo.html) applies
`-log(penalty + 1)`; the [authors' fork](https://github.com/wagnerlab-berkeley/Compass)
also defines larger raw output as less metabolic consistency.

The saved `PGM_pos` raw-penalty correlation is **−0.2912475688**. A strictly
decreasing negative-log conversion reverses its consistency correlation to
**+0.2912475688**. Two-sided p-values and absolute-correlation ranking are invariant
under this sign reversal, but the statement that the PGAM sign survives is not.
The same issue affects other signed reaction interpretations. Micropools nested
within four libraries and two animals do not create independent biological units.

**Next correction:** recover/hash the raw matrix, declare penalty and transformed
score conventions, add a meaningful orientation check, and publish a new governed
version of the signed tables/report. Preserve v1/v2 code, receipts and outputs.
Raw-matrix recovery is needed before claiming a completed end-to-end correction;
this audit does not rerun a solver or certify the paper's Figure 1 ranking.

### P2 — A30 entrypoints still made superseded or unsupported claims

The old README/canonical card said activation was excluded, BH was 0.063–0.068,
regulatory competence was unchanged, and shared-clone comparison could establish
residency. PR140's v3 table instead gives inflammatory BH **0.0321/0.0368/0.0321**,
with residual activation medians **+0.00845/+0.00897/+0.02791**. Activation
Wilcoxon p-values are 0.0391/0.0371/0.1641 (unadjusted contextual tests).

Gene-disjoint panels are not independent measurements of activation. Broad
tertile membership does not establish within-stratum balance. Regulatory BH
0.8174 is non-significance, not equivalence or preserved suppressive function.
Shared TCR establishes clonal relatedness, not residence, migration direction or
induction. The two activation tests address different nulls; their differing
p-values are not contradictory evidence about an identical hypothesis.

**Addressed editorially:** current README, canonical card, dossier, literature
context and v2 schematic now state the bounded association and alternatives.
The v2 measured plot is linked as historical. The [extension baseline](../../../RQ_Specified/A30_csf_compartment_effector_state/EXTENSION_BASELINE_V2.md)
separates existing measurement qualification from conditional new experiments.

### P2 — Random-set calibration and Monte Carlo claims exceed the evidence

The activation script samples size-matched sets from `common`: the loaded
marker/module/programme subset with nonzero variance, not all expressed genes.
It does not match expression or detection, and its pool includes the scored
programmes. A small empirical p-value is therefore specific to that restricted
null; it is not a test against every activation-associated programme.

The erratum compares raw-p Monte Carlo SE (~0.006) directly with BH distances
0.013–0.018, calls both inside two SE, and attributes the threshold crossing to
an underpowered null. This neither propagates uncertainty through BH nor supports
the stated arithmetic. Both normalization and draw count changed; their separate
contributions were not isolated. Ten thousand draws reduce simulation noise but
do not repair an unsuitable gene universe or quantify donor uncertainty.

**Disposition:** retain the observed v3 table; interpret it against its actual
null. A new sensitivity needs a justified universe/matching strategy, retained
draws and Monte Carlo uncertainty on the decision statistic. Historical erratum
text is preserved with a link to this correction of its interpretation.

### P2 — QC and decomposition support do not establish comparable CD4 states

The code implements UMI/gene/mitochondrial and library-depth filters, T-marker
support, marker dominance and a hard-zero CD8A/CD8B gate. It does not establish
positive CD4 identity or perform a doublet call in this entrypoint. The exported
QC table retains final counts, not the complete filtering cascade; cell exports
lack original barcode IDs. The recovery assertion checks library/tissue **counts**,
not identical barcode membership. Equal counts are confirmed; identical cells
were not independently verified.

Both v3 runs export 35,928 cells over 22 retained donor/tissue libraries. Ten
donors are paired overall; the ≥50-cell stratum floor leaves 9/10/9. Donor-level
units are correctly used for those contrasts. The stratified script records a
failed optional clustering path; the separately registered state-decomposition
run supplies the 23-state analysis. This separation is legitimate and must remain
visible rather than treating the internal failure as a successful cluster run.

Saved per-donor decompositions are arithmetically exact. Their aggregate
**38.8%** is median(composition)/median(total), whereas median(composition/total)
is **33.3%**. Separately calculated medians need not add to the median total.
Pooled-mean filling for a state absent from one compartment assigns its contribution
to composition by convention. PTC41540 has **82.3% of retained CSF cells** in such
states. This is a concrete support limitation, not proof of a wrong arithmetic
implementation. Biological cluster identity and common-support sensitivity remain
unqualified; the summary is not a causal fraction explained.

### Wp-R1 floor sensitivity is internally coherent but exploratory

The universe falls from 18,500 genes at floor 0 to 10,732 at 1 CPM; discoveries
fall from 18 to 0. Sixteen of the 18 unfiltered hits never reach 1 CPM in any
tested library. Named-gene raw effects/p-values are invariant across floors, as
expected because the fit is unchanged and only eligibility/BH changes.

The model has eight libraries from two animals, unmoderated log-CPM OLS and three
residual degrees of freedom. The floor was selected after outcome exposure, which
the report acknowledges. This is a useful stability diagnostic, not confirmatory
evidence or a replacement for a qualified count/variance model. No broad new
floor sweep is justified merely to regain discoveries.

## What Wp means and how it connects to the paper

| Route | Source, purpose and biological unit | Relationship and limit |
|---|---|---|
| Wp-R0 | Source identity/metadata qualification | Provenance and feasibility, not expression evidence. |
| Wp-R1 → A28 | GSE289733; glucose/polarisation; eight libraries, two mice | Reconstructs the Figure 3 setting using the deposited matrix. Missing author final-cell membership prevents exact replay. A28's protein question remains conditional. |
| Wp-R2 → A29 / Wp-P02 | Restricted Compass reactions on micropooled RNA | Version/input sensitivity, not Figure 1 reproduction. Direction defect prevents the current signed mechanistic reading. |
| Wp-R3 / Wp-E3 | GSE290297 TPM, drug/protocol contrasts | Library-level description without recovered animal/culture identities; not biological-replicate count DE or independent validation. |
| Wp-R4 → Wp-M3 → A30 | GSE138266; disease reconstruction then paired CSF/blood | Paper Figure S4 asks a disease contrast; A30 is an exposed-data compartment extension on the same lineage of evidence. |
| Wp-M1/M2/M3 | Metadata-led follow-ups to the existing data | Distinct from Wp-E extension labels; they do not supply new independent samples. |
| Wp-E5 | External source eligibility screen | A screen is not an executed expression validation or independent replication. |

Wp denotes the [Wang 2025 PGAM paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12443480/);
Wg denotes the 2021 Compass package; Niethamer W1 is separate. A30 does not test
PGAM flux, the mouse intervention or the entire paper. A failure to reproduce a
human score pattern under this implementation cannot refute those distinct experiments.

The [joint-preparation note](../../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/JOINT_EXPERIMENT.md)
concerns A28, A29 and Wp-P02, not A30. It correctly separates glucose from PGAM
perturbations, but its five listed A29/P02 arms are not a complete three-factor
PGAM×PHGDH×PEP design. A PEP add-back contrast also needs a justified control
strategy before rescue specificity is claimed. Shared preparations may save work;
they do not require joint execution, merge estimands or create independence.

## Agent-policy audit and completed documentation correction

[Decision workflow and instruction review](../../AGENT_DECISION_WORKFLOW.md)
records the inappropriate universal-mechanism requirement found in the canonical
question register, the broader ambiguity in AGENTS.md, and the corrected
work-type routing. No tissue-specific instruction was found in either tracked
agent entrypoint. No validator, schema, frozen contract or historical baseline
was weakened. Policy edits remain explicit review material, not self-certified
human approval. The latest validation and delivery state is in [PROGRESS.md](../../../PROGRESS.md).

Remaining numerical work is deliberately versioned and unexecuted: Compass
orientation correction and A30 QC/null/support sensitivity. This audit makes those
next actions concrete without overwriting protected evidence or promoting claims.
