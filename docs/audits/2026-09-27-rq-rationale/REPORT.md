# Repository-wide research rationale audit

27 September 2026. Baseline: merged `origin/main` snapshot
`329c07c2c7752b861ef94ffd5bd23575daae9d2b` (through PR #89, including #90).
The original open checkout is an older `main` at `e9d79e0`; it is not the current
research baseline. Its untracked directories and ignored data were preserved.
Changes from this review live in a separate managed worktree.

**Conclusion:** the repository supports a coherent hypothesis-generation project,
but it does not yet connect shared epithelial RNA, regulatory state, niche activity
and functional repair in one identified causal chain. Most completed trials are
valid narrower measurements. The most consequential newly confirmed errors are
overinterpretation of A2's nonsignificance/depth sensitivity, A15's purity and
mediator-null claims, and an internally inconsistent A15 eligibility fallback.
These affect interpretation and future decisions; this audit found no reason to
replace the saved primary estimates or re-grade the historical claim register.

## Coverage and method

The [machine inventory](evidence.json) records every tracked file in this snapshot,
Python syntax and JSON parsing, all question-workspace document headings/hashes,
and independent numerical/mathematical probes. The baseline has 2,620 tracked files,
334 Python sources and 492 JSON files. Current research scope is A0–A15, A12-S1,
eight individual RQ workspaces and the A5/A11 enabling contract. The RQ-by-RQ and
trial-by-trial matrices below are the semantic review record.

Read the root purpose, architecture, claims, handoffs and measurement contracts;
the paper/correction precedents; every current RQ card; all workspace plans and
current result chains. Historical trial families were checked through their
claim/provenance contracts and their relationship to current questions. Inspected
the relevant scoring, selection, gating and verification code; independently
reaggregated the current A0 transfer and A2 ITGB6 estimates. This is not a
line-by-line certification of every historical script or a fresh raw-data
reproduction. Cached sequencing matrices, PDFs and software environments were
not exhaustively reprocessed. No additional model fit or result-driven threshold
change was needed to resolve the confirmed contradictions.

The original checkout's validator failed after walking into other worktrees and
temporary snapshots. The clean current baseline passes 2,740 checks. The traversal
fix now excludes nested checkouts, with focused regression coverage; it does not
suppress failures in the active repository's own scientific artifacts.

## Findings and synchronization

| Priority / ID | Confirmed problem and evidence | Consequence and disposition |
|---|---|---|
| High L1 | [A2 depth report](../../../RQ_Specified/A2_areg_source_delivery/reports/LEG2_DEPTH_STANDARDISED_RESULTS.md) says a positive rho 0.293, p 0.186 means no coupling, and concludes the original association was depth | Nonsignificance is not absence; a measure change is not a causal decomposition. Current summaries corrected, estimates preserved. [A2 addendum](../../../RQ_Specified/A2_areg_source_delivery/reports/INTERPRETATION_AUDIT_2026-09-27.md). |
| High L2 | The same report recommends B≈100 as the only rate-invariant continuation, citing [a test](../../../RQ_Specified/A2_areg_source_delivery/scripts/test_depth_measure.py) that holds K/N fixed and sometimes uses fractional K | The test confuses a conditional finite-population probability with its expectation over count sampling. Exact enumeration in this audit disproves the universal necessity of a small budget. Withdraw that automatic next step; keep the correct hypergeometric instrument and recorded results. |
| High L3 | [A15 rival-2 report](../../../RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/RIVAL2_RESULTS.md) calls marker enrichment pure and says composition did not produce the null | Marker checks do not establish purity/equivalence; bulk epithelial subtypes can change. Wide endpoint intervals and a nonsignificant omnibus leave the mediator rival unresolved. Current interpretation corrected in the [A15 addendum](../../../RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/INTERPRETATION_AUDIT_2026-09-27.md). |
| High L4 | [A15 parent plan](../../../RQ_Specified/A15_epithelial_integrin_tgfb_activation/PLAN.md) condition 2 demands independent units but condition 6 permits proceeding when that independence is unknown | The fallback cannot pass the parent gate. The dated clarification treats unknown independence as unresolved eligibility; separately specified descriptive work remains possible. The parent mechanism remains untested. |
| High L5 | A2/A15 contrast delivery or activation with ligand supply, while source-specific protein supply, receptor engagement, positions and preparations are unresolved | The screen supplies a lead, not route selection. Separate-species logCPM does not measure relative secreted ligand supply. Recipient blockade can create a floor, not prove mediation. Future factorial/engagement/rescue requirements are stated without pretending the current data meet them. |
| Medium L6 | Root handoffs claim all PRs through #81 are current, A2 stage-5 still queues the completed depth pass, and older A1 holds persist in historical tables | Current dated pointers now identify the merged snapshot, completed work and interpretation overrides. Frozen reports/configs keep their historical status; their old queue is not an execution instruction. No branch was merged, cleaned or deleted. |
| Medium L7 | [A13 coverage report](../../../RQ_Specified/A13_fibroblast_beyond_macrophage_il1b/reports/COVERAGE_RESULTS.md) generalizes fibroblast scarcity from the inspected cohorts to larger cohorts in general | Retain zero exact-definition and three wider-definition pairs, but limit that conclusion to those cohorts. Recovery depends on depth, protocol, sampling and subtype definition; more patients can improve total complete units. A different cohort needs an actual count, not an assumed failure. |
| Medium L8 | `CLAIMS.md` ends at C168; later completed question-level outcomes are outside that generated ledger/negative-results view | README now states the coverage boundary. This audit/index records stopped and inconclusive RQ results without inventing owner grades. Historical claim grade and execution status are separate. |
| Medium L9 | A0 has two pilots with different discovery cohorts, intestinal intermediates and scorers; the old checkout exposes only the first | Current status is `pilot_v1`, not a blend of their sample counts/effects. Both reuse repair/Haber sources; a newly frozen candidate is not a wholly untouched cohort. Historical replay scripts can overwrite outputs and must run in an isolated copy. |

The repository's shared architecture is now stated in
[RESEARCH_ARCHITECTURE.md](../../RESEARCH_ARCHITECTURE.md). The invariant is an
explicit question-to-measurement-to-decision chain, not identical software,
one universal gene score, a universal cell floor or an insistence that every
useful exploratory analysis must establish causation.

## Every research question challenged

| RQ | Strongest defensible reading | Attack on the biological rationale | Decision / next discriminating evidence |
|---|---|---|---|
| A0 | A frozen selected lung signature fails the specified mature intestinal endpoint in three mice | Intermediate peaking is only one consequence of a conserved process; different genes, timing and branch identities can implement related biology. D1/D2 scores are selected estimates; V1 is not an equivalence test. | Keep the stop and P4 pruning. Broader conservation remains unresolved. A future test needs a new justified branch/cohort and independent state evidence, not retuning Haber until positive. |
| A1 | Context-sensitive markers, direct-mark descriptions, paired CD44 responses and measured descendant/protein endpoints | Separate cohorts cannot establish regulatory information beyond RNA about the same outcome. One cell line/two preparations is not donor replication. HOPX acquisition is not mature function; source/chase aliasing survives identity recovery. | Completed batches stand. Select one candidate regulatory discriminator and a compatible replicated outcome-linked design. No new taxonomy or chromatin-mediated fate claim. |
| A2 | No demonstrated AREG decrement in the screen; ITGB6-associated decrease; depth-sensitive, unresolved donor correlation | Delivery and abundance are not exclusive causes. Neither leg manipulates delivery at controlled dose; RNA cannot bound effective source or recipient ligand. | Apply L1/L2/L5. No automatic 100-UMI continuation. Source presentation/dose and recipient competence must be separately testable. |
| A3 | Late macrophage/state-composition observations | Injury history and age/harvest are aliased. Covariate adjustment cannot invent aged uninjured animals; fractions do not show survival of the same cells. | Hold for age-matched controls and estimable sampling. Tracing is additionally required for same-cell persistence. |
| A4 | Sparse Axin2/Il1r1 and Wnt-source observations motivate feasibility | Co-detection cannot distinguish sequence, concurrent activity or separate subsets. Reporter history differs from present activity and responsiveness. | Require pulse/chase, washout, activity and lineage-linked response; Nb1's baseline/early coverage cannot answer an acute switch. |
| A5 | Externally defined Guo genes show positive average detection differences in 24 repair mice, including declared exclusions | A P1 mixed-identity list can capture birth stress or generic remodelling. Average recruitment does not show a coordinated programme in each cell, developmental identity or lineage reuse. Old Strunz-filtered modules leak test-cohort selection. | Retain partial recruitment. Replicate the unchanged external instrument in another eligible injury study before expanding mechanism claims. |
| A6 | Mixture and within-state explanations remain plausible | State harmonization can erase disease biology or select on the tested programme; exclusion of cycling cells changes the target population. Similar labels are not necessarily comparable states. | Freeze a programme-independent state map, donor support and target population before any fit. Equivalence is needed for a composition-only conclusion. |
| A7 | Mutants shift both the reference and labelled contrast descriptively | Genotype affects selection into Sftpc-defined states, and score floors/ceilings can compress contrasts. A state interaction is not separately replicated in current wells. | Independent state definitions and replicated genotype-by-state design; report reference and intermediate levels, not only their difference. |
| A8 | Signature overlap motivates a disjoint maturation measurement | List overlap is weak biological evidence; a positive maturation score can simply increase with AT1 mixture. An RNA-defined outcome would be circular. | Independent mature protein, morphology/function or traced yield with a frozen incremental test. No additional score search without the endpoint. |
| A9 | Receptor encoding and donor coverage are measurement prerequisites | Database complexes and coexpression do not measure dimers, surface receptor or ligand-specific competence. AREG is not the only EGFR ligand. | Controlled ligand exposure and receptor-specific engagement/response; retain RNA as screening. |
| A10 | RNA growth blocks add conditional information in this screen; absolute transport is poor | Day-14 RNA is concurrent with the outcome; conditioning on post-treatment variables is not a total treatment effect. Outcome-centred held-out groups are descriptive. Plate holdouts change target mix as well as plate. | Follow-up complete. Resolve preparations, imaging units/calibration and fresh validation before another model cycle; mean area is not repair. |
| A11 | Lesion association replicates in eight pairs; stronger relative-score criterion is unresolved | A difference of score changes is not added predictive information or a separate mechanism. Tumour epithelium versus normal AT2 changes identity/composition; no non-neoplastic injury arm tests specificity. | Preserve threshold and q=0.0547. Obtain comparable epithelial states and a non-neoplastic comparator; do not optimize the existing eight pairs. |
| A12 | Recipient-specific RNA compatibility motivates a parsimonious model | Unsigned prior fits/rank denominators cannot show activation or inhibition. Source and receiver can share inflammation; receptor RNA and outcome panels can overlap. | Verify matched units and disjoint predictors/outcomes, compare source-only and recipient extensions, then seek activation/selective perturbation for IL-1 specificity. |
| A12-S1 | Unassigned cells carry much recovered IL1B RNA | An unknown label is not a novel macrophage state; ambient RNA, doublets, recovery and confidence abstention remain alternatives. | Independent identity and source attribution first. Keep unknowns visible; secreted IL-1 remains a separate endpoint. |
| A13 | Exact triad coverage fails in the inspected cohorts | A label-defined zero is not absence of epithelium. Largest-label gating may compare different fibroblast states across donors; ten units does not guarantee enough degrees of freedom or power. | Keep no-fit result. Predefine comparable compartment/state estimands and count another cohort only if recovery could plausibly open the gate. No mediation/feedback claim from a joint association. |
| A14 | Two meaningful future hypotheses: duration and recipient contribution | Exposure duration, cumulative dose, age and time since withdrawal can be entangled. State loss can reflect death/replacement. Recipient deletion may alter baseline viability. | Factorial timing/dose/recipient controls, verified withdrawal, viability and traced mature/function outcomes. Decisions remain separate; RNA alone cannot supply them. |
| A15 | ITGB6 motivates an activation-route hypothesis; systemic-antibody side-branch has downstream and epithelial measurements | Ligand versus activation is a false forced dichotomy if both act. Recipient-ligand removal changes the system; a mediator null at day 7 does not rule out another time or modality. | Apply L3–L5. Parent remains blocked and proposed. Require verified units, bounded source perturbations, active-ligand/response assays and route-discriminating controls. |

## All RQ trial families and stages

| Workspace / stages | Rationale check and result | Remaining limitation or correction |
|---|---|---|
| A0 original P0/local/public/extended coverage | Correctly retains failed animal/state floors and unresolved mappings | Metadata eligibility is not a negative biological finding. |
| A0 exploratory E1 | Full leave-one-mouse-out selection supports internal source stability | Author labels and one source study remain; this is the earlier repair-only instrument. |
| A0 exploratory E2 | Depth, cycle, synthetic mixtures and matched sets challenge named measurement rivals | Selected-module random-set tails are not selection-adjusted biological p-values; low-cycle eligibility collapses. |
| A0 exploratory E3/E3a/E4 | Frozen descriptive transfer, then disclosed post-transfer depth sensitivity and closeout | One developmental capture is not an animal replicate; two intestinal mice and matched subsets cannot exclude weak sharing. No independent corroboration between pilot versions. |
| A0 continuation P0/P1/P2 | Source-driven replacements, raw-count alignment and four-contrast ortholog discovery | Early human airway development differs from adult mouse alveolar repair; selected discovery positivity does not prove conservation. |
| A0 continuation P3/P4 | Independent aggregation confirms start passes and mature endpoint fails; P4 is deliberately pruned | Negative transfer cannot identify whether branch, assay, species or biology explains failure. Pruning specificity is justified for the stopped transfer claim, not for a new claim that the lung module is specific. |
| A1 first batch | Correct animal/field denominators; ten-mouse IRE1 model; HPCS/CD44 input audit; PATS caller hold | RNA, ATAC and tracing are separate experiments; four FDR hits do not validate the nominated pathways. |
| A1 second J1–J8 | Omission sensitivity, native-assembly marks, methylation reference and measured descendant reconstruction | Direction stability is not external replication; CpG-domain overlap is not a replicated DMR or temporal fate result. |
| A1 robustness | Library/chase rank audit, source influence, partition comparison and alternative TSSs directly attack interpretation | Promoter-dependent signs and fixed-library aliasing are substantive boundaries; identities alone cannot repair them. |
| A1 adaptive closure | CD44 crosswalk and direct paired interaction; HPCS abstention map; bounded source recovery | Bulk sorted fractions can differ in mixture; fragile Sftpc magnitude and dependent classifiers remain visible. |
| A1 regulatory/outcome continuation | Recovers named mice/harvest; inventories regulatory preparations; nests AP-1 fields within mice; separates culture endpoints and signed TP53 lists | No same-unit chromatin-to-fate mediation. AP-1 interaction remains descriptive; selected gene-list overlap cannot replace full directional analysis. |
| Shared A5/A11 stages 1–3 | Source lists, orthologs, exclusions and pairwise partition are reproducible | The 12-gene union has no three-way core; source-list-exclusive is not biologically exclusive. |
| A5 revised test | External Guo primary and external exclusions remove the known Strunz selection leak | Replication across independent injury studies and functional interpretation remain open. |
| A11 discovery reproduction + revised Kim test | Preserves normalization scope and separates primary association from relative/stress tests | Relative score contrast is not a nested-model increment; near-threshold failure must not be rescued post hoc. |
| A10 stages 1–4 | Joins/design audits and original/adapted fits answer progressively narrower questions | Earlier BH and retained-model promises were not all implemented; later amendment discloses this rather than fabricating tests. |
| A10 follow-up diagnostic/model/verification | Four-plate target overlap and train-only transforms meaningfully test conditional information and shift robustness | Negative absolute R-squared on 3/4 plates limits utility despite relative gains; no independent preparations identified. |
| A2 stages 1–2 | Audit withdraws an unjustified inferential freeze before scoring | Fixed positions and unresolved units still prohibit causal/randomization interpretation. |
| A2 leg 1/stage 3 + robustness | Retains all arms, eligibility and culture diagnostics | Relative RNA effects do not isolate TGF-beta activation; post hoc checks cannot prove unchanged cultures. |
| A2 leg 2/stages 4–5 + depth pass | The original gate refuses raw-depth coupling; exact-molecule expectation is a useful declared sensitivity | Apply L1/L2. The synthesis's queued depth run is completed; a smaller-budget rerun is not automatically required. |
| A13 audit + refused first attempt | Reproduces 240 historical flags after exposing single-label gating; counts exact/wider Kim coverage | Keep no fit. The definition is a real constraint, not a license to lower floors until fit succeeds. |
| A15 parent stage 0/1 | Registration/data search and explicit activation-readout requirement protect scope | Search absence is bounded to inspected resources; parent gate contradiction corrected prospectively. |
| A15 rival-2 metadata, withdrawn v1/v2, v3 execution/verification | Correctly compares batch-matched four-versus-four mice and retains uncertainty | Enrichment is not purity; nonsignificant epithelial panels do not eliminate a mediator. Historical `weak bound` is qualified, not promoted. |

Questions A3/A4/A6/A7/A8/A9/A12/A14 have no standalone executed workspace in
this snapshot. Their related paper/correction analyses are inputs, not silently
completed tests of their biological propositions. Nb1 informs A4; G1/G2/W1 and
their corrections inform A3/A6; ES1 and M-series inform A1/A5/A7/A8; ligand and
U-series context analyses inform A2/A9/A11/A12/A13. These dependencies do not
multiply independent cohorts.

## Critical logical gaps still open

1. **The organizing outcome is missing.** The cohorts do not share a defined,
   independently measured functional repair endpoint. Neither a late sample,
   lower transition score, larger organoid nor HOPX-positive descendant is by
   itself that endpoint. The project currently discriminates associations and
   measurement explanations more strongly than repair mechanisms.
2. **Regulation-to-fate linkage is missing.** A1's direct marks, A5 recruitment,
   A11 lesion association and A10 size models cannot be assembled across different
   individuals into a causal cell-state trajectory. Same-unit or appropriately
   linked replicated perturbation/outcome data are needed.
3. **The most attractive niche lead remains confounded.** ITGB6 has one fixed
   position/guide pool per target and unresolved preparation independence.
   Neither the culture checks nor systemic-antibody comparison identifies the
   source-to-recipient activation route. The A15 parent gate is still closed.
4. **Specificity is incompletely identified.** Developmental reuse versus generic
   remodelling, lesion association versus neoplastic specificity, and present
   state versus future fate require different comparators. More gene-set variants
   on the same data cannot supply those missing comparisons.
5. **Current question outcomes are incompletely represented by the graded ledger.**
   This is a coverage/governance gap, not absence of artifacts. Keep the RQ outcome
   index visible and submit finite claim proposals for owner grading separately.

## Research direction

The repo's useful product is a small set of hypotheses with known evidence,
explicit alternatives and an executable discriminating next test. Counting RQs,
successful gates, figures or nominal discoveries is not progress toward its goal.

Recommended sequence, based on the current evidence rather than a new dataset
popularity search:

1. **Finish interpretation and authority synchronization.** This review supplies
   the shared architecture, A0–A15 coverage, corrected A2/A15 reading and current
   pointers. Preserve all completed stop decisions. Do not refit to improve them.
2. **Prioritize a bounded design-recovery task over another model.** For A10/A2's
   screen, recover preparation/lot IDs, plate-position/guide allocation, imaging
   scale and medium/matrix conditions from specific existing primary records.
   If unavailable, stop at the stated within-screen ceiling. No author message
   has been sent; any contact needs explicit authorization.
3. **If a computational scientific extension is chosen, make A5 generality the
   first candidate.** Seek one independent adult-injury study with supported ADI
   and activated-AT2 comparators, verified animal IDs and adequate capture. Test
   the unchanged external Guo modules and fixed estimand. Coverage and precision
   must be audited first; no new cohort is declared eligible by this review.
4. **For the central repair question, select one linked outcome design.** A1/A8
   need a frozen regulatory/maturation feature tested against independently
   measured mature-cell contribution or function. A14's withdrawal/factorial
   design is closer to a causal repair test but requires suitable new data.
5. **Keep the mechanism branches conditional.** A2/A9/A12/A15 need source/receiver
   engagement and controlled ligand/activation contrasts; A13 needs comparable
   complete triads. A3/A4/A7 need their missing age, history or genotype designs.
   A0 needs a genuinely distinct, justified conservation test if resumed. None
   is unblocked by another atlas embedding or a lower p-value on current data.

For any selected extension, record one primary estimand, the exact unit and
population, an effect/precision criterion, the principal rival and the result
that would stop further investment. Power should use the planned biological
design and plausible variance, not cell count or a universal minimum n.

Primary-source spot checks support the distinction between partial recruitment
and global developmental equivalence: Strunz already discusses poor overall
developmental correspondence, despite injury transitions.
[Strunz et al.](https://www.nature.com/articles/s41467-020-17358-3).
The AREG precedent measures a macrophage–pericyte pathway and barrier restoration;
its demonstrated context cannot be assumed for a mixed-species organoid screen.
[Minutti et al.](https://pubmed.ncbi.nlm.nih.gov/30770250/).
These checks are not a comprehensive novelty or public-data-exhaustion search.

## Verification and preservation

See [evidence.json](evidence.json) for the census and independent probes, and
[validation.json](validation.json) for final commands and results. Python compilation,
the 18-binding claim contract, 17 Nb1 output hashes and repository validation pass.
The unit suite ran 53 tests with one skipped module requiring the scientific runtime;
the two new traversal regressions pass. Raw-input verification was not requested.
These checks validate artifact consistency, not every biological inference. Frozen configs,
scientific code, numerical tables, claim grades and source inputs were preserved.
Current summaries were corrected through explicit dated interpretation addenda;
the original historical verdicts remain inspectable. No cloud compute, raw-read
download, study note on an unread paper, message to an author, commit or merge is
part of this review.
