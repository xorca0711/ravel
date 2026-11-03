# A32 GSE234197: prospective resolution-context screen

3 November 2026; main `445a0ca`. Metadata recovered at freeze `7132cc0`; raw barcode/HTO joins verified; no new gene outcome viewed. Original A32 functional comparison and Speth access hold remain.

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


## Metadata-qualified execution choices (before expression)

Native-R recovery retained 45,311 cells, 41 source celltype labels and 36 distinct
capture+HTO mice. All cell barcodes match their original RNA capture and all
HTO/treatment fields agree. The raw source-count equality check remains a run
prerequisite. Source `celltype` is used, not endothelial-refined `cellstate`.

Exact primary myeloid labels: `AM1`, `AM2`, `AM3`, `Prolif. AM`, `IM`, `LCM`,
`cMonocytes`, `ncMonocytes`, `Neutrophil-like Monocytes`, `Neutrophils`.
Other primary labels: `Fibroblasts`, `AT1`, `AT2`. Secondary `AM_all` combines
AM1/AM2/AM3/Prolif. AM only; it is explicitly composition-sensitive context,
not evidence for a within-state change. Keep every original primary label.

Eligibility is at least 10 retained cells per mouse/state, selected from metadata
before outcomes as a practical minimum, not a power calculation. Save every
mouse/state including zero cells, support counts and raw totals. RNA summaries
below the floor remain unestimated. Group contrasts require all three PBS and
all three BLM mice to meet that floor; no dropped-mouse or pooled rescue.

Metadata already rules out epithelial BLM/PBS contrasts: AT1 has 22 cells total,
AT2 130. Fibroblasts have 559 cells and complete support only in young D14.
This source cannot answer three-compartment resolution coupling or matrix
resolution trajectories. It can support bounded myeloid contrasts and a young
D14 fibroblast comparison. Preserve that limit regardless of gene directions.

Primary tables retain mouse-level log2(CPM+1). Eligible group differences use
an unpaired equal-mouse mean(BLM) minus mean(PBS). Show 95% Welch-t pointwise
descriptive intervals using the two sample variances and Satterthwaite degrees
of freedom. With n=3 per arm normality is unverifiable and precision is fragile;
intervals are not simultaneous or confirmatory. No p-values or equivalence calls.

Show all fixed genes and eligible contrasts. Secondary AM_all is clearly labelled;
no across-state averaging, stage pooling, direct age inference, adjusted
correlation or significance-based nomination. Source/metadata parity and an
independent original-matrix calculation precede result interpretation.

Exact panel-source locators and contrary findings are recorded in the
[3 November literature-context addition](../LITERATURE_CONTEXT.md#public-resolution-context-branch--3-november-2026).


If both groups have zero observed variance, retain the observed mean difference
but leave interval bounds and degrees of freedom NA with a degenerate-interval
flag; zero observed dispersion does not establish precise absence of an effect.
The focused mouse-value panels are fixed before outcomes: Arg1 in AM1, AM_all,
cMonocytes, ncMonocytes and Neutrophils, plus all four fibroblast genes. These
highlight the focal endpoint and metadata-supported populations; the full fixed
panel remains in tables and the complete heatmap, including unsupported rows.
