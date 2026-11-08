# Exact-byte freeze correction before biological contrasts

8 November 2026. The initial metadata freeze `b886c7c` normalized the IL-10
JSON files to LF in Git while their declared working-copy hashes used CRLF.
The first Gorby metadata run completed with the declared runtime bytes; it did
not estimate target effects. Its receipt and outputs are retained, but that
commit alone does not recover the exact declared dependency bytes on every OS.

Scoped `.gitattributes` entries now preserve the existing exact working bytes,
including the original v1 contracts/config, without changing their declared
hashes or content. Version 2 contracts supersede all three metadata freezes;
the unused screen dependency is removed from the Gorby code list. The interaction
screens use the same checks under the corrected freeze. Gorby additionally uses
the distinct [source amendment](SOURCE_AMENDMENT_V2.md), because its first
common-matrix qualification failed; that failure remains unchanged.
This is serialization/provenance repair, not a changed eligibility rule or a
validator relaxation. Original results, contracts and scripts are not overwritten.

Check exact committed blob SHA-256 against every declared code hash before the
v2 runner calls. Register both the original Gorby receipt and the corrected
metadata receipts. The original record remains historical, not independent evidence.
