# Published evidence and reproduction targets

Source: [Wang, Wagner, Fessler et al. 2025](https://doi.org/10.1016/j.celrep.2025.115799),
owner-supplied PDF (16 pages, main text with STAR Methods) and the supplemental
information PDF (9 pages, legends plus Table S2). Page numbers below are PDF
pages of those two files. Everything in the second column is a published
observation, not a repository finding.

| Source locator | Published measurement | Reproduction product under Wp-R01 | Interpretation limit |
|---|---|---|---|
| Fig. 1A–1B; main pp. 3–4; Methods p. 16; Table S2 | Compass potential activity of ~900 reactions in 1,311 Th17n cells, ranked by Spearman correlation with the pathogenicity score; 3PG→PEP and the 3PG serine shunt negative, LDH/PDH/PCK positive | Wp-R2 only: re-derive reaction scores and the correlation ranking | Potential activity is neither measured flux nor enzyme activity; the ranking is over cells, which are not independent units |
| Fig. 1C–1D; main pp. 3–5; Methods p. 15 | Flow-cytometry cytokine frequencies in division-1 Th17n cells under DHEA, EGCG, shikonin, DCA against matched solvents at viability-guided doses (EGCG 20–50 µM, DHEA 50 µM, DCA 40 µM, shikonin 10 µM) | None. No numeric values deposited | Inhibitor selectivity is assumed, not measured here; a frequency change in surviving divided cells can reflect state, survival or division gating |
| Fig. 1E; main p. 5; Methods p. 15 | 13C ratio in 3PG, 2PG and PEP after 15 min of 8 mM [U-13C]glucose at 96 h; 2PG labelling falls from 51% to 7% with EGCG | None. No LC/MS values deposited | Fractional labelling is not flux; the result supports on-target action at the PGAM step within glycolysis, not whole-pathway specificity |
| Fig. 1F–1G; main p. 5 | RT-qPCR knockdown and secreted IL-17A/IL-17F/IL-2/TNF-α after PGAM sgRNA in Cas9 Th17n cells, one dot per lentiviral infection | None. No numeric values deposited | Independent infections are not independent animals; knockdown magnitude is not reported per experiment here |
| Fig. 2A–2D; main pp. 5–6; Table S3 | Bulk RNA-seq of division-1 Th17n/Th17p under EGCG or DHEA and solvents; EGCG raises the pathogenic program and lowers the Th17n program; DHEA promotes the regulatory program only in Th17p | Wp-R3: recover the 79-library design, reproduce the four within-cell-type contrasts and the three-group logFC partition (BH ≤ 0.05, \|log2FC\| ≥ 1.5 between DMSO Th17p and Th17n) | Deposit is TPM only with no animal field; the library is the only verifiable unit, so these are descriptive contrasts, not animal-level inference |
| Fig. 2E; main p. 5; Table S3 | Per-cell EGCG and DHEA response signatures scored in untreated Th17n cells; Pearson rho 0.79 (EGCG) and 0.36 (DHEA) against the pathogenicity score | Wp-R1: re-derive both signatures from the bulk contrasts and re-score cells | Both scores are built from overlapping gene sets; a high correlation between two transcriptional summaries is not independent validation |
| Fig. S2; Table S4 | Spearman and DHEA-adjusted partial Spearman correlation of each gene with the EGCG signature; CD5L highlighted | Wp-R1 extension: recompute both correlations | A gene correlated with a treatment-response signature is not shown to mediate it |
| Fig. 3A–3C, S3; main pp. 7–8; Methods p. 15 | Extended single-cell dataset (25 mM and 1 mM glucose), metabolic-transcript fraction, and the pathogenicity score rising at low glucose through loss of the pro-regulatory arm (two-sample t test p < 10⁻³³) | Wp-R1: re-derive the embedding, the metabolic fraction and the arm-wise score decomposition from the deposited matrix | Cell-cycle phase dominated the structure and was regressed out; proliferation differs by condition, so it is a confounder, not a nuisance. the two animals are crossed with all four conditions, so a paired contrast exists at n = 2, and a cell-wise t test is not population inference |
| Fig. 3D; main p. 8 | Genes with a significant glucose-by-condition interaction (p < 0.001), including TBX21, CCL5, IL23R, IL22 up at high glucose and CSF2, GZMB up at low glucose in Th17p; FOXP3, CTLA4, IL2RA, TSC22D3 glucose-sensitive in Th17n | Wp-R1: refit the interaction model on re-derived labels | with two animals crossed over the conditions the interaction is estimable but rests on n = 2; gene selection was annotation-restricted to Th17 effector genes |
| Fig. 3E–3G, Tables S5–S6; main p. 8; Methods p. 16 | Leiden resolution 0.8 gives 10 clusters, 3 excluded (110 cells), 7 retained as N1–N3 and P1–P4 under a ≤100-cells-in-other-conditions rule; N1 is FOXP3/SGK1-high and least pathogenic | Wp-R1: re-cluster and map to the published programs by marker concordance only | Cluster identity across pipelines is not established by name; the final 5,192-cell set and its exclusions are not deposited |
| Fig. 3H–3J; main p. 8 | N1 cells score lowest for the EGCG signature; GSEA of N1 markers against EGCG-downregulated genes BH-adjusted p < 10⁻⁸; no comparable DHEA trend | Wp-R1: repeat the score comparison and the GSEA with re-derived gene sets | The N1 markers and the EGCG signature both come from the same two datasets; this is internal consistency, not independent replication |
| Fig. S4; main p. 8 | Human reuse of GEO GSE138266: CD4 T cells pseudobulked by donor and tissue; both modules up in MS blood and CSF, EGCG signature up in MS blood only, N1/P1/P4 higher in MS blood | Wp-R4: rebuild the donor-level pseudobulk and re-test, with an activation score as a competing explanation | Both modules moving together is consistent with generalised T-cell activation; this cohort is the only donor-level unit in the paper |
| Fig. 4A–4J, S5; main pp. 8–10 | Adoptive-transfer EAE: DHEA-treated Th17p reduces peak severity without changing incidence or lesion counts; EGCG-treated Th17n induces EAE (10 of 12 versus 0 of 12, Fisher p = 1.1 × 10⁻⁴), raises CNS lesions (p = 0.0093), raises MOG-recall IL-17/IL-17F/IL-22/IL-6, and is the only group with Wallerian degeneration | None. No animal-level numeric data deposited | This is the only functional outcome in the paper; it is CNS autoimmunity after transfer of drug-exposed cells, not a within-tissue PGAM manipulation |

## What is not available

The Excel supplements are not in the supplied supplemental PDF, which carries
legends and Table S2 only, but **all five were recovered on 4 October 2026** from
the NIH PMC Cloud open-data package `PMC12443480.1` (see
[source manifest](SOURCE_MANIFEST.md)): Table S1 the module gene lists with their
`is_HVG` flags, Table S3 the limma differential expression behind the EGCG and
DHEA signatures, Table S4 the per-gene correlations, and Tables S5–S6 the
programme markers. Wp-R1 and Wp-R3 are therefore exact reproductions of the
published definitions, and each re-derived signature can be compared gene-for-gene
against the authors' own table rather than only re-estimated.

What remains unavailable is the processed single-cell object: the 5,192-cell
analysed set, its exclusions and the fitted scVI model are not deposited, so a
re-derived embedding and its clusters differ from the published ones by
construction. That limit is independent of the tables.

Two documentation problems are recorded rather than resolved:

1. **Sign conflict.** The Results text defines the pathogenicity score as
   pro-inflammatory minus pro-regulatory; STAR Methods states the score is
   obtained "by subtracting the pro-inflammatory module score from the
   pro-regulatory module score". The figures behave as the Results text, so the
   Methods sentence is read as an error. The same conflict is already recorded as
   an open dependency in the
   [2021 package](../gate2_W1_wagner_th17_autoimmunity/HANDOFF_2026-10-04.md),
   so a single authoritative resolution would serve both.
2. **Cohort description.** The reused human deposit contradicts itself:
   GSE138266's own overall-design field states a five-versus-five case-control
   design with two samples per donor, while its sample records resolve to 22
   samples across 6 MS and 6 control donor codes. This is the deposit's
   discrepancy, not a statement in the Wang text, which describes the cohort only
   in general terms. See [Datasets](DATASETS.md#human-reuse-cohort).

## Reproduction outcomes recorded 4 October 2026

Four stages have executed under the governed runner. The claim-by-claim outcome
table lives in [REPRODUCTION_SCOPE.md](REPRODUCTION_SCOPE.md#claim-by-claim-outcome-4-october-2026);
the stage reports are [R0](R0_RESULTS.md), [R3](R3_RESULTS.md), [R1](R1_RESULTS.md)
and [R4](R4_RESULTS.md). Three findings change how rows above should be read.

1. **Fig. 2 (bulk, Th17n EGCG).** The contrast reproduces against Table S3 on the
   first-division gate, but at module level the EGCG effect in Th17n is not
   selective for the pro-inflammatory group once the global shift is centred out.
   The single-gene claims (IL17A, IL17F) do reproduce.
2. **Fig. S4 (human).** Not module-specific. A matched-size random gene set
   separates the two blood cohorts as well as the modules do, and nothing
   separates the CSF cohorts at all.
3. **EAE incidence p value.** The deposited table (10/12 versus 0/12) gives
   two-sided Fisher p = 6.7e-5 against the published 1.1e-4. Ours is the smaller
   value, so the published figure is more conservative and the conclusion stands;
   the test used is not stated in the paper.
