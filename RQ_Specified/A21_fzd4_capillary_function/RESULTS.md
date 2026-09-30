# A21 results: vascular context versus regenerative entry

30 September 2026 · exploratory_v1.
[Figures](FIGURES.md) · [Methods](METHODS.md) · [Source eligibility](SOURCES.md).

**The independent dataset supports a gCap expression context for Fzd4, but does
not support a consistent high-Fzd4/cycling association.** No inspected dataset
directly tests Fzd4-dependent capillary descendant production. Vascular stability
remains a concrete competing mechanism.

## 1. Existing cohort identities are resolved, not statistically disentangled

The [eight day-42 records](tables/prior_day42_cohort.tsv) have matching round,
label cohort, reporter genotype and sex. Each of four label cohorts appears once
in each round. Three of four animals in the first round are reporter homozygotes;
all four in the second are heterozygotes. Sex also differs across rounds.
Those reporter genotypes do not manipulate Fzd4.

The original Fzd4-cycling coefficients remain +0.738 pooled, -0.400 in round 1
and +1.000 in round 2 (four animals per round). No saturated adjustment resolves
that design. The pooled coefficient is retired as affirmative support for
renewal; the historical result is preserved. Resolving identifiers does not
create replication or prove that a particular covariate caused the association.

## 2. Independent gCap enrichment recurs with limited injury coverage

GSE211335 contributes 12 animals and 5,423 endothelial cells from a different
injury model. Independent identity markers agree with the gCap/aerocyte crosswalk
in all seven primary eligible pairs: Aplnr/Gpihbp1/Cd93/Kit are higher in gCap,
and Car4/Ednrb/Apln/Fibin higher in aerocytes.

| Condition | Eligible animal pairs | Mean Fzd4 gCap minus aerocyte | Direction |
|---|---:|---:|---|
| Control | 3 | +0.984 | 3/3 positive |
| Day 3 | 1 | +0.500 | 1/1 positive |
| Day 5 | 1 | +0.105 | 1/1 positive |
| Day 7 | 2 | +1.194 | 2/2 positive |

Values are differences in log2(CPM+1), not literal log2 fold changes.
At the 10-cell floor, 10 pairs qualify and the two day-5 pairs have opposite
directions. At 50 cells, only four pairs qualify, with none at day 5.
The baseline comparison is descriptively replicated in three animals; injury
comparisons are coverage-limited. Broad endothelial expression is compatible
with a receptor role but does not establish gCap-selective function.

## 3. Transitional gCap has less Fzd4 RNA than major gCap

In all 11 primary eligible animal pairs, author transitional state 1 has lower
Fzd4 RNA than major state 0. Mean differences are -0.466, -1.525, -0.421 and
-1.034 for control/day-3/day-5/day-7, respectively. This direction persists at
both fixed alternative floors. Cycling-panel RNA is higher in the transitional
state in control/day 3/day 7, but lower in both eligible day-5 pairs.

The result separates receptor abundance from cycling-associated context.
It does not establish a temporal Fzd4 decrease, prove that these cells are
ancestors/descendants, or show that low receptor expression means dispensability.
A transient earlier response or altered signaling per receptor remains possible.

The dedicated cycling state 7 never reaches 20 cells in any animal. At the
10-cell sensitivity floor, only one day-5 comparison qualifies. Its negative
Fzd4 difference is retained as a single comparison, not a replicated state result.

## 4. The within-condition association is inconsistent

| Condition | Aggregate gCap rho (n) | Major gCap state 0 rho (n) |
|---|---:|---:|
| Control | -1.00 (3) | -0.50 (3) |
| Day 3 | -1.00 (3) | +1.00 (3) |
| Day 5 | +0.50 (3) | Unavailable (2) |
| Day 7 | -1.00 (3) | -1.00 (3) |

These are three-animal rank summaries with coarse possible values.
They establish neither a population anticorrelation nor a reliable positive
replication. No pooled across-day value was used to rescue the original lead.
Changing cell floors is sensitivity analysis, not additional biological replication.

## 5. Functional literature separates what remains plausible

Gillich supplies capillary lineage rationale without a Fzd4 perturbation.
Bian supplies FZD4 restoration effects on pathway/vascular-structure outcomes
in a Foxf1-deficient tumor setting, without normal gCap fate tracing.
Neither transfers its result into the missing adult-repair receptor-by-lineage
test. The [source audit](SOURCES.md) retains the precise compartments and endpoints.

## Hypothesis refinement and discriminating biological outcomes

The original primary endpoint remains **traced gCap renewal and aerocyte
descendant output per initial viable labelled population**, assessed separately.

A plausible refined mechanism is that **Fzd4 sustains endothelial competence
that permits later capillary repopulation**, without requiring high receptor
RNA in the cycling/transitional state. This is a proposed maintenance-mediated
route to repair, not an accepted explanation. Selective regenerative entry
remains a competing receptor-dependent route.

| Valid perturbation outcome | Biological interpretation |
|---|---|
| Early vascular competence is impaired, followed by lower traced descendant output | Compatible with a maintenance-mediated contribution; order alone does not prove mediation |
| Maintenance is independently preserved/characterized but traced renewal is selectively reduced | Favors a renewal-specific receptor effect |
| Vascular performance changes while useful descendant output is preserved | Supports a maintenance role without the proposed renewal consequence |
| A precise absence or reverse of a useful lineage effect under valid engagement | Weakens the nominated renewal prediction |
| Only RNA/cycling changes, sparse lineage data or failed engagement | Inconclusive for receptor-dependent renewal |

Keep viability, absolute endothelial abundance, barrier/perfusion and lineage
output separate. Post-treatment survival adjustment is not a mechanistic test.
A lung-wide intervention also needs compartment attribution because epithelial
FZD4 effects exist in other settings.

## Execution decision

Stage 0 cohort/crosswalk/context work is complete. The high-Fzd4 renewal-marker
lead is not retained as affirmative mechanistic evidence. A21 remains conditional
and biologically untested, with vascular competence versus selective lineage
production as the useful functional distinction.

Next execution requires an eligible Fzd4 perturbation source with initial gCap
identity, independent animals, engagement, traced descendants and maintenance
outcomes. No such joined dataset was identified in this audit. Additional pooled
correlations or pseudotime fits in these same data would not resolve that gap.

The denominator amendment does not change this conclusion: all 648 mean contrast
directions agree under the fixed sensitivity. Source state/lineage limitations
remain even where arithmetic is robust. Prior A19/A20 scientific evidence is
preserved; no claim grade or biological acceptance has changed.

## Subsequent extension, 30 September 2026

The [priorities 1-3 extension](extensions/extension_v1/RESULTS.md) supersedes the
source-access limitation recorded in the original audit: Bian Figure 3 and Figure 7
workbooks are now retrieved. Their descriptive reconstruction supports structural
restoration in tumor vessels, with no Fzd4-rescue perfusion or normal gCap lineage
measurement. The all-ten-Fzd comparison finds no robust alternative-receptor
nominee. New Foxf1 extraction is lower in all 11 primary state pairs. The original
results above remain unchanged; the focused functional hypothesis remains untested.
