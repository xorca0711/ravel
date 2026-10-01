# GSE199329 sample roles

Metadata were retrieved from NCBI GEO's compressed SOFT family file on 1 October
2026; [exact fields and download hash](GSE199329_metadata.json). No matrix was
read. The raw metadata cache is ignored; the parsed provenance is tracked.

| GEO sample | Source label | Proposed role |
|---|---|---|
| GSM5970468 | PAM1; CD45-negative PAM lung | Candidate epithelial fraction, pending coverage and annotation |
| GSM5970469 | PAM2; CD45-positive PAM lung | Immune context; not a second independent PAM patient |
| GSM5970470 | D071; normal donor lung, age 24 | Control context; sampling compatibility must be audited |

The [primary article](https://doi.org/10.1038/s41467-023-36810-8) reports a
single PAM child explant and one control. A new grouping key would be an
analysis label grounded in that statement, not a recovered donor identifier.
Do not infer patient replication from the two PAM libraries. Age and disease
cannot be separated with this contrast. CD45 selection also prevents an
unqualified tissue-composition comparison. Published cell counts are not
independent replication and are not adopted as a future QC target.

GEO advertises raw and filtered feature-barcode HDF5 matrices. The HTML page
returned a browser check; the official FTP metadata retrieval succeeded.
The article's source-workbook link was identified but its retrieval failed;
no workbook contents or new expression outcomes have been inspected.
