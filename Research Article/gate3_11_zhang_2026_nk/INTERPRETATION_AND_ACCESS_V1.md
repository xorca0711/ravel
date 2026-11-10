# Zhang NK: biological interpretation and remaining access

10 November 2026 (Asia/Seoul). Review of completed Zh26-P01 evidence at
`47b284a7b6c0a58c3a5a6c13df0d98fa23af6ec0`, against main `1a6769f`.
This dated reading/access addendum supplements [RESULTS](RESULTS.md) and the
[figure guide](FIGURES.md). It preserves all numerical results, contracts,
receipts and failed runs. No new biological analysis, count model, functional
reconstruction, canonical question or scientific acceptance was performed.

## Biological purpose and what the reconstruction establishes

The organizing question is how local Tregs restrain NK-mediated tumor control.
[Zhang et al. (2026)](https://doi.org/10.1126/sciimmunol.adx4411) already report
the relevant tumor immune circuit. The repository asks the narrower measurement
question: can the released sorted-NK RNA contrasts be reconstructed, and which
descriptions depend on analysis choices? Its unit is a pooled NK preparation,
with three reported experimental blocks and nine libraries. Constituent mouse
identities and exact pool membership remain unknown. The endpoint is transcript
abundance, with prior exposure to the published and released outcomes.

Local Treg removal is followed by higher abundance of many source-selected NK
transcripts; removing CD4 cells as well reverses their direction relative to
Treg removal alone. All three 12,708-gene released contrast tables reproduce.
This pattern was already reported by **Zhang et al., Figure 3B–G**, using the
same samples. Our contribution is numerical reconstruction and sensitivity,
not independent biological replication or discovery of a new NK programme.

Biologically, the pattern is compatible with CD4-dependent support for the
recovered NK population after release from local Treg suppression. It does not
identify which bulk differences reflect altered NK-state proportions, selection
or changes within individual NK cells. Those explanations can coexist. Anti-CD4
treatment affects more than one helper function; the RNA contrasts alone do not
identify IL-2 as the sole mediator. The paper's separate perturbation,
signaling and functional experiments support the more specific circuit.

## Reading the six reconstructed figures

| Display | What it shows and changes in interpretation | Limit that matters |
|---|---|---|
| Three volcano plots | ITDT−PBS has a predominantly positive source pattern; adding anti-CD4 reverses many differences relative to ITDT. The anti-CD4+ITDT−PBS contrast has only one BH<0.05 gene. | A near-null test is not an equivalence result. Panel y-scales differ; compare estimates and tables rather than apparent plot heights. Two middle-panel labels overlap; exact values are linked in the figure guide. |
| PCA and library distributions | The ITDT libraries separate on the source PCA, while PBS and anti-CD4 libraries show considerable block heterogeneity. This supports retaining the reported block term. | PCA is descriptive, not a treatment test or a reason to discard a library. Pools are not individual animals. |
| Fixed-panel heatmaps | Activation-associated, cytotoxic-cargo, checkpoint and selected metabolic transcripts often rise together after ITDT and fall with anti-CD4. Individual-library displays expose variation hidden by means. | Colors use gene-wise scaling from group means; they cannot compare absolute abundance across genes. Checkpoint RNA is not proof of exhaustion, and four metabolic genes do not measure flux. Tigit appears in two panels. |
| Released enrichment curves | IL2/STAT5, TNF/NF-kappaB and IFN-gamma transcript sets have positive enrichment for ITDT−PBS and negative enrichment for anti-CD4+ITDT−ITDT. | These are associations among ranked transcripts, not secretion or signaling measurements. ES/NES and leading-edge sets reproduce; Monte Carlo P values do not exactly reproduce. The second IFN-gamma contrast retains BH 0.1201. |
| Omit-one-block plots | Every fixed-panel gene/contrast keeps its direction under all three omissions. A single block does not explain those selected directions. | The panels were source-selected after outcome exposure. Many other genes change sign under omission. Connecting ranges are not confidence intervals; magnitudes still vary and each refit has only two residual degrees of freedom. |
| Ranking sensitivity | Using signed moderated t preserves the three displayed sets' directions, but the second IFN-gamma BH changes from 0.1201 to 0.001024. | “Significant versus not significant” is method-sensitive here. The two curves have different gene orders; their x positions do not identify the same gene. Eighteen full-family pathway/contrast ES directions change. |

All six figures were visually inspected in this review. They are readable for
their stated purpose, with the already disclosed volcano-label overlap. No
figure regeneration or biological rerun was needed. The combination of stable
selected directions and ranking-sensitive significance is the result; neither
part should be omitted to simplify the story.

## How the paper's functional figures complement the RNA

**Figures 1–2** connect local Treg depletion to tumor control and test cellular
requirements in the studied mouse models. The biological implication is that
removing local immune suppression can expose an NK-mediated route against
tumors resistant to CD8 recognition. MHC-I loss by itself is not sufficient
evidence of effective NK control. Tested mouse toxicity outcomes do not establish
human safety or efficacy.

**Figure 4** adds phenotype and time-bounded DNA-synthesis measurements.
KLRG1 is not by itself exhaustion or senescence, SCA-1 is not stemness, and BrdU
does not establish durable expansion or lineage change. These measurements
remain informative without those stronger labels.

**Figure 5B–G** supplies protein, target-cell lysis and perforin-dependent tumor
control evidence that RNA cannot replace. Increased killing coexists with no
CD107a increase in the reported stimulation assay. More granule cargo is the
authors' explanation; a higher degranulation/release rate is not established.
The plotted axes and main Results identify F as IFN-gamma and G as CD107a,
whereas their caption order differs. Preserve this discrepancy in any extraction.

**Figures 6–7** support cDC2/CD4/IL-2 involvement, NK CD25/pSTAT5 and the tested
IL-2 dependence/rescue. The RNA enrichment is consistent with this evidence but
does not independently establish the mechanism. Local pSTAT5 and the separate
trafficking experiment answer different questions. Figure 6J's Tconv FOXP3-positive
caption still requires gating/source clarification before numerical relabeling.

The Treg–CD4–IL-2–NK relationship also has an older precedent in
[Gasteiger et al. (2013), Figures 3–6](https://doi.org/10.1084/jem.20122462),
in a different setting; their Figure 1 also limits a universal activation-ligand
interpretation. Zhang extends the question to local tumor control. The
[literature context](LITERATURE_CONTEXT.md) retains the distinct precedents,
contrary/contextual findings and exact access limits. No new mechanistic RQ is
justified merely by successful replay of an already published pattern.

## Remaining work: a narrower, actionable disposition

| Work | Verified current position | Next informative action |
|---|---|---|
| Released TPM RNA and bounded sensitivities | Complete, with mixed outcomes preserved. | Use the existing figures/tables; no repeat run needed. |
| Adapted raw-read/count reanalysis | Public raw-read access is available. This removes a source-access obstacle, but no new count matrix or execution-ready workflow is qualified. | Freeze a separate exposed-data contract to test whether transcript estimates depend materially on quantification/model choice. Declare reference FASTA/GTF and aggregation, inspect read/library conventions, verify storage/runtime and checksums, then process the same nine pools with block adjustment. Preserve agreement and disagreement. |
| Exact published count/voom replay | Still unresolved: mm10 is reported, but exact transcript annotation/index, original count/length outputs and processing/aggregation provenance are unqualified. | Obtain those original inputs/provenance or label the next run an adapted reanalysis. A chosen modern annotation must not be represented as the authors' original one. TPM cannot be rounded back into counts. |
| Functional numerical reconstruction | Supplement filenames are known, but PDF/XLSX binaries remain unacquired through the tested routes. | Obtain the official supplements through a working normal download or owner-provided copies; verify file content/version, then qualify each panel's units and identities. A descriptive panel extraction may proceed before every cross-panel identity is known; only analyses requiring missing identities stay held. |
| Exact fgsea Monte Carlo P values | Author repository is unchanged; no R-session/backend/random-stream record was found in the saved source files. | Original environment/provenance is required for an exact replay claim. Do not tune seeds/backends to match a P value. This is not necessary to use the reproduced ES/NES or explain the biological result. |

For the adapted count comparison, concordance would reduce concern that the
described RNA direction depends on the released TPM analysis; disagreement
would narrow or weaken that description. Neither outcome resolves bulk-state
mixture, establishes NK function or supplies independent replication. The
high-value immediate follow-up is supplement acquisition/qualification, because
it addresses assay interpretation and biological units beyond another RNA fit.
No bulk FASTQ download, new compute installation or scientific run was launched
for this feasibility check.

## Source/access inspection record

Actual checks: **10 November 2026**; saved requests carry their exact UTC times. These are
source-reading/access observations, not a new statistical analysis or a completed
metadata-qualification run. Fresh raw responses are retained under ignored
`raw_data/zhang_2026/access_review_v1/` for a later prospective contract.

- NCBI Entrez `esearch`, db `sra`, term `PRJNA1213767`, `retmax=20`, returned nine
  records. `efetch` runinfo for those records supplies SRR32063287–SRR32063295,
  corresponding to SRX27412091–SRX27412099 and GSM8748408–GSM8748416. The GSM
  identities can be joined to the existing S0 crosswalk without inventing mouse
  identities. [BioProject](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1213767)
  and [ENA study](https://www.ebi.ac.uk/ena/browser/view/PRJNA1213767).
- ENA `filereport`, accession `PRJNA1213767`, result `read_run`, TSV fields
  `run_accession,experiment_accession,sample_accession,library_layout,library_strategy,read_count,base_count,fastq_bytes,fastq_md5,fastq_ftp,submitted_ftp`:
  nine paired RNA-seq runs, 18 FASTQ URLs with MD5s and 11,886,027,182 compressed
  bytes (about 11.9 GB; working/reference space is additional). A 16-byte range
  request to the listed SRR32063289 mate-1 URL returned HTTP 206 and a gzip
  header. This verifies one delivery route, not full downloads or all checksums.
- SRA and ENA base totals differ. Example SRR32063295's SRA XML lists four read
  lengths, 150/150/17/8; ENA's paired-file base count corresponds to 300 bases per
  spot. The shorter reads' roles and exact export/processing policy remain to be
  checked before raw-read work. The records are not interchangeable byte-level
  inputs. GEO says assembly mm10 but does not identify an exact transcript GTF.
- Rechecked [author repository](https://github.com/wagnerlab-berkeley/itdt_rna_seq_data):
  default-branch tip remains `61ac9a440ba3f9db754ff8b8ad5008b450e647c0`.
  Saved README/Rmd/notebook source searches for runtime/backend/reference terms
  supplied no full session or quantification provenance. No remote changes
  justify repeating the completed replay.
- [PMC's manuscript page](https://pmc.ncbi.nlm.nih.gov/articles/PMC13334847/#supplementary-material)
  lists `All_supplemental_Tables.xlsx`, `Supp__Figures_and_Materials.pdf`, the
  MDAR checklist and `Datafiles_S1-S17.pdf`. Fresh requests for the first, second
  and last returned HTTP 200 **HTML reCAPTCHA pages**, not PDF/XLSX files.
  Ordinary in-app-browser navigation to Datafiles S1–S17 also reached the
  challenge. No challenge was solved or bypassed. The original supplied-paper
  folder contained no matching supplement files.
- The legacy PMC OA endpoint returned 404. [Official current documentation](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/)
  reports the August 2026 service transition, so that response is not evidence
  of absent supplements. The replacement public S3 listing for prefix
  `PMC13334847.` returned only `.json`, `.txt` and `.xml` for version 1.
  Its [metadata](https://pmc-oa-opendata.s3.amazonaws.com/PMC13334847.1/PMC13334847.1.json)
  identify an author manuscript, `license_code=TDM`, `is_pmc_openaccess=false`,
  and no PDF/media URLs. This particular cloud route therefore does not supply
  the binaries; the manuscript page still lists them. The earlier Europe PMC
  OA-service refusal remains a separate bounded route finding.

Selected saved-source SHA-256 values:

| Raw response | SHA-256 |
|---|---|
| `sra_runinfo.csv` | `569d0c5e6b260cd659076f15b381594cc889fbfc6c87e0e6768590f64a66a496` |
| `ena_runs.tsv` | `720f18192e445304a6dce7915fcfa18d202dea8cfaef96111332d7a7b4856434` |
| `sra_example.xml` | `4cfd7c34186c2cf05495d5779ac585bbb85d8a0bce07290242e2308fd09ea1ee` |
| `PMC13334847.1.json` | `aa214e32affb6f61a888eb5ef68a74d9ab3650c46ebb22102583264ff58fb1ea` |

The biological comparison and source reading are unchanged, so the existing
literature scan was reused. Focused access searches used `"NIHMS2180395"
supplement`, `"PMC13334847" supplemental data`, `"sciimmunol.adx4411" "suppl"`
and `site.pmc.ncbi.nlm.nih.gov "PMC Cloud" author manuscripts supplementary`.
Only official repository/publisher/NCBI/ENA records support access conclusions.
Personal lab-fit and training notes remain outside the public repository.

## Review delivery verification

Refreshed `origin/main` remains `1a6769fc3d808ccf6b27aed3ecedc71341026f33`.
Repository validation passes **19,048 checks**, and the base-aware research gate
returns `ok: true` with no errors. The diff changes documentation and one
article-evidence registry reference only; numerical outputs, scripts and frozen
contracts remain unchanged. Existing valid analysis/session/archive checks were
reused rather than rerunning biology for a reading update. Git whitespace checks
pass. CLI and connector identities are `xorca0711`; the effective Git author and
committer are Xorca with the previously verified GitHub-mapped email. This is
local delivery, with no push, merge, author contact or governance change.
