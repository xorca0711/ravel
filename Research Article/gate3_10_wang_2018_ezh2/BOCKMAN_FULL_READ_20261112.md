# Bockman full-paper review and revised tumor extension

12 November 2026, Asia/Seoul. Literature synthesis for Wang18-P01 and its
conditional tumor extension; no new experiment, effect estimate or RQ.
Read with the [public-source audit](public_gap_followup_20261112/G1_SOURCE_AUDIT_V1.md)
and [Wang interpretation](BIOLOGICAL_INTERPRETATION_V1.md).

## Source and completed reading

[Bockman et al., Intratumoral Regulatory T-cell Ablation Mediates Tumor
Control Systemically without Autoimmunity](https://doi.org/10.1158/0008-5472.CAN-25-3473),
Cancer Research 86:4028–4042 (2026), PMID 42228092, PMCID PMC13321386,
NIHMS2188295. Read the complete 34-page author manuscript: Introduction,
Methods, Results, Discussion, references and main Figure 1–7 legends; visually
inspected all seven main figures. This is the author manuscript marked
available in PMC 2 July 2026, not a claim to have compared every revision
against the publisher's version of record.

Undermind recovered the open-access PDF after direct publisher/PMC access
failed. Local ignored source:
`raw_data/literature/bockman_2026_20261112/Bockman_2026.pdf`, 2,931,174 bytes,
SHA-256 `c1dfab6992bc0b28b4594b8ab2392dc9f42f6006425cfa83c9ce28f6067ce499`.
NCBI [PMC EFetch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=13321386)
also supplied the article XML. The PDF, XML, extracted text and rendered main
pages remain in that ignored directory. The manuscript links seven supplementary
PDFs but does not embed them. Direct supplement requests returned HTML;
Europe PMC's supplement route returned a non-ZIP response. Consequently S1–S7
below are **main-text descriptions, not independently read supplement panels**.
The supplement/source-data access gap does not prevent reading the full main
paper or revising its mechanistic interpretation.

## Published flow and its limits

| Step / exact locator | Published evidence | What it does not establish |
|---|---|---|
| Local depletion, Fig. 1A–F; manuscript pp. 6–7, 21–22 | Intratumoral DT in Foxp3-DTR hosts reduces tumor Treg frequency and controls MC38/B16F10 growth; the autochthonous KP sarcoma comparison includes a DTR-negative control. | No EZH2 perturbation. Reduced FOXP3/CD25 frequency is not an absolute viable-lineage recovery measurement. |
| Peripheral effects, Fig. 2; pp. 7, 23–24 | Compared with systemic DT, local treatment preserves peripheral Tregs more effectively and avoids the measured weight, activation and tissue-pathology changes over the assessed window. | Not universal or clinical safety. Moderate tdLN Treg reduction remains, and Discussion p. 15 explicitly leaves a contribution from it possible. |
| Activation, Fig. 3; pp. 8, 25–26 | Local conventional CD4/CD8 activation increases; stimulated intracellular IL-2-positive CD4 cells increase. TNF/IFN-gamma responses do not show the same increase. | Cytokine-positive frequency after ex-vivo stimulation is not in-vivo extracellular IL-2 availability. Activated/increased CD8 cells need not be necessary effectors. |
| Effector and DC perturbations, Fig. 4B–H; pp. 8–10, 27–28 | CD4 depletion impairs treated-tumor control; adding CD8 depletion removes residual control. CD8 or NK depletion alone does not prevent control in these tested settings. Pan-cDC depletion prevents control; control remains in either Batf3-deficient or Zeb2-enhancer-deficient hosts. | **cDC2 is not uniquely necessary in the single-tumor comparison.** Retained control with either subtype absent supports alternative routes; an insignificant difference is not a formal equivalence result. Germline subset deficiencies also permit compensation. |
| Distal tumors, Fig. 5; pp. 10–11, 29–30 | One treated tumor can promote control of a contralateral tumor of the same line. MC38/B16F10 mismatching removes distal benefit. | Not spontaneous metastatic disease or direct proof of a particular shared antigen. Host-level tumor pairs are nested, not independent mice. Treatment ends when the injected lesion is no longer palpable; later distal escape is not evidence of durable eradication. |
| Site-dependent effectors, Fig. 6; pp. 11–12, 31–32 | CD8 depletion impairs distal control despite maintained control at the treated site; CD4 and cDC perturbations impair both. Batf3 deficiency does not prevent either. | The distal experiment does not itself test Zeb2 deficiency. Fig. 6D/F each came from one experiment with five mice/group; do not silently treat all panels as repeated experiments. |
| DC uptake, Fig. 7; pp. 12, 33–34 | In CD8-predepleted MC38-mCherry hosts, local Treg ablation increases tumor cDC2 antigen-associated fluorescence and costimulatory markers. Ex-vivo bead uptake also increases, more prominently in cDC2s. | Fluorescent uptake and costimulation are distinct from peptide–MHC presentation and from T-cell killing. CD8 predepletion limits one antigen-release alternative, not all cell-death or population-selection alternatives. |
| Presentation/other supporting results, Results pp. 6, 8, 10, 12–13 | Main text describes anti-CCR8 failure in B16F10 despite depletion (S1), retained control under FTY720 (S3), emergent CD8 dependence in cDC2-deficient hosts (S4I), and increased cDC2 SIINFEKL–H-2Kb display in B2m-deficient OVA tumors (S7). | Supplements were not recovered. The reported S7 assay is **MHC-I**, not a direct demonstration of the proposed cDC2-to-CD4 MHC-II presentation step. FTY720 does not identify lineage history or exclude every tdLN contribution. |

Anti-CCR8 is administered **systemically (IP)** in Methods p. 5; “intratumoral
Treg depletion” describes its intended cellular effect, not its injection route.
It is not interchangeable with intratumoral DT. The manuscript's sarcoma
induction dose and some timing/statistical wording differ between Methods and
Results/legends; these are reasons to resolve source methods before reproducing
an assay, not to silently choose a value. No protocol was implemented here.

## What this review changes

The earlier neighboring-paper note called Bockman a cDC2/CD4-dependent
precedent from indexed text. That compressed description is superseded:
**the dependence is conditional on tumor site, model and remaining immune
populations.** The full paper's Fig. 4H and Fig. 6 are decisive qualifications.
Bockman's own broader cDC2 language should be read alongside those perturbations.

[Zhang 2026](https://doi.org/10.1126/sciimmunol.adx4411) supplies a different
published setting: MHC-I/recognition context, CD4-derived IL-2 and NK-mediated
control, including the RMA/H60a comparison in Fig. 2H–J. It is not contradicted
simply by Bockman's NK-depletion result in other tumor settings. Bockman cites
Zhang as reference 57; Zhang cites Bockman's preprint as reference 64. They share
authors and laboratory/model resources. No mouse-level cross-paper manifest
was recovered, so neither independence nor animal reuse is asserted and their
results are not pooled as independent replication.

Wang already compares EZH2 disruption with depletion (Fig. 7), and its MC38
effector-depletion result includes both CD4 and CD8 requirements (S2E, previously
read source synthesis). Thus neither “local Tregs suppress tumors,” “depletion
helps,” “CD4 can contribute,” nor simply adding a depletion comparator is a
new contribution here. The existing bulk RNA analyses add cultured-Treg
expression robustness/context evidence, not a tumor effector-dependence test.

## Conditional extension beyond Bockman

**Remaining question:** under a defined tumor context, does perturbing EZH2
in established Tregs alter their restraint of DC antigen handling while
preserving a measurable viable Treg population, and how does that response
compare with local depletion? This is an intervention/context comparison, not
a claim that an A33–A35 gene mediates tumor control or that the idea is novel.
Bockman removes Tregs; it does not estimate the effect of an acute,
Treg-restricted EZH2 perturbation on this endpoint. Wang supplies an existing
reprogramming/depletion precedent, so the proposed increment is the **specific
DC functional response and its defined context**, rather than that distinction
alone. A refreshed discriminator-specific literature review and model feasibility
check are required before a numerical contract or experiment package.

1. **Qualify the intervention and unit.** Define the tumor line, MHC-I and
   relevant recognition status, treated site, baseline tumor range, established
   Treg perturbation timing, actual controls and target engagement. Independent
   hosts are units; paired tumors, sampled cells and aliquots are nested. Use
   absolute viable lineage recovery and current FOXP3 state alongside the
   functional endpoint. Systemic inhibitor exposure cannot identify a
   Treg-intrinsic effect without an appropriate attribution design. Wang S4D
   provides an ex-vivo engagement precedent, not in-vivo tumor qualification.
2. **Estimate the bounded functional comparison first.** Compare qualified
   Treg-restricted EZH2 perturbation with matched control, measuring a specified
   DC antigen-uptake endpoint. Add a local-depletion comparator only if directly
   testing the relation to ablation. Collect comparable tissue and time windows;
   report uptake, DC composition, costimulation and Treg recovery separately.
   An uptake effect alone does not establish presentation. A CD4-presentation
   claim needs a relevant MHC-II/functional CD4 assay; the reported Bockman S7
   MHC-I assay cannot substitute for it.
3. **Review before extending.** A functional shift with retained viable-lineage
   recovery would support altered restraint in that tested setting, while still
   allowing changes among surviving Treg states. A shift accompanying Treg
   loss leaves depletion/selection plausible. A qualified null limits that
   functional extension; an imprecise or failed-engagement result remains
   unresolved. Do not condition on post-treatment counts and label the residual
   association a direct effect, or infer equivalence from two nonsignificant tests.
4. **Only then test the relevant tumor consequence.** Prespecify treated versus
   distal tumor endpoints separately. Choose a focused effector perturbation
   from the observed/model-supported route; Bockman's CD4/CD8/DC results and
   Zhang's recognition-dependent NK route do not justify an automatic exhaustive
   depletion screen. Retain discordant or unfavorable outcomes. A33–A35 can
   proceed on their own comparisons; their completion is not a prerequisite
   for this separate article-local extension.

This extension is now biologically specified but remains **unexecuted**. The
public sources reviewed here do not provide the joint EZH2 intervention,
viable-lineage recovery and DC functional endpoint with the necessary host
crosswalk. Bockman's data-availability statement names article/supplements or
author request; no raw FCS or host-level linked dataset was recovered. Existing
public evidence resolves the precedent and narrows design, while new compatible
source records or experiments are needed for the intervention estimate.

## Access/search boundary

Actual 12 November routes: DOI/title/PMID lookup; publisher and PMC article
pages; Europe PMC full-text/attachment routes; PMC XML/reader/PDF routes;
read-only Drive searches for `Bockman` and `Intratumoral`; DuPage lab publication
page; Undermind DOI lookup/download; NCBI PMC EFetch. Direct article access
failures were overcome for the main paper. Seven EFetch-listed attachment
requests returned non-PDF responses, recorded locally in `supplement_access.json`.
The author-lab page and Zhang's primary article provided the citation relationship.
No author was contacted, no search certifies novelty, and no claim grade or human
acceptance state changed.

A final bounded discriminator search on 12 November used:

- `EZH2 regulatory T cells dendritic antigen uptake presentation cDC2 2024 2025 2026` (PubMed, PMC, JCI and Nature domains).
- `"Ezh2" "Treg" "dendritic" "antigen" reprogramming uptake` (PubMed, PMC and Cell domains).

These returned the already reviewed DuPage/Peeters/Bockman sources and
non-Treg-targeted EZH2 studies. One recent primary lead was the
[2024 Stat5b/Ezh2 tolerogenic-DC study](https://pubmed.ncbi.nlm.nih.gov/38678673/),
whose indexed abstract describes DC PD-L1 effects; direct PubMed opening did
not expose its body here. It was not treated as a full read, a matched tumor
experiment or a qualified dataset. It reinforces the already stated need to
separate Treg-restricted perturbation from direct DC drug exposure. This bounded
search supplies contrary cell-target context, not novelty clearance or evidence
that no other study has tested the proposed comparison.
