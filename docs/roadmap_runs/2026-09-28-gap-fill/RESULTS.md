# Gap-fill execution, 28 September 2026

Fetched `origin`; the starting local main and remote main both resolved to `33b27cf1f03da706ee987f3fd00b7127eaaff79e`. Work runs on `codex/rq-gap-fill` in an attached managed checkout. The primary checkout's untracked work and all historical scientific outputs are preserved. The [earlier adversarial review](../../audits/2026-09-28-rq-adversarial-review/REPORT.md) describes its earlier snapshot; this report records execution against the newer state.

The imported baseline review's machine-local Markdown links were made repository-relative during final validation. Its scientific text and recorded evidence remain historical; the original untracked copy stays in the primary checkout.

Three agents handled A15 correction, A5 recovery and A12 recovery in parallel. The latter two then handled bounded A17 source accounting and A16 correction. The primary agent reviewed and committed specifications before outcomes, corrected shared documentation and integrated verification. User authorization covers execution; it does not imply acceptance of an assistant's scientific interpretation or a changed claim grade. [Execution scope](PLAN.md).

## Work completed and consequences

**A15's faulty alternative normalization is replaced in a new version.** The original implementation divided raw counts by a median-ratio factor and by library depth again. The corrected estimator uses 15,174 independent reference genes and divides by its factor once. Corrected transitional and identity effects are respectively -0.085856 (p=0.685714) and +0.021399 (p=0.885714), in log2 normalized-count units. Both remain nonseparating; the identity point estimate changes sign. The CPM primary is independently reproduced and unchanged. These score scales differ, so their numerical effects must not be subtracted as a common-unit change. Nonseparation does not exclude epithelial mediation. [Erratum, provenance and 62 independent checks](../../../RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/NORMALIZATION_ERRATUM_2026-09-28.md).

**A5 now has a precise metadata recovery target.** GSE303646's author code explicitly names the required Krt8-ADI and activated-AT2 states. Fifty-six library records match GEO, including 24 in the fixed time window. The missing per-barcode metadata in `230111_Bleo_Ageing_annotated_final.h5ad`, and the paper's 55 mice versus 56 libraries, still prevent independent mouse/state pairing. No expression matrix or score was acquired. The 99/57/53-gene instruments and all gates remain frozen. [Recovery report](../../../RQ_Specified/A5_developmental_programme_reuse/replication_gate_20260928/REPORT.md).

**A12's three candidate gates are resolved without fitting ineligible data.** Kim has ten patient pairs but zero tumour cells labelled AT2; Laughney has three title-matched pairs and at most four possible pairs; Wu has 42 tumour biopsies and no separate normal arm. None supplies the unchanged comparison. The new contract distinguishes independent replication of a learning procedure from transport of one fitted model. The 46-patient precision illustration is explicitly not biological power or an equivalence design. [Evidence and candidate ledger](../../../RQ_Specified/A12_recipient_context/external_validation_20260928/reports/RECOVERY_REPORT.md).

**Documentation defects are corrected without changing grades.** C49's approximate rho 0.43 significance cutoff is no longer presented as a bound on absent effects. C36 now points to the later ligand-resource and recipient-expression work while retaining “Not established” for reception. The generated claim manifest and negative-results index were rebuilt. A11's acute-assay paragraph is under A11, with its estimates preserved.

**A17's source inputs are independently reconciled.** Fresh MAT decoding reproduces all 58 batch1 mouse/analysis-channel count rows. The unchanged RFP comparison has 11 source-indexed mice and 16,113 clones of size >=2. Five printed Table S1 rows retain discrepancies. Positional argument tracing resolves the code's fast/slow mapping and 14-day switch, while manuscript-symbol and published-curve provenance remain unresolved. No fit or simulation ran. [Manifest, discrepancy ledger and parameter trace](a17_source_accounting/REPORT.md); [safe replay instructions](a17_source_accounting/REPLAY.md). Scope was committed at `7f1aae4`.

**A16's corrected C1 comparison is executed.** The new space excludes 660 grouping, gate and outcome genes before normalization and matches within each library and depth quartile. All 79 and 60 original positive cells remain. Priming raw differences attenuate from 1.255829 to 0.409807 and from 1.331844 to 0.315110 at k=10; on each library's common fixed-population SD scale, 1.4553 to 0.4749 and 1.8392 to 0.4352. Residual PC imbalance remains substantial (maximum 0.625 and 0.521), and the k sensitivities vary. Neither attenuation nor persistence establishes specificity, intrinsic biology or a fraction of signal explained. All 42 effects were independently recomputed; raw-score parity and original Stage 1 hashes pass. [Corrected report](../../../RQ_Specified/A16_cd177_state_attribution/correction_20260928/reports/CORRECTED_C1_REPORT.md). Contract committed at `e1d46b4` before outcomes; this remains an exposed-data C1 amendment, not a full attribution test.

## Every question: execution decision and exact remaining gap

“Held” means the necessary evidence is absent or an earlier stop remains valid. It is not a completed biological test. Computational corrections cannot supply new independent animals, preparations, fate measurements or source identities.

| RQ | Treatment in this execution | Evidence needed for the next scientific decision |
|---|---|---|
| A0 | Retain the pruned intestinal-transfer branch; no rescue search | A separately justified transfer hypothesis, independent discovery/validation and a prospective falsifier |
| A1 | Hold the linked regulatory/fate comparison | Early regulatory and RNA measurements linked to independent later fate at clone/animal/preparation level; RNA-only replacement does not qualify |
| A2 | Retain P1's split-well and medium/design ceiling | Independent source/recipient preparations, source supply versus presentation information, and measured engagement in comparable recipients |
| A3 | Hold intrinsic-memory interpretation | Matched age/harvest/sham units and independently defined states; ancestry/function linkage for memory language |
| A4 | Retain closed co-accessibility route | Verified prior activity, present activity and linked later response/fate; current RNA cannot substitute for history |
| A5 | Execute author-source and metadata recovery; do not score | Barcode-to-state/mouse export, 55/56 reconciliation, raw-UMI alignment and independence check before candidate-specific scoring freeze |
| A6 | Retain the owner's earlier low-priority decision | Named effector/outcome, independent state definitions and donor replication; do not reopen a general composition-only claim |
| A7 | Retain selection-dependence finding; do not rename states to rescue it | Biological genotype-by-state replication with state assignment independent of Sftpc/identity score, and a direct interaction contrast |
| A8 | Share A1's missing-outcome gate | Independently measured mature lineage yield, protein/morphology or function linked to fixed early predictors |
| A9 | Hold receptor-competence inference | Receptor availability/engagement and interpretable recipient response in independent units; expression-resource coverage alone is insufficient |
| A10 | Correct C49's null wording; retain split-preparation limits | Preparation/guide/image-calibration map; choose concurrent association versus future prediction, then independent-preparation calibration and absolute performance |
| A11 | Move misplaced assay paragraph; retain q=0.0547 decision | Independently comparable non-neoplastic epithelial context and supported identities, with the intended specificity/additional-information contrast fixed first |
| A12 | Execute three independent-cohort eligibility audits; all fail unchanged design | A different paired cohort with supported AT2 and source/mixture mapping; serialize full-pilot coefficients before outcomes if testing model transport |
| A12-S1 | Preserve assigned-plus-unknown source accounting | Orthogonal unknown-cell identity and contamination evidence; mature secreted protein is a separate measurement |
| A13 | Close current fixed-predictor/cohort cycle; no same-data retuning | Independent biological motivation, complete comparable triads and distinct outcome for a new trial; current RMSE worsened 0.2283 to 0.2373 |
| A14 | Retain the design as unexecuted | Independent preparation-level observations linking withdrawal/reception to viable traced mature yield; variance/precision evidence for its two separate decisions |
| A15 | Execute versioned normalization correction and independent verification | Parent study still needs independent units, active-versus-total ligand and recipient response; registration pending and mediation unresolved |
| A16 | Execute corrected C1 only after provenance recovery and committed amendment | Independent functional/outcome evidence remains necessary; corrected matching cannot exclude ambient origin or establish stable phenotype |
| A17 | Execute raw-archive count and code-parameter reconciliation | Explicit source-variant, rate-switch, shared-fold/likelihood and tail-diagnostic amendment before a fair model refit; curve provenance remains unresolved |
| A18 | Preserve pooled-spatial limitation; no animal-level fit | Mouse/clone IDs and spatial geometry linked to pair rows; mapped nonspatial mice cannot supply those spatial identities |

## Next queue and stopping rules

1. Obtain the narrowly specified A5 author metadata export, rather than another expression matrix without labels. Author contact was not performed. The browser/source search is bounded and does not prove that no export exists elsewhere.
2. Seek a genuinely compatible A12 paired cohort; the three rejected candidates stay rejected under this estimand. Changing tumour labels to AT2 would create a different analysis.
3. Use the A17 verified input manifest to finalize an explicitly exploratory model-comparison amendment. Preserve the original simulator, corrected implementation and manuscript variants; a code defect alone does not disprove founder biology.
4. For the remaining questions, collect the named missing independent units or linked measurements. Keep A0's stop, A6's priority and A13's negative prediction result visible. Do not replace these gaps with repeated scoring of the same matrices.

No new biological experiment, author communication, claim-grade change or remote publication occurred. The [verification record](VALIDATION.json) records executed checks, their scope and preserved evidence. Repository validation passes 3,709 checks. Unit coverage is the 60-test suite (one skip) plus six subsequently added A16 invariant tests, all successful. Compilation, all 18 claim bindings, 17 Nb1 output hashes and 1,867 archived A16 checks pass. All 168 claim status/authority rows remain unchanged. A broken imported baseline link was repaired and the complete repository validator then passed.
