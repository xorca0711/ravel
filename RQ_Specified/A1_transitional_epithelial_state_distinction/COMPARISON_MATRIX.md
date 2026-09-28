# A1 comparison matrix and the one test worth running next

Written 28 September 2026 as a documentation pass over completed A1 work, implementing the
[combined proposal](../../docs/audits/2026-09-28-rq-development-proposal/PROPOSAL.md)'s A1 item
("choose one decisive comparison within the umbrella"). Nothing was rescored, refitted or
searched for. Every number here is copied from the report that produced it.

Two inventories support this page and carry the detail it summarizes: the
[branch inventory](reports/A1_BRANCH_INVENTORY.md), 27 branches with their features, populations,
units, verdicts and missing inputs, and the
[outcome inventory](reports/A1_A8_A14_OUTCOME_INVENTORY.md), 29 measured mature-epithelial
outcomes shared with A8 and A14.

## The question A1 is trying to answer

Do regulatory programmes distinguish RNA-similar transitional epithelial states, and do they
carry information about what those states later do? The proposal words the next primary test as:
*does a specified early regulatory feature add information about a later measured mature
epithelial outcome beyond early RNA, within a defined transitional population?*

## The finding that governs the nomination

**No A1 branch can currently instantiate that test, and the obstacle is linkage rather than
evidence volume.** Across outcomes O1 to O25 of the outcome inventory, no measured mature
epithelial outcome has an early regulatory measurement recorded in the same experimental units.
The closure ledger states the same conclusion for the branch as a whole: "Histone, lineage and
intervention observations currently come from different experiments"
([EVIDENCE_CLOSURE_REPORT.md](reports/EVIDENCE_CLOSURE_REPORT.md)). The repository's own gate for
A1 is recorded as "Early regulatory and RNA measurements linked to independent later fate at
clone/animal/preparation level; RNA-only replacement does not qualify"
([gap-fill ledger](../../docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md)).

This is not a negative result about the biology. It is a statement about which measurements exist
in which animals, and it means the useful next step is a linkage design, not another analysis of
the present matrices.

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
| Tsutsui perturbation (B19-B21) | CUT&Tag; RNA and reporter endpoints | iPSC-derived culture | culture endpoint | 64 runs; 65 endpoint summaries; 1 parental line | library identities, culture endpoints | partial, but the outcome is RNA | same-layer circularity; one donor |
| CD44 genotype contrasts (B23) | sorted bulk RNA | transported transitional state, 8 mice | single harvest | 8 mice, 4 paired per genotype | paired contrasts and direct interaction, completed | **none** | state definition is RNA-transported |
| Methylation reference (B24) | WGBS domains | promoter context | n/a | 1 donor, 414 intersection checks | genomic context | **none** | single donor; context, not outcome |
| TP53 source lists (B22), TIGIT (B18), comparators (B25-B27) | supplied gene lists; paired ATAC; deposited tracks | various | various | lists or held records | direction audits, holds | **none** | inputs absent or identities unresolved |

## Nominated primary test

**Nomination: link the existing IRE1-alpha early regulatory/RNA measurement to the existing
day-14 mature endpoint in one cohort of animals, then ask whether the early feature adds
information about the later endpoint beyond early RNA.**

This is nominated because the two halves already exist and are already frozen, and only their
co-measurement is missing. The day-7 epithelial RiboTag RNA (B7: ten mice, five per arm, eight
frozen features, estimates stable under leave-one-mouse-out) and the day-14 AGER endpoint under
KIRA8 (O3) are the same intervention at two timepoints, but they are "different experiments and
different experimental units" ([FIRST_BATCH_REPORT.md](reports/FIRST_BATCH_REPORT.md)). No other
family in the matrix comes as close: the PATS lineage endpoint has a measured mature fraction but
its chromatin comes from separate sorts, and the histone, HPCS, CD44 and Tsutsui families have no
later outcome in any units at all.

| Element | Specification |
|---|---|
| Population | epithelial compartment under the recorded KIRA8 and vehicle arms, transitional state defined independently of the scored features |
| Early predictor | the eight frozen day-7 features, fixed before outcomes are inspected; a named regulatory feature enters only if measured in the same animals |
| Later outcome | the day-14 mature endpoint (AGER-based), measured per animal, not an RNA score |
| Beyond-term | early RNA in the same animals; the test is added information over it, never a bare association |
| Unit | the animal; at least the existing five per arm, with identities deposited |
| Estimand | added information about the day-14 endpoint from the early feature, conditional on early RNA, per arm |
| Decision | a positive result nominates an early-to-later informational link and licenses no causal claim; a null leaves the regulatory distinction descriptive; an inconclusive result is reported as such |
| Stop rule | if the two measurements cannot be obtained in the same animals, the test is not attempted with cross-cohort pairing, and A1 retains its evidence synthesis |

**What this nomination is not.** It is not a computational task that can start now. It requires
an experiment or an author-supplied cohort in which both measurements exist per animal. Prediction
here is not causation, and a positive result would not establish that the regulatory feature
controls fate.

## Supporting roles of the remaining branches

- **Histone families (B1-B5)** supply the frozen loci and the mark definitions any future
  regulatory predictor would use, plus the promoter-definition and normalization sensitivities
  that bound it. They are instrument development, not candidate tests.
- **HPCS families (B12-B17)** supply verified animal identities and the design algebra showing
  which contrasts are identifiable. Their value is to prevent a future test being specified on
  non-identifiable units.
- **CD44 (B23)** is the completed within-study genotype contrast and is the clearest evidence
  that familiar transitional markers change in both wild-type and mutant lungs, which is why a
  marker panel alone cannot define the population for the nominated test.
- **AP-1 (B10, B11)** supplies the regional heterogeneity that any whole-lung outcome would
  average over, and its three-mice-per-genotype resolution is a warning about the unit count.
- **Tsutsui (B19-B21)** is the only family with chromatin and an endpoint in one system, and its
  limitation — same-layer circularity and a single parental line — defines what "noncircular"
  has to mean in the nominated test.

## Shared outcome inventory for A8 and A14

The [outcome inventory](reports/A1_A8_A14_OUTCOME_INVENTORY.md) is the shared sourcing the
proposal asks A8 and A14 to use rather than each assembling its own. Three results from it bear
directly on those two questions.

- **A8's mature AT1 endpoint (O27) is missing entirely**, not merely unlinked: it needs the
  outcome measured in independent animals, with predictor timing specified and the predictor not
  defined from the outcome's own genes.
- **A14's recovery endpoints (O28) need the experiment**: independent preparation-level
  observations linking exposure duration or reception to viable traced mature output with
  documented timing.
- **No EdU, BrdU or label-retention assay is named anywhere in the A1 evidence (O29).** The only
  Ki67-related record is an Mki67-tagRFP sorting gate in the GSE141635 metadata. This is a
  coverage gap in the record, not a measured negative, and it matters because several proposed
  designs across A1, A8, A14 and A16 assume a proliferation readout is available.

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

A1 proceeds to a new primary analysis only when one cohort carries an early regulatory or RNA
measurement and an independent later mature outcome in the same animals, clones or preparations.
Until then the branch retains its evidence synthesis and adds no further disconnected assay. This
matrix is the record of that decision and of which single linkage would unblock it.