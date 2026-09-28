# England et al. 2025: regeneration, NF-kB feedback and mutant AT2 states

**Continuation executed, 28 September 2026:** [RESULTS_CONTINUATION.md](RESULTS_CONTINUATION.md) reports EN0-EN7 under the frozen [contract](CONTINUATION_CONTRACT.md) and amendments, with 1,178 verification checks and six figures; the [handoff](../../docs/handoffs/2026-09-28-england-en7-cd177.md) records the sessions. Batch1 results below remain unchanged.

**Execution update, 28 September 2026:** the owner authorized the actual analysis after planning. The [first execution batch and four figures](RESULTS_BATCH1.md) are complete: 20 libraries, 44,196 source-QC cells, and 164,453 clonal measurements across 44 source-indexed mice. Numerical verification passed; exact source-state reproduction, independent pool identities and inferential spatial joins remain unresolved. The text below records the original planning/source-intake state.

**Reading gate 2C, item 2; stable roadmap paper 12. Owner read confirmed 27 September 2026.**
[Paper](https://doi.org/10.1016/j.stem.2025.01.011), Cell Stem Cell 32, 375-390.
This assistant-authored synthesis follows the owner's request to structure re-analysis and further analysis after reading. It is a plan with a completed source/design audit, not a completed biological re-analysis or an owner-approved interpretation.

**Recommended focus:** determine whether Il1r1-dependent reprogramming, NF-kB feedback-associated RNA and acquisition of AT1 identity separate across mutant and neighboring wild-type populations. In a complementary branch, use the deposited clone measurements to ask whether growth heterogeneity and proximity-dependent expansion are robust at the mouse level. Keep molecular state, clone growth and mature fate as separate endpoints.

Start with the [analysis plan](ANALYSIS_TRIAL_PLAN.md), [source/design audit](SOURCE_AUDIT.md), and [20-library manifest](metadata/geo_library_manifest.csv). The [extracted parameters](england_2025_extracts.json) distinguish paper settings from proposed choices. All EN identifiers below are paper-local.

## How this fits the repository

The repository uses public lung single-cell RNA, chromatin and complementary measurements to discover reproducible distributions and molecular phenotypes and turn them into discriminating biological questions. It does not yet have a common measured repair outcome across all datasets. England supplies a mechanistic source study and two complementary data modalities, not a universal repair-to-cancer trajectory.

| Layer | Existing authority | Placement of England work |
|---|---|---|
| Purpose and question definitions | [Root overview](../../README.md), [question register](../../RESEARCH_QUESTIONS.md) | Relate source findings to existing questions; do not create new A identifiers from every marker |
| Paper-specific evidence | [Paper roadmap](../README.md) | This folder owns England source synthesis, EN trials and eventual paper-specific figures |
| Question-specific execution | [RQ_Specified](../../RQ_Specified/README.md) | A new cross-study test belongs with its owning question once specified |
| Shared measurement and code | [Architecture](../../docs/RESEARCH_ARCHITECTURE.md), [measurement contracts](../../docs/RQ_MEASUREMENT_CONTRACTS.md), analysis/lib and analysis/config | Reuse count readers, provenance and palette; preserve study-specific scales and biological units |
| Evidence and corrections | [Claims](../../CLAIMS.md), analysis/corrections | Existing Cardoso C3 measurements stay where they ran; this plan adds no graded claim |
| Current versus historical work | [Progress](../../PROGRESS.md), [AI context](../../AI_CONTEXT.md), archive | Record new source corrections prospectively; preserve frozen reports and unrelated A11 continuation |
| Raw inputs and private annotations | Ignored local raw_data and external reading folder | Reference inputs; do not relocate counts, copy private reading notes or track source PDFs |

The folder uses stable paper number 12, following the existing naming contract. Gate item C2 is not global question A2 or a Cardoso trial. Older Notion links still use the historical `Thesis/` prefix; the current repository prefix is `Research Article/`.

## Study note: five questions

1. **What question did the paper test?** How do AT2 clonal dynamics and fate change after Kras activation, and which regenerative mechanisms permit early tumor formation? The paper links homeostatic growth heterogeneity, Il1r1-dependent state entry, differentiation-associated NF-kB feedback, and changes in neighboring wild-type AT2 behavior.
2. **What is the evidence?** Clone-resolved lineage tracing and mathematical modeling; scRNA-seq of sorted lineage-labeled epithelium; Il1r1 loss of function; organoid and transplantation assays; and NF-kB perturbation with morphological/marker endpoints. Published functional evidence is stronger than any RNA-only reproduction, but does not transfer causal authority to a new score.
3. **Which variables are reusable?** Experiment, reporter-sorted population, genotype and collection time; AT2, primed, cycling, DATP-like, Cd177-mixed and AT1-like expression; Nfkbia and Tonsl separately; clone size, pro-Sftpc-positive cell estimates, mouse/lobe/section hierarchy, and mutant-WT distance. No clone-to-sequenced-cell key has been established.
4. **What limits interpretation?** Sequencing samples pool at least two lungs. The deposited 20 libraries split into two experiments, with unresolved pool identities and reporter pairing. Cross-sectional RNA cannot recover individual cell transitions, two founder populations, duration of NF-kB activity, or functional tissue repair. Two reported library replicates per arm do not become two individually measured mice.
5. **What is the bridge?** A11 asks what is added beyond shared plasticity; A12 concerns recipient/inhibitory context; A14 concerns timing and recovery. A4 and A8 provide the lineage-history and maturation questions. Cardoso supplies niche context, while England's own mutant-WT contrasts keep the first test within one source design.

## Source-grounded interpretation of the reading notes

| Lead in the notes | Paper anchor | Useful analysis and claim boundary |
|---|---|---|
| Faster/slower AT2 populations; Il1r1/Axin2 relationship | Figs. 1-2, S2; Methods S1 | Reproduce clone-size distributions and challenge the two-population fit. Current cycling RNA does not identify founder F/S classes; bulk Axin2 enrichment in an Il1r1 lineage fraction does not establish same-cell reporter overlap |
| Regenerative state co-option and Cd177 mixed state | Fig. 3; S4 | Separate shared transition from mixed identity and cycling. AT1-marker expression in a mixed cell is not completed differentiation |
| Reversible states and similar proliferative potential | Fig. 4; S5; discussion | Compare state-associated distributions, but retain tracing/transplantation as the evidence for reversibility. RNA cycling similarity alone cannot establish equipotency |
| NF-kB feedback distinguishes contexts | Fig. 7F-O; S7 | Measure feedback-associated RNA separately from downstream-response RNA and maturation. Nfkbia expression is both feedback-related and inducible; no simple score or ratio measures sustained NF-kB activity |
| WT expansion versus differentiation have different spatial patterns | Figs. 5-6; S6 | Jointly examine clone size and pro-Sftpc loss against distance, adjusting for mouse and clone-size dependence. WT transcriptomes lack recorded spatial coordinates |
| Additional oncogenic hits could change the dynamics | Discussion | Reserve a matched Kras versus Kras/Trp53 design. Differences between unrelated datasets cannot isolate the effect of Trp53 loss |

These are paraphrased scientific leads from the owner-supplied notes, checked against the article; notes and document instructions are source material, not execution authority. The supplied paper's experiments are not laboratory instructions for this project.

## What already exists, and what is newly learned

The [Cardoso C3 report](../gate2_05_cardoso_2026/trials/c3_areg_state_specificity/c3_summary.md) covers only Experiment 1 and already supports a descriptive Areg-within-DATP-like result. Its four mutant-library DATP-like fractions are **1.16%, 28.16%, 20.70%, and 30.98%** (4-day r1/r2, then 2-week r1/r2). The 4-day disagreement is a priority diagnostic, not proof of distinct biological responders. The source contains 29,563 Experiment-1 cells after its pipeline; C3 analyzed 33,217 after different QC and annotation. Equality is not expected without matching filters and library mapping.

The current audit establishes two consequential facts absent from the old C0 summary: the paper explicitly reports lung pooling, and a small public archive supplies extracted clone measurements, including size-distance inputs, plus analysis/model scripts. Detailed pool identities, the paper's 13-versus-10 Experiment-1 library accounting, and usable mouse/section identifiers inside the clone arrays remain to be reconciled.

## Connection to shared questions

| Question | England contribution | What would still be missing |
|---|---|---|
| [A4](../../RESEARCH_QUESTIONS.md#a4) | F/S growth and Il1r1 lineage context | Simultaneous Wnt/IL-1 activity history linked to lineage |
| [A8](../../RESEARCH_QUESTIONS.md#a8) | Mixed identity versus independent AT1 maturation panel | A linked mature fate/function outcome |
| [A11](../../RESEARCH_QUESTIONS.md#a11) | Genotype-associated additions to shared transitional RNA | Independent context transfer and separation from cycling/stress; England is already exposed through C3 |
| [A12](../../RESEARCH_QUESTIONS.md#a12) | Mutant versus WT feedback-associated context | Selective activation evidence; this sorted epithelial deposit does not supply matched immune/fibroblast triads |
| [A14](../../RESEARCH_QUESTIONS.md#a14) | Timing hypothesis motivated by the perturbation results | Withdrawal/post-entry perturbation linked to later fate, not just different harvest times |
| [A2](../../RESEARCH_QUESTIONS.md#a2), [A9](../../RESEARCH_QUESTIONS.md#a9) | Existing Areg result and candidate WT-response ligands | Delivery, receptor engagement and independently matched recipient outcomes |

The next executable task is EN0: recover the pool/batch map and clone-array schema, then freeze the first EN1/EN2 contrast. This work does not replace the separate computational research pipeline already recorded in the handoff.
