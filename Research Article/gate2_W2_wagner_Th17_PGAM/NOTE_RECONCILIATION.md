# Reconcile the owner's notes with the source

Reviewed **4 October 2026**, after the package was first written. The owner's two
Notion pages — **Results(Body)** (fetched 11:23 UTC) and **Discussion** (fetched
08:20 UTC), both children of the paper page under `Acutal_Thesis_Study_Note` —
were read as the owner's reading outline. No Notion page was edited. The primary
PDF controls attribution. This document records clarifications and where each
note-marked question entered the package; it is not an owner acceptance decision
and it does not rewrite the personal notes.

## The owner's own marked questions, and where each one lives

The notes carry four passages the owner emphasised. Each is a question, and each
now has an owner in this package.

| Owner's marked question (verbatim intent) | Where it is now specified |
|---|---|
| Results note, human section: both modules up in MS blood and CSF, "Higher activation level of T helper cells that span across multiple T helper programs … **Verification? And extensions?**" | [Wp-P05](branches/P05_human_signature_activation.md). The note's own reading — generalised activation — is exactly the rival the card puts in the model, so the card was already pointed at this question and now says so |
| Discussion note: "**Further study — connection btw serine biosynthesis, cellular stress(TGF-β), Th17 cell pathogenicity?**" | [Wp-P02](branches/P02_serine_one_carbon_direction.md), **extended because of this note**. The card originally covered only the serine/one-carbon direction; the cellular-stress and TGF-β leg was missing and is now a second, separately qualified arm |
| Discussion note: predominant effect of PGAM inhibition on N1, lowest pathogenicity score, "**A role of PGAM in maintaining a niche pro-regulatory state in Th17n cell?**" | [Wp-P03](branches/P03_glucose_composition_vs_state.md). The card's composition-versus-within-state decomposition is the measurable form of "maintaining": a maintenance claim requires the N1 population to persist, not merely the average score to move |
| Discussion note, closing: reactions in one pathway can modulate immune function in opposing ways, "**May be applied to universal context? other cells, subsets?**" | Split deliberately. The within-pathway opposition question is already owned by [Wg-P02](../gate2_W1_wagner_th17_autoimmunity/branches/P02_reaction_heterogeneity.md) in the 2021 package, and this paper is one worked instance of it; the transfer-to-another-compartment question is [Wp-P06](branches/P06_epithelial_transfer_condition.md), which stays conditional because no dataset meets its requirements |

## Source checks on the notes' content

| Note statement | Check and implication |
|---|---|
| "chemical inhibition of the enzyme that catalyze upstream, the segment itself, the downstream segment — G6PD - PKM - GK, respectively" | The source's mapping is G6PD upstream, **PGAM the segment itself**, PKM downstream, with GK inhibited additionally (main text p. 4). The note's three-way list omits PGAM and shifts the others, so it should not be used as the enzyme-to-position key |
| "inhibitor: DHEA, EGCG, PKM2, DCA" | PKM2 is the target, not the inhibitor; the compound is **shikonin** (STAR Methods p. 15: EGCG 20–50 µM for PGAM, DHEA 50 µM for G6PD, DCA 40 µM for GK, shikonin 10 µM for PKM2) |
| "EGCG signature upregulated in MS, but not CSF" | The source's contrast is MS **blood** versus CSF (Fig. S4C). Keeping "blood" matters because the blood-only result is what makes the tissue comparison in Wp-P05 informative |
| "Th17m" in several places | Reads as Th17n; normalised to the source's Th17n/Th17p in all analysis metadata. An ambiguous group identity is never inferred from a typo |
| Results note: carbon tracing shows a sharp decrease in 2PG "but not in 3PG, PEP" | Retain, with the quantity named: this is **fractional ¹³C labelling** (51% to 7% in 2PG), not pool size and not flux. It supports on-target action at the PGAM step within glycolysis, not pathway-wide specificity |
| Results note: pathogenicity score "based on pre-established module" | Retain. The constraint the notes could not see has since been removed: Table S1 was recovered on 4 October 2026 and supplies the module membership plus the `is_HVG` flags giving the 63 and 30 genes actually scored out of 116 and 68. The score is reproducible from the authors' list. See [Evidence map](EVIDENCE_MAP.md#what-is-not-available) |
| Discussion note: "N1, P1 program straddled btw 2 cond, but mostly belong to high-glucose cond." | Retain as the source's own wording. It is also the reason Wp-P03 exists: a program that is present in both conditions but unevenly distributed moves a condition average through composition alone |
| Discussion note: "2-DG drive glycolysis blockade → Promote Th17 cell effector fn by TGF-β signaling network activation (which PGAM essential for signaling in cancer cells)" | **Two citation checks, abstract level only.** The cited stress study's own abstract states that cell stress supports Th17 differentiation *in the absence of* TGF-β signalling, while the source's sentence describes TGF-β signalling networks being activated; the two characterise TGF-β's role differently. The reference cited for "PGAM is essential for TGF-β signalling in cancer cells" is an allosteric-PGAM1-inhibitor study in non-small-cell lung cancer whose abstract does not mention TGF-β at all. Neither full text was accessed in this pass, so this is not a refutation — it means the TGF-β leg of the chain is an **unverified premise** and must be qualified as one wherever the package uses it |

## Reading card

**Finding** — a reaction-level RNA inference nominated one step inside glycolysis
whose perturbation moves Th17 cells the opposite way from the pathway as a whole,
and the direction was then tested with chemical, genetic, transcriptional and
disease endpoints. **Limitation** — the nominating score is potential activity,
not flux; the two mouse deposits cannot reach population inference; and the
mechanism the Discussion proposes (serine, cellular stress, TGF-β) is a
hypothesis whose TGF-β leg rests on citations that do not support it at abstract
level. **Bridge** — the notes' closing question, whether within-pathway
opposition generalises to other cells and subsets, is a real question, but it is
answered by repeating the reaction-level analysis in a compartment with its own
functional endpoint, not by scoring more datasets.

No branch is preferred, no claim grade is assigned, and no owner retain/reject
decision is recorded here.
