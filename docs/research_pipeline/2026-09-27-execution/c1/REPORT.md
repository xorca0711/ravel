# C1: the object inspected, and the nominated pathogen is the weakest arm

27 September 2026. **C1 is complete. No module score was computed, no contract was frozen and
C2 has not been started.** Every number below comes from this directory's tables and their run
records. The earlier [environment gate](ENVIRONMENT_GATE.md) records the memory measurement
that blocked the first attempt and is superseded by this run.

## What had to be fixed before the drafted script would run

**The published archive is double gzipped.** The 2.12 GB `.rds.gz` wraps an RDS that R had
already compressed, so the outer layer achieves a compression ratio of 1.00 and `readRDS` on the
published file cannot reach the serialization. Stripping the outer layer once gives a 1.98 GB
`.rds` that R reads normally. The true serialized size is 6.54 GB and the loaded object reports
7.09 GB, so anyone sizing this object from the download figure is out by more than threefold.

The previous session's [`inspect_gse198864.R`](../../scripts/inspect_gse198864.R) was left
untracked and unrun. It was run here unchanged. It is sound for C1: it reads slots through base R
without Seurat, dumps the cell metadata and its field inventory, records assay slots and
dimensions, checks the count matrix, and computes per-cell totals. It computes no programme score.

## The object

| Fact | Value |
|---|--:|
| Class | Seurat, 146,476 cells |
| Explant cells | 112,476 |
| Autopsy cells | 34,000 |
| Assays | RNA and integrated |
| RNA stored values | 209,357,601 |
| Non-finite, negative or non-integer counts | 0, 0, 0 |
| Count range | 1 to 33,094 |
| Duplicated gene names | 0 |

The RNA assay holds raw integer counts, which is what a pseudobulk contrast needs. The
`colnames` of the count matrix match the metadata rownames exactly, a check the script makes
before writing anything.

## The control-medium question the handoff raised is answered by the object

The handoff flagged that libraries named `control` do not establish the matched medium by name
alone, and asked for the source supplement or explicit object metadata to justify any pairing.
**The object settles it: the `protocol` field records BSA or FCS for every explant cell, for
infected and control libraries alike**, 32,134 BSA and 80,342 FCS, with the 34,000 autopsy cells
carrying no protocol. No protocol inference is needed, and the series metadata agrees
independently: the control libraries name their medium in the treatment field.

## The design, and why the nominated arm is the weakest

Medium-matched means the same donor supplies both the infected arm and a control in the same
medium. Author-annotated AT2 is the `cluster` label, 4,732 explant cells.

| Arm | Medium-matched pairs | Pairs with AT2 at or above 20 on both sides | At or above 50 |
|---|--:|--:|--:|
| **H3N2, the nominated candidate** | **2** | **1** | **1** |
| SARS-CoV-1 | 5 | 5 | 4 |
| SARS-CoV-2 | 5 | 5 | 3 |
| MERS-CoV | 5 | 5 | 2 |

Every H3N2 library is in BSA, but only two donors have a BSA control, and one of those two has
19 AT2 cells on its infected side. So the acute-injury arm the handoff nominated yields one
usable matched pair. The three coronavirus arms each yield five matched pairs, and they differ
in AT2 depth rather than in availability.

That is a design fact established before any programme value, which is what C1 was for. It does
not choose the arm. If C2 selects on coverage and protocol matching, the choice is defensible
because both were counted before any score; selecting after seeing a programme value would not
be.

The biological cost of the swap has to be weighed by the owner, not by this table. The handoff
nominated influenza because it supplies an acute-injury challenge, and a coronavirus arm is a
different injury with different tropism. A coverage argument cannot settle that.

## Two things that remain unresolved

**The donor labels do not join.** The object names its explant donors pat1 to pat6. The series
names its six single-cell explant donors 102C, 1169Z, 218V, 219V, 700D and 89C. Six against six,
but no source states the mapping. The arm structure constrains it into groups, because one donor
carries only a control and an influenza arm and two donors carry both control media, and those
groups are identifiable on both sides. No individual pair is resolved, and none is asserted here.

**The A11 transfer question is untouched.** Whether the frozen lesion programme can be scored in
this object at all depends on gene coverage against the 73-gene human module, which C2 must gate.
The gene index is persisted here for that purpose and was not used to score anything.

## State after C1

The queue advances to C2 and nothing else changes. No contract exists, so there is no eligible
donor set and no frozen contrast. `new_biological_analysis_executed` stays false, the register is
untouched and no claim row was added. The first crosswalk attempt, whose donor parser did not fit
the explant titles, is preserved in
[`geo_attempt1_parser_defect/`](geo_attempt1_parser_defect/).
