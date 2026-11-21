# RNA description validation

1 November 2026. [Results](RNA_RESULTS.md); [receipt](../../analysis/research/runs/arz1_rna_description_v1/receipt.json).
Freeze: `a9e469e8fbd09ccbaeae3610bdeae2e69497c616`.
Parent scope base: `7d7b721f486a2be3af0593fb20011ef33cd6f416`.

Eight targeted synthetic tests passed before execution. They distinguish all-source
from common-only denominators, pooled from equal weighting, transformation after
averaging from averaging transformed barcodes, inclusive QC boundaries, zero-depth
and empty subsets, ambiguous symbols/mitochondrial labels, sparse-format agreement
and invalid duplicate/fractional RNA entries. Exact staged bytes were checked for
the implementation/specification, including the archival brief copy. Its bytes
equal the parent brief's Git blob; the original brief and every prior freeze are
unchanged. Input preflight and base-aware research gate passed before execution.

The runner completed all seven libraries and all 15 expected outputs. Receipt
verification passed. No target-map or empty-subset holds occurred. Both PNGs were
visually inspected at their generated resolution: signed values, case labels,
units, source labels, legends and interpretation notes are legible without clipping.
SVG versions and the exact numerical plotting input are preserved alongside them.
No result file or figure was changed after execution.

The originating reviewer independently reconstructed raw selected-target counts
and barcode-QC sets for all seven libraries, successfully checking the source
inputs without importing production analysis code. The full saved-table arithmetic
audit remains with originating review at this technical handoff; it is not claimed
complete here.
Both actual PNGs also passed originating visual review; they were not regenerated.
A successful runner alone is not independent numerical review or biological
replication.

Final repository checks passed against freshly fetched, unchanged
`origin/main = 51d3b930b3805c616e67e414390ecf060647d090`: 13,058 repository checks,
base-aware research gate, compile check, 158 shared tests successful with two
Windows skips, 18 claim bindings, and all required Nabhan, Travaglini/Nabhan,
A16, A23 and A22/A23 archive/evidence verifiers. Logs are retained locally under
`.tools/arz1_rna_validation/`. The eight unchanged synthetic RNA tests were reused
from the pre-execution freeze; no numerical run or figure was repeated.

The final staged-byte check caught the repository's general gzip ignore rule;
the four declared compressed tables were explicitly staged. All 18 run files
(15 outputs, receipt and two logs) match worktree bytes exactly. A plain
`git diff --check` has two new formatting exceptions: the frozen Matplotlib SVG
files contain trailing spaces in path data. They remain unchanged because the
receipt hashes and passed visual review bind those exact artifacts. No attribute,
validator or whitespace rule was weakened. All other new files are whitespace
clean; the broader PR's three older Saxton exceptions also remain preserved.

Q4a consists only of bounded source/header/annotation reading and resource
assessment. It generated no fragment counts or accessibility contrasts. Prefix
hashes are not full-file hashes. The observed GRCm39/ARC2.1 conflict is preserved
separately from the article/GEO mm10/ARC2.0.2 statements and was exposed before the
RNA numerical freeze. The RNA numerical workflow performs no genomic remapping.

Parent-owned README, literature context, PROGRESS and PR integration were not
edited by this technical phase. No push, main merge, governance/validator change,
claim-grade promotion or human scientific decision was made. Next scientific
step is originating numerical/visual review and a separate Q4a brief if accepted.
