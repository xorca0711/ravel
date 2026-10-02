# Nb4 proposal source and exposure ledger

**Planning audit, 3 October 2026.** This ledger separates previously used data
from candidate inputs. It does not add numerical dataset usage. See
[existing Nb4 provenance](../../DATASETS.md) and the
[repository inventory](../../../../docs/DATASETS.md) for executed work.

| ID | Source and current evidence | Proposed role | Qualification needed before fitting |
|---|---|---|---|
| S01 | [Travaglini/Nabhan 2020](https://doi.org/10.1038/s41586-020-2922-4); Nb4 used pinned human CELLxGENE releases, source supplements and author code | Discovery and selected source reconstruction across P01–P09 | Verify each newly extracted compartment, full-gene layer, sample nesting and label exclusions; prior Nb4 effects are exposed |
| S02 | Original mouse atlas, [PRJNA632939](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA632939); source metadata inspected in Nb4 | P01 mouse reference; P02/P06 comparative context | Individual versus pooled animals, age/anatomy, assay and gene maps remain unresolved for the new matched comparison; published differential-gene tables are not a complete ortholog universe |
| S03 | [Madissoon 2023](https://doi.org/10.1038/s41588-022-01243-4); Nb4 used only its pinned fibroblast subset | P09/P03 fibroblast context; full release is a candidate for immune, epithelial and vascular validation | Existing fibroblast subset cannot supply missing compartments. Full expression: PRJEB52292; spatial: E-MTAB-11640; imaging: S-BIAD570. Recover exact version, cell/nucleus modality, region, donor overlap and independent image annotation |
| S04 | [Sikkema HLCA 2023](https://doi.org/10.1038/s41591-023-02327-2); neighboring repository article available | Annotation crosswalk, cohort discovery, independent study selection | Trace source-study and donor IDs; an integrated object can contain S01, S03 and disease cohorts. Exclude overlaps and document annotation-training exposure; return to original counts for expression tests |
| S05 | [Adams GSE136831](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE136831); already used in neighboring article analyses | P03 IPF discovery, P05 immune context, P07 disease epithelium | Re-audit diagnosis, regional sampling, raw layer, donor joins and prior exposure; use source-defined IPF/control groups, not a mixed diagnosis bucket |
| S06 | [Habermann GSE135893](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135893); already used in neighboring analyses | P03/P07 second-cohort transport | Restrict primary disease comparison to verified IPF and controls; exclude other fibrotic diagnoses from that estimand; reconcile donor overlap, anatomy and labels |
| S07 | [Murthy GSE178360](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178360); three source filtered matrices joined in the completed Nb4 MYRF diagnostic | Candidate epithelial reference for P01/P06/P07 | Prior candidate epithelial labels and sparse AT1 coverage do not establish basal/AT2-s coverage, regional validity or independence for the new endpoint |
| S08 | [Mouse lemur atlas 2025](https://doi.org/10.1038/s41586-025-09114-8); primary paper inspected, no new matrix used | P02 third-species qualification and updated novelty screen | Audit actual lung biological units, age, orthology release, raw layers and reuse of human/mouse sources. Published expression-based mappings must not define the same alignment used to test expression conservation |
| S09 | Independent matched human lung–blood cohort | P04 external validation | **No qualified accession selected.** Find paired donor/subtype coverage and tissue-processing details; a lung-only atlas can validate localization but not the lung–blood contrast |
| S10 | Independently annotated spatial or functional observations | P05/P07/P08/P09 specificity; P04 persistence; P06 fate | **No linked functional dataset qualified.** Spatial candidate S03 does not by itself measure duration, ancestry, stemness, perfusion or electrophysiology |

The repository's previous numerical use of S05/S06/S07 does not make their
new proposal contrasts eligible or unseen. Current GEO page retrieval returned
a browser challenge for S05/S06; their accessions/previous use here are grounded
in the local inventory, not a newly completed remote payload audit.

## Existing research to reuse as evidence

| Repository case | Reusable lesson or source | Boundary |
|---|---|---|
| [Nb3](../../../gate2_N2_nabhan_2026/README.md), [A22](../../../../RQ_Specified/A22_epithelial_identity_niche_response/README.md) | Identity versus amount; chemokine endpoint and target-omission sensitivity | Mixed-species screen and current prediction limitations are not healthy-atlas validation |
| [A13](../../../../RQ_Specified/A13_fibroblast_beyond_macrophage_il1b/README.md) | Fibroblast contribution beyond macrophage context | Existing unsuccessful held-out gain is not rescued by an atlas correlation |
| [A8](../../../../RQ_Specified/A8_maturation_component_at1_contribution/README.md) | Separate RNA identity from independent mature contribution | No mature-function endpoint in current Nb4 atlases |
| [A0](../../../../RQ_Specified/A0_conserved_epithelial_transition_program/README.md), [A5](../../../../RQ_Specified/A5_developmental_programme_reuse/README.md), [A11](../../../../RQ_Specified/A11_lesion_programme_addition/README.md) | Shared versus context-specific epithelial programs | P07 must test regional redeployment separately from a generic plasticity score |
| [A19](../../../../RQ_Specified/A19_fzd_response_reversibility/README.md), [A20](../../../../RQ_Specified/A20_fibroblast_fzd_context/README.md), [A21](../../../../RQ_Specified/A21_fzd4_capillary_function/README.md) | Receptor response, fibroblast support and vascular function are different endpoints | Expression does not supply withdrawal recovery, epithelial support or vascular integrity |
| [Cardoso article](../../../gate2_05_cardoso_2026/README.md), [HLCA article](../../../gate1_04_sikkema_2023_hlca/README.md) | Disease data intake, donor-level comparisons, annotation context | Preserve original source units and prior analytical exposure |
| [Nb4 completed sequence](../RQ_SEQUENCE_RESULTS.md) | Captured composition, C3/panel disagreement and comparator coverage | These already observed diagnostics constrain new interpretation; do not relabel them new discovery |

## Note coverage and corrections

The owner-linked [Result Body notes](https://app.notion.com/p/Result-Body-3ec151616b448084976cfd33b11847e3)
motivate the following coverage: disease catalogue → P03; species differences
→ P01; evolutionary redistribution → P02; immune tissue association → P04;
IGSF21/EREG/TREM2 populations → P05; Wnt/metabolic AT2 heterogeneity → P06;
regional basal identity → P07; pericyte/endothelial diversity → P08;
SCN7A/GRIA1 fibroblasts → P09. MYRF maturation and C3/chemokine follow-ups
retain their existing owners and completed reports.

Use corrected **GRIA1** and **SPINT2** symbols. Differentiating basal cells
have reduced KRT5 with increased HES1/KRT7/SCGB3A2 in the source interpretation.
Wnt RNA is not pathway activity; disease-gene localization is not disease
causation; tissue association is not demonstrated long-term residency.
Private notes and target-map content remain outside the public repository.
Only these scientific topics and source corrections are summarized.

## Literature screen before promotion

The 2020 paper already compared cell-type expression across species, so
rediscovering an HHIP/SERPINA1 switch is a reproduction target, not novelty.
The 2023 HLCA and spatial atlas broaden reference and disease context, and
the 2025 lemur study makes orthology and comparative-cell-expression questions
especially important to screen against later work. The proposed contributions
are the specific discriminating contrasts in each plan. None is labelled
novel until a targeted search establishes what remains unanswered.
