# A19 results: context constraints on temporal control

**30 September 2026 · exploratory_v1 · secondary analysis of public source data.**
[Figures and captions](FIGURES.md) · [Methods and reproduction](METHODS.md) ·
[Source eligibility](SOURCES.md) · [Original biological plan](PLAN.md).

## Biological conclusion

The new analysis narrows A19 toward **context-dependent release of alveolar
maturation**. Removing a growth-maintenance input cannot be assumed to produce
mature AT1 cells: human alveolar-derived organoids without CHIR show stronger
airway-marker expression in qPCR, whereas bulk RNA exhibits a mixture of
AT1-associated and airway changes. In airway-derived cultures, an early SFTPC
increase diminishes despite continued CHIR. These observations distinguish
induction of an alveolar marker from sustained alveolar competence.

This is supporting RNA evidence from a GSK3 inhibitor context. It neither tests
receptor-selective Fzd withdrawal nor measures lineage-derived mature output,
AT2 reserve, or response to a later bout. **H1–H3 remain unresolved; no claim
grade or acceptance decision changes.** Existing Nb2 results were not rerun or
counted as independent validation.

## CHIR absence redirects the marker balance in alveolar-derived organoids

Source Fig. 4b contains three matched donor lines, D2, D5 and D7, derived from
HTII-280-positive human cells. With CHIR absent, SFTPC decreases in every line;
FOXJ1, TP63 and SCGB1A1 increase in every line. The mean effects below are
comparison minus reference on the negative-DeltaCt scale; positive values
indicate higher normalized expression. These are exact donor-paired contrasts,
not the publication's original fold-scale tests. [Figure 1](FIGURES.md#figure-1)
shows all observations from the [source workbook](SOURCES.md).

| Marker | Mean log2 change, absent − present | Conditional 95% t interval | Pairs |
|---|---:|---:|---:|
| SFTPC | −3.89 | −12.35 to +4.57 | 3 |
| FOXJ1 | +3.41 | −3.33 to +10.16 | 3 |
| TP63 | +1.66 | −0.05 to +3.37 | 3 |
| SCGB1A1 | +5.83 | +3.05 to +8.60 | 3 |

The pattern is consistent with loss of alveolar identity or enrichment of
airway-like populations in this culture environment. It does not distinguish
conversion of individual cells from selective growth or survival. Most intervals
are wide. An AT2 marker decrease is not, by itself, evidence of AT1 maturation.
The experiment contrasts media conditions; it is not a verified Fzd on/off series.

## Initial origin constrains interpretation of transient alveolar-marker induction

In source Fig. 6a, **airway-derived pooled organoid cultures**, coded D3, D5 and
D7, show a mean SFTPC increase of +6.77 log2 units at passage 1 with CHIR
versus without it (95% interval +1.79 to +11.75). Between passages 1 and 3 under
continued CHIR, SFTPC falls in all three source lines: mean −4.65 (−7.42 to −1.89).
[Figure 2A](FIGURES.md#figure-2) connects source codes, not individual cells.

Thus early marker induction can be transient in a lineage context that does not
maintain an alveolar phenotype. This motivates H2's competence question, but
comparing separate source figures cannot identify a treatment-by-initial-state
interaction. Passage-dependent selection is a biological rival to loss of
identity within cells.

Source Fig. 6c supplies an additional passage series, with changing donor labels
across some genes. Only D21 provides a quantified SFTPC P3–P1 pair (−5.79);
P5 SFTPC values are all reported as undetected. We do not replace those values
with zero or treat row position as donor matching. Other markers retain two or
three pairs. [Supplementary Figure 1](FIGURES.md#supplementary-figure-1) makes
that evidence boundary visible; it is not a second three-donor SFTPC trajectory.

## Genetic and pharmacological input contexts do not yield a uniform RNA response

For source Fig. 5c, three paired alveolar-derived donor lines under CHIR show
lower GSK3B RNA after knockdown (mean −2.70 log2 units; interval −3.58 to −1.82).
TP63 and KRT5 decrease by −4.09 and −3.65, respectively. SFTPC is heterogeneous,
with a mean near zero (−0.03; interval −5.24 to +5.18), rather than a precise
unchanged effect. All seven nominated outcomes are retained in [Figure 2B](FIGURES.md#figure-2)
and the [complete summary](tables/exploratory_v1/qpcr_effect_summary.tsv).

This separates reduction of GSK3B RNA from a uniform shift of every identity
marker. It does not prove an off-target mechanism for CHIR: residual protein,
GSK3A activity, exposure history and other network responses remain unresolved.
There is no Fzd comparator or calibrated engagement range, so H3 is not tested.

## Bulk RNA shows mixed differentiation-associated responses

Eight uninfected alveolar-organoid libraries in [GSE197949](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE197949)
form two source blocks with control/knockdown backgrounds and CHIR present/absent.
The paper describes two donor cultures; GEO does not map those donors explicitly,
and the knockdown hairpin changes with block. We report each block separately,
without population tests. Of 60,662 annotated count rows, 14,581 pass the frozen
filter. Scores are unweighted means of log2(TMM CPM + 1) for eligible marker panels.

| RNA panel | Control B1 | Control B2 | Knockdown B1 | Knockdown B2 |
|---|---:|---:|---:|---:|
| AT2 identity | −0.15 | −0.02 | −0.36 | +0.79 |
| AT1-associated | +0.88 | +1.35 | +2.28 | +2.54 |
| Airway differentiation | +0.49 | +0.61 | +0.94 | +0.05 |
| Canonical Wnt targets | −0.90 | −0.40 | −3.64 | −5.18 |
| Proliferation | −0.61 | −0.27 | −0.77 | −0.27 |

Values are CHIR-absent minus CHIR-present score differences, not cell fractions
or measured pathway activities. [Figure 3](FIGURES.md#figure-3) displays these
results and every AT1-panel gene. AGER, HOPX and CLIC5 rise in both backgrounds
and blocks, while PDPN and RTKN2 include opposing directions. The basal panel
fails its coverage rule (1/4 genes), so no basal score is reported; the airway
panel passes with 2/3 genes. Total-count normalization changes the sign of one
of 20 program effects: control-block-2 AT2 identity, −0.018 to +0.063. The main
AT1, airway, Wnt-target and proliferation directions are unchanged.

A material discordance remains: control-background bulk SFTPC changes are
+0.21 and +2.62, whereas all three qPCR effects are negative. The preparations
and normalization differ; the datasets cannot be pooled into one estimate or
used to declare universal loss of AT2 identity. Neither assay measures mature
barrier function. Reduced cycling-associated RNA and higher AT1-associated RNA
are compatible with differentiation, but also with shifts in population mixture.

The four qPCR target assays are also nonuniform: LEF1 falls in all four donor
lines (mean −1.47), AXIN2 is mixed (−0.05), source-labelled TCF4 increases
(+1.11), and TGFB1 increases (+1.73). TCF4 is retained as the source assay name,
not assigned to TCF7L2. These outcomes do not establish a direct Wnt activity
trajectory or Hippo/YAP mediation.

## Hypothesis refinement and discriminating biological outcomes

This refinement is **post-analysis**. The original H1–H3 and their functional
requirements remain in force; the executed CHIR context results do not validate
a Fzd schedule or identify a causal state interaction. The focused extension asks:

> Does acquisition of an airway-associated state during expansion limit subsequent
> AT1 maturation after Fzd stimulation ends, under a specified maturation environment?

The proposed mechanism is competition between alveolar retention and an acquired
basal/airway programme. Such a programme may reduce later mature alveolar output,
but the restriction need not be irreversible. Missing differentiation cues,
selective population growth/survival and input-dependent plasticity are competing
explanations. States must be defined before the relevant withdrawal decision,
independently of the later functional outcome; an RNA score cannot define
"competence" merely by recapitulating the endpoint.

[The extension pipeline](EXTENSION_PIPELINE.md) incorporates the three priorities
into these existing hypotheses. [The external evidence review](EXTERNAL_EVIDENCE.md)
adds published support and counterconstraints, not new A19 numerical results.

| Existing hypothesis | What the current analysis contributes | Extension priority and discriminating biological outcome |
|---|---|---|
| H1: temporal separation with preserved reserve | CHIR absence produces mixed identity responses; no traced output or reserve endpoint | **P1** describes the cells underlying mixed expression; **P3** requires withdrawal versus continuation with absolute mature AT1 descendants and retained AT2 responsiveness. Precise failure of useful gain or reserve preservation weakens the combined claim |
| H2: initial-state competence | Separate source origins motivate a context constraint, without an identified state-by-schedule interaction | **P1** provides descriptive origin/culture-context evidence; **P3** tests schedule response across independently measured pre-exposure states. Precise equivalence or a contrary interaction weakens the nominated state effect |
| H2-extension: acquired pre-withdrawal state | Transient SFTPC induction and airway-associated responses motivate possible fate competition | **P1** distinguishes separate populations from mixed cellular identity; **P3** needs common expansion, a state measured before withdrawal assignment, and later AT1/airway output. A precise absence or reversal of the predicted state-dependent withdrawal benefit weakens this extension |
| H3: input-dependent regulation | GSK3B knockdown and CHIR contexts show nonuniform RNA responses | **P2** presents existing background-by-CHIR differences without a new discovery claim; **P3** requires independently calibrated Fzd/comparator inputs linked to later fate/function. RNA-only effects cannot establish H3 |

Pre-exposure state (S0), acquired pre-withdrawal state (S1) and later fate (Y)
are separate variables. If the complete schedule was assigned before S1 arose,
S1 may be a mediator and cannot be treated as a baseline cause or adjusted out
of H1. Even a valid state-dependent withdrawal effect does not by itself prove
that state acquisition causes loss of capacity. The pipeline preserves that
causal distinction and keeps H1's AT2-reserve requirement.

The next work is ordered by scientific priority: **P1 cellular-state analysis**,
**P2 bounded synthesis of existing input-context contrasts**, and **P3 linked
functional-data inventory and conditional testing**. P3 inventory can start
without waiting for favorable P1/P2 results. No extension figures or functional
results are claimed here before execution; all existing exploratory_v1 values
and four figures remain unchanged.

The [eligibility inventory](SOURCES.md) also identifies a rat engineered-lung
study in which CHIR and KGF were removed together. Its reported modest
AEC1 differentiation response motivates the need for additional maturation cues,
but the combined intervention cannot isolate Wnt and its individual Fig. 6
values were not recovered here. The iPSC study's maturation endpoint concerns
AT2 maturation, which must not be substituted for AT1 production. Both remain
published context, not new quantitative replications.

The next decisive analysis requires linked starting-state, engagement, lineage,
absolute mature-output and reserve evidence in the same independent units.
Survival and differential expansion must distinguish true transitions from
selection. Functional maturation, competence and reserve remain the biological
outcomes; assay concordance is a supporting check.
