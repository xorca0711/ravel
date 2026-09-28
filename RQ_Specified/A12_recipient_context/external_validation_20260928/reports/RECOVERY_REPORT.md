# A12 external epithelial validation: bounded recovery

**Recovery completed; no cohort passes the unchanged design, so no external A12 score or fit was produced.** This is a resolved three-candidate eligibility audit, not evidence against a recipient-context contribution. The original exploratory pilot and source-attribution uncertainty remain unchanged.

The [prospective specification](../config/prospective_gate_specification.json) was committed at `f3950253ae229f062dbae94551b04a908a8e5ade` before external scoring. Recovery used three hash-logged GEO metadata deposits and the original Kim clinical workbook/cell annotation. No expression matrix was opened, and the main checkout was read only. [Gate ledger](../tables/candidate_gate_ledger.json), [run record](../tables/recovery_run.json), [source evidence](../sources/primary_source_evidence.json).

## Recovered units and decisions

| Candidate | Recovered paired design | Source/recipient intersection | Decision |
|---|---|---|---|
| Kim, GSE131907 | 10 primary-lung normal/tumour patient pairs from original author workbook | All 10 have at least 50 normal AT2 and candidate macrophages in both arms; every tumour arm has **zero cells labelled AT2**, so complete intersection = **0** | Fixed recipient-state/coverage gate fails |
| Laughney, GSE123902 | 17 sample records; three normal/primary-tumour title-token pairs, LX675/LX682/LX684, all recorded without chemotherapy | Not measured; only four normal samples exist, so even the most permissive pairing has at most **4** pairs | Below unchanged 10-pair computational floor before cell-state gates |
| Wu, GSE148071 | 42 primary-tumour biopsies from 42 patients; no separate matched normal tissue arm | Paired tissue intersection = **0**; cell-state counts not recovered | Required within-patient normal/LUAD contrast absent |

For Kim, the [patient intersection table](../tables/kim_patient_intersection.tsv) preserves all ten patient IDs, four compartment counts, source-mixture numerator counts and exclusions. Pair IDs and sample IDs match the earlier A11 metadata crosswalk, but eligibility was recomputed for A12. The [22-sample crosswalk](../tables/kim_sample_crosswalk.tsv) also retains the unmatched normal/tumour samples. The double-primary case P0028 is shown as `ADC(Double)`; excluding it still leaves zero tumour AT2 units. GEO's description distinguishes untreated surgical lung specimens from the advanced/metastatic specimens excluded here. [Original GEO record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE131907).

Kim source counts use the deposited `Alveolar Mac`, `mo-Mac` and `Pleural Mac` labels as an explicit **candidate** union. The original `mo-Mac` count is retained separately. The source mapping and the pilot's confidence threshold have not been independently adjudicated. Neither a matching AT2 name nor a macrophage synonym establishes pilot-state comparability. These labels are sufficient to show the recipient failure; they are not admitted as an unchanged validation instrument. Tumour-labelled epithelial cells were not substituted for AT2, and no reference mapping was fitted.

Laughney's [manifest](../tables/laughney_sample_manifest.tsv) and [title-pair table](../tables/laughney_title_pair_intersection.tsv) separate evidence from inference. GEO says 17 donors, while its sample titles contain 14 distinct patient-like tokens, three repeated across tumour and normal. The inferred three pairs therefore retain title-based provenance rather than being promoted to an independently verified patient crosswalk. This ambiguity cannot rescue eligibility: four normal specimens impose an upper bound of four paired units. Source/recipient annotations, counts and state correspondence remain **unknown**, not zero. No expression or large count archive was downloaded after this decisive ceiling. [Original GEO record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123902).

Wu's [42-sample manifest](../tables/wu_sample_manifest.tsv) is joined to the primary paper's explicit statement that all biopsies came from primary lung tumours (Figure 1e). The paper's AT2-like cells inside tumour biopsies cannot supply a separately sampled normal arm. The GEO sample fields alone contain age/sex and source tissue, so this clinical-arm classification cites the paper rather than pretending GEO supplied it. Cell-level annotation counts remain unmeasured. [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE148071), [primary paper](https://www.nature.com/articles/s41467-021-22801-0).

## What a future validation would test

The pilot stored leave-one-patient-out predictions, not a single deployable fitted model. Repeating its fixed alpha=1 algorithm with new-cohort LOPO would be independent **algorithm replication** at a new training size; it would not test transport of one frozen pilot fit. Genuine fitted-model validation would first fit the unchanged models to all twelve pilot AT2 pairs, serialize their training means/SDs/intercepts/coefficients, and commit them before opening an eligible cohort's outcomes. That fit was not manufactured for these ineligible candidates.

The frozen comparison retains source IL1A/IL1B, the monocyte-derived macrophage mixture fraction, TNF and the recipient receptor/inhibitor RNA index; the primary contrast remains joint versus source-plus-TNF. The response stays the exact predictor-disjoint inflammatory RNA gene set using full-library log2(1+CPM). It is not IL-1-specific or a protein-activation measurement. A later eligible evaluation must report all baselines, absolute errors and calibration, without outcome-driven relabelling or tuning.

The ten-pair floor is a computational pilot guard. The separate **46-patient** target is a pragmatic planning calculation: for independent external fixed-model paired losses, the nominal 95% t mean half-width is `t(.975,45)/sqrt(46) = 0.296963` between-patient loss SD. It is **not** substantive power, a biological effect threshold, an equivalence margin, or a guarantee under heavy-tailed loss distributions. Ordinary paired t uncertainty must not be applied to overlapping LOPO fold losses. None of these candidates reaches the state/design gate, regardless of the precision target.

## Reproduction and verification

Run from the managed checkout with the supplied Python runtime and compatible packages:

```powershell
$python = 'C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$base = 'RQ_Specified/A12_recipient_context/external_validation_20260928'
& $python "$base/scripts/01_retrieve_metadata.py"
& $python analysis/scripts/run_with_environment.py --site-packages X:/GitHub/scRNA_seq/.venv-x64/Lib/site-packages "$base/scripts/02_audit_candidate_gates.py" --data-root X:/GitHub/scRNA_seq
& $python "$base/scripts/03_verify_recovery.py"
```

The verifier checks the frozen-spec hash, input/output and downloaded-source integrity, every Kim patient intersection, the complete Laughney/Wu sample inventories, and the distinction between unmeasured cells and zero paired tissue units. Its [verification record](../tables/verification.json) records the result. The earlier openpyxl failure was resolved by reading the original workbook XML; no input file was changed.

**Bounded conclusion:** these three candidates do not permit the requested unchanged external epithelial validation. Additional large downloads, alternative epithelial labels or count scoring cannot repair their demonstrated unit/state failures. A different eligible cohort with an independently adjudicated state/source/mixture mapping is still required; this audit does not establish that none exists. No claim grade changed.
