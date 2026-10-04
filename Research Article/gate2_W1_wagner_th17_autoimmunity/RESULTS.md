# Current Wagner execution result

**4 October 2026: R1 numerical source-score reconstruction and formal figures completed.**

Read [current numerical findings](SOURCE_SCORE_RESULTS.md), the
[verification amendment](NUMERICAL_AMENDMENT_v3.md) and [figures/captions](FIGURES.md)
before the original plan. Wg-R01 owns the run; Wg-P02 gains a bounded descriptive
pathway-heterogeneity result. R2–R5 and the other biological branches remain
separately gated, with exact next steps in the [handoff](HANDOFF_2026-10-04.md).

The run covers 290 qualified cells, 6,373 individual reactions and 1,722 tested
metareactions. Twenty of 53 display pathways have both source-significant
directions; glycolysis has 19 positive and zero negative groups at the source
threshold. There are 784 core groups, but 1,912 formed groups versus the paper's
1,911. Unknown biological nesting and numerical/source-version differences
preclude an exact manuscript or population-inference claim.

The bundled Python interpreter successfully uses the existing x64 scientific
packages. No installation was needed. Two failed attempts are preserved and a
third passed numerical verification. See [validation](VALIDATION.md) for the
repository gate's handling of those failed records and integration status.

The following section is the preserved earlier R0 checkpoint. Its statements
about unrun stages and package availability describe that earlier checkpoint.

# Historical R0 source-qualification result

**4 October 2026 — R0 source qualification executed; biological analyses unrun.**
Read this result and the [continued precedent review](PRECEDENT_REVIEW.md)
before the initial plan. Owner: **Wg-R01**. The decision is whether exact source
identity permits a descriptive author-score reconstruction. The strongest rival
is that matching totals conceal different cells or mistaken biological units.

## Governed evidence

- [Frozen contract](config/source_qualification_v1.json), committed at `fee96e4`.
- [Verified run receipt](../../analysis/research/runs/wg_source_qualification_v1/receipt.json).
- [Qualification result](../../analysis/research/runs/wg_source_qualification_v1/qualification.json).
- [Exact cell join](../../analysis/research/runs/wg_source_qualification_v1/cell_join.tsv),
  [sample/design labels](../../analysis/research/runs/wg_source_qualification_v1/samples.tsv),
  [download manifest](../../analysis/research/runs/wg_source_qualification_v1/source_manifest.json).

The runner verified 14 hash-bound local inputs. Six author files also match Git
blob identities at `31141a8d82872fb09803a0bf66ffc793d1410be8`. This is a
documentation/tutorial revision, not proof of the precise manuscript runtime.
Expression and reaction values were downloaded but not analysed by R0.

## Confirmed identity and design observations

| Source | Observed records and labels | Permitted interpretation |
|---|---|---|
| Author example and GSE75109/GSE75111 | 290 exact SRX joins: 139 Th17p and 151 Th17n. Both author matrices have the same 290 unique cell columns in metadata order. | Author-labelled SRR cells join to GSM through SRX. SRA RunInfo was not independently checked; animal/preparation mapping is unresolved. |
| GSE162300 | 36 libraries; WT1–WT3, Th17n/Th17p/iTreg, Vehicle/DFMO, run1/run2. | Three explicit animal labels, with repeated runs; 36 libraries are not 36 animals. Technical-run handling needs source verification before RNA fitting. |
| GSE162382 | 28 libraries; WT1–WT4 and JMJD3CKO1–3; Th17n/iTreg, ctrl/DFMO. | The deposited design does not contain Th17p. Qualify actual matrix columns, within-animal pairing and rank before an interaction model. |
| GSE165088 | 12 libraries; WT1–WT3; Th17n/iTreg, Vehicle/DFMO. | ATAC animal labels are present. Repeated WT labels across series do not establish RNA–ATAC pairing. |

The endpoint is identity/metadata concordance. Biological units are animals or
independent preparations; sorted-cell units remain unknown. No cell-level
population test, gene contrast, measured flux, fate or functional conclusion
was produced. No biological effect margin or sample size was invented.

## Verification independent of the production join

The receipt verifier passed. A separate regex extraction of raw SOFT SAMPLE
blocks checked all 290 output GSM/SRX pairs against the original author metadata,
exact series membership, condition and absent animal labels. It reproduced the
139/151 split and found no duplicate GSM or invented animal identifier. The
five targeted tests also reject duplicate SRX/cell IDs, missing membership and
condition conflicts. These are mechanical checks, not biological replication.

## Stage decisions

- **R1:** exact source identities permit a separately frozen **descriptive**
  precomputed-score reconstruction. Preserve the tutorial's reaction-level
  versus optional metareaction distinction. Any cell-level source p-values must
  be labelled source reconstruction, not population evidence.
- **R2:** full Compass remains held for historical normalization/model/runtime
  equivalence and local solver/license qualification.
- **R3/R4:** metadata progressed; assay matrix joins, technical runs, model rank,
  peak/genome annotations and functional source values remain separate tasks.
- **R5/P01–P06:** no numerical branch execution or human acceptance occurred.
  P05/P06 still require nominated biological tuples and linked measurements.

There was no failed numerical run. A missing `python` command on PATH was
resolved by using the bundled interpreter; its environment has NumPy/pandas
but lacks SciPy/statsmodels/matplotlib. That observation does not establish that
the separate repository scientific environment is unusable; qualify it before
installing another environment. CPLEX and actual laboratory access remain unknown.

The [handoff](HANDOFF_2026-10-04.md) distinguishes completed jobs from these
remaining stages. This result initiates the pipeline without claiming that
source-score reproduction or the six biological branches are complete.
