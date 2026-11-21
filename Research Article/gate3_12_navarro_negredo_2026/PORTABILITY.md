# Execution-byte portability — 8 November 2026

The cloud return is imported with exact source/configuration bytes. Package-local
Git attributes preserve those bytes across Windows and Linux checkouts; run
outputs are already protected by the repository's `analysis/research/**` rule.

A targeted comparison of the three earlier Navarro receipts found that the
working copy of `contracts/source_qualification_v1.json` matched its recorded
execution SHA-256, but Git had normalized its CRLF line endings to LF. The other
six declared contract/code/configuration files matched both the working copy
and Git blobs. This discrepancy would break exact receipt verification in a
fresh checkout even though the original Windows working copy verified.

The existing, hash-matching CRLF contract bytes were retained and staged under
the new byte-preservation attribute. No working-file content, contract field,
source input, scientific script, result, or receipt was changed, and no analysis
was rerun. The original freeze commit remains historical evidence of the same
canonical contract text; the current blob now preserves the actual executed
bytes recorded by its receipt. This is a storage correction, not a new analysis
or a claim of unexposed confirmation.
