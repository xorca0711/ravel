# Capability record and exact enabling inputs

**Actual wet-lab access remains unknown.** The private PI/funding planning context and public papers describe possible scientific fit; neither establishes access, validated assays, available specimens or independent preparations. This report makes no lab assignment and publishes no private planning details. These are capability requirements at the scientific-design level, not experimental procedures.

| Capability | Current evidence | What would establish feasibility |
|---|---|---|
| Repository metadata processing | Five source snapshots, four frozen contracts and successful hash-bound runs | Demonstrated for deposited identity metadata only; no expression or functional assay validation follows. |
| Models, species and specimens | Not supplied for the user's present lab access | Named available model/specimen and responsible laboratory confirmation; distinguish an existing model from one merely described in a paper. |
| Independent biological units | Source-specific holds documented in RESULTS.md | Animal/donor/preparation IDs, pools/splits, pairing, exclusions and feasible independent acquisition. Technical wells stay nested. |
| Linked fate/recovery measurements | No generally qualified source for the proposed early-to-later comparisons | Starting identity, measurement time and independently defined later descendant/function endpoint linked within the intended unit. |
| Source–recipient activity | Gene expression and published precedents are available; direct local capability unconfirmed | Source amount/viability, protein availability or activation, receptor engagement and a specific recipient outcome as appropriate to the question. |
| Physiological function | Vascular integrity, phosphate flux, chemokine action and mature epithelial function are not interchangeable with RNA | A validated assay for the chosen quantity and model, with a credible attribution/control strategy. |
| Precision and practical scale | Useful effect, independent-unit variance and feasible throughput remain unset | Relevant pilot/source variance, biologically meaningful effect and realistic acquisition constraints before confirmatory design. |

## Exact data exports that could remove current holds

These are requests to prepare or locate, not messages sent to authors or labs.

1. **MesSTIM / GSE169125:** map GSM5176672–GSM5176689 to source animals or explicit pools, independent isolation/preparation, population and technical well. State which records share a preparation across populations or input groups and which figure-level repeats are represented in the deposit. Preserve the existing sample titles and clarify their numeric suffixes. The public RNA data alone will still not measure delivery.
2. **A5 / GSE303646:** export raw barcode, `identifier`, biological mouse ID, treatment/day and original author state (`cell_type`/`meta_label`) from `230111_Bleo_Ageing_annotated_final.h5ad`, plus annotation version and raw-count join. Reconcile 56 library IDs with the reported 55 mice. The existing [source-request guidance](../../../RQ_Specified/A5_developmental_programme_reuse/replication_gate_20260928/REPORT.md) remains authoritative; no need to redownload all expression before the join is available.
3. **A7 / ES1:** map CEBPA and AP-1 study records separately to pool members, preparation and paired RNA/ATAC material. Identify any additional independent condition replicates. Do not relabel source controls or post-genotype states as interchangeable starting populations.
4. **Nb3 screen / GSE307112:** map deposited library and plate/well IDs to epithelial preparation, fibroblast donor/preparation, technical split, target assignment and imaging time. The existing one-to-one library/imaging joins do not establish these biological identities.
5. **Nb3 spatial / GSE307128:** map the four deposited blocks to animals, sections, genotype, actual treatment and collection time, with region/bin assignment. Reconcile the paper/sample treatment descriptions before a genotype effect; large spatial downloads do not resolve missing animal identities.
6. **Linked-outcome questions:** for A1/A4/A8/A14/A19/A20/A21, supply the source-unit and early-to-later join for the specific outcome required in PORTFOLIO.md. A collection of unlinked endpoint assays is not that export.

## How to use a future capability answer

Record each capability as demonstrated, documented-but-unverified, unavailable in the named setting, or unknown, with its evidence and date. Keep source eligibility separate from lab access: the former can permit a descriptive public-data study while the latter remains unknown. Do not invent sample sizes or a molecular mediator to fill a planning template.

Once a comparison is feasible, write its exact hypothesis, strongest rival, total and mechanistic outcomes, attribution controls, biological unit, precision rationale and stop/revise rule. Then freeze a new contract for the intended analysis. A confirmatory plan needs more than the metadata inventory completed here.
