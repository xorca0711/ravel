# Expanded candidate audit

**18 additional GEO records inspected, including reused saved records; no new A5 or lesion-specificity score.** The [metadata directory](metadata/) preserves series/sample methods and acquisition hashes. The earlier Choi and Riemondy decisions stand. This is a bounded candidate audit, not a proof that no suitable public data exist.

## A5: preserve the existing instrument and comparator

The inherited floor is three eligible independent mice in the selected time window, **not three mice at every time point**. The earlier title-based gate audit misstated this. An AT2 label alone is not the required activated-AT2 comparator. A new classifier or assay amendment needs its own externally checked definition; it cannot silently turn into an unchanged replication.

| Additional cohort | Source finding | Decision for unchanged A5 |
|---|---|---|
| GSE262927 | Six retained, author-annotated early samples; transitional counts 4, 23, 14, 11, 127, 10 before the depth filter | Only one reaches 30; activated-AT2 label also absent. Stop for the current annotated population. Unknown/unannotated cells are not relabelled to rescue it. |
| GSE243124 | Day 10; multiple mice pooled into one GEM lane per treatment | No recovered mouse-resolved contrasts |
| GSE243135 | Demultiplexed individual samples exist, but day 28 | Outside fixed day 2–21 window; eight sequencing sublibraries are not eight animals |
| GSE252588 | Three lineage-sorted populations at four weeks | Outside window; populations are not independent mice |
| GSE132771 | Two bleomycin mice, each split GFP+/−, day 14 | Below three-mouse floor; sorted fractions do not add mice |
| GSE129605 | Four numbered bleomycin samples, day 11, counts locally available | No deposited per-cell state annotation or independently verified sample-to-animal crosswalk established by this pass; no invented activated comparator |
| GSE202325 | Three young and three aged samples at days 3/9; original code uses broad AT2 annotations and local RDS files | Strong candidate for an amended annotation/transport study, not a ready unchanged state contrast. Lack of uninjured controls is not the A5 exclusion. |
| GSE292515 | Fixed-RNA/probe profiling, day 7, three infected samples per age | Assay transport and population correspondence not established; do not silently equate a fixed-probe budget with the frozen full-transcript UMI measurement |
| GSE184854 | Silica; TAS-Seq processing describes read counts, two pooled sequencing records | Frozen 500-UMI measurement not established; read counts are not molecule counts |
| GSE264278 | Five biological replicates described, with sample tags; TAS-Seq read-count processing | Replication is not the only gate: unchanged UMI instrument fails assay correspondence |
| GSE201698 | Six time-point records; processing says reads counted, despite raw-read UMI description | Deduplicated UMI provenance not established; time-point GSMs do not prove animal replication |
| GSE303646 | 56 samples, with 24 young/old bleomycin samples at days 3/10/20 | Promising candidate requiring barcode-level author state labels, sample identity and raw-count provenance; deposited dge/summary files alone do not provide the required state contrast |

[Measured GSE262927 counts](GSE262927_early_state_coverage.json) use the full retained-cell table, not the narrower epithelial-subanalysis subset. A first subset check was refined to that authoritative universe before reporting the counts here. The three source papers and author-code availability checks are linked through [primary-source retrieval](primary_source_checks.json). GSE202325 author code: [Flu_Spatial_Sequencing](https://github.com/ryanjbrown21/Flu_Spatial_Sequencing).

**Next enabling input:** a validated barcode-to-transitional/activated-AT2 map for GSE303646 or GSE202325, independent of the tested module, plus mouse provenance. Automated clustering alone does not establish that biological correspondence. No outcome-guided relabelling or unrelated injury mechanism branch is introduced.

## A3: correct the previously overconfident eligibility statement

[GSE303646 design counts](A3_design_cells.json) show nine young and eight old baseline control libraries. Every later library is bleomycin. Thus an age-by-postinjury comparison against baseline can be defined, but it does not isolate persistent injury from elapsed aging/harvest effects without assumptions or later uninjured controls. Neither a large sample count nor one shared study makes sampling comparable by construction. Same-cell persistence additionally requires tracing. No memory model is fit under the original claim.

## A11: 91 records are not 91 comparable injured patients

[GSE198864](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE198864) comprises 24 ex-vivo macrophage, eight autopsy, 49 explant, four bronchial-organoid and six alveolar-organoid libraries. [Design inventory](A11_candidate_design.json). Processed counts and RDS objects are publicly listed; the FASTQ privacy statement is not treated as absence of counts. A programme-independent matched injured epithelial state and a cohort-comparable specificity contrast are not established by those records. Acute infected explants could support a separately specified one-context falsification test; they cannot, by themselves, establish tumour specificity or repair capacity. A11's prior lesion contrast remains intact, and no new score is justified by the present gate.

## Regulatory linkage and recovery candidates

GSE215824 has organoid RNA at days 14/21/28 and separate ATAC preparations: no verified replicated early-mark-to-later-descendant linkage is provided. GSE286986 concerns embryonic CTCF/multiomics, not the selected adult-injury future-outcome contrast. GSE295566 has four Fgf10-lineage saline/bleomycin time-point records; no IL1 withdrawal crossed with selective post-entry recipient intervention. None closes the P3/P5 design gate merely by containing chromatin or a late time point.

## A13

The two external candidate checks and the new local pilot are completed in [A13 results](A13_PILOT_AND_COVERAGE.md). Blood sampling and measured fibroblast scarcity resolve these candidate decisions without forcing a model.
