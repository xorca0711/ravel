# Bounded source/access log — 7 October 2026

Purpose: check PR140 score semantics and A30's current biological rationale.
Service: web search and direct publisher/PMC/official software documentation.
Window: 2024–2026 for recent CSF/T-cell work, plus unrestricted source-paper,
dataset and foundational searches. Existing 5 October literature is reused where
unchanged. Publication dates, rather than index crawl dates, determine recency.

## Queries actually issued

- `"The glycolytic reaction PGAM restrains" PMC`
- `site.github.com/YosefLab/Compass reactions.tsv penalty -log score`
- `"106324" "CCR5" Th17`
- `CSF blood matched TCR CD4 activation multiple sclerosis single cell 2024 2025 2026 compartment`
- `"10.1016/j.ebiom.2026.106324"`
- `"Schafflick" "14118" PMC`
- `CSF CD4 T cell Th17.1 CCR5 natalizumab 2026 paired blood`
- `"s41590-025-02412-3" correction`
- `"106324" correction CCR5` and `"115799" "correction" PGAM`
- `site:pmc.ncbi.nlm.nih.gov/articles/PMC13264205 "Fig. 3" natalizumab`
- `"10.1016/j.ebiom.2026.106324" correction retraction`
- `"10.1016/j.celrep.2025.115799" correction retraction`

Several numerical-title searches returned irrelevant results. They do not provide
correction clearance. No relevant correction surfaced in this bounded pass;
Crossmark/retraction databases and all citing papers were not exhaustively checked.

## Read evidence and access

| Source/version | Access and exact scope |
|---|---|
| [Wang et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12443480/), Cell Reports 44:115799; online 5 June, issue 24 June | PMC HTML Results/Figure 3, human Figure S4 discussion and relevant STAR Methods. DOI route refused access. This is a contrast/source audit, not independent inspection of every raw assay or supplement. |
| [Schafflick et al. 2020](https://pubmed.ncbi.nlm.nih.gov/31937773/), Nat Commun 11:247, 14 January | Indexed abstract/identity and previously recorded GSE138266 linkage. Publisher retrieval failed; PMC browser challenge prevented full-text methods access. |
| [van Puijfelik et al. 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13264205/), EBioMedicine 129:106324, 2026 journal version | Indexed full-text Results, Figures 2–3 and assay descriptions. Direct reopening hit a browser challenge. Fig. 2 uses paired CSF/blood; Fig. 3 compares pre/post-treatment blood. No PDF/visual supplement audit claimed. |
| [Hayashi, Mittl et al. 2026](https://www.nature.com/articles/s41590-025-02412-3), Nat Immunol 27:490–502; online 5 February | Publisher HTML Results/Figure 1 and paired RNA/TCR methods. CD4 compartment context was distinguished from CD8 antigen findings. Reused-source independence remains to be qualified. |
| [Compass tutorial](https://yoseflab.github.io/Compass/notebooks/Demo.html), [authors' fork](https://github.com/wagnerlab-berkeley/Compass), [settings](https://compass-wagnerlab.readthedocs.io/en/latest/settings.html) | Current official raw-output convention and explicit negative-log preprocessing; compared against the PR140 script and serial shim. No claim that a historical software checkout was rerun. |
| [ARRIVE study-design guidance](https://arriveguidelines.org/arrive-guidelines/study-design/1a/explanation) | Item 1a: comparator choice depends on the objective, including WT/genetically modified examples. Used to support design-proportional instruction wording, not to mandate an animal protocol for every RQ. |

References linking the source human analysis to GSE138266 were followed. No
systematic forward-citation database search was completed. Brain 2018 Th17.1 and
other retrieved leads were not promoted to read evidence. The stop point was
sufficient to distinguish the paper's disease/PGAM contrasts, the composition
alternative and TCR interpretation limits. Detailed assay feasibility, cohort
overlap and full Schafflick methods remain specific follow-ups, not claims of
novelty, comprehensive literature coverage or experimental readiness.
