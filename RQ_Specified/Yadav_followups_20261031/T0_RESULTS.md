# T0 source and endpoint qualification

31 October 2026. T0-B/R (Wg-P06) and T0-E (Yd1-P02) are complete within the
authorized metadata scope. **No new biological effect, expression, flux or
joint repair analysis was run.** The reviewed plan was adopted at
`1473ad87d1246d336402d2ea5f6a2881bc51d774`; the two contracts and their code
were frozen at `33c39eed1903cd56bc50de64fd048498b53a6d3b` before execution.

The next decision is whether to authorize the bounded
[T1 designs](T1_DESIGNS.md). A processed-isotope description is feasible for
unambiguous Hamanaka blocks. Collagen-effect reconstruction, exact published
error bars, flux and a joint ARG1–matrix–mature-repair effect retain specific
holds. This does not change scientific acceptance, canonical questions or grades.

## Execution and source authority

| Owner | Frozen contract and receipt | Evidence produced |
| --- | --- | --- |
| Wg-P06, shared B/R acquisition | [Contract](config/t0_br_contract_v1.json), [receipt](../../analysis/research/runs/Wg_P06_followup_t0_br_v1/receipt.json) | [Assay/unit map](../../analysis/research/runs/Wg_P06_followup_t0_br_v1/assay_unit_map.csv), [tracer map](../../analysis/research/runs/Wg_P06_followup_t0_br_v1/tracer_map.csv), [source issues](../../analysis/research/runs/Wg_P06_followup_t0_br_v1/source_issues.csv), [GEO sample map](../../analysis/research/runs/Wg_P06_followup_t0_br_v1/geo_sample_map.csv), [workbook layout](../../analysis/research/runs/Wg_P06_followup_t0_br_v1/workbook_layout.json), [sample labels](../../analysis/research/runs/Wg_P06_followup_t0_br_v1/workbook_sample_map.csv), [file inventory](../../analysis/research/runs/Wg_P06_followup_t0_br_v1/file_inventory.csv) |
| Yd1-P02, separate endpoint question | [Contract](config/t0_e_contract_v1.json), [receipt](../../analysis/research/runs/Yd1_P02_followup_t0_e_v1/receipt.json) | [Endpoint/unit map](../../analysis/research/runs/Yd1_P02_followup_t0_e_v1/endpoint_unit_map.csv), [disposition](../../analysis/research/runs/Yd1_P02_followup_t0_e_v1/t1_disposition.json) |

Primary-source citations below establish published observations. Repository
records establish this project's prior results; they are not independent
replication of the cited studies. All outcomes, source headers and plotted
patterns were exposed before freeze. The metadata work is descriptive.

| Primary source/version | Completed inspection and access |
| --- | --- |
| [Hamanaka 2025, published DOI](https://doi.org/10.1042/BCJ20253033), [PMC12235046](https://pmc.ncbi.nlm.nih.gov/articles/PMC12235046/) | Europe PMC full JATS; Figs. 3–6 images; seven-page supplement, especially S1/S4–S7. This published article supersedes its preprint. |
| [Figshare 28087574 v1](https://doi.org/10.6084/m9.figshare.28087574.v1), published 7 January 2025 | One 56,247-byte processed workbook, source MD5 `08a4c633551c7ee448a9c0696c4ee3c0`, independently matched. Eleven sheet schemas/sample labels inspected, not numerical effects. This prepublication deposit has source-version discrepancies below. |
| [GSE273882](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273882), series updated 3 July 2025 | All 52 header-only sample records joined to series and file listing. The listed 139,264,000-byte archive and individual expression files were not downloaded. It is RNA-seq, not metabolomics. |
| [Author code](https://github.com/MutluHamanakaLab/Arginine/tree/3e1f22fa215cd8d7176f499c297e1cf33ed8ff3c), commit `3e1f22fa215cd8d7176f499c297e1cf33ed8ff3c` | README and recursive tree read. Listed scripts cover Fig. 1D and Fig. 2/S2–S3 transcriptomic analyses; no tracing-correction script is listed. Scripts were not executed. |
| [Lee 2024](https://doi.org/10.1038/s12276-024-01170-w), [PMC10907606](https://pmc.ncbi.nlm.nih.gov/articles/PMC10907606/) | Full JATS, Figs. 6–7 images, necessary Fig. 5 text/methods, six-page supplement including S1/S3/S4. |
| [Li et al., Atg5 2026](https://doi.org/10.1016/j.stemcr.2026.102979), [PMC13385427](https://pmc.ncbi.nlm.nih.gov/articles/PMC13385427/) | Published 2 July, collection 14 July 2026. Full JATS, Fig. 2/6 images including 6L–M, twelve-page Document S1 and relevant methods. No need to acquire the 28.6 MB combined article/supplement or expression data for this endpoint decision. |

Actual UTC retrieval times, URLs, bytes, SHA-256 values, archive members and
failures are retained in [B/R access](../../analysis/research/runs/Wg_P06_followup_t0_br_v1/source_access.json)
and [E access](../../analysis/research/runs/Yd1_P02_followup_t0_e_v1/source_access.json).
Contract hashes bind the ignored cache `raw_data/Yadav_followups_T0_20261031/`.
Direct PMC PDF links returned HTML challenges; OA utility links returned 404;
the Hamanaka PDF mirror returned 403; a Springer CDN attempt failed DNS. These
are recorded access failures, not missing biological results. Europe PMC ZIPs
and Elsevier's small supplement/figure assets supplied the necessary material.
The initial GEO `targ=all` request exceeded the 5 MB cap and was discarded unread;
the successful `targ=gsm&view=brief` records contain no expression rows.

## T0-B: what substrate evidence is actually available

Hamanaka tests **recipient fibroblasts**, not the nominated neutrophil-source
ARG1 perturbation. Standard HPLM has Arg/Orn/Cit at 0.11/0.07/0.04 mM; the
reported DMEM context has 0.4 mM Arg without added Orn/Cit. The general culture
method uses TGF-beta (1 ng/ml) after 24 h serum starvation. Media contain other
differences, so HPLM versus DMEM is not a pure arginine contrast.

Fig. 5A/B measures lysate collagen1, alpha-SMA and signaling proteins at 0/24/48 h;
Fig. 5C/D measures SMAD phosphorylation over 0–120 min. Fig. 5E/F is 24 h relative
qPCR, normalized to Arg-replete untreated. These are not measurements of
newly deposited collagen or viable-recipient-normalized production. No numeric
source sheet for these blots/qPCR panels was recovered. Fig. 6D/F supplies
intracellular metabolite peak areas at 48 h, not calibrated concentration,
extracellular exposure or synthesis rate.

The donor/clone distinction matters. Three control and three IPF clones are
explicit for the clone comparisons, including 6H. Figs. 3/4 and 5E/F refer to
four biologic replicates without a donor/preparation/well key. The common
Hamanaka unit string in the map summarizes this legend language; it does not
establish a replicate count for Fig. 5's blots. GEO has 16 NHLF media
libraries plus 36 libraries with six clone-title prefixes, three suffixes per
condition. The metabolite clone sheet has four suffixes per condition. Neither
equal suffixes nor shared clone tokens establish cross-assay pairing. The GEO
`clone` characteristic is NHLF/Control/IPF, not a resolved independent donor ID.

Preserved findings that constrain the proposed question include Orn-only failure
to rescue complete Arg/Orn/Cit dropout, Cit/ASS1 rescue in the appropriate
context, ASS1 dispensability when Arg is present, retained Cit rescue in IPF
clones, the HPLM SERPINE1 comparison labelled NS, and S7's TGF-treated Arg-pool
comparisons labelled NS. None implies equivalence. The measured recipient
requirement can stand even if source ARG1 never changes exposure enough to
produce compensation in the nominated coculture.

## T0-R: route, abundance, signaling and flux

Fig. 3/S4 traces 13C6-Arg, guanido-15N2-Arg, D4-Cit and 15N2-Orn in HPLM.
Fig. 4/S5 traces 13C6-Arg, guanido-15N2-Arg and 13C5-Gln in DMEM. Products are
intracellular amino-acid/intermediate/polyamine pools; no isolated labelled
collagen, hydroxyproline or matched source-conditioned extracellular trajectory
is supplied. Main figures show relative metabolite abundance; supplements show
label fractions. The workbook contains processed areas and fractions, not raw
instrument files. Methods name IsoCor natural-abundance correction, but exact
correction parameters, isotope purity and tracer pulse duration are unresolved.
Intracellular precursor label is not an extracellular enrichment time course.

The reported negative Arg-to-Pro and weak Arg-to-Orn labeling, medium-dependent
Cit behavior, Orn-to-putrescine labeling and Gln contribution remain in the map.
They are model/context constraints, not reasons to omit inconvenient panels.
OAT direction is not uniquely identifiable from expression or inhibition alone.

Source fidelity needs these explicit exceptions:

- **Fig. 4F:** three supplied labels per condition for every metabolite, versus
  four in Fig. 4/S5 legends. Fig. 4 says SEM, S5 says SD. Do not add a fourth sample
  or claim exact published uncertainty reconstruction.
- **Fig. 3F:** fraction headers AP15/AQ15 repeat M+14/M+15 after M+16/M+17.
  Do not silently relabel them. The Methods also mention 13C5-Cit whereas this
  panel, the catalogue and workbook identify D4-Cit.
- **Fig. 4B putrescine:** rows 63–70 repeat metadata in P:S; T:X lacks its own
  isotope header. The earlier P:Z header cannot simply be inherited.
- **Fig. 6D/F:** A/O/C/AOC/unprefixed labels suggest the published add-back
  conditions, but the exact source sample key is absent. Treat that mapping as
  an explicit inference requiring review, not recovered metadata.

Lee Fig. 6 supplies MRC5 proline ELISA, PRODH protein and MitoSOX/flow endpoints.
PRODH knockdown in OAT-overexpressing cells supports a signaling alternative
in that model; it does not measure collagen precursor incorporation or flux.
The ROS-specific method uses three days, distinct from the general 48 h method.
Fig. 7 is a separate mouse inhibitor study: tissue hydroxyproline, active TGF-beta,
OAT and inflammation at day 21. It cannot identify a fibroblast-specific source
ARG1 mechanism. S3's cytotoxicity assay is in cells named C57MG, not the MRC5
recipient model or the proposed primary coculture. Its limited assay cannot
establish general viability preservation.

The [reviewed Yadav result](../../Research%20Article/gate2_W3_yadav_2025/extensions_20261031/FINAL_SYNTHESIS.md)
remains separate: Fig. 3K is relative Pro/Hyp abundance. Discussion wording does
not convert the measured panel into isotope flux. Existing OAT/rescue,
donor-reuse, spatial and source-version limits remain unchanged.

## T0-E: matrix and mature epithelial output are not jointly qualified

Atg5 deletion in Tbx4-lineage mesenchyme is a relevant **endpoint precedent**,
not an ARG1 intervention. Fig. 2 includes tissue hydroxyproline in ug/g,
fibrotic area, RNA and relative protein. Fig. 6H–J measures day 10 organoid
formation and diameter; the legend labels n=5 mice/group pooled across three
experiments. Methods state 20,000 starting AT2 cells and 200,000 fibroblasts per
well and passage2 fibroblasts, but do not provide animal-to-well/AT2-source
crossing or individual preparation keys. Equal initial inputs do not establish
equal subsequent viable support.

SB431542 is removed after day 10 for differentiation. The exact subsequent
harvest day is not specified for 6K–M. Fig. 6K is relative T1alpha RNA (n=3/group).
Fig. 6L–M adds staining evidence (n=4/group), which must not be omitted: the image
axes are **SPC+/DAPI+ percent** and **PDPN+/SPC+ percent**. These are not
absolute lineage-linked mature descendants per starting AT2 input. There is no
qualified mature functional assay or per-unit matrix-to-epithelial join.
Diameter and SPC-ratio comparisons labelled NS do not establish preservation.
The Hgf RNA comparison is also NS; factor RNA is not secreted protein.

The mouse scRNA-seq Methods explicitly pool three mice into one library per
group. Cells/scores cannot supply replicate-aware sample inference. No new
classifier or expression analysis was run. Available supplements add biological
context but not the missing paired raw endpoint table.

The [endpoint map](../../analysis/research/runs/Yd1_P02_followup_t0_e_v1/endpoint_unit_map.csv)
keeps A13's failed proxy/coverage results, A20's Fzd2/Fzd1 mature-output question
and unmatched human cohorts, A8's missing early-to-later link, A19's
conversion-versus-selection uncertainty, and A22's failed generalization intact.
Atg5 does not nominate an ARG1 mediator, rescue those negatives or establish
that reducing matrix restores mature epithelium.

## Verification and delivery boundary

Both receipts verify. The independent verifier passed 26 checks, using openpyxl
against the runner's separate XLSX-XML parser, source-provided MD5, GEO series
joins/zero-data rows and primary XML. It verified the three-label conflict,
duplicate/shifted headers and distinct Atg5 endpoint units. Visual inspection
covered Hamanaka Figs. 3–6, Lee Figs. 6–7, Atg5 Figs. 2/6, and rendered Hamanaka S5, Lee S3 and
Atg5 supplement legends. Remaining relevant supplement pages were read as PDF
text. This is source verification, not biological replication or human review.

The execution ledger records 12,376 passing repository checks and a passing
research gate against freshly fetched main. All earlier
contracts, receipts, frozen outputs, A0–A31 and guides are preserved. Original
X3–X5 and spatial holds are not reopened. Local cache and source papers remain
ignored; no large expression/raw-MS files, remote writes, outreach or bench
work occurred. Stop here for T0 review before any T1 numerical work.
