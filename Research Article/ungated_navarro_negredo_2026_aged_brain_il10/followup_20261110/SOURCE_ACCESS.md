# Public source acquisition record — 10 November 2026

Raw downloads remain under ignored `raw_data/navarro_2026/followup_20261110/`.
The [frozen input manifest](../../../analysis/research/runs/nn26_public_source_followup_v1/input_manifest.json)
records every input's exact byte count and SHA-256. Do not overwrite a different
future response to reproduce this snapshot; use a new version and record its
actual source date. The [qualified source snapshot](../../../analysis/research/runs/nn26_public_source_followup_v1/source_refresh.json)
and [GSM/library crosswalk](../../../analysis/research/runs/nn26_public_source_followup_v1/public_sample_crosswalk.csv)
retain the scientific metadata used in interpretation.

| Input | Exact public route |
|---|---|
| Current six BioSamples | [Entrez efetch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=biosample&id=SAMN53298929,SAMN53298930,SAMN53298931,SAMN53298932,SAMN53298933,SAMN53298934&retmode=xml) |
| Current project run report | [ENA read_run](https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA1365936&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,library_name,library_strategy,sample_title,experiment_title&format=tsv) |
| Latest data/code identities | [Data latest](https://zenodo.org/api/records/17594828/versions/latest), [code latest](https://zenodo.org/api/records/18174039/versions/latest) |
| Author code identity | [Commit](https://api.github.com/repos/PalomaNavarro/TargetingImmuneCellsSVZ/commits/c08010bb29f0cb9b56143a25f6a2b1c28692cf70), [tree](https://api.github.com/repos/PalomaNavarro/TargetingImmuneCellsSVZ/git/trees/c08010bb29f0cb9b56143a25f6a2b1c28692cf70?recursive=1) |
| GSE318914 sample metadata | [Family SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE318nnn/GSE318914/soft/GSE318914_family.soft.gz) |
| GSE318914 count matrix | [Processed gene counts](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE318nnn/GSE318914/suppl/GSE318914_PBMC_Gene_Expression_Count.featureCounts.txt.gz) |
| GSE318915 sample metadata | [Family SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE318nnn/GSE318915/soft/GSE318915_family.soft.gz) |
| GSE318915 count matrix | [Processed gene counts](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE318nnn/GSE318915/suppl/GSE318915_Tcell.Gene_Expression_Count.featureCounts.txt.gz) |

Entrez used the `ncbi-entrez-skill` wrapper with explicit endpoint/database,
bounded results and saved raw responses for repository provenance. The GDS
search response mixes series and sample UIDs; it is not a count of independent
studies. Exact queries and unsuccessful browser routes are in the
[follow-up report](README.md#5-verification-access-record-and-remaining-decisions).
Standard public GEO text/HTTPS download routes succeeded. There was no author
contact or access-control workaround. The original S4 and other source inputs
were reused only after matching their existing contract hashes.
