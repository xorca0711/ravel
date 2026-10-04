# Primary-source update for the pre-derivation review

Searched and inspected 4 October 2026. This is a bounded update to the
[earlier review](../PRECEDENT_REVIEW.md), triggered by the completed R3 model
and the requested extension/overlap assessment. No finite search proves novelty.
Source findings below are distinct from [local numerical evidence](../MODEL_RESULTS.md).

## New close precedents and contrary boundaries

| Source and version | Evidence actually inspected | Consequence / qualification |
|---|---|---|
| [Hu et al., Molecular Therapy](https://doi.org/10.1016/j.ymthe.2022.10.013), online 28 October 2022; issue 1 February 2023, 31:569–584 | Full-text XML: relevant Results, Fig. 1/2/5/6 legends, study design, cell-source and statistical methods; supplement PDF pp. 2–6, Tables S1/S2 and S1–S4 legends/text | MDSC/ornithine/polyamine support of Th17 polarization is an existing premise for P03/P06. Human cultures use cord-derived cells; SLE PBMC associations and humanized-mouse outcomes are separate units. S1/S2 report no detected DFMO-alone effect under their conditions, which is not equivalence or a matched contradiction of Wagner. Representative-experiment triplicates are not independent donors. Precursor routing is partly inferred; total-polyamine measurements do not resolve compartment-specific flux. No reusable expression accession was located in the inspected XML |
| [Wu et al., Science Translational Medicine 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4895207/), 23 March 2016, 8:331ra40 | Hu backward reference; primary abstract/Results context, study design and supplement inventory. Full supplementary data not audited in this pass | ARG1-dependent MDSC–Th17 autoimmunity predates Hu and Wagner. Recruitment at the First Hospital of Jilin University in May 2012–June 2014 overlaps Hu's September 2012–November 2013 SLE recruitment. Shared patients are possible, not proven; no patient identity reconciliation. Count as a connected research lineage until independence is established |
| [Ren et al., Science Translational Medicine 2025](https://pubmed.ncbi.nlm.nih.gov/41124285/), 22 October 2025, DOI 10.1126/scitranslmed.adn1150 | Primary abstract and bibliographic/full-text metadata only. Publisher returned 403; Europe PMC reports subscription access and no PMCID | HIVEP1–ODC1 control of Th17 differentiation/cytokines in NASH is reported. This constrains a generic claim that ODC1 regulation in inflammatory Th17 contexts is new. Exact perturbation comparisons, supplements, data accessions and reuse remain unverified; no mechanism is imported into lung or the current R3 interpretation |
| [Yu et al., FASEB Journal 2026](https://pubmed.ncbi.nlm.nih.gov/41797515/), DOI 10.1096/fj.202503998R | Primary abstract; Europe PMC first-publication metadata 1 March 2026, PubMed issue date 31 March 2026. Publisher full text not retrieved; no open full text in Europe PMC | Reports GEO-based ALDH5A1 discovery and functional Th17 follow-up in SLE. It is a nearby enzyme-discovery precedent, not evidence for a local ALDH5A1 result. Exact GEO reuse, model validation and proliferation-versus-differentiation discrimination require full text before an overlapping proposal |
| [Li et al., PLOS Genetics 2014](https://doi.org/10.1371/journal.pgen.1004524), 31 July 2014; [correction](https://doi.org/10.1371/journal.pgen.1010701), 30 March 2023 | Relevant conditional/stage-specific Results, Fig. 2/3 context, microarray/ChIP methods; correction text and revised Fig. 3/6 legends | Developmental stage and compartment constrain JMJD3 lung phenotypes. The correction replaces duplicated images in Fig. 3D and Fig. 6H. Use the corrected record; no independent image-forensics or raw-data validation is claimed. Developmental architecture/surfactant endpoints do not establish adult post-injury AT1 competence |
| [Peng et al., Molecular Medicine Reports 2021](https://doi.org/10.3892/mmr.2021.12447), 24:807 | Publisher Results/Fig. 1–4 legends, animal/cell/statistical methods, limitations and data availability | Reports injury-associated effects of epithelial JMJD3 deficiency and Nrf2-related measurements. A549 is a tumor line; short-term lung injury and ferroptosis-associated markers are not durable maturation. Methods describe an Sftpc-cre; Jmjd3+/flox genotype, so complete deletion should not be inferred from the “CKO” label alone. Data are available on request; no qualified public numerical matrix was identified |
| [eFPA author repository](https://github.com/WalhoutLab/eFPA), checked 4 October 2026 | Current README, 10/1/2025 notice and runtime/data requirements, in addition to the earlier full-paper/appendix audit | The notice describes continuing development, not a scientific correction. A comparative rerun would need a pinned implementation, model, solver and distance matrix. Current code is not automatically the paper version, and eFPA is not a drop-in recovery of historical Compass |

For Peng, Nrf2 overexpression accompanying the JMJD3 perturbation does not by
itself establish Nrf2 necessity. Retain the distinction between the authors'
mechanistic interpretation and the specific comparisons inspected.

Hu's supplement was retrieved through the Europe PMC supplementary-files API
after PMC browser challenges; PDF text inspection covered the control and source
comparisons above. Its plots were not digitized and the entire supplement was
not independently reanalyzed. The claimed no-effect result stays a reported
null at its own conditions. Wu's raw-data supplement is listed publicly but was
not fetched for numerical reanalysis.

## Existing closest work retained without a duplicate full audit

| Candidate | Prior primary findings that already answer the broad premise | Exact remaining distinction |
|---|---|---|
| P01/P02 | [PGAM 2025](https://doi.org/10.1016/j.celrep.2025.115799) tests glycolytic control; [eFPA 2025](https://doi.org/10.1038/s44320-025-00090-9) examines expression/network information | A Wagner-specific representation and robustness comparison, not a first glycolysis mechanism or first network benchmark. PGAM's Results/Methods signature-sign discrepancy remains unresolved |
| P03 | [Puleston 2021](https://doi.org/10.1016/j.cell.2021.06.007) includes lineage fidelity, division-stratified markers and growth/viability controls | A newly specified conditional outcome or transport comparison, not merely “polyamines act beyond proliferation” |
| P04 | Wagner Fig. 6 and earlier [Li 2014](https://doi.org/10.1038/ncomms6780)/[Liu 2015](https://doi.org/10.1093/jmcb/mjv022) T-cell JMJD3 studies | Direct genotype-by-treatment differences at a defined endpoint; no universal statement about JMJD3 from one RNA assay |
| P05 | [Choi 2020](https://doi.org/10.1016/j.stem.2020.06.020) tests withdrawal/glycolysis; [AHR organoid 2025](https://doi.org/10.1038/s42003-025-08446-5) supplies a stromal/functional comparator | Added information from an early feature to later mature output on linked biological units, conditional on current state and exposure |
| P06 | [Yadav 2025](https://doi.org/10.1172/JCI188734) tests myeloid ornithine supply and fibroblast use; [Hamanaka 2025](https://doi.org/10.1042/BCJ20253033) tests fibroblast arginine context | A specified context or recipient-routing boundary with a distinct endpoint; collagen, alpha-SMA and Th17 cytokine output are not interchangeable |

Methods/supplement locators and accession identities for these sources remain
in [PRECEDENT_REVIEW.md](../PRECEDENT_REVIEW.md). Its preprint/successor links
and shared-human-MS-data finding are retained. No new full-paper audit of those
unchanged premises is claimed here.

## Search and access ledger

Service: live web search with primary publisher, PubMed/PMC and Europe PMC
follow-up. Recent discovery terms covered 2024–2026, alongside unrestricted
older-precedent searches; no date-filter exclusion was applied. Queries below
are the actual strings used in this review, including searches that returned
irrelevant material. Search snippets and reviews were discovery aids only.

| Search purpose | Queries |
|---|---|
| Broad recent boundary scan | `"polyamine" "Th17" "Treg" 2025 2026 metabolism lineage stability`; `"alveolar" "polyamine" "epithelial" regeneration 2024 2025 2026`; `"ornithine" "fibroblast" "arginine" fibrosis 2025 2026`; `"metabolic" "Compass" "benchmark" "expression" eFPA` |
| Lung and algorithm specificity | `"alveolar epithelial" spermidine regeneration differentiation`; `"JMJD3" "alveolar" regeneration epithelial`; `"Th17" "polyamine" "2026" -review -Frontiers`; `"eFPA" "metabolic" "2025"`; `spermidine alveolar epithelial type II cells pulmonary fibrosis 2015 2018 primary study`; `enhanced flux potential analysis enzyme expression metabolic flux eFPA 2025 Nature` |
| Closest new primary leads | `"JMJD3" "lung" "12447"`; `"Polyamines from myeloid-derived suppressor cells"`; `"HIVEP1" "ODC1" Th17`; `"HIVEP1 aggravates NASH by reprogramming polyamine metabolism in TH17 cells"`; `"Arginase-1-dependent promotion" "2016"` |
| Source identity, access and updates | `"adn1150" "GSE"`; `"adn1150" full text supplementary data`; `"HIVEP1" "NASH" "GSE" "Ren"`; `"10.1016/j.ymthe.2022.10.013" correction OR retraction`; `"10.3892/mmr.2021.12447" correction OR retraction`; `"10.1371/journal.pgen.1004524" correction retraction`; `"HIVEP1" "adn1150" correction retraction` |

Backward tracing: Hu references to Wu 2016 and Puleston 2021 were inspected.
Forward discovery: the Hu DOI search returned the 2026 ALDH5A1 primary paper;
its abstract was screened. This is targeted citation tracing, not a complete
citing-paper audit. The earlier Wagner/Choi forward-title scan is retained as
historical coverage and was not repeated.

Corrections/version checks found the PLOS 2023 correction. The queried Hu,
Peng and HIVEP1 records/searches returned no linked correction/retraction in
this pass; Hu/HIVEP1/ALDH5A1 Europe PMC core records had no correction list.
Absence from those records is not a guarantee. HIVEP1 and ALDH5A1 exact data
reuse remain unknown. The 2026 polyamine-guided **alveolar bone** repair lead
(PMID 42610507) was screened as a different tissue, not lung evidence.

Open-source caches are ignored local files under
`raw_data/wagner_literature_20261004`: Hu and developmental-JMJD3 XML, the PLOS
correction XML, Hu `mmc1.pdf`, and the three Europe PMC core metadata responses.
PMC browser challenges were bypassed using the legitimate open-access API;
Wu XML returned HTTP 500 but its PMC HTML supplied the study-design text.
Restricted publisher full texts were not accessed through alternative credentials.

**Stopping rule:** the closest inspected premise and its leading rival are
mapped for all six existing candidates. Newly found inaccessible sources remain
explicitly abstract-level leads. Their full methods/data identities must be
resolved before claiming a specific overlapping enzyme mechanism as a new RQ.
P05/P06 still need exact biological tuples; further untargeted searching cannot
substitute for that specification. This review does not certify exhaustive
coverage, novelty, independent replication or laboratory feasibility.
