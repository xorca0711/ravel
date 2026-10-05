# Wp-P04 — Which endpoint class does PGAM inhibition actually move?

**Status:** proposed; **blocked for reanalysis** because no numeric values are
deposited for the protein and disease panels. Retained as an endpoint-separation
constraint on every other card and on any future experiment.

## Why the card exists

The paper's claim chain crosses four measurement classes, and the evidence is not
uniform across them:

| Class | What was observed |
|---|---|
| RNA program | EGCG raises the pathogenic and lowers the Th17n program in bulk; the EGCG signature correlates with the pathogenicity score at rho 0.79 |
| Intracellular cytokine frequency | IL-17 and IL-2 positive fractions rise in division-1 cells |
| Secreted protein | Legendplex panels show EGCG-treated cells "retained their cytokine profile with a few exceptions"; MOG-recall secretion after transfer rises for IL-17, IL-17F, IL-22 and IL-6 but not IL-10, IL-21, TNF-α or IFN-γ |
| Disease | Th17n+EGCG transfer induces EAE (10 of 12 versus 0 of 12), and severity rises further only when IL-23 is added |

A program shift, a frequency shift, a selective secretion change and a disease
outcome are different claims. The paper's own data show the classes do not move
together: the broad secretion panel is largely unchanged in vitro while the RNA
program moves clearly, and the disease effect needed IL-23 co-stimulation to
become severe.

## Proposition, stated so it can fail

PGAM inhibition moves the RNA program and a restricted set of cytokines, not
effector output as a class. If a complete, unit-resolved protein panel showed
coordinated increases across the secreted cytokines, this proposition fails and
"PGAM restrains effector output" is the better description.

## Strongest rival

Assay sensitivity. Supernatant concentrations after fixed culture time integrate
secretion, consumption and cell number; a real coordinated increase can be
flattened by normalisation to culture or by division differences. The paper
controlled for arrested cells by gating on division 1 for frequencies, but the
secretion panels are per culture.

## What would distinguish them

Not reanalysis: the numbers are not deposited. A future experiment would measure,
in the same cultures and with the mouse as unit, (a) per-cell cytokine protein by
intracellular staining with division tracking, (b) secretion per viable cell over
a defined window rather than per well, and (c) the RNA program, so the three
classes are comparable on one set of units. Reporting each class separately — and
refusing to let the RNA program stand in for protein or disease — is the
contribution.

## Decision this would inform

Which readout a PGAM-directed intervention should be judged on, and what
"pathogenicity" means operationally when the RNA program and the secreted panel
disagree. This also constrains how [Wp-P02](P02_serine_one_carbon_direction.md)'s
proposed experiment is read: a Foxp3 or IL-17 protein endpoint is the decisive
one there, precisely because the RNA program is already known to move.

## Unit, endpoint, limit

Unit: culture for protein, animal for disease. Endpoint: class-specific effect
with its own unit and denominator. Limit: this card cannot be advanced with
deposited data at all; recording it as blocked is its current function, and
substituting an RNA program for the missing protein endpoint is the specific
error it exists to prevent.

## Stop condition

Remains blocked unless the lead contact supplies source values for Figures 1C–1G,
4 and S5, or the owner authorises a separately labelled digitisation with stated
extraction uncertainty. A digitised series is never described as raw data and
never enters a claim as a measurement.

## Status check, 5 October 2026

The stop condition names two routes out: source values from the lead contact, or
an owner-authorised digitisation. The owner judged author contact implausible on
4 October 2026 and declined digitisation, which closed Wp-R5. **This card is
therefore blocked permanently for reanalysis, not pending**, and its function is
now entirely the endpoint-separation constraint it places on the other cards.

That constraint earned its keep twice in the executed work. [Wp-R3](../R3_RESULTS.md)
found the RNA module shift under EGCG in Th17n non-selective once the global
shift is centred out, while the single cytokine transcripts moved as published —
a disagreement *within* the RNA class that would have been invisible if the
module score had been allowed to stand for effector output. And
[Wp-R4](../R4_RESULTS.md) found the human module separation non-specific against
matched random gene sets. Both are instances of this card's rule: an RNA
programme is not a protein endpoint and not a disease endpoint.
