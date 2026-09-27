# A13: fibroblast programmes beyond macrophage interleukin-1 beta

**Latest follow-through:** [A13 results and candidate decisions](../../docs/roadmap_runs/2026-09-27-followthrough/A13_PILOT_AND_COVERAGE.md). Historical specifications and numerical results below are preserved; read the dated follow-through for the current execution state.

**Scope clarification, 27 September 2026:** the [rationale audit](../../docs/audits/2026-09-27-rq-rationale/REPORT.md)
retains the zero/three-pair coverage result and no-fit decision. The recorded
fibroblast bottleneck applies to the inspected cohorts; it does not prove that
a larger or differently sampled cohort cannot supply complete triads. Comparable
states, protocol, depth and actual per-patient counts govern a new eligibility audit.

**Status, 27 September 2026: coverage counted, the gate is not met, nothing fitted.** The
register card for [A13](../../RESEARCH_QUESTIONS.md#a13) says coverage is next and not
mediation fitting. This folder is that coverage and nothing more. No model was fitted, no
association was estimated, and no claim row was added.

Read the [coverage results](reports/COVERAGE_RESULTS.md). The frozen decisions are in
[`config/a13_triad_coverage_spec.json`](config/a13_triad_coverage_spec.json), committed before
any count existed.

## What the gate asked, and the answer

A joint model needs at least ten patients holding a complete macrophage, fibroblast and
epithelial triad. The card recorded six and three such donors in the two IPF cohorts and
warned that 23 human cohort patients does not mean 23 complete paired triads.

The only cohort on disk that had never been counted is the Kim lung adenocarcinoma deposit.
It gives **zero** complete paired triads at the 50-cell floor under the epithelial definition
the two IPF cohorts used, and **three** under a wider one. Both are far below ten.

**The zero is definitional.** Every one of the eleven tumour samples holds exactly zero cells
labelled type 2, because the deposit annotates tumour-sample epithelium as tumour states
instead. A paired tumour-versus-normal contrast and a type 2 epithelial compartment are
therefore incompatible in this deposit at any cohort size.

**Under the wider definition, fibroblast capture binds**, with the largest fibroblast label
reaching 50 cells in ten of twenty-two samples and a median of 32.5. That constraint is a
property of the assay rather than of the cohort, so a larger deposit does not open the gate by
itself.

## Two things a later session should know

1. **The earlier triad rule was label-level, and it was not written down.** A compartment met
   the floor when one single cell label reached it, not when its labels summed to it. The first
   run here assumed pooling, reproduced 230 of 240 prior flags, and refused at its own check.
   The rule was recovered from the disagreement pattern and now reproduces all 240. Any future
   count must use it, or its numbers will not be comparable with the six and three the card
   quotes.
2. **Do not fit anything on this coverage.** Three patients cannot support a joint model, and
   the card already warns that a met floor would not be a power guarantee either.

## Layout

| Path | Contents |
|---|---|
| `config/a13_triad_coverage_spec.json` | floors, compartment labels per cohort, the reproduction requirement, the declared reading |
| `scripts/01_count_triads.py` | standard library only, hash-verified inputs, refuses to overwrite, and refuses to report new counts if the reproduction check fails |
| `tables/` | per-unit counts, the reproduction check, the run record, and the refused first attempt |
| `reports/` | [coverage results](reports/COVERAGE_RESULTS.md) |
