# A5 destination-feature screen v1

3 November 2026; exposed exploratory reference-state comparison, not fate tracing.
[PS1 rationale](../../docs/research_reviews/2026-11-03-primary-candidate-literature/ANALYSIS_PLAN_V1.md).

Question: do literature-named KLF/identity RNA features in existing repair states
align uniformly with an alveolar or secretory-airway reference? Strunz's existing
Guo result is a premise, not recomputed or replaced. The main threat is that
cross-sectional state labels, selection and time mixture are mistaken for future
destination. No association can establish ancestry, HIF activity or repair function.

Sources read before outcomes: Dong 2025 [primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7618356/),
Fig. 1E (KRT5/TP63 and SCGB1A1/SCGB3A2), Fig. 6 (KLF4/KLF5), Fig. 7A/F
(SFTPC, LAMP3, TP63, KRT17); Strunz 2020 [primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7366678/),
Fig. 7e/8b (Ager), Fig. 8g and adjoining Results (Hopx), original Krt8+ ADI.
Exact mouse symbols are listed in the JSON: human TP63 maps to mouse Trp63;
this is a named-gene panel, not a regulon, fate score or whole human programme.
Dong human hypoxia and Liu bronchiolar repair motivate alternative interpretations;
this mouse bleomycin comparison does not reproduce either intervention.

All input bytes match original deposited hashes. Original sample_id = mouse,
32 deposited samples; NC controls excluded; day 2-21 retained. Keep raw >=500 UMI
and >=30 cells per mouse/state, and >=3 mice per reported contrast. Basal has at
most 14 cells per mouse even before depth; its absent support is reported, never
rescued by pooling. Primary ADI minus activated AT2 uses its supported mice.
AT1 minus ADI and Club minus ADI use the SAME three-state common-support mice.
Their estimates must not be directly subtracted from the different-support primary.
Report all support, per-mouse values, sampling times and named-gene outcomes.

Endpoint: expected detection probability after sampling 500 raw UMI without
replacement, averaged over cells within each mouse/state, expressed in percentage
points. Equal-mouse paired differences; pointwise descriptive 95% t intervals
if >=3 mice, equal-day means, and per-day means retained. No p-values, selected
significance claim, equivalence margin, multigene score, batch correction,
pseudotime, causal direction or cell-as-replicate uncertainty. Intervals are not
simultaneous and apply only to the selected sampling schedule.

Verify count/barcode cardinality, matrix orientation/integrality, unit/day mapping,
complete feature coverage and rarefaction arithmetic against exact combination
probabilities. Stop for a failed input/hash/join or missing named feature. Preserve
all zero/opposite results. Rendering occurs in the same governed run. Frozen Guo
modules, prior counts, old outputs and held GSE303646 replication remain intact.

Review clarification before execution: this 12-gene panel is not the fixed Guo
component. Its reference-state pattern cannot identify a driver or explain the
positive Guo recruitment result without separate membership/relationship evidence.
