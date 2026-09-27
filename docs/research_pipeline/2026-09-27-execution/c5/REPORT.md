# C5: the A11 acute-injury contrast is unresolved, and the cells scored are bystanders

27 September 2026. Executed under the contract frozen at
[C2](../../config/a11_acute_injury_contract.json), gated at
[C3](../c3/gate_report.json), scored at [C4](../c4/inference.tsv) and verified at
[C5](../c4/verification.json). **No claim row is added and no register grade changes.**

## Verdict

**Unresolved, as the contract predicted before running, and for a second reason it did not
anticipate.** The exact interval is unavailable at four pairs. The direction is consistent under
the frozen instrument but does not survive a change of normalisation. And the type 2 cells the
primary arm scores are 99.4 per cent virus-negative, so whatever is being measured is a bystander
response rather than a cell-intrinsic one.

## The gates passed cleanly

| Gate | Result |
|---|---|
| Module coverage in this object | 73 of 73 lesion genes, fraction 1.000, against a 0.7 gate |
| Eligible pair recomputation | SCoV1 4, SCoV2 3, MERS 2, H3N2 1, matching the contract exactly |
| Raw integer counts | confirmed at C1 |
| Pseudobulk | 11 units, 50,558 genes, 2,370 type 2 cells, every unit above the inherited 50-cell floor |

## The primary result

Per-donor difference in the lesion score, infected minus the medium-matched control, in log2 CPM.

| Test | n | Mean | Donors positive | Exact interval |
|---|--:|--:|---|---|
| **SARS-CoV-1, lesion_specific** | 4 | **+0.260** | **4 of 4** | unavailable |
| SARS-CoV-1, stress_excluded | 4 | +0.258 | 4 of 4 | unavailable |
| SARS-CoV-1, beyond_shared | 4 | +0.173 | 3 of 4 | unavailable |
| SARS-CoV-2, lesion_specific | 3 | +0.141 | 2 of 3 | unavailable |
| SARS-CoV-2, stress_excluded | 3 | +0.138 | 2 of 3 | unavailable |
| SARS-CoV-2, beyond_shared | 3 | +0.008 | 3 of 3 | unavailable |

The exact paired test the contract designated returns no interval and no p-value on any test, which
the contract declared in advance would happen at these unit counts. The instrument refused rather
than substituting an approximation, which is what it is built to do. For orientation only, the
t-based interval on the primary is -0.055 to +0.574 with a nominal p of 0.079, so even the
approximate test does not reach 0.05 and the interval excludes neither zero nor the 0.10 margin.

The stress-excluded variant tracks the primary almost exactly, +0.258 against +0.260, so the
movement is not carried by the stress genes. The beyond-shared contrast is noisy, because the
shared component moves too and in one donor moves further than the lesion score.

## What the verification found

Seven of eight checks passed: the pseudobulk holds only non-negative integers, its per-unit totals
match the library sizes the scoring recorded, the cell counts agree with C3, every unit clears the
floor, the paired differences follow from the per-unit scores to within 8e-15, all 73 genes are
present, and the exact interval is unavailable everywhere as predicted.

**The eighth check is a robustness probe I added, and it fails.** Recomputing the primary contrast
from raw counts with plain counts-per-million and no trimmed-mean normalisation gives a mean of
+0.090 with three of four donors positive, against +0.260 with four of four under the frozen
instrument. The effect shrinks to about a third and one donor changes sign. That is not a contract
violation, because the contract inherited the trimmed-mean normalisation from A11 and inheriting it
was the right call, but it does mean the consistency of the direction is partly a property of the
normalisation rather than of the data.

I checked the obvious culprit and it is not the cause. The count matrix does contain viral
transcripts, 34 SARS-CoV-2 entries, 10 influenza and 9 MERS, so viral reads sit inside the library
sizes. In these type 2 libraries they are negligible, between 0 and 10 counts against millions, and
host-only normalisation gives numerically identical scores. The divergence is a genuine host-gene
composition effect.

## The finding the contract did not anticipate

Per-cell virus detection in the type 2 compartment, from the object's own field:

| Arm | Type 2 cells | Virus-positive |
|---|--:|--:|
| control | 1,171 | 0, 0.0% |
| **SARS-CoV-1, the primary arm** | 1,270 | **7, 0.6%** |
| SARS-CoV-2, the secondary arm | 702 | 6, 0.9% |
| H3N2 | 887 | 138, 15.6% |
| MERS-CoV | 702 | 309, 44.0% |

In the four eligible donors the primary arm's type 2 cells are between 0.0 and 1.5 per cent
virus-positive. **So the primary contrast compares mock type 2 cells against almost entirely
uninfected type 2 cells in an infected explant.** Any movement is a bystander or microenvironment
response, not a response of infected cells.

That is still a legitimate acute-injury challenge to a tumour-exclusive reading of the programme,
and arguably a cleaner one, since it is not confounded by direct viral takeover of the cell being
measured. But it is a different claim from the one a reader would assume, and the report says so
rather than letting the arm label imply cell-intrinsic infection.

The tension is structural. The two arms where type 2 cells are actually infected, MERS at 44 per
cent and influenza at 15.6 per cent, are the two the inherited unit floor declares ineligible, at
two and one eligible pairs. Coverage and infection point in opposite directions in this cohort.

## What this establishes

**Establishes.** Nothing about acute induction. The contract's decision rule returns unresolved,
which is what an unavailable exact interval means, and the normalisation sensitivity and the
bystander composition both argue against reading the point estimate as a finding.

**Establishes as a design record.** That this cohort cannot carry the A11 acute-injury
falsification with A11's inherited instrument and floors. The arm with adequate paired coverage has
an essentially uninfected target compartment, and the arms with an infected target compartment fall
below the unit floor. That is a property of the deposit, not of the hypothesis.

**Does not establish.** Tumour specificity in either direction, which the contract ruled out in
advance. Nor an absence: four pairs bound nothing.

## What would settle it

A cohort with more donors per infected arm, or a compartment-resolved design that scores infected
and bystander type 2 cells separately, which would need enough virus-positive type 2 cells per
donor to pass a floor. On these numbers only MERS-CoV comes close, at 309 virus-positive type 2
cells across two eligible donors, and two donors cannot carry a paired test.

## Proposed wording, not graded here

1. **Not established.** In GSE198864 lung explants, the frozen A11 lesion programme in
   author-annotated type 2 cells differs between SARS-CoV-1 infected and medium-matched mock
   explants by a mean of +0.260 log2 CPM across four paired donors, positive in all four, but the
   exact paired interval is unavailable at that unit count and the effect falls to +0.090 with
   three of four positive when the trimmed-mean normalisation is dropped.
2. **Descriptive, and it bounds the design.** The type 2 cells scored in that arm are 0.6 per cent
   virus-positive, so the contrast measures a bystander response; the arms whose type 2 cells are
   substantially infected, MERS-CoV at 44.0 per cent and H3N2 at 15.6 per cent, have two and one
   eligible pairs against an inherited three-unit floor.
