# CCR2: directed movement versus context-dependent fitness

7 November 2026. Exploratory Dp1-P01 subquestion; not an accepted new RQ.
[Follow-up overview](../CANDIDATE_FOLLOWUP.md) · [Source audit](SOURCE_QUALIFICATION.md).

**Completed numerical follow-up:** [gain-context results](../CANDIDATE_ANALYSIS_RESULT_V1.md).
The experimental stages below remain proposed; interpret their RNA premise with that result.

## Published finding → repository observation → remaining question

[Zhan et al., online 2018 / issue 2020](https://doi.org/10.1038/s41423-018-0187-8),
Figures 5–6, supports CCR2-dependent CD25 regulation in an inflammatory mixed-cell
context. Purified Tregs responded little to CpG; CCL2/MCP-1 alone did not clearly
increase CD25 (reported without displayed data). TCR- and IL-2-stimulated CD25
upregulation were not similarly CCR2-dependent. Thus, loss of an inflammatory
accessory-dependent response is a more defensible fitness hypothesis than a
universal autonomous CCL2→CD25 pathway.

DuPage's exposed [coding table](../../../analysis/research/runs/dupage_target_screen_v2/all_annotated.tsv)
has lower Ccr2 in KO-low and a stable signed interaction. Il2ra RNA does not show
a substantial stable corresponding deficit. Tissue recovery in the original
paper cannot separate movement, retention, survival and proliferation.

**Question:** does Ezh2-associated CCR2 reduction accompany impaired directed
movement, impaired context-dependent fitness, both, or neither? The contribution
would be model discrimination in this Ezh2 context. CCR2 trafficking and fitness
are already established biological possibilities.

## Comparison tuple and estimands

| Element | Prospective specification |
|---|---|
| Population/model | Viable lineage-identified murine lymphoid Tregs after matched activation; tissue/background/allele and comparator to be specified |
| Exposure | Defined CCR2-ligand gradient for movement; separately, a qualified inflammatory accessory-cell condition for CD25 response |
| Comparator | Ezh2-deficient versus matched genetic control, with relevant vehicle/no-gradient or unstimulated condition |
| Movement endpoint | Absolute viable cells traversing the assay and fraction of viable input; gradient-free/equal-concentration controls distinguish directed movement from general motility |
| Fitness endpoints | CD25 protein response, subsequent IL-2-induced pSTAT5, and absolute viable recovery; proliferation only if a division readout is collected |
| Biological unit | Independent mouse/preparation; matched aliquots and technical wells nested; accessory-source identity/blocking explicitly recorded |
| Timing | Movement window qualified to minimize growth; signaling and later recovery measured as distinct windows, not conflated |
| Limit | In-vitro migration is not in-vivo homing; pSTAT5 is not suppression; tissue frequency is neither movement nor survival rate |

## Hypothesis, alternatives and informative outcomes

The candidate hypothesis is that reduced CCR2 contributes to at least one of the
two specified response deficits. A general activated-state or viability deficit
is the main rival; different receptor expression may also be functionally buffered.

| Result after assay qualification | Interpretation |
|---|---|
| Lower directed movement, preserved CD25/signaling/recovery | Supports a migration-specific phenotype in this assay |
| Preserved movement, altered inflammatory CD25 response or recovery | Supports a fitness/context branch; does not show a homing defect |
| Both change | Compatible with joint mechanisms or general state loss; target-specific perturbation is needed to distinguish contribution |
| Neither changes with adequate precision | Weakens these endpoint-specific mediator hypotheses; RNA may mark state |
| CCL2 does not change CD25 in purified cells | Not a decisive negative result: the closest precedent did not establish that response |

## Staged experimental design

1. Confirm CCR2 protein and viable-cell identity in matched preparations. Qualify
   a ligand gradient and a migration-responsive control. Keep CD25 as a protein
   measurement rather than substituting the near-null Il2ra RNA result.
2. Compare movement and fitness in parallel aliquots. For the fitness branch,
   first reproduce a responsive accessory-dependent context with the same
   accessory source across Treg genotypes. IL-2 is a downstream response assay
   and general competence control, not proof that CCR2 directly controls IL-2R.
3. If a qualified deficit appears, use a Treg-restricted CCR2 perturbation or
   restoration to test contribution. Exposing all mixed cells to an antagonist
   cannot by itself identify a Treg-intrinsic effect. A claim about in-vivo entry
   requires tracking input, circulation, arrival and retention separately from
   local survival; that larger experiment is conditional, not yet justified.

No rescue arm is needed merely to report a genotype difference. A rescue or
orthogonal perturbation becomes relevant when attributing that difference to
CCR2. Record unfavorable or discordant outcomes without switching endpoints.

## Data and readiness decision

The 2024 intestinal microniche source provides spatial context, not a CCR2
intervention. Its ligand–receptor inference cannot distinguish the present
movement/fitness alternatives. The closer CCR2 paper has mouse-level chimera
comparisons but also replicate-well assays; its well counts are not animal counts.
Full supplement access remains incomplete. No new numerical dataset was treated
as functional validation.

Model/reagent availability, usable migration range, accessory-cell formulation,
measurement windows, assay variance and meaningful precision remain unresolved.
These must be established before sample-size planning. Source HET controls must
not be renamed WT in the new experimental specification.
