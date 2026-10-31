# Saxton IL-22 paper and research fit

31 October 2026. Reading assessment against fetched main `8cb50dd15a12a41abc6d5edb36349d33fc512661`, which includes merged DY1 PR #153. This is a literature assessment, not a reproduction, new canonical RQ, execution contract or human scientific decision. The user's abstract/introduction/discussion reading is distinguished from this review of the main results, relevant methods and figures.

## Assessment

The paper is useful for the owner's interest in how inflammation changes epithelial cells and their niches, and why tissue recovers or remains dysfunctional. Its strongest contribution is a causal example of **recipient context changing the biological meaning of a cytokine input**. Structure-guided perturbation enables that test; protein engineering need not become the owner's preferred method or research identity.

The correct paper is Saxton et al., *Immunity* 54, 660–672.e9 (2021), [DOI 10.1016/j.immuni.2021.03.008](https://doi.org/10.1016/j.immuni.2021.03.008). The initially attached IL-10 *Science* article is a separate study. Both local PDFs were identified; the subsequently supplied IL-22 PDF is the primary source here. Its 23-page version includes the graphical abstract and STAR Methods. The local filename is `Saxton et al_2021_The tissue protective functions of interleukin-22 can be decoupled from pro-inflammatory actions through structure-based design.pdf` in the owner's `AC_document/Research_Article/SAP_Thesis study/Gate3/Saxton` folder.

The owner-provided research notes prioritize inflammatory state, regenerative competence and epithelial–niche communication. The scientific fit is distinct from preference for a particular experimental method. Private planning notes and their links are not reproduced in this research record.

## Evidence worth reading

| Figure and local PDF locator | Biological result | Interpretation limit |
|---|---|---|
| Fig. 7, PDF p. 10 | Selected organoid/intestinal radiation and acute pancreatic injury outcomes are retained while several inflammatory outputs fall | Organoid metabolic viability, crypt recovery and serum injury markers are distinct endpoints. They do not establish durable epithelial lineage restoration, lung AT1 maturation or chronic safety |
| Fig. 5, PDF p. 8 | The same 22-B3 variant has different signaling profiles across tissues: strong STAT3 bias in colon, weaker bias in pancreas, and little detectable activation in liver/skin. Receptor-expression experiments support a role for IL-10Rβ availability | Whole-tissue receptor RNA is not cell-specific surface protein. Tissue context cannot be reduced to one receptor transcript |
| Figs. 3–4, PDF pp. 6–7 and accompanying results | STAT1 and STAT3 responses can separate; receptor-associated signaling has different requirements/thresholds | A phospho-STAT response is a proximal measurement, not a repair endpoint. Selectivity is conditional on the tested recipient context |
| Fig. 6, PDF p. 9; RNA-seq methods p. 23 | Bulk colon RNA links retained barrier-associated programs and reduced selected inflammatory transcripts to the altered input | Bulk composition and within-cell regulation are not separated. The methods report two independent biological replicates; technical qPCR triplicates are not extra biological units |
| Figs. 1–2, PDF pp. 4–5 | Structural work supplies a controlled perturbation of receptor engagement | Read enough to understand what was changed and why the comparison is informative; detailed interface engineering is optional for the owner's biological question |

Two processes contribute to the outcome: different downstream signaling within a responsive tissue, and different activity across tissues. The paper's discussion (PDF pp. 11–12) explicitly notes that hepatic acute-phase outputs such as SAA1/2 are STAT3 targets. Reduced liver STAT3 activation can therefore reduce systemic inflammatory output, while potentially losing beneficial IL-22 actions in that tissue. The result is not a general equation of STAT3 with protection and STAT1 with damage.

The main paper's acute outcomes are valuable evidence of separability in those models. They do not answer whether a previously injured epithelial state retains the same response, whether the response persists after withdrawal, or whether early survival becomes durable functional regeneration. Main-paper figures 5–7 were also visually checked against their extracted text; supplementary experiments were not exhaustively reviewed.

## The necessary companion and the remaining question

[Cineus, Luo et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12133592/) provide the relevant boundary: epithelial IL-22-dependent OSMR induction requires STAT3 (Fig. 4f–h), and the IL-22–OSM circuit supports intestinal inflammation and tumorigenesis. OSMR falls after IL-22 withdrawal in the examined organoid setting (Supplementary Fig. 5e, reported in main text). This is not a test or refutation of 22-B3; it shows why STAT3 activation alone cannot certify protection. Review scope: abstract, Fig. 4/results and the relevant withdrawal/discussion passages.

An older precedent, [Bachmann et al. 2013](https://pubmed.ncbi.nlm.nih.gov/23153456/), reports that IFNα priming changes epithelial IL-22 responses toward STAT1 and inflammatory targets. Only its abstract was read. Thus, "inflammatory context changes cytokine response" is an established premise, not a novelty claim.

A useful discussion question is: **Does an injury-associated epithelial state change the balance of inflammatory output and recovery after the same cytokine input, and does that difference remain after the preceding inflammatory signal has ceased?**

This is a framing prompt, not a registered or execution-ready RQ. Its fit-for-purpose comparisons would distinguish current receptor availability and ongoing cytokine exposure from retained state/history, and distinguish composition shifts from responses within comparable epithelial populations. Evidence that the difference disappears after withdrawal would argue against persistent memory; a persistent RNA difference alone would still not establish altered regenerative function. A future functional claim requires a nominated tissue-relevant recovery endpoint and valid biological units. No effect margin or new experimental group is invented here.

## Fit to current repository evidence

| Existing question/evidence | What the paper adds | What it does not supply |
|---|---|---|
| [A19 receptor response/reversibility](../../../RQ_Specified/A19_fzd_response_reversibility/RESULTS.md) | A concrete example of receptor context making the same signaling input biologically different | The current withdrawal evidence does not become receptor-specific Fzd evidence or mature AT1 recovery |
| [A14 withdrawal/reception](../../../RQ_Specified/A14_withdrawal_recovery_and_reception/README.md) | A reason to separate inflammatory history, ongoing input and recipient responsiveness | The acute IL-22 study does not test post-cessation persistence or fibroblast IL-1 reception |
| [A22 epithelial identity/niche response](../../../RQ_Specified/A22_epithelial_identity_niche_response/README.md) and [A2 source/delivery](../../../RQ_Specified/A2_areg_source_delivery/README.md) | Ligand/source RNA alone cannot determine what the recipient does; recipient context matters | No proof that the IL-22 mechanism explains the existing NKX2-1/chemokine observations or acts directly in fibroblasts; RNA remains distinct from extracellular protein output |
| [A1 regulatory distinction](../../research_dossiers/A1.md) and [A8 mature output](../../research_dossiers/A8.md) | A useful separation of receptor, proximal signaling, transcription and functional endpoints | No paired chromatin/fate evidence, lineage tracing or mature alveolar repair endpoint |
| [DY1 RNA–ATAC branch](../../../Research%20Article/gate2_DY1_damani_yokota_2026/rq_discordance/README.md) | Reinforces that expression, signaling activity and biological outcome are different measurements | Does not resolve RNA–ATAC discordance or establish STAT6–PPARγ/RXRA or ARG1 mediation |

The existing [Niethamer S1 proposal](../../../Research%20Article/gate1_01_niethamer_2025/ANALYSIS_TRIAL_PLAN.md) describes “STAT3-like protective versus STAT1-like inflammatory” epithelial program scores. Before any future execution, interpret these as context-dependent response signatures and evaluate protection separately. This recommendation leaves the historical proposal, its unrun status and numerical gate unchanged. Reading is already open and does not require a favorable numerical result.

## Bounded computational opportunity

The paper deposits bulk colon RNA-seq as [GSE160217](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE160217). The indexed GEO entry identifies PBS, WT IL-22 and 22-B3 groups and a read-count supplement. Direct GEO page access returned a browser challenge in this review; file contents, sample-to-animal identities and exact group sizes were not qualified. No data were downloaded or analyzed.

If the owner chooses a reproduction, the first useful sequence is:

1. Qualify count files, sample/animal identities, treatment metadata, annotation and the reported replication. Record prior exposure to Fig. 6 and formulate an exploratory/reproduction contract before numerical work.
2. Compare WT versus PBS, 22-B3 versus PBS and **22-B3 directly versus WT**, using the animal as the biological unit. Show effect estimates and uncertainty; a significant WT result beside a nonsignificant variant result is not itself a between-treatment difference.
3. Describe retained and reduced transcriptional responses without calling an underpowered null “equivalence.” Separate reproduction of published gene panels from independently specified exploratory gene sets. Bulk RNA does not identify the responding cell type or directly measure STAT phosphorylation.
4. Only then consider mapping context to a qualified epithelial-state dataset. Receptor RNA can describe candidate response context; it cannot establish variant sensitivity, persistent memory or repair benefit. Reusing the original samples is reanalysis, not independent replication.

This is a smaller and more relevant possible entry point than reproducing the structural-design workflow. It remains optional, gated by source qualification and a prospective contract, with no analysis or canonical RQ change authorized by this reading record.

## Reading decision and source record

The owner-provided reading order recommends **Fig. 7 → Figs. 3–6 → Figs. 1–2**. For the owner's stated concern, start with Fig. 7, then read Fig. 5 closely and Figs. 3–4/6 as its mechanistic/transcriptional support. Skim the structural details after understanding the biological comparison. Add the 2025 companion's abstract and Fig. 4 before deciding whether to pursue this direction. The separate IL-10 paper is optional follow-up, not a substitute for this evidence.

The owner-provided paper and discussion notes were read; the results note was empty. A small note correction is JAK1/TYK2 rather than “JAL1/TRK2.” No private note was modified or paper reading marked complete.

Search date: 31 October 2026, Asia/Seoul. Sources: supplied published IL-22 PDF, PMC published full text for the 2025 companion, PubMed abstract for the 2013 precedent, supplied Notion pages and their reading-order/notes links, and current repository evidence above. The bounded web searches were:

- `Saxton 2021 tissue protective functions interleukin-22 decoupled pro-inflammatory structure-based design`
- `"s41590-025-02149-z"`
- `"IL-22" "STAT3" "lung" repair epithelial 2024 2025 2026`
- `IL-22 STAT1 interferon priming IL10RB Bachmann 2013 epithelial`
- `GSE160217 samples WT B3 PBS colon RNA sequencing`

Coverage establishes the paper's identity, the closest owner-nominated contrary context and an older priming precedent. Other lung search hits were not qualified as functional maturation evidence. This is neither a systematic review nor novelty clearance. Future question development must refresh the literature for its actual comparison under the [literature workflow](../../LITERATURE_WORKFLOW.md).
