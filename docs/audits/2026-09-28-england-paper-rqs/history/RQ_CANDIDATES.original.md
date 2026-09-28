# Additional questions justified by the England audit

**28 September 2026. Candidate questions, not registered claims or completed tests.**

These candidates follow the paper's clonal, RNA, perturbation and neighbour evidence, including negative and missing results. “Feasible now” means a bounded analysis can run with existing data; it does not mean the causal question can be settled. Candidate labels E-N1 to E-N8 are local to this audit and do not reserve A19 onward. Existing A-question owners should absorb overlapping extensions.

## Highest priority with existing data

### E-N1. Does tissue-wide loss of AT2 identity reflect within-clone composition, or preferential expansion of clones with different composition?

**Why this follows.** Source Figures 1J, 2H–J and 6A–C describe clone composition and fate balance. A cell-weighted tissue fraction can shift because of clone growth even if the typical clone's composition does not. The deposited nonspatial arrays retain size and pro-Sftpc estimates within mouse and lobe; batch1 already reports both clone-weighted and cell-weighted summaries, but has not made their decomposition the biological test.

**Discriminating analysis.** Compare those two estimands per mouse and reporter, then standardize across a prespecified common clone-size distribution. Model size continuously or use fixed bins; do not define “fast” from size and then use size to prove a founder effect. Separate within-mouse associations from between-time comparisons. Check sensitivity to singlet inclusion and measurement-derived, noninteger cell numbers.

**What would change the reading.** Persistence of identity-loss differences after size standardization supports a compositional shift within comparable clones; disappearance supports an important contribution from clone-size weighting. Neither proves individual-cell differentiation, founder ancestry or mature AT1 function.

**Feasibility:** ready for an exposed-data, mouse-level analysis. Existing `clone_measurements.csv.gz`, `clone_summary_by_mouse.csv` and the source archive supply the variables. Resolve the Table S1/archive accounting first. **Relation:** A8/A17/A18; potentially a distinct biological subquestion.

### E-N2. Within the same oncogenic lung, does greater mutant burden accompany WT expansion, WT identity loss, or neither?

**Why this follows.** The source explicitly leaves open whether WT responses promote or constrain tumour progression. The spatial array lacks identifiers, but the nonspatial archive preserves RFP and YFP measurements under the same mouse index, with sampled lobe area. This offers a different, usable scale of comparison.

**Discriminating analysis.** Construct paired mouse summaries: area-normalized mutant labelled-cell burden, WT clone/cell density and WT pro-Sftpc-negative fraction. Compare within-time relationships before pooling times; retain mouse and lobe hierarchy and show every mouse. Treat induction density, shared injury, area estimation and the YFP-labelled subset as alternatives. Three or four mice per time point support descriptive paired contrasts, not a flexible covariate model.

**What would change the reading.** Different associations with WT size versus identity loss would support a host-level distinction beyond pooled distance curves. Positive correlation is not tumour promotion, and negative correlation is not protective competition. Direction requires intervention or longitudinal linked observations.

**Feasibility:** ready for descriptive analysis after mouse/channel mapping checks; no new spatial IDs are needed for this particular estimand. **Relation:** A18 and the source's unresolved WT-fitness question. Do not relabel it a spatial test.

### E-N3. Is apparent enrichment of fast founders explained by conditioning on surviving, expanded clones?

**Why this follows.** Methods S1 fits clones with size at least two. A starting founder fraction, fraction among surviving/proliferative clones and fraction of cells contributed by those clones are different quantities. EN6 already demonstrates strong implementation-dependent retention differences.

**Discriminating analysis.** Under each fully specified birth-death model, map founder mixture weights to expected extinction, singlet and expanded-clone fractions over time. Report the conditional and unconditional quantities together. Assess identifiability with the actual sampling rule; keep ambiguous observed singlets out of a forced proliferation interpretation.

**What would change the reading.** Similar conditional size tails arising from different founder mixtures and survival laws would weaken interpretation of a fitted mixture weight as a measured stem-cell frequency. Agreement between weights and independent lineage prevalence would strengthen it, but the current deposit does not supply the full joint lineage test.

**Feasibility:** ready as an A17 extension after the parameter/schedule contract is repaired. An analytical birth-death calculation can validate the corrected simulator cheaply; it cannot validate the literal erroneous code or replace its comparison silently. **Relation:** A4/A17; do not create a separate global RQ for a denominator correction alone.

### E-N4. Are the putative lesion-associated epithelial outputs coordinated beyond transitional-state occupancy?

**Why this follows.** Source Figure S7F highlights Hmga2 and EGFR ligands; S6 implicates SPP1/DLK1 in WT responses. The repository has mostly ranked single ligands or compared whole states. Whether these outputs form one programme or occur in different epithelial populations matters for choosing a niche mechanism.

**Discriminating analysis.** Freeze a small source-derived panel and contrasts before inspection. Within each eligible library, separate programme prevalence from within-state expression; define neighbourhoods without the tested genes, hold depth and cycling comparisons fixed, and include negative/control genes. Compare Cd177-enriched and DATP-like territories only where both have coverage. Report SPP1/DLK1 and EGFR-ligand axes separately rather than constructing a favourable composite after seeing them.

**What would change the reading.** Consistent residual co-variation would nominate a coordinated epithelial output phenotype. Dissociation would argue against one homogeneous “signalling hub.” Neither measures secretion, range or causal recipient activation.

**Feasibility:** counts are available for exploratory within-library work; phenotype coverage must be checked without relaxing gates. No animal-level RNA inference without independent pool mapping. **Relation:** A2/A9/A11/A12; this is a specified extension, not an unclaimed new pathway.

## Public-data pilots with explicit limits

### E-N5. Which epithelial identity features distinguish an aberrant hybrid state from a maturing AT1-like state across injury and oncogenic contexts?

**Why this follows.** The source supports mixed protein identities; the repository's RNA classification changes dramatically with its AT1 gate. “Transition,” “mixed” and “mature” cannot be treated as one continuum solely because modules overlap.

**Discriminating analysis.** Fit disjoint AT2-retention, transitional and late-AT1 axes; calibrate and evaluate on different animals/studies rather than reporting in-sample sensitivity as validation. Match effective RNA depth and assess ambiguous calls. Transfer frozen axes to England without forcing every cell into a mature class. Benchmark against independently labelled morphology/protein/fate where available.

**Feasibility:** an RNA-classification audit is feasible from existing England, Choi and Niethamer data. A functional mature-fate answer remains unavailable. **Relation:** A1/A8/A16; consolidate with these questions instead of assigning another identifier.

### E-N6. Does the CD177/priming association generalize to other oncogenic contexts, and is any difference attributable to a second driver?

**Why this follows.** England's Discussion contrasts Kras-only dynamics with Kras/Trp53 contexts. Transfer of a phenotype and causal attribution to Trp53 loss are separate questions.

**Candidate resources checked:** [GSE253461](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253461) contains WT and Kras/p53-deficient epithelial/organoid/mesenchymal observations; [GSE227719](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227719) contains organoid RNA/ATAC profiles. Its four GSMs are assay/condition entries, not evidence for four independent biological replicates. Neither metadata record alone supplies a matched Kras-only versus Kras-plus-Trp53 causal contrast.

**Discriminating analysis.** First audit biological preparations, genotype, time, culture and same-population coverage. If eligible, apply the corrected A16 test with frozen genes and separate libraries. Report within-study contrasts; do not subtract unrelated studies and call the difference a Trp53 effect.

**Feasibility:** metadata and conditional descriptive transfer are feasible; causal second-hit effects on reversible state transitions or equipotency require matched design and functional lineage outcomes. **Relation:** A16 and the source's second-hit hypothesis. The question is broader than the source's existing observation, but novelty across the literature is not asserted.

## Mechanistically valuable, not answerable from the current RNA/clone deposit

### E-N7. What permits feedback-regulator induction during productive maturation, and why is it altered in mutant states?

**Why this follows.** This is an explicit source limitation. The current analysis treats Nfkbia abundance as a candidate feedback-associated transcript, but feedback competence is a response over time, not a single expression level.

**Discriminating evidence needed.** Compare pathway activity, regulator induction and later maturation in linked cells or biological units under matched contexts. Test whether a regulatory/chromatin difference predicts or mediates that response, rather than merely co-occurring with an RNA state. Distinguish early state-entry inhibition from intervention after entry, and quantify viable mature-cell yield separately from growth suppression.

**Feasibility:** current data can nominate RNA/regulatory associations; they do not measure feedback dynamics, durable rescue or functional repair. Existing multiome candidates are context-mismatched and must not be promoted automatically. **Relation:** A1/A12/A14. The source's Nfkbia/BMS experiments motivate this question but do not answer the endogenous-induction mechanism.

### E-N8. Are SPP1 and DLK1 redundant, antagonistic or context-dependent drivers of WT-neighbour responses?

**Why this follows.** The paper reports greater WT organoid output with either ligand and a smaller size effect with their combination. That pattern motivates a non-additivity question; it does not already identify antagonism or a single causal mediator.

**Discriminating evidence needed.** A factorial comparison with independent biological preparations, separate formation/size/maturation outcomes and recipient engagement would distinguish redundancy, saturation, toxicity and antagonism. Establish ligand-source necessity before assigning an in-vivo spatial range. AREG-mediated fibroblast effects are a competing indirect route, not a substitute WT epithelial endpoint.

**Feasibility:** inspect/digitize existing figure-level evidence descriptively if needed; new causal resolution requires suitable measurements. [GSE316244](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE316244) is an Areg genotype study with separate epithelial and niche sorts from pooled mice, not a SPP1-by-DLK1 experiment and not spatial validation. **Relation:** A9/A12/A18; a bounded mechanistic subquestion.

## Directions kept as gaps, not advertised as feasible discoveries

- **Do fast and slow AT2 founders generate different mature AT1 subtypes?** Explicitly raised by the source. Needs founder-to-descendant linkage with AT1-resolved outcomes; current RNA sorting and inferred size classes cannot provide it.
- **Do remote WT neighbours eliminate small mutant clones?** Remote Cl-Casp3 staining motivates the hypothesis. The public clone sizes do not jointly identify apoptosis, local WT fitness and longitudinal clone disappearance. Repeated cross-sectional samples do not track extinction of a particular clone.
- **Can NF-kB inhibition restore durable alveolar function in vivo?** Organoid/PCLS marker and morphology changes motivate this, but the source explicitly leaves in-vivo validation open. This repository has no linked durable functional outcome.
- **Can velocity alone settle reversibility?** Re-quantification might enable additional model-dependent directional estimates. It would not supply lineage ground truth or demonstrate reversibility; it is lower priority than the specific attribution and mouse-level analyses above.

No claim of literature-wide novelty follows from this bounded sweep. The practical order is to correct A16's comparison, reconcile A17's inputs, then pursue E-N1/E-N2 using the available mouse hierarchy. E-N4/E-N5 are feasible but overlap existing RNA programmes; E-N6 needs a metadata gate; E-N7/E-N8 require additional mechanistic measurements.
