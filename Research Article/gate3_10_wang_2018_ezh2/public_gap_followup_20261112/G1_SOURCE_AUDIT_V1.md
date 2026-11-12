# G1 public-source qualification for Wang and A33–A35

12 November 2026, Asia/Seoul. The unit of this audit is the public record,
reported experiment or deposited sample. No expression, response or
genotype effect was estimated. The question is which source can narrow
model choice, response measurement or the need for linked preparations.
Wang and the Dp1/Peeters candidate directions were already known.
[Neighboring-paper review](../RQ_FOLLOWUP_REVIEW_20261112.md) ·
[Frozen Wang results](../RESULTS_V1.md) · [F3 measurement plan](../F3_MEASUREMENT_PLAN_V1.md).

## Perturbation timing and target engagement

| Source and comparison | What was actually measured | Decision for model qualification |
|---|---|---|
| **Wang 2018**, Figure 1B,D and Figure S4A–D; main article and original publisher supplement p. 6 inspected. | Systemic CPI-1205 in MC38 hosts lowers the H3K27me3 staining signal in gated tumor Tregs (Fig. 1D). The Foxp3-CreERT2 lineage-reporter experiment compares H3K27me3 MFI in recombined and unrecombined lymph-node Tregs after induction (S4A), and follows reporter-positive frequencies on and after withdrawal (S4B–C). S4D shows H3K27me3 and total H3 staining in already sort-purified Tregs with ex-vivo inducible deletion, at day five of stimulation. | **S4D is the closest public precedent for verifying recent Ezh2 loss in already established, cultured Tregs.** It provides a model and mark readout, not a recovered per-preparation dataset or candidate response assay. S4A reporter recombination and the chromatin mark address distinct aspects of engagement. The systemic drug comparison also includes other exposed cells. [Wang](https://doi.org/10.1016/j.celrep.2018.05.050) · [Supplement](https://ars.els-cdn.com/content/image/1-s2.0-S2211124718307964-mmc1.pdf). |
| **Wang and DuPage longstanding loss.** Wang GSE114298 count columns `D4_Ez_1–4` and `D4_WT_1–5`; DuPage GSE58998 sorted FOXP3-positive cells from healthy mosaic mice, Figure 6. | Wang measures cultured day-four relative RNA, after constitutive Foxp3-driven deletion. DuPage compares CD62L-high/low recovered FOXP3-positive RNA in KO and heterozygous context. The DuPage overlap with H3K27me3 tracks is not matched KO chromatin. | The existing analyses support direction and state-context checks. They cannot supply an acute-loss estimate, and the unresolved Wang mouse/pool and control crosswalk remains material. [Wang audit](../F1_SOURCE_AUDIT_20261112.md) · [Dp1 source review](../../gate3_09_dupage_2015/SOURCE_REVIEW.md). |
| **Peeters 2024**, Figure 4A–F and S4, versus Figures 6–7 and the deposited assays. Version-of-record text and GEO SOFT inspected. | Inducible Y641F gain in differentiated Tregs measured higher H3K27me3 relative to total H3 after two weeks, with no detected change in total lymph-node Treg frequency or number. Figure 4D measures surface TIGIT-positive fraction. Figure 4F measures CXCR3, CCR8 and CCR6, without a CCR2 endpoint. GSE262130 GSM8158034–45 are the constitutive Foxp3-hCre gain/WT fresh and day-four libraries. GSE262129 uses corresponding genotype/state labels for CUT&RUN, with antibody and cell type as additional fields. | Acute gain supplies a target-engagement and phenotype precedent. The deposited RNA/CUT&RUN does not describe that inducible cohort, and the observed phenotype supplies no TIGIT-evoked AREG or CCR2 movement. Reuse the existing gain comparison without a new count run or a preparation-level cross-assay join. [Peeters](https://doi.org/10.1016/j.celrep.2024.114724) · [GSE262129](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262129) · [GSE262130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262130) · [Dp1 results](../../gate3_09_dupage_2015/CANDIDATE_ANALYSIS_RESULT_V1.md). |
| **Goswami 2018**, Figure 2 and main Results describing Supplemental Figures 2–4; journal PDF and both GEO family SOFT records inspected. | GSE114717 GSM3148411–18 are mouse iTregs differentiated with or without CPI-1205, four deposited libraries per label. The A–D suffixes do not establish matched preparations. The paper separately reports suppression using human iTregs differentiated with inhibitor or vehicle. GSE114716 GSM3148403–10 are baseline/post-ipilimumab peripheral CD4 RNA with four patient labels. | Pharmacological intervention **during induction** differs from inhibition of already-established Tregs. The mouse RNA and human functional assays cannot be joined. The patient pairing supports a different exposure and endpoint. No linked candidate-specific target-engagement and response result was qualified in these records. [Goswami](https://www.jci.org/articles/view/99760) · [GSE114717](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE114717) · [GSE114716](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE114716). |

An acute catalytic claim needs measured engagement in the actual Treg
preparation at the assay window. A validated H3K27me3 measurement with an
appropriate total-H3 reference is a precedent; gene-level Ezh2 RNA or
reporter positivity alone cannot supply that measurement. A verified
longstanding genotype can still support its own bounded response comparison.
No public linked day-four total recovery, observed-state RNA and candidate
functional measurements were located in the records audited here.

## Silveria 2026 · a FOXP3-state alternative

The journal version (`vkag145`, publisher online date 7 July 2026) and
linked September 2025 preprint v1 are one publication lineage. The journal
abstract reports p53 activation with reduced H3K27me3, FOXP3 protection
under MDM2 inhibition in IL-6/IL-1β conditions, and greater FOXP3 loss with
Treg p53 deficiency. These are distinct perturbations. Stabilizing p53 is
an intervention on p53 turnover, and p53 loss tests p53's contribution to
FOXP3 maintenance in that inflammatory context. Neither supplies an
acute-Ezh2-loss response estimate in Wang's day-four culture.
[Journal version](https://doi.org/10.1093/jimmun/vkag145) ·
[PubMed version link](https://pubmed.ncbi.nlm.nih.gov/42413200/) ·
[Preprint](https://pubmed.ncbi.nlm.nih.gov/40950180/).

The indexed author dissertation, chapter 2, gives relevant experimental
details. Figure 2.2D–E reports day-four target qPCR and p53 immunoblot after
longstanding Ezh2 deletion, including a p53-loss comparison for the qPCR.
The Results distinguish higher p53 protein from unchanged Trp53 RNA
and retain RNA findings that did not reach significance. Figure 2.2K
uses locus-level H3K27me3 ChIP-qPCR in the genetic-loss comparison.
Figures 2.3A–F separate current FOXP3, p53 protein, viability, expansion
and division measurements. The report describes greater FOXP3 maintenance
under p53 stabilization in the inflammatory condition, with no detected
viability difference, modestly lower expansion and no detected difference
in the separately measured division endpoint after withdrawal. That
separation strengthens the rationale for ancestry, state and recovery
readouts. It gives no reason to add a p53 arm to G1 or assume a p53
mechanism in Wang. The thesis RNA description cites Wang (reference 237),
so treat its Ezh2 RNA as potentially shared until the underlying library
manifest resolves reuse. The measured qPCR, immunoblot and chromatin
endpoints are panel-level precedents with no recovered preparation join.
[Author dissertation, Chapter 2 and reference 237](https://escholarship.org/content/qt8pk5j709/qt8pk5j709_noSplash_74f9193cfcdb232b8a216ead8c496abf.pdf).

Access was limited to the final abstract, preprint abstract and selected
thesis text/legends. PubMed lists the journal PMC release for 7 July 2027.
Europe PMC XML for the preprint returned 500; NCBI PMC EFetch exposed
front matter without a body. The PubMed-to-GEO link query returned no
linked record for either PMID. An accession and sample manifest for an
independent linked dataset were not verified in these routes.
[PubMed-to-GEO query](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=gds&id=42413200,40950180&retmode=json).

## Bonfiglio 2025 · a broad CD4 movement precedent

The version-of-record article, published online 7 February 2025, and its
GEO deposits qualify longstanding Cd4-Cre Ezh2 loss in an atherosclerosis
setting. The paper also uses a separate CD8-directed deletion arm.
Figure 2G measures lesional FOXP3-positive cells, Figure 3C–D measures
splenic CD3-positive single-cell composition, and Figure 4B–H measures
plasma or bulk CD4-culture cytokines and a macrophage response to bulk
CD4 supernatant. The Discussion reports that IL-10 and TGF-β were not
diminished in this broad setting (S6E as cited in the main text). These
endpoints preserve both the abundance and non-Treg cytokine alternatives
without tracing a Treg-specific response. [Article and figure legends](https://pmc.ncbi.nlm.nih.gov/articles/PMC12063685/).

- **GSE283002 / Fig. 3C–D.** The paper reports four mice per group.
  GEO exposes two genotype-level GSMs, GSM8654519 KO and GSM8654520 WT.
  The supplementary file list has one filtered 10x H5 matrix per GSM.
  The inspected metadata and inventory do not map barcodes to mice;
  the H5 payloads were not audited. A matrix or a cell does not provide an
  additional independent mouse. [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE283002) ·
  [File inventory](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE283nnn/GSE283002/suppl/filelist.txt).
- **GSE283191 / Fig. 5A.** One GSM8657479 contains multiplexed Prime-seq.
  The released README identifies four included WT and three included KO
  sample barcodes and two genotype-issue exclusions. The paper describes
  four versus three mouse samples for the comparison. The barcode manifest
  is a genuine key for the bulk splenic CD4 comparison, with no mouse-to-flow,
  supernatant or movement link in that README. This is a different selection
  and endpoint from A33–A35. [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE283191) ·
  [Barcode README](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE283nnn/GSE283191/suppl/GSE283191_README.TXT).
- **Figure 8C–D.** Ezh2 loss accompanies lower actin polymerization and
  impaired movement in the bulk CD4 context. Figure 8D reports four versus
  four and measures transwell migration with CCL19 or CCL22 versus the
  corresponding no-chemokine count. Figure 8C's displayed sample counts
  refer to cells. Localization and actin are not a direct catalytic
  engagement readout. These results justify checking general movement
  competence alongside a CCR2-ligand-specific response. Neither the cell
  gate nor the ligands identify a CCR2-dependent Treg response.
  Individual movement values and an RNA/flow/response crosswalk were not
  recovered in the assessed routes. [Figure 8 and Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC12063685/#F8).

The human plaque analyses reuse GSE159677 and GSE253904. They supply
human expression context without an Ezh2 perturbation or a join to the
mouse functional measurements. The two new mouse accessions are both
Bonfiglio evidence. Overlap among sequencing and functional cohorts
remains unresolved. An additional bulk CD4 expression analysis would
answer a different question from the current Treg measurement decisions.

## Candidate dispositions

| Question | Closest qualified public evidence | What the next fit-for-purpose comparison needs |
|---|---|---|
| **A33 · TIGIT-evoked AREG** | Panetti 2025 Fig. 5b–e and 6h–i give activation-context and TIGIT agonist/isotype comparisons. The 6h outcome is cellular AREG induction normalized to unstimulated. The in-vitro stimulation/flow methods use transport and shedding inhibitors, so this is a cellular staining endpoint. AREG induction and Blimp-1 staining motivate the control and activation window. Peeters acute gain measures a TIGIT-positive fraction only. Wang's basal RNA directions for Tigit, Prdm1 and Areg disagree. [Panetti primary text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12571903/) · [A33 plan](../../../RQ_Specified/A33_ezh2_tigit_areg_output/PLAN.md). | Retain a defined activation context and a within-preparation TIGIT engagement-minus-matched-control contrast in extracellular AREG accumulation, then compare that response across verified Ezh2 groups. Include basal output, matched window and viable recovery. The paired conventional T-cell suppression endpoint is optional and separate. An otherwise qualified response estimate can stand alone. For RNA/protein discordance, the RNA and measured protein must share preparation, condition and window. |
| **A34 · CCR2 and movement versus fitness** | Loyher 2016 Fig. 1E–G compares CCR2-deficient and control Treg accumulation in paired hosts. The author manuscript reports an anti-CCR2 stain that did not detect CCR2 on Tregs while fluorescent CCL2 binding did, with Ccr2-loss and competition controls (Fig. 2 and S3). This supports validating a surface assay with a specificity control. Watanabe Fig. 5 compares CNS contexts and a CCL12 response trend. Bonfiglio Fig. 8D shows a broader genotype/movement result with other ligands. Wang's Ccr2 direction crosses zero under omission. [Loyher author manuscript](https://krummel.org/images/Publications/loyher-pub-2016-01.pdf) · [Watanabe](https://doi.org/10.1186/s12974-024-03144-1) · [A34 plan](../../../RQ_Specified/A34_ezh2_ccr2_movement_fitness/PLAN.md). | First qualify CCR2 surface abundance or specific ligand binding in actual Tregs. A within-preparation ligand-gradient-minus-control movement endpoint needs viable input/recovery and a comparison that distinguishes directed movement from generic movement. Report recovery and IL-2 response separately. Bonfiglio's result supports considering general movement competence as an explanation. Existing Zhan and Chorro evidence keeps CD25/IL-2 context and genetic background as separate alternatives. |
| **A35 · intact IGFBP4 and native-IGF response** | Karino Fig. 3G–I and the prior repository reading distinguish polarized-cell expression, cleavage of recombinant IGFBP4 by ADAM9 or Th17-derived material, and a mature-Th17 perturbation null reported in the Results. Bilbao 2014 Fig. 1 measures FOXP3/Ki67 and cell numbers in sorted human Tregs after unmodified recombinant IGF-1, with a small reported experiment. Fig. 6E verifies IGF1R deletion by immunoblot in its separate mouse comparison. DiToro's desIGF1 rationale and Shapiro's IGF1/IL-2 comparison bound ligand and cytokine context. [Karino](https://doi.org/10.1002/art.43313) · [Bilbao](https://pmc.ncbi.nlm.nih.gov/articles/PMC4237469/) · [DiToro](https://doi.org/10.1016/j.immuni.2020.03.013) · [Shapiro](https://doi.org/10.4049/jimmunol.2200651) · [A35 plan](../../../RQ_Specified/A35_treg_igfbp4_source_igf_response/PLAN.md). | First identify intact extracellular IGFBP4 from lineage-identified Tregs and distinguish fragments, medium background and recovery. Published recombinant IGF-1 responses establish recipient competence in their tested contexts. They do not show endogenous IGFBP4 contribution. A linked native-IGF response and a specified IGFBP4 comparison follow only if the intact-source measurement qualifies. |

**Panetti sample linkage.** E-MTAB-8861 SDRF exposes `Source Name`,
organ/phenotype labels and ENA sample, experiment and run keys (for example
`Sample 1` → ERS4377299 / ERX3981637 / ERR3978923). These identify
sequencing inputs, without a link in the SDRF to Fig. 6h's flow assay.
Zenodo 14041419 republishes processed/raw derivatives from that sequencing
lineage. GSE79339 and GSE121838 are previously reported Blimp-1 data cited
by Panetti. These objects cannot be counted as extra biological replicates
of the flow response. [BioStudies record](https://www.ebi.ac.uk/biostudies/ArrayExpress/studies/E-MTAB-8861) ·
[SDRF](https://www.ebi.ac.uk/biostudies/files/E-MTAB-8861/E-MTAB-8861.sdrf.txt) ·
[Zenodo](https://doi.org/10.5281/zenodo.14041419).

The Panetti article XML lists the Fig. 5, Fig. 6 and Extended Data Fig. 8
statistical source workbooks as MOESM7, MOESM8 and MOESM15. These are
identified public-source leads. The publisher landing page redirected,
the static CDN did not resolve, and direct PMC and publisher-media
attachment attempts returned HTML instead of XLSX. The Europe PMC
supplement bundle did not deliver an inspectable workbook within the
checkpoint. Therefore the Fig. 6h pairing and unit keys remain unverified.
Even a confirmed Fig. 6h pairing would support a standalone TIGIT cellular
induction estimate in Panetti's setting, with no Ezh2 comparison, extracellular
AREG or demonstrated linkage to sequencing. [Publisher source-data listing](https://www.nature.com/articles/s41590-025-02300-w) ·
[Fig. 6 workbook route](https://pmc.ncbi.nlm.nih.gov/articles/instance/12571903/bin/41590_2025_2300_MOESM8_ESM.xlsx).

The closest sources provide assay and comparison precedents. None of the
inspected public datasets supplies the joint Ezh2-by-response contrast for
these three questions. There is no new candidate analysis ready for an
execution contract from G1. The next checkpoint can choose one qualified
measurement and request only its missing preparation-level records. Any
standalone response requires its own documented units and comparator.
Inferring RNA-to-protein discordance additionally requires matched
aliquots, timing, conditions and recovery. The present bulk RNA evidence
cannot be substituted for either endpoint.

## Search and access record

Web searches were run on 12 November 2026 without a restrictive date
filter. Principal exact queries that informed the checkpoint follow.

- `39917842 Bonfiglio Ezh2 Shapes T Cell Plasticity to Drive Atherosclerosis GEO GSE data availability Treg EZH2 inhibitor`
- `EZH2 acute primary mature regulatory T cell deletion inhibition Treg H3K27me3 RNA seq GEO mature Tregs inducible ex vivo EZH2 Goswami Peeters`
- `Goswami 2018 GSE114716 GSE114717 CPI-1205 RNA Treg primary mature Treg EZH2 JCI99760 supplemental`
- `TIGIT ligation amphiregulin Treg AREG TIGIT primary Treg Joller dataset anti TIGIT supernatant`
- `"Panetti" TIGIT amphiregulin "Data availability" "GEO" s41590 02300`
- `Panetti 41094201 MOESM8_ESM xlsx source data Fig 6h`
- `Treg CCR2 CCL2 migration Transwell Ccr2 knockout regulatory T cells protein mouse Foxp3 Watanabe CCL12 source data`
- `Bonfiglio 39917842 supplement source data CCL19 CCL22 transwell migration Figure 8 article supplemental material`
- `IGF1 regulatory T cells native IGF-1 IGFBP4 IGF1R Bilbao 2014 Treg Igfbp4 protein ELISA secretion Karino`
- `Bilbao 2014 25339185 recombinant IGF 1 purified human regulatory T cells proliferation figure 1 Foxp3`
- `42413200 Epigenetic control of p53 activity in regulatory T cells maintains their identity Ezh2 data GEO 2026 Silveria figure H3K27me3 Foxp3`
- `"vkag145" "data availability" GEO RNA-seq Silveria`
- `"2025.08.29.673118" "Data availability" RNA sequencing Ezh2 GSE Silveria`

Saved source responses are under ignored `raw_data/wang_20261112/g1/`.
The [Bonfiglio](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12063685/fullTextXML),
[Peeters](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12052300/fullTextXML),
[Panetti](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12571903/fullTextXML)
and [Bilbao](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4237469/fullTextXML)
article XML responses were read for named panels and methods. The
[Goswami publisher PDF](https://www.jci.org/articles/view/99760/files/pdf)
was used after its XML route returned 500. Loyher was inspected via the
public author manuscript. The Watanabe and Karino endpoint details and
DiToro ligand rationale reuse the documented prior primary reading
because the direct Watanabe DOI and Karino/DiToro XML routes did not
deliver usable files in this checkpoint. GEO metadata came from each
linked series' family SOFT. No raw sequencing, figure digitization, new
numerical execution or inference was needed. Access failures bound what
was inspected. The separately coordinated tumor literature review is
outside this audit.
