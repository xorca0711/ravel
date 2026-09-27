# Computational research: next-session handoff

**Date:** 2026-09-27. **Status corrected the same day:** C1 through C7 ran. The A11 acute-injury assay is scored, reported and merged on `main`, so the original status, "ready to resume at C1; no new biological score yet", no longer holds. This file is retained as the authorization and environment record of the session that executed it, not as a live instruction to resume at C1. The results are at [ACUTE_INJURY_RESULTS.md](../../RQ_Specified/A11_lesion_programme_addition/reports/ACUTE_INJURY_RESULTS.md).

## Summary

The owner authorized committing, opening a PR and merging the completed rationale audit and roadmap work, then structuring and executing computational analyses of the remaining gaps. The owner subsequently requested small resumable tasks and this handoff for a different session. [PR #94](https://github.com/xorca0711/scRNA_seq/pull/94) is merged at `17ca9b49a4da29afef4214449ea940d1b62b999e`. The new work is on `codex/computational-research-pipeline`. A public annotated count object has been downloaded and hashed, but its internal metadata, matrix semantics, eligible contrasts and module scores have **not** been examined. Continue with the intake task, not with an assumption that the analysis passed.

## Details

### Checkout and authorization

- Active worktree: `C:/Users/dream/.codex/worktrees/rq-rationale-audit/scRNA_seq`.
- Original data checkout: `X:/GitHub/scRNA_seq`. Preserve its untracked files and caches; it is not the current code checkout.
- Remote: `https://github.com/xorca0711/scRNA_seq.git`.
- No analysis process remains running at handoff. Download session 8238 finished successfully. No new Codex chat or automation was created.
- The owner authorized implementation and real analysis, with updates between work packages. Do not ask again for routine execution, reversible edits or the already requested Git landing. Do not send author emails or other external messages without explicit authorization.
- No subagent delegation was requested. Run the small tasks sequentially; scripts handle deterministic work.
- This managed worktree can require elevated filesystem permission in Codex. Reuse it rather than creating a duplicate. The original checkout's `tmp/rq-audit/` is staging, not the scientific record.

### What is complete: do not repeat it

1. Repository-wide A0–A15/A12-S1 audit, context synchronization and biological roadmap: [architecture](../RESEARCH_ARCHITECTURE.md), [audit](../audits/2026-09-27-rq-rationale/REPORT.md), [roadmap](../RESEARCH_ROADMAP.md).
2. [P0–P5 execution](../roadmap_runs/2026-09-27/README.md): outcome ledger; 886-library screen crosswalk; source supplement recovery; A5 candidate gates; regulatory/fate linkage audit; IL1B assignment bounds; selective post-entry experimental design.
3. [Follow-through](../roadmap_runs/2026-09-27-followthrough/README.md): A12 and A13 exploratory 12-patient paired pilots, 18 additional GEO records, 76,070-cell external annotation coverage and experimental precision scenarios.
4. A12 epithelial held-out RMSE improved from 0.4271 to 0.3244 with recipient context; fibroblast increment was unstable. This is exposed discovery data, not independent validation or IL1-specific activation.
5. A13's nominated fibroblast programme worsened aggregate prediction in every eligible sensitivity. Do not tune a replacement on these same outcomes.
6. GSE233844 is PBMCs, not a lung-triad cohort. GSE122960 supplies only 3/16 complete triads at the fixed 50-cell floor (two donor/IPF-subset donors and PM-ILD); none of the IPF subjects qualifies. Those candidate decisions are closed under the existing rules.
7. Main's later provenance correction is preserved: 16 recovered A0 files were already archived on main; decision records A0-015/016 were already live. Do not resurrect the rejected recovery claim or the deleted LinkedIn draft.

Validation before merge: 56 unit tests; compileall; 18 numeric bindings; Nb1 evidence verifier; 2,910 repository checks; historical P0–P5 verifier passed. The latter now reports living-context hash drift separately from immutable scientific-source failure. Earlier follow-through validation independently reproduced 1,050 held-out predictions. These are software/evidence checks, not acceptance of a scientific claim.

### Immediate input, already downloaded

`X:/GitHub/scRNA_seq/raw_data/GSE198864/GSE198864_lung_combined_all.rds.gz`

- Public source: [GEO RDS](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE198nnn/GSE198864/suppl/GSE198864_lung_combined_all.rds.gz).
- Bytes: `2115735865`.
- SHA-256: `db0e696ddebe71d097ef84050d985b8e0affa231283038916410d869d301b5e5`.
- Retrieval record: [tracked copy](../../RQ_Specified/A11_lesion_programme_addition/tables/acute_injury_gse198864/intake/GSE198864_retrieval.json); original `raw_data/GSE198864/retrieval.json`.
- Do not download the 9.9-GB RAW tar merely to discover labels. Do not commit the RDS.
- The download completed in this session. Hashes certify bytes, not count semantics or scientific eligibility.

Primary design sources are already saved in [GEO metadata](../roadmap_runs/2026-09-27-followthrough/metadata/GSE198864.json) and [primary-source provenance](../roadmap_runs/2026-09-27-followthrough/primary_source_checks.json). The paper is [Hönzke et al., ERJ](https://pmc.ncbi.nlm.nih.gov/articles/PMC9712848/), PMID 35728978, DOI 10.1183/13993003.02725-2021; cached XML is `X:/GitHub/scRNA_seq/tmp/rq-audit/sources/PMC9712848.xml`.

The 91 GEO records mix assays: 24 ex-vivo macrophage, 8 autopsy, 49 explant, 4 bronchial-organoid and 6 alveolar-organoid records. **49 explant records are not 49 single-cell donors.** The 29 records GSM5958261–GSM5958289 list single-cell raw HDF5 files and six donor identifiers: 102C, 1169Z, 218V, 219V, 700D, 89C. Later explant records include bulk RNA. Verify all joins against the RDS and source metadata.

Control-medium issue to resolve before a primary contrast: 102C and 219V have separate BSA and FCS libraries. The source protocol uses BSA for IAV and FCS for coronaviruses. Other libraries named `control` do not establish the exact matched medium by name alone. Do not pool or silently choose controls. Paper/source supplement or explicit object metadata must justify the pairing; otherwise report the uncertainty and restrict or stop the relevant inference.

### First biological question to make executable

Candidate **A11 acute-injury falsification**, a new assay with its own contract: does the already frozen lesion-associated programme increase in author-annotated AT2 cells in infected versus appropriately matched mock explants from the same donor? Acute induction would challenge a broad interpretation of tumour-exclusive RNA. It would not prove that infection and cancer share one mechanism, nor compare matched transitional states. A negative or imprecise result cannot establish tumour specificity. These tumour-free explants originated from surgical cancer patients, so they are not a cancer-naive population.

No pathogen, primary contrast, eligible donor set or new analysis contract has yet been frozen. H3N2/IAV was nominated as a candidate because it supplies an acute-injury challenge; selection must be justified from metadata and biology **before scores**, with SARS-CoV-2 or other arms predeclared as secondary rather than chosen after results.

Use the [small-task pipeline](../COMPUTATIONAL_RESEARCH_PIPELINE.md) and [machine-readable queue](../research_pipeline/queue.json). C1 is next. C2 commits the contract before C3/C4 scoring; this handoff is not that contract.

### Runtime and useful existing code

```powershell
Set-Location C:/Users/dream/.codex/worktrees/rq-rationale-audit/scRNA_seq
$env:PYTHONPATH='X:/GitHub/scRNA_seq/.venv-x64/Lib/site-packages'
$researchPython='C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$researchR='X:/GitHub/scRNA_seq/analysis/corrections/statistics/.tools/R-portable/app/bin/Rscript.exe'
git status --short
git branch --show-current
```

Python 3.12.14 with numpy/pandas/scipy/h5py/sklearn is available through the path above. R's additional library is `X:/GitHub/scRNA_seq/analysis/corrections/statistics/.tools/R-library`; Matrix and edgeR are installed. Seurat, SeuratObject and jsonlite were not installed in the checked library; pyreadr/rdata were absent from the checked Python environment. Do not install a full environment before testing whether base R can inspect saved S4 attributes. R emits locale startup warnings here; distinguish those from nonzero exits.

Useful existing code and immutable instruments:

- [A11 v2 contract](../../RQ_Specified/A11_lesion_programme_addition/config/kim2020_test_contract.json): source normalization and original interpretation.
- [A11 scoring](../../RQ_Specified/A11_lesion_programme_addition/scripts/04_score_kim.R): edgeR TMM, logCPM prior.count=1, exact paired inference.
- [A11 human module map](../../RQ_Specified/A11_lesion_programme_addition/tables/test_v2/human_module_genes.tsv): 73 human lesion genes mapped from 91 mouse genes, 56 stress-excluded genes; verify against the source contract rather than deriving new genes from this cohort.
- [Paired inference helper](../../RQ_Specified/A5_A11_shared_component_contract/scripts/paired_inference.R): handles unattainable exact confidence intervals explicitly. With very few pairs, nominal p/interval granularity matters; do not report false precision.
- [A5 frozen contract](../../RQ_Specified/A5_developmental_programme_reuse/config/strunz_test_contract.json): a later independent annotation-transport branch must preserve or explicitly amend it.

### Recovery and validation discipline

Each task writes a small report/JSON, input hashes, script/specification hashes, exit state and explicit next task. New results use new directories. Never overwrite frozen original outputs; never rerun a successful stage without changed inputs or a concrete unresolved concern. A crash or context limit means `interrupted`, not `completed` or a biological stop. Preserve any valid partial artifact and resume at the smallest unfinished stage.

After C1, report counts, labels, donor/control ambiguity and the next decision. After C2, report the frozen contract commit. After C3, report eligible donors and coverage. After C4/C5, report estimates, uncertainty and independent verification. Update this queue, PROGRESS and AI_CONTEXT between packages.

Run only checks appropriate to changed files. The existing CI commands are compileall on `analysis`, `Research Article`, `RQ_Specified`; unittest discovery in `analysis/tests`; `analysis/scripts/claim_contract.py --check`; Nb1 `verify_outputs.py`; `analysis/scripts/validate_repository.py`. Successful old scientific checks need not be repeated just to produce more output.

## Next steps

1. C1: inspect the downloaded object's metadata and assay inventory without module scoring; persist the sample/donor/condition/state crosswalk.
2. C2–C5: freeze, gate, execute and independently verify an identifiable A11 contrast, or record the exact failed gate without substitution.
3. Continue the independent A5 annotation task and A12 cohort intake in the pipeline. The [remaining-gap ledger](../roadmap_runs/2026-09-27-followthrough/remaining_work.json) remains authoritative historical evidence; add a dated current status rather than rewriting it.
4. Do not claim computational closure of regulatory-to-future-fate, selective receptor engagement, or withdrawal mechanisms without the linked/interventional data those claims require.
