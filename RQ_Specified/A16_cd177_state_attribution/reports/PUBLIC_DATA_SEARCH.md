# A16 public data search, 28 September 2026: a negative result

Recorded because a failed search is a result the register keeps, not a gap to be quietly retried. The
question is whether any public deposit can satisfy the Stage 2 eligibility gate in
[PLAN.md](../PLAN.md) — CD177 measured as protein and used for prospective separation, **and** a
measured outcome on the separated fractions.

## What was queried

Four NCBI GEO DataSets queries were run through E-utilities on 28 September 2026, with the contact
address supplied by the platform. The queries and the accession lists they returned are recorded in
the England session handoff (`handoff/rq_data_search.json`, `handoff/geo_ids.json`).

| Query | Intent | Returned |
|---|---|---|
| `Cd177 AND lung AND Mus musculus AND expression profiling by high throughput sequencing` | any mouse lung deposit indexed on this marker | **2 series**, GSE260762 and GSE155166, both on unrelated subjects |
| `(Itga2 OR CD49b OR CD177) AND (sorted OR FACS) AND lung AND Mus musculus` | sorted surface-marker lung deposits | 25 records, at the retrieval cap |
| `KrasG12D AND lung AND single cell AND Mus musculus` | the oncogenic-initiation literature around the source | 25 records, at the retrieval cap |
| `(clonal OR lineage tracing OR Confetti) AND (alveolar OR AT2) AND lung AND Mus musculus` | clonal alveolar deposits | 25 records, at the retrieval cap |

## Conclusion

**No deposit pairs surface CD177 separation with a proliferation or fate readout in lung.** The
binding gap is the outcome measurement, not the marker: the sorted-marker query returns lung deposits
that sort on other surface proteins, and the two deposits indexed on Cd177 itself are unrelated to
alveolar biology. Condition 1 and condition 2 of the gate are not satisfied together by anything
found, so the hard stop rule applies and no transfer is attempted.

## Partially eligible candidates, for the positional part only

Neither carries a sorted-CD177 arm with an outcome, so neither can address the attribution question.
Both are recorded because they bear on the composition question that Stage 1 addresses internally,
and eligibility has **not** been checked beyond the indexed metadata.

| Series | Samples | Content | Which part it could inform |
|---|---|---|---|
| GSE253461 | 39 | KrasG12D p53−/− Rosa26-YFP AT2 cells, organoids and co-cultures | whether the primed neighbourhood persists under a second oncogenic hit |
| GSE316244 | 4 | early fibrotic niches, KrasG12D AT2 reprogramming, Areg–EGFR | whether the neighbourhood appears outside this source's model |

Two further deposits surfaced in the same searches and are noted without assessment: GSE227719
(KrasG12D;p53 AT2 organoid multiome, 4 samples) and GSE310539 (AP-1-driven AT2 transition multiome,
8 samples).

## Caveat on the search itself

These are keyword searches over indexed metadata, three of them truncated at a 25-record retrieval
cap, so the negative is a statement about what is discoverable this way and not a proof of absence. A
deposit that separated cells on CD177 protein but described it differently, or recorded the outcome in
a supplementary table rather than in its metadata, would not surface. Two routes are stronger than
another keyword pass and are the recommended next actions if the owner retains the question: ask the
source authors directly, since they performed sorted-CD177 organoid and transplantation experiments
whose input fractions were never deposited, and search publication text rather than deposit metadata.
