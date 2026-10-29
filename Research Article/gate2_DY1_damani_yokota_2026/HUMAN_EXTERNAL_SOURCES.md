Current disposition: the discovery checkpoint below predates the executed
[assay qualification and bounded external plan](HUMAN_EXTERNAL_PLAN.md).
Its original uncertainties are retained as historical search evidence. The
subsequent raw-assay audit resolves RNA identity for the nine outcome genes;
SELENOP and exact NAM reproduction remain unqualified.

# Bounded discovery of external human cohorts

29 October 2026. Purpose: assess leads for the conditional external-cohort step
in the reviewed stage 7. This is source discovery, not a qualified replication
cohort or a new numerical analysis. Expression matrices were not inspected.

## Search and access

Two live primary-source searches used the queries:

- `GSE122960 Reyfman pulmonary fibrosis single cell human donor metadata`
- `GSE135893 pulmonary fibrosis single cell donor macrophage Habermann 2020`

The domain filter was NCBI/PMC. Indexed GEO records were returned; direct web-reader
opens of both series and PMID32832598 returned a client challenge. Public GEO text
records were then read from the standard `targ=self&form=text&view=full` endpoint.
The exact query URLs, retrieval timestamps and returned source fields are saved
in `independent_human_candidates.json`. No raw sequencing data were retrieved.

## Candidate findings

[GSE135893](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135893), Habermann
et al., links processed matrix, gene/barcode tables, an annotated object, metadata
and a processing README. Its series summary describes 20 fibrotic and 10 control
lungs; 34 sample records must not be equated with independent donors. The metadata
header includes Diagnosis, Sample_Name, Sample_Source, Status, population and
celltype. The public README describes the processed annotation workflow; this
has not been shown equivalent to the Damani-Yokota NAM annotation.

[GSE122960](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122960), Reyfman
et al., has 17 sample records and public processed HDF5 count files. The summary
describes eight donor and eight fibrotic lungs plus an early-disease biopsy;
the overall-design field says eight donor and nine fibrotic lungs. Diagnoses span
forms of fibrosis, so the disease group cannot automatically be called IPF.

## Remaining qualification

Neither source is yet qualified as independent participants or comparable cell
populations. Recover donor-to-library/barcode joins, diagnoses, preparation and
annotation conventions, and evaluate potential participant/source overlap with
GSE136831. Different accession numbers or local identifiers do not prove
independence. Full primary methods/figure reviews and exact planned comparison
matching remain outstanding. This bounded search does not establish novelty,
exhaustive coverage or that external validation is impossible.

A subsequent primary-source check of [Liu et al. 2024](https://academic.oup.com/ajrcmb/article/71/2/229/8405611),
Results on atlas generation and Fig. E1C, reports an expression-scale discrepancy
for some GSE135893 genes and separate handling of that dataset. Thus the identity
of the deposited assay (raw UMI versus corrected/other processed values) requires
verification before borrowing the primary cohort's normalization. This is a
measurement warning from a published comparison, not proof that GSE135893 cannot
support a suitably qualified external description.

The [Habermann primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7439444/)
was subsequently inspected at Results (opening and final paragraphs), Subjects
and samples, and reference 49. It reports 12 IPF cases, eight other fibrotic cases
and ten controls, with collection at VUMC and NTI. Its final Results paragraph
explicitly describes the Adams companion study (reference 49;
DOI 10.1126/sciadv.aba1983) as using a separate dataset and pipeline. This is
published evidence supporting separate source collection; it is not a direct
patient-identity audit. Exact donor/library joins, assay semantics and annotation
matching still determine numerical eligibility. An IPF-specific comparison must
not relabel all fibrotic cases as IPF.

## Cached discovery files

The coordinating review's original discovery files are preserved in this article's `source_metadata/external_human_v1/` directory; the public metadata is retained in ignored `raw_data/DY1_human_external_v1/`:
`GSE122960_candidate.txt`, `GSE135893_candidate.txt`,
`independent_human_candidates.json`,
`GSE135893_readme_for_ILD_annotated_fullsize.rds.txt` and
`GSE135893_IPF_metadata.csv.gz`.

The metadata download is 3,354,014 bytes, SHA-256
`5c67b3717375859aafc4463024847cf30d7af7bb9d5f4ad9a5364ee6d7726bf5`.
The 642-byte README has SHA-256
`a7f878eb36efe4e549ae00538973da7c51de2cdbcf855058ba5d1ff9fdc788ab`.
Source metadata exposure must be recorded in any later prospective contract.
