# A8/A9 runtime and exact-design preparation v1

3 November 2026. Current results read first: A8 panel_attribution_v1 and A9 receptor_context_v1. Outcomes are exposed. No new sampling, co-detection or pseudobulk endpoint was calculated in this preparation; A9 feasibility used only donor/disease/label/library metadata. Await coordinator design review before numerical freeze/run.

## A8 proposed bounded computation

Retain all 35 original units, full 1,503-gene category order/residual, 2,000-count budget, original depth/airway filters and original two-marker/reference definitions. All five original raw objects remain available in the task-owned X: execution checkout. Reuse their original hashes and readers; never replay archived main/output writers. Compact saved draws alone cannot generate new realizations.

Propose exactly 32 new predeclared seeds 7001 through 7032. The original seeds 17 and 29 are immutable landmarks, not extra independent animals. Primary estimand is the original joint draw: groups and panel scores from the same new draw. Two separately labeled diagnostics fix group membership to landmark 17 or 29 while scoring panel counts from each new draw. This separates distributions conditional on a chosen assignment; variance differences are not an additive or causal decomposition of group-selection noise. Both landmarks are retained, so no favorable reference is chosen.

For each original unit and each new seed save all seven member contributions, early/late totals, group counts and original >=30-cell/coverage>=0.8 disposition. Fixed-group diagnostics retain the original landmark support disposition, including the failed 7-week-control seed-29 gate. Save cell-level counts of membership in each group across the 32 draws and agreement with each landmark. Report support frequency and contribution/sign distributions only within units; pooled libraries and external animals stay separate. Sign summaries conditional on supported draws show the actual denominator; unsupported draws never become successful observations.

Computational precision target: 32 independent RNG seeds give a worst-case Monte Carlo standard error <=0.5/sqrt(32)=0.0884 for an unconditional per-unit support or sign indicator. This is a modest computational precision target, not a biological margin. Conditional sign probabilities with fewer supported draws have a larger declared Monte Carlo error; do not append draws to improve an inconvenient result. No population intervals, seed-based biological n or relaxed cell floor.

Maximum work: 32 new joint draws per original unit, plus reconstruction of the two landmarks for parity. The previous complete two-draw job took 212.20 seconds including reading/output. A conservative linear upper projection for 32 new draws is about 57 minutes; it is not a benchmark because shared input costs dominate part of that time. Set a 60-minute wall-clock numerical budget and retain partial outputs with explicit incomplete status if it is reached, without changing the design or claiming a completed receipt. Process units sequentially and aggregate membership counts; do not save every full 1,503-gene draw. No package install or paid compute. Root should review this cost/precision tradeoff before freeze.

## A9 proposed fixed pair and depth design

Use only the original 4,648-cell, 22-donor primitives and fixed six genes. Primary same-cell questions: EGFR–ERRFI1 and EGFR–LRIG1. The three fixed family/context companions EGFR–ERBB2, EGFR–ERBB3 and EGFR–ERBB4 are reported separately; the latter two are not designated direct AREG receptors. No new score or ligand refit.

Use the same explicit common-support construction as A31: primary floor(log2(library)/0.5), coarse sensitivity width 1.0, >=5 cells per label/bin; retain the A9 original >=10-cell recipient floor and require >=10 retained cells per label. Both labels receive the same normalized min(label-count) bin weights. Preserve all 22 donor pairs and all five target pairs at both widths, including unsupported rows. Paired contrast is Myofibroblast minus Fibroblast for observed, expected and residual co-detection; both marginals remain visible. Residuals depend on marginal prevalence and do not demonstrate effective inhibition or independence.

Metadata feasibility: 19 original paired donors (17 IPF, 2 Control) qualify before depth restriction. Primary shared-depth support retains 14 (12 IPF, 2 Control); coarse sensitivity retains 17 (15 IPF, 2 Control). See A9_DEPTH_FEASIBILITY_V1.tsv. Keep disease labels attached to donor summaries, but do not fit a disease interaction or interpret a two-control comparison as a transported disease effect. The original four Control donors include two that already fail subtype support. Coarse-only results cannot rescue primary holds.

Prespecified normalization context: report all six raw-count pseudobulk sums/full-library sums and log2(1+CPM) alongside the original mean-cell natural log1p(CP10k), clearly as different estimands with different scales. Use separate labels/axes and paired directions; no pooled correlation, predictive refit or interchangeable effect-size assertion. Preserve the old 7/22 encoded-complex failure. This compact job needs only existing Python/pandas/numpy/plotting, with no matrix recovery; bounded work is 22 donors by five pairs by two widths.

## Ownership

Root has taken A12_SOURCE_INTAKE.md and any A12 source/numerical qualification. Technical will not duplicate that scan. A3/DY1 and A27 bounded source intake remain with technical. Root maintains PROGRESS; this note and the technical ledger record only this chat's preparation.
