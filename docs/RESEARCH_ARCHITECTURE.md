# Research architecture and interpretation authority

**Latest authority:** the [follow-through](roadmap_runs/2026-09-27-followthrough/README.md) records new exploratory A12/A13 results and source-based candidate corrections. Historical run hashes remain snapshots; living-context changes do not rewrite earlier measurements.

The [roadmap execution record](roadmap_runs/2026-09-27/README.md) supplies the latest P1 source facts and P4 accounting evidence. Completed feasibility work does not imply its biological gate has passed.

Updated 27 September 2026 after the [A0–A15 rationale audit](audits/2026-09-27-rq-rationale/REPORT.md).

The purpose is to generate and discriminate biological hypotheses about lung
repair and remodelling from public data. The organizing question is not yet an
answer: no common measured repair outcome links all these cohorts. A0 extends
the lung programme into a bounded cross-tissue test; it does not redefine the
whole project as a search for one universal signature.

## One evidence chain, with question-specific designs

```mermaid
flowchart LR
    S[Source and biological units] --> M[Defined measurement and comparator]
    M --> E[Estimate and relevant rival checks]
    E --> D[Question-specific decision]
    D --> O[Independent outcome or perturbation test]
```

The stages are not interchangeable. A passed arithmetic check validates the
calculation. A repeated expression direction supports an association. Neither
automatically validates a regulatory mechanism, lineage route or repair outcome.
One study can inform several questions, but reuse never adds independent evidence.

| Layer | Authoritative location | Required distinction |
|---|---|---|
| Purpose and biological hypotheses | `RESEARCH_QUESTIONS.md` | Motivation, actual measurement, rival, decision and missing design |
| Paper-specific evidence | `Research Article/` | Source result versus repository reanalysis; reading order versus execution order |
| Question-specific work | `RQ_Specified/` | Metadata gate, dated specification, implementation, units, outputs and current interpretation |
| Shared definitions and measurement controls | `analysis/`, `docs/RQ_MEASUREMENT_CONTRACTS.md` | Common provenance without a common assumed biological scale |
| Historical graded claims | `CLAIMS.md`, generated manifest/summary | C1–C168 do not exhaust newer question-level results; grades require their own decision |
| Current state and amendments | RQ README, `PROGRESS.md`, `AI_CONTEXT.md` | Latest dated interpretation overrides a stale execution queue, not historical numbers |
| Historical protocols and run records | Frozen configs, reports, hashes and archives | Preserve original bytes; record corrections and exposure rather than retroactively changing a freeze |

The [current audit](audits/2026-09-27-rq-rationale/REPORT.md) and its A2/A15 addenda
govern the corrected interpretations described there. Historical labels such as
`weak bound` and `null` remain in frozen run records and are not current evidence
grades. A15 registration remains pending; this audit does not impersonate owner review.

## Rules shared by every question

1. Declare the unit, population, comparator and endpoint before deciding which
   analysis can answer the question. Sample identity, pairing, nested fields,
   pooled animals and repeated libraries must be explicit. A numerical sample
   floor is eligibility, not power, exchangeability or verified independence.
2. Separate what a method measures: RNA from protein activity, accessibility
   from direct histone marks, enrichment from purity, composition from within-cell
   change, and cross-sectional association from fate or mediation.
3. Preserve both selection and exposure history. A new freeze on previously
   inspected data is an amendment, not untouched external confirmation. A0's
   two pilots reuse repair and intestinal sources with different instruments.
4. Keep primary, sensitivity and post hoc analyses distinct. A smaller p-value,
   a lower depth budget, another label, or another gene set cannot repair an
   unidentifiable design. A stopped pilot can be complete while its biological
   hypothesis remains unresolved.
5. Use biological-unit uncertainty for population claims. Positive nonsignificant
   estimates do not establish absence. Equivalence needs a stated useful-effect
   margin and suitable precision. Cell draws and gene-set controls answer other
   questions. A threshold crossing is not a causal decomposition of confounding.
6. Define gene membership, source universe and score scale. Shared or list-exclusive
   genes do not prove shared or exclusive biology. Rank, detection, logCPM and
   standardized-score differences must not be compared as the same effect scale.
7. Require a discriminating design for mechanism. Delivery and abundance can both
   matter; perturbations of source, receiver and ligand are not interchangeable.
   Spatial RNA can support proximity associations but cannot alone measure ligand
   processing or transmission. A downstream response is not strict target engagement.
8. Record failed gates and negative results in the question index even when no
   graded claim exists. Never change a graded row merely to put a trial in the
   generated negative-results page. Historical report generators may overwrite
   files: replay them only in a separate output copy, keeping originals intact.

## Decision-driven continuation

For each new run write one sentence specifying what result would change which
decision. Prefer recovering a missing preparation map, comparable state definition
or linked endpoint over adding another correlated score. If no possible result of
the proposed calculation can distinguish the stated rivals, stop at feasibility.

The open critical gaps are in the [audit](audits/2026-09-27-rq-rationale/REPORT.md#critical-logical-gaps-still-open).
The [research roadmap](RESEARCH_ROADMAP.md) develops them into six work packages,
biological rationales, data requirements and explicit proceed/stop decisions.
This is guidance for future specifications, not a new analysis authorization or
an instruction to repeat completed fits.
