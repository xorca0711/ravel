# Literature search for the three Wp candidates

Searched **5 October 2026**. Service: NCBI E-utilities against PubMed
(`esearch`, `esummary`, `efetch`), with a contact address supplied. Full text
fetched through Unpaywall where open access permitted.

This records what was actually searched and read. It certifies no novelty: no
finite search proves the literature exhausted, and an absent hit is not
evidence of a first.

## Queries executed

All thirteen returned without error. `n` is the PubMed hit count; the top
records by relevance were retrieved for each (40 maximum), giving 294 unique
records screened on title, journal and year.

| Key | Query | n |
|---|---|---|
| Q1a | `Th17 AND (pathogenic OR pathogenicity) AND (Foxp3 AND IL-17) AND (co-expression OR coexpression OR plasticity)` | 14 |
| Q1b | `"regulatory T" AND Th17 AND (interconversion OR transdifferentiation OR "ex-Foxp3")` | 29 |
| Q1c | `Th17 AND (signature OR module OR score) AND (pro-inflammatory AND regulatory) AND single-cell` | 3 |
| Q2a | `(glycolysis OR "2-deoxyglucose" OR glycolytic) AND Th17 AND (effector OR IL-17) AND (inhibition OR restriction OR blockade)` | 39 |
| Q2b | `(ATF4 OR "integrated stress response" OR eIF2alpha OR GCN2) AND ("T helper" OR Th17 OR "CD4 T") AND differentiation` | 16 |
| Q2c | `(proliferation OR "cell cycle" OR "division rate") AND (cytokine AND ("per cell" OR output)) AND ("T cell" OR Th17)` | 52 |
| Q2d | `PGAM1 AND ("T cell" OR Th17 OR immune)` | 37 |
| Q3a | `(cerebrospinal OR CSF) AND "multiple sclerosis" AND ("T cell" OR CD4) AND (single-cell OR scRNA) AND (blood OR paired)` | 40 |
| Q3b | `(CSF OR cerebrospinal) AND "T cell" AND (activation OR "tissue-resident" OR residency) AND (compartment OR compartmentalization)` | 38 |
| Q3c | `"multiple sclerosis" AND Th17 AND (cerebrospinal OR CSF) AND (pathogenic OR GM-CSF OR IL-17)` | 149 |
| F1 | `Gaublomme[au] AND Th17 AND single-cell` | 3 |
| F2 | `Schafflick[au] AND (cerebrospinal OR CSF) AND "multiple sclerosis"` | 3 |
| F3 | `Th17 AND (TGF-beta) AND (IL-1beta OR IL-23) AND pathogenic AND (nonpathogenic OR "non-pathogenic")` | 5 |

All fields restricted to title/abstract. Searches were **not** restricted to
the target authors or to the downloaded corpus, and three unrestricted
foundational searches (F1 to F3) ran alongside the recent-window ones. The
2026 records returned show the index was current at the search date.

**Coverage limits.** PubMed only; Europe PMC, Scopus, Web of Science and
Google Scholar were not queried. Citation directions were not traversed
systematically: forward and backward citation chasing was done only for the
one source read in full. Preprints appear in the results (bioRxiv, medRxiv,
Res Sq) and at least one pair is a preprint and its later article, which were
not de-duplicated because neither entered the evidence.

## The finding that changed a question

**Ishikawa and colleagues, 2023.** "Phosphoenolpyruvate regulates the Th17
transcriptional program and inhibits autoimmunity." *Cell Reports* 42:112205,
[doi:10.1016/j.celrep.2023.112205](https://doi.org/10.1016/j.celrep.2023.112205),
PMID 36857180. **Full text retrieved and read** (open access, gold).

What it measured: PEP supplementation, or inhibition of glycolytic enzymes
downstream of PEP, raises intracellular PEP and suppresses IL-17A in
differentiating Th17 cells; PEP binds JunB and blocks DNA binding of the
JunB/BATF/IRF4 complex; the effect occurs without significant change to
glycolysis, proliferation or survival; daily PEP administration reduces Th17
generation and ameliorates EAE in mice.

Why it matters here. PGAM converts 3PG to 2PG, the immediate precursor of PEP.
PGAM inhibition should lower PEP, release JunB/BATF/IRF4 and raise IL-17 — the
exact phenotype the source reports, through a route requiring neither stress
nor serine. It also predicts the [Wp-E3](../E3_RESULTS.md) effector-programme
rise, which no other candidate mechanism does.

Three things make this a question rather than an answer:

1. **The source's own ¹³C tracing argues against it.** Figure 1E reports that
   EGCG collapses labelled 2PG from 51% to 7% while 3PG and PEP are *not*
   significantly changed, with no other glycolytic metabolite moving. Read at
   face value this eliminates the PEP route.
2. **But a 15-minute label ratio is not a pool size.** A labelling ratio can
   hold steady while the absolute pool falls, and the measurement is from one
   condition.
3. **The source cites this paper, but only as background.** It is reference 7
   of the source, appearing in the Introduction's opening citation bundle
   ("Glycolysis is central to Th17 cell differentiation and function.¹⁻⁷") and
   nowhere else in the text. The Discussion proposes stress and serine, closes
   by saying the mechanism needs further study, and does not return to the PEP
   mechanism — even though the pathway segment its own Compass analysis singles
   out, 3PG to PEP, is exactly what that reference concerns. The gap is
   engagement, not awareness.

Contribution: **this is a premise, not our finding.** Wp-Q2 was reframed from
a two-way demand-versus-stress question to a three-way one, with the prior
framing preserved on the card.

## Other sources inspected, and what each changes

Abstract-level unless marked. An abstract check is not a figure and methods
audit, and none of these was read in full.

| Source | What it measured | Contribution here |
|---|---|---|
| [Gaublomme et al. 2015](https://doi.org/10.1016/j.cell.2015.11.009), *Cell* 163:1400 (PMID 26607794) | Single-cell Th17 heterogeneity; the pro-inflammatory and pro-regulatory modules the source scores | **Premise.** These are the gene lists in every Wp score. Wp-Q1 is about how their two arms move, not about their derivation. |
| [Brucklacher-Waldert et al. 2017](https://doi.org/10.1016/j.celrep.2017.05.052), *Cell Rep* 19:2357 (PMID 28614720) — **full text read, prior pass** | Cellular stress supports Th17 differentiation **in the absence of** TGF-β; 2-DG and 3-bromopyruvate enhance polarisation; mechanism is sustained cytoplasmic calcium with partial XBP1 | **Contradiction of the source's premise.** Stress substitutes for TGF-β rather than activating it. Supplies Wp-Q2's calcium rival, which a transcript module cannot see. |
| [Huang et al. 2019](https://doi.org/10.1016/j.cmet.2019.09.014), *Cell Metab* 30:1107 (PMID 31607564) | Allosteric PGAM1 inhibitor HKB99 via PGAM1-ACTA2, JNK/c-Jun, AKT, ERK in lung cancer | **Unresolved.** Paywalled; abstract does not mention TGF-β. Remains a flag, not a refutation; needs the PDF. |
| [Toriyama et al. 2020](https://doi.org/10.1038/s42003-020-01122-w), *Commun Biol* 3:394 (PMID 32709928) | T-cell-specific *Pgam1* deletion attenuates CD4 and CD8 responses; glycolysis augments mTORC1 and TCR signals, with glutamine as a hub | **Boundary constraint on Wp-Q2.** Complete ablation attenuates responses while partial inhibition promotes pathogenicity, so dose matters and genetic reduction must be titrated rather than knocked out. |
| [Ishikawa and colleagues 2023](https://doi.org/10.1016/j.celrep.2023.112205) — **full text read** | PEP inhibits the Th17 programme via JunB/BATF/IRF4 | **Reframes Wp-Q2**, as above. |
| [iScience 2025, 114051](https://doi.org/10.1016/j.isci.2025.114051) (PMID 41399496) | 2-DG inhibition of glycolysis **impairs** IL-17A production in lung Th17 TRM cells in vivo and in lung slices | **Contrary finding, and important.** Glycolysis inhibition reduces IL-17 here, the opposite direction to both the source and Brucklacher-Waldert. Memory versus differentiating cells and a different inhibition point are the obvious differences; the honest reading is that the direction is context-dependent and the source's phenotype is not a general rule. |
| [Immunity 2025](https://doi.org/10.1016/j.immuni.2025.09.007) (PMID 41043415) | Notch3⁺ Treg cells increased in MS; Notch3-DLL1 subverts Tregs into Th17 cells; deletion stabilises Tregs | **Rival for Wp-Q1's human leg.** A documented route by which regulatory character is lost and effector character gained in CNS autoimmunity, which a two-arm score would read as a single pathogenicity rise. |
| [Front Immunol 2026, 1767639](https://doi.org/10.3389/fimmu.2026.1767639) (PMID 42131332) | Helminth exposure shifts Th17-lineage cells toward Tr1/Treg-like rather than Th1-like function, using an IL-17 fate reporter | **Supports Wp-Q1's premise and names its missing tool.** Th17 lineage cells move between regulatory and inflammatory function; a fate reporter is how that is shown, and Wp-Q1's protein design is the cheaper version of the same logic. |
| [Schafflick et al. 2020](https://doi.org/10.1038/s41467-019-14118-w), *Nat Commun* 11:247 (PMID 31937773) | The deposit Wp-R4 and Wp-M3 reuse: CSF leukocyte composition and transcriptome in MS, with compartment-specific findings and cytotoxic T helper enrichment in CSF | **Same evidence lineage, not independent support.** Establishes that MS immune mechanisms are compartmentalised, which is Wp-Q3's premise; its own analysis is of the data Wp-Q3 would reanalyse. |
| [EBioMedicine 2026, 106324](https://doi.org/10.1016/j.ebiom.2026.106324) (PMID 42250325) | A CCR5-high Th17.1 cluster enriched in CSF versus paired blood, pre-cytotoxic, reduced after natalizumab | **Direct rival for Wp-Q3.** A specific CSF-enriched Th17-lineage subset would raise an effector module in CSF through composition rather than through a compartment-imposed state — exactly Wp-Q3's composition rival, now with a named population. |
| [Cell Mol Immunol 2025](https://doi.org/10.1038/s41423-025-01356-w) (PMID 41087718) | IL-18 drives Bhlhe40-dependent glycolysis and GM-CSF in pathogenic Th17 | **Context.** Pathogenic Th17 with *increased* glycolytic flux, the conventional direction, against which the source's PGAM result is the exception. |

## Trace, per candidate

**Wp-Q1.** Published: the two modules are an established construction
(Gaublomme 2015) and Th17-lineage plasticity in both directions is established
(Front Immunol 2026; Immunity 2025). Repository: the score's two arms move
one-sidedly, in *opposite* arms, under a nutrient perturbation in mouse culture
and a compartment contrast in human disease, and the arms are anti-correlated
across 15,830 cells. Unresolved contrast: whether that reflects separately
regulated competences or one latent axis, which same-transcriptome RNA cannot
settle. Hypothesis and rival are on [the card](Q1_arm_asymmetry.md).
Contribution: **model discrimination**.

**Wp-Q2.** Published: three candidate mechanisms exist for the source's
phenotype — stress substituting for TGF-β (2017), PEP release from JunB
inhibition (2023), and demand competition (general) — and a fourth result
points the opposite way entirely in memory cells (iScience 2025). Repository:
the effector programme rises in the one arm, biosynthetic and proliferative
programmes fall, ATF4 output falls, and no other stress axis moves. Unresolved
contrast: which mechanism produces the phenotype; the source's Discussion names
one, its own libraries move against it, and the mechanism attached to its own
pathway segment is cited only as Introduction background (reference 7) and
never evaluated against its result. Contribution: **model discrimination among
published mechanisms**.

**Wp-Q3.** Published: CSF compartmentalisation in MS is established
(Schafflick 2020), and a specific CSF-enriched Th17-lineage subset is now
described (EBioMedicine 2026). Repository: the source's disease contrast does
not reproduce, matched random gene sets separate the blood cohorts as well as
the modules do, and the surviving contrast is a paired within-donor tissue
difference that moves the pro-inflammatory arm only. Unresolved contrast:
whether that is a compartment-imposed state, local activation, or the
composition shift the 2026 paper would predict. Contribution: **measurement
validation and boundary extension**.

## Next literature check

Planned, not executed: `phosphoenolpyruvate pool size T cell metabolomics PGAM
inhibition` and `JunB BATF IRF4 metabolite regulation Th17 2026`, plus forward
citations of Ishikawa 2023 and of the source itself. Refresh when the Wp-Q2
design is prepared as an experiment package, or if the Huang 2019 full text
becomes available.
