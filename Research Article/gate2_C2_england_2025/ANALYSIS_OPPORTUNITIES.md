# England et al. 2025 — what the deposits can and cannot still surface

**Interpretation amendment, 28 September 2026:** the [source/code audit](../../docs/audits/2026-09-28-england-paper-rqs/REPORT.md)
supersedes the earlier A16 population, A17 readiness and Figure-7 reproduction
interpretations. The later [corrected A16 C1](../../RQ_Specified/A16_cd177_state_attribution/correction_20260928/reports/CORRECTED_C1_REPORT.md)
and [A17 source accounting](../../docs/roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md)
complete bounded follow-through on that review. Original numerical reports and
contracts remain unchanged.

**Written 28 September 2026**, from a second reading of the paper and its STAR Methods against the
deposited material. This is a scoping ledger, not a results file: it records which of the paper's
claims can still be interrogated with what was released, which are closed, and which are blocked and
on what. Results live in [RESULTS_BATCH1.md](RESULTS_BATCH1.md),
[RESULTS_CONTINUATION.md](RESULTS_CONTINUATION.md) and [RESULTS_FOLLOWUP.md](RESULTS_FOLLOWUP.md).

## Source methods and interpretation scope

The inspected article/supplements describe clustering, integration, signatures,
correlations and CellChat, but do not document a computational directional
trajectory method. The contribution statement mentions trajectory analysis;
absence of a documented algorithm is not proof that none was performed.
Sorted-state organoids and transplantation provide functional plasticity
evidence. Double-positive staining alone does not establish interconversion.
Deposited filtered matrices lack spliced/unspliced layers; any re-quantified
velocity analysis would remain model-dependent, not lineage ground truth.

## Claim-by-claim ledger

| # | Source claim (figure) | Evidence type in paper | Deposited material | Our status |
| --- | --- | --- | --- | --- |
| 1 | A two-population model encapsulates homeostatic AT2 dynamics (Fig 1) | clone-size distributions + simulated-likelihood fit | Zenodo clone archive (conf1w–conf72w, 3–5 mice each); MATLAB `sim_two_pop_model.m` | **Audited, one finding open.** Confetti mixture weights are not identifiable from the deposited sizes (0.09–0.89, overlapping components). Folded into **A17** |
| 2 | Two-population dynamics are conserved in KrasG12D initiation (Fig 2) | same, on kras4d–kras4w | clone archive (RFP and YFP separately) | **Audited, finding open.** The deposited script's S-loss branch changes the q = 0.7 clone-size distribution materially (KS 0.104–0.281; size ≥2 fraction 0.91–0.96 literal vs 0.57–0.59 fixed branch vs 0.50–0.55 Gillespie). **A17** source-count reconciliation and source-code mapping are complete. FU_S model/score amendments, published-curve provenance and the full stochastic refit remain open |
| 3 | Mutant AT2 cells co-opt a regeneration program (Fig 3) | scRNA-seq clustering, state occupancy | GSE247505, 20 libraries | **RNA proxies reproduced and extended; exact author states not recovered.** EN1–EN4. Transition gate is cluster-concentrated; AT1 gate is not, which motivated the calibrated module gate (FU_B) |
| 4 | Reversible transitions between mutant states (Fig 4) | IF double-positives, sorted organoids, transplantation, EdU | **none of it** — no protein, no sorted fractions, no lineage barcodes | **Closed on this deposit.** Direction and reversibility are not recoverable from these matrices; deliberately not claimed. Velocity impossible (no spliced/unspliced) |
| 5 | Oncogenic clones increase wild-type proliferation, proximity-dependently (Fig 5) | Ki67, EdU, clone size vs distance | pooled spatial pair rows, no mouse or clone IDs | **Reproduced descriptively** (FU_W): size slope −109 to −16% per 100 um, robust to bin occupancy. Inferential test blocked without identifiers → **A18** |
| 6 | Oncogenic clones trigger a regenerative response in tissue-sharing wild-type AT2 (Fig 6) | pro-Sftpc− fraction, IF, scRNA-seq of YFP+ cells | pooled spatial rows + WT-in-oncogenic YFP libraries | **Reproduced on both axes.** EN4 gives the transcriptional side (Spp1 +3.3, Dlk1 +4.0, transition RNA +1.0, priming +1.7); FU_W gives the spatial side, where the proximity-independence claim is *consistent with* but not strongly supported by the deposit |
| 7 | Sustained NF-kB activation distinguishes oncogenesis from regeneration (Fig 7) | Il1r1 loss and genetic/pharmacological NF-kB inhibition | Il1r1 het/homozygous RNA libraries; no deposited BMS RNA arm | **Partial RNA comparison only.** EN2 tests genotype-associated entry/state differences, not post-entry NF-kB rescue, pathway activity or mature repair. Its lower transition occupancy and AT1 scores are not a failure to reproduce the inhibition experiment |

## Current opportunities and prerequisites

1. **A16 attribution:** corrected C1 now preserves the original compartment and
   separate libraries with a frozen embedding and common effect scale. Priming
   attenuates, but substantial residual matching imbalance prevents attribution.
   Specificity, contamination limits and independent functional outcomes remain
   unresolved; repeating the old pooled FU_C comparison would not settle them.
2. **A17 clone-growth models:** raw-source accounting reproduces all 58 count
   rows and identifies 11 primary mice. Source-code parameter mapping and the
   14-day switch are documented; published-curve provenance remains unresolved.
   FU_S still needs a model/score amendment before a held-out comparison; the
   full stochastic refit has not run. A code defect cannot by itself overturn
   biological founder evidence.
3. **E-N1/E-N2 mouse-level questions:** assess distributed identity loss and
   paired mutant burden/WT response with the nonspatial mouse/lobe hierarchy.
   These are narrower than A18's blocked spatial interaction.
4. **E-N4/E-N5 RNA pilots:** assess coordinated output and incomplete maturation
   as extensions of existing questions. Classification is supporting work.
5. **E-N6/E-N7/E-N8 mechanisms:** second-hit effects, feedback induction and
   SPP1/DLK1 interaction need their stated metadata or mechanistic endpoints.
   Public RNA transfer cannot supply missing causal contrasts.

Read the [eight hypothesis cards](CANDIDATE_HYPOTHESES.md) and
[technical gates](CANDIDATE_CHECKS.md). A18 still needs spatial mouse/clone IDs
for inference; those IDs are not missing from every nonspatial clone estimate.
Requesting author data is a possible next step, not an action taken here.

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
