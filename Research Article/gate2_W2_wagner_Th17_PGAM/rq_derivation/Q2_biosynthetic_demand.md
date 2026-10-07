# Wp-Q2 — Does PGAM restriction raise Th17 effector output through phosphoenolpyruvate, through relieved biosynthetic demand, or through stress?

**Historical derivation:** the [7 October correction report](../CORRECTIONS_2026-10-07.md) and current A28–A30 dossiers supersede affected Compass/human values and inference wording below. Retain this record of what was known when the questions were proposed.

**Wp-Q2 · Proposed biological question · Outcome-exposed.**
[Derivation index](README.md) · [Overlap](OVERLAP_MATRIX.md) ·
[Grounding](SOURCES_AND_GROUNDING.md).

## Observation → gap → question

The source's Discussion proposes that PGAM inhibition raises Th17 pathogenicity
through cellular stress, citing a glycolysis-blockade study and a cancer study
of PGAM1 in TGF-β signalling. [Wp-P02](../branches/P02_serine_one_carbon_direction.md)
read both: the first reports that cellular stress **substitutes for** TGF-β
rather than activating it, with sustained cytoplasmic calcium and a partial
XBP1 contribution as the mechanism; the second is paywalled and its abstract
does not mention TGF-β.

[Wp-E3](../E3_RESULTS.md) then measured what the authors' own bulk libraries do
under EGCG in Th17n, against a null matched on expression decile — the
construction that absorbs the TPM compositional confound:

| Programme | Centred median | Null p |
|---|---|---|
| Th17 effector | **+0.544** | 0.000 |
| Integrated stress response | **−0.491** | 0.000 |
| Histones | −0.465 | 0.000 |
| Serine / one-carbon | −0.299 | 0.001 |
| Cell cycle | −0.260 | 0.000 |
| Ribosomal proteins | −0.205 | 0.000 |
| UPR (incl. *XBP1*), NRF2, heat shock, glycolysis, OXPHOS, hypoxia | not distinguishable from null | 0.06 to 0.90 |

Th17n + EGCG is the **only** one of the four drug-by-cell-type arms in which
the effector programme rises; in the other three it falls by 0.73 to 1.18. A
[frozen sensitivity](../../../analysis/research/runs/wp_e3_isr_sensitivity_v1/results.json)
established that the stress result is not an artefact of the two genes shared
with the serine set (*MTHFD2*, *SHMT2*): removing them leaves the ISR shift at
−0.491, unchanged to four decimals. At gene level, ATF4 *output* falls — *CHAC1*
−2.03, *TRIB3* −1.75, *NUPR1* −1.28, *DDIT3* −1.11, *ASNS* −0.87 — while *ATF4*
itself does not move (−0.19, adjusted p 0.77) and *SESN2* rises (+1.53,
adjusted p 0.0004).

So the effector gain co-occurs with a coordinated **fall in biosynthetic and
proliferative programmes** and with reduced ATF4 output, and with no movement in
any other stress axis measured. The gap: co-occurrence in five bulk libraries
per arm is not a mechanism, and nothing here measures stress-response activity
or protein.

### A third explanation the literature supplies, and the source's own data constrain

A 5 October 2026 search (see [LITERATURE_UPDATE.md](LITERATURE_UPDATE.md))
found a mechanism neither the source's Discussion nor this package had
considered.
[Ishikawa and colleagues 2023](https://doi.org/10.1016/j.celrep.2023.112205)
(PMID 36857180) identify **phosphoenolpyruvate (PEP)** — two steps downstream of
PGAM's substrate — as a *negative* regulator of Th17 differentiation: PEP
supplementation, or inhibition of enzymes downstream of PEP, raises intracellular
PEP and suppresses IL-17A; PEP binds JunB and blocks DNA binding of the
JunB/BATF/IRF4 complex; and the effect is reported without significant change to
glycolysis, proliferation or survival.

This supplies the most parsimonious reading of the source's own phenotype.
PGAM converts 3PG to 2PG, the immediate precursor of PEP. Inhibiting PGAM should
*lower* PEP, release JunB/BATF/IRF4, and raise IL-17 — with no stress response
and no appeal to serine. It also predicts the effector-programme rise that
[Wp-E3](../E3_RESULTS.md) measured, and it is the only candidate mechanism that
predicts both the cytokine phenotype and the transcriptional one.

**The source's own data argue against it as stated, and this is the point of
the question.** The paper's ¹³C tracing (Fig. 1E) reports that EGCG collapses
labelled 2PG from 51% to 7% while **3PG and PEP are not significantly changed**,
and no other glycolytic metabolite moved. If PEP is genuinely unchanged under
PGAM inhibition, the PEP-JunB route cannot be the explanation. But that
measurement is a 15-minute label ratio, not a pool size, in one condition — and
a labelling ratio can hold steady while the absolute pool falls. The source
cites the PEP paper as its reference 7, but only inside the Introduction's
opening citation bundle for "glycolysis is central to Th17 differentiation";
the Discussion proposes stress and serine and never returns to it, although
3PG-to-PEP is precisely the segment its Compass analysis singles out.

**Question.** Does restriction of glycolysis at PGAM raise Th17 effector output
by lowering phosphoenolpyruvate and relieving PEP-mediated inhibition of the
JunB/BATF/IRF4 complex, by relieving biosynthetic and proliferative demand, or
by inducing a stress response?

## Hypothesis and biology

**Primary (metabolite-signalling).** PGAM restriction lowers the intracellular
PEP pool; PEP-mediated inhibition of the JunB/BATF/IRF4 complex is relieved; the
Th17 effector programme is transcribed more. This is a signalling mechanism
through a metabolite, not an energetic or stress one, and it predicts the
transcriptional observation directly: the effector programme should rise and
nothing else needs to move, which is close to what Wp-E3 found. The prediction
is directional and falsifiable — measure the **PEP pool size** (not the label
ratio) under PGAM inhibition; it must fall. PEP supplementation should then
abolish the EGCG-driven IL-17 increase.

**Secondary (demand relief).** Effector output and biosynthetic growth compete
for the same cell. When PGAM restriction slows ribosome and histone production,
nucleotide and one-carbon demand, the resources and transcriptional bandwidth
that growth consumed become available to the effector programme; no stress
sensor and no metabolite signal are needed. Prediction: a perturbation that
slows proliferation and biosynthesis **without touching PGAM** — mitotic arrest,
mTORC1 inhibition, serine or methionine restriction — reproduces the effector
gain.

The two are separable in one experiment, because PEP supplementation rescues
the first and not the second, and matched growth slowing reproduces the second
and not the first.

A prediction common to both, and negative: on the PGAM arm itself,
phospho-eIF2α and ATF4 protein should **not** rise under EGCG in Th17n. This is
the readout [Wp-P02 now carries](../branches/P02_serine_one_carbon_direction.md)
on an experiment it already specifies.

## Strongest rivals

0. **PEP is genuinely unchanged.** The source's own ¹³C tracing reports no
   significant change in labelled PEP under EGCG, which if it reflects the pool
   would eliminate the primary hypothesis outright. This is the first thing the
   experiment must settle, and it is settled by a pool measurement rather than
   a label ratio. Reported as a rival rather than folded into the design,
   because it is published data from the authors themselves pointing the other
   way.
1. **ISR-independent stress.** The cited stress mechanism is sustained
   cytoplasmic calcium with partial XBP1, which a transcript module does not
   see. Wp-E3 found the UPR set, which contains *XBP1*, flat — but flat
   transcripts do not exclude a calcium-driven response. This rival needs a
   calcium and phospho-protein readout, not another gene list.
2. **Compositional artefact in a different form.** TPM renormalisation produces
   a global shift that Wp-E3's expression-matched null absorbs; it cannot
   exclude a genuine global response that is itself expression-dependent. Cells
   with fewer ribosomal and histone transcripts have more of the total for
   everything else, so the effector "gain" may be a per-cell-RNA-content effect
   rather than increased output per cell.
3. **Division-rate dilution.** Fewer divisions means less dilution of
   accumulated cytokine transcript. [Wp-M1](../METADATA_PHENOTYPES_RESULTS.md)
   found that both inhibitors restructure the first-division-versus-bulk
   signature rather than remove it, so the gate does not control this.
4. **Drug off-target.** EGCG is a promiscuous polyphenol. [Wp-R2](../R2_RESULTS.md)
   found the forward PGAM reaction at rho −0.291, rank 11 of 83 and failing BH,
   well short of lactate dehydrogenase at −0.52, so the reaction-level evidence
   does not single PGAM out either. Genetic PGAM1 loss is the control this
   rival requires.

## Unit, contrast and endpoint

Mouse. The bulk deposit has no animal field, so every Wp-E3 value is
library-level and descriptive; this question cannot be advanced on it.

The design is a **culture experiment in Th17n with three factors**, each
present because it separates two of the candidate mechanisms:

1. PGAM restriction — EGCG, with genetic *Pgam1* reduction as the specificity
   control for the promiscuity of the inhibitor.
2. PEP rescue — PEP supplementation on the PGAM-inhibited arm.
3. A growth-slowing perturbation that does not touch PGAM.

Readouts: **PEP, 2PG and 3PG pool sizes by targeted metabolomics** (absolute,
not label ratio), IL-17A protein per cell, a division tracker, phospho-eIF2α
and ATF4 protein, and total RNA or ribosome content per cell so the
compositional rival is measured rather than argued about. Mouse is the unit.

The pool measurement is the step that distinguishes this from re-reading the
source: the published ¹³C ratio cannot tell a steady pool from a falling one,
and every candidate mechanism here turns on which it is.

A ¹³C arm is already specified on [Wp-P02](../branches/P02_serine_one_carbon_direction.md)
for the serine question and would share these cultures; adding PEP to the
targeted panel is close to free once the cultures exist.

## Informative outcomes

| Outcome | Interpretation and action |
|---|---|
| PEP pool falls under PGAM inhibition, and PEP supplementation abolishes the IL-17 increase | Supports the metabolite-signalling route; the source's stress premise is unnecessary and the 2023 PEP mechanism explains its phenotype |
| PEP pool is genuinely unchanged | The primary hypothesis is eliminated on the authors' own measurement extended to pools; demand relief and the serine route remain |
| Growth slowing without PGAM inhibition reproduces the effector gain; p-eIF2α/ATF4 flat | Supports demand relief; the stress premise should be withdrawn as a mechanism |
| Effector gain requires PGAM specifically, survives PEP rescue, and is absent under matched growth slowing | A PGAM-specific route exists that is none of the three; the serine and 2PG branches become the live alternatives |
| p-eIF2α/ATF4 protein rise under EGCG despite falling target transcripts | Transcript modules mis-read the response; Wp-E3's conclusion is limited to transcript level and the stress premise survives at protein level |
| Effector gain disappears when per-cell RNA content is accounted for | Compositional; the Wp-E3 effector result does not support increased output per cell |
| Calcium readout positive with ISR flat | The cited calcium mechanism holds and is invisible to transcript modules; the question is reframed rather than answered |

## Contribution and readiness

Contribution description: **model discrimination between three published or
published-adjacent mechanisms**, none of them proposed here as new. That
glycolytic inhibition can enhance Th17 polarisation is established
(Brucklacher-Waldert 2017); that PEP suppresses the Th17 programme through
JunB/BATF/IRF4 is established (Ishikawa and colleagues 2023); that biosynthetic
demand competes with effector output in T cells is a general premise. The
unresolved point is **which of them produces this paper's phenotype**. The
source's Discussion names only the mechanism its own libraries move against,
and cites the PEP work as Introduction background (reference 7) without
evaluating it against its own result.

The card's framing changed on 5 October 2026 after the literature search, from
a two-way demand-versus-stress question to this three-way one. The prior
framing and the reason are preserved above rather than overwritten. Nothing
here claims a novel mechanism, and a transcript
result cannot establish one.

Readiness: specified, **not executable in this package**. It needs culture work,
protein and per-cell content readouts, and animal-level replication. No effect
margin is nominated.
