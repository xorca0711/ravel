# DuPage-first exploratory target screen, version 1

7 November 2026. Owner-requested follow-up to the completed S0–S6 reconstruction,
under article-local Dp1-P01. The owner explicitly released the screen from the
Zhang 2026 tumor/NK direction. This is a new exploratory selection, not a replay
or a change to the frozen S0–S3 analyses. No canonical question is adopted here.

## Biological purpose and comparison

Which specific Ezh2-associated RNA changes offer a tractable explanation for
failure of activated Tregs to retain identity, survive, or perform their
suppressive function? Start with the original spleen/LN Tregs, not a tumor
requirement. The screen measures conditional KO–HET differences in the observed
CD62L-low state and their difference from CD62L-high. Source preparations remain
the units; mouse/pool identity, pairing and independence are unknown.

The current reconstruction found mixed state dependence and weak external
chromatin consistency, not a validated target. Large RNA changes may reflect
within-cell regulation, different activation states, selective survival, or
technical variation. These explanations can coexist. The screen can organize
specific RNA observations; protein, direct Ezh2 regulation and causal function
remain separate questions. See [current results](RESULTS.md) and
[literature context](LITERATURE_CONTEXT.md).

## Frozen selection rule

Reuse all 11,614 S1-eligible loci and the same 11 retained libraries. Use
log2(FPKM + 1), with means after transformation. Preserve all four group means,
both genotype contrasts and the state interaction I = low contrast − high
contrast. Recalculate only the additional sensitivity quantities needed here;
reconcile primary contrasts and interaction with the frozen S1/S2 tables.

For each gene, retain primary estimates, every one-library omission and the
two existing pseudocount alternatives (0.5 and 2, full sample). These are
separate sensitivity configurations, not a crossed sensitivity design. Record
the smallest sign-oriented estimate across configurations for the low contrast
and I. These minima are descriptive sensitivity bounds, not confidence limits.

Two discovery tracks, each with positive and negative directions:

1. **Low-state genotype track:** the low contrast has the same nonzero sign in
   every configuration. Order by its sign-oriented minimum, descending, then
   gene symbol. This permits changes shared with the high state.
2. **State-prioritized track:** both low contrast and I retain their signs in
   every configuration, those signs agree, and the primary absolute low contrast
   exceeds the absolute high contrast. Order by the sign-oriented minimum of I,
   then that of the low contrast, descending, then symbol. This is a screening
   preference, not proof of activation-specific regulation.

Retain all genes, including failures, in the complete table. Display the first
10 genes in each signed track (at most 40 distinct genes) for bounded biological
triage. Ten is a reading-budget cutoff, not a meaningful-effect threshold.
Report track membership, overlap and omitted candidates transparently. Do not
convert this ordering into a target-validity score or use p-values/FDR.

Separately display the original paper's named examples Pde3b, Tcf7 and Lef1,
and endpoint/context anchors Ezh2, Foxp3, Il10, Ctla4, Il2, Il2ra, Tgfb1,
Bcl2, Bcl2l11, Bach2, Klf2, Prdm1, Irf4, Ccr7, S1pr1 and Areg. These named
anchors cannot enter the discovery set merely because they are familiar.
Missing or ineligible anchors must remain explicit. Chromatin coverage from S3
is an annotation, not an eligibility rule; uncovered does not mean unmarked.

## Literature triage and informative outcomes

After the frozen run, inspect the complete displayed union. Record which
candidates merit a focused primary-source read and why; retain contrary and
unresolved entries rather than silently dropping them. Use current primary
literature, closest older perturbations and contradictory/context-dependent
findings to separate already-tested biology from a useful unresolved comparison.
No claim of novelty follows from absent search hits. A selected candidate needs
a measured RNA observation, a plausible functional role with an exact source
locator, a competing explanation, and an experiment that can change the decision.

Possible outcomes: a tractable candidate motivates protein/function validation;
a familiar mechanism becomes a comparator rather than a discovery; activation
markers or immunoglobulin/lineage-mixture signals motivate qualification rather
than a causal Treg claim; fragile or unsupported candidates stay unresolved.
Do not add datasets merely to produce a favorable result. A new independent
dataset would require its own source qualification and contract.

## Exposure and limits

S0–S3 outcomes and original DuPage conclusions were already read. Before this
freeze, Zhang 2026 and Wang 2018 suggested Il2/Ctla4-centered alternatives;
existing rows for Il2, Ctla4, Il2ra, Il10 and Tgfb1 were viewed. The owner then
requested a DuPage-first screen. Their prior viewing is disclosed, not erased.
DuPage's Discussion names Pde3b, Tcf7 and Lef1; the search already found a 2024
TCF7/LEF1 tumor-Treg paper and the existing EZH2 gain/KDM6B context. No new
screening ranks or sensitivity minima were calculated before freezing.

All follow-up hypotheses remain exposed and exploratory. Sample size, meaningful
effect margin, reagents, model access and laboratory feasibility are unknown.
The hypothesis-generation skill supports competing explanations and falsifiable
predictions; it does not supply missing experimental evidence or require a
mechanism to be invented for this descriptive screen.
