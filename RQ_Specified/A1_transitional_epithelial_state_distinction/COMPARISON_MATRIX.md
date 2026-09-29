# A1 comparison matrix and requirements for the next primary test

Written 28 September 2026 as a documentation pass over completed A1 work, implementing the
[combined proposal](../../docs/audits/2026-09-28-rq-development-proposal/PROPOSAL.md)'s A1 item
("choose one decisive comparison within the umbrella"). Nothing was rescored, refitted or
searched for. Every number here is copied from the report that produced it.
Corrected 29 September 2026 after the [delivery review](../../docs/audits/2026-09-29-rq-delivery-review/REPORT.md):
the IRE1-alpha RNA linkage is a supporting candidate; a regulatory primary test remains unspecified.

Two inventories support this page and carry the detail it summarizes: the
[branch inventory](reports/A1_BRANCH_INVENTORY.md), 27 branches with their features, populations,
units, verdicts and missing inputs, and the
[outcome inventory](reports/A1_A8_A14_OUTCOME_INVENTORY.md), 29 inventory records covering
measured outcomes, contextual readouts and unmet requirements shared with A8 and A14.

## The question A1 is trying to answer

Do regulatory programmes distinguish RNA-similar transitional epithelial states, and do they
carry information about what those states later do? The proposal words the next primary test as:
*does a specified early regulatory feature add information about a later measured mature
epithelial outcome beyond early RNA, within a defined transitional population?*

## The finding that governs the nomination

**No A1 branch can currently instantiate that test: a specified regulatory predictor and
compatible unit-level linkage are both required.** Across outcomes O1 to O25 of the outcome inventory, no measured mature
epithelial outcome has an early regulatory measurement recorded in the same experimental units.
The closure ledger states the same conclusion for the branch as a whole: "Histone, lineage and
intervention observations currently come from different experiments"
([EVIDENCE_CLOSURE_REPORT.md](reports/EVIDENCE_CLOSURE_REPORT.md)). The repository's own gate for
A1 is recorded as "Early regulatory and RNA measurements linked to independent later fate at
clone/animal/preparation level; RNA-only replacement does not qualify"
([gap-fill ledger](../../docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md)).

This is not a negative result about the biology. It is a statement about which measurements exist
in which animals. The next step is to specify the regulatory measurement, its RNA comparator
and a feasible linkage to a later outcome before another primary analysis.

## The matrix

Branch families, with the detail per branch in the [branch inventory](reports/A1_BRANCH_INVENTORY.md).
"Layer" distinguishes what was actually measured, because the umbrella spans four assay layers
that are not interchangeable. "Linked outcome" is the column that decides the nomination.

| Family | Layer measured | Population | Timing | Unit and n | Endpoint reached | Linked later outcome in the same units | Principal rival |
|---|---|---|---|---|---|---|---|
| Native-assembly histone tracks (B1, B2) | H3K27ac, H3K4me3, H3K27me3 against matched H3 | iATC / iAT2 / iAT1 induced states | culture endpoint | 2 CUT&Tag preparations per state; 23 loci, 46 TSS positions | mark levels and promoter-definition robustness | **none** | one parental line; preparations are not donors |
| PATS deposited chromatin (B3, B4, B5 pruned) | deposited histone tracks and called intervals | PATS sort, day 8 and day 12 | days 8-12 | 20 GSM records, 2 replicates | normalization and interval-geometry audits | **none** | per-library scaling unexecuted |
| PATS lineage endpoint (B6) | lineage label, microscopy | KRT8 and AGER fractions | pulse day 7, harvest day 12 | 3 named mice per marker | measured mature fractions | **none** — chromatin came from separate sorts | 18 zero-denominator control fields cannot form an arm |
| IRE1-alpha RNA (B7, B8) | epithelial ribosome-associated RNA | epithelial compartment under KIRA8 | day 7 | 10 mice, 5 per arm | 8 frozen features, leave-one-mouse-out stable | **none in these mice** | batch structure; published day-14 endpoint is a different cohort |
| IRE1-alpha cell-resolved follow-up (B9) | scRNA | epithelium, saline vs bleomycin | post-injury | 1 pooled GEM library per condition | held | no demultiplexed mice | pooling removes animal-level replication |
| AP-1 regulatory context (B10, B11) | regional HOPX protein; bulk ATAC peaks | mutant vs wild-type lung regions | post-viral time points | 3 mice per genotype, 3 fields; 14 ATAC records | opposite regional HOPX responses | **none** | 3 mice per genotype fixes permutation resolution at p=0.10 |
| HPCS lineage and identity (B12-B17) | RNA state labels; identity and design audits | traced HPCS descendants | chase | 5,333 traced cells, 22 animals | source composition, abstention audit, design identifiability | **none** — labels are RNA | chase and library are not separately identifiable |
| Tsutsui perturbation (B19-B21) | CUT&Tag; RNA and reporter endpoints | iPSC-derived culture | culture endpoint | 64 runs; 65 endpoint summaries; 1 parental line | library identities, RNA and reporter culture endpoints | **not established** — CUT&Tag and endpoint preparations are separate | RNA-endpoint circularity; unlinked reporter measurement; one parental line |
| CD44 genotype contrasts (B23) | sorted bulk RNA | transported transitional state, 8 mice | single harvest | 8 mice, 4 paired per genotype | paired contrasts and direct interaction, completed | **none** | state definition is RNA-transported |
| Methylation reference (B24) | WGBS domains | promoter context | n/a | 1 donor, 414 intersection checks | genomic context | **none** | single donor; context, not outcome |
| TP53 source lists (B22), TIGIT (B18), comparators (B25-B27) | supplied gene lists; paired ATAC; deposited tracks | various | various | lists or held records | direction audits, holds | **none** | inputs absent or identities unresolved |

## Primary test not yet specified; IRE1-alpha as a supporting candidate

**The decisive regulatory primary test remains unspecified.** The existing IRE1-alpha day-7
epithelial RiboTag features are RNA measurements, not a separate regulatory predictor that can
be tested for added information beyond early RNA. Linking them to a later endpoint would
address a supporting RNA-to-outcome question; it would not meet A1's regulatory gate.

The IRE1-alpha branch is a candidate for linkage assessment because it provides day-7 RNA
(B7: ten mice, five per arm, eight frozen features) and a published day-14 AGER endpoint under
the same intervention (O3). However, these are "different experiments and different experimental
units" ([FIRST_BATCH_REPORT.md](reports/FIRST_BATCH_REPORT.md)). Their existence does not
establish that the measurements can be linked longitudinally, and no cross-cohort pairing is
permitted. The day-14 endpoint's unit count and usable numerical source also require verification.

| Element | Requirement for the regulatory primary test | Current evidence / gap |
|---|---|---|
| Population | A defined transitional population independent of the scored features | The IRE1 RNA is from an epithelial compartment; its suitability for this population must be established |
| Early regulatory predictor | A named regulatory measurement, its assay and scoring rule specified before outcome inspection | Not nominated; the eight day-7 RNA features cannot replace it |
| RNA comparator | A specified early RNA baseline measured in the linked biological units | Day-7 RNA exists in ten mice; linkage to regulatory and outcome measurements is missing |
| Later outcome | Independently measured mature epithelial outcome with verified timing and unit identities | Day-14 AGER is a candidate endpoint type, measured in different animals |
| Unit and feasibility | Verified animals, clones or preparations linking both early layers to the later endpoint; an adequate design for the intended contrast | No eligible cohort identified; the historical five mice per RNA arm are not a sample-size justification for a new test |
| Estimand and decision | Added information from the specified regulatory feature beyond the RNA baseline; a meaningful increment and uncertainty rule fixed before fitting | Cannot be finalized without a predictor and identifiable linked design; imprecision is inconclusive |
| Stop rule | Do not substitute RNA-only measurements or pair unrelated cohorts | Retain the evidence synthesis while these requirements are unmet |

**Next action:** assess whether an existing or author-provided cohort can supply the required
regulatory measurement, RNA comparator and later outcome with a feasible unit-level linkage.
The IRE1 RNA-to-outcome candidate may guide sourcing, but it is neither an executable analysis
nor the nominated decisive regulatory test. Added predictive information would not by itself
establish causal control of fate.

## Supporting roles of the remaining branches

- **Histone families (B1-B5)** supply the frozen loci and the mark definitions any future
  regulatory predictor would use, plus the promoter-definition and normalization sensitivities
  that bound it. They are instrument development, not candidate tests.
- **HPCS families (B12-B17)** supply verified animal identities and the design algebra showing
  which contrasts are identifiable. Their value is to prevent a future test being specified on
  non-identifiable units.
- **CD44 (B23)** is the completed within-study genotype contrast and is the clearest evidence
  that familiar transitional markers change in both wild-type and mutant lungs, which is why a
  marker panel alone cannot define the population for a future primary test.
- **AP-1 (B10, B11)** supplies the regional heterogeneity that any whole-lung outcome would
  average over, and its three-mice-per-genotype resolution is a warning about the unit count.
- **Tsutsui (B19-B21)** supplies chromatin, RNA differentiation readouts and an AGER reporter
  in an induced-cell system. Separate CUT&Tag and endpoint preparations prevent assumed linkage.
  The RNA readouts raise same-layer circularity concerns; the reporter is a different assay but
  remains unlinked, and one parental line does not establish transport across donors.

## Shared outcome inventory for A8 and A14

The [outcome inventory](reports/A1_A8_A14_OUTCOME_INVENTORY.md) is the shared sourcing the
proposal asks A8 and A14 to use rather than each assembling its own. Three results from it bear
directly on those two questions.

- **A8 lacks an eligible predictor–endpoint linkage (O27).** O2/O3 already record mature
  AT1 protein endpoints on genetically labelled cells. What has not been identified is a
  compatible dataset linking a frozen maturation/shared-transition component to such an
  endpoint in independent biological units. Specified concurrent timing can serve association;
  earlier predictor timing is required for prospective prediction.
- **A14 lacks eligible recovery observations (O28).** Independent preparation-level data must
  link the relevant exposure or reception contrast to viable traced mature output with
  documented timing. Suitable existing or author-provided data may qualify; the inventory
  does not establish that a new experiment is necessary.
- **No EdU, BrdU or label-retention assay is named in the surveyed A1 record (O29).** This
  bounds documented proliferation/retention readouts. It does not erase genetic lineage
  endpoints such as O2/O3, and it does not establish absence from public archives.

**A10's organoid endpoint is bound here and does not qualify as a later outcome.** The
[A10 endpoint statement](../A10_organoid_growth_outcome/reports/ENDPOINT_TIMING_UNITS_2026-09-28.md)
records that its imaging is at days 7 and 14 while the RNA libraries are day-14, so predictor and
outcome are concurrent and in the same well; the day-7 image is the only earlier measurement and
is itself post-perturbation. Its unit is the well — 885 analysed wells in 15 plate-replicate
groups across four plates, with a target's four repeat wells aliquots of one cell-Matrigel
mixture — and no deposited field maps a library to an isolation, animal or donor. A1, A8 and A14
may cite it as a measured, non-RNA, concurrent growth endpoint with an unresolved biological unit;
they may not cite it as the later outcome of an early-feature-to-later-outcome test.

## The gate, restated

A1 proceeds to a new primary analysis only when a specified early regulatory measurement
**and** an early RNA comparator are linked to an independent later mature outcome in verified
animals, clones or preparations. The linkage must be feasible and the intended contrast
identifiable; RNA-only replacement and cross-cohort pairing do not qualify. Until then the
regulatory primary test remains unspecified and the existing synthesis is retained.
