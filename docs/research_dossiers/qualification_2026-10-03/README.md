# Source and capability qualification, 3 October 2026

**The fresh metadata checks resolve source identities, but do not establish the missing biological replication or outcome linkage.** All 24 questions and nine Nb4 candidates remain available. This stage does not select an RQ, promote a claim or declare a wet experiment ready.

Four exposed metadata contracts were frozen with their parser at commit `6ef2cf9d3017722297d3b5f4a3f5cbb8e1d9cee1`, then executed through the repository runner. Five public GEO SOFT files supplied the metadata. No expression matrix was downloaded or scored and no inferential biological model ran. Published results and selected metadata had already been seen; these are prospective execution records, not blinded validation.

- [Fresh metadata results](RESULTS.md): A2/A9, A5, A7 and A10/A22, with run receipts and exact source distinctions.
- [Portfolio disposition](PORTFOLIO.md): all 24 RQs and nine Nb4 candidates; fresh findings and carried-forward source holds are distinguished.
- [Capability requirements and exact enabling exports](CAPABILITIES.md): what a source or collaborating lab must provide; no access is assumed.
- [A11 primary-source comparison](A11_PRECEDENTS.md): established HPCS findings and the narrower unresolved contribution.
- [Source versions and hashes](SOURCES.md) and [verification](VALIDATION.md).

This is a completed bounded qualification pass, not an exhaustive search for every possible dataset. Existing source audits were reused where no new evidence justified repeating them. Public metadata can establish an accession, assay or missing field without establishing that a requested export exists nowhere else.

## Decisions from this stage

| Source | Decision |
|---|---|
| GSE169125, MesSTIM | Retain as a recipient-expression source lead. Do not use it to claim delivery, receptor competence or independent biological inference without preparation mapping and appropriate measurements. |
| GSE303646, A5 | The deposited 56-library inventory matches the prior crosswalk. The mouse mapping and author per-cell state export remain missing; the replication hold remains. |
| GSE247130 / GSE310539, A7 | Keep CEBPA and AP-1 sources separate. Paired RNA/ATAC records and pooled conditions cannot be promoted to genotype replicates. |
| GSE307351, Nb3 | Use the organoid and spatial subseries separately. Their deposited identities confirm existing accounting, not additional independent preparations. |

The first real use of the new runner also exposed a publication issue: it recorded machine-specific executable/worktree paths in receipts. New receipts now record repository-relative replay commands while executing with resolved paths. A regression test verifies that behavior; hashes, freeze checks, unit gates and historical evidence protections remain intact. This change is disclosed for review in draft PR #130, not presented as independent human approval.

## What can advance next

The next useful work is the exact source-export recovery listed in CAPABILITIES.md and, when available, a real laboratory capability record. Recovering a missing join may enable a bounded exploratory analysis; an unavailable endpoint requires another source or a genuinely new measurement. Repeated score fitting on the same data cannot substitute for those inputs.

Keep exploratory/descriptive work available under new contracts when it can answer a named decision. A hold on a causal, predictive or confirmatory claim is not a ban on all research. Before any new fit, specify its biological unit, actual endpoint, prior exposure, rival, uncertainty and stop rule. Owner review of the corrected scientific scopes remains pending, and draft PR #130 remains unmerged.
