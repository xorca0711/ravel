# Frozen annotation and QC strategy v1

30 October 2026. Freeze follows completed full-entry integrity QC and precedes
local class-specific Arg1/Il6 summaries. Published outcomes, functional source
contrasts and technical QC distributions are exposed. This is an adapted
descriptive workflow; it is not the paper's integrated SingleR/ImmGen/DoubletFinder
analysis. The [exact specification](config/annotation_spec_v1.json) owns thresholds.

## Source and technical evidence

The [count-integrity run](../../analysis/research/runs/Yd1_count_integrity_v1/receipt.json)
fully parsed six matrices. All entries are nonnegative integers, coordinate and
identifier joins agree, and no duplicate coordinates or explicit zeros were found.
All deposited barcodes have more than 200 detected genes; the two first coculture
libraries also include barcodes above 10,000 genes. Most mitochondrial proportions
are low, with a small high tail. These observations inform QC, not target-gene effects.

[Yadav Methods, scRNA-Seq data analysis](https://www.jci.org/articles/view/188734)
uses thresholds of 200 and 10,000 genes and 5% mitochondrial content, followed by
integration, DoubletFinder and SingleR. Our primary mask explicitly excludes any
barcode with genes <200, genes >10,000 or mitochondrial counts >5%. The wording
of the original combined sentence is not substituted for executable author code.
The fixed broad sensitivity retains genes >=200 and mitochondrial counts <=10%
without a high-gene cutoff. Report both masks, never pick the favorable one.

The [miQC primary study](https://doi.org/10.1371/journal.pcbi.1009290) motivates
caution about tissue- and technology-dependent mitochondrial thresholds; it does
not validate our thresholds. We do not implement or claim miQC.

## Conservative marker compatibility

Annotation uses raw counts >=2 for a marker to count as detected, reducing
dependence on single-count ambient detection. This heuristic does not remove
ambient RNA. Three distinct markers are required for each nominated class.

- Fibroblast-like: >=3 of Col1a1, Col1a2, Col3a1, Dcn, Lum, Pdgfra, including
  >=2 of Col1a1, Col1a2, Dcn, Lum.
- Macrophage-like: >=3 of Csf1r, Adgre1, Fcgr1, Cd68, Aif1, Lyz2, Ptprc, including
  >=1 of Csf1r, Adgre1, Fcgr1.
- Simultaneous fibroblast/macrophage support remains mixed.
- Prespecified epithelial, endothelial, mural, granulocyte or dendritic marker
  pairs flag other-or-mixed compatibility, without claiming those finer identities.
  Neither primary class is forced when the marker rules fail.
- Held-out compatibility genes: Col6a1/Sparc/Pdgfrb for fibroblast-like and
  Mertk/Tyrobp/Lst1 for macrophage-like. These do not assign labels.
- Arg1 and Il6 never enter annotation, QC thresholds or eligibility.

Marker nominations are literature-grounded but the combination/count thresholds
are an explicit local conservative adaptation. Fibroblast genes match the
interstitial-fibroblast marker table indexed from
[Angelidis et al. 2019](https://doi.org/10.1038/s41467-019-08831-9).
Canonical myeloid markers Csf1r/Adgre1/Fcgr1/Lyz2 appear in the depositor's
[GSE154692 study description](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE154692);
that aortic study supports marker conventions, not lung-context validation.
Yadav's S2 and Methods give independent CD64/CD11b/MERTK source context.
[Regenerating-lung study, Fig. 2f](https://doi.org/10.1038/s41467-024-46469-4)
provides Dcn/Col1a1/Col1a2 context. We do not infer sublineage or homologous human
identity from these panels.

Actual search date: 30 October 2026. Queries covered mouse-lung fibroblast
Pdgfra/Dcn/Lum and macrophage Csf1r/Adgre1/Fcgr1 conventions, plus primary scRNA QC
threshold studies. JCI full text was accessible. Nature/PMC/GEO page opens were
challenged; other marker/QC premises above were inspected in primary-source
indexed text, not claimed as newly completed full reads. This targeted methods
check is not novelty or portfolio literature clearance.

## Descriptive eligibility and limits

Per library, QC mask and nominated class: at least 20 retained cells and at least
50% detecting one held-out compatibility marker at >=2 counts are required before
the subsequent endpoint run. This is a transparent coverage/compatibility floor,
not power, purity, lineage validation or biological replication. Display all
class counts and hold reasons, including fibroblast-alone myeloid-compatible
cells if any; condition names do not override observed markers.

All deposited barcodes remain in the label/QC table. All mixed, other, unassigned
and excluded cells remain in composition summaries. No preparation pairing, cell
population DE or donor identity is inferred. If class support fails, that class
is held; unrelated qualified classes may proceed under the next endpoint contract.
RNA results can remain sensitive to conservative-core selection, activation,
ambient RNA, doublets and unqualified biological preparation identities.
