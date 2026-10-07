# Neighbouring packages and existing questions

**Current execution and interpretation — 7 October 2026:** see [corrections](CORRECTIONS_2026-10-07.md) and [the current README](README.md). Dated stage plans, intake states and derivation counts below remain historical. A28–A30 are now registered; the full portfolio is A0–A30.

Reviewed against fetched `main` `9a49d26a79f4f9a32142bb07281ac062c62cb1a4`,
4 October 2026, which already contains the merged 2021 Wagner package (PR #137).
The question register holds **A0–A27**; this package adds none and changes none.
Shared guidance read for this pass: `AGENTS.md`, `AI_CONTEXT.md`,
`docs/RESEARCH_GOVERNANCE.md`, `docs/LITERATURE_WORKFLOW.md` and the roadmap.

| Neighbour and its premise | Repository evidence consulted | What this paper adds, and the boundary |
|---|---|---|
| **Wagner 2021 (paper 15)** — reaction-level metabolic potential from single-cell RNA | [Package](../gate2_W1_wagner_th17_autoimmunity/README.md), [reproduction scope](../gate2_W1_wagner_th17_autoimmunity/REPRODUCTION_SCOPE.md), [branch register](../gate2_W1_wagner_th17_autoimmunity/BRANCH_REGISTER.md) | This is the same method applied to a new perturbation, by overlapping authors. It is **one evidence lineage**, so agreement between the two papers is not independent replication. It does supply a worked instance of Wg-P02's reaction-heterogeneity question, and it shares the unresolved PGAM reference-sign conflict |
| **Yadav 2025 (paper 16)** — myeloid-to-mesenchymal ARG1 and ornithine circuit in lung fibrosis | Roadmap entry only; not read | Wagner is a co-author there too. That paper is about *intercellular substrate supply*; this one is about an *intracellular reaction*. Keeping those separate is the point of [Wg-P06](../gate2_W1_wagner_th17_autoimmunity/branches/P06_ornithine_context.md), and this package does not reopen it |
| **Choi 2020 (paper 2)** — IL-1β/HIF1α-driven AT2→DATP→AT1 transition | [Package](../gate1_02_choi_2020/README.md) | The closest lung precedent for metabolism gating a transitional state, and the reason a metabolic bridge is tempting. HIF1α-driven glycolysis in epithelium is not a reaction-level claim, and nothing here tests PGAM in epithelium. [Wp-P06](branches/P06_epithelial_transfer_condition.md) holds the conditions |
| **A1 / A8 / A14** — maintenance, maturation components and withdrawal recovery | [A1 dossier](../../docs/research_dossiers/A1.md), [A8](../../docs/research_dossiers/A8.md), [A14](../../docs/research_dossiers/A14.md) | These questions already record the missing early-measurement-to-later-outcome linkage in the same biological units. A metabolic feature inherits that gap. This package must not be cited as progress on it |
| **A2 / A9 / A12 / A13** — delivery and recipient competence | [A12 dossier](../../docs/research_dossiers/A12.md), [A13](../../docs/research_dossiers/A13.md) | Useful as design discipline: those questions separate exposure from reception and keep an RNA receptor index distinct from measured signalling. The same separation applies to reading an RNA metabolic module as a flux |
| **England 2025 (paper 12) and the A16 work** — within-state versus compositional attribution | [Package](../gate2_C2_england_2025/README.md) | The composition-versus-within-state method in [Wp-P03](branches/P03_glucose_composition_vs_state.md) is this project's existing discipline, learned where a marker contrast largely dissolved inside subclusters. The biology does not transfer; the decomposition does |
| **Nb5 ageing/immune comparison (paper 14 family)** | [Extension completion](../gate2_N4_nabhan_aging_atlas_2020/EXTENSION_COMPLETION.md) | Precedent for separating composition from within-state change in an immune compartment with few animals, and for reporting donor- or animal-level limits plainly. CD8 ageing evidence is not Th17 validation |

## What this package deliberately does not do

- It does not create or renumber a canonical question. The register stays
  A0–A27, and the six Wp candidates are article-local.
- It does not merge with the 2021 package. Separate paper, separate deposits,
  separate namespace (**Wp** against **Wg**), with explicit cross-links where a
  question is shared.
- It does not mark Yadav (paper 16) as read, change the reading order, or alter
  any existing paper's status.
- It does not import a metabolic score into any lung question. That route is
  gated by [Wp-P06](branches/P06_epithelial_transfer_condition.md)'s conditions.
- It does not treat the Th17/EAE system as a model of lung repair. CNS
  autoimmunity after adoptive transfer of drug-exposed cells answers a different
  question from alveolar regeneration, and the shared vocabulary of
  "transitional" and "regulatory" states is not evidence of a shared mechanism.
