# England 2025: source, claim and research-question audit

**28 September 2026. Completed evidence audit, with one bounded post-hoc diagnostic.**

The paper supports a distinction between Il1r1-dependent reprogramming and later acquisition of AT1-like features, alongside heterogeneous clone growth and altered wild-type neighbours. The repository recovers useful expression and clonal distributions. Several summaries nevertheless give those measurements more authority than their design supports. **A16 needs a corrected evidential basis; A17 is a worthwhile implementation/model-identifiability question, not a demonstrated refutation of two founder populations; A18 remains a mechanistic hypothesis with descriptive spatial support.**

The strongest new finding in this audit concerns A16: its existing within-subcluster comparison changes both the sampled population and the library grouping. When the original transition gate and separate libraries are retained, only two library/subcluster strata qualify, and their priming effects are +2.105 and +0.069 standardized units. The claimed consistent residual priming programme is therefore not established by this comparison.

Additional questions and their actual feasibility are in [RQ_CANDIDATES.md](RQ_CANDIDATES.md). All judgments below are audit recommendations; the historical C1–C168 grades and A-question registrations are unchanged.

## Scope and repository state

- The active checkout was `main` at `bbfa4e7`. Its paper index still calls England unstarted and its question register ends at A15. That is an incomplete view of ongoing repository work.
- England's completed batch1, continuation and follow-up analyses, and proposed A16–A18, were in `C:/Users/dream/.codex/worktrees/england-analysis-plan/scRNA_seq`, at commit `d485507`. This audit pins that commit instead of merging or modifying another chat's worktree.
- At the initial comparison, all 136 selected tracked files matched that commit after newline normalization. During the audit, the live register gained a link to a new `RQ_Specified/A16_cd177_state_attribution/` Stage 0 package. Its README and plan were also inspected. That plan correctly requires separate libraries and the original gate, but repeats the overstrong interpretation of the older FU_C results. Its full Stage 1 was not executed here.
- The ignored `tmp/england_plan_stage/` folder is an earlier source/planning snapshot, not the latest results. Existing caches and `.claude/` content were preserved.
- Official root claims still end at C168; the England follow-up's internal claim table and the proposed A16–A18 cards are not newly graded C-register findings.

**Primary reading:** [England et al., Cell Stem Cell 2025](https://doi.org/10.1016/j.stem.2025.01.011), the local final article (26 PDF pages), supplement `mmc1.pdf` (19 pages), and Methods S1 `mmc2.pdf` (9 pages). Main Figures 3 and 7 and supplementary Tables S1 and model Table 3 were visually checked. The source PDF and archive hashes, committed-file comparisons, checked tables and cache hashes are retained in [evidence.json](evidence.json). PDF page numbers below include the article's cover page.

The audit independently checked the deposited MATLAB event-selection branch, reproduced 49 selected FU_C effect sizes from saved cell data (maximum discrepancy <1e-15), and ran the population-preserving diagnostic. It did not rebuild the atlas, rerun the stochastic simulation, execute FU_S, recover missing biological IDs or contact authors. Public GEO metadata was checked for candidate feasibility, not used for a new expression analysis.

## What the paper establishes, and what the repository can reproduce

| Source claim | Paper evidence | Audit verdict and repository ceiling |
|---|---|---|
| Heterogeneous AT2 growth is compatible with two kinetic populations | Figures 1–2; mouse-level clone distributions; Il1r1 lineage experiments; Methods S1 | **Supported model, not unique identification of immutable founders.** The authors explicitly retain a single-hierarchy alternative in the Discussion. A distributional mixture and an independently marked cell type are different observations. |
| Il1r1-lineage cells have enriched Axin2 expression and greater organoid output | Figure 1L–N; S2L–Q | **Supported at the sorted-population/lineage level.** S2L–N are bulk qPCR, not same-cell current Axin2/Il1r1 overlap or dual-reporter tracing. |
| Mutant cells acquire repair-associated and mixed-identity states | Figure 3; S4 | **Supported in the source with context-specific state definitions.** The repository's three-marker transition gate and permissive AT1 gate are different classifiers. Co-expression in source staining is not overturned by failure of a new RNA gate. |
| Mutant states can regenerate other states and have broadly similar proliferative potential | Figure 4; S5; sorted-state organoids and transplantation; EdU | **Functional evidence for plasticity under the tested conditions.** Snapshot RNA, connected PAGA graphs and small cycling-score differences do not measure bidirectional conversion rates or demonstrate equivalence. Double-positive staining alone also does not prove interconversion. |
| CD177 mixed cells may help sustain division or bypass senescence | Discussion of GO enrichment on PDF p9 | **A source hypothesis, not a CD177-specific necessity result.** Cell cycling being inconsistent across two repository libraries does not refute future proliferative potential or a role in senescence escape. Neither is established by the repository. |
| Mutant tissue alters WT growth and AT2 identity, with different spatial patterns | Figures 5–6; Ki67, clone size, pro-Sftpc and AT1-marker/morphology observations | **Supported source phenotype.** FU_W recovers pooled spatial patterns. It cannot establish distance independence, a mouse-level interaction, or two causal signalling channels. |
| SPP1/DLK1 are candidates for the WT response | S6Q–V; paper PDF pp9,12,14 | **Functional organoid motivation, not identified in-vivo necessity.** Either ligand increased WT organoid output; their combination reduced the size effect. The paper favours SPP1 as a candidate. An AREG short-range mechanism is an additional hypothesis from other evidence. |
| Il1r1 loss suppresses mutant expansion/reprogramming | Figure 7A–E; S7A–D | **Supported in the source; directionally consistent repository RNA results.** Recovered-cell occupancy cannot distinguish impaired entry, survival/selection or capture effects. Heterozygous controls are not intact-dosage controls. |
| NF-kB inhibition shifts mutant phenotypes toward AT1-like differentiation | Figure 7J–N; S7G–V; genetic and pharmacological inhibition in organoids/PCLS | **Supported within the reported assays.** This is not demonstrated functional alveolar repair or an in-vivo therapeutic result. EN2's Il1r1 deletion contrast does not reproduce this post-entry intervention. |
| CD177 is exclusive to mutant cells | In-vivo comparisons in Figure 3, but also WT inflammatory organoids in S7R–V | **Only a scoped in-vivo comparison is supported.** The same paper induces CD177 in non-mutant WT organoids. A16's unqualified “absent from regeneration” wording should become “negligible in the compared in-vivo repair dataset.” |

The paper's published RNA methods document clustering, integration, signatures, correlations and CellChat. They do not specify a computational directional trajectory algorithm. Phrase this as **“no computational directional trajectory method is documented in the inspected article/supplements”**, rather than asserting what the authors never performed: their contribution statement mentions trajectory analysis. Sorted-state functional experiments are the relevant evidence for plasticity.

## Historical claim-register crosswalk

This is the bounded England-related subset, not a reassessment of all 168 unrelated claims.

| Registered row(s) | What survives scrutiny | Correction or limit |
|---|---|---|
| C19 | Historical inventory of the accessions then opened | “Complete” means the deposited files inspected, not a reconciled England experiment. The paper says 13 comparative libraries; GEO/manifest contain 10 Experiment-1 GSMs. The C19 comment about an omitted accession belongs to the Cardoso reading context and must not be misattributed to England, whose data statement lists GSE247505. |
| C31 | Its table shows higher Areg in repository-defined DATP-like than AT2 cells in all four mutant libraries | Keep **within-library** descriptive contrasts. Replace “within-animal” and avoid implying animal replication or exact author-state reproduction. |
| C32–C33 | Recorded abundance ordering is Areg > Hbegf > Ereg > Tgfa; abundance and enrichment are explicitly different rankings | Source Figure S7F motivates Areg/Ereg, but does not independently certify this four-ligand ranking. Neither ranking measures secretion, delivery or receptor activation. |
| C34 | C3 records WT DATP-like fractions 0.08% and 1.14% versus larger mutant fractions | “Same animals” is unverified. Use same model/time and reporter-defined populations; pool pairing remains unresolved. |
| C35 | A documented neighbour-mixing rule supported the no-correction decision | Embedding mixing does not establish absence of batch effects, equivalent cell recovery or independence of libraries. |
| C105 | The sampled epithelial transcript contrasts do not support broad Epcam RNA loss as the proposed escape mechanism | Preserve “not established”: sorted-in epithelial RNA does not measure surface EpCAM in the cells excluded by sorting. |
| C136–C137 | C136's current caveat correctly distinguishes bulk enrichment, historical lineage and present signalling | No dual-reporter intersection is quantified here. Keep absence-of-dataset claims restricted to a dated, explicit search; metadata searches do not prove absent co-measurement. |
| C141 | Its correction to laboratory attribution is consistent with England's authorship | The historical negative assertion remains refuted; no new biological conclusion follows. |
| C148 | The relevant S2 panel is bulk qPCR, not deposited scRNA-seq | A missing scRNA series is not withheld evidence. Published plotted qPCR can be inspected descriptively, but cannot supply the absent same-cell contingency table. |
| C149 | Aggregate Il1r1 expression does not independently verify the genotype labels | This does not falsify GEO genotype metadata. Keep genotype-dependent results explicitly conditional on those labels; do not revive the unsupported exon explanation. |
| C150 | Il1r1-to-Wnt coupling is unresolved by the historical aborted test | England's main result is not this coupling test. A new metadata-conditioned exploratory contrast requires a declared amendment; previously inspected values are not held out. With 2 versus 2 independent units, the permutation floor is 1/6 one-sided or 1/3 for an absolute two-sided statistic. |

## A16: retain the question, revise its premise

**Recommended wording:** “Within the same transitional compartment and separately within each library, does CD177-associated priming remain after accounting for transcriptomic neighbourhood, detection depth and contamination?” A surviving association would nominate an RNA phenotype; cell-intrinsic persistence/function still requires an independent outcome. Intrinsic state and compositional position can coexist, so this is not an exclusive either/or.

Three findings prevent the current answer from being treated as established:

1. **The frozen FU_A outcome is inconclusive.** All 12 endpoint verdicts are `depth_dependent_or_inconclusive`; the 3,000-UMI arm has only 26 positives in one library. Available adjustments preserve several directions, but the declared post-hoc relaxation cannot erase that missing comparison. Rank-biserial correlation is a change of effect statistic, not a control for depth. Residualized SMDs use a changed standard deviation: retaining about 87% of an SMD is not evidence that 87% of biological signal survives adjustment.
2. **FU_C is not nested within FU_A.** `run_followup.py` lines 64–71 select two libraries and `gate_transition`. Lines 244–250 instead pool all retained libraries within each experiment and condition only on `primary_include` and subcluster. They also report unadjusted SMDs, not the promised matched comparison. Marker-linked differences can change because population, library weights, depth and gate membership changed. The seven reported eligible clusters include both experiments.
3. **A same-population diagnostic is heterogeneous.** Reusing the saved clusters while retaining the original libraries, gate, inclusion rule and 30-per-side floor gives the following. This was specified and computed during the audit after exposure to the earlier findings; it is not independent validation or execution of A16 Stage 1.

| Endpoint, SMD | GSM7890835 / cluster 18 (45 positive, 222 negative) | GSM7890836 / cluster 16 (35 positive, 47 negative) |
|---|---:|---:|
| Priming | +2.105 | +0.069 |
| AT2 identity | +1.151 | -0.362 |
| AT1 identity | +1.139 | -0.301 |
| Itga2 | -0.355 | +0.324 |
| Shared remodelling | -0.805 | +0.381 |
| Lesion remodelling | -1.098 | +0.189 |

[Coverage](a16_same_population_coverage.csv), [effects](a16_same_population_effects.csv), and [depth ratios](depth_effect_ratios.csv) retain the exact values. The two qualifying clusters are different neighbourhoods and represent only part of each original population. Existing clusters may contain the marker or endpoint programme in their construction. These results establish heterogeneity and a limitation of the prior argument, not intrinsic priming, its absence, or a causal composition effect.

**Next feasible step:** the newly drafted A16 attribution plan is the appropriate owner for gene-disjoint neighbourhood matching, continuous Cd177, matched control genes and contamination sensitivity. Apply all comparisons to the same cells, separately by library, and disclose lost support. A successful computational result still cannot establish future cell behaviour.

## A17: confirmed code defect; biological discrimination remains open

**Recommended wording:** “How much support for discrete versus continuous clone-growth heterogeneity remains after reconciling source inputs and correcting the deposited simulator?” Avoid the directional hypothesis that correction *will* eliminate two populations.

The archive checksum and both repeated-loss cumulative branches were independently checked. For a pure slow founder at q=0.7, the birth branch accepts draws through 0.7; the erroneous loss branch ends at 0.6. Loss is unreachable and the remaining draws become null events. The deposited implementation therefore differs from its stated birth-death model. Existing EN6 tables report literal-versus-branch-corrected conditional KS distances 0.104, 0.281 and 0.281 at 1, 2 and 4 weeks. These are implementation-sensitivity results, not newly rerun simulations.

However, Methods S1 first fits analytical biexponential distributions and then performs stochastic fits. The branch defect does not by itself invalidate the analytical fit, Il1r1 tracing or observed size heterogeneity. The batch1 shifted-negative-binomial comparison concerns another statistical model family; its advantage is not yet the held-out result of a corrected full stochastic refit. The implementation that generated the published curves remains unverified.

**FU_S is computationally feasible but not fully specified for exact source reproduction.** Its grid and bins exist; an executed refit does not. Before execution, state whether rate changes and switching times are fixed from the archive, re-estimated or removed; reconcile the manuscript's parameter symbols with the code; and give the negative-binomial comparator the same held-out bins and training folds. The source used log-CCDF RMSLE, while FU_S proposes binned likelihood. That is a defensible new comparison, not the original fitting objective. A terminal 51+ bin may hide precisely the upper tail that distinguishes models, so a separately frozen tail diagnostic is needed.

There are also concrete input discrepancies:

- Supplementary Table S1 lists three mice at 1 and 2 weeks, whereas the decoded archive has four. Its 1-week YFP printed entries sum to 10,966, while the printed total 12,073 equals the four-mouse archive total. Its 4-day RFP entries sum to 922, but the printed total is 10,464; the decoded archive gives 922. At 2 weeks YFP, the printed third-mouse entry is 1,142 whereas decoding gives 1,152. See [the complete comparison](table_s1_reconciliation.csv).
- Visually checked Methods S1 Table 3 prints `f_S=0.16` and a best-fit slow expansion rate 1.1/week. The archived mutant parameter block used by EN6 instead uses its `fs=0.08` allocation and 0.9/week early slow expansion. The symbol/allocation mapping is not safely inferred from names. Report manuscript-table and archived-code variants separately until reconciled.

These are reproducibility/accounting issues, not evidence of misconduct or proof that two biological populations do not exist. A fair outcome may be corrected discrete support, continuous support or insufficient discrimination. Unchanged fitted parameters alone do not close the question without held-out model comparison and identifiability checks.

## A18: retain as a conditional mechanism question

**Recommended wording:** “Do WT clone expansion and loss of AT2 identity show different distance associations after accounting for sampling geometry, clone size, repeated neighbours and animal variability?” Separate that empirical question from whether two mediators cause it.

FU_W correctly discloses prior exposure, declining distal occupancy and absent mouse/clone IDs. Its log-size/logit-fraction sensitivity improves on a direct percent-slope comparison, but does not supply an animal-level estimand or validate separate channels. A flat/noisy identity-loss slope is not a demonstrated distance-independent process. Nor do log and logit slopes become biologically interchangeable simply because both are unbounded; compare prespecified predicted changes on meaningful scales with uncertainty.

The paper's nearest-mutant definition must be reconciled with the archive pair-array construction before describing every row as a unique nearest-neighbour observation. The same neighbour may recur, and this cannot be checked from the exported identifiers. Mouse-indexed nonspatial clone arrays **do** exist; the identity block applies to the pooled spatial arrays, not every clonal estimate.

A18's AREG proposal omits the source's closer SPP1/DLK1 lead. Neither transcript abundance nor ligand class establishes an in-vivo range. Retain SPP1/DLK1, AREG, relay signalling, geometry and mechanics as competing possibilities, without assigning mechanisms to distances in advance. Cell fractions around 0.2–0.3 are not, by themselves, evidence that a bounded readout is near saturation. Source EdU observations about mutant cells also do not directly validate the distance dependence of WT growth.

The spatial interaction is blocked for animal-level inference until identifiers or suitable new spatial data exist. A new RNA fit cannot supply them. No author message was sent.

## Other interpretation corrections

- **EN2 is not reproduction of the NF-kB rescue experiment.** The internal opportunities ledger's Figure-7 “reproduced” label should be narrowed to the Il1r1 genotype-associated RNA direction. Lower state entry and no AT1-score rise do not contradict later post-entry NF-kB inhibition.
- **FU_B is calibration, not independent validation.** The same Niethamer cells select the Youden threshold and estimate its 0.99 sensitivity/specificity. Cross-study chemistry and incomplete states matter. Collapse of the repository's permissive mixed gate establishes definition sensitivity, not disappearance of the source's protein-supported mixed state.
- **FU_T2 does not establish populated biological intermediates.** The script projects every retained epithelial cell onto an axis between two mutant-cluster centroids, without restricting to mutant cells or bounding perpendicular distance. Off-axis cells can occupy middle projection bins. A negligible change after removing flagged doublets only addresses those flags; it cannot prove absence of doublet artefacts or ambient RNA.
- **Missing coverage is not failed biological transfer.** EN7's rare CD177 detections make its planned contrast untestable in the inspected repair samples. They do not establish that CD177 cannot occur in repair; the source's WT inflammatory organoids already illustrate context dependence.
- **NF-kB response and feedback require distinct measurements.** Nfkbia is inducible and inhibitory; its transcript alone does not reveal pathway activity or feedback capacity. Tonsl is a source-reported feature, not a separately validated interchangeable activity meter in this audit.

## Recommended follow-through

1. Carry the A16 population correction and the narrower depth-control verdict into its existing Stage 0 package; use its same-population, gene-disjoint attribution analysis next.
2. Reconcile A17's manuscript/archive mouse counts and parameter mapping, then amend the proposed refit contract before fitting. Preserve both original and corrected implementations and all undecidable outcomes.
3. Prioritize the mouse-indexed clone composition and paired mutant/WT questions in [the candidate list](RQ_CANDIDATES.md). They add biological questions using a stronger unit than another pooled-cell analysis.
4. Keep A18's spatial inference gate explicit. Retain the feedback-induction and second-hit questions as mechanistic directions requiring additional measurements.

No new A identifier is silently assigned, and no official claim grade is changed. The audit's numerical record can be regenerated with [check_evidence.py](check_evidence.py), using the England worktree for ignored cell caches and the supplied PDF directory for source hashes.
