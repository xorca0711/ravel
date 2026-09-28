# England et al. 2025 — what the deposits can and cannot still surface

**Written 28 September 2026**, from a second reading of the paper and its STAR Methods against the
deposited material. This is a scoping ledger, not a results file: it records which of the paper's
claims can still be interrogated with what was released, which are closed, and which are blocked and
on what. Results live in [RESULTS_BATCH1.md](RESULTS_BATCH1.md),
[RESULTS_CONTINUATION.md](RESULTS_CONTINUATION.md) and [RESULTS_FOLLOWUP.md](RESULTS_FOLLOWUP.md).

## What the paper actually ran

Worth stating plainly, because it bounds every "reproduce their trajectory" request: the study ran
**no computational trajectory analysis**. Seurat v4.3.0 on R 4.2.1, CellRanger v3.1.0 against GRCm38,
QC removing >15% mitochondrial reads, <1,000 genes or >50,000 UMIs, log-normalisation and scaling,
top 5,000 variable genes, PCA, Louvain clustering, UMAP on the first two dimensions, contaminant
clusters discarded on Ptprc / Pecam1 / Col1a1 / Foxj1, then two rounds of integration with
renormalisation and re-clustering, markers by FindMarkers, and CellChat for ligand–receptor
inference. No pseudotime, no RNA velocity, no Monocle, no PAGA. The reversibility and bidirectionality
claims rest on **protein and functional assays**: CD177/Itga2 double-positive immunofluorescence,
organoids from sorted CD177+, Itga2+, double-negative and double-positive fractions, orthotopic
transplantation into NSG mice, EdU label retention, and the absence of a clone-size-to-composition
correlation. Any trajectory we compute is our own addition and carries no directional authority; RNA
velocity is not available at all, because the deposit holds filtered count matrices with no
spliced/unspliced layers.

## Claim-by-claim ledger

| # | Source claim (figure) | Evidence type in paper | Deposited material | Our status |
| --- | --- | --- | --- | --- |
| 1 | A two-population model encapsulates homeostatic AT2 dynamics (Fig 1) | clone-size distributions + simulated-likelihood fit | Zenodo clone archive (conf1w–conf72w, 3–5 mice each); MATLAB `sim_two_pop_model.m` | **Audited, one finding open.** Confetti mixture weights are not identifiable from the deposited sizes (0.09–0.89, overlapping components). Folded into **A17** |
| 2 | Two-population dynamics are conserved in KrasG12D initiation (Fig 2) | same, on kras4d–kras4w | clone archive (RFP and YFP separately) | **Audited, finding open.** The deposited script's S-loss branch changes the q = 0.7 clone-size distribution materially (KS 0.104–0.281; size ≥2 fraction 0.91–0.96 literal vs 0.50–0.59 corrected). Refit specified as FU_S / **A17**, ready to run |
| 3 | Mutant AT2 cells co-opt a regeneration program (Fig 3) | scRNA-seq clustering, state occupancy | GSE247505, 20 libraries | **Reproduced and extended.** EN1–EN4. Transition gate is cluster-concentrated; AT1 gate is not, which motivated the calibrated module gate (FU_B) |
| 4 | Reversible transitions between mutant states (Fig 4) | IF double-positives, sorted organoids, transplantation, EdU | **none of it** — no protein, no sorted fractions, no lineage barcodes | **Closed on this deposit.** Direction and reversibility are not recoverable from these matrices; deliberately not claimed. Velocity impossible (no spliced/unspliced) |
| 5 | Oncogenic clones increase wild-type proliferation, proximity-dependently (Fig 5) | Ki67, EdU, clone size vs distance | pooled spatial pair rows, no mouse or clone IDs | **Reproduced descriptively** (FU_W): size slope −109 to −16% per 100 um, robust to bin occupancy. Inferential test blocked without identifiers → **A18** |
| 6 | Oncogenic clones trigger a regenerative response in tissue-sharing wild-type AT2 (Fig 6) | pro-Sftpc− fraction, IF, scRNA-seq of YFP+ cells | pooled spatial rows + WT-in-oncogenic YFP libraries | **Reproduced on both axes.** EN4 gives the transcriptional side (Spp1 +3.3, Dlk1 +4.0, transition RNA +1.0, priming +1.7); FU_W gives the spatial side, where the proximity-independence claim is *consistent with* but not strongly supported by the deposit |
| 7 | Sustained NF-κB activation distinguishes oncogenesis from regeneration (Fig 7) | Il1r1 deletion tracing, scRNA-seq, BMS-345541 | Il1r1 het/homozygous libraries at 2 and 12 weeks | **Reproduced.** EN2: transition occupancy −0.057 / −0.123, within-AT2 Cd177 ≈ −4 log2, and **no AT1 maturation rescue** (−0.50 / −0.60). The BMS arm is not deposited |

## Open opportunities, ranked by whether they could change a conclusion

1. **FU_S, the corrected-implementation refit (A17).** The only item that could overturn a
   *foundational* claim of the paper, needs no new data, and is already specified in the frozen
   contract. Highest value per unit of work.
2. **The two-channel test for wild-type growth versus differentiation (A18).** Matches the study's
   own stated limitation and the owner's flagged unknown. Descriptively complete; the interaction
   test needs mouse-level and clone-level rows, so the action is a **request to the authors** for the
   identifiers behind the pooled arrays, which would also unblock every clone-level estimate above.
3. **Cd177 attribution (A16).** Within-subcluster conditioning already dissolved most of the
   phenotype and left priming-associated RNA standing in 5 of 7 subclusters. The discriminating test
   is a wet experiment; no GEO deposit pairs CD177 sorting with a proliferation readout in lung.
4. **Spliced/unspliced re-quantification of the 68 PRJNA1039244 runs.** The only route to
   directional evidence from this deposit. Needs remote compute and separate authorization, and would
   still not settle reversibility, only local direction.
5. **Loss of equipotency under a second oncogenic hit.** The paper's Discussion raises Kras;Trp53 and
   an Itga2+ high-plasticity state; the owner's notes flag the mechanism as open. GSE253461 (39
   samples, KrasG12D p53−/− AT2 cells, organoids and co-cultures) is the closest public resource and
   would support a descriptive transfer of our frozen gates and modules only. **Not promoted to a
   research question**: it needs an eligibility check first, and a descriptive transfer cannot
   establish loss of equipotency, which is a clone-level property.

## Blocked, with the specific missing item

- **Biological pool and animal identities for the 20 libraries.** Without them every scRNA-seq
  estimate in this package stays a library-level description, and the replicate-to-replicate spread
  we measured (response-high fraction differing 2–3× between libraries of the same condition) cannot
  be separated from animal variation.
- **Mouse and clone identifiers for the spatial pair arrays.** All 25,173 rows are marked
  `pooled_only` with `biological_inference_allowed = False`.
- **The paper's Experiment 1 library count.** The text describes 13 Experiment-1 libraries; 10 are
  deposited. A GEO check on 28 September 2026 found no additional series: GSE247503
  (10 samples) and GSE247504 (10) total the 20 deposited libraries, and a keyword search on the paper
  title and the Red2Kras model surfaced no further England series. **This is an arithmetic and search
  argument, not a machine-confirmed linkage**: the GEO `relations` field came back empty for
  GSE247505, GSE247503 and GSE247504 alike, so the superseries-to-subseries structure was not
  returned by the API and a third subseries is not formally excluded. Either the missing three were
  not deposited or the text counts something other than libraries. Unresolved; an author query is the
  only route.
- **Mendeley Data `ss6pb96pty` (Figure 1 of the Mendeley deposit)**, cited for the Figure 6 wild-type
  composition data, returns HTTP 403 and has never been inspected.
- **The BMS-345541 NF-κB inhibition arm** of Figure 7 has no deposited sequencing.

## External data candidates

Searched on GEO 28 September 2026. Eligibility unchecked in every case; none is a matched replication
of this design, and each would support descriptive transfer of our frozen gates only.

| Series | n | Content | Bears on |
| --- | --- | --- | --- |
| GSE253461 | 39 | KrasG12D p53−/− Rosa26-YFP AT2 cells, organoids, co-cultures | item 5 above; A16 attribution |
| GSE316244, GSE316243, GSE316241 | 4, 2, 2 | early fibrotic niches, KrasG12D AT2 reprogramming, Areg–EGFR | A18 mediator range; A16 |
| GSE227719 | 4 | KrasG12D;p53 AT2 organoid multiome | item 5 |
| GSE310539 | 8 | AP-1-driven AT2 transition, multiome | A8, A11 |
| GSE267731 | 14 | cell of origin in lung adenocarcinoma | item 5 |

Already used as external comparators: **GSE145031** (Choi 2020) and **GSE262927** (Niethamer 2025),
in EN7 and FU_B. Neither holds a Cd177-positive transitional population large enough for the
contrast (2 of 117 and 0–1 of 1–50 transition cells), which is itself the result that closed the
CD177-transfer question.
