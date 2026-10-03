# A5 v2 identity-schema stop

The frozen v2 contract stopped before producing an inventory: the BioSample
records do not include a reverse GEO identifier. The parser required that field.
This is an accession-schema mismatch, not a biological negative result or evidence
that these public samples lack provenance. The runner's missing-inventory error
is secondary to the parser's explicit missing-GEO-identity exception.

The [original receipt](A5_FAILED_RECEIPT.json) is retained byte for byte with
`execution_failed` and no outputs. It is a failure archive, not a successful
registered receipt. Full logs are retained privately and under ignored raw_data;
the traceback contains a local machine path. The original run directory was
preserved in ignored storage, not overwritten or silently retried.

The new A5 v3 contract uses the explicit GEO-to-BioSample accession and requires
the BioSample submitter library alias to match the MUC identifier at the start of
the GEO title. Any provided reverse GEO identifier must agree. Absent reverse
links remain explicitly absent. Neither version supplies a mouse or cell-state
join. The frozen v2 contract/parser remains unchanged.

Original file hashes:

- `receipt.json`: `53ce5846e7c21d52845e251cd28fa66a0aaac2f0338a220a1e8793f0f918d13f`
- `stderr.log`: `8edc8916d9d43e20b96aa53d2cec6f338f890202eb82edb77ceb08af832277a0`
- `stdout.log`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
