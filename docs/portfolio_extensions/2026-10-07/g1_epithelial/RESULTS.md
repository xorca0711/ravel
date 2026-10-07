# G1 results and experimental bridge

7 October 2026. New contracts, entrypoints and synthetic tests were committed
at `95b0118f8374950baca6f74e9a459bebe312002b` before either numerical run.
Both use existing owners; no A ID, claim grade or human acceptance is created.
See [scope and prior evidence](AUDIT.md) and [primary-source review](LITERATURE.md).
The subsequent A11 regularization diagnostic was separately frozen at
`46af8e0c6ea9c658d5aba37545b4486917f038d9` after inspecting the first result and
before calculating any duplicate-feature controls.

## A17: founder, retained-clone and cell denominators differ substantially

The source-script no-switching model starts with 8% fast founders. At the
primary size>=2 threshold, that component remains a small share of retained
clones while contributing most expected retained cells by weeks 2–4.

| Week | Starting fast founders | Fast share of retained clones | Fast share of expected retained cells |
|---|---:|---:|---:|
| 1 | 8.00% | 9.03% | 45.99% |
| 2 | 8.00% | 8.25% | 87.74% |
| 4 | 8.00% | 8.24% | 95.01% |

This is a deterministic consequence of the **fixed source-script parameters**,
not an estimate of biological founder prevalence. The retained-clone and
expected-cell denominators answer different questions. Expected-cell shares
are ratios of expected contributions, not the expectation of a finite-sample
ratio or measured tissue proportions. No England clone outcome was fitted.

For each latent founder class, the retained size law is a zero-inflated
geometric distribution. With extinction probability `p0` and geometric ratio
`a`, retention at floor `k` is `(1-p0) a^(k-1)` and expected retained-cell
contribution is that retention times `k + a/(1-a)`. Mixing those quantities with
the fixed starting weights produces the two reported denominators. The tail
is infinite and retained analytically; it is not cut at an observed maximum.

All 36 parameter/time/floor combinations are retained in
[ascertainment.tsv](../../../../analysis/research/runs/g1_a17_ascertainment_v1/ascertainment.tsv).
At week 4, floor 2, the 0.16-founder sensitivity gives 16.44% of retained clones
and 97.66% of expected retained cells. Changing only the early slow net rate
from 0.9 to 1.1/week gives 8.14% and 92.70%; changing both gives 16.26% and
96.53%. These are separate transcribed parameter sensitivities, never selected
reproductions. For the primary source parameters at week 1, changing the size
floor from 1 to 5 changes the retained-clone fast fraction from 6.82% to 19.79%.
Thus the observation rule itself also changes what a reported class fraction
would mean.

Independent backward probability-generating-function coefficient ODEs verify
extinction, retention and truncated first moments at all frozen settings.
The maximum probability/relative-moment discrepancy is `4.7628e-12`, below the
`1e-7` numerical tolerance. The [verification](../../../../analysis/research/runs/g1_a17_ascertainment_v1/verification.json)
records every check; [receipt](../../../../analysis/research/runs/g1_a17_ascertainment_v1/receipt.json)
verification passed. This is numerical verification, not independent biology.

**Decision:** carry an explicit observation model and denominator into A17's
future comparison. Do not infer a large founder population from cell dominance
or a molecular cell type from a latent rate class. The full cohort comparison
still needs fixed fair model domains, switching-start assumptions, probability
and tail qualification, ascertainment sensitivities and recoverability under
the actual mouse schedule. Terminal cohorts cannot supply clone extinction or
longitudinal transitions without the missing founder/detection denominator.

## A11: lower log loss does not establish distinct residual information

The primary fixed-penalty model improves mean paired log loss from **0.226980
to 0.191987 nats** after adding the fixed lesion component, a gain of **0.034993**.
All eight held-out patients improve; individual gains range from 0.010038 to
0.069134. Both baseline and augmented models already order all eight pairs
correctly. The gain therefore reflects confidence/log loss, not additional
correctly ordered patients. Chance pair log loss is 0.693147.

| Fixed penalty | Added module | Baseline mean loss | Augmented mean loss | Mean gain | Patients improved |
|---|---|---:|---:|---:|---:|
| 1, primary | Lesion component | 0.226980 | 0.191987 | 0.034993 | 8/8 |
| 1 | Stress-excluded component | 0.226980 | 0.189412 | 0.037568 | 8/8 |
| 0.1 | Lesion component | 0.069540 | 0.055737 | 0.013803 | 8/8 |
| 0.1 | Stress-excluded component | 0.069540 | 0.056109 | 0.013431 | 8/8 |
| 10 | Lesion component | 0.524138 | 0.487476 | 0.036662 | 8/8 |
| 10 | Stress-excluded component | 0.524138 | 0.486190 | 0.037948 | 8/8 |

The raw reconstruction recovered the fixed 16 pseudobulks, 7,490 cells and
29,634 genes; every original full-library count total matches exactly. Gene
lists and populations were fixed. Each sample uses its own full-library
log2(CPM+1) scale, without all-patient TMM; only the seven training patients
determine feature scales and coefficients in a fold. This changes the original
score scale transparently, rather than treating the historical normalized
values as a clean holdout pipeline. Independent Newton and BFGS coefficients
agree within `7.0254e-9`.

[Every prediction](../../../../analysis/research/runs/g1_a11_paired_prediction_v1/heldout_predictions.tsv),
[all comparisons](../../../../analysis/research/runs/g1_a11_paired_prediction_v1/comparisons.tsv),
[verification](../../../../analysis/research/runs/g1_a11_paired_prediction_v1/verification.json)
and the verified [receipt](../../../../analysis/research/runs/g1_a11_paired_prediction_v1/receipt.json)
retain the run. Historical signed-rank outcomes, including beyond-shared
BH q=0.0547, remain unchanged because they concern a different estimand and
scale. The original injury-specificity limit also remains.

**The capacity diagnostic changes the interpretation.** At the primary penalty,
duplicating the existing p53 feature gives mean log loss **0.190882**, slightly
lower than **0.191987** with the lesion component. The duplicate adds no new
predictor information: it only changes the L2 penalty geometry. Its gain over
baseline is **0.036098**, versus **0.034993** for the lesion component. It also
has lower loss than the lesion model in five of eight held-out patients. This
demonstrates that a similar aggregate confidence gain can arise without a new
biological feature; the first model comparison therefore does **not** establish
distinct residual information beyond the fixed baseline.

All four controls and all penalties were fixed before their calculations:

| Penalty | Duplicated existing feature | Duplicate mean loss | Duplicate gain over baseline | Lesion gain over duplicate |
|---|---|---:|---:|---:|
| 1, primary | Shared remodelling | 0.222949 | 0.004031 | +0.030962 |
| 1, primary | p53 | 0.190882 | 0.036098 | -0.001105 |
| 1, primary | Hypoxia | 0.193235 | 0.033745 | +0.001248 |
| 1, primary | Inflammatory response | 0.217190 | 0.009790 | +0.025203 |
| 0.1 | Shared remodelling | 0.070663 | -0.001123 | +0.014926 |
| 0.1 | p53 | 0.052631 | 0.016909 | -0.003106 |
| 0.1 | Hypoxia | 0.056853 | 0.012687 | +0.001116 |
| 0.1 | Inflammatory response | 0.073853 | -0.004313 | +0.018117 |
| 10 | Shared remodelling | 0.510073 | 0.014065 | +0.022597 |
| 10 | p53 | 0.488344 | 0.035795 | +0.000868 |
| 10 | Hypoxia | 0.490583 | 0.033555 | +0.003107 |
| 10 | Inflammatory response | 0.500492 | 0.023646 | +0.013016 |

Positive final-column values favor the lesion model; negative values favor
the no-new-information duplicate. Penalty 1 remains primary. The lambda 10
and stress-excluded sensitivities are not selected to rescue a biological
reading. This does not prove the lesion genes are biologically uninformative
or that p53 is the causal explanation: duplicated features are a mathematical
control, and no formal equivalence test was performed.

The [capacity comparisons](../../../../analysis/research/runs/g1_a11_capacity_qualification_v1/capacity_comparisons.tsv)
and [96 control predictions](../../../../analysis/research/runs/g1_a11_capacity_qualification_v1/duplicate_predictions.tsv)
retain all results. The [independent verification](../../../../analysis/research/runs/g1_a11_capacity_qualification_v1/verification.json)
reconstructs all 72 original predictions and six aggregate gains from saved
scores/coefficients with standard-library arithmetic; maximum error is
`2.2205e-16`. Duplicate-model Newton/BFGS agreement is within `7.2809e-9`.
The [receipt](../../../../analysis/research/runs/g1_a11_capacity_qualification_v1/receipt.json)
passes verification. This diagnostic is an explicitly exposed amendment; the
[rationale](LITERATURE.md) and original positive outputs remain preserved.

Regardless of that diagnostic, Kim outcomes informed the choice to do this
follow-up. This is internal conditional reuse performance, not untouched
confirmation or validation of the historical feature-discovery pipeline.
Normal-AT2 versus author tumour-epithelial composition remains a consequential
alternative. No malignancy, future fate, mechanism, injury specificity or
clinical utility is established.

**Decision:** retain the original lesion association and this numerical
qualification, but do not promote a claim of distinct residual information.
Further model tuning on these same eight patients is not the next biological
experiment. A new independent comparison would need the population/endpoint
qualification below and a prospective model/control specification.

## Conditional experimental baseline

| Question family | Existing published baseline | Measurement needed to change the decision |
|---|---|---|
| A0 conservation | The frozen cross-tissue transfer failed; published common repair biology is a premise | Independent biological justification that the two transitions and their endpoints correspond before any reopening; conserved fate control would then require comparable functional perturbation endpoints. No replacement signature is authorized by the failure. |
| A1/A8/A14 competence and recovery | Transitional states and withdrawal-associated recovery already have primary precedents | A named early feature, the same independent lineage/preparation units and later absolute mature-descendant output; verify cessation and separate survival/total yield. A1 additionally needs the nominated non-RNA regulatory measurement. |
| A7 state dependence | CEBPA-dependent AT2 identity is published | Pre-intervention states and independent genotype preparations; estimate broad identity effect and additional state interaction separately, with viability measured. |
| A10 growth | Screen imaging and RNA associations are established measurements | Earlier predictor and later viable growth in identified independent preparations; separate formation, area, cell number and survival. |
| A11 residual utility | HPCS function and regeneration overlap are published; original lesion association stands | Independent patient cohort with comparable epithelial populations and a qualified non-neoplastic-injury arm before cancer-specific utility; a functional mediator is not nominated by classification. |
| A13/A22 reciprocal niche | Published epithelial–fibroblast and NKX2-1/chemokine RNA relations | A nominated extracellular product and calibrated collection/recovery, viable source amount, recipient state/survival and separate functional readout. Reverse-direction induction is not evidence of feedback. |
| A16 marker | Published mutant heterogeneity plus attenuated corrected RNA contrast | Epithelial-localized specific CD177 protein and one linked later response within comparable baseline cells; a perturbation would ask a distinct causal question. |
| A17 clones | Source clonal tracing and model premise | Founder/clone ascertainment and reliable lineage identity over time, or an explicit cross-sectional observation model; counts, loss, merger and growth must not be conflated. |
| A23 homeostasis | SLC34A2/phosphate repair effects and transitional RNA module are published | Direct transport, relevant phosphate compartment and linked acquisition/exit, division and loss; endpoint occupancy alone cannot distinguish entry from residence. |

These are fit-for-purpose requirements, not unqualified experimental protocols.
Host model access, validated assays, meaningful effects, independent-unit
variance and sample-size justification remain unconfirmed. A qualified
mutant/control contrast can estimate its stated genotype effect; an extra arm
is warranted only by the intended inference. No adverse prior result is erased.
