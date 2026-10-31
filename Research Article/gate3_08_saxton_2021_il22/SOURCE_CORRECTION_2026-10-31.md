# Documentary correction to the Saxton source audit

31 October 2026. This note supersedes the **panel-location and endpoint entries**
identified below in [SOURCE_AUDIT](SOURCE_AUDIT.md); the original file, contracts
and receipt remain byte-preserved. It does not change a scientific interpretation
boundary, estimate an effect, resolve sample identities or claim an author erratum.

Primary source: [Saxton et al., Immunity 2021](https://doi.org/10.1016/j.immuni.2021.03.008),
the supplied 23-page final PDF, SHA-256
`437f76f8f63e3c4282de61959b34d86d1fd04f585aa0cc9e04066f4e3f9b578d`.
Read-only hash verification passed. Poppler rendered PDF pp. 6–11 to temporary PNGs;
figure panels/captions were visually inspected. PDF page numbers below differ
from journal pagination. Methods pp. 22–23 were also text-checked for RNA identity
and source-reported replication. No pixels or curves were digitized.

## Corrected locations

| Source locator | Visible figure / accompanying text | Caption / historical-audit discrepancy | Documentary disposition |
|---|---|---|---|
| Fig. 5, PDF p. 8 / journal p. 666 | **H** contains relative receptor qPCR bars; p. 7 main text also cites 5H | Caption calls this **F**; original audit copied that error and included H among blots | Use **5H** for the qPCR locator. Gapdh normalization, mean SEM and n=3 are caption-reported assay metadata; individual animal values are unqualified |
| Fig. 5F/G, same page | Both panels are explicitly labeled **HepG2 cells**; both show immunoblots | Caption's G/H blot description says HT-29; H is visibly qPCR | Identify these as **figure-labeled HepG2 blots**, retain the caption conflict; do not infer raw preparation identity from either label alone |
| Fig. 5I, same page | HEK-293T receptor-expression comparison shown as immunoblots | No relocation needed | Keep **5I** distinct from H qPCR and F/G blots; no surface-abundance inference from whole-tissue RNA |
| Fig. 7G/H, PDF p. 10 / p. 668 | G is headed **liver**, H **skin**; p. 11 main text cites hepatic expression as 7G and skin as 7H | Continued caption on PDF p. 11 / p. 669 says skin (G), liver (H) | Figure and main text agree; caption reverses organs. Use image-qualified locators, retain unresolved provenance conflict before any tissue-assigned numerical reconstruction |

The corrected blot list is **3F; 4A–C; 5B–G and 5I**, excluding 5H.
Figure 4D and Figure 5J are conceptual models, not measured response curves.

## Endpoint and replication check

| Panels / PDF pages | Source-reported endpoint and uncertainty | Remaining numerical qualification |
|---|---|---|
| 3D/E / p. 6 | Same-analyte normalized flow fluorescence; mean SD, three replicates. E is a fitted-maximum summary of D | Independent preparation/replicate series and raw values unqualified; no fits, ratios or new maxima computed |
| 3F; 4A–C; 5B–G,I / pp. 6–8 | Immunoblots, including tissue lysates and indicated cell preparations | Raw intensity series, replicate keys and some caption identities unqualified; no densitometry |
| 5H / p. 8 | Relative receptor qPCR; source caption reports mean SEM, n=3 | Raw animal values and surface/cell-specific receptor measurements not qualified |
| 6A/B/D / p. 9, methods pp. 22–23 | Bulk colon RNA after six-hour treatment; two independent biological RNA replicates source-reported | R1 qualifies deposited libraries, not animal independence. Counts recovered; R2/R3 remain policy-held |
| 6C/E / p. 9 | Relative qPCR; mean SD, two biological replicates, each technical triplicate | Raw Ct values and nesting links unavailable in the inspected material; triplicates do not increase biological n |
| 7A/B / p. 10 | MTT metabolic viability / relative marker qPCR in organoids; caption n=3 mice per group | Organoid/well-to-mouse mapping unqualified. MTT is not a survival-time endpoint or mature lineage output |
| 7C / p. 10 | Crypts per circumference and mean crypt depth (micrometres); caption n=3 and n=8 mice respectively | Crypt-to-animal measurement links/raw values unqualified; these are distinct endpoints |
| 7D / p. 10 | Serum lipase and amylase, axis U/L with displayed scale; caption n=5 mice per group | Separate acute injury markers, not linked durable functional recovery |
| 7E/G/H / pp. 10–11 | Relative tissue qPCR; mean SD, two biological replicates, each technical triplicate | Raw Ct/animal/nesting keys unqualified; G/H organ-caption discrepancy retained |
| 7F / pp. 10–11 | Serum SAA1/2 and haptoglobin, micrograms/ml, at 24 hours; mean SEM, three biological replicates | Raw sample keys/values unqualified; systemic outputs are not epithelial repair |

For 7A–D the general statistical-methods section reports SEM, but the individual
captions do not fully specify every aggregation hierarchy. Retain that provenance
level rather than inventing organoid/crypt-level error models. No new significance
or functional-effect estimate is supplied.

## Access and coverage boundary

Reuse the original audit's dated access record: official GEO SOFT and both tables
were recovered; publisher supplement access returned 403 and attempted PMC local
retrieval returned challenge HTML. These are recorded retrieval failures, not
proof that supplements or raw measurements do not exist. Their contents remain
**not assessed** here. The main-figure source audit is complete at this bounded
coverage; full supplementary reproduction is not claimed. The supplied PDF's
annotations/highlights are retained in its hash-bound source copy.
