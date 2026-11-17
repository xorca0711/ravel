# S5M v2 amendment: distinguish count zeros from zero-containing ranges

18 November 2026. Owner `Nk17-P01`. The coordinator identified the
[v1 aggregate-flag defect](S5M_RESULTS_V1.md) before accepting S5M and explicitly
authorized this bounded versioned correction. All original S5M outcomes are
exposed. The [v1 method](S5M_METHOD_V1.md) still defines the biological purpose,
finite feature association, units, fixed universes, comparisons and limitations.
No new association, selection rule or functional claim is introduced.

## Correction and immutable boundaries

Replace the ambiguous derived `rna_any_zero_flag` with two named aggregates:

- `rna_any_count_zero_flag`: any of the 23 **explicitly allowed count-zero
  source fields** is positive/true.
- `rna_any_adjustment_range_includes_zero_flag`: the OR of exactly
  `s4__W6_adjustment_range_includes_zero` and
  `s4__W12_adjustment_range_includes_zero`.

The count allowlist is closed and specified in
[the correction script](scripts/s5m_correct_flags_v2.py):

| Stage/time prefix | Exactly allowed count-zero suffixes |
|---|---|
| `s2__D6`, `s2__D30` | `_zero_libraries`, `_control_zero`, `_exposed_zero`, `_all_zero` |
| `s4__B0`, `s4__W6`, `s4__W12` | `_zero_libraries`, `_control_zero`, `_exposed_zero`, `_all_zero` |
| `s4b__primary`, `s4b__c2_h2`, `s4b__c1_h1` | `_reference_any_zero` |

The five library-count fields are integers 0–4; the remaining count flags and
both range flags are explicit booleans. Missing/invalid fields fail; no substring
selection or zero imputation is allowed. The source flags retain their exact
definitions: group-zero flags mean all libraries in that group have zero counts,
whereas zero-library counts also detect a single zero. All original source
fields and low/regularization flags remain unchanged.

Stream-copy the v1 gene and anchor tables, replacing only the ambiguous derived
column with these two columns. Update the two universe summaries, all five
fixed anchor records and Figure 2 labels; retain the unqualified Il1b example.
Report how often a range includes zero without any count zero. Preserve original
eligibility, source-presence, ranks, ranges, units and numerical strings exactly.

Copy **byte-for-byte** `association_results.tsv`, `covariance_identity.tsv`,
`gene_atac.tsv.gz`, and Figure 1 PNG/PDF from the immutable v1 run. Do not
recalculate the 312 coefficients or 96 covariance identities, refit any upstream
analysis, choose a sensitivity, or modify any completed artifact. The new
`flag_correction_audit.json` records the correction's exact extent. V1 remains
registered with its defect; v2 supersedes its aggregate warnings and anchor
display only. The retained numerical results remain shared-source description.

## Independent semantic and preservation verification

The separate stdlib verifier reads the original **16 author-provided two-column
count tables**, GSM2440985–GSM2441000, with their frozen input hashes. It does not
import the correction's allowlist or boolean-aggregation helpers. For every
gene, reconstruct all 23 source zero fields directly from the raw counts and
compare them with the unchanged copied fields. Compute the aggregate count flag
as any raw count equal to zero across those 16 libraries. D30/B0 reuse of four
libraries remains explicit; this checks semantics, not new biological evidence.

Verify the separate range flag from the two explicitly named original S4 range
indicators. Check every other field in every gene/anchor row by exact string
equality, the entire anchor manifest and universe summary, all five byte-copied
files by SHA-256, all gene IDs against every raw-count file, and the declared
312/96 row counts. The preserved v1 numerical verification supports arithmetic
only; this new check resolves the specific warning-semantic defect. No
floating-point tolerance is needed for the correction/preservation comparisons.

The artificial regression has four genes with all combinations of a count zero
and a zero-containing adjustment range. In particular, 16 strictly positive
counts with a range including zero must give **count-zero false / range true**;
an actual raw zero must give count-zero true. An unrelated zero-named field is
ignored. Missing or invalid declared fields fail. Tampered count flags, copied
fields and coefficients are rejected. Four tests and 247 independent fixture
checks passed before freeze, without reading real biological outcomes.

Freeze and commit the amendment, four code files and input-bound contract before
the correction run. Preserve failed runs if any. Inspect corrected Figure 2 and
the unchanged Figure 1, then return actual S5M results for coordinator review
before S5F. Execution and AI review do not confer human scientific acceptance.
