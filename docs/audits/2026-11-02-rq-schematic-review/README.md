# Registered question and schematic quality review

2 November 2026, Asia/Seoul. Owner requested a review of the registered questions
and their illustrations, followed by a new technical chat for biological
schematic redesign using available external connectors, preferably BioRender.

Reviewed checkout: `9e7fe4dd86c6610a2e8cafbe65b7f812b0148ea2`, the clean final
head of [PR #158](https://github.com/xorca0711/ravel/pull/158). Refreshed main was
`96e6a8d033b11da2599e0fd5d91f87d16817f58c`; A32 remains proposed on the PR branch.
This follow-up uses `codex/rq-schematic-quality-20261102`, preserving that PR.

## Coverage and review method

The [registry](../../../analysis/research/registry.json) identified all 33 current
canonical guides. The reviewer read each dossier's working hypothesis, relevant
alternative and maturity statement; extracted every illustration's visible text;
rendered all 33 original SVG files directly with sharp/librsvg; and inspected six
contact sheets plus full-size A8, A28 and A31 views. Existing hash/link reconciliation
from the [navigation audit](../2026-11-02-navigation-hygiene/REPORT.md) remains
valid at this unchanged source head. No new biological analysis was run.

This is a question-framing and visual-communication review, not an independent
reproduction, full paper reread, portfolio ranking or novelty certification.
Before a redesigned arrow uses a biological claim, the technical author must
check its current owning context/result. A registered question is not an accepted
mechanism. Current hypotheses and scientific dispositions are not rewritten here.

Rendered review images and inventory are local scratch artifacts under
`rq_visual_audit` in the coordinating chat's visualization directory. They are
presentation previews of existing qualitative drawings, not measured figures.
The original registry paths remain the reproducible review inputs.

## Overall assessment

The strongest feature is scientific restraint: the questions generally separate
description, replication, prediction and perturbation effects, retain unfavorable
results, and name missing discriminators. The remaining problem is uneven
biological specificity. A1/A2/A3/A6/A9/A12/A13 and A24 still have an unnamed
feature, product, compartment, consequence or population. A more detailed icon
cannot legitimately fill that gap. Several other questions have a defined
comparison but lack linked lineage/function data or qualified biological units.

The drawings are generally orderly and their cautionary captions are useful.
A0–A27 already contain schematic cells, organs or lineage symbols; describing
all of them as text-only would be inaccurate. Their repeated two-row/three-box
template nevertheless makes very different questions look alike, and places too
much reasoning in small prose. Intracellular, extracellular, tissue and time
relationships often exist only in labels. The generic RNA glyph is not a
biological pathway. At README scale the reader must still read most of the text.

Priority here means **redesign order**, not scientific priority:

- A31 is entirely a workflow of boxes and arrows, with no biological cell or
  receptor depiction. It is the clearest first redesign.
- A28 and A29 contain 431 and 427 whitespace-separated words, respectively.
  Their central visual is four culture-dish symbols; the biological distinction
  is largely carried by an experiment/readout table. These need biological
  overview figures, with detailed design material retained in their documents.
- A30 is a 289-word comparison/checklist layout. A paired blood/CSF donor diagram
  can clarify its association question without asserting trafficking or residency.
- A32's 191-word v2 is more biologically legible, but its metabolic/matrix arrows
  should be made more locally explicit about context-specific published premises.
  The complete chain in a new model and the epithelial effect remain unresolved.

The 24 earlier A0–A23 drawings contain 203–254 visible words each. The full
hypothesis paragraph, outcomes and provenance should remain available beside
the figure, rather than competing with its biological story inside the canvas.
Word counts describe typography only; they are not quality or evidence scores.

## Question-by-question redesign brief

| ID | Question framing / boundary to preserve | Visual change that would help |
|---|---|---|
| A0 | Failed fixed-component transfer; state comparability remains open | Distinct lung alveolus and intestinal epithelium, with the failed transfer visibly separated from proposed state correspondence. No shared lineage claim. |
| A1 | Early regulatory predictor unnamed; later mature output must be linked | Transitional epithelial cell/nucleus and a separate lineage timeline; candidate chromatin feature stays explicitly unknown. Prediction link must not look causal. |
| A2 | Delivery versus receptor context; source/presentation contrast and function unnamed | Epithelial source, extracellular AREG and fibroblast membrane as separate compartments. Do not select a release route or endpoint by drawing it. |
| A3 | History beyond age, origin and continuing stimulation; programme/function unnamed | Same-origin macrophage timeline with resolved versus continuing context. Show a chromatin/RNA compartment only as a measurement possibility, not a proven memory mechanism. |
| A4 | Within-lineage response acquisition versus selection | Alveolar AT2 clones with persistent lineage IDs; split Wnt history from current Wnt and IL-1 response. Do not introduce a Fzd5 entry gate. |
| A5 | Exact developmental component replication, not functional reuse | Developmental and adult-repair tissue contexts linked by the same fixed measurement. Independent animal units, without a causal gene-network illustration. |
| A6 | Within-state disease association versus abundance; sparse control support | Macrophage populations in distinct tissue contexts with separate within-cell RNA and composition panels. No inferred effector activity. |
| A7 | Broad CEBPA identity premise versus baseline-state interaction | AT2 nucleus/identity and pre-defined starting states, followed by the same genotype contrast. Avoid grouping on states created by treatment. |
| A8 | Early RNA incremental prediction; not fate | Time-separated AT2-derived lineage and mature AT1 anatomy, with a clearly labelled prediction link and independent later endpoint. |
| A9 | Recipient competence at comparable effective AREG; contrast/function unnamed | Close-up fibroblast membrane and qualified EGFR-context concept. Unknown cofactor or inhibitory contrast remains unknown; RNA is not receptor activity. |
| A10 | Early growth prediction; existing measurements concurrent | Organoid silhouette with initial and later area separated in time. No simulated data curve or automatic proliferation/repair interpretation. |
| A11 | Frozen residual's incremental lesion information unresolved | Repair and lesion epithelial contexts beside fixed measurement definitions. Do not invent a cancer-specific cell type or pathway. |
| A12 | Recipient compartment and receptor/inhibitory contrast still open | Separate epithelial and fibroblast IL-1 reception panels; indicate unresolved choice instead of combining both into one inferred mechanism. |
| A13 | Fibroblast product unselected; negative proxy pilot retained | Myeloid input, fibroblast secretion compartment and epithelium; product labelled unknown. Do not replace the failed proxy with an attractive invented mediator. |
| A14 | H1 duration/cessation; H2 stromal reception has no assigned direction | Exposure-and-recovery timeline above epithelial/stromal compartments. Separate mature lineage output from survival and residual stimulation. |
| A15 | Published integrin/latent TGF-beta activation premise; context-specific attribution untested | Epithelial surface integrin, matrix-bound latent ligand and fibroblast receptor context. Visually distinguish known pathway from unmeasured activation/function in this source. |
| A16 | CD177 candidate marker, not fate regulator; source and later response unqualified | Surface protein on a qualified epithelial cell with contamination/mixture inset. No CD177-to-fate causal arrow or invented response. |
| A17 | Founder heterogeneity versus switching/observation; latent term not cell type | Branching lineage trees with observation/survival overlays. No measured clone counts or newly named founder subtype. |
| A18 | WT expansion and identity are separate outcomes | Mutant and WT neighbours in alveolar tissue, plus two independent readouts. SPP1/DLK1 stay candidates, not two established signaling channels. |
| A19 | Ending versus continued Fzd input; mature output plus retained AT2 reserve | Schedule split followed by flattened AT1 and retained responsive AT2 cells. Keep source-supported input candidate separate from fixed reagent choice. |
| A20 | Fzd2/Fzd1 source contrast and early pool versus late maturation | Fibroblast receptor comparison beside a time-resolved AT2 pool/AT1 panel. No assumption that early-pool adjustment proves mediation. |
| A21 | Capillary function linked to lineage output; full route unproved | Alveolar capillary barrier, gCap and aerocyte compartments, separating integrity, survival and traced output. No tumour-to-normal repair transfer claim. |
| A22 | Focal NKX2-1 contrast and extracellular protein extension; protein unnamed | Epithelial identity/viable amount, fibroblast cell state and extracellular product shown separately. Flag the older generic maturity wording for reconciliation, without silently changing the hypothesis. |
| A23 | Increased entry versus prolonged residence; mature exit separate | AT2-to-intermediate-to-AT1 timeline with transport at the membrane and entry/exit alternatives. Preserve the published premise and failed external marker transfer. |
| A24 | Stromal contribution versus epithelial ageing; population unnamed | Layered bladder stroma and urothelium with barrier anatomy. Do not assign a particular stromal subtype or mechanism. |
| A25 | RNA organization/model comparison, not new state/function | Recognizable microglia and brain-region context beside labelled model alternatives. No invented cluster geometry or empirical distribution. |
| A26 | Paired tissue age association at fixed state/sampling | Spleen and marrow from one animal; T-cell identity and clone symbols with a qualitative legend. No local niche mechanism or cell-count-as-data appearance. |
| A27 | Within-state contribution plus redistribution, not causal percentage | State and clone symbols encoded separately; total versus composition-standardized comparison. No causal fraction or immune-function claim. |
| A28 | Same-cell regulatory/effector dissociation; markers do not equal competence | One T cell with nuclear/surface/cytokine marker locations and two independently evaluated outputs. Shared-axis alternative inset; move culture instructions out of the overview. |
| A29 | Published PEP, stress and demand alternatives can coexist | T-cell metabolism, transcriptional complex and growth/stress branches. Solid published premises versus dashed source-specific hypotheses; no invented kinetics, unique rescue proof or increased cytokine secretion claim. |
| A30 | Paired CSF/blood within-state RNA association | Donor-linked blood/CSF sampling and matched T-cell states, with activation/composition alternatives. Do not depict demonstrated migration, CNS residency or preserved regulatory function. |
| A31 | GRIA1-dependent acute response, assay still unnamed | Alveolar fibroblast with membrane receptor candidate, glutamate and matched comparison. Do not pick calcium/electrophysiology or functional surface assembly as established; SCN7A is optional context. |
| A32 | Separate matrix and mature epithelial effects; direction unresolved | Retain myeloid/fibroblast/alveolar entities, add local evidence labels and clearer source-restricted comparison. No assumed collagen-to-recovery mediation or fixed myeloid identity. |

## Technical acceptance criteria

1. Give the eye a biological subject: appropriate cell/tissue geometry,
   compartment and relevant molecule. Decorative icons beside unchanged text
   boxes do not meet the owner's request.
2. Separate established premise, proposed effect, prediction/association and
   unresolved identity using both labels and line styles. Unknown molecules,
   endpoints and assay choices stay unknown. Keep solid arrows local to their
   source-qualified statement; a whole solid pathway can overclaim its chain.
3. Prefer one comparison and one main uncertainty per overview. Use a short
   caption for the unit, readout and interpretation limit. Retain the complete
   hypothesis in its dossier; do not squeeze it into the image. Roughly 80–140
   on-canvas words is a design target, not a scientific gate or forced cutoff.
4. Review at full size and ordinary README width (about 800 pixels): readable
   labels, no overlap, recognisable entities, consistent vocabulary, sufficient
   contrast and meaning independent of colour. No fake numerical plots.
5. Preserve every currently registered illustration and working hypothesis.
   Corrections get new versioned files, supersession captions, registry hashes
   and updated owning README/context/guide links. Keep article galleries and
   root collection navigation unchanged. No numerical rerun or claim promotion.
6. The current inert-SVG gate permits svg/title/desc/rect/line/ellipse/polygon/
   text/a only, with no active or external content. Do not weaken it or create
   infrastructure exemptions for arbitrary connector output. Export format and
   public-repository reuse rights must be checked before integration. A licensed
   BioRender draft is not automatically an admissible registered SVG.
7. Record a per-question disposition, source/asset provenance, connector used,
   new version, visual QA and any precise hold. Stop repeating identical access
   failures. Run link/registry/preservation checks for the final integration.

## Connector qualification and execution plan

The owner reports BioRender connected through ChatGPT Apps. This coordinating
chat's refreshed tool inventory still exposes no BioRender method, and its
BioRender plugin search returned no result. This is a visibility limitation,
not proof that the owner's connection failed. Sequence/NGS viewers and protein
prediction tools are not substitutes for a biological illustration connector.

The new technical chat must independently check its live tools. Qualify search,
asset preview, editable figure creation, save/export, attribution/reuse rights
and account identity separately. Search-only functionality must be reported as
such. Verify the user's external xorca identity before account-dependent writes;
never use the AI-host identity or copy credentials. Do not reconnect accounts,
purchase a plan, send messages or bypass access controls.

Start with A31 (receptor/cell), A3 (history/tissue) and A28 (same-cell two-output
question), then apply the reviewed visual language to the rest. This order spans
three design problems; it does not rank research value. For each unresolved
connector or license condition, finish the biological storyboard and document
the exact blocked export step. If BioRender remains unavailable, make useful
original editable SVG improvements with available native/vector tools and
label them honestly; do not call them BioRender-generated. Do not stop at a
capability report or regenerate a second text-only template.

Existing complete context and source-result links are in each registered guide.
Do not scan the old chat history or follow the previous problematic chat deep
link; this note and current repository evidence provide the technical handoff.

## Execution status

The portfolio review and redesign brief are complete. Technical chat
`01a199c1-39af-7b92-bdf0-32711480c2eb` checked the now-visible BioRender connector:
template search succeeds, while three long-prompt preview jobs failed. The
coordinator's later short/template attempt also failed. The owner rejected the
rough native SVG pilots as the solution; they are preserved only as local
backups. No registered illustration has changed.

The active route is authenticated BioRender editor assembly from discovered
templates, with the coordinator owning browser control and xorca sign-in.
See the [implementation and failure record](IMPLEMENTATION.md),
[source-grounded pilot storyboards](BIORENDER_STORYBOARDS.md) and
[per-question ledger](LEDGER.md). Redesign remains unfinished. No main merge,
numerical execution or public BioRender export is claimed or authorized here.
