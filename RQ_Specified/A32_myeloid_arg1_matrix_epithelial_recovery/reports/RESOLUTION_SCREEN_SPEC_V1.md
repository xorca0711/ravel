# A32 GSE234197: prospective resolution-context screen

3 November 2026; main `445a0ca`. Metadata qualification in progress; no new gene outcome viewed. Original A32 functional comparison and Speth access hold remain.

## Purpose and decision

Describe whether myeloid Arg1-associated RNA, fibroblast matrix RNA and epithelial transitional/identity RNA retain or decouple their injury-associated changes at D14/D28/D60. Supported divergence can nominate a stage/source population for later work. Concordance or divergence identifies neither ARG1 activity/mediation, deposited collagen nor mature epithelial function. This is exposed exploration, not confirmation.

## Source and exposure

[Truchi et al., Nature Communications 2025](https://doi.org/10.1038/s41467-025-62431-4), Fig. 2 and Methods, report 36 male mice and 45,311 whole-lung cells. Fig. S2E/F already reports similar macrophage abundance dynamics across ages: reproducing those curves alone is not the contribution. Original broad injury DE pools PBS times and omits D60 BLM; this screen retains time-matched controls and D60.

GSE234197 provides six RNA/HTO capture pairs and a six-tag assignment workbook. Author code at `b822811cb96de4811be6c5ce33bb9d5f57f760f7` defines capture+HTO mouse IDs and source annotations. Its mitochondrial fraction is mt-counts/all-counts; 0.25 means 25%, despite the Methods' 0.25% wording. Preserve deposited retention/labels; no integration rerun or outcome-based relabelling.

Published results and earlier A32/Yadav/Speth reads are exposed. The panel below is specified before new gene aggregation. Finalize exact labels and eligibility from metadata only, then freeze before expression. Record changes prospectively.

## Units, comparison and alternatives

Mouse = original capture plus HTO; tags 1–3 PBS, 4–6 BLM. Verify against source metadata and raw files. Cells are nested, and days contain different mice. Keep ages separate; compare BLM minus PBS within each age×day capture. Display these contrasts across stages with the run×condition caveat: age/day are confounded with capture. No direct age-effect attribution, longitudinal trajectory or causal cross-compartment regression.

Shared injury severity, dissociation/selection, depth, within-label composition and run×condition effects can explain coordination. Proportions use all retained cells per mouse and measure relative recovery, not tissue abundance. The broad fibroblast label cannot exclude fibroblast substate replacement. AT1/AT2 labels do not independently identify transitional cells.

## Candidate panel and summaries

- Myeloid: Arg1 focal; Spp1 and Trem2 contextual.
- Fibroblasts: Col1a1, Col3a1, Fn1, Cthrc1 individually.
- AT1 and AT2: Krt8/Cldn4 transition-associated; Sftpc/Abca3 AT2-associated; Ager/Hopx/Aqp5 AT1-associated.

Fourteen named genes; no composite repair score. Finalize the source myeloid label list from metadata before expression. No post hoc gene substitution. Krt8/Cldn4 does not reclassify cells; identity RNA does not establish lineage/function.

Primary endpoint: mouse×source-state per-gene raw-count pseudobulk CPM using all RNA UMIs, transformed log2(CPM+1). Report all mouse values, support, equal-mouse BLM-minus-PBS differences and descriptive pointwise uncertainty where eligible. Raw counts and detection fractions are measurement context. Keep proportions and expression separate.

Set the source-state cell floor and complete three-versus-three contrast eligibility from metadata only. Unsupported compartments remain visible; no cell-level inference, pooled-mouse rescue or outcome-driven relaxation. Report every fixed gene/state, without significance selection. No power/equivalence margin, endpoint independence or simultaneous uncertainty claim.

## Runtime and independent checks

The 2,514,729,263-byte GEO object has two gzip layers. Current memory does not support an unbounded full load. Author GitHub/Zenodo list no separate annotation table. A bounded metadata extraction must first pass native-R synthetic serialization checks. Retain metadata bytes and deserialize the reduced stream in native R; discarded assay payloads must never serve as expression. Original GEO sparse matrices supply gene counts.

Stop for unsupported serialization, truncation, ambiguous join, noninteger counts or inconsistent IDs. Verify retained cell count, HTO condition, unique mice/barcodes, matrix dimensions and per-cell RNA totals. Independently verify endpoint arithmetic and figures before interpretation. Same-data verification is not biological replication.

## Ownership

Technical chat owns new contracts/code/receipts and A32 pages. Coordinator owns PROGRESS and integration. No governance, canonical hypothesis, schematic, claim-grade or frozen-output change; execution does not establish scientific acceptance.
