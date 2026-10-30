# Yadav source qualification: first review checkpoint

**30 October 2026 (Asia/Seoul). Steps 1-2 complete to the available-source boundary.**
Metadata owner **Yd1-P01** supports the existing [Wg-P06 question](../gate2_W1_wagner_th17_autoimmunity/rq_derivation/P06.md).
It creates no canonical A ID, revised hypothesis or scientific acceptance.
Published outcomes and workbook values were exposed before freezing. No functional
effect, expression contrast, population estimate or new biological score ran.

Read this checkpoint before the historical [six-step proposal](README.md).
Eligibility below is permission to specify a bounded next job for review, not a
claim that its biological inference has already been validated.

## Execution and exact repository evidence

- [Frozen contract](config/source_qualification_v1.json) and [bound script](scripts/qualify_sources_v1.py).
- Freeze commit: `6753251515c1c2f1b0aea18997b526b30c107d5c`.
- [Executed receipt](../../analysis/research/runs/Yd1_source_qualification_v1/receipt.json).
- [Seven input hashes and sizes](../../analysis/research/runs/Yd1_source_qualification_v1/input_inventory.json).
- [Workbook sheet/label/merge inventory](../../analysis/research/runs/Yd1_source_qualification_v1/workbook_inventory.json) and [all source cells with coordinates](../../analysis/research/runs/Yd1_source_qualification_v1/workbook_cells.tsv).
- [GEO/BioSample/experiment joins and unit holds](../../analysis/research/runs/Yd1_source_qualification_v1/geo_library_qualification.json).
- [Archive member hashes and matrix dimensions](../../analysis/research/runs/Yd1_source_qualification_v1/matrix_inventory.json), [qualification checks](../../analysis/research/runs/Yd1_source_qualification_v1/qualification_checks.json).

The script inventories all 34 workbook sheets and 18 archive members. It checks
matrix headers against unique feature/barcode IDs; it does **not** exhaustively
validate expression entries, annotate cells or estimate expression. Reusing the
publication's source data is reconstruction, never independent replication.

## Primary sources and acquisition

Recovered 30 October 2026. Immutable copies are under ignored
`raw_data/Yd1_source_v1/` in this execution worktree. Preserve that cache before
retiring the worktree. The original checkout and review cache were read only.

| Saved input | Source/version and access |
|---|---|
| `JCI188734.sdval.xlsx` | [Official supporting-values landing page](https://www.jci.org/articles/view/188734/sd/4) and [exact XLSX](https://dm5migu4zj3pb.cloudfront.net/manuscripts/188000/188734/JCI188734.sdval.xlsx). 49,224 bytes; version identified by SHA-256, not an invented workbook revision date. |
| `GSE242510_family.soft.gz` | [Official SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE242nnn/GSE242510/soft/GSE242510_family.soft.gz). Series/sample last-update fields: 15 August 2025; submission: 6 September 2023. |
| `GSE242510_RAW.tar` | [Official archive](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE242nnn/GSE242510/suppl/GSE242510_RAW.tar), 213,104,640 bytes. Six count-matrix triplets; no spatial coordinates, segmentation or specimen map in this archive. |
| `biosamples.xml` | [NCBI EFetch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=biosample&id=SAMN37307448,SAMN37307449,SAMN37307450,SAMN37307451,SAMN37307452,SAMN37307453&retmode=xml), all six linked BioSamples. |
| `experiments.xml` | [ENA experiment XML](https://www.ebi.ac.uk/ena/browser/api/xml/SRX21653362,SRX21653363,SRX21653364,SRX21653365,SRX21653366,SRX21653367), all six linked sequencing experiments. |
| `article.pdf` | Owner-supplied 16-page final JCI article, 135(21):e188734. The supplied copy includes reading annotations. |
| `supplement.pdf` | Seven-page [publisher supplement](https://www.jci.org/articles/view/188734/sd/1), copied byte-for-byte from the review chat's read-only cache. |

The GEO web viewer was challenged, but direct official SOFT retrieval succeeded.
Initial sandbox write/DNS attempts failed; authorized escalated recovery succeeded.
No completed run was repeated after the capacity interruption. The registry's
formatting churn was removed after semantic comparison: only this owner, contract
and receipt were added. No remote write, message, Notion edit or external setting
change occurred.

This is source qualification for the unchanged comparison, not new RQ development.
The existing article/P06 literature record remains the premise; no new novelty
claim or completed broad literature search is asserted.

## Claim-to-assay map and ambiguity disposition

Primary locators below refer to the supplied article's printed pages and S1-S3
supplement. Repository outputs above separately establish what was recovered.

| Claim/link | Model, comparator and measured endpoint | Unit and interpretation limit |
|---|---|---|
| ARG1-positive source identity: Figs. 1-2; S1-S2 | Mouse coculture RNA and reporter/flow versus human IPF MIBI protein. | Cell classifications within source animals/patients. Mouse macrophages and human neutrophils remain distinct contexts. MIBI FOVs were selected from ARG1-positive staining (Methods p.13); this does not estimate unbiased whole-lung prevalence. Mixed LY6G/CD64/CD11C markers do not establish lineage or human homology. |
| ARG1 perturbation to ornithine/collagen: Fig. 3B-E/J; S3B-C | Chemical inhibitor, Lysm-Cre Arg1 deletion and supplementation; ornithine, COL1A1 immunoblot/MFI and lung hydroxyproline. | Animals, patients or preparations as appropriate. Inhibitor specificity, broad myeloid targeting, culture selection and normalization remain alternatives. Reduced collagen is not epithelial repair. |
| Ornithine/OAT to collagen versus alpha-SMA: Fig. 3F-I; S3C-D | Monoculture/coculture and supplementation/inhibition; COL1A1 MFI versus alpha-SMA MFI. | Separate cultures, with donor/preparation identities absent. Alpha-SMA is a distinct endpoint; nonsignificance does not prove no change. OAT inhibition does not uniquely establish substrate routing. |
| ARG1 to fibroblast proline: Fig. 3K, legend p.6, LC-MS Methods p.14 | Isolated fibroblast lysate proline/hydroxyproline relative abundance after coculture with/without CB-1158. | Three author-described biological replicates per condition, identities/pairing absent. Protein/cell normalization is described; raw normalizers and isotope/isotopologue measurements are absent. No measured transfer flux or incorporation rate follows. |
| IL-6 to ARG1: Figs. 4C-D, 5A/D-F | Mouse stimulation/whole-animal deletion, human PCLS/coculture IL-6R blockade; ARG1 protein/RNA, ornithine and COL1A1 MFI. | Fig. 4D normalizes BAL ARG1 to macrophage count and measures sorted-cell Arg1/Gapdh. This addresses abundance partly, but whole-animal deletion also changes the environment. Human blockade affects the coculture, not uniquely the source cell. |
| P2RX4 to IL-6: Fig. 6A-G | Fibroblast genotype, knockdown or inhibitor contexts; Il6 RNA and IL-6 ELISA. | Direct genotype/library contrast can assess transcript consistency after QC; capture, composition, preparation and batch remain threats. An eATP source is not uniquely identified. |
| Spatial/context compatibility: Fig. 5B-C, Methods pp.13-14 | Xenium probability ratio at 25 micrometres; reused NSCLC neutrophil ARG1/IL6R correlation. | Nine IPF patients versus a separate NSCLC atlas. Proximity is not transfer, and detection-selected RNA correlation is not IPF receptor function. Five half-cell subsamples are sensitivity draws, not independent patients or patient confidence intervals. |

**S3C resolved for contrast naming, with the discrepancy retained.** The actual
panel on supplement p.5 and worksheet `S3c!A1:E4` agree on monoculture, coculture,
coculture + CB-1158, coculture + CB-1158 + ornithine, and coculture + OAT inhibitor.
The supplement p.6 legend instead says monocultured fibroblasts. The main-text
rescue comparison is supported by the panel and workbook. Use the coculture labels
for a future exposed source reconstruction and cite the legend conflict; do not
claim to have corrected the publication or qualified independent preparations.

**Other retained ambiguities and missingness:**

- `3e!A1:B1` repeats “Bleomycin” and omits genotype. Fig. 3E's color key supplies
  control Arg1 fl/fl **or** fl/+ versus Lysm-Cre Arg1 fl/fl; `A2:A11` and
  `B2:B10` match the legend's 10 and 9 mice. Individual control genotype,
  animal IDs, litter/cage/allocation and batch are unavailable.
- `3j!B1:C1` repeats “Fib + Mac”. Fig. 3J identifies B as control macrophages
  and C as Arg1-deleted macrophages; D is the deleted-macrophage coculture with
  CB-1158. The source headers alone cannot recover these genotypes.
- `5d!D2` is blank: donor-1 fibroblast-alone has two supplied values, while
  the legend says three cultures each. Retain the missing value; neither
  impute a third point nor borrow it from Fig. 5E/F.
- Methods p.14 visually prints IL-6-positive in **both** spatial fibroblast
  categories (b) and (c), whereas Fig. 5B and `5b!A1:B1` contrast IL6-positive
  and IL6-negative fibroblasts. The likely intended negative category is an
  inference, not executable author code. Boolean grouping and denominator
  fidelity must be resolved before raw spatial reconstruction.
- Fig. 3K/workbook contain relative abundance, with no tracer channels. Discussion
  “labeling” language does not upgrade this endpoint. ARG2, polyamine routing,
  intracellular/extracellular ornithine generation and alternate eATP sources
  remain unresolved premises, not reasons to expand this checkpoint.

## Source and biological-unit qualification

### GSE242510

The SOFT summary identifies WT macrophages with WT or fibroblast-specific
Pdgfrb-Cre P2rx4 fl/fl fibroblasts after sterile bleomycin injury. Fig. 6A describes
two separate cultures per condition. The source processing records specify PIPseq
v4, PIPseeker 1.0.0 sensitivity 3 and mm10. Each matrix has 32,285 feature rows,
including Arg1 and Il6; the third feature column is `protein_coding`, not the
usual 10x `Gene Expression` label. A future loader must retain this distinction.

| GEO accession | Published title | BioSample | Sequencing experiment | Deposited barcodes |
|---|---|---|---|---:|
| GSM7764752 | Fib alone 1 | SAMN37307453 | SRX21653362 | 2,081 |
| GSM7764753 | Fib + Mac 1 | SAMN37307452 | SRX21653363 | 1,674 |
| GSM7764754 | P2rx4KO Fib + Mac 1 | SAMN37307451 | SRX21653364 | 2,333 |
| GSM7764755 | Fib alone 2 | SAMN37307450 | SRX21653365 | 1,856 |
| GSM7764756 | Fib + Mac 2 | SAMN37307449 | SRX21653366 | 1,984 |
| GSM7764757 | P2rx4KO Fib + Mac 2 | SAMN37307448 | SRX21653367 | 2,591 |

These are deposited barcode counts, not QC-retained cells or biological replicates.
GEO/BioSample/SRA joins agree. BioSample attributes give tissue, cell type, genotype
and treatment; collection date/location are missing. No record supplies animal IDs,
number of animals per culture, pooling, preparation IDs, culture sharing, pairing,
litter, sex or biological batch. ENA has no pool elements, which is not proof of
no pooling. Six accessions and suffixes 1/2 cannot establish independent animals,
preparations or matched contrasts. All animal/preparation/pairing fields therefore
remain unknown. Library-level descriptions can proceed after review, while
population differential-expression inference and paired preparation models remain held.

### Functional and spatial source-value ledger

Counts below are supplied measurements. “Reported” biological units come from the
publication, not from newly recovered specimen IDs. Workbook cells have uniform
data styles and no donor comments, hidden sheets or extra drawing/comment parts;
formatting does not provide a concealed donor map.

| Source locator | Endpoint and available measurements | Biological-unit/pairing qualification |
|---|---|---|
| `3b!A2:B9` | Mouse lung ornithine, micromolar; 8 + 8 values. | Legend declares mice. Anonymous independent-animal grouping is usable for an exposed unpaired source reconstruction; allocation/batch and individual identities unknown. |
| `3b!D2:E17` | Human PCLS ornithine relative to untreated; 16 + 16 values. | Three patients reported. No slice-to-patient, treatment-pair or raw-normalization map. Rows do not authorize pairing. |
| `3d!A2:B9` | PCLS COL1A1/GAPDH normalized to untreated; 8 + 8 values. | Three patients reported; slice-to-patient and normalization denominators unavailable. No patient-level effect estimate. |
| `3e!A2:A11,B2:B10` | Mouse lung hydroxyproline, mg/mL; 10 + 9 values. | Each point reported as one mouse. Group identity recovered from Fig. 3E; pooled control genotypes, allocation and batch limit the effect interpretation. No invented pairing. |
| `3j!A2:D4` | COL1A1 MFI; three values in each of four culture conditions. | Three separate cultures reported; animal/preparation origin and sharing unknown. Genotype labels require Fig. 3J. |
| `S3c!A2:E4`, `S3d!A2:D4` | COL1A1 MFI and alpha-SMA MFI; three per group. | Panel/condition identity qualified; independent preparation identity and pairing unknown. |
| `3k!B2:G3` | Relative proline/hydroxyproline abundance; three per condition per metabolite. | Author-described biological replicates; identities/pairing and raw protein/cell denominators absent. Description only in reported normalization. |
| `5a!A2:B10` | PCLS lysate ARG1, pg/mL; 9 + 9 values. | Three patients with three slices per condition each reported. The workbook does not assign rows to patients; grouping consecutive triples would be invented. |
| `5d!B2:D4,E2:G4` | COL1A1 MFI; two donor groups, normally three culture values per condition, except D2 blank. | Merged headers identify donor combinations; legend says distinct neutrophil and fibroblast donors for combinations 1 and 2. Donor-group contrasts are describable. No well matching or population precision inferred. |
| `5e!B2:D4,E2:G4`, `5f!B2:D4,E2:G4` | ARG1 pg/mL and ornithine micromolar; three values per condition per donor group. | Same cocultures as D by legend: these endpoints are dependent, not independent replication. Column order alone does not prove well-level correspondence. |
| `6g!B2:D5,E2:G5` | IL-6 pg/mL, two donor groups, three technical replicates per condition. | Two distinct blood/lung donor combinations by legend. Reuse of the same physical donors across Figs. 5 and 6 is not documented; do not pool. |
| `5b!A2:B10` | Published 25-micrometre probability ratios; nine values per category. | Nine patients and a paired comparison are stated in the legend and plotted. No patient IDs or explicit workbook row-to-patient key. Marginal source summaries are available; a rowwise paired reconstruction needs pairing confirmation. |

### Per-job completion, eligibility and holds

All **eligible** jobs below still await review and their own frozen numerical
contract. “Held” names the stronger job that cannot be justified from current data.

| Job | Completed now | Eligible next bounded job | Held / exact release condition |
|---|---|---|---|
| Q1 claim/assay audit | Source map and S3C disposition, 3K limit, genotype/header and spatial-category discrepancies. | Documentation refinement if review identifies an error. | Mechanism/flux or acceptance promotion lacks the relevant evidence/authority. |
| Q2 source qualification | Seven hashed inputs; workbook inventory; six accession joins; 18-file structure check. | No further routine inventory needed. | Animal/preparation/pool/pair map requires new metadata; suffix-based reconstruction is not allowed. |
| F1 human PCLS, 3B/D and 5A | Values/units recovered, patient nesting explicitly unknown at row level. | Describe supplied values in reported units and disclose nested sampling. | Donor-level paired effects, patient CIs and raw normalization reconstruction require donor/slice/treatment and denominator maps. |
| F2 human coculture, 5D-F (6G optional) | Two donor combinations identified; D2 missingness retained; endpoints' shared origin recorded. | Per-donor-combination condition means/differences with raw technical points; separate endpoints and transparent missingness. | Generalized patient-population estimation, crossed-donor effects and well-paired covariance require more qualified independent donors and actual pairing. |
| F3 mouse lung, 3B-left/3E | Source values and mouse counts agree; genotype grouping recovered for 3E. | Exposed source-animal group contrast with bounded uncertainty and design caveats under a separate contract. | Specific macrophage mediation, universal causal/genotype claims and paired effects require allocation/target-specificity evidence; no precision guarantee is invented. |
| F4 culture rescue/source specificity, S3C-D/3J | Condition map and separate endpoints qualified. | Source-culture descriptive reconstruction; retain all arms and unfavorable outcomes. | Population effect/paired-preparation model requires preparation, animal and sharing map. |
| F5 metabolite abundance, 3K | Relative-abundance endpoint qualified. | Source-value description, if useful for review. | Flux, isotope incorporation and absolute synthesis-rate claims require corresponding tracer/normalizer data. |
| R1 coculture RNA | Six count matrices recovered; identifiers, dimensions and gene presence qualified. | Library-by-cell-class QC/annotation, then descriptive macrophage Arg1 and fibroblast Il6 summaries from nonintegrated counts. | Preparation-population DE or matched models need independently qualified preparations/pools/batches. Cell-level tests cannot substitute. |
| S1 spatial, 5B/Fig. 2 | Published summary ratios and Methods scope inspected. | Optional description of supplied 5B marginal values. | Raw reconstruction/spatial nulls need coordinates, counts, segmentation, patient/FOV maps, exact categories and implementation. No such data are in recovered GSE242510. |
| C1 reused contexts | Existing source locators retained: BAL GSE70867/GPL14550, Strunz/Tsukui, Salcher NSCLC. | Separate future metadata qualification only if review chooses a specific comparison. | No external counts/donor/reuse audit executed here. Do not substitute these cohorts for original matched evidence. |

The source findings constrain which published comparisons can be reconstructed.
They do not answer Wg-P06's joint arginine/ornithine balance question: source
exposure ranges, recipient arginine compensation, route discrimination and
functional precision remain unknown. Existing RQs and unfavorable results are preserved.

## Verification and checkpoint boundary

Independent openpyxl 3.x reading agreed with every one of the 1,429 populated cells
and all 34 sheet names from the standard-library OOXML extraction. It confirmed
`5d!D2` is blank, and no hidden sheets or cell comments supply missing identities.
The two parsers are computational checks on the same workbook, not replication.
Actual S3, main Fig. 3, main Fig. 5 and Methods p.14 were rendered and visually
checked; the source discrepancies above were confirmed against pixels.

The governed receipt verifies; accession joins and all six matrix-dimension checks
pass. Large matrix entry streams have not undergone biological QC. Hash-locked
published Choi outputs were restored by the repository helper without analysis.
Scoped Git attributes inside this article and its run preserve the new frozen
script/contract bytes and intentional blank TSV formula fields. The first base-aware
gate rejected an attempted root-attributes addition because prior Choi contracts
hash that file. Its exact original bytes were restored; those contracts and outputs
were not changed. No validator, governance or interpretation rule was altered.

Repository-required validation and the refreshed integration-base check are recorded
in PROGRESS at final delivery. No dependent effect run is started at this checkpoint.
Next: review F2/F3/F4 and R1 scope, select the first bounded jobs, then freeze their
separate contracts. Holds reopen only when their stated evidence becomes available.
