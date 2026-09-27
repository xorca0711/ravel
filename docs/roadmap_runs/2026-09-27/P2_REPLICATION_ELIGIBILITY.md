# P2 — Independent replication eligibility

**Status: bounded eligibility work completed; replication stopped at its unit gate.** No new expression matrix was downloaded and no module score was calculated. This is a data/design result, not a negative biological replication.

The primary candidate was Choi's independent bleomycin lineage study; the fallback was Riemondy's adult LPS-injury study. Both are biologically relevant to an alveolar transitional-state contrast. Selection did not use candidate module scores.

| Candidate | Unit evidence | Decision |
|---|---|---|
| Choi, GSE145031 | Six submitted samples; the only day-14 Tomato-positive sample is a pool. Methods specify two mice per pool. Day-28 samples fall outside the inherited day 2–21 window. The negative-lineage sort does not add independent mice. | No resolved individual-mouse contrasts for the unchanged instrument; ineligible. |
| Riemondy, GSE113049 | Ten submitted libraries overall. The four injured libraries are two experimental injured-mouse labels, each with two explicitly technical replicates. | At most two injured biological samples, below the inherited three-mouse eligibility floor. |

Sources: [Choi methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC7487779/), [Choi deposited metadata](GSE145031_sample_metadata.json), and [Riemondy deposited metadata](GSE113049_sample_metadata.json). This repository has previously inspected Choi data: source independence from Strunz is not an untouched-source claim. The [eligibility record](P2_eligibility.json) retains metadata hashes and unperformed downstream checks.

## Precision is a separate requirement

Even a future candidate with three mice would only pass the sample floor. Under the inherited t-interval model, the anticipated half-width is the multiplier below times the between-mouse standard deviation. These are sensitivity calculations, not a power calculation or a biological effect margin.

| Independent mice | 95% interval half-width / between-mouse SD |
|---|---:|
| 3 | 2.484 |
| 6 | 1.049 |
| 12 | 0.635 |
| 24 | 0.422 |
| 40 | 0.320 |

## Work pruned and next action

Do not lower the floor, use technical libraries/cells as mice, extend the day window after seeing scores, or substitute a pooled-sample estimand while calling it unchanged replication. Coverage, depth and annotation calculations cannot repair the failed unit gate, so they were not run.

T3 remains not launched. A separate expanded search could seek at least three individually identified injured mice with raw counts and comparable paired states, then justify precision beyond the floor. The present bounded search does not establish that no eligible public study exists. It deliberately ends after the named primary and fallback.

A11 still needs comparable epithelial states across non-neoplastic injury, tumour and normal tissue; these candidates do not supply that design. A0's failed pilot remains stopped. No independent conservation branch was established here.

Verification: sample counts and biological-versus-technical grouping were independently computed from the deposited SOFT metadata. No existing A5 module, endpoint, threshold or result was changed.
