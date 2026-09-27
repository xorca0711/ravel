# C1 environment gate: the object does not fit in this machine as it stands

27 September 2026, recorded by the session that picked up
[the handoff](../../../handoffs/2026-09-27-computational-research.md). **C1 is not complete
and not failed. It is blocked on memory, and the block is measured rather than estimated.**
No module score was computed, no contract was frozen and nothing was committed.

## What was measured

| Quantity | Value | How |
|---|--:|---|
| File on disk | 2,115,735,865 bytes | as recorded in `retrieval.json`, hash unchanged |
| Outer gzip layer expands to | 1.98 GB | streamed and counted, 9 s |
| That output is itself gzip | magic `1f8b08` | first bytes of the outer layer |
| True serialized size | **7,023,973,824 bytes, 6.54 GB** | inner layer streamed and counted, 28 s |
| Serialization format | R XDR, version 3 | inner header `580a 0000 0003` |
| Memory available | **2.4 GB** | `Win32_PerfFormattedData_PerfOS_Memory` AvailableMBytes |
| Commit headroom | **5.0 GB** of a 29.9 GB limit, 24.9 GB committed | `Win32_OperatingSystem` |

**The file is double gzipped.** The published `.rds.gz` wraps an RDS that R had already
compressed, which is why the outer layer achieves a ratio of 1.00. Anyone estimating the
object from the download size will be out by more than threefold.

## Why the drafted script was not run

[`scripts/inspect_gse198864.R`](../../scripts/inspect_gse198864.R), left untracked by the
previous session, is sound for its purpose: it reads attributes through base R without Seurat,
dumps cell metadata and the metadata field inventory, records assay slots and dimensions,
checks the count matrix for non-finite, negative and non-integer values, and writes per-cell
totals. It computes no module score, which is what C1 requires.

It cannot run here. Its first statement is `readRDS`, which materialises the whole object.
That needs at least the 6.54 GB serialized size and in practice more, against 2.4 GB available
and 5.0 GB of commit headroom. Starting it would page heavily for a long time, fail on
allocation, and put the other sessions on this machine at risk. The handoff's own discipline
says an interruption is `interrupted`, not a biological stop, so the honest record is this gate
rather than a crash log.

## The two ways forward, neither chosen here

1. **Give the machine headroom and run the drafted script unchanged.** It needs roughly 8 GB
   free to be safe. Nothing about the script needs changing, and this is the cheaper path if
   the memory can be freed. The script already refuses to overwrite its own outputs.
2. **Stream the serialization and extract only the metadata.** The inner stream is R XDR
   version 3, a tagged format that can be walked while skipping the large numeric vectors, so
   peak memory stays small. This discharges C1 without the allocation, at the cost of writing
   a reader that must fail closed: it would have to validate the recovered cell count against
   the assay dimensions and the recovered donor labels against the six the series lists, and
   refuse rather than guess if either disagrees.

## What C1 still owes, and what has not been touched

The deliverable remains a persisted sample, donor, condition and state crosswalk verified
against the object rather than against GEO titles. That verification is exactly what is
blocked, so the control-medium question the handoff raises for 102C and 219V, the BSA and FCS
libraries, stays open and no pairing has been chosen.

The queue is unchanged: C1 is still `ready`, `new_biological_analysis_executed` is still false,
and C2 has not been reached, so no A11 acute-injury contract exists. Nothing in the register
was edited and no claim row was added.
