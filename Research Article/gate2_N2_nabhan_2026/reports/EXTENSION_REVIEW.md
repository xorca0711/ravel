# Nb3 extension review: first descriptive pass

**1 October 2026.** The eight annotated questions have executable outputs or a
named eligibility hold. E1 and E8 share one analysis. This pass uses the source
screen and its deposited component tables; it is not independent validation of
the paper and does not establish a molecular or clinical mechanism.

**Source-consistency hold:** the human S5 numeric contrasts fail source
concordance and disagree with the table's own up/down lists. The computations
below come from deposited counts and retain their verified inputs; they must
not be described as recovered human S5 results. The
[concordance audit](CONCORDANCE_AUDIT.md) records the discrepancy without changing
source labels or refitting endpoints.

The paired RNA set contains **771 wells**. Four NKX21 wells are compared with
30 mouse and 27 human in-plate TIGIT/tdTomato reference libraries. These are
technical wells with unresolved independent preparations. The complete
[panel-effect table](../runs/R4_v1/fixed_panel_effects.tsv) contains 4,221 planned
contrasts, of which 4,150 meet the declared design floors. CSF3R is not estimable
in mouse; BAP1, CSF3R, ETV5, IRX1, MAPK3 and MEGF6 are not estimable in human.

Panel effects below are differences in mean **log2(TMM CPM + 0.5)** across fixed
source markers. They are not gene-level log-fold changes, complete pathway
activities or cell fractions. Intervals are unadjusted technical-well intervals,
not independent-preparation confidence intervals. All required panel genes were
present; gene-level DE eligibility is a separate check.

## E1 and E8: identity, chemokines and wound-associated expression

| NKX21-associated panel | Effect | Technical 95% interval |
|---|---:|---:|
| Mouse AT2 markers | −2.072 | −2.315 to −1.828 |
| Mouse gastric markers | +7.341 | +6.570 to +8.112 |
| Human chemokine markers | −3.357 | −3.961 to −2.753 |
| Human wound markers | +1.468 | +1.114 to +1.821 |
| Human PLIN2 sentinel | −1.456 | −1.796 to −1.117 |
| Human mitochondrial ND markers | −1.012 | −1.472 to −0.552 |

The source contrast combines decreased epithelial AT2 markers with lower
fibroblast chemokine expression and higher wound-associated expression. This
supports prioritizing the **selectivity of the fibroblast response**. It does
not show that all fibroblast activity is suppressed, nor directly measure immune
recruitment, immune activation, tissue specificity or immunotherapy response.

Across 195 eligible targets, AT2-marker and fibroblast-chemokine contrasts have
Spearman rho **0.182**, or **0.221** after the declared linear growth-residual
diagnostic. Removing NKX21 gives **0.169**. Coverage versus chemokine effects has
rho **0.059** (without NKX21, **0.076**). The broad cross-target relationship is
therefore modest; the prominent NKX21 phenotype does not establish a general
identity effect independent of growth. Conditioning on growth is not mediation.

Depth remains relevant. Among 99 paired reference wells, mouse AT2 scores
correlate with human read depth at rho **0.234** (plate-residual rho **0.441**),
and human PLIN2 with mouse read depth at **0.411** (**0.451** after plate residuals).
These diagnostics prevent treating paired RNA scores as independent measurements
of cell abundance or lineage identity. No extra QC exclusions were selected
after inspecting these correlations.

Evidence: [target associations](../runs/extensions_v1/target_associations.tsv),
[leave-target-out checks](../runs/extensions_v1/leave_target_out.tsv),
[paired depth diagnostics](../runs/extensions_v1/paired_depth_diagnostics.tsv).
The next causal question needs independent biological units and an immune
outcome; lung specificity additionally needs relevant tissue comparators.

## E2: distinguish expression patterns before assigning fate

NKX21 has transition **+2.378**, interferon **−3.577**, hypoxia **+1.631** and
gastric **+7.341** panel effects. CSNK2A1 instead has interferon **+2.288** and
hypoxia **−0.680**; BECN1 has hypoxia **+2.393** with interferon **+0.430**.
These fixed panels distinguish source-associated bulk expression patterns.
They do not demonstrate two trajectories, normal versus aberrant fate, or
reversible versus persistent repair states within a matched cell population.

Deposited ICA13 has strong positive projections for the five IFN markers;
ICA5 has strong positive projections for the three transition markers. Component
activities and gene projections are kept separate. No new cPCA, JADE fit,
pseudotime or donor-level state comparison is claimed. The Reyfman source cohort
is identified, but its exact author PCA/AT2 annotations still need recovery;
see [context eligibility](CONTEXT_ELIGIBILITY.md).

## E3: ELOVL1/ATP6V0E pattern comparison

| Target | Wnt marker effect (technical interval) | AT1 marker effect (technical interval) |
|---|---:|---:|
| ELOVL1 | +0.920 (−0.012 to +1.853) | −0.767 (−1.200 to −0.333) |
| ATP6V0E | +0.679 (−0.248 to +1.606) | −1.013 (−1.415 to −0.611) |
| FZD5, nominated opposite-direction comparator | +0.240 (−1.104 to +1.584) | +0.267 (−0.247 to +0.780) |

CTNNB1-active has a larger Wnt-panel effect (**+2.637**); PORCN has **−0.885**.
The ELOVL1/ATP6V0E results are compatible with a shared AT1-marker decrease,
but their Wnt-panel intervals are broad and the nominated FZD5 comparator does
not supply a clear opposite pattern under this summary. A ranking of molecular
mechanisms is not supported. The source ICA17 activity signs must be interpreted
together with signed projections; a negative component score does not itself
mean pathway inhibition.

Both published S3 budding contrasts were recovered for the fixed markers in
[source_budding_markers.tsv](../runs/R3_v1/source_budding_markers.tsv). Those are
the authors' statistics. Original image embeddings and morphology assignments
were not regenerated. Wnt/AT1 panels are exactly the displayed Fig. S7 marker
lists; only two of the five Wnt markers appear in the source S7 ICA gene universe,
so a projection average over those two is not a complete Wnt programme.

## E4: SLC34A2 has a transition-associated pattern without broad AT2 loss here

SLC34A2 has transition **+0.524** (technical interval **+0.331 to +0.716**),
AT2 **−0.110** (**−0.277 to +0.057**) and AT1 **+0.062** (**−0.168 to +0.293**).
Its deposited ICA5 activity is **+0.837**. Day-14 coverage is **−0.140** plate SD
units. This is narrower than an NKX21-like loss of AT2 identity. The targeted
Slc34a2 gene is absent from these marker panels, avoiding self-scoring of the
perturbed transcript. Phosphate transport and human fibrosis mechanisms remain
unidentified by this screen.

## E5 and E6: receptor detection and recipient ambiguity

The [receptor-expression table](../runs/extensions_v1/receptor_expression.tsv)
finds Egfr/Erbb2/Erbb3 in the mouse epithelial compartment and EGFR/ERBB2 in
human fibroblasts. EGFR is detectable in both compartments: median control
TMM CPM is **3.452** in mouse and **65.178** in human, with positive counts in
**87.4%** and **100%** of reference libraries, respectively. These are separately
normalized species libraries; their CPM values are not a cross-species
quantification of receptor abundance. The mouse compartment also does not
separate AT2 from AT1 cells.

ERBB2/ERBB3 targets reduce day-14 coverage (**−1.393/−2.331** plate SD units);
EGFR has a small source-screen effect (**+0.098**). This does not establish EGFR
dispensability or identify which compartment accounts for the medium's EGF
requirement. RNA detection/depletion is not validated receptor protein loss.
The existing A2/P1 evidence limitations still apply; A2 was not refitted.

The DepMap release, assay, lineage selection and 93-versus-96 denominator remain
unresolved. No cancer-dependency model, normal AT1 requirement, AT2-origin claim
or drug-induced fibrosis conclusion is drawn. Those are separate evidence needs.

## E7: bulk programme response is available; heterogeneity is not

Paired fibroblast-marker effects and their growth associations were computed,
with both-compartment depth checks. A change in a well's average expression
cannot distinguish altered fibroblast states, proportions or total cell number.
Single-cell/spatial heterogeneity and local paracrine geography remain held
until the relevant sample identities, cell labels and spatial design are eligible.

## Decision after this pass

Prioritize E1/E8's selective chemokine-versus-wound phenotype and E2's contrasting
expression patterns for source-exact and independent-context work. Keep E3's
uncertain Wnt comparator and E4's limited AT2 shift visible. Receptor expression
supports the relevance of E5/E6 but does not resolve function. E7 requires
different measurement resolution. No research-question grade or registered
scientific claim was upgraded by this pass.

The [execution record](../runs/extensions_v1/run_record.json),
[focal panels](../runs/extensions_v1/focal_target_panels.tsv),
[source ICA values](../runs/extensions_v1/focal_source_ICA.tsv) and
[figures](../FIGURES.md) provide the underlying evidence. Full gene-level DE and
its source comparison are reviewed separately in the
[reproduction review](REPRODUCTION_REVIEW.md).
