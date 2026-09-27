# A12: conditional recipient-context pilot

**Executed, exploratory; no mechanism or claim-grade change.** A new gene-disjoint RNA comparison was specified before scores/fits, after exposure to earlier results and coverage. [Specification](A12_pilot_specification.json), [inputs](A12_model_inputs.csv), [held-out predictions](A12_heldout_predictions.csv), [metrics](A12_model_metrics.csv), [provenance](A12_pilot_results.json), [script](scripts/a12_conditional_pilot.py).

## Biological interpretation and design

IL1R1/IL1RAP and antagonist/decoy RNA may describe a recipient context in which inflammatory responses differ. RNA is not receptor occupancy. The outcome is the externally defined [MSigDB TNF/NFkB hallmark](https://www.gsea-msigdb.org/gsea/msigdb/cards/HALLMARK_TNFA_SIGNALING_VIA_NFKB), with IL1A, IL1B and TNF removed to avoid direct predictor overlap. It measures general inflammatory transcription, not selective IL-1 activation. Of 197 frozen genes, 193 are assayed. Absent genes were excluded, not filled with biological zeros or repaired through aliases.

GSE308103 supplies 12 paired patients at the primary 50-cell floor in exact existing AT2 and alveolar-fibroblast candidate labels. The source is explicitly the broad **assigned** macrophage compartment. Scores are mean log2(1+full-library CPM); all features and the outcome are LUAD-minus-normal within patient. The equal-weight recipient RNA index subtracts mean IL1R2/IL1RN/SIGIRR from mean IL1R1/IL1RAP. It is an operational summary, not a biophysical model.

The source model uses IL1A, IL1B and monocyte-derived macrophage fraction. The primary comparison adds the recipient index to the same model already containing TNF. This challenges one important alternative ligand. All five models use identical held-out patients. Ridge strength is fixed before fitting, with train-only feature centering/scaling and an unpenalized intercept. No held-out outcome is used for normalization, selection or prediction.

## Results

| Recipient | Training-mean baseline RMSE | Source + TNF RMSE | + recipient context RMSE | Patients with lower squared error |
|---|---:|---:|---:|---:|
| AT2, primary | 0.3763 | 0.4271 | 0.3244 | 7/12 |
| Alveolar fibroblasts, secondary | 0.4085 | 0.2098 | 0.2283 | 5/12 |

The AT2 primary MSE improvement is 0.07723; its joint-model prediction Q2 against the held-out training-mean baseline is 0.2569. Positive numerical improvement persists at ridge strengths 0.1 and 10, at the 30-cell floor (18 pairs), and under the existing confidence sensitivity (16 pairs). These are robustness descriptions, not independent replications. At the 100-cell floor fewer than ten pairs remain and no model is fit.

Fibroblast context worsens the primary comparison by 0.00810 MSE, with direction changing under ridge/confidence sensitivity. The source-only versus recipient extension would look favorable for fibroblasts (RMSE 0.4072 to 0.3648), illustrating why the alternative-ligand comparator matters. No model was chosen after inspecting these results.

## Limits and decision

Twelve pairs support a small exploratory prediction calculation, not a powered population claim. Cross-validation folds share training observations, so their errors are dependent: no naive t test, confidence interval or significance declaration is reported. The assay, reference annotation, shared inflammation and within-compartment composition remain rivals; paired differences do not remove disease-dependent confounding. Healthy-reference AT2 labels do not independently validate malignant-cell identity. Gene disjointness does not remove shared-normalization artifacts. Assignment-sensitive IL1B counts remain outside the nominated macrophage source.

Prioritize **independent epithelial validation**, retaining the fixed model and all alternatives. Do not promote IL-1 specificity, transmission, fibroblast mediation or successful repair. This pilot closes the runnable conditional comparison; it does not close A12's biological hypothesis or A12-S1.
