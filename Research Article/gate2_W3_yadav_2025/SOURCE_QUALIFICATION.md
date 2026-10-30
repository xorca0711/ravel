# Yadav source qualification: first review checkpoint

Metadata-only owner **Yd1-P01** supports the existing Wg-P06 context question.
It introduces no canonical A ID, biological hypothesis or acceptance decision.
The six-step [article plan](README.md) remains the scope. Published outcomes and
workbook values are exposed. No dependent effect analysis is authorized at this checkpoint.

## Frozen scope

The [versioned contract](config/source_qualification_v1.json) binds the official
workbook, GEO SOFT and count archive, linked BioSample and ENA experiment XML,
and supplied article/supplement copies. The runner inventories cell labels,
accession relationships and count-file structure. It does not estimate effects.

## Acquisition and preservation

Recovered 30 October 2026 (Asia/Seoul). Inputs are ignored, immutable copies under
`raw_data/Yd1_source_v1/` in the execution worktree. Preserve this worktree/cache.
The review cache and original checkout were read only.

- Workbook: [official Supporting Data Values](https://www.jci.org/articles/view/188734/sd/4), [exact XLSX](https://dm5migu4zj3pb.cloudfront.net/manuscripts/188000/188734/JCI188734.sdval.xlsx).
- GEO: [series](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE242510), [SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE242nnn/GSE242510/soft/GSE242510_family.soft.gz), [count archive](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE242nnn/GSE242510/suppl/GSE242510_RAW.tar).
- BioSample: NCBI EFetch `db=biosample`, accessions SAMN37307448 through SAMN37307453, XML response saved as `biosamples.xml`.
- Sequencing experiment: ENA browser XML API, SRX21653362 through SRX21653367, saved as `experiments.xml`.
- Main PDF: owner-supplied 16-page final JCI article, copied as `article.pdf`; supplied copy includes reading annotations.
- Supplement: seven-page publisher supplement, copied from the read-only review cache as `supplement.pdf`.

The web viewer challenged the GEO page; direct official SOFT retrieval succeeded.
Initial sandbox writes/DNS failed; authorized escalated retrieval succeeded.
No source file was substituted or modified. Source hashes and exact accession
joins will be preserved in the governed run receipt and output inventory.

## Pending execution

Run source qualification after committing the frozen contract and code. Then
record the claim/assay ambiguities, per-job eligibility and independent checks
here. Keep all population-inference holds until the required units qualify.
