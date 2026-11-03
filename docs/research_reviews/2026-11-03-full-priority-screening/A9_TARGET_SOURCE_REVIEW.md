# A9: bounded receptor-context annotation review

3 November 2026, Asia/Seoul. This fixes the roles of six proposed sentinel
transcripts before new expression extraction. It does not introduce a ligand
ranking, receptor-activity score or functional inference from co-detection.

## Primary support and access limits

| Source | Actual read scope and role |
|---|---|
| [Macdonald-Obermann and Pike, 2014](https://doi.org/10.1074/jbc.M114.586826), *Different epidermal growth factor receptor ligands show distinct kinetics and biased or partial agonism for homodimer and heterodimer formation* | Indexed primary introduction/results and PubMed metadata/compact abstract. The study measures ligand-induced EGFR homodimers and EGFR/ERBB2 heterodimers, including amphiregulin context. It supports separating receptor partners and ligand-specific responses. Full-page/figure audit was not recovered, so no quantitative binding or kinetic claim is imported. |
| [Park et al., 2015](https://doi.org/10.1038/nsmb.3074), *Structure and mechanism of activity-based inhibition of the EGF receptor by Mig6* | Indexed primary text and compact PubMed abstract identify MIG6/ERRFI1 as a feedback inhibitor acting on activated receptors. This supplies a protein-function annotation, not a calibration from ERRFI1 transcript abundance to inhibition. Full figure/method audit was unavailable. |
| [Laederich et al., 2004](https://pubmed.ncbi.nlm.nih.gov/15345710/), *The leucine-rich repeat protein LRIG1 is a negative regulator of ErbB family receptor tyrosine kinases*; [DOI](https://doi.org/10.1074/jbc.M409703200) | Complete PubMed abstract inspected. Reported cell-system experiments associate LRIG1 with all four ErbB receptors and examine receptor level/turnover and growth responses. These findings support the selected regulator/family labels; they do not establish an AREG-dependent mechanism in adult lung fibroblasts. Full article retrieval returned 403. |

The evidence is adequate for these narrow role labels. It is not a completed
mechanistic review or independent validation of the proposed lung comparison.
No molecular-interface design, quantitative affinity or intervention prescription
is inferred from the structural precedent.

## Fixed six-target map

| Symbol | Label in the new RNA screen | Boundary |
|---|---|---|
| EGFR | AREG-receptor transcript context | RNA does not measure surface receptor, ligand exposure or engagement |
| ERBB2 | Potential ErbB partner context | Co-detection does not identify an EGFR/ERBB2 complex |
| ERBB3 | Additional ErbB-family context | No direct AREG-receptor assignment in this screen |
| ERBB4 | Additional ErbB-family context | No direct AREG-receptor assignment in this screen |
| ERRFI1 | Feedback-inhibitor-associated transcript | Higher RNA does not establish effective inhibition |
| LRIG1 | Receptor-regulator-associated transcript | Higher RNA does not establish receptor turnover or inhibited response |

EGFR/ERBB2 context uses the first source; broader family/regulator context uses
the LRIG1 source; ERRFI1 uses the MIG6 source. The panel is selected, not an
exhaustive receptor or feedback inventory. No positive/negative weights or new
index are assigned. Alternative ligands and recipient state remain explanations
for these transcripts; receptor co-detection alone cannot identify the input.

The original EGFR_ERBB2 resource result remains 7/22 with its unchanged
11-donor floor. New component descriptions must not replace that failed
coverage result or turn lack of partner RNA into a homodimer conclusion.
The technical specification still must establish original cohort parity,
deposited subtype IDs, matrix semantics/full-feature denominator and exact
feature mappings before freeze.

## Search and capability record

Web queries on 3 November, no date/domain filters unless included literally:

- `amphiregulin binds EGFR not ErbB3 ErbB4 primary ligand specificity ErbB2`
- `MIG6 ERRFI1 EGFR ERBB2 inhibition LRIG1 ErbB receptors 2004 2007 primary study`
- `LRIG1 EGFR feedback fibroblast amphiregulin 2024 2025 2026`
- `LRIG1 restricts growth factor signaling enhanced receptor ubiquitylation 2004 PMC`
- `"Different Epidermal Growth Factor" "Ligands" "doi" 2014 Macdonald-Obermann Pike`
- `"Structure and mechanism of activity-based inhibition" "doi"`
- `site:pmc.ncbi.nlm.nih.gov/articles/PMC4176247/ "FIGURE" "amphiregulin"`
- `site:pmc.ncbi.nlm.nih.gov/articles/PMC4176247/ "AREG" "ErbB4"`

The last two queries returned mostly irrelevant results and supplied no added
authority. Recent-window querying did not identify a directly applicable new
fibroblast comparison in the inspected results; absence of a hit is not novelty.
Reviews were discovery aids only. PMC pages returned browser challenges,
Europe PMC was inaccessible through the web tool, the Nature route failed and
the Harvard manuscript fetch timed out. No access failure was interpreted as
absence of the biology.

The installed NCBI Entrez skill successfully retrieved the two exact PubMed
records after an initial sandbox DNS failure and a reviewed read-only network
retry. Its compact output truncates abstracts, so the record is explicitly a
compact-abstract/metadata read, not full-text recovery. No plugin installation,
credential change or raw scientific workflow was needed. No systematic citation
census or correction-database audit was performed for this role-label review.
