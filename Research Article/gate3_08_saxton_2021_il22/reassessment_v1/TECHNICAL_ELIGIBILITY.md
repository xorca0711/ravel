# Job-level technical eligibility reassessment

1 November 2026 (Asia/Seoul). Owner **Sx22-P01**. This is the requested initial
source/runtime/governance assessment, **not authorization or execution of biological
endpoints**. The subsequently received parent brief is identified at the end;
this file records eligibility before its numerical execution.

Branch `codex/saxton-eligibility-reassessment-20261101` starts from shared local
scope clarification `21aa646d8c6c7228277ddaa6ac9923e4dec057f5`. Fresh main is
`51d3b930b3805c616e67e414390ecf060647d090` (merged gallery PR #156). The existing
technical worktree was clean and remains preserved. This phase owns only this
file; the parent owns PROGRESS, navigation, current dispositions and the amendment.

## Question and limits being assessed

The proposed exposed shared-source replication/robustness question asks whether
the six deposited colon libraries support a selectively different
interferon-associated versus epithelial barrier-associated transcriptional
pattern, beyond nonspecific weakening of the overall response and the paper's
selected panels. The source is Saxton's engineered-IL-22 paper; the deposited
groups are PBS, WT IL-22 and 22-B3. This context is retained explicitly. This is
not ligand design/optimization, a new mechanism or an unrelated-atlas substitute.

The prospective comparison concerns transcript measurements among those saved
groups. Library records are observed technical units; independent biological
colon samples are author-reported, while separate animal/preparation and batch
keys remain unverified. Neither counts nor a gene-set summary measures STAT
phosphorylation, pathway activation, epithelial-intrinsic regulation, repair or
chromatin memory. Bulk-cell composition and a broadly attenuated response are
consequential alternatives. The parent must define the precise selectivity
comparison and endpoints before execution; this assessment does not select a
model, memberships, effect margin or favorable-result threshold.

## Historical service failure versus current status

The owner-supplied historical error is:

> Invalid prompt: we have limited access to this content for safety reasons

The [recovery record](../RECOVERY_SCOPE_2026-10-31.md) documents two failed turns
in the original technical chat and says the service did not identify the
triggering item. No R2/R3 result was produced. Thus the recorded failure was
prompt-level, not an identified R2a, R2b or R3a–c model failure. The older
[ledger](../COMPLETION_LEDGER.md) applied a broad execution hold during the bounded
recovery; its historical wording is preserved rather than silently rewritten.

No job-specific service refusal occurred in this reassessment's read-only file
reads and runtime imports. **No biological endpoint request was attempted**, so
these successful reads establish neither service clearance for future execution
nor a new blanket prohibition. The historical failure is not explained by missing
counts, missing packages or a scientific-design error. Those are separate issues.
No rejected request was retried under different wording or in a replacement chat.
If a later authorized job receives a current refusal, retain its exact error and
stop that dependent work; do not disguise the context or route around the refusal.

## Evidence reused without rerunning R1/X1/X2

- [R1 review](../R1_REVIEW.md): the count and FPKM tables have 35,275 rows and six
  libraries; deposited Ensembl IDs are unique; source/sample joins and technical
  quantities were independently checked. The three declared raw cache files are
  present now. This phase did not rehash/recalculate their already-reviewed QC;
  any future runner must still enforce its declared input hashes.
- [X1/X2 results](../extensions_20261031/RESULTS.md): 52 repeated symbol labels
  span 122 rows and refer to different stable IDs. Exact annotation release is
  unknown. All six GEO/BioSample/SRA chains reconcile, but explicit animal,
  preparation, pooling-composition, allocation and batch keys were not recovered.
  SRA paired-end layout and database membership do not establish animal pairing.
- [Source audit](../SOURCE_AUDIT.md), qualified by the
  [source correction](../SOURCE_CORRECTION_2026-10-31.md): main Figure 6 and methods
  on supplied PDF pp. 22–23 report two independent biological RNA samples per
  group. qPCR technical triplicates are separate and do not enlarge RNA-seq n.
- The registry has seven existing Saxton contracts and no R2/R3 execution
  contract at this assessment checkpoint. No frozen machine-readable Saxton
  panel/set asset is registered yet. The parent's later pointers enabled
  qualification of literal Figure 6 memberships and an existing public-release
  GMT cache, as recorded below.

## R2/R3 eligibility by job

All rows below remain **unexecuted in this phase**. “Source-ready” means a
prospective descriptive job can be specified from existing evidence; it does
not mean the service has accepted an endpoint request.

| Job | Available evidence and bounded feasible scope | Exact remaining requirements / interpretation limit |
|---|---|---|
| **R2a: normalized expression and direct descriptive contrasts** | Reviewed counts, FPKM and six source labels are available. Fixed per-library normalized quantities and explicitly descriptive group contrasts can be scoped without claiming animal-level precision. The existing Python stack can support basic table/array arithmetic. | Parent must freeze the normalization, filtering/zero handling, contrast definitions, identifier policy and outputs. Published FPKM availability does not identify the paper's exact display transformation. Preserve stable-ID rows; no arbitrary collapse of repeated symbols. No sampling p-values/intervals or causal/selectivity claim follows merely from a descriptive difference. Method-specific runtime qualification follows the chosen brief. |
| **R2b: inferential count model** | The author's n=2 independent-biological-replicate statement supports an intended replicated, unpaired design; it is not evidence of technical duplicates. Missing individual mouse IDs does not itself prove pseudoreplication or make every count model scientifically impossible. The supplied portable R stack loads edgeR and limma successfully. | Current R1 `unit_status` is `unknown`, and the current gate rejects population inference without verified units. An explicit evidence-backed unit qualification is needed before an inferential contract can pass honestly; the parent agrees this hold remains. Runtime availability does not remove it. Do not call an inferential model “descriptive” just to bypass this requirement. Unreported batch/allocation cannot be reconstructed or adjusted with invented covariates; small n and model-dependent uncertainty remain even after qualification. |
| **R3a: exact published panel reproduction** | Figure 6 image and literal memberships were source-checked below. All 30 RNA-panel symbols and the additional qPCR-only Cxcl1 symbol have unique exact deposited-symbol matches; none hits the 52 repeated-symbol ambiguities. Figure 6B/D labels report log2 fold changes relative to PBS. | Freeze a machine-readable panel asset and the chosen calculation before use. Exact author gene/filter/zero-handling and aggregation choices are not recovered, particularly for 6A; an adapted descriptive reanalysis must not be called exact author replay. qPCR bar heights are not raw RNA-seq observations. Author-selected panels are reproduction targets, not independent confirmation of selectivity beyond selection. |
| **R3b: bounded independently sourced gene-set interpretation** | The cached mouse Hallmark 2026.1 GMT matches the public release exactly; actual memberships and selected exact-symbol coverage are qualified below. It can supply source memberships without another atlas. | The parent must adopt and freeze the appropriate definitions, biological rationale, background universe, unmapped-member policy, overlap accounting and endpoint. The three inventoried sets are not automatically an epithelial-barrier or activation definition. “Independent” means independent of the paper's selected list, not independent samples/replication. Shared genes and cell composition prevent direct STAT activation or universal STAT3=repair/STAT1=damage claims. GSEApy absence matters only if that implementation is chosen. |
| **R3c: library/normalization sensitivity** | The same six library records and reviewed QC can support a bounded descriptive sensitivity assessment after the primary R2a specification/output exists. Such checks need not claim population inference. | Freeze the allowed normalizations and library influence checks before looking at endpoint results. They reuse the same data and cannot supply new biological replicates, remove unknown batch confounding or validate a mechanism. No cell/gene pseudoreplication, outcome-driven library exclusion, noisy-denominator retention ratio or equivalence claim from a nonsignificant result. Runtime requirements depend on the prespecified alternatives. |

### R2b: reconcile the source report with the actual gate

The source audit's statement that a conditional unpaired model may use the
author-reported n=2 is a scientific possibility, not a currently completed unit
verification. The immutable [R1 contract](../config/r1_contract_v2.json) records
`unit_status: unknown` and `inference_scope: descriptive`. The current
[gate implementation](../../../analysis/lib/research_governance.py) explicitly
checks non-descriptive inference against verified unit status and emits:

> Population inference requires verified independent biological units

That is a condition read from validator code, **not an error triggered by a new
R2b execution attempt**. The [governance](../../../docs/RESEARCH_GOVERNANCE.md)
also distinguishes descriptive work, exploration and confirmation. Prior outcome
exposure prevents relabeling this as unexposed confirmation.

A later qualification may assess whether the paper's explicit biological-sample
statement and sample mapping sufficiently establish the chosen independent unit.
The gate does not require a literal field named “mouse ID,” and absent IDs alone
are not proof against the authors' report. But changing `unknown` to `verified`
requires a documented evidentiary judgment, not an agent changing a flag to make
its model run. If independence remains unresolved, keep population inference
held and retain only properly labelled descriptive endpoints. No validator or
scientific acceptance record is changed here.

## Source membership qualification

The parent supplied a Figure 6 render of the final PDF p. 9. Visual inspection
confirmed these literal source labels and members; author-category names are
retained without certifying their biological function:

| Locator / literal author grouping | Members |
|---|---|
| 6B tissue protection | Reg3b, Reg3g, Muc1, Muc13, Hamp2, Lbp |
| 6B DNA-damage response | Brca1, Rad51, Cdc45, Mcm2, Mcm5, Cdt1, Chek1 |
| 6B anti-inflammatory | Il18bp, Trim40, Socs3, Socs1 |
| 6D interferon response | Isg15, Apobec3, Tmem173, Ifit1, Ddx60, Gbp2, Apol9b |
| 6D TNF/Trail pathway | Tnfrsf1b, Tnfsf10, Tifa, Ripk2, Bcl3 |
| 6D separate plot | Il1rn |
| 6E additional qPCR-only target | Cxcl1 |

The source image is
`C:/Users/dream/.codex/visualizations/2026/10/29/01a18687-3e55-7b51-b514-52f5f55a210b/saxton_review/IL22_page_9.png`,
SHA-256 `bdab2a92ba855dae1bf1f38a4d776b1bd0e2be6517c2ea24ebca179c04e28d76`.
An exact-symbol join against the frozen X1 annotation metadata found all 31
symbols once each. No expression columns were read. These literal memberships
can now be frozen in an execution asset, while exact author numerical replay
remains distinct from an adapted descriptive calculation.

The existing cache
`C:/Users/dream/.codex/worktrees/saxton-il22-execution-20261031/ravel/raw_data/Sx22/mh.all.v2026.1.Mm.symbols.gmt`
contains 48,007 bytes, 50 uniquely named sets, nonempty member fields and no
within-set duplicate symbol. Its SHA-256 is
`3a21be724a87dc0375955e725ca9688b87a26e7b74b62fba0c62da0967b789f7`.
An ordinary read-only retrieval from the authoritative
[Broad mouse Hallmark 2026.1 release](https://data.broadinstitute.org/gsea-msigdb/msigdb/release/2026.1.Mm/mh.all.v2026.1.Mm.symbols.gmt)
returned HTTP 200 and exactly the same bytes/hash on 1 November 2026; no file was
written. The payload's gene-set links identify the mouse MSigDB collection.

| Inventoried membership | Source symbols | Unique exact deposited matches | Unmatched symbols |
|---|---:|---:|---|
| HALLMARK_INTERFERON_ALPHA_RESPONSE | 94 | 92 | Tent5a, Wars1 |
| HALLMARK_INTERFERON_GAMMA_RESPONSE | 188 | 184 | Marchf1, Rigi, Tmt1b, Wars1 |
| HALLMARK_IL6_JAK_STAT3_SIGNALING | 85 | 85 | None |

No member of these three inventories has multiple exact deposited-symbol
matches. Unmatched names are annotation/mapping gaps, not zero expression or
biological absence; no aliases were guessed. This was membership qualification,
not adoption or scoring. The subsequent parent brief authorizes only the two
interferon sets for execution; the IL6/JAK/STAT3 inventory is not an execution
set and does not establish a barrier/repair definition. Set overlap and the
selected universe still require explicit accounting in the prospective contract.

## Runtime qualification actually performed

The active executable is
`C:/Users/dream/AppData/Local/Programs/Python/Python312-arm64/python.exe`,
Python 3.12.10 ARM64. Availability was tested by module discovery and actual
imports only; no fit, normalization, gene-set score or expression contrast ran.

| Component | Observed state | Consequence |
|---|---|---|
| NumPy / SciPy / Matplotlib | Imports passed: 2.5.1 / 1.18.0 / 3.11.1 | Basic numerical/table support and plotting available; not qualification of a particular count model |
| pandas / statsmodels / PyDESeq2 | Not importable in active Python | These Python implementations are unavailable; the portable R alternative below changes the overall runtime assessment. No package was installed |
| GSEApy | Not importable | Any proposal using it requires a separate runtime qualification; its absence does not preclude every bounded gene-set summary |
| anndata / Scanpy | Not importable | Not required merely to read the existing bulk tab-delimited inputs; no single-cell substitute is proposed |
| h5py | Not in default import path; isolated `.tools/sx22_e1a_runtime` imports 3.16.0 successfully | Existing optional HDF5 reader retained, but not needed for the bulk source or a count model |
| Default R discovery | No Rscript application on PATH; `C:/Program Files/R` absent | Initial PATH-only inventory was incomplete; the supplied portable path below is usable |
| Portable R / edgeR / limma | R 4.6.1 (ucrt); namespace imports passed for edgeR 4.10.5 and limma 3.68.5 | An existing implementation is available for the parent's method choice; no biological fit or numerical model test was run |
| Portable R DESeq2 / ggplot2 / data.table | Not available through the qualified library paths | Method-specific gaps only; not a blanket runtime hold |

Qualified executable:
`X:/GitHub/ravel/analysis/corrections/statistics/.tools/R-portable/app/bin/Rscript.exe`.
The existing library
`X:/GitHub/ravel/analysis/corrections/statistics/.tools/R-library` was prepended to
the R process's library paths for these namespace checks. Startup emitted
nonfatal failures setting `LC_COLLATE`, `LC_CTYPE`, `LC_MONETARY` and `LC_TIME` to
`C.UTF-8`; package imports nevertheless completed with exit code zero. No machine
locale setting was changed. These warnings are not service restrictions.

Python/package presence is not a scientific eligibility decision. The final
brief must select the method before any missing dependency is installed or a
synthetic runtime test is treated as sufficient validation. No ad hoc replacement
of an absent established count model was constructed.

## Remaining R4/R5/E1/E2 dependencies

These entries reuse reviewed locators and later amendments. They do not claim
new current service refusals, and this phase does not authorize their endpoints.
“Unqualified” describes the inspected evidence, not proof that no other source
file could contain the information.

| Job / endpoint | Exact remaining dependency and resulting limit |
|---|---|
| **R4: Fig. 3D/E signaling curves; Fig. 3F/4A–C/5B–G,I blots** | Raw same-analyte measurements, dose/replicate/preparation links and curve-identifying coverage remain unqualified. Representative blots are not a verified intensity series. Unlike antibody-channel values cannot establish a meaningful ratio. Fig. 5F/G have figure/caption cell-identity conflicts retained by the source correction. Curve parameters, densitometry and new STAT ratios remain unqualified. |
| **R4: Fig. 5H receptor qPCR / context** | Raw animal/preparation values and cell-specific/surface-protein measurements remain unqualified. The corrected locator is 5H; receptor RNA is not receptor abundance or signaling response. |
| **R5: Fig. 7A/B organoid endpoints; 7C crypt endpoints** | Organoid/well-to-mouse and crypt-to-animal links and raw measurements remain unqualified. MTT is a metabolic viability endpoint, not survival time or mature lineage function. Crypt number and depth are different endpoints, not independent replicates of one repair score. |
| **R5: Fig. 7D/F serum endpoints; 7E/G/H tissue qPCR** | Raw sample values/keys remain unqualified; qPCR requires Ct/normalization and biological/technical nesting links. Fig. 7G/H organ assignment remains conflicted between visible labels/main text and caption. Acute injury/inflammatory markers do not establish durable functional recovery or chronic safety. |
| **E1: recipient-state/response extension** | [E1a](../recipient_context_v1/RESULTS.md) completed a separate descriptive transcript question. The saved Choi benchmark has one pooled library per condition, no animal-resolved map, imperfect labels and absent pAT2 recovery. Only two single Il22ra1 counts were observed, not a responsive-state pattern or proof of absence. No linked IL-22 exposure/response or functional endpoint connects those cells to Saxton. This source cannot supply the intended animal-level mechanistic comparison; no new atlas search is authorized. |
| **E2: persistence after cessation and later function** | [X3](../extensions_20261031/X3_SOURCE_LINKAGE.md) did inspect S5e/caption and named reporting-summary/workbook-index material, superseding the old uninspected status at that coverage. It supplies a withdrawal transcript, not verified residual-signal cessation, per-time preparation IDs/replication/error-bar meaning or a within-unit later-function join. Neighboring mouse counts cannot be assigned to S5e. Other advertised/raw material remains explicitly unassessed; neither the transcript series nor an acute program score establishes memory or recovery. |

## Concrete inputs needed in the parent's execution brief

1. Final question/contrast and permitted claims, including how the proposed
   selective pattern differs from an overall attenuated response; no invented
   biological margin or universal STAT-function label.
2. R2a normalization/filtering/zero/identifier policy and exact outputs. Any R2b
   addition needs its own unit-qualification rationale, inferential scope and
   qualified implementation; source-reported and independently verified facts
   must remain distinguishable.
3. Exact published-panel and independent-set membership sources/versions with
   stable-ID reconciliation, ambiguity dispositions, overlap/background handling
   and paper-selection versus independent-definition status.
4. A bounded R3c sensitivity list and interpretation rules, followed by committed
   hash-bound code/tests/contracts and fresh runner paths for each authorized job.

No numerical contract or registry entry is added in this assessment. No endpoint
output exists from this phase. R1/X1/X2, source contracts/outputs, canonical RQs,
attributes and validators remain unchanged. Parent owns status/navigation and
the literature-grounded amendment. No push, PR, external-service write or human
scientific acceptance occurred.

## Documentation verification

Repository validation passed 12,846 checks and the base-aware research gate
passed with zero errors against freshly fetched main `51d3b93`. These checks
preceded the final source/runtime additions; their only new link is the verified
public GMT URL. A final targeted link/scope/whitespace check follows those
additions. No duplicate full test suite or scientific source analysis was rerun.
The parent will validate the subsequent combined numerical/documentation tree.

The parent supplied execution brief commit
`07c8752706eac10f6cc9a2f895f702a49c0d6d60` after these findings. At this report's
commit, no biological endpoint has yet been calculated. The subsequent phase
must integrate that brief, freeze the declared descriptive code/contracts and
preserve this assessment checkpoint; Q5/R2b population inference remains held.
