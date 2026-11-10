# Three Saxton extensions: plans and execution

8 November 2026, Asia/Seoul. Owner-authorized follow-through under existing
Sx10-P01/Sx22-P01. Outcomes were exposed; no new canonical RQ, scientific
acceptance, structure redesign or laboratory result is claimed.

| Direction | Established plan | Executed work and disposition |
|---|---|---|
| IL-10 output transport | [Route 1 and source amendment](../../../Research%20Article/gate3_07_saxton_2021_il10/extensions_20261108/PLAN.md) | Workbook qualification failed a common-matrix requirement; narrower table qualification and fixed three-target description completed. [Results and figure](../../../Research%20Article/gate3_07_saxton_2021_il10/extensions_20261108/RESULTS.md). |
| IL-10 ligand × IL-18 | [Route 2](../../../Research%20Article/gate3_07_saxton_2021_il10/extensions_20261108/PLAN.md#route-2-does-ligand-choice-alter-the-il-18-response-increment) | Two public candidates screened; no qualified matched human CD8 variant × IL-18 source. Interaction held. |
| IL-22 B3 × IFNα priming | [Plan](../../../Research%20Article/gate3_08_saxton_2021_il22/priming_extension_20261108/PLAN.md) | Sixteen GSE records retained, with related records distinguished. No qualified epithelial factorial source. [Screen result and missing evidence](../../../Research%20Article/gate3_08_saxton_2021_il22/priming_extension_20261108/RESULTS.md). |

## Biological implication

The Gorby reported estimates show all three targets favoring R5A11D at 0.1 nM
and WT at 50 nM. The Saxton IFNG-up/GZMB-down split therefore is not a portable
description across these deposited comparisons. High-dose IL18RAP is sensitive
to calculation/source omission. This narrows an RQ toward a matched ligand,
dose and activation-context comparison; it does not identify which changed
factor caused the difference. Published low-dose enhancement was already
specified by Gorby et al. (2020), Figs. 5–6; see the linked result for exact values,
primary attribution and normalization/donor limitations.

The other two directions remain specific interaction questions requiring missing
intervention arms and response measurements. Receptor RNA, keyword hits and
separate studies cannot substitute for those arms. IL-10/IL-18 coactivation and
IFN-primed IL-22 signaling are already published premises. Existing negative
acute B3/Osmr evidence remains unchanged.

## Separate technical execution

Plans/initial source contracts were frozen at `b886c7c`. The first workbook
qualification was retained as ineligible. A Windows line-ending issue between
working bytes and committed JSON bytes was documented and repaired with scoped
exact-byte attributes, not with a relaxed validator. [Correction](../../../Research%20Article/gate3_07_saxton_2021_il10/extensions_20261108/FREEZE_CORRECTION.md).
Final checking found that the root attribute file is itself a historical Choi
dependency. Its exact original bytes were restored and equivalent rules moved
into the two new Saxton folders; the correction record retains this failed check.
V2 source screens ran at `4fb14dd`; the numerical contract and three scripts
were frozen at `d31c123`. Exact Git blob hashes were checked before these runs.

The numerical job produced all 36 source records, 36 contrasts, 48 summaries and
a PNG/PDF figure. A separate raw-table/Decimal implementation verified 324
scalars within 1e-10 tolerance. The PNG was visually inspected: six readable
panels, individual codes, zero references, primary means and secondary means;
no omitted unfavorable source or unsupported uncertainty interval.
The [registry](../../../analysis/research/registry.json) locates every contract
and receipt. Raw inputs, acquisition successes/failures and query JSON remain
hash-bound in ignored `raw_data/Saxton_extensions_20261108/`.

Initial numerical preflight exposed unfinished amendment-field serialization;
it was corrected before the first numerical freeze and execution. No numerical
failure or overwrite occurred. The common-matrix scientific failure remains
visible, with an explicit prospective change in endpoint rather than a claim
that the original method passed. No old biological analysis was rerun.

Repository delivery checks and integration-base status are recorded in
[PROGRESS](../../../PROGRESS.md). Parent review of the earlier `16627aa`
technical handoff is separate; these checks do not claim human acceptance or
complete that broader audit.

## Reading needed next

Read the complete biological Results argument and relevant legends/methods in
both Saxton papers before committing to an RQ. A full cryo-EM processing-methods
read is not required for these response/context questions. For route 1, Gorby
Figs. 5–6, S7 and RNA methods supply the immediate comparison; the current pass
read their indexed primary text, not a complete raw-data or figure-image audit.
For route 2, resolve the species/activation differences in Freeman's co-input
experiments. For route 3, obtain Bachmann's full methods before selecting a
priming schedule. The 2026 modeling manuscript remains an access gap; its public
code's source reuse is already documented. No additional broad screen is needed
to turn these missing measurements into an apparent mechanism.
