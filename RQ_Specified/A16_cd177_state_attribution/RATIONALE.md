# A16 rationale: why marker attribution is its own question

## The proposition, stated so it can fail

Cd177 detection in a transitional alveolar cell carries information about that cell beyond the
information carried by its position in the transcriptional landscape. Stated to fail: hold position
fixed, and Cd177-positive and Cd177-negative cells become indistinguishable on every frozen endpoint,
because Cd177 was a coordinate all along.

Two readings, and both predict the marginal association that motivates the question:

- **Intrinsic.** A priming programme operates in individual cells, Cd177 is part of it or is
  co-regulated with it, and a cell's Cd177 status therefore predicts its behaviour among neighbours
  that look otherwise alike.
- **Positional.** The primed, identity-retaining region of the landscape expresses Cd177, and a
  cell's Cd177 status is a noisy readout of where it sits. Conditional on position it adds nothing.

Neither is a straw man, and the difference is not semantic. Under the intrinsic reading, sorting on
CD177 enriches for a cell property and the marker is a handle. Under the positional reading, sorting
on CD177 enriches for a region and the marker is a coordinate; an experiment that compares sorted
fractions is then comparing neighbourhoods, and any difference it finds is a difference between
regions of the landscape that was already visible without sorting.

## What the England work supports, and exactly how far it goes

The founding numbers are in the [England follow-up](../../Research%20Article/gate2_C2_england_2025/RESULTS_FOLLOWUP.md)
and belong to that package. Three things about them bound this question.

They rest on **one marker measured as RNA in two libraries**. The primary contrast exists only in
GSM7890835 (79 positive against 799 negative) and GSM7890836 (60 against 598); every other library in
the deposit has too few Cd177-positive transitional cells. Two libraries from the same experiment are
not two biological replicates, and no animal identities were deposited.

They are **not depth artefacts**, which is worth stating because it is the first thing to suspect
with a low-detection marker. Seven associations keep their sign under every depth-control method
available in both libraries, and residualisation on log depth and detected genes retains 87 to 159
per cent of each effect. The frozen four-method rule returned "inconclusive" only because 3,000-UMI
thinning drops one library to 26 positive cells, below the pre-set 30-cell floor.

They are **largely compositional**. Within-subcluster conditioning flips Itga2 positive in 5 of 7
testable subclusters and spreads AT2 identity from −0.36 to +1.27. Only priming-associated RNA
persists, in 5 of 7 subclusters. So the honest summary of the founding work is: the CD177 phenotype is
real, is not a depth artefact, and is mostly a statement about where Cd177-positive cells sit — with
one component unexplained by the clustering used.

That unexplained component is the whole of A16, and it is a single residual in a seven-endpoint
family, computed at one clustering resolution, on a module that overlaps neutrophil biology.

## Why RNA co-variation cannot settle it, and what can

The reason this question needs a design rather than another analysis: conditioning on position
reduces the estimate under **both** hypotheses. Under the positional reading it should fall to zero;
under the intrinsic reading it should fall too, because position and an intrinsic programme are
correlated. A smaller number after conditioning is therefore not a verdict, and this is why the
project's architecture rule applies directly — if no possible result of a calculation can distinguish
the stated rivals, stop at feasibility rather than compute it.

What the existing matrices can still decide is narrower and genuinely decisive in one direction. They
can establish that the residual is **not** worth a question: if a typical gene matched to Cd177 on
detection and expression shows the same residual, the persistence is generic; if the residual tracks
a neutrophil and ambient panel, it is contamination; if it inverts across detection thresholds, the
marker cannot support attribution at all. Each of those closes A16 negatively without new data. None
of them can close it positively, which is the asymmetry recorded in the plan.

What would decide it positively is prospective separation: take cells from the **same neighbourhood**,
separate them on CD177 protein, and measure what they then do. That is a wet experiment, and the
prediction is already on record from the founding work — enrichment for primed, identity-retaining
cells and **not** for more cycling ones, since the cycling association is the one endpoint that
disagrees between the two libraries.

## Rivals

1. **Finer-scale composition.** The residual is position, at a scale below the round-2 clusters.
   Addressed by continuous neighbourhood matching and a resolution ladder; if the effect decays
   monotonically with resolution, this rival wins.
2. **Generic gradient behaviour.** Any gene with Cd177's detection profile would show the same
   residual, because a marginal gradient leaves a within-cluster remainder. Addressed by the
   detection-matched gene null; this is the rival most likely to be correct.
3. **Ambient neutrophil RNA.** Cd177 is a neutrophil surface protein, and Lcn2, Lrg1 and Retnla are
   inflammation-associated, so soup from neutrophils co-varies with both. A residual would then have
   no cell state behind it. Addressed by the ambient-origin control. Filtered matrices without empty
   droplets limit this check to within-cell panels, which is a real weakness of the available data.
4. **A detection threshold masquerading as a population.** Cd177 UMIs in positives run 1 to 53 with
   no break, so "positive" is an arbitrary cut on a continuum. Addressed by threshold sensitivity.
5. **Library-specific biology or handling.** The two libraries disagree on cycling; whatever causes
   that could also inflate the priming residual in one of them. Per-library reporting only, never
   pooled.
6. **State-definition dependence.** The transitional gate captures a subset of author-labelled
   transitional cells, and a different gate would sample a different neighbourhood. The gate is
   frozen and not varied; this rival is disclosed rather than tested.
7. **RNA is not protein.** Surface CD177 availability, not transcript detection, is what any sorting
   experiment would act on, and the two need not agree. Unresolvable here.

## Connections and boundaries

- **A8** owns the maturation component and the mature AT1 endpoints. A16 does not ask what the primed
  state matures into.
- **A11** owns lesion-associated programmes against shared plasticity. A16 uses the frozen disjoint
  modules only as endpoints, and adds nothing to that partition.
- **A1** owns the regulatory distinction between RNA-similar transitional states. A16 is narrower: one
  marker, one attribution, and no chromatin or regulatory layer.
- **A4** owns the lineage question. Nothing here traces a cell, and nothing here licenses a direction.
- **A17** owns the clone-dynamics simulation from the same source paper; the two share a package of
  origin and no data or estimand.

The sibling relationship worth naming explicitly: A16 is an attribution question about a marker,
which is the same shape as the enabling source-identity work under A12-S1 — useful because several
questions would otherwise each assume the marker means what it appears to mean.
