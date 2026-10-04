# Wp-P06 — Conditional: a 3PG/2PG-adjacent feature in alveolar transitional states

**Status:** proposed and **conditional**. No eligible dataset exists; this card
exists to state the conditions under which the transfer would become a question,
and to prevent an unqualified metabolic score from being imported into the lung
questions.

**Owner's framing, 4 October 2026.** The Discussion note closes by asking whether
within-pathway opposition "may be applied to universal context? other cells,
subsets?" That question splits in two, and only the second half belongs here: the
*general* claim that reactions in one pathway can act in opposing directions is
already owned by [Wg-P02](../../gate2_W1_wagner_th17_autoimmunity/branches/P02_reaction_heterogeneity.md),
for which this paper is a worked instance; the *transfer to a specific other
compartment* is this card, and it stays conditional. Generalisation is earned by
repeating the reaction-level analysis in a compartment that has its own
functional endpoint, not by scoring more datasets.

## The tempting inference, and why it is not yet a question

This paper shows that one reaction inside glycolysis can run against the
pathway's overall association with an effector program, and that perturbing it
shifts cells out of a regulatory state. The project's lung questions ask what
keeps alveolar epithelial cells in, or lets them leave, transitional states. The
tempting move is to score a 3PG/2PG-adjacent feature in AT2-to-AT1 transitional
cells and call it regulatory competence.

That move fails on three counts, all of them recorded elsewhere in this
repository rather than new:

1. **No linked early and later measurement.** Across the A1 evidence branches, no
   dataset carries an early regulatory measurement and a later independent
   maturation outcome in the same biological units. A metabolic feature inherits
   that gap; it does not close it.
2. **Compartment mismatch.** Th17n cells are a clonal in-vitro culture under
   defined cytokines at 25 mM or 1 mM glucose. Alveolar epithelium sits in a
   niche with unknown local glucose, lactate and serine availability. A reaction
   association fitted in one does not transfer to the other by name.
3. **Score status.** Compass potential activity is not flux, and the one stage of
   this package that would produce such scores (Wp-R2) is blocked on a solver
   licence. Importing an unqualified score into a lung question would add a
   number without adding evidence.

## What would make it a question

All four of these, stated in advance:

- A dataset where the same animals or donors supply an **early** epithelial
  measurement and a **later independently measured** mature outcome — the
  requirement already recorded for A1, A8 and A14.
- A metabolic feature defined on something other than the RNA being used as the
  predictor — stable-isotope labelling, extracellular flux, or a protein-level
  enzyme measurement — so the feature and the outcome are not two summaries of
  one transcriptome.
- Evidence that the serine/one-carbon axis is operative in the epithelial
  compartment at all, which is testable cheaply in existing alveolar data as a
  precondition rather than as a result.
- A direction resolved by [Wp-P02](P02_serine_one_carbon_direction.md). Until the
  3PG arm's direction is settled in the compartment where it was proposed, a
  transfer would import an unresolved sign.

## Unit, endpoint, limit

Unit: animal or donor with linked early and later measurements — not currently
available in any deposit this project holds. Endpoint: incremental prediction of
an independently measured mature outcome beyond current RNA state. Limit: the
only legitimate output of this card today is the condition list above. CNS
autoimmunity after Th17 transfer is not lung repair, and a cross-tissue analogy
is not a shared mechanism.

## Stop condition

This card stays closed until its four conditions are met. It must not be opened
by relabelling an existing lung analysis as metabolic, and it does not justify
running Compass on lung data to see what appears.

**Repository connection:** this is the narrower successor to
[Wg-P05](../../gate2_W1_wagner_th17_autoimmunity/branches/P05_lung_regulatory_competence.md),
which proposed the same bridge from the 2021 paper and is held for the same
missing linkage. Keeping one conditional card per package, cross-referenced,
avoids two questions that would need the same unavailable dataset.
