# Biological review of DuPage results and the three follow-up candidates

**Subsequent question-development update — 7 November 2026:** [A33–A35 and the reframing audit](rq_derivation/README.md) now own the three proposed comparisons. The refresh adds a missed Il2ra/background counterexample to the CCR2 premise and restricts loss/gain interpretation to descriptive RNA context. The dated checkpoint below remains historical; frozen evidence is unchanged.

7 November 2026. Agent review requested by the owner before opening a PR.
This records scientific reasoning and corrections; it is not human approval,
target validation or adoption of a canonical question. Reviewed through local
commit `b207aef`, against refreshed unchanged main `dcee4b6`.

## Scope and overall judgment

Reviewed the current S0–S6 synthesis, source/assay qualifications, S2 sensitivity,
S3 mapping limits, both target-screen specifications, complete coding-frontier
dispositions, proposal text and figure captions. Reused the valid arithmetic,
annotation and rendering checks rather than recalculating the same data.

The results support **exploratory, gene-specific questions about activated Treg
state and function**. They do not identify direct Ezh2 targets, explain the EAE
phenotype, prove failed homing, or establish repair competence. All three
candidate directions may proceed to qualification, but none is experiment-ready.
The screen's finite reading frontier and prior outcome exposure are explicit;
the 32 entries are not statistically selected discoveries.

## Findings that change interpretation or experimental planning

| Finding | Evidence | Required interpretation / next action |
|---|---|---|
| Genotype and state are not interchangeable | KO is compared with HET; CD62L is observed after perturbation; profiled cells are Foxp3-positive survivors | Keep the descriptive comparison distinct from an activation intervention and from total lineage-level effects. A common-exposure follow-up is justified, but cannot retroactively identify those effects in the source data. |
| IGFBP4 is not activation-induced in this table | Existing mean-log values: HET high 7.247, low 4.712; KO high 7.718, low 6.225. Existing state contrasts are −2.535 and −1.492 | The KO-low excess is compatible with *less downregulation across observed states*, not activation-induced Igfbp4. The samples are not a time course. Regulatory failure, compensatory expression and state composition remain alternatives. |
| The IGF precedent deliberately bypasses binding-protein regulation | [2020 IGF study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8078727/), Results after Figure 1 and Figure 2: desIGF1 has reduced affinity for IGF-binding proteins | It supports receptor-response biology, not an IGFBP4-buffering assay by itself. A buffering test must retain native-ligand binding; a reduced-binding ligand can be a separate receptor-competence/bypass comparison. |
| TIGIT/PRDM1 changes are attenuated state contrasts, not disappearance | Tigit high→low contrasts: HET +4.440, KO +3.397; Prdm1: HET +1.570, KO +0.416. Areg interaction is fragile | Ask about a response deficit, not complete absence of the pathway. Qualify TIGIT protein and assay responsiveness before interpreting a negative result. These values are cross-sectional differences, not measured induction kinetics. |
| TIGIT precedent depends on activation and priming context | [2025 TIGIT study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12571903/), Figures 5–6 and Extended Data 8; main Results and stimulation descriptions | Published primed-cell/splenocyte responses do not guarantee a response in purified, otherwise naive Tregs. Specify activation history, accessory-cell context and a responsive control. An assay-negative control population cannot falsify the Ezh2-specific hypothesis. |
| A CCR2/CD25 model is plausible but not already supported by CD25 RNA | [CCR2 study](https://pmc.ncbi.nlm.nih.gov/articles/PMC7000403/), Figure 5 and Discussion; DuPage Il2ra contrasts are small/fragile | Measure receptor protein and signaling. Keep chemotaxis, viable recovery and IL-2 response separate. The source's mixed-cell stimulation experiments do not establish an autonomous CCR2→CD25 response in purified Tregs. |
| Biological precedent limits novelty claims | [EZH2 gain study](https://pubmed.ncbi.nlm.nih.gov/39264807/), Figures 2B/4D/7G; 2025 TIGIT mechanism; established CCR2 and IGF biology | The candidate genes and broad relationships are known. Potential contribution lies in a specified Ezh2-dependent functional comparison or contextual boundary, not rediscovering those associations. |
| Single-cell and chromatin context are not validation | Arvey is reused published context; source/lineage contrasts involving Igfbp4 and Dapl1 vary across papers | Confirm molecular source and protein before perturbation. Do not label uncovered loci unmarked or mapped loci direct Ezh2 targets. |

All quoted numerical values are rounded lookups from the existing
[all-annotated table](../../analysis/research/runs/dupage_target_screen_v2/all_annotated.tsv),
in mean log2(FPKM + 1) units. No new numerical analysis or inferential test was
performed for this review.

## Decision for the requested three candidates

- **TIGIT–PRDM1:** proceed with assay-context/source qualification and a specified
  genotype-dependent response comparison. Protein/secreted output and a recipient
  functional endpoint are separate stages. The broad EZH2/TIGIT relationship is
  already a premise, and this review does not rank this route as experimentally
  readier than the other two.
- **CCR2:** proceed with a localization-versus-fitness question. Direct movement
  and signaling/viability readouts are required to distinguish those accounts;
  expression or tissue abundance cannot substitute for either.
- **IGFBP4:** proceed first with molecular-source and ligand-compatibility checks.
  This has a greater expression-context uncertainty; the proposed action is
  qualification, not an assumption that blocking IGFBP4 will restore function.

For each candidate, retain mediator, general state/selection and compensatory or
assay-limited explanations where relevant. Measure both absolute recovery and
per-viable-cell output: normalization alone must not hide differential survival.
Any future target-specific perturbation must distinguish its intended target
from effects on recipient/accessory cells. Precision and sample size remain
unspecified until a model, assay variance and meaningful endpoint are established.

## Search and access audit

Reused the same-day bounded literature scan and retrieved TIGIT full text.
Targeted live checks on 7 November 2026 used:
`"CCR2 enhances CD25" "chemotaxis" "Tregs"`,
`"IGFBP4" "Ezh2" Treg`, and `"TIGIT" "EZH2" "AREG"`.
The IGF primary Results were read specifically for desIGF1 and assay design.
The broad IGFBP4/EZH2 search also returned a 2024 hepatocellular-carcinoma
perturbation study; it is a cross-cell-type precedent lead, not Treg validation.
No source was counted as independent replication on the basis of a different
paper title. Direct PMC access to some pages still returns browser checks;
CCR2 review remains based on the indexed primary Results/legend and explicitly
requires fuller source qualification in the follow-up.

## Publication disposition

Suitable for a PR as an exposed reconstruction, measurement audit, exploratory
candidate screen and proposed experiment portfolio with the qualifications
above. Existing frozen contracts, results, figures and prior unfavorable findings
are preserved. This addendum governs interpretation of the earlier proposal
wording, including the earlier "clearest functional extension" preference.
Candidate-specific follow-up records will document what can actually be done
next; the PR does not confer scientific acceptance.

Documentation validation: 17,065 repository checks and the research gate against
refreshed `origin/main` passed. Earlier arithmetic, source and figure checks
remain applicable because their inputs, scripts and frozen outputs did not change.
