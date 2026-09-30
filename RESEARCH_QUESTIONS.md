# Research questions

**Nb2 synthesis, 29 September 2026:** [derivation from overall results](Research%20Article/gate2_N1_nabhan_2023/RQ_DERIVATION.md) proposes **A19–A21**: epithelial response reversibility, fibroblast receptor context and capillary renewal versus maintenance. These are post-analysis questions; A19 now has an [exploratory context analysis](RQ_Specified/A19_fzd_response_reversibility/RESULTS.md), and A20 has a [fibroblast context analysis](RQ_Specified/A20_fibroblast_fzd_context/RESULTS.md); A21 now has an [independent capillary context analysis](RQ_Specified/A21_fzd4_capillary_function/RESULTS.md); all direct functional designs remain unexecuted. No mechanism, acceptance or claim grade is inferred.

**28 September gap-fill execution:** [current results and every-question ledger](docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md). A15's normalization sensitivity is corrected in a new version; A5/A12 metadata gates are resolved as far as recovered inputs permit. The newer A16/A17 computational follow-ups preserve their historical outputs and all claim grades.

**A16 branch integration, 28 September 2026:** [executed Stage 1 and review](RQ_Specified/A16_cd177_state_attribution/README.md)
are now included. Sensitivity results are retained; contamination, complete
depth control and intrinsic biology remain unresolved. No claim grade changed.

**England interpretation update, 28 September 2026:** [source/claim audit](docs/audits/2026-09-28-england-paper-rqs/REPORT.md)
and [eight readable candidate hypotheses](#england-candidates). A16–A18 below
incorporate the audit's population, model and spatial-inference corrections;
historical results and claim grades are unchanged.

**Latest follow-through:** [results and open gates](docs/roadmap_runs/2026-09-27-followthrough/README.md). A12 and an explicitly amended A13 pilot now ran; prior failed cohort gates remain failed. New results are exploratory, with no claim-grade changes.

**Roadmap execution, 27 September 2026:** [package results](docs/roadmap_runs/2026-09-27/README.md). P1 recovered split-well replication and supplemented EGF in the screen; P2 replication remains gated, and P4 quantifies source-attribution uncertainty. Current interpretations below retain the original numerical results.

**Interpretation audit, 27 September 2026:** [all questions and trials](docs/audits/2026-09-27-rq-rationale/REPORT.md);
[shared research architecture](docs/RESEARCH_ARCHITECTURE.md). A2 and A15
interpretations below incorporate the dated corrections; recorded estimates,
thresholds and historical claim grades are unchanged.
The [research roadmap](docs/RESEARCH_ROADMAP.md) structures proposed next work, biological context and stop rules.

> Which epithelial programmes and immune–stromal interactions distinguish
> productive lung repair from persistent remodelling after injury?

This project uses public lung RNA, chromatin and complementary assays to develop
and test its own biological hypotheses. Our observations motivate developmental
programme reuse, context-dependent loss of epithelial identity, and recipient
and fibroblast contributions to injury responses. Those interpretations are
scientific propositions to distinguish from alternatives, not just criticisms
of markers or analysis tools.

**Rewritten 25 September 2026; A0 registered 26 September.** All A1–A14 identifiers remain; A12-S1 remains an
enabling source-identity question. There is no fixed number of “surviving” RQs.
**A15 is proposed on 27 September 2026, and A16, A17 and A18 on 28 September 2026, each pending the owner's retain or reject**;
until that decision they grade nothing and add no claim row. A16, A17 and A18 derive from the
[England re-analysis follow-up](Research%20Article/gate2_C2_england_2025/RESULTS_FOLLOWUP.md);
A16 connects to the existing A8 and A11 identity and lesion-programme questions, A17 to the A4 lineage question,
and A18 to the A13 and A15 niche-signalling questions,
but each retains its own test and decision.
Related questions share evidence but retain separate tests and decisions.

The [claim register](CLAIMS.md) grades the original measurements. A new biological
interpretation does not inherit a historical claim's status. Here **motivation**
describes the connection to observations; **readiness** describes whether a
discriminating test can run. This rewrite establishes no new mechanism and
changes no result, threshold or claim grade. These are source-informed and often
post-analysis hypotheses, not retrospective preregistrations or novelty claims.

The [measurement contracts](docs/RQ_MEASUREMENT_CONTRACTS.md) collect technical
checks that can change a decision. The [figure gallery](analysis/figures/rq/README.md)
preserves measured panels, full captions, diagnostics and labelled designs.
The [migration record](docs/migrations/2026-09-25-rq-reframing/README.md) preserves
the previous register. Paper-specific evidence stays under `Research Article/`;
question-specific execution stays under `RQ_Specified/`.

## Biological hypotheses and execution priorities

The collections do not share an independently measured repair outcome. Analyse
development, infection, fibrosis and neoplasia within their own designs; do not
order them along an assumed repair-to-cancer trajectory. Late sampling is not a
recovery endpoint, and population persistence does not trace the same cells.

| ID | Biological hypothesis / decisive endpoint | Motivation | Readiness and next task |
|---|---|---|---|
| [A0](#a0) | A conserved transition-associated programme may contribute to epithelial fate modulation | Related transitional RNA states across repair and development; shared fate control remains a hypothesis | [Pilot complete](RQ_Specified/A0_conserved_epithelial_transition_program/reports/PILOT_V1_RESULTS.md): 50-gene lung signature fails the mature intestinal endpoint; P4 pruned; universal/causal fate claims unresolved |
| [A1](#a1) | Regulatory features distinguish RNA-similar transitional states and responses | Direct marks, lineage, perturbation and paired CD44 context contrasts | Adaptive batch complete; matched replicated regulatory/fate linkage remains missing |
| [A2](#a2) | AREG changes a fibroblast response through delivery to a competent recipient rather than through source abundance | Seven register rows do not establish a depth-independent epithelial source hierarchy; delivery is a distinct hypothesis | [Both legs run](RQ_Specified/A2_areg_source_delivery/reports/STAGE5_SYNTHESIS.md): no Areg decrement is established; epithelial Itgb6 is associated with -0.938 log2 CPM in three readable split wells; depth-standardized rho 0.293 is inconclusive, not evidence of no coupling |
| [A3](#a3) | Injury leaves a macrophage programme beyond normal aging | Late population composition | Age-matched controls and comparable sampling needed |
| [A4](#a4) | Wnt maintenance and IL-1 response occur sequentially in an AT2 lineage | Transcript/source observations; sequence untested | Measured activity/history and lineage-linked response needed |
| [A5](#a5) | Adult repair reuses a developmental epithelial component | Neonatal coexpression and label-excluded ADI enrichment; outside developmental list now sourced | Revised external-signature test positive in 24 mice and after identity/control exclusions; lineage/function untested |
| [A6](#a6) | IPF changes shared macrophage states beyond subtype abundance | Cell fractions and RNA contributions differ | Harmonize states and audit donors before a within-state fit |
| [A7](#a7) | Cebpa loss attenuates identity across AT2 states | Reference and transitional contrasts both change | Replicated genotype-by-state design needed |
| [A8](#a8) | A maturation component adds information about mature AT1 contribution | Score dependence motivates separation; limited biological support | Independent mature endpoints needed |
| [A9](#a9) | Fibroblast receptor context modifies AREG response | RNA/resource observations nominate a competence question | RNA screen possible; protein/function data needed |
| [A10](#a10) | Epithelial programmes add information about measured organoid growth | Public RNA and imaging design | Follow-up complete: added information beyond E2F/G2M and positive plate-shift error gains, but negative absolute R-squared on 3/4 plates; independent units unresolved |
| [A11](#a11) | Lesion-associated programmes add to shared plasticity | Reduced HPCS signal across repair, development, IPF and LUAD | Kim lesion association replicates in 8 patients; beyond-shared criterion unresolved (BH q=0.0547) |
| [A12](#a12) | Recipient context explains responses beyond ligand RNA | Cohort/recipient heterogeneity | Exploratory 12-patient pilot: epithelial held-out error improves; fibroblast increment unstable; activation unmeasured |
| [A13](#a13) | Fibroblast programmes add information beyond macrophage IL1B | Niche heterogeneity motivates joint association | [Amended exploratory pilot complete](docs/roadmap_runs/2026-09-27-followthrough/A13_PILOT_AND_COVERAGE.md): 12 paired triads; no aggregate held-out gain. Older failed coverage gates preserved; no mediation claim |
| [A14](#a14) | Exposure duration and fibroblast reception separately affect recovery | Mechanistic follow-up to the repair/persistence question | Two decisions; withdrawal and recipient-specific data needed |
| [A15](#a15) | The epithelial input to fibroblast activation runs through integrin-mediated TGF-beta activation rather than through ligand supply | A2's exploratory association: Itgb6-targeted wells have a -0.938 log2 CPM median contrast in three readable split wells; no Areg decrement is established | **Proposed, pending the owner's retain or reject.** Blocked: no eligible deposit found in the recorded search. The authorized side-branch has run; epithelial-state mediation remains unresolved |
| [A16](#a16) | A CD177-associated priming phenotype may persist within comparable mutant transitional cells | Original population mismatch and Stage 1 sensitivities leave specificity, contamination and composition unresolved | **Proposed, pending retain/reject.** [Stage 1 integrated with corrections](RQ_Specified/A16_cd177_state_attribution/reports/INTEGRATION_REVIEW.md): partly measured and inconclusive; corrected attribution and functional evidence remain open |
| [A17](#a17) | Persistent growth differences between founder lineages may help explain mutant clone-size heterogeneity | Clone distributions and source lineage evidence motivate the model; a deposited simulator defect affects one implementation | **Proposed, pending retain/reject.** Computationally feasible after source-count, parameter and schedule amendments; held-out refit unexecuted |
| [A18](#a18) | WT expansion and loss of AT2 identity may be regulated differently near mutant clones | Source phenotype and reproduced pooled distance profiles; two causal channels remain a hypothesis | **Proposed, pending retain/reject.** Descriptive profiles complete; spatial inference needs mouse/clone identifiers |
| [A19](#a19) | Terminating Fzd-supported expansion permits mature alveolar contribution while preserving an AT2 reserve | Nb2 withdrawal lead, selective RNA output and receptor/target dissociation | **Exploratory RNA/context analysis completed.** Direct Fzd schedule, mature-output and reserve test remains unresolved; [results](RQ_Specified/A19_fzd_response_reversibility/RESULTS.md) |
| [A20](#a20) | Fzd2 is more necessary than Fzd1 for AF1 functional support of AT2-derived mature repair | Receptor/context motivation; RNA responses do not establish functional support | **Exploratory phase complete; H1 narrowed and untested.** Pool maintenance is the mechanistic focus; original subtype H2 deferred. [Focused design](RQ_Specified/A20_fibroblast_fzd_context/NARROWED_HYPOTHESIS.md) |
| [A21](#a21) | Fzd4-dependent vascular competence may permit later capillary repopulation; renewal-selective effects remain an alternative | Independent capillary enrichment; lower transitional-state Fzd4 and inconsistent cycling association | **Exploratory context completed; conditional priority.** Perturbation-linked lineage versus maintenance remains untested; [results](RQ_Specified/A21_fzd4_capillary_function/RESULTS.md) |

A0 completed its bounded pilot: the frozen programme fails the mature intestinal
endpoint, and its conditional specificity work is pruned. The A1 continuation,
A5/A11 revised tests and A10 outcome join/fits are complete.
The A10 plate/design diagnostics and separately specified growth-block test have
also run. Further A10 expansion now needs preparation identities and imaging/
validation design evidence; stronger A1, A5 and A11 conclusions require the
missing evidence named in their cards. Existing joins and scores need not be
rerun. The other questions remain conditional; their design gates still apply.
A16–A18 remain proposed. Their [source audit](docs/audits/2026-09-28-england-paper-rqs/REPORT.md)
corrects the premises below without changing historical outputs or claim grades.
A16 needs the same-compartment, separate-library comparison; A17 needs a model
and source-accounting amendment before its refit; A18 lacks spatial inferential
units. Eight further paper-local candidates are indexed below.

<a id="england-candidates"></a>
### England candidate extensions: E-N1–E-N8

Read the [eight biological hypothesis cards](Research%20Article/gate2_C2_england_2025/CANDIDATE_HYPOTHESES.md)
for context, predictions, rivals and feasibility, and the
[supporting checks](Research%20Article/gate2_C2_england_2025/CANDIDATE_CHECKS.md)
for analysis requirements. E-N1 concerns distributed identity loss; E-N2 mutant
burden and WT response; E-N3 survival selection; E-N4 coordinated epithelial
signals; E-N5 incomplete AT1 maturation; E-N6 p53-dependent growth advantage;
E-N7 failed feedback induction; E-N8 SPP1/DLK1 interaction. E-N3/E-N5 began as
technical checks and support existing A17/A1/A8 questions. These are not eight
independent discoveries or registrations; no A19–A26 identifiers are assigned.

The [logical review](docs/LOGICAL_RATIONALE_REVIEW.md) checks this sequence against
the actual measurements and implementation, with an adaptive follow-up order.

<a id="nabhan-branch"></a>
### Nabhan branch: Nb2-N1–Nb2-N8

The owner completed Nabhan 2023 and requested registration of the Nabhan branch
from their theme list on 29 September 2026. The [paper-local register](Research%20Article/gate2_N1_nabhan_2023/HYPOTHESIS_REGISTER.md#nabhan-branch)
preserves their order: intermittent stimulation/differentiation; Hippo-associated
plasticity; starting-state-specific Wnt responses; compensation after Fzd5 loss;
receptor context and diverse outputs; fibroblast Fzd1; endothelial Fzd4; and the
additional endogenous-Fzd6-input question. Each card includes a hypothesis, rival,
measurable test, contrary result and data limitation. The initial
[Nb2 execution](Research%20Article/gate2_N1_nabhan_2023/RESULTS.md) adds measured
premises and limits to each card; the hypotheses remain unvalidated.

The [three-track plan](Research%20Article/gate2_N1_nabhan_2023/ANALYSIS_TRIAL_PLAN.md)
links ten source propositions, five exploratory branches and those candidates.
Nb2-N1/N3 connect to A4/A8, Nb2-N2 to A1/A5/A8/A10, and Nb2-N6 to A13/A15;
these links do not replace their existing endpoints or establish a common mechanism.
The owner's earlier Axin2/Il1r1 theme stays with A4 and Nb1. The initial paper-local
registration assigned no new A-series IDs or C-grades. GSE208770 describes bulk
organoid RNA, not treated single-cell states.

The [Nb2 branch analyses](Research%20Article/gate2_N1_nabhan_2023/branch_analysis/README.md)
remain under `Research Article`, as the owner clarified. Their
[results](Research%20Article/gate2_N1_nabhan_2023/branch_analysis/RESULTS.md) and
paper-local candidate notes now inform the [29 September synthesis](Research%20Article/gate2_N1_nabhan_2023/RQ_DERIVATION.md).
It combines N1/N2/N3/N5 into A19, derives A20 from N6 and retains A21 from N7 at
conditional priority. N4/N8 remain paper-local pending comparable perturbation
evidence. The retired Nb2-RQ1–RQ8 identifiers are not restored. Only the new
question plans live under `RQ_Specified`; prior analyses stay with the paper.
A0–A18 keep their existing scopes. A19–A21 are proposed, not validated or approved
mechanisms; their contracts do not yet authorize confirmatory scoring.

## Hypothesis cards

<a id="a0"></a>

### A0. Is a conserved programme reused across epithelial transitions, and could it modulate fate?

**Hypothesis.** Different epithelia may reuse part of the cellular work needed to
leave an established identity and acquire another. A shared RNA component is one
possible observable consequence. Whether that component controls maturation,
persistence or reversibility is a separate causal question.

**Biological logic.** First establish the starting, intermediate and destination
populations from each study's biological context. Compare the intermediate with
both endpoints within mice or donors: a difference from the starting population
alone could measure ordinary acquisition of destination identity. Seek one shared
intermediate-enriched module in injury and normal development, then freeze it
before testing another epithelium. Challenge any transferable association with
stress, proliferation and measurement controls. Only matched perturbation and
fate endpoints could subsequently support modulation of fate.

**Current measurement.** The [A0 workspace](RQ_Specified/A0_conserved_epithelial_transition_program/README.md)
contains the original feasibility audit and the separately specified scientific
pilot. D1 is Strunz mouse alveolar repair; D2 is Sountoulidis human early airway
development; V1 is Haber mouse intestinal enterocyte commitment. These are
biologically distinct axes, not a single pooled trajectory. Source spatial and
developmental evidence supports the comparison but does not trace the future of
each sequenced cell. Read the [executed result and stopping decision](RQ_Specified/A0_conserved_epithelial_transition_program/reports/PILOT_V1_RESULTS.md)
before proposing any further score or module. Of 134 qualifying genes, 50 were
frozen. In three intestinal mice, the intermediate-minus-mature median is −0.0914
score points with only one positive mouse; the primary transfer rule fails.
Specificity work is pruned under the rule declared before V1 scores.

**Relation to established work.** A5's external developmental signature supports
partial recruitment in adult repair, not a universal transition machinery.
A5/A11's shared contract contains pairwise overlaps rather than one three-context
core. A1 addresses regulatory and response distinctions; A10 measures organoid
growth. Those results motivate A0 without supplying its cross-tissue transfer or
causal fate test. The [source recovery report](RQ_Specified/A0_conserved_epithelial_transition_program/reports/SOURCE_RECOVERY.md)
records the analysis precedents, cohort decisions and prior exposure.

**Scope of the decision.** The pilot requires 20–50 qualifying one-to-one orthologs
under fixed four-contrast criteria. Failing that operational prediction cannot
exclude a smaller shared component, conserved regulation with different RNA
outputs, or all possible transition processes. A positive transfer would remain
a state association. Neither outcome by itself resolves universality or fate.

<a id="a1-which-regulatory-and-phenotypic-features-distinguish-transitional-epithelial-states-beyond-rna-markers"></a>
<a id="a1"></a>

### A1. Do regulatory programmes distinguish RNA-similar transitional states and their functional responses?

**Hypothesis.** Transitional epithelia share part of an RNA response but differ
in regulatory programmes that help explain maturation, persistence or perturbation
response. DATP, PATS, Krt8 ADI, ABI/aberrant basaloid and HPCS remain source-defined
states; their names predetermine neither equivalence nor separate cell types.

**Our observation.** AT2 RNA loss survives the specified depth controls in two
same-laboratory deposits (C118). Distal-accessibility comparisons do not establish
closure or its timing (C131/C133). The completed
[first batch](RQ_Specified/A1_transitional_epithelial_state_distinction/reports/FIRST_BATCH_REPORT.md)
adds measured PATS endpoints, a separate ten-mouse IRE1α RiboTag contrast and
descriptive ATAC/CD44 profiles. Four of 14,811 genes pass whole-family FDR;
none of the predefined markers or eligible pathways does. The verified
[second batch](RQ_Specified/A1_transitional_epithelial_state_distinction/reports/SECOND_BATCH_REPORT.md)
adds directionally stable but significance-sensitive IRE1α effects, direct
histone profiles at 23 loci in two induced-cell preparations, and one-donor
methylation-domain context. Histone directions can depend on H3/window choice.
Recovered HPCS trace-linked RNA composition covers 5,333 cells / 22 sources;
the latest primary animal table resolves the mouse identities, while current
mScarlet remains unavailable.
The [robustness batch](RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ROBUSTNESS_REPORT.md)
shows promoter-dependent CDKN1A acetylation, source-sensitive HPCS fractions and
chase/library aliasing that prevents the proposed fixed-library-adjusted temporal
contrast. The [closure batch](RQ_Specified/A1_transitional_epithelial_state_distinction/reports/EVIDENCE_CLOSURE_REPORT.md)
recovers CD44's exact eight-mouse crosswalk and fits paired genotype contrasts
plus their direct interaction. Seven transported markers change in both
genotypes; four have detected effect-size interactions, although Sftpc's effect
nearly vanishes when WT2 is omitted. HPCS's author biological
map is now verified, and all stringent K12 changes are confidence abstentions.
The [regulatory/outcome continuation](RQ_Specified/A1_transitional_epithelial_state_distinction/reports/REGULATORY_FATE_REPORT.md)
resolves HPCS harvest timing and Tsutsui perturbation-library identities, and
reanalyzes AP-1 microscopy with fields nested within mice. HOPX responses have
opposite directions by lung region; culture program suppression and
differentiation capacity remain separate experiments. TP53 selected RNA lists
include shared and opposing responses across AT1/AT2 origins. These results
make origin and local context necessary parts of the proposed comparison.
The [reference map](RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md)
connects published precedents, dependent reanalyses and the next decision.
These within-context measurements do not establish an epigenetic taxonomy.

**Rivals and test.** A common regulatory continuum, distinct branches, and
different routes sharing stress RNA remain alternatives. Compare frozen
loci/programmes in compatible direct histone-mark or accessibility assays using
independent animals/donors and independent state definitions. Where observations
can be linked, test added information beyond RNA about measured protein,
lineage-descendant or perturbation endpoints. Separate studies triangulate;
they do not constitute a paired multiomic fate test. ATAC does not measure
histone marks, methylation or chromosome conformation.

**Decision / readiness.** A precise independent exclusion of the predefined
meaningful regulatory effect or added endpoint information retires that specified
discriminator. Incompatible callers, pooled identities or low replication leave
it inconclusive. The [plan](RQ_Specified/A1_transitional_epithelial_state_distinction/PLAN.md),
[assay map](RQ_Specified/A1_transitional_epithelial_state_distinction/STUDY_MAP.md)
and [lineage audit](RQ_Specified/A1_transitional_epithelial_state_distinction/LINEAGE_AUDIT.md)
govern the input gate. PATS track scaling and TIGIT pool membership remain
specific holds. HPCS animal identities and Hopx harvest are resolved; library/chase
confounding and the missing current reporter remain. CD44 count identities are
resolved. The [corrected comparison matrix](RQ_Specified/A1_transitional_epithelial_state_distinction/COMPARISON_MATRIX.md)
records that the regulatory primary test is not executable: the regulatory
predictor is unspecified and no cohort links it, early RNA and later mature
output in the same biological units. The IRE1 RNA-to-outcome candidate alone
would not satisfy this gate. The newer IRE1 cell-resolved cohort has one pooled library per
condition and cannot supply replicated treatment inference. Temporal closure or memory additionally needs actual
time/fate evidence (A14).

**Figures / contracts.** [Existing assay and endpoint panels](RQ_Specified/A1_transitional_epithelial_state_distinction/figures/README.md);
Descriptive direct-mark and descendant-source panels are available; independently
replicated regulatory/endpoint tests remain future work. [Depth panels](analysis/figures/rq/README.md#a1) are
supporting diagnostics. [MC1–MC2](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1).

<a id="a2-which-cells-express-areg-and-how-sensitive-are-candidate-rankings-to-the-resource"></a>
<a id="a2-does-the-functional-contribution-of-areg-sources-depend-on-tissue-context"></a>
<a id="a2"></a>

### A2. Does the fibroblast response to AREG depend on delivery or on abundance?

**Hypothesis.** AREG's contribution to a fibroblast response is set by where the
ligand is released relative to a competent recipient, rather than by how much of it a
compartment transcribes. The mechanism is short-range and recipient-licensed, so the
quantity that matters is the recipient's state and the ligand's point of release.

**Why this analysis moved beyond source ranking.** This card previously asked which source
dominates. Seven register rows answer that question and none establishes a
depth-independent epithelial hierarchy: the epithelial over myeloid contrast is
sensitive to annotation and molecule matching (C37), an epithelial source in
adenocarcinoma is not established because dendritic cells sit above both tumour states
(C39), those cells are a major source in their own right, a ranking in the opposite
direction (C45), tumour enrichment is refuted and fibrosis enrichment is not
established (C40, C48), and no donor-level correlation between epithelial AREG and
fibroblast EGFR or fibroblast activation was established (C49, C50). C51 records why a
further correlation on those variables would be unreadable: the one significant pair
in that trial tracked sequencing depth, and a frozen rule refused it.

**Mechanism.** Amphiregulin acts on a mesenchymal recipient through that recipient's
own EGFR, and the signal then activates integrin alphaV to release bioactive TGF-beta
from latent complexes, driving myofibroblast differentiation. The recipient in that
work is a PDGFRB-positive pericyte and macrophages are a critical source
([Minutti 2019](https://doi.org/10.1016/j.immuni.2019.01.008)). Silencing
amphiregulin or inhibiting EGFR reduces TGF-beta1-driven fibroblast proliferation,
smooth-muscle actin and collagen, and the amphiregulin silenced there is the
fibroblast's own ([Zhou 2012](https://doi.org/10.1074/jbc.M112.356824)). A
short-range ligand that converts a store the recipient already holds does not require
tissue-level ligand to be rate-limiting, so C49 and C50 do not refute the axis;
neither row is evidence for this framing either, and C49's point estimate is positive
and underpowered. Leukocyte amphiregulin can be non-redundant for lung protection
([Arpaia 2015](https://doi.org/10.1016/j.cell.2015.08.021)), and a review establishes
both epithelial and leukocyte sources
([Zaiss 2015](https://doi.org/10.1016/j.immuni.2015.01.020)), which is why C45
constrains an epithelium-only reading rather than refuting the axis.

**Rivals and test.** [Analysis A2](RQ_Specified/A2_areg_source_delivery/README.md)
holds the plan, the contract and the freeze that governs what may be computed.
Rivals: the recipient supplies the same ligand itself; another EGFR ligand carries the
response; the epithelial state rather than its ligand changes the fibroblast; the
epithelium activates TGF-beta through its own integrin; the fibroblast profile moves
with well composition or read depth. The organoid screen perturbs the mouse epithelium
only and leaves the human fibroblasts unedited, so it can compare an epithelial source
contribution against loss of epithelial reception and against loss of epithelial
integrin-mediated TGF-beta activation. It cannot separate delivery from abundance: a
single well holds one source compartment with no spatial variation, and recipient AREG RNA leaves an autocrine contribution plausible. Separately
normalized mouse and human RNA levels do not quantify relative secreted ligand supply.
A positive result would also be consistent with an abundance effect. Separating the
routes needs controlled presentation/proximity and dose; spatial RNA alone is insufficient.

**Decision / readiness.** Conditional and descriptive; both legs have now run and
neither settles the question. In the organoid screen the frozen fibroblast activation
score has a median difference of +0.036 log2 CPM in epithelial Areg-knockout wells against
depth-matched controls with two of four split wells in the predicted direction and an endpoint
standard deviation of 0.482. This does not establish a zero contribution: recipient AREG RNA is present,
the perturbation is partial, and regular medium contains recombinant EGF; well-specific ligand concentrations and preparation mapping remain unresolved (see P1). The normalized
RNA values do not measure the amount of ligand removed or secreted. The arm that moved is epithelial **Itgb6**, at a
median of -0.938 in three of three readable split wells, with small observed organoid-size and RNA-content differences in post hoc checks, which motivates an epithelial integrin-mediated activation hypothesis requiring its
own design; it does not choose that route over ligand supply. The donor-level leg was refused by the frozen
C51 depth rule at a composite depth coupling of 0.770, and has since been read: on a common
molecule budget the coupling falls to 0.232 and the correlation falls from 0.433 at nominal
p 0.044 to 0.293 at p 0.186. This is measurement sensitivity, not a proof of
absence or of how much was caused by technical depth. The
[interpretation correction](RQ_Specified/A2_areg_source_delivery/reports/INTERPRETATION_AUDIT_2026-09-27.md)
also withdraws the automatic recommendation to rerun at 100 molecules. The first freeze, which
declared a rank test with an exact null, is
[withdrawn](RQ_Specified/A2_areg_source_delivery/reports/STAGE2_WITHDRAWN.md). Read the
[synthesis](RQ_Specified/A2_areg_source_delivery/reports/STAGE5_SYNTHESIS.md). Secreted
ligand, receptor engagement (C36) and proximity remain outside the repository, and the
decisive delivery-versus-abundance contrast needs controlled source presentation,
ligand dose and recipient engagement, beyond spatial RNA proximity alone.
[Current figures](analysis/figures/rq/README.md#a2) are diagnostics.
[MC2 to MC4](docs/RQ_MEASUREMENT_CONTRACTS.md#mc2).

<a id="a3-which-macrophage-programmes-vary-with-phase-and-what-explains-the-differences"></a>
<a id="a3"></a>

### A3. Does prior injury leave a macrophage programme that differs from normal aging?

**Hypothesis.** Prior infection is associated with a late macrophage programme
or state distribution beyond changes expected with age alone.

**Our observation.** Late myeloid states and altered capillary composition
motivate a lasting tissue-response question. G1/W1 retain age and processing
confounding (C158). Reference CAMERA yields no significant W1 sets; its
seven-gene ornithine set is ineligible, not negative. See the
[sample-level analysis](analysis/corrections/statistics/README.md).

**Rivals and test.** Normal aging, recruitment/replacement, subtype mixture and
processing compete with an injury-history effect. Compare age-matched uninjured
and previously injured animals using harmonized states and an estimable
injury-history contrast. Report state fractions and within-state programmes.
Same-cell persistence requires tracing; metabolic flux requires a metabolic
endpoint. Neither follows from late RNA or relative fractions.

**Decision / readiness.** A matched design precisely excluding a predefined
meaningful effect retires the specified injury-associated programme. The current
confounded contrast cannot decide it. Age-matched data are the gate.
[Existing temporal panels](analysis/figures/rq/README.md#a3) describe sampling
after infection; desired primary plots compare animal-level effects with matched
controls. [MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1),
[MC5](docs/RQ_MEASUREMENT_CONTRACTS.md#mc5).

<a id="a4-how-do-current-wnt-activity-and-il-1-responsiveness-overlap-in-at2-cells"></a>
<a id="a4"></a>

### A4. Can Wnt-supported maintenance precede an IL-1-responsive transition in the same AT2 lineage?

**Hypothesis.** Wnt-associated maintenance and IL-1-associated transition can be
sequential states of a lineage rather than fixed opposing subsets.

**Our observation.** Transcript co-detection and Wnt/source profiles provide
feasibility information, not a measured sequence. [Nb1](Research%20Article/gate1_03_nabhan_2018/nb1/README.md)
starts at day 6 and has only one eligible baseline and one day-11 AT2 unit;
it cannot test an acute switch. Current activity, reporter history and sparse
Axin2/Il1r1 transcripts are different measurements.

**Rivals and test.** Stable subsets, concurrent signalling and selection of
different cells remain alternatives. Use a Wnt-history pulse/chase with reporter
washout, present pathway activity, IL-1 challenge and traced descendant/function
endpoints across independent animals. Separate fibroblast ligand sources from
epithelial receiver activity.

**Decision / readiness.** A precise absence of the predicted transition among
verified history-labelled responsive cells weakens the sequential model.
Sparse RNA overlap or an unverified reporter is inconclusive. Suitable
history/activity data are required. [Current figures](analysis/figures/rq/README.md#a4)
are screens; the desired figure is a lineage-linked activity/response time course.
[MC1–MC3](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1).

<a id="a5-which-transitional-signatures-are-specific-to-injury-rather-than-development-or-genotype"></a>
<a id="a5"></a>

### A5. Does adult alveolar repair reuse part of a developmental epithelial programme?

**Hypothesis.** Development and adult repair recruit a shared epithelial
remodelling component, with context-specific additions contributing to different
outcomes.

**Our observation.** Neonatal controls contain Krt8/Cldn4 co-detection at the
common depth budget (3.69%; C119). ES1's label-excluded ADI enrichment is
+1.04/+1.21 detection points in neonatal controls and +7.61/+6.53 in injured
adult controls across technical seeds. These positive within-well observations
motivate reuse without equating neonatal and adult injury states. Only one of
25 external-study animals passes both group floors. See
[ES1](Research%20Article/epithelial_state_specificity/README.md).

The [shared component contract](RQ_Specified/A5_A11_shared_component_contract/README.md)
sourced an outside developmental list, the signature of a mixed type 1 and type 2
population in normal lung at postnatal day 1 (Guo et al. 2019), and froze a
94-gene development-specific module, retained by the owner. At list level the
developmental list shares only five genes with the adult injury list, four of them
type 1 identity genes, and none with the lesion list. List overlap is a
conservative measure, so this does not show the programmes differ.

**Rivals and test.** Generic stress, cycling, age/genotype imbalance and shared
label genes can explain overlap. Freeze source-defined shared and context-specific
components excluding selection genes; test effects beyond generic stress/cycling
in independent developmental and injury contrasts. Use animals as units, retain
genotype and validate outside the component-selection data. Type 1-directed
identity is now the leading rival: 43 of the 94 development-specific genes are
type 1 or type 2 identity genes. A shared transcriptional component would also not
imply a shared route, since neonatal injury is reported to regenerate by type 1 to
type 2 reprogramming (Penkala et al. 2021).

**Decision / readiness.** The revised external Guo test is complete: 24 mice,
transitional versus activated AT2, mean +0.735 detection percentage points
(95% CI 0.579–0.892). Identity-excluded (57 genes) and identity/control-excluded
(53 genes) effects remain positive after Holm correction. This supports partial
transcriptional recruitment, not a shared lineage or repair outcome. The original
94/51-gene modules were filtered with Strunz test-cohort markers and are descriptive
there. Strunz's published poor overall developmental correspondence remains relevant
counterevidence to global equivalence. [Plan](RQ_Specified/A5_developmental_programme_reuse/PLAN.md);
[results and biological interpretation](RQ_Specified/A5_A11_shared_component_contract/reports/REVISED_TEST_RESULTS.md).
A [new independent-cohort recovery](RQ_Specified/A5_developmental_programme_reuse/replication_gate_20260928/REPORT.md)
identifies GSE303646's author Krt8-ADI/activated-AT2 vocabulary and 56 library records.
The barcode-to-state/mouse map and 55-mice/56-libraries discrepancy remain unresolved;
no unchanged external score was computed.
[Current figures](analysis/figures/rq/README.md#a5) motivate animal-level
shared-versus-specific effects and held-out evaluation.
[MC1–MC2](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1), [MC5](docs/RQ_MEASUREMENT_CONTRACTS.md#mc5).

<a id="a6-how-much-of-the-ipf-macrophage-proliferation-signal-is-composition-and-what-remains-within-a-shared-noncycling-state"></a>
<a id="a6"></a>

### A6. Does IPF alter shared macrophage states beyond changing their abundance?

**Hypothesis.** IPF has a within-state macrophage programme component in addition
to changes in resident, recruited and proliferating cell proportions.

**Our observation.** Validation-cohort proliferating macrophage fractions average
3.77% in IPF versus 2.11% in controls. Cell and programme-RNA contributions differ,
motivating a biological decomposition. Only three IPF donors and one control
exceed the proliferating-state floor, and cohort labels are not harmonized.
[Existing enrichment](analysis/corrections/statistics/README.md) does not establish
the within-state hypothesis.

**Rivals and test.** Mixture alone, inconsistent annotation and batch effects
compete with a within-state change. Harmonize states independently of the tested
programme, compare donor pseudobulks under a frozen composition standard, and
replicate across cohorts. Do not define “noncycling” solely with the score tested.

**Decision / readiness.** A replicated effect supports the within-state component.
A narrow interval inside a prespecified equivalence margin supports a
composition-only explanation for that programme; nonsignificance does not.
Harmonization and donor coverage are gates. Extend the
[composition panels](analysis/figures/rq/README.md#a6) to donor-level standardized
effects and intervals. [MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1),
[MC3](docs/RQ_MEASUREMENT_CONTRACTS.md#mc3), [MC5](docs/RQ_MEASUREMENT_CONTRACTS.md#mc5).

<a id="a7-does-cebpa-genotype-shift-the-reference-at2-population-and-compress-the-apparent-transitional-contrast"></a>
<a id="a7"></a>

### A7. Does Cebpa loss attenuate AT2 identity across states or preferentially within a transitional state?

**Hypothesis.** Cebpa loss reduces identity across AT2 states, so the smaller
transitional–reference contrast partly reflects a changed reference rather than
selective preservation of intermediates.

**Our observation.** Both reference identity and labelled–reference differences
decrease in mutant wells (C167). The P9 contrast changes from -4.59/-4.79 points
in controls to -0.70/-0.31 in mutants across technical seeds; adult injured wells
show the same qualitative compression. This motivates a genotype-wide effect,
but one well per condition cannot establish an interaction. See
[ES1](Research%20Article/epithelial_state_specificity/README.md).

**Rivals and test.** State-selective effects, genotype-dependent reference
selection and sampling remain alternatives. Estimate genotype effects in both
states and their interaction in replicated age-matched animals. Define states
independently of Sftpc and scored identity genes.

**Decision / readiness.** Comparable shifts with a precisely bounded interaction
support broad attenuation; a replicated meaningful interaction supports a
state-selective component. Both can coexist. Current one-well measurements are
descriptive. Extend [two-population plots](analysis/figures/rq/README.md#a7) to
animal effects and interaction intervals. [MC1–MC3](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1).

<a id="a8-does-a-broad-at1-score-capture-shared-transition-programmes-rather-than-late-maturation"></a>
<a id="a8"></a>

### A8. Does a maturation-specific programme add information about mature AT1 contribution beyond shared transition?

**Hypothesis.** A component beyond shared transition provides additional
information about measured mature AT1 contribution.

**Our observation.** ADI and AT1 holdout lists share 119 genes, and the small
late-AT1 panel is seed-sensitive (C168). This definitional dependence motivates
separation but is weak biological evidence. It does not show that mature AT1
identity is merely an extension of transition.

**Rivals and test.** Shared transition alone, timing, mixture or measurement
quality may explain the endpoint. Freeze disjoint/shared components and test
incremental association or prediction against measured AT1 protein, morphology
or traced descendant yield in independent animals. Do not define both predictor
and “mature” outcome with the same RNA panel.

**Decision / readiness.** Added information that transports supports the nominated
component; a precise absence of a meaningful increment weakens it. Missing
independent endpoints or imprecision is inconclusive. The
[A1 lineage audit](RQ_Specified/A1_transitional_epithelial_state_distinction/LINEAGE_AUDIT.md)
guides sourcing. [Overlap figures](analysis/figures/rq/README.md#a8) are diagnostics;
desired panels compare component effects and held-out endpoint performance.
[MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1), [MC5](docs/RQ_MEASUREMENT_CONTRACTS.md#mc5).

<a id="a9-does-apparent-egfr-ligand-specificity-reflect-receiver-biology-or-receptor-representation-and-coverage"></a>
<a id="a9"></a>

### A9. Does fibroblast receptor context determine the response to AREG?

**Hypothesis.** Receptor abundance and complex competence modify fibroblast
responses to a defined AREG exposure.

**Our observation.** Exact EGFR and EGFR_ERBB2 definitions have different donor
coverage: the complex is scored in 7/22 donors, below the 11-donor retention rule.
This nominates a competence question and identifies a measurement prerequisite;
it does not measure dimer composition or support EGFR-homodimer predominance.

**Rivals and test.** Resource representation, depth, fibroblast mixture and
other pathways compete with receiver biology. Following a within-state RNA
screen, measure receptor protein/activation and matched ligand responses under
receptor-specific perturbation across independent preparations. Complex
composition needs an appropriate direct assay.

**Decision / readiness.** A receptor-specific outcome change with verified
engagement supports context dependence; its precise absence weakens the nominated
mechanism. RNA/resource discordance cannot decide it. The
[ligand report](analysis/corrections/ligand/RESULTS.md) and
[coverage panels](analysis/figures/rq/README.md#a9) support screening; primary
future panels are protein/activation and functional contrasts.
[MC3–MC4](docs/RQ_MEASUREMENT_CONTRACTS.md#mc3).

<a id="a10-do-epithelial-perturbation-responses-predict-organoid-growth-and-fibroblast-responses-across-independent-preparations"></a>
<a id="a10"></a>

### A10. Do epithelial programmes add information about measured organoid growth?

**Hypothesis.** Epithelial perturbation programmes add information about growth
beyond baseline imaging and plate effects; fibroblast response programmes may
provide a separate increment.

**Observation.** GSE307112 provides species-separated epithelial/fibroblast RNA
and well-linked imaging. The [revised analysis](RQ_Specified/A10_organoid_growth_outcome/reports/STAGE4_REVISED_REPORT.md)
uses 885 wells in 15 deposited plate-replicate groups. Epithelial growth programmes
add 0.0426 under the within-unit metric, above the declared 0.02 margin in all
four sensitivity settings. The fibroblast increment is -0.0154. Only 8/15 groups
have a positive epithelial increment, with the pooled result concentrated in
plates 1 and 3. The [dataset gate](docs/NEXT_DATASET_GATE.md) preserves the initial
selection rationale; it is no longer the next unexecuted task.

The [completed follow-up](RQ_Specified/A10_organoid_growth_outcome/reports/FOLLOWUP_RESULTS.md)
finds only four targets shared between plates; 886 GEO sample records still lack
preparation IDs. The six growth scores add beyond E2F/G2M: 4.84% less reference
squared error within groups and 36.96% less under joint plate/target shift.
Full-growth plate-shift improvement is 42.39%, positive in each held-out plate,
but absolute R-squared is negative on 3/4 plates. These percentages use a new
reference-error metric, not the original delta-R-squared. Both fixed outcome
scales and the drop-both sensitivity support the conditional addition.

**Rivals and test.** Initial size, plate/preparation, guide effects or mixture
may explain growth. The completed analysis joined well metadata and fixed day-14
area conditional on day-7 area; number/coverage were nominated as secondary
endpoints, not substituted for the primary. Entire deposited groups were held
out, but independent preparations remain unidentified. Outcome-time RNA supports
concurrent association. The target-transcript check is a limited diagnostic,
not validation of all perturbations or of a positive-control imaging response.

**Decision / readiness.** The revised rule is met descriptively, not as independent
confirmation: it followed the first analysis on the same screen, and centring
uses each held-out group's own outcome mean. The grouping labels do not establish
independent preparations. No confidence bound establishes precise absence of a
fibroblast contribution. Organoid mean area measures size/morphology, not total
tissue production, mature AT1 fate or in vivo repair. The follow-up comparisons
are complete and remain descriptive. Additional model/target extensions were
pruned: resolve preparation mapping, imaging calibration and a matched validation
design before another model-selection cycle.
[Original design schematic](analysis/figures/rq/README.md#a10);
[MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1),
[MC5](docs/RQ_MEASUREMENT_CONTRACTS.md#mc5).

<a id="a11-shared-plasticity-versus-neoplasia-associated-context"></a>
<a id="a11"></a>

### A11. Which lesion-associated programmes add to a shared epithelial plasticity component?

**Hypothesis.** Neoplasia-associated epithelial states contain a shared
remodelling component plus context-associated additions distinguishable from
non-neoplastic repair and fibrosis.

**Our observation.** The overlap-reduced HPCS score rises in 7/7 pooled
repair/development libraries, 3/3 IPF donor pairs and 19/23 LUAD paired comparisons
(mean +0.327 log2 CPM). This positively motivates shared transcriptional biology;
it establishes neither one cell identity nor the absence of lesion-specific
additions. The [evidence review](Research%20Article/gate2_C3_yu_lee_choi_min_2026/EVIDENCE_REVIEW.md)
preserves each context's units and limitations. The 0.327 figure is the discovery
run's broad type 2 compartment; its narrower type 2 label gives 0.323 with the same
19 positive patients.

The [shared component contract](RQ_Specified/A5_A11_shared_component_contract/README.md)
froze a lesion-specific module that is identical, gene for gene, to this
overlap-reduced score, so the 23-patient result is discovery and cannot also
evaluate. At list level the adult injury programme shares seven genes with the
lesion list, mostly stress genes such as the p53 targets Bax and Gdf15, and the
developmental list shares none.

**Rivals and test.** Generic stress, cycling, annotation and composition can
mimic sharing or specificity. Define shared and candidate context-associated
components in discovery data, then evaluate frozen additions in independent
within-study contrasts with paired patients and supported epithelial states.
Require independent identity evidence before calling a cell malignant;
histology groups are not longitudinal progression stages.

**Decision / readiness.** The amended Kim test is complete after reproducing all
46 broad/narrow discovery contrasts. All eight patient differences are positive:
HL +0.681 log2 CPM (exact 95% CI 0.386–0.976; p=0.0078125), with the interval above
the pragmatic 0.10 margin. Stress exclusion remains positive (BH q=0.0234), but
beyond-shared does not meet its declared threshold (HL +0.549; CI −0.034–1.063;
BH q=0.0547). Thus lesion association replicates and the stronger relative-activation
criterion remains unresolved. Changed population definition and lack of a
non-neoplastic injury comparator limit specificity claims. [Plan](RQ_Specified/A11_lesion_programme_addition/PLAN.md);
[results](RQ_Specified/A5_A11_shared_component_contract/reports/REVISED_TEST_RESULTS.md).
[Current PCA/paired panels](analysis/figures/rq/README.md#a11)
motivate disjoint-component heatmaps and held-out patient effects.
[MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1), [MC3](docs/RQ_MEASUREMENT_CONTRACTS.md#mc3),
[MC5](docs/RQ_MEASUREMENT_CONTRACTS.md#mc5).

A [second assay under A11](RQ_Specified/A11_lesion_programme_addition/reports/ACUTE_INJURY_RESULTS.md)
asks whether the same frozen module rises in acute injury, which would challenge a tumour-associated
reading. In GSE198864 lung explants it is higher in SARS-CoV-1 infected than in medium-matched mock
type 2 cells by +0.225 log2 CPM across three identity-concordant paired donors, positive in all
three, at an exact p of 0.25 which is the floor at that unit count; the beyond-shared contrast is
-0.039, so the rise is not separable from the shared component, and the cells scored are bystanders
at 5 viral reads in 1,039 cells. Unresolved, and tumour specificity is untouched in either
direction. This paragraph was moved from A13 on 28 September 2026; its results are unchanged.

<a id="a12-recipient-context-and-il-1-specificity"></a>
<a id="a12"></a>

### A12. Does recipient receptor and inhibitor context explain responses beyond IL-1 ligand RNA?

**Hypothesis.** Fibroblast and epithelial receptor/inhibitor context contributes
to recipient programme variation beyond source IL1A/IL1B RNA and subtype mixture.

**Our observation.** IL1B compatibility differs between IPF cohorts and human
target fits vary by recipient. These patterns motivate a recipient model;
different rank denominators cannot establish stronger signalling. Human pathway
results yield 0/279 significant primary estimated-correlation tests versus
148/279 under fixed-0.01 sensitivity. The primary result remains primary.

**Rivals and test.** Ligand amount, mixture, shared inflammation and alternative
ligand families compete with the recipient explanation. Within supported states,
compare a frozen source-only model with a parsimonious receptor/inhibitor
extension using verified patient/donor units. Include IL1R1/IL1RAP and regulatory
components; retain alternative ligands, pathway eligibility and omission
sensitivity. Ligand–receptor inference and pathway enrichment explicitly support
this analysis. IL-1 specificity needs activation or selective perturbation data.

**Decision / readiness.** Replicated added information supports an association;
a precisely excluded meaningful increment weakens it. Ineligible targets or
insufficient matched units leave it unresolved. The
[methods/report](analysis/figures/rq/il1b_context/REPORT.md) and
[component, enrichment and target figures](analysis/figures/rq/README.md#a12)
are complete. A [new exploratory conditional pilot](docs/roadmap_runs/2026-09-27-followthrough/A12_PILOT.md) now ran on fixed candidate states with a gene-disjoint inflammatory RNA response and TNF comparator: AT2 RMSE fell from 0.4271 to 0.3244, while the fibroblast increment was unstable. Independent cohort validation and activation/perturbation are still required.
The [28 September recovery](RQ_Specified/A12_recipient_context/external_validation_20260928/reports/RECOVERY_REPORT.md)
closes three candidate gates: Kim has zero tumour AT2-labelled cells, Laughney has
at most four possible pairs, and Wu lacks a separate normal arm. No external fit ran.
[MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1), [MC3–MC5](docs/RQ_MEASUREMENT_CONTRACTS.md#mc3).

<a id="a12-s1"></a>

**A12-S1, an enabling source-identity question.** Unassigned cells carry median
52–72% of recovered IL1B counts across human histologies. Resolving their identity
can change source attribution; an unknown label does not define a new macrophage
state. Retain this question in the [annotation contract](docs/RQ_MEASUREMENT_CONTRACTS.md#a12-s1)
and [source gallery](analysis/figures/rq/README.md#a12-s1). Cytokine secretion is
a separate measurement.

<a id="a13-fibroblast-context-and-reciprocal-niche-associations"></a>
<a id="a13"></a>

### A13. Do fibroblast programmes add information about epithelial plasticity beyond macrophage IL1B?

**Hypothesis.** Fibroblast inflammatory/recruitment, matrix and trophic programmes
contribute information about epithelial plasticity beyond macrophage IL1B RNA.

**Motivation.** Heterogeneous niche associations motivate a joint model, but
completed analyses establish neither fibroblast mediation nor reciprocal feedback.
See the [human niche report](Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_niche/REPORT.md).

**Rivals and test.** Shared inflammation, histology, capture composition and
macrophage state can explain apparent fibroblast information. Count complete
macrophage–fibroblast–epithelial triads for the exact variables and contrast.
Freeze a small programme/multiplicity family, then compare parsimonious joint
models using within-patient changes where available. Marginal correlations do
not test “beyond IL1B.” Spatial work requires independently defined pathology
regions and a patient-level null; feedback requires intervention.

**Decision / readiness.** Replicated added information supports the association;
precise absence weakens the nominated programme. IPF has six and three complete triads,
below the ten-unit joint-model floor; 23 human cohort patients does not mean 23 complete
paired triads. **The historical coverage gate for the inspected IPF/Kim definitions is not met**
([results](RQ_Specified/A13_fibroblast_beyond_macrophage_il1b/reports/COVERAGE_RESULTS.md)):
the one uncounted cohort on disk gives zero complete paired triads at the 50-cell floor under
the epithelial definition the IPF cohorts used, and three under a wider one. The zero is
definitional, because every tumour sample there holds zero cells labelled type 2, so a paired
tumour-versus-normal contrast and a type 2 epithelial compartment are incompatible in that
deposit at any cohort size. Under the wider definition fibroblast recovery binds, at a median
of 32.5 cells for the largest fibroblast label. Nothing was fitted, and a joint model should not
be fitted on this coverage. This finding is confined to the inspected datasets and
definitions; different capture, sampling or more independently eligible patients can
change coverage. The ten-unit floor does not itself establish power or model adequacy.

A [separately frozen GSE308103 pilot](docs/roadmap_runs/2026-09-27-followthrough/A13_PILOT_AND_COVERAGE.md) subsequently verified 12 paired triads with fixed AT2 and alveolar-fibroblast labels and explicit broad assigned macrophages, an amended compartment rule. Adding the frozen fibroblast RNA programme worsened primary held-out RMSE from 0.2283 to 0.2373 and worsened every eligible sensitivity. It is not independent confirmation or a test of feedback. The two external candidates are resolved: GSE233844 is blood; author annotations for GSE122960 fail the ten-unit gate.
[Figure plan/spatial evidence](analysis/figures/rq/README.md#a13): coverage heatmap
first, then patient effects if eligible. [MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1),
[MC3–MC5](docs/RQ_MEASUREMENT_CONTRACTS.md#mc3).

<a id="a14-resolution-versus-persistence-after-signal-withdrawal"></a>
<a id="a14"></a>

### A14. Do exposure duration and fibroblast IL-1 reception separately determine recovery after withdrawal?

**Two hypotheses, separate decisions.** Longer IL-1β exposure reduces mature
epithelial recovery after withdrawal. Separately, fibroblast IL-1 reception
modifies recovery beyond direct epithelial reception. Either can hold without
the other.

**Motivation.** Shared RNA cannot distinguish reversible repair from persistent
dysfunction. This is a mechanistic follow-up, not an existing withdrawal-fate
result. Published tracing informs the design but cannot replace that experiment.

**Rivals and test.** Residual exposure, toxicity, death/replacement and an
epithelial-only response compete with duration and fibroblast dependence.
Compare transient/sustained exposure and verified withdrawal with time-matched
controls and epithelial- versus fibroblast-specific IL1R1 perturbation. Use
independent animals or culture preparations. Measure mature-cell yield, viability,
traced descendants and function alongside exposure and target engagement, with
comparable post-withdrawal intervals. Loss of a transitional score cannot by
itself distinguish maturation, reversion, death or replacement.

**Decision / readiness.** A recovery difference after verified withdrawal
supports the duration hypothesis; an outcome change under fibroblast-specific
intervention with controlled direct epithelial reception supports the second.
Precise absence weakens each separately. Failed engagement or no withdrawal
observation is inconclusive. Appropriate new data are needed; neither result
alone establishes malignant transformation.

**Figures / contracts.** [Existing design schematic](analysis/figures/rq/README.md#a14);
future primary panels: replicate-level recovery, mature-cell yield and
recipient-specific contrasts with exposure/engagement controls. No anticipated
response curve is a result. [MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1),
[MC3–MC4](docs/RQ_MEASUREMENT_CONTRACTS.md#mc3).

<a id="a15"></a>

### A15. Does the epithelial input to fibroblast activation run through the integrin or through the ligand?

**Proposed 27 September 2026, and pending the owner's retain or reject.** This card is
assistant-proposed wording. It grades nothing, adds no claim row, and carries no result of
its own. The argument for and against the identifier, with three rejected alternatives,
is in [reports/REGISTER_DECISION.md](RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/REGISTER_DECISION.md).

**Hypothesis.** Where an epithelium and a fibroblast share a matrix, the epithelial
contribution to the fibroblast myofibroblast and collagen programme is carried by
epithelial integrin alphaVbeta6 converting latent TGF-beta that is already present, rather
than by epithelial supply of an EGFR ligand. Three predictions can each fail alone:
removing epithelial ITGB6 lowers the fibroblast programme while removing epithelial ligand
supply does not, in a system where the recipient's own ligand is also removed; the same
removal lowers **activated** TGF-beta at the recipient; and blocking TGF-beta receptor
signalling in the recipient abolishes the effect.

**What is not being asked.** That integrin alphaVbeta6 binds the TGF-beta1
latency-associated peptide and activates latent TGF-beta in a spatially restricted way is
established ([Munger 1999](https://doi.org/10.1016/s0092-8674(00)80545-0)), the integrin is
overexpressed on pneumocytes in human pulmonary fibrosis and a blocking antibody prevents
murine bleomycin fibrosis ([Horan 2008](https://doi.org/10.1164/rccm.200706-805OC)), and
two sources of active TGF-beta are already proposed, the epithelial integrin and an
amplifying alphaV integrin on the activated fibroblast itself
([Sheppard 2015](https://doi.org/10.1513/AnnalsATS.201406-245MG)). This repository does not
re-ask any of that. What it owns is the **partition of the epithelial output**, which the
cited work does not test: epithelial ligand supply against epithelial integrin activation
in one system with an autocrine-competent recipient.

**Observation.** A2's leg 1 produced the lead as an unplanned result. In the GSE307112
alveolosphere screen, epithelial **Itgb6** knockout wells sit a median of -0.938 log2 CPM
below their unit's depth-matched controls on the frozen five-gene fibroblast activation
score, in three of three readable split wells, against an endpoint standard deviation of 0.482;
it survives the epithelial-fraction adjustment at -0.992, with organoid size within 0.022
log units of controls and fibroblast content at 0.93 of theirs, while the Erbb3 decrease
fails that same check. The ligand arm gives +0.036 in two of four split wells. Read
[A2 stage 3](RQ_Specified/A2_areg_source_delivery/reports/STAGE3_LEG1_RESULTS.md) and
[A2 stage 5](RQ_Specified/A2_areg_source_delivery/reports/STAGE5_SYNTHESIS.md). **That
observation is confounded motivation for A15, not a demonstrated mechanism.**
It belongs to A2's measurement record and supplies neither an inherited grade
nor independent confirmation of the new interpretation.

**Rivals and test.** The strongest rival is fibroblast-side amplification: if the
recipient's own alphaV integrins do most of the activating, the epithelial step is not the
rate-limiting input. Next is the epithelial state itself, since Itgb6 loss changes the
epithelium in vivo, producing Mmp12-dependent emphysema
([Morris 2003](https://doi.org/10.1038/nature01413)) and altered surfactant and collectin
homeostasis ([Koth 2007](https://doi.org/10.1165/rcmb.2006-0428OC)). Then generic
perturbation effects, plate position and guide pool, well composition and depth, the latent
pool and TGF-beta isoform, and the unverified assumption that a mouse integrin activates a
latent complex read by a human recipient. The test needs an epithelial integrin
perturbation with at least three independent units per arm, positions that vary, a
separated fibroblast readout, a bounded ligand arm, and **activated TGF-beta measured as
protein or receptor-proximal signalling**. The
[eligibility gate](RQ_Specified/A15_epithelial_integrin_tgfb_activation/PLAN.md) is frozen
before any candidate is opened.

**Decision / readiness.** **Blocked, and the blocking constraint is nameable.** A search of
GEO, PRIDE, the Image Data Resource and the BioImage Archive found no deposit pairing an
epithelial integrin perturbation with a measurement of activated TGF-beta
([search report](RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/PUBLIC_DATA_SEARCH.md)).
The nearest, GSE190821, blocks integrin beta6 in vivo with four treated against seven
antibody-control mice but reads whole lung and epithelium only, so it fails the separated
recipient and the activation readout, and it has no ligand arm. One bounded side-branch was authorized by the owner on
27 September 2026 and has run. In GSE190821, 3G9 anti-integrin-beta6 lowered a frozen
whole-lung collagen and myofibroblast programme by 1.2424 standardised units with complete
separation of four treated from four control mice, reproducing the published direction for
this antibody, while in the same mice the epithelial immunoprecipitation showed no detectable
difference in a frozen transitional panel (-0.3599, p 0.8857), a frozen identity panel
(-0.2107, p 0.6857) or a 15,062-gene omnibus statistic (p 0.6571), with epithelial enrichment
differing between arms by at most 0.294 log2 units. Its historical frozen label is **weak bound on rival 2**. Current interpretation
is that the epithelial-state rival remains unresolved: enrichment does not establish
purity or fixed subtype composition, and the intervals permit large shifts. Read the
[interpretation and gate clarification](RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/INTERPRETATION_AUDIT_2026-09-27.md)
before using this result. It is not a mediation test. Two freezes were withdrawn on adversarial review before
anything was scored. Read [the results](RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/RIVAL2_RESULTS.md). The clinical record bounds any answer
in advance, because an anti-alphaVbeta6 antibody trial in idiopathic pulmonary fibrosis
terminated early without benefit and with more serious adverse events
([Raghu 2022](https://doi.org/10.1164/rccm.202112-2824OC)), while a dual alphaVbeta6 and
alphaVbeta1 inhibitor was better tolerated with exploratory signals
([Lancaster 2024](https://doi.org/10.1164/rccm.202403-0636OC)); a positive answer here would
be a statement about which epithelial output moves a fibroblast programme, not about
whether blocking it helps a patient.
A [versioned normalization erratum](RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/NORMALIZATION_ERRATUM_2026-09-28.md)
replaces the double-normalized sensitivity. Corrected transitional and identity
contrasts remain nonseparating; the identity point estimate changes sign. The CPM
primary and historical algorithmic label are preserved, with mediation unresolved.
[MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1),
[MC2 to MC4](docs/RQ_MEASUREMENT_CONTRACTS.md#mc2).

<a id="a16"></a>

### A16. Does CD177 identify a priming phenotype within comparable mutant cells?

**Proposed 28 September 2026; pending the owner's retain or reject.** Current
wording amended by the [source/code audit](docs/audits/2026-09-28-england-paper-rqs/REPORT.md).
No claim grade or completed functional result is added.

**Hypothesis and biology.** Within the same transitional compartment, CD177
may identify cells with a priming-associated programme beyond the local mixture
of epithelial states. Such a phenotype could help explain the source's mixed
mutant state. A stable cell-intrinsic programme and a neighbourhood-associated
phenotype can coexist; RNA alone cannot distinguish their persistence or function.

**Current evidence.** The source supports a CD177-associated mutant state and
functional plasticity of sorted states. It does not establish CD177-specific
necessity. The marker is scarce in the compared in-vivo repair dataset, but the
same paper induces it in WT inflammatory organoids (Figure S7); it is not
universally mutant-exclusive. FU_A preserves several effect directions under
available depth adjustments, but its frozen verdict is inconclusive: one
thinning arm has 26 positive cells, below the required 30. SMD ratios do not
measure a percentage of biological signal retained. FU_C then pools libraries
and drops the original transition gate, so its seven-cluster result cannot be
read as the same comparison conditioned on neighbourhood.

The audit's post-hoc diagnostic preserves the original two libraries, gate and
30-per-side floor. Two strata qualify: priming SMD +2.105 in GSM7890835/cluster
18 and +0.069 in GSM7890836/cluster 16. These are different neighbourhoods with
outcome-informed labels, not independent validation or proof of a common residue.
The [saved diagnostic](docs/audits/2026-09-28-england-paper-rqs/a16_same_population_effects.csv)
does not execute the separate A16 Stage 1 plan.

**Prediction, rival and decision.** A consistent association within separately
analysed libraries and independently defined comparable states would nominate
a CD177-associated RNA phenotype. Disappearance with valid conditioning would
favour state composition, but could also reflect removal of genuine biology
encoded by the clustering. Depth, ambient RNA and RNA/protein mismatch remain
rivals. Independent surface-marker and outcome linkage is needed for the
stable/functionally distinct phenotype; snapshot cell-cycle RNA is insufficient.

**Stage 1 now integrated.** The subsequently reviewed [A16 workspace](RQ_Specified/A16_cd177_state_attribution/README.md)
contains executed C1–C5 sensitivities and their two-arm population amendment.
Specificity remains inconclusive; seven of nine entries have fewer than 40
matched controls. The panel adjustment does not exclude contamination, and all
four thinned-depth rows in the two primary libraries fail the cell floor. UMAP
matching is a declared substitute for the frozen space; the two arms do not
make the original population comparison nested. The [integration review](RQ_Specified/A16_cd177_state_attribution/reports/INTEGRATION_REVIEW.md)
supersedes the old report's stronger exclusions without changing its numbers.

**Readiness.** Partly measured and inconclusive. A separately frozen
[corrected C1 comparison](RQ_Specified/A16_cd177_state_attribution/correction_20260928/reports/CORRECTED_C1_REPORT.md)
now retains each library's original transition population and excludes grouping,
gate and outcome genes before constructing its local PCA neighbourhoods. Priming
raw differences attenuate from 1.2558 to 0.4098 and from 1.3318 to 0.3151 at k=10.
Substantial residual PC imbalance remains; positive residuals do not establish
specificity or intrinsic biology. This executes C1's computational amendment,
not the full attribution or functional test, and preserves original Stage 1.
The full functional test remains data-limited. GSE253461 and GSE316244 are
conditional external candidates with differing genotype/culture and pooling,
not independent confirmation. [E-N5/E-N6](Research%20Article/gate2_C2_england_2025/CANDIDATE_HYPOTHESES.md)
separate maturation and second-hit hypotheses from marker transfer.
[MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1),
[MC2–MC3](docs/RQ_MEASUREMENT_CONTRACTS.md#mc2).

<a id="a17"></a>

### A17. Do persistent founder differences help explain unequal mutant clone growth?

**Proposed 28 September 2026; pending the owner's retain or reject.** The
biological question is retained; the simulator correction is its enabling check.

**Hypothesis and biology.** Persistent differences between founder lineages
contribute to the unequal expansion of mutant AT2 clones. A discrete fast/slow
model is one representation. Continuous variation, reversible state changes,
survival selection and clone merger can also generate unequal clone sizes.
England's Figures 1–2 and Il1r1 lineage experiments motivate founder differences;
the Discussion explicitly retains a single-hierarchy possibility. A fitted
mixture does not independently identify immutable cell types.

**Current evidence.** The deposited slow-loss event branch is unreachable in
the q=0.7 setting audited by EN6; literal and corrected-branch distributions
differ (KS 0.104, 0.281 and 0.281 at one, two and four weeks). This confirms an
implementation problem, not which implementation generated the published
curves. Methods S1 also fits analytical biexponential distributions, and the
paper has independent lineage evidence. Neither is refuted by that code defect.
Batch1's alternative distribution fits are not a completed corrected stochastic
refit. The [audit](docs/audits/2026-09-28-england-paper-rqs/REPORT.md)
also records Table S1/archive mouse-count and parameter discrepancies.

**Prediction, rival and decision.** A correctly specified discrete model should
retain useful held-out predictive advantage over a continuous alternative and
identify its parameters adequately. Comparable prediction or weak
identifiability leaves founder structure unresolved. Lack of advantage rejects
that model's claimed discrimination, not every biological founder difference.
Report survivor/expanded-clone fractions separately from initial founder
fractions; [E-N3](Research%20Article/gate2_C2_england_2025/CANDIDATE_HYPOTHESES.md#e-n3)
develops the survival rival.

**Readiness.** Computation is feasible with existing inputs, but FU_S has not
run and needs an explicit amendment: reconcile source units and parameter
symbols, specify rate changes/switching times, and score both model families
on the same held-out bins/folds, with a separately specified tail diagnostic.
The existing [FU_S contract](Research%20Article/gate2_C2_england_2025/config/followup_contract.json)
is preserved as the original proposal. Unchanged best-fit parameters alone
would not close the question. [MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1).

The [28 September raw-source reconciliation](docs/roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md)
reproduces all 58 saved mouse/analysis-channel count rows and traces the deposited
fast/slow argument mapping and rate switch. The primary input contains 11
source-indexed mice. Printed-table and manuscript/curve-provenance discrepancies
remain explicit; no stochastic refit ran.

<a id="a18"></a>

### A18. Are WT expansion and loss of AT2 identity regulated differently near mutant clones?

**Proposed 28 September 2026; pending the owner's retain or reject.**

**Hypothesis and biology.** Mutant tissue influences WT cell expansion and AT2
identity through partly separable controls. The source's different spatial
patterns motivate this hypothesis, but do not identify two mediators or their
ranges. SPP1/DLK1 have direct source organoid motivation (Figure S6Q–V); AREG,
relay signalling and mechanical effects are alternatives. Ligand RNA abundance
or ligand class cannot assign an in-vivo signalling distance.

**Current evidence.** Source Figures 5–6 support altered WT growth and identity.
FU_W reproduces pooled size and pro-Sftpc profiles and checks bin occupancy and
scale. The identity-loss slope is noisy and inconsistent in sign; that does not
establish distance independence. Pair rows omit mouse/clone identifiers, may
repeat neighbours and become sparse at distance. Log-size/logit-fraction
transformations do not restore replication or make biological effects directly
interchangeable. Cell fractions around 0.2–0.3 do not establish saturation.
The source's mutant-cell EdU results are not a WT distance-dependent division test.

**Prediction, rival and decision.** With identified mice/clones, WT expansion
and identity loss should retain distinguishable distance associations after
accounting for sampling geometry, repeated neighbours and clone merger. A common
response distorted by different readout sensitivities remains a rival. Compare
predicted changes on meaningful scales with uncertainty; a distance-by-readout
interaction alone would still not identify separate causal signals. Source
necessity and recipient response require separate evidence.

**Readiness.** Descriptive profiles are complete. Animal-level spatial inference
is blocked pending identifiers or suitable new data. Nonspatial mouse-indexed
arrays do exist and permit the narrower [E-N1/E-N2](Research%20Article/gate2_C2_england_2025/CANDIDATE_HYPOTHESES.md)
questions. E-N8 develops SPP1/DLK1 interaction. Neither these analyses nor a new
RNA fit would show whether WT responses promote or restrain tumour progression.
No author was contacted. [Source audit](docs/audits/2026-09-28-england-paper-rqs/REPORT.md),
[MC1](docs/RQ_MEASUREMENT_CONTRACTS.md#mc1),
[MC3–MC4](docs/RQ_MEASUREMENT_CONTRACTS.md#mc3).

<a id="a19"></a>

### A19. Can transient Fzd signaling separate AT2 expansion from later alveolar maturation?

**Primary priority; exploratory context analysis completed 30 September 2026; direct H1–H3 unresolved.**
[Biological rationale](RQ_Specified/A19_fzd_response_reversibility/README.md) ·
[Investigation plan](RQ_Specified/A19_fzd_response_reversibility/PLAN.md) ·
[Results and refinement](RQ_Specified/A19_fzd_response_reversibility/RESULTS.md) ·
[Figures](RQ_Specified/A19_fzd_response_reversibility/FIGURES.md) ·
[Extension priorities](RQ_Specified/A19_fzd_response_reversibility/EXTENSION_PIPELINE.md) ·
[External evidence](RQ_Specified/A19_fzd_response_reversibility/EXTERNAL_EVIDENCE.md).

**Hypothesis and mechanism.** Fzd stimulation maintains an expandable AT2 state;
termination permits competent descendants to enter an AT1 maturation program
while preserving a responsive AT2 reserve. Initial state and receptor-level input
may tune this reversible transition. YAP/TAZ dynamics are a candidate component,
not an established mediator. H1 (duration), H2 (initial-state competence) and H3
(input-dependent regulation) retain separate decisions.

**Evidence to hypothesis.** The withdrawal AT1 RNA direction survives omissions
but is imprecise. Fzd agonists compare above CHIR and below withdrawal48 on that
score. Narrow YAP-associated and broad sustained-YT responses disagree; matched
AT1/AT2 units dissociate Fzd5 abundance from canonical-target RNA. These motivate
reversible, context-dependent biology without demonstrating it.

**New supporting analysis, 30 September 2026.** Three donor-coded human qPCR
comparisons show lower SFTPC and higher airway markers without CHIR. In separate
airway-derived cultures, early SFTPC induction declines by passage 3 despite
continued CHIR. Eight bulk libraries in two source blocks show mixed AT1/airway
RNA increases, lower Wnt-target/proliferation scores and an opposing SFTPC
pattern across assays. These observations motivate a post-analysis competence
constraint: ending a maintenance input may permit alveolar maturation only
while alveolar competence is retained. They do not establish a Fzd schedule
effect, a starting-state interaction, lineage-derived function or preserved
AT2 reserve. No claim grade changes; all direct H1–H3 decisions remain unresolved.

**Prediction, rival and decision.** Verified off-periods should increase traced
mature output per initial viable population without exhausting the AT2 reserve.
Selection, toxicity and generic growth remain rivals. A precise absence of useful
mature-output gain, a reliable reverse effect or failed reserve preservation
weakens H1. State/input effects require their own contrasts; matching on achieved
growth or post-treatment scores cannot identify a direct mechanism. Missing
engagement or independent mature endpoints is inconclusive. The bounded inventory
and supporting RNA analysis are complete; the next decisive test needs linked
source, exposure, fate and reserve outcomes. A4, A8, A10 and A1 retain their distinct scopes.

<a id="a20"></a>

### A20. Does Fzd2, more than Fzd1, sustain AF1 fibroblast support of AT2-derived alveolar repair?

**Exploratory phase complete; primary scope narrowed, 30 September 2026.
Functional H1 untested; original subtype H2 deferred.**

[Focused hypothesis and biological decisions](RQ_Specified/A20_fibroblast_fzd_context/NARROWED_HYPOTHESIS.md) ·
[Investigation plan](RQ_Specified/A20_fibroblast_fzd_context/PLAN.md) ·
[Atlas results](RQ_Specified/A20_fibroblast_fzd_context/RESULTS.md) ·
[Extension results](RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1/RESULTS.md) ·
[Six figures](RQ_Specified/A20_fibroblast_fzd_context/FIGURES.md).

**Directional H1.** In a defined adult alveolar repair context, comparable
Fzd2 loss in prospectively identified AF1-like fibroblasts reduces functional
epithelial support and absolute mature AT2-descendant output more than comparable
Fzd1 loss. The original mature-output endpoint is retained.

**Mechanistic focus.** Maintenance of an AT2 pool capable of later maturation
is the proposed explanation to distinguish from maturation-specific support,
general fibroblast loss and matrix effects. A particular secreted mediator is
not assigned. The mechanism remains untested.

**Evidence and limit.** The paired atlas supplies receptor/context motivation;
the four-donor concurrent-input extension dissociates FZD2/canonical-response
RNA from selected support-ligand RNA. Neither supplies the comparable
receptor-specific functional test. RNA rank, organoid size alone and mature-cell
percentages cannot settle H1.

**Decision.** A greater Fzd2-dependent loss of source support and absolute mature
output would support the directional hypothesis under valid attribution.
A precise absence of a useful difference or reliable reverse would weaken it.
An earlier pool deficit versus preserved early pool with impaired later maturation
distinguishes competing mechanisms only with suitable lineage/function evidence;
post-treatment count adjustment alone is insufficient.

**Scope.** The primary test is one initial AF1-like adult repair context.
Original H2, receptor-by-initial-subtype dependence, is retained and deferred.
Notch interaction, other FZD members and cross-stage generalization require
additional evidence. A13/A15 scopes are unchanged. No claim grade or biological
acceptance changes; new execution waits for an eligible functional source.

<a id="a21"></a>

### A21. Does Fzd4 signaling recruit general-capillary cells into regenerative renewal after injury?

**Exploratory cohort/substate analysis completed, 30 September 2026;
functional hypothesis untested; conditional priority retained.**

[Biological rationale](RQ_Specified/A21_fzd4_capillary_function/README.md) ·
[Investigation plan](RQ_Specified/A21_fzd4_capillary_function/PLAN.md) ·
[Results and refined hypotheses](RQ_Specified/A21_fzd4_capillary_function/RESULTS.md) ·
[Three figures](RQ_Specified/A21_fzd4_capillary_function/FIGURES.md).

**Hypothesis and competing mechanism.** Fzd4-dependent signaling may support
capillary renewal through early regenerative entry or by sustaining vascular
competence that permits later repopulation. The original traced descendant
endpoint is retained. Neither mechanism is established by receptor RNA.

**Evidence to hypothesis.** In an independent 12-animal cohort, Fzd4 is higher
in gCap than aerocytes in all seven primary eligible pairs, but lower in author
transitional state 1 than major gCap state 0 in all 11 eligible pairs.
Within-condition Fzd4-cycling associations are inconsistent and involve at most
three animals. The dedicated cycling state lacks primary coverage. Prior Nb2
round/label/genotype/sex records are now resolved; their imbalance qualifies
rather than rescues the original pooled association.

**Prediction, rival and decision.** A valid Fzd4 perturbation should change
traced gCap and aerocyte contribution per initial viable labelled population
if the renewal hypothesis holds. Early maintenance impairment followed by lower
output is compatible with a maintenance-mediated route but does not alone prove
mediation. Selective lineage loss with independently preserved/characterized
maintenance favors a renewal-specific route. A precise absence or reverse of a
useful lineage effect weakens the nominated prediction. Failed engagement,
missing function or sparse lineage output is inconclusive.

**Next gate.** No inspected source joins receptor perturbation, initial gCap
identity, independent animals, lineage output and maintenance in the target
adult-repair setting. Tumor-vessel FZD4 restoration supplies context, not normal
gCap lineage validation. The high-expression renewal-marker lead is retired as
affirmative support; the biological receptor question remains open.


**Extension update, 30 September 2026.** [Priorities 1-3](RQ_Specified/A21_fzd4_capillary_function/extensions/extension_v1/RESULTS.md)
recover tumor Fzd4-rescue source data and complete the all-ten-Fzd comparison.
Structural-maintenance plausibility is strengthened within the tumor context;
Fzd4-rescue perfusion remains unmeasured. Foxf1, Fzd4 and Lrp6 are lower in all
11 primary state pairs. No alternative receptor meets the frozen nomination
rule and no compatible independent substate validation is claimed. The
[focused functional design](RQ_Specified/A21_fzd4_capillary_function/extensions/extension_v1/FUNCTIONAL_DESIGN.md)
retains gCap renewal and aerocyte yields separately, with maintenance, entry and
fate-specific alternatives. Priority 3 remains specified but untested; no claim
grade or biological acceptance changes.

## Execution and interpretation rules

**Biological-hypothesis rule (owner clarification, 29 September 2026).** Every
RQ must propose a plausible biological process, state its causal or directional
prediction, identify competing biological explanations, and name a discriminating
outcome. Explain how the result motivates that mechanism and where the inferential
step remains untested. Marker disagreement, batch effects, score robustness or
measurement artifacts belong in eligibility/controls and can revise a question;
they are not sufficient as its organizing biological hypothesis. Statistical
interactions and prediction gains do not by themselves establish a mechanism.


Before a new fit, freeze its estimand, biological unit, eligible observations,
primary comparison, multiplicity family, meaningful effect/prediction margin
and validation split in the question-specific plan. Sample floors are eligibility
rules, not power guarantees. Separate confirmation, exploratory discovery and
tests left inconclusive by inadequate data.

Reuse completed measurement checks within their recorded scope; repeat only if
inputs, estimands or a concrete unresolved risk change. Do not broaden a
sensitivity sweep merely to obtain significance. The [methods guide](REPRODUCIBILITY.md),
[measurement contracts](docs/RQ_MEASUREMENT_CONTRACTS.md) and
[ID crosswalk](docs/RQ_MEASUREMENT_CONTRACTS.md#crosswalk) locate requirements
without making diagnostics the biological questions.
