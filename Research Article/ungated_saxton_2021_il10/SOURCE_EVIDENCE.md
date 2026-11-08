# Assay and source evidence map

8 November 2026. [Final paper](https://doi.org/10.1126/science.abc8433) locators use
printed article pages; the supplied PDF includes an extra summary page.

| Evidence | System and treatment | Measured endpoint / units | Source and interpretation boundary |
|---|---|---|---|
| Figure 3 and signaling methods, printed pp.4,9 | Human PBMC subsets, variants/dose series; 20-min stimulation; selected Treg assay 10 nM | Phospho-flow MFI, background-subtracted and normalized within cell type; raw donor/experiment keys not recovered | Published signaling premise only; no RNA-to-pSTAT conversion or cross-assay pairing |
| Figure 4A-D and methods, printed pp.5,9-10 | Human PBMC/monocyte/macrophage assays; LPS 1 ng/mL with active IL-10 10 nM for 24h in cytokine assays | Supernatant ELISA and HLA-DR/CD86 surface staining; published replicate summaries | Separate myeloid evidence, not present in GSE160332 |
| Figure 4E and sepsis methods, printed pp.5,10 | Female C57BL/6 mice, LPS challenge; PBS, WT or 10-DE | Survival to 120h; animal observations | No D25K survival arm; RNA description does not reconstruct survival |
| Figure 5A/B, printed p.6; RNA methods p.10 | Human MACS-isolated CD8 cells, anti-CD3/CD28 activation 3 days; PBS or 10 nM WT/super-10/10-DE for 24h | RNA-seq, two author-reported biological replicates; eight deposited libraries | GSE160332 counts/FPKM and explicit treatment attributes; donor/preparation identities and pairing unknown |
| Figure 5C, printed p.6; methods p.10 | Activated CD8, 3 further days with active ligand 10 nM, then anti-CD3 restimulation 4h; includes D25K | ELISA IFN-gamma, IL-9 and granzyme B | Distinct timing, assays and reported repeats; no invented matching to RNA libraries |
| Figure 5D, printed p.6; methods p.10 | Naive CD4 cells, Th1 differentiation with or without IL-10 10 nM for 5 days | ELISA IFN-gamma | Different cells and assay; not a CD8 RNA arm |
| S9 | Referenced for RNA analysis | Panel and exact processing not qualified | Public supplement access failed; no exact replay claim |

GEO active-ligand protocol text is copied onto PBS samples too. Explicit sample
source/characteristics identify PBS and override interpreting that generic text
as actual PBS ligand exposure. The library aliases are Unt=PBS, BS30=WT IL-10,
BS45=super-10, BS65=10-DE; source suffixes do not prove pairing. Donor attributes
are absent from retrieved BioSample/SRA attributes. The two biological-replicate
statement is preserved; absence of donor keys is not proof of technical duplication.

Count and FPKM tables advertise GRCh38/hg38 and STAR v2.5. Exact gene annotation
release, count assignment options and author plotting transformation remain unknown.
Exact stable-ID rows are preserved; symbols are joined only when uniquely matched.
All source request URLs, response status, dates and SHA-256 values remain in
acquisition records and are bound in the source contract. Published papers and
outcomes were previously read; this cannot be unexposed confirmation.
