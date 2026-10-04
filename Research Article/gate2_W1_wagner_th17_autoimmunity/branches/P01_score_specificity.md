# Wg-P01: specificity of inferred metabolic state

**Updated precedent boundary (4 October):** eFPA 2025 already compares network
integration with enzyme-only expression, including a Compass comparator with
different implementation/sharing choices. This branch is a Th17-specific
measurement validation; a network-versus-expression comparison alone is not a
new general contribution. The inspected Appendix S1/S4 changes sharing, penalties and normalization;
its exact benchmark transfer still needs a faithful implementation specification. See [comparison and source locators](../PRECEDENT_REVIEW.md).

**Question/decision:** Does the Compass representation retain reaction-level
condition associations beyond simpler expression summaries and measured technical
or activation differences? Decide whether a network feature merits further
biological validation. This is an exposed measurement comparison, not a new
metabolic mechanism.

**Published starting point:** Wagner Fig. 1/2 and STAR Methods; scores combine
gene/reaction relationships with a network and optional transcriptome-wide
neighbor sharing. No local scores have yet been reproduced.

**Hypothesis:** Some qualified reaction associations remain informative beyond
enzyme-expression or pathway summaries. **Strongest rival:** expression depth,
activation/proliferation, batch or neighbor construction explains the apparent
advantage. Shared expression inputs and signatures can induce circular agreement.

**Tuple:** Source-defined sorted Th17n/p cells, original culture context and
collection, condition comparison; biological preparation/animal is the inference
unit, with cells nested. Compare fixed reaction scores with declared matched
expression baselines on the same observations and scale-appropriate metrics.
Use held-out biological blocks only if enough source units and allocation are
verified. All fitted transformations and neighbor graphs must respect any split.

**Discriminator and action:** Consistent incremental information motivates an
independent biochemical test; attenuation supports the simpler/technical rival;
missing independent blocks restricts the result to descriptive sensitivity.
Unsmoothed versus source-smoothed scores assess a specific dependency, not an
automatic correction. Predeclare baselines and avoid post-result score selection.

**Limit/hold:** An RNA signature is not external ground truth, even if its genes
are absent from enzyme mappings. No flux, pathogenic function or out-of-study
transport claim follows. R0/R1 and exact expression/model identification are
required; sample size and useful increment remain unspecified.

[Shared sources and search limits](../LITERATURE_CONTEXT.md).
