# Feasible extensions and joins with existing RQs

4 October 2026. Companion to the [review](README.md). E1–E6 are option labels
within this review, not registered questions, frozen designs or accepted work.
Feasibility means the stated inputs permit a bounded next step; it does not
establish laboratory resources, power or novelty.

## Extension specification

| Option / branch | Available inputs and feasibility | Comparison, unit and measured endpoint | Strongest rival and informative outcomes | Increment and limit |
|---|---|---|---|---|
| E1 / P03–P04: model and animal-influence robustness | Both qualified bulk matrices and working limma runtime are local. New contract required; no new data acquisition needed | Keep each animal's cultures together; examine prespecified normalization/design alternatives and leave-one-animal-out sensitivity of treatment/interaction estimates and fixed-program summaries | One animal or analysis choice may drive the apparent response. Stability would strengthen descriptive robustness; instability would identify fragility. Neither result estimates a new biological sample size | Measurement robustness. Existing program-definition sensitivities are inputs, not work to repeat. Very small animal counts limit precision; do not choose a model for more favorable q values |
| E2 / P03–P04: fixed-program transport | A/B gene tables and counts are local. Qualify common IDs/universe and source-condition differences first | Define the program in A and apply it unchanged to B WT Th17n/iTreg; any reverse comparison must be declared in advance. Unit: animal, endpoint: program RNA response at 68 h | Same-data program selection versus a response that transports across series. Concordance would support transport; discordance could reflect program selection, quantification or culture differences | Removes target-series vehicle-based selection for the transported program. Both series were already viewed; specimen independence is unknown. B has no Th17p. No confirmation or independent replication claim |
| E3 / P01–P02: RNA-to-reaction representation audit | Source expression and deposited scores are local; exact gene/GPR/direction mapping must be qualified. A descriptive comparison need not rerun CPLEX | Compare fixed enzyme/GPR RNA summaries with corresponding reaction-score contrasts under declared mapping rules. Unit: recorded cells; preparation-level unit unresolved. Endpoint: concordance/rank/effect sensitivity | Network output may mostly inherit input expression or smoothing. Agreement limits incremental information; disagreement requires tracing mapping/network context and is not flux validation | Wagner-specific measurement audit; eFPA already studies the general expression/network comparison. Whole-cohort smoothing or normalization cannot be treated as training-only in naive cross-validation. No causal enzyme ranking |
| E4 / P04: RNA–ATAC endpoint correspondence | Held: exact GSE165088 counts/peak annotation and qualified runtime are missing; no approved biological pairing across assays | Matched biological conditions at qualified time points; peak accessibility and RNA response, with peak–gene mapping declared | Accessibility can covary without direct JMJD3 action or measured histone demethylation. Concordance is multi-assay consistency; discordance can expose timing/endpoint limits | Conditional mechanistic discrimination only with orthogonal measurements. No Th17p ATAC inference and no claim that an open peak proves a causal regulatory target |
| E5 / P05: early competence versus later repair | No qualified linked-unit dataset in this package. Feasible now: define the missing tuple in A1/A8/A14/A19; numerical and laboratory feasibility unknown | Early metabolic/regulatory feature conditional on current RNA state and exposure, paired by donor/animal/culture with later mature AT1 output and, where applicable, AT2 reserve after withdrawal | Survival, cell amount, stromal support and residual exposure versus intrinsic competence. Added out-of-unit predictive value would justify the feature; no added value would constrain it | Fits existing competence/recovery RQs. Choi already establishes glycolysis/withdrawal relevance. Do not choose ODC1/JMJD3 solely from Wagner or equate organoid growth with repair |
| E6 / P06: source supply versus recipient routing across contexts | Published studies are accessible in part; matched source/recipient measurements and raw unit maps are not qualified | Specify one recipient and exposure context. Unit: independent donor/animal/coculture; endpoint: recipient metabolite use plus its relevant function, keeping Th17 cytokine output and fibroblast collagen distinct | Source abundance, substrate availability and recipient routing may each explain the response. Supply tracking without recipient discrimination favors availability; different output at comparable exposure motivates recipient context | Boundary/model comparison, because Yadav and Hu/Wu already test supply-related mechanisms. AREG receptor competence offers design logic only; ornithine is not an AREG receptor mechanism |

E1/E2 use available numerical inputs and have the lowest acquisition burden;
E3 needs a mapping qualification. That is a resource distinction, not scientific
ranking. E4 remains held. E5/E6 require specified biology and new evidence; no
bench protocol, sample-size claim or favorable effect margin is supplied.

## RQ overlap map

The registry and all A0–A27 canonical titles were screened. Focused current
dossier/result review covered A1, A3, A8, A9, A10, A12, A13, A14, A19, A22,
A23, A26 and A27. Other rows are title/context-level routing checks, not full
new audits. Dossier links lead to their current result and amendment references.

| Existing question(s) / evidence | Relationship to Wagner candidates | Routing boundary |
|---|---|---|
| [A1](../../../docs/research_dossiers/A1.md): regulatory distinction among RNA-similar transitional cells | Direct P05 overlap: early regulatory information beyond RNA state | Put a metabolic/chromatin feature here if the later functional discriminator is the same. No qualified early/later linked-unit tuple currently exists |
| [A8](../../../docs/research_dossiers/A8.md): maturation-specific programs beyond shared transition | Direct P05 overlap: independent mature AT1 outcome | Existing overlap signatures are not fate evidence; a metabolic feature must improve that exact endpoint rather than rename the shared transition score |
| [A14](../../../docs/research_dossiers/A14.md): exposure duration and fibroblast IL1 reception after withdrawal | Direct temporal/niche join for P05 | Separate epithelial competence from exposure history, survival and stromal reception. Existing two hypotheses retain their identities |
| [A19](../../../docs/research_dossiers/A19.md): Fzd withdrawal, mature output and AT2 reserve | Direct recovery-endpoint join for P05 | A pre-withdrawal competence feature could extend this design. Fzd and inflammatory inputs cannot be pooled as one exposure |
| [A3](../../../docs/research_dossiers/A3.md): injury-history macrophages versus ageing | Conditional P06 source-history join; P01/P02 methods analogy | Existing W1 is pseudobulk, not Compass; age/processing confounding, corrected no-hit pathways and an ineligible ornithine gene set remain. New scores cannot rescue a failed comparison |
| [A9](../../../docs/research_dossiers/A9.md): AREG recipient competence; A2: AREG delivery | Supply-versus-recipient design analogy to P06 | A9's receptor coverage is 7/22 donors, below its recorded floor of 11. Receptor RNA is not competence. Retain AREG identity; substrate routing needs a distinct biological specification |
| [A12](../../../docs/research_dossiers/A12.md): recipient context beyond IL1 ligand RNA | Design analogy to P05/P06 | Source assignment remains incomplete and the endpoint is not IL1-specific function. Do not assume macrophages are the only sender |
| [A13](../../../docs/research_dossiers/A13.md): fibroblast contribution beyond IL1B | Potential niche rival to P05 | Current weak/poor predictive comparisons do not nominate a fibroblast mediator. Metabolic features require their own incremental endpoint comparison |
| [A10](../../../docs/research_dossiers/A10.md): epithelial programs and organoid growth | Endpoint warning for P05 | Day-14 RNA/area are concurrent, target/plate are entangled, and absolute predictive performance is poor. Growth cannot substitute for later mature repair |
| [A22](../../../docs/research_dossiers/A22.md): epithelial identity versus fibroblast chemokine competence | Identity-versus-amount analogy | Current signal is sensitive to NKX2-1 and plate holdout; cohort directions differ. Chemokine competence and collagen are distinct endpoints |
| [A23](../../../docs/research_dossiers/A23.md): phosphate handling and transition entry/exit | Nutrient-context analogy to P05/P06 | External PAM did not establish a coordinated program or RNA compensation. Polyamine biology does not validate phosphate homeostasis; handling and timing measurements are still missing |
| [A26](../../../docs/research_dossiers/A26.md), [A27](../../../docs/research_dossiers/A27.md): CD8 tissue/age/repertoire | P03 composition-versus-within-state method analogy | Tissue clonality and receptor-recovery limits stay local. These CD8 results are not Th17 metabolic validation or a mechanistic join |
| A6: macrophage composition versus within-state IPF | P03 method analogy only | Shared contrast structure does not merge tissues, perturbations or endpoints |
| A15: integrin-mediated TGFβ activation versus ligand input | P06 exposure-versus-processing analogy only | Latent TGFβ activation is not ornithine routing; no joint mechanism is established |
| A0, A4, A5, A7, A11 | General transition/development/state context | Title/context screen found no specified shared discriminator requiring a merge. Revisit only if the P05 tuple actually uses these mechanisms |
| A16, A17, A18 | Priming, founder and neighborhood context | Potential selection/amount analogies only; no matched lineage or outcome to the Wagner data |
| A20, A21 | Fibroblast Fzd and vascular receptor contexts | Compartment logic only; no direct polyamine/JMJD3 link established here |
| A24, A25 | Bladder and microglial ageing | No direct join identified in this bounded title/context screen |

All 28 questions remain available. The map proposes routing; it does not adopt
an extension, change a canonical hypothesis, or assign a human decision.

## Conditions that would change this assessment

- A qualified linked early/later lung dataset would change E5 from specification
  work to a testable existing-RQ extension; another cross-sectional state score
  would not.
- Recovered ATAC/source supplement bytes, exact metadata and a verified runtime
  would permit a separately frozen E4/source-reproduction contract.
- Complete HIVEP1/ALDH5A1 methods and data identities could narrow an enzyme-level
  proposal further. Until then, those papers block a claim of unsearched novelty.
- A source-defined shared-patient/animal map could resolve whether studies supply
  independent validation; different accession numbers or publication dates alone
  cannot do so.
