# Nabhan hypotheses: source reproduction and new questions

Status on 29 September 2026: **initial analyses executed; hypotheses remain unvalidated**.
See [results](RESULTS.md), the [stage ledger](metadata/stage_status.tsv), and the
execution update within each candidate card.
The later [branch execution and candidate interpretations](branch_analysis/README.md)
remain paper-local. The subsequent [overall synthesis](RQ_DERIVATION.md) derives
proposed A19–A21 question plans under `RQ_Specified`; the eight branch identities
remain unchanged. Source claims below retain their own status.
P1 refers to the supplied [2023 paper](https://doi.org/10.1016/j.cell.2023.05.022);
N1–N3 are the sources in the [audit](SOURCE_AUDIT.md). Source findings, the owner's
ideas and the assistant's operational hypotheses are identified separately.
Paper-local IDs are distinct from the subsequently proposed A19–A21; no C-register grade changes.

<a id="published-claims"></a>
## Track 1: the paper's claim/hypothesis list

These are propositions to reproduce or audit, not assertions of repository success.

| ID | Published proposition | Source anchor | Accessible test and limit |
|---|---|---|---|
| Nb2-P1 | Receptor RNA separates epithelial Fzd5/6, stromal Fzd1 and endothelial Fzd4 compartments, with disease-state exceptions | Figure 1/S1; PDF pp.3–4/27 | R1: donor/animal receptor maps; spatial puncta reproduction needs original imaging/animal tables |
| Nb2-P2 | AT2 cells and fibroblasts depend on different receptor families | Figure 2/S2; pp.6/29 | R4: culture-level inhibition/qPCR recovery; expression ranking alone does not reproduce dependency |
| Nb2-P3 | Fzd5 is required for Wnt-driven AT2 activity among tested receptors | Figure 2G–J/S2G; p.6 | R4: growth and editing efficiency jointly; distinguish edited-cell mixtures from single-cell genotype |
| Nb2-P4 | Fzd5 and synthetic Fzd6 activation stimulate AT2 growth; the Fzd6 response is receptor-dependent | Figure 3/S3; pp.6–7/30–31 | R4: organoid and reporter controls, separately; this is synthetic sufficiency, not endogenous Fzd6 necessity |
| Nb2-P5 | Agonists restore Wnt/proliferation/AT2 transcription and suppress AT1/airway-associated transcription after CHIR withdrawal | Figure 4B–D; pp.7–9 | R2: bulk condition contrasts and exact gene panels; qPCR is a separate assay |
| Nb2-P6 | Receptor agonists differ from CHIR in Hippo-associated transcription; no significant Fzd5/Fzd6 transcriptomic difference was detected | Figure 4D; p.9 | R3: direct contrasts, gene-level effects and uncertainty; no equivalence claim without a margin |
| Nb2-P7 | Epithelial-targeted agonists outperform broad CHIR in mixed alveolosphere growth, while Fzd1 agonism reduces growth | Figure 5A–E/S4A–B; p.9 | R4: independent culture growth and AT1-marker outcomes; do not join these cultures to Figure 4 RNA without IDs |
| Nb2-P8 | Fzd5/Fzd6 agonists increase AT2 proliferation after injury | Figure 5F–H; pp.9–10 | R4: mouse-level EdU fractions and denominators; captured-cell abundance is not this endpoint |
| Nb2-P9 | Agonists improve survival without increased measured fibrosis in the assessed preventative setting | Figure 6/S5; pp.11–12/15/33 | R4: separate survival experiments and fibrosis cohorts; delayed survival benefit does not establish delayed antifibrotic efficacy |
| Nb2-P10 | Fzd6 agonism promotes AT2-like features in airway-derived progenitors | Figure 7/S6; pp.11/13/34 | R4: lineage, Lysotracker and identity endpoints; a nonsignificant Fzd5 arm does not by itself prove a Fzd6-versus-Fzd5 difference |

<a id="nabhan-branch"></a>
## Track 3: Nabhan branch register

The following order preserves the seven items under **Nabhan branch** in the
owner's [theme list](https://app.notion.com/p/3e0151616b44807ba675e28eeb4db751),
followed by the additional ligand question as Nb2-N8. Each testable formulation
below is an assistant proposal grounded in that item, not an owner-accepted result.
These are questions left open by the 2023 paper, not a claim that all remain
unanswered in the 2026 literature. Update the targeted literature/novelty check
before promoting a candidate to a new study claim.

The owner's follow-up priorities are developed in the [focused extension roadmap](EXTENSION_BRANCHES.md),
including discriminating comparisons, current-data limits and later primary literature.
It preserves these identifiers and distinguishes Hippo kinase signaling from
YAP/TAZ-associated output. No new hypothesis is promoted by that roadmap.

### Nb2-N1 — Does a withdrawal interval permit differentiation after expansion?

**Origin:** owner item 1; P1 Discussion p.14. **Hypothesis:** transient receptor
agonism expands an AT2 pool, and a subsequent off-period permits a greater mature
AT1 contribution than continuous stimulation at comparable exposure and survival.
**Rivals:** reduced growth, selective death, unequal exposure, or no durable maturation.
**Test:** independent preparations/animals with continuous, intermittent and withdrawal
comparators, verified exposure and later lineage-linked AT1 function. Analyze growth
and mature output separately. **Against it:** no maturation advantage with useful
precision, or an apparent advantage explained by loss of AT2 cells rather than
descendant gain. **Available now:** R2's 24/48-hour CHIR-withdrawal contrast is only
a transcriptional lead; it has no intermittent Fzd schedule or mature endpoint.
**Home/cross-links:** Nb2 branch; A4, A8 and A14 (timing analogy, not an IL-1 substitution).

**Nb2 execution update:** The six bulk conditions recover source panel directions but do not test intermittent scheduling or later mature outcome. Timing/preparation discrepancies remain; N1 needs a schedule-linked outcome design. See the [bulk](trials/bulk_v1/REPORT.md), [atlas](trials/atlas_v1/REPORT.md) and [functional](FUNCTIONAL_SOURCE_AUDIT.md) reports.

### Nb2-N2 — Does the receptor-level Hippo-associated response preserve plasticity?

**Origin:** owner item 2; P1 pp.9/14. **Hypothesis:** receptor agonism elicits a
YAP/TEAD-associated component absent or weaker with downstream CHIR, and this
component predicts later differentiation capacity beyond proliferation alone.
**Rivals:** mechanical/culture stress, unequal pathway strength, cell mixture,
or generic growth effects. **Test now:** R3/B1, with direct Fzd5–CHIR and Fzd6–CHIR
contrasts, exact Figure 4 panels, independent target sets and cycling sensitivity.
Bulk concordance cannot demonstrate simultaneous programs within individual cells.
**Discriminating follow-up:** compatible regulatory measurements and later
lineage/function in the same experimental design, with a separate perturbation of
the nominated regulatory process. **Against it:** no receptor-specific component,
or no added endpoint information after independent replication. **Links:** A1/A5/A8/A10;
the present RNA/imaging experiments cannot be paired by assumption.

**Nb2 execution update:** Fzd5–CHIR has a coherent three-gene Hippo-associated direction (+1.870 mean log2CPM; all9 cross-arm library differences positive). Fzd6 is heterogeneous; individual genes do not pass genome-wide FDR. Metabolic enrichment is correlation-sensitive. This is a measured RNA premise, not YAP activity or bipotency. See the [bulk](trials/bulk_v1/REPORT.md), [atlas](trials/atlas_v1/REPORT.md) and [functional](FUNCTIONAL_SOURCE_AUDIT.md) reports.

### Nb2-N3 — Does the starting epithelial state change the response to Wnt activation?

**Origin:** owner item 3; P1 Discussion p.14. **Hypothesis:** comparable receptor
activation has different effects on expansion and maturation in AT2, transitional
and airway-derived starting populations. **Rivals:** receptor dose/availability,
injury severity, state-label circularity and different culture survival.
**Test:** a treatment-by-starting-state interaction in independently replicated,
compatible experiments, with state defined before treatment and later fate measured.
**Available now:** B2/B3 receptor-context maps and the existing A4 Axin2/Il1r1 work
nominate populations; GSE208770 cannot supply this interaction. **Against it:**
responses are adequately explained by common activation/exposure with no useful
state interaction. **Links:** A1/A4/A8. Pseudotime alone cannot establish response order.

**Nb2 execution update:** Human receptor context differs across author states, but only one IPF participant passes the50-cell transitional-AT2 floor. FZD6 remains above FZD1 in all3 eligible KRT5−/KRT17+ participants after depth sensitivity. Treatment-by-state response remains unmeasured. See the [bulk](trials/bulk_v1/REPORT.md), [atlas](trials/atlas_v1/REPORT.md) and [functional](FUNCTIONAL_SOURCE_AUDIT.md) reports.

### Nb2-N4 — Does sustained Fzd5 loss provoke compensation?

**Origin:** owner item 4; P1 pp.6/14. **Hypothesis:** after verified Fzd5 loss,
alternative receptor/regulatory activity partially restores growth over time.
**Rivals to test first:** incomplete editing (source score 65%), persistence of
protein, selection of unedited cells, and the broader Fzd5/8 antibody target scope.
**Test:** genotype- and protein-resolved perturbation/time data, target engagement
and independent growth measurements. **Against compensation:** residual growth
tracks surviving unedited cells or the discrepancy disappears at comparable verified
target inhibition. **Available now:** source-data audit R4 only; no deletion RNA is
in GSE208770. Do not infer adaptation from expression of another Fzd in untreated
cells. **Home:** Nb2 branch; methodological link to A1, without repurposing its data.

**Nb2 execution update:** The functional audit recovered no deletion-linked genotype/protein/growth table. Agonist RNA cannot distinguish compensation from incomplete editing or selection. Keep the source65% editing limitation as a primary rival. See the [bulk](trials/bulk_v1/REPORT.md), [atlas](trials/atlas_v1/REPORT.md) and [functional](FUNCTIONAL_SOURCE_AUDIT.md) reports.

### Nb2-N5 — Does receptor use help explain divergent Wnt fate outputs?

**Origin:** owner item 5; P1 Discussion p.14. **Hypothesis:** receptor/context
combinations help determine alveolar, basal or ciliated outcomes and canonical
versus planar-cell-polarity responses. **Rivals:** ligand availability, co-receptors,
cell history and exposure kinetics. **Test now:** B3 maps receptor/co-receptor RNA
across explicitly defined airway/alveolar states. **Decisive evidence:** factorial
receptor/input comparisons within a common starting population with downstream
functional and fate endpoints. **Against it:** receptor choice adds no predictive
or intervention effect once context and activation are comparable. Transcript
ligand–receptor scores cannot establish signal routing. **Links:** A1/A4; relation
to recipient-context A12 is conceptual, not evidence of the same IL-1 mechanism.

**Nb2 execution update:** Captured airway and alveolar states differ in FZD5/6 context; ciliated cells show substantially more FZD6 than FZD5. This does not establish receptor routing, canonical versus PCP output, or founding lineage. No endogenous response is inferred from coexpression. See the [bulk](trials/bulk_v1/REPORT.md), [atlas](trials/atlas_v1/REPORT.md) and [functional](FUNCTIONAL_SOURCE_AUDIT.md) reports.

### Nb2-N6 — Does fibroblast Fzd1 have a context-dependent repair/fibrosis role?

**Origin:** owner item 6; P1 pp.3/14–15. **Hypothesis:** Fzd1-associated fibroblast
responses differ between resolving injury and persistent matrix-producing states,
potentially separating transient repair support from sustained remodeling.
**Rivals:** changing fibroblast mixture, shared Fzd2/7 function, and fibrosis-driven
receptor expression as a consequence rather than a cause. **Test now:** B4,
within-subtype animal/donor summaries of Fzd1/2/7 and independent ECM/response panels.
**Decisive evidence:** selective Fzd1 perturbation with epithelial support and matrix
outcomes in acute versus persistent contexts. **Against uniqueness:** effects are
shared with other receptors or disappear under subtype control. **Links:** A13/A15
for niche and matrix endpoints; neither existing question establishes Fzd1 signaling.

**Nb2 execution update:** Five eligible IPF myofibroblast participants support FZD1/2/7 profiles, but only one control passes the same floor. The post-run ECM association is shared in direction with FZD7 and is unadjusted at n=5. Unique FZD1 function and acute-versus-persistent outcome remain open. See the [bulk](trials/bulk_v1/REPORT.md), [atlas](trials/atlas_v1/REPORT.md) and [functional](FUNCTIONAL_SOURCE_AUDIT.md) reports.

### Nb2-N7 — Does endothelial Fzd4 support alveolar capillary regeneration?

**Origin:** owner item 7; P1 Discussion p.14 and ref.97. **Hypothesis:** Fzd4-dependent
signaling contributes to capillary progenitor response and functional vascular repair.
**Rivals:** Fzd4 is a broad endothelial identity marker or a barrier-maintenance
component, without a progenitor-specific regenerative role. **Test now:** B5,
separate general/aerocyte and any source-supported progenitor states; compare within
animals and disease contexts. **Decisive evidence:** endothelial-specific perturbation,
lineage and barrier/perfusion endpoints. **Against progenitor specificity:** the
association is uniform across mature endothelium and no selective response remains;
this would not exclude a general vascular function. **Home:** Nb2 vascular extension;
no existing A-series question is relabeled to claim ownership.

**Nb2 execution update:** At mouse day42, Fzd4 is prominent in CAP1/CAP2 and arterial/venous endothelium. This supports the broad-endothelial-identity rival; it does not isolate capillary progenitor function. Source labels remain CAP1/CAP2, with no inferred gCap functional identity. See the [bulk](trials/bulk_v1/REPORT.md), [atlas](trials/atlas_v1/REPORT.md) and [functional](FUNCTIONAL_SOURCE_AUDIT.md) reports.

### Nb2-N8 — Is a physiological canonical Fzd6 input present in a defined context?

**Origin:** owner's extra question; P1 Results p.7. **Hypothesis:** a context-dependent
endogenous input/co-receptor arrangement can engage Fzd6 in a canonical response.
**Rival:** canonical activation here depends on the synthetic agonist's arrangement,
while endogenous Fzd6 biology primarily uses other signaling outputs.
**Available now:** literature/resource and B3 expression-compatibility triage only.
**Discriminating test:** direct interaction/engagement evidence plus Fzd6-dependent
canonical and noncanonical response controls. **Against a nominated input:** absent
binding or receptor-dependent response under a valid assay; failure of one candidate
does not exclude all endogenous inputs. A database prediction, docking score or
coexpression is not ligand discovery. **Home:** Nb2 branch, lower execution priority.

**Nb2 execution update:** No direct endogenous ligand engagement measurement was recovered or generated. Atlas compatibility and synthetic Fzd6 sufficiency cannot nominate a verified physiological canonical ligand. See the [bulk](trials/bulk_v1/REPORT.md), [atlas](trials/atlas_v1/REPORT.md) and [functional](FUNCTIONAL_SOURCE_AUDIT.md) reports.

## Existing Nabhan bridge: Axin2, Il1r1, niche candidates, motifs and GO

Owner theme 3 outside the seven-item list asks whether Axin2-positive AT2 cells
form a distinct subset and how they relate to Il1r1-positive AT2 cells. Retain it
under [A4](../../RESEARCH_QUESTIONS.md#a4), the [existing transcript/co-detection
analyses](../gate1_02_choi_2020/axin2_il1r1/README.md) and [Nb1](../gate1_03_nabhan_2018/nb1/README.md).
Connect it to Nb2-N1/N3/N5 through receptor context; do not duplicate it as a new RQ.
Axin2 RNA, an Axin2 reporter and a stable lineage are different measurements.
Use GO on frozen, tested-gene universes as functional annotation; add motif analysis
only with appropriate ATAC/regulatory sequence backgrounds and state-linked samples.
Neither GO nor motif enrichment measures metabolic flux, TF occupancy or fate.
