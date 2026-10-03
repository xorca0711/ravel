# Nb5 biological extensions stage 1 results

3 October 2026. **Two biologically focused exploratory comparisons completed.**
Lung and bladder show different relationships between within-type RNA and
captured composition. T-cell clone repetition differs among immune tissues,
and older local-clone burden remains higher under fixed tissue representation
in a small balanced mouse subset. These observations refine biological
alternatives; they do not establish a mechanism, function or a new global RQ.

[New figures 7–10](EXTENSION_FIGURES.md) · [Four-page PDF](../../analysis/research/runs/nb5_biological_figures_v1/nb5_biological_extensions.pdf) ·
[Frozen stage design](EXTENSION_STAGE1.md) · [Prior descriptive results](RESULTS.md).

## Questions and evidence scope

P01 asks whether tissue RNA changes occur within comparable annotations, through
population redistribution, or both. P06 asks whether repertoire concentration
reflects local repetition within compartments or changing tissue representation.
Both use the same previously exposed atlas animals and source tables. Reuse and
mouse deletion are not independent replication. P02's intermediate-state versus
mixture comparison remains unrun for the source reasons below.

The biological unit is the deposited mouse within a comparison. Cell counts
describe capture, not independent replication or absolute tissue abundance.
The analysis retained all 29 available genes from the existing fixed family:
232 RNA decompositions across two tissues, two sex scopes and two endpoints.
The four displayed genes were fixed before the extension, not chosen by effect.
No significance tests, effect-margin claims or mechanistic scores were added.

## P01 Tissue remodelling and within-type RNA

Observed and standardized values now use exactly the same cell universe.
Eight common lung FACS annotations cover 91.34–99.01% of each included mouse's
cells; four bladder annotations cover 100%. Lung has 6 young/4 old mice; bladder
has 3/3. The male-only analysis uses the same annotations, with 4/4 and 2/3
mice respectively. All 24-month animals are male; this is not a sex interaction.

The table gives 24-minus-3-month detection differences in **percentage points**.
The four components sum to the total. Animal covariance records within-age
covariation of population weight and RNA; omitting it would incorrectly treat
a mean of products as a product of means. Values are descriptive accounting,
not causal shares or percentages of ageing explained.

| Tissue | Gene | Total | Composition | Within type | Interaction | Animal covariance |
|---|---|---|---|---|---|---|
| Lung | Cdkn2a | +0.714 | +0.166 | +1.616 | -0.699 | -0.370 |
| Lung | Cdkn1a | -5.685 | +0.004 | -3.843 | -2.052 | +0.207 |
| Lung | Lmnb1 | -0.484 | -0.786 | -0.816 | +1.000 | +0.117 |
| Lung | Il1b | -0.775 | -2.499 | +1.851 | -0.943 | +0.815 |
| Bladder | Cdkn2a | -1.238 | -0.921 | -0.526 | +0.315 | -0.106 |
| Bladder | Cdkn1a | +0.556 | +0.990 | -1.404 | +0.914 | +0.056 |
| Bladder | Lmnb1 | +3.997 | +4.673 | +1.151 | -1.963 | +0.136 |
| Bladder | Il1b | -1.176 | +2.628 | -3.361 | -0.578 | +0.135 |

**Lung:** Cdkn2a detection rises from 0.666% to 1.380% in the common-type
universe. The positive within-type term exceeds the aggregate difference,
because interaction and animal covariance offset it. The broad source
`lymphocyte` annotation changes from 0% to 13.78% detection, with minimum
10 young and 5 old captured cells per mouse in that annotation. This localizes
a candidate RNA difference; it does not identify a lymphocyte subtype or prove
cell-intrinsic senescence. Coarse labels and subtype replacement remain rivals.

Lung Il1b illustrates a different relationship: the aggregate detection contrast
is negative while its young-composition within-type term is positive. Thus a
tissue average can mask opposing population-level associations. Neither measure
tests cytokine release. Mean RNA and detection are also distinct endpoints:
Cdkn1a detection decreases while its mean normalized RNA increases in these
captured lung cells, as shown separately in Figure 7.

**Bladder:** Cdkn2a detection falls from 2.149% to 0.911%, with negative
composition and within-type terms. For Lmnb1, the aggregate increase (+3.997 pp)
coexists with a decrease within urothelial cells (−1.519 pp) and an increase
within the mesenchymal annotation (+3.952 pp). Changing population proportions
and heterogeneous within-type changes therefore both matter; the tissue mean
does not describe a uniform cellular programme. Normalized Cdkn2a mean RNA also
falls, but its small within-type term is positive, reinforcing the need to keep
detection frequency and RNA magnitude separate.

The all-sex Cdkn2a detection contrast stays positive for every single-mouse
deletion in lung (+0.248 to +0.937 pp) and negative in bladder (−1.808 to
−0.914 pp). The male-only bladder within-type component spans negative and
positive values under deletion. These are finite-sample sensitivity results;
they do not supply population precision or remove sex/capture confounding.

**Biological decision:** a uniform tissue-wide interpretation is insufficient.
P01 follow-up should connect independently measured abundance with RNA/protein
within independently resolved cell populations. A cell-intrinsic or functional
claim requires those additional discriminators. No target or preferred RQ is
selected by this decomposition.

Evidence: [four-term results](../../analysis/research/runs/nb5_composition_biological_v1/decomposition.tsv),
[within-type estimates and minimum cell counts](../../analysis/research/runs/nb5_composition_biological_v1/within_type.tsv),
[coverage](../../analysis/research/runs/nb5_composition_biological_v1/coverage.tsv),
[mouse estimates](../../analysis/research/runs/nb5_composition_biological_v1/composition_mouse.tsv)
and [all deletions](../../analysis/research/runs/nb5_composition_biological_v1/leave_one_mouse_out.tsv).

## P06 Compartment-local repertoire concentration

The 6,000 matched source T-cell rows retain the inherited source-clone
definitions. Eleven unmatched rows remain in the audit. A local repeat requires
at least two sampled members in the same mouse and tissue. A clone sampled
once in two tissues is shared, but is not a local repeat in either. This is
different from the previous whole-animal source-clone fraction.

All values below are equal-mouse means, ordered **3 / 18 / 24 months**.
Common depths are 93 cells for thymus, 29 for spleen and 8 for marrow, chosen
from the tissue-specific minimum across all ages. Compare ages within each
tissue; these different depths do not support direct between-tissue ranking.

| Tissue | Mice at 3/18/24 months | Observed local-repeat cells (%) | Common-depth expectation (%) |
|---|---|---|---|
| Thymus | 5/4/4 | 0.96 / 6.47 / 3.73 | 0.55 / 4.93 / 3.13 |
| Spleen | 4/3/4 | 1.98 / 10.70 / 6.61 | 1.20 / 5.77 / 5.03 |
| Marrow | 3/4/4 | 8.33 / 25.49 / 6.81 | 8.33 / 8.29 / 1.32 |

Older thymus and spleen means remain above their young means after conditioning
on sampling depth. Marrow does not show a universal monotonic age increase:
its 18-month expectation is close to the young value and the 24-month value is
lower. The young marrow mean itself includes a mouse with only eight cells,
so this is a contrasting observed pattern, not evidence of biological recovery.
Figure 9 retains the zeros and large animal differences.

The **balanced comparison** includes only mice with all three focal tissues:
2 young, 3 at 18 months and 4 at 24 months. Its endpoint is local-repeat cells
within those tissues; it is not the earlier pooled whole-atlas clonality.

| Age (months) | Mice | Observed (%) | Young tissue reference (%) | Equal tissue weights (%) |
|---|---|---|---|---|
| 3 | 2 | 0.860 | 1.424 | 5.489 |
| 18 | 3 | 9.242 | 5.866 | 12.850 |
| 24 | 4 | 5.268 | 4.389 | 5.714 |

The average captured thymus share declines from 77.45% to 67.82% and 61.19%;
marrow's share increases from 6.21% to 17.75% and 19.03%. Fixing tissue weights
therefore changes the observed contrast, but does not remove the higher older
mean. Young-reference contrasts are +4.442 pp at 18 months and +2.964 pp at
24 months. The young standardized mean also changes because each young mouse
receives common weights; it need not equal its original weighted mean.

For 24 versus 3 months, the observed +4.408 pp comprises composition +1.739,
within-tissue +2.964, interaction −1.245 and animal covariance +0.949 pp.
All terms are retained rather than interpreting one as a causal explanation.
The within-tissue term remains positive under each single-mouse deletion
(+2.631 to +7.117 pp at 18 months; +0.672 to +4.304 pp at 24 months), but two
young animals cannot establish robust population precision. Equal tissue
weights produce a different descriptive magnitude and are reported explicitly.

Cross-tissue shared-clone-cell fractions are also higher in older spleen and
marrow observations (Figure 10D). This describes observed distribution across
tissues, not migration or its direction. These panels use all supported mice
per tissue and are not an additional independent sample from the balanced set.

**Biological decision:** changing sampled tissue proportions alone does not
account for the older local-repeat mean in this balanced subset. The next
discriminator is whether this difference persists within comparable T-cell
subtypes with independently qualified receptor recovery. The current metadata
has no subtype field, so tissue restriction cannot distinguish subtype
redistribution from concentration within a subtype. Longitudinal or functional
evidence would be required to address expansion dynamics or immune performance.

Evidence: [local and shared endpoints](../../analysis/research/runs/nb5_repertoire_biological_v1/tissue_mouse.tsv),
[all tissues and missing strata](../../analysis/research/runs/nb5_repertoire_biological_v1/tissue_support.tsv),
[clone distributions](../../analysis/research/runs/nb5_repertoire_biological_v1/clone_distribution.tsv),
[balanced estimates](../../analysis/research/runs/nb5_repertoire_biological_v1/balanced_mouse.tsv),
[balanced accounting](../../analysis/research/runs/nb5_repertoire_biological_v1/balanced_decomposition.tsv)
and [all deletions](../../analysis/research/runs/nb5_repertoire_biological_v1/leave_one_mouse_out.tsv).

## Unresolved biological questions and holds

- **P02 microglia:** the author notebook reads the all-age figure object but
  does not establish how its transformed expression was constructed. The general
  brain object has qualified normalized 3/24-month values but lacks 18 months.
  Distinct-state versus mixture remains untested. A new expression representation
  needs qualified scale, animal and processing identity; another UMAP would not
  answer the question. Published-cluster identity is a separate reproduction hold.
- **Kidney:** common-type coverage ranges from 7.94% to 95.40% and contains only
  immune annotations. No whole-kidney or tubular compensation conclusion is
  drawn. The missing renal annotation at 24 months is not treated as cell loss.
- **P03/P04/P07/P08:** compatible injury/disease cohorts, homologous populations,
  missing sex strata and age/cohort support remain as previously recorded.
  This stage does not change their status or rank them.

These results supply bounded biological observations and competing explanations.
Novelty, functional meaning and an independent discriminator remain requirements
for RQ derivation; none is replaced by a new name, a score or successful execution.

## Provenance and validation

The [Nature 2020 atlas](https://www.nature.com/articles/s41586-020-2496-1)
provides the source study and published composition/immune context. This report's
numerical extensions are repository results, not additional claims attributed
to the paper or an independent replication. The source data and study code are
located through the [source manifest](SOURCE_MANIFEST.md).

Both numerical contracts and exact code were committed at `a44dc24` before
execution; the rendering contract was committed at `8106334` after outcomes
were inspected. Verified receipts bind the
[composition run](../../analysis/research/runs/nb5_composition_biological_v1/receipt.json),
[repertoire run](../../analysis/research/runs/nb5_repertoire_biological_v1/receipt.json)
and [figure run](../../analysis/research/runs/nb5_biological_figures_v1/receipt.json).

Arithmetic checks passed for every full/deletion decomposition, independent
count-based reconstruction, clone-size/category partitions and exhaustive toy
rarefaction. Two analytic mixture examples tested interaction and covariance
explicitly. These checks validate calculation, not biological independence.
All four PNGs were visually inspected, their short captions passed bounds and
separation checks, and 300-dpi metadata and four-page PDF caption extraction
were verified. Final repository checks are recorded in the
[execution ledger](EXECUTION_VALIDATION.md).
