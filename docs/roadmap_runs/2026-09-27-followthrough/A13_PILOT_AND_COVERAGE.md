# A13: fixed-state pilot and external coverage

**Executed, exploratory; no evidence grade changed.** [Specification](A13_pilot_specification.json), [model inputs](A13_model_inputs.csv), [predictions](A13_heldout_predictions.csv), [metrics](A13_model_metrics.csv), [run](A13_pilot_results.json), [script](scripts/a13_conditional_pilot.py).

## Newly measured local triads

The GSE308103 follow-through checks the intersection, not merely separate compartment totals: 12 patients have normal and LUAD samples with at least 50 cells in fixed AT2, fixed Alveolar fibroblasts and broad assigned macrophages. This **new, explicitly amended compartment rule** differs from the historical A13 largest-single-macrophage-label gate. It neither rewrites that gate nor demonstrates eligibility for the same original test. Fixed fibroblast labels avoid choosing each donor's largest fibroblast population. Existing healthy-reference identities remain conditional.

The outcome uses the fixed HPCS-without-ADI/operational-markers RNA proxy: 91 original mouse genes, 73 frozen human mappings, 72 present in the assay. The fibroblast predictor uses the [MSigDB TGF-beta hallmark](https://www.gsea-msigdb.org/gsea/msigdb/cards/HALLMARK_TGF_BETA_SIGNALING), excluding the overlapping outcome gene TGIF1: 53 frozen, 52 assayed. These are RNA measurements; the outcome is not lineage potential, and the predictor is not active TGF-beta. The score is a newly declared mean log2(1+CPM) instrument, not a rerun of A11's TMM instrument.

The primary held-out comparison adds the fibroblast programme to IL1B, macrophage subtype fraction and TNF. Normalization, paired differencing and fixed ridge evaluation follow A12. All data were already exposed in prior repository analyses, and A12 results were known before this specification. This is a new exploratory question on reused data, not new independent evidence.

| Model | Held-out RMSE | Q2 versus held-out training-mean baseline |
|---|---:|---:|
| Training mean | 0.2167 | 0 |
| IL1B + macrophage mixture | 0.2426 | -0.2527 |
| Source + fibroblast programme | 0.2671 | -0.5193 |
| Source + TNF | 0.2283 | -0.1094 |
| Source + TNF + fibroblast programme | 0.2373 | -0.1984 |

Primary MSE worsens by 0.004181. Although eight patients have smaller individual errors, the aggregate loss worsens; votes are not a substitute for the frozen loss. It also worsens in every eligible predeclared sensitivity (ridge 0.1/10, 30-cell floor, confidence 0.3). At floor 100, fewer than ten complete patients remain. No confirmatory inference or exclusion of a meaningful biological effect is claimed.

**Decision:** do not expand this fibroblast programme on this cohort. The fixed test supplies no predictive reason to favor it beyond the source/alternative comparator. This does not refute fibroblast biology or prove a zero effect.

## The two named external candidates are resolved

- [GSE233844](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE233844): its primary design is PBMCs, not lung tissue. It cannot supply a lung AT2/fibroblast/macrophage triad. The prior title-based candidate designation is withdrawn.
- [GSE122960](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122960): author annotations were recovered from the [paper-linked cell browser](https://sqlifts.fsm.northwestern.edu/public/resources/). The Figure 1 export holds 76,070 cells across 16 subjects; the 17th GEO record is a separate cryobiopsy. Under the exact author AT2 Cells/Fibroblasts/Macrophages labels, **3/16** subjects pass floor 50 across all diagnoses: Donor 5, Donor 7 and PM-ILD. Restricting to donor/IPF gives **2**, with no represented IPF subject passing. Even granting the uncounted separate cryobiopsy one eligible subject cannot reach ten. No large count-matrix download or fit is justified.

[External pre-count specification](A13_external_coverage_specification.json), [every subject](A13_external_subject_coverage.csv), [source hash and result](A13_external_coverage_results.json), [saved author annotation](inputs/GSE122960_author_meta.tsv.gz). At floors 30/100 the all-diagnosis totals are 9/0; sensitivities do not replace the primary. The exported column spelling was corrected after the first attempt refused before producing counts; the event is recorded.
