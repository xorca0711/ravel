# A14: withdrawal source, endpoint and unit manifest

Reviewed 3 November 2026 by the coordinator before numerical extraction.
Scope: the published Choi 2020 Fig7 withdrawal reference, not a new exposure-
duration interaction or fibroblast-reception effect. [Prospective sequence](PLANS.md#a14--withdrawal-recovery-measurement-qualification).

## Source and measured comparison

[Choi 2020](https://doi.org/10.1016/j.stem.2020.06.020), Results section on
terminal AT1 maturation, Fig7D/E and its legend: organoids receive IL-1beta
for 14 days, followed by seven days with continued input or withdrawal;
an untreated control is also displayed. Panel E measures relative qPCR RNA
in isolated epithelium. The legend reports four biological replicates from
two experiments; preparation identities and pairing are unspecified. The
quantitative RT-PCR methods specify Gapdh normalization with the delta-Ct
method. Figure7 labels Limch1, whereas the methods list Limch2; that annotation
discrepancy is retained rather than silently resolved.

| Panel | Displayed endpoints | Use here |
|---|---|---|
| 7E, top two rows | Ager, Aqp5, Vegfa, Clic5, Cav-1, Sdpr, Spock2, Limch1 | Late-marker withdrawal reference |
| 7E, bottom row | Hif1a, Slc16a3, Slc2a1, Cldn4 | Metabolic/transition RNA context |
| 7A-C | Organoid scRNA comparisons | Continuous-input context; not withdrawal |
| 7F-H | 2-DG during continued IL-1beta | Separate intervention; not cessation |

The Fig7E late-marker charts display bars/error bars without recoverable
individual dots; the lower row displays dots without unit IDs. No preparation-
linked numerical values were found in the checked attachments. This statement
is bounded to those sources, not a claim that no data exist elsewhere.

## Actual access and provenance

The repository's cached PMC XML was read at `raw_data/A32_GSE234197_v1/choi2020.xml`
(SHA256 `bd84f05276c124ddd7fdab3e29407bc26c84f35fd04a2a1fde66030cc4cb9736`).
Its data-availability section lists GSE145031, GSE144468 and GSE144598; its
supplement list contains figure/article PDFs rather than a qPCR spreadsheet.

The [Cambridge author deposit](https://www.repository.cam.ac.uk/items/0ba47cf1-0230-43df-9d13-59751b9253c4)
was independently inspected through its public attachment API. The ORIGINAL
bundle contains ten files: manuscript and supplement PDFs, a graphical abstract
and seven figure TIFFs. The [manuscript PDF](https://api.repository.cam.ac.uk/server/api/core/bitstreams/cff8fe07-88da-4e51-838e-dc0fd5e05979/content)
legend agrees on the unit description. The [Figure7 TIFF](https://api.repository.cam.ac.uk/server/api/core/bitstreams/526e3c41-8b0f-4690-976e-e5d706e22922/content)
was visually inspected for panel labels and displayed units. The
[16-page supplement](https://api.repository.cam.ac.uk/server/api/core/bitstreams/22fd2c5e-5522-4023-a5c0-4a7eda7c05d2/content)
was text-indexed: Figures S1-S7 and legends, with no linked qPCR value table.
This is the author-deposit version; exact pixel equivalence to the final
publisher figure was not asserted.

Local ignored source cache: `raw_data/full_priority_20261103/A14/`, containing
the API attachment index, `retrieval.json`, original TIFF/PDF and a review PNG.
Figure TIFF SHA256: `e1a6a4419a1fc6f27d91d11de99eb3a49c3da5049cd7b5d91b4c482b5d281ef0`.
Supplement SHA256: `d304e01ad5a55e55c0c0ccfc8acdbbad8e5053db1fb70793a9d4ea442a6855eb`.
No source image or full copyrighted text is added to the tracked repository.

Search date: 3 November 2026. Queries: `"Choi" "2020" "IL-1beta" "Figure 7"
withdrawal source data` (the actual query used beta as a Greek character),
`"10.1016/j.stem.2020.06.020" supplementary data`, `"Inflammatory Signals
Induce AT2" site:repository.cam.ac.uk`, `"PMC7487779" "mmc1"`, and `"Choi"
"Fig. 7E" "Spock2"`. This was source recovery, not a new literature census.
PMC web access returned a browser challenge, Cell returned 403, Europe PMC
web access failed, and the Cambridge page timed out in web retrieval. Its
public API and manuscript PDF succeeded. An initially guessed Cambridge handle
was unavailable and was not used as evidence; the resolved item above was used.

## Disposition and biological implications

**Intake complete; exact quantitative reproduction remains unestimated.**
The specific missing inputs are the Fig7E preparation-level values (including
the underlying target/reference measurements or author-normalized equivalents)
and preparation-to-experiment/condition map. Published n is not a substitute
for that map. Figure pixels cannot recover missing pairing, batch structure
or exact qPCR values. No digitized value, inferred biological n, p-value or
effect estimate was generated.

The next informative step would be to obtain that existing source table and
unit map, then freeze a narrowly defined reproduction at the supported unit.
No author was contacted. The current GSE144468 control/continuous-input
analysis cannot be relabelled as withdrawal. Neither marker recovery nor an
approximate bar-height difference would establish lineage-derived mature
output, persistence after verified cessation, an exposure-duration effect or
a fibroblast-specific contribution. Selection/survival and culture history
remain alternatives for those broader questions.
