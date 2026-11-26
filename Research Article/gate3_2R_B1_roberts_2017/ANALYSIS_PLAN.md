# B1 · How can a tissue macrophage clear dying cells without treating their nucleic acids as danger?

**Organizing question.** A macrophage repeatedly engulfs dying neighbors and delivers their contents to a compartment that can sense nucleic acids. Which part of the restraint is present before uptake, which part changes after cargo arrives, and how readily can a tissue reverse that restraint? This is the question raised by the reading notes and by the contrast between resident phagocytes and cultured cells. Study the uptake and sensing arms separately before asking whether KLF-dependent tissue programming coordinates them. [Roberts et al., Figs. 1–7](https://doi.org/10.1016/j.immuni.2017.10.006)

**Working explanation.** The niche equips selected macrophages to recognize dying cells while setting a high threshold for an inflammatory response. Receptor abundance is one layer. The decisive observation is Fig. 2F: enforced TLR9 expression restores responsiveness to its ligand while apoptotic cells still fail to elicit the same response. Interferon produces another partial restoration in Fig. 6. An inducible response to digestion can also operate after uptake. Selection of different cells during 60 h of culture is a further explanation for a bulk expression change. The paper already establishes several parts of this model. Ravel can test which measured components track together across the released experiments. [Literature comparisons and external source](LITERATURE_CONTEXT.md)

## S0 · Reconstruct the phenotype before choosing transcripts

Start a figure-to-evidence table from the paper. For each row record population, cargo or ligand, exposure time, assay, biological unit, denominator and source format. Extract individual values only where traceable. Retain a categorical author-reported observation for representative blots, histograms or curves lacking source values.

| Comparison | Published anchor | Biological decision |
|---|---|---|
| Who clears cells at steady state? | Fig. 1C–E, peritoneal, pleural and lung populations | Use the gated fraction that acquires cargo. Tim-4 marks cavity engulfers, whereas alveolar macrophages can clear cargo without it. |
| Does receptor availability explain silence? | Fig. 2B–F and Fig. S2C, TLR9 reporter, protein, enforced expression, CpG versus apoptotic cells and uptake control | Retain the ligand/cargo dissociation. Lower cargo uptake would give a different explanation from higher activation threshold. |
| Can the environment remove and confer the phenotype? | Fig. 3A–F after culture and Fig. 4A–D after transfer of bone-marrow-derived macrophages into cavity or lung | Contrast loss and acquisition in their own experiments. The reciprocal design is stronger evidence for environmental instruction than either expression profile alone. |

Fig. 2E uses myeloid-restricted TLR9 expression and littermates to test ligand responsiveness across macrophage populations. Fig. 2F compares TLR ligands and apoptotic cells in Tim-4-positive peritoneal macrophages from constitutive RosaTlr9 mice. Fig. S2C addresses the uptake alternative. Keep the two expression models and their comparators visible when reconstructing that negative result.

**First deliverable.** A population-by-exposure figure key showing uptake, TLR9 and TNF as different columns, with observed and missing combinations explicit. The first numerical reproduction is the two-experiment peritoneal comparison below.

## S1 · Reproduce loss of the tissue-associated program

Build a manifest with GSM, experiment, time, cargo, sample type, preparation or pool, replicate role, input filename, scale and checksum. The 14 GEO records break down as follows.

| GSM suffix (GSM246…) | Deposited samples | Analysis use |
|---|---|---|
| 2968–2970 and 2971–2973 | In each experiment, one immediate ex vivo and two 60 h Tim-4-positive peritoneal macrophage libraries | Two within-experiment comparisons. Keep both 60 h values visible. |
| 2974–2977 | Programmed macrophages, two without and two with apoptotic cells | One challenge experiment with technical duplicates according to Fig. 3G |
| 2978–2979 | Deprogrammed macrophages with apoptotic cells | Matching 60 h unstimulated challenge denominator has no explicit GSM label |
| 2980–2981 | Apoptotic thymocytes alone | Cargo RNA control |

Read the Kallisto quantification headers or HDF5 fields, verify transcript IDs against the reported mouse GRCm38 release 79 transcriptome and map uniquely to genes. Distinguish estimated counts from TPM. Establish whether the 60 h specimens in the first six records also supply the Fig. 3G denominator from explicit source evidence. An identical culture duration is insufficient. Deliver a sample map and a panel eligibility note before calculating fold changes.

Use 60 h minus immediate ex vivo on a common log-expression scale within each experiment. Define normalization and low-expression handling before reading values. Summarize the two 60 h libraries within each experiment and show their scatter. Report both experimental effects. The unit for concordance is the experiment until source documentation establishes individual animals or pools.

Use a fixed paper-derived panel with recognition genes *Timd4, Marco, Olr1*, signaling regulators *Socs3, Dusp1, Ptpn6*, and *Tlr9* separately. Give each gene’s baseline, direction and magnitude. Mark low or missing values and preserve cases that remain stable. Display an experiment-by-gene plot with its underlying values. Two experiment contrasts support a descriptive reproducibility check.

**What would change.** Loss of recognition and inhibitory genes in both experiments would support coordinated lability. Preserved recognition with a selective change in inhibitors would focus the question on signal handling after uptake. Heterogeneity between experiments leaves individual genes unresolved. None of those patterns demonstrates that a given resident cell changed state.

## S2 · Reproduce the response to apoptotic cargo

Collapse the technical duplicates after QC. For the verified programmed comparison, calculate the within-experiment stimulated-to-unstimulated change for *Tnf, Il1a, Il1b* and *Cxcl2*. Follow the authors’ rule excluding genes expressed more than twofold higher in cargo-only RNA than macrophage RNA, documenting which reference and scale were used. Flag any unresolved denominator or cargo assignment. If the matched deprogrammed baseline is established, show both fold changes and their difference on the log scale. Otherwise report the supported programmed arm, the available deprogrammed stimulated values and the precise missing link. No mouse-level test is available for this challenge.

Ask separately about inflammatory cytokine RNA, resolving mediators and the ability to take up a second corpse. Figure 3G measures the first category at one time. Even a quiet inflammatory RNA panel permits rapid transcription of processing genes. Report whether any assayed transcript can be attributed confidently to the macrophage. A positive cargo-only flag or unresolved denominator limits that comparison alone.

## S3 · Distinguish TLR9 availability, downstream sensitivity and niche dependence

Read the dose series in Fig. 5C–G alongside phospho-ERK (5A) and the inhibitor RNA panel (5B). Within a ligand and preparation, record low- and high-dose responses and whether the cells retain response capacity. In Fig. 6A–B record how interferon changes CpG response, TLR9 protein and response to apoptotic cells. Locate the corresponding receptor and signaling perturbations in Fig. 3E–F and the KLF-loss or gain experiments in Fig. 7. Do not combine doses or tissues across panels. If only representative curves are released, report the ordering and controls, leaving fitted thresholds and between-mouse variation unestimated.

Assemble these as a figure with one row per perturbation and columns for uptake, receptor, signaling and cytokine. This tests whether recovery of receptor alone, as opposed to recovery of additional signaling competence, predicts cargo responsiveness. Use the configuration that fails the proposed explanation, particularly TLR9 restoration with persistent silence, to interpret any RNA agreement. Pestal can then address how cells acquire a KLF-dependent cavity identity. Its native KLF2 peaks do not measure Roberts’s TNF response. [Pestal comparison](../gate3_2R_B2_pestal_2025/ANALYSIS_PLAN.md)

## S4 · Test whether the distinction travels to another phagocyte context

A-Gonzalez et al. compare cargo-positive and cargo-negative macrophages within marrow, intestine and spleen. If S1/S2 leave a constitutive-versus-cargo-associated question, qualify GSE83222 by tissue, label, preparation and pooling. Freeze the overlapping recognition and inhibitor genes from S1, then compare cargo-positive minus cargo-negative **within each tissue**. Show genes absent from the platform and all tissue directions. This estimates an association with cargo status among resident cells. Preferential uptake by pre-existing subsets is a live biological explanation. If this design cannot discriminate induction from selection, report the association and use the timed uptake/processing studies in the context note to identify the missing measurement. [External deposit](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE83222)

## S5 · Write the biological synthesis

Organize the finished account under three findings: which cells engulf, what permits them to remain quiet, and what engulfment itself induces. Place Roberts's two restoration experiments beside the reanalysis and the external prospective-label or timed-uptake evidence. Identify which transition is demonstrated in the same population and which would require following individual viable cells through niche withdrawal or a second encounter. If the RNA contrasts add only reproduction, close there with the measured figures and a precise statement about signaling sufficiency.

**New-session prompt.** Start `gate3_2R_B1` with the Fig. 2F and Fig. 6 counterexamples and the S0 population map. Run the eligible RNA reproductions sequentially, then use S3 and the literature context to decide whether S4 would distinguish a remaining explanation. Return the source-value figures, unsupported panels and the biological conclusion about uptake, sensing and cargo response. [Shared execution instructions](../README.md#gate-3-second-round)
