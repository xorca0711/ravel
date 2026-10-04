# Article-local development branches

All six entries are **proposed and outcome-exposed**, 4 October 2026. They are
registered for navigation and future contract ownership, not as accepted
questions, and none is ranked as preferred. Wp-R01 owns
[source reproduction](REPRODUCTION_SCOPE.md). The existing A0–A27 questions
remain available and unchanged; nothing here allocates a global A identifier.

| Candidate | Question and contribution | Unit and endpoint | Current gate |
|---|---|---|---|
| [Wp-P01](branches/P01_score_construction.md) | Is the pathogenicity ranking a property of the cells or of how the score was built? Measurement validation | Cells within library; score arms and their gene-list sensitivity | Needs Wp-R1; module lists substituted |
| [Wp-P02](branches/P02_serine_one_carbon_direction.md) | Does the 3PG serine arm run with or against the regulatory program? Model discrimination against an independent 2025 result | Cells within library for RNA; the discriminating experiment needs cultures and animals | Needs Wp-R1/R3; direction conflict stated in the literature context |
| [Wp-P03](branches/P03_glucose_composition_vs_state.md) | Is the low-glucose pathogenicity shift composition or within-state change? Decomposition of a published aggregate | Cells within 8 libraries, 2 animals; within-cluster score versus cluster proportion | Needs Wp-R1; two animals cap this at descriptive |
| [Wp-P04](branches/P04_endpoint_class_dependence.md) | Which endpoint class does PGAM inhibition actually move — RNA program, secreted protein, or disease? Endpoint separation | Culture for protein, animal for disease; no deposited values | Blocked for reanalysis; usable as a design constraint |
| [Wp-P05](branches/P05_human_signature_activation.md) | Does the EGCG/N1 signature separate MS from control donors beyond generalised T-cell activation? Transport with a competing explanation | Donor, paired across tissue where available | Needs Wp-R4; signature exposed |
| [Wp-P06](branches/P06_epithelial_transfer_condition.md) | Could a 3PG/2PG-adjacent feature distinguish regulatory competence in alveolar transitional states? Conditional extension | Animal or donor with linked early and later measurements — not available | Conditional; inherits the missing linkage from A1/A8/A14 |

Wp-P01 and Wp-P03 interrogate how the published summaries were constructed,
Wp-P02 and Wp-P04 contrast competing readings of the perturbation, and Wp-P05 and
Wp-P06 are transport questions — one with data, one without. Each card states its
proposition so it can fail, its strongest rival, its unit, its endpoint, the
informative outcomes and its stop condition.

The [literature context](LITERATURE_CONTEXT.md) bounds what any of these can
contribute: PGAM's role in T-cell glycolysis, EGCG's promiscuity, reaction-level
heterogeneity within glycolysis and serine control of regulatory differentiation
are published premises, not discoveries of this package. The one genuinely
unresolved contrast is the *direction* of the serine arm, which is why Wp-P02 is
specified in the most detail.

Relation to the 2021 package: [Wg-P02](../gate2_W1_wagner_th17_autoimmunity/branches/P02_reaction_heterogeneity.md)
asks which opposing reaction associations disappear under pathway aggregation,
and this paper is one worked instance of that question. Wp-P01 therefore cites
Wg-P02 rather than duplicating it, and Wp-P06 is the narrower, data-conditional
successor to Wg-P05's lung bridge.
