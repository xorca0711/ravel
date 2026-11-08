# Missing-file request — draft, not sent

Updated after [qualification of the supplied Tables S1–S6](SUPPLEMENTS_RESULTS.md).
Those workbooks are received and no longer requested. The [original GEO result](RESULTS.md)
retains the earlier holds as dated evidence. This request now names only remaining
exports, exact identity mappings and source clarifications.

Purpose: reproduce author pathology/state composition and the specified
80-micrometer neighborhood comparison for Peng et al., DOI
[10.1016/j.ccell.2025.10.004](https://doi.org/10.1016/j.ccell.2025.10.004).
No recipient or external account is selected; no message or access request has
been submitted. A permitted public download or approved controlled-access export
would suffice. Restricted records need the source's normal access process.

1. **Exact sample and diagnosis manifest beyond Table S1:** discovery identifiers,
   patient→lesion→block→section and section order/distance, platform/library/GSM
   aliases, normal versus adjacent-normal substitution, original/reviewed diagnosis.
   Which P7 library was reclassified, from which diagnosis, in which review version?
   Which of P4's AAH blocks and P21's AIS blocks were selected for discovery Xenium?
   S1 confirms participation but does not map the selected blocks to suffixed aliases.
2. **WES reconciliation:** clarify GSM9226083 (`P6_AAH` in title/description versus
   `P6_AIS` in VCF filename) and provide the correct mapping without replacing
   historical labels. S1 localizes the 79-versus-54 difference to 24 Normal samples
   and one of P4's two AAH blocks. Please supply the corresponding deposit,
   matched-normal control, block and exclusion mapping rather than another total.
   Confirm the five
   snRNA suffix discrepancies listed in [RESULTS](RESULTS.md#discrepancies-that-remain-visible).
3. **Visium spot annotations:** per-section full barcode, pathology category,
   author state and inferred clone as separate fields, excluded-spot/QC flags,
   label dictionary and review/version provenance; cloupe or equivalent export.
   Preserve the mixed-spot rule and identify genes/assays used to support labels.
4. **Images and geometry:** original or approved-reference SVS/H&E images and
   checksums, 11 mm ROI squares, same-section identifiers, image dimensions,
   units/origin/orientation, Xenium OME.TIFF registration transforms/landmarks,
   lesion/RPII polygons and polygon-to-cell exports.
5. **Whole-tissue Xenium data:** section/slide manifest, full cell IDs, centroids/
   boundaries, measured counts/transcripts, exact complete base-plus-add-on panel, author
   labels and QC. Please reconcile the different discovery cell totals in Results
   and Methods and provide exclusions. Do not supply only a downsampled embedding
   as the neighborhood analysis denominator.
6. **Neighborhood recipe and processed objects:** radius, center inclusion,
   boundaries/edge exclusions, eligible cells, density normalization, clustering
   and label maps for C15/C16 and TMA C4. The exact eleven referenced Figure 1/5
   objects are listed in [the dependency inventory](../../analysis/research/runs/Pg1_metadata_v3_20261108/author_required_objects.csv),
   including `Figure 1B.rda`, `Figure 1C.downsample_25_percent.rds`, `Figure 1D.rds`,
   and Figure 5A, 5B 5C, 5D, 5E, 5G, 5H, 5J and 5K `.rds` files. Full inputs and
   producing code/version are needed where a plotted matrix is insufficient.
7. **Full panel and individual TMA map:** S2/S3 programs/signatures and S4's two
   100-gene custom add-ons are received. The exact versioned base panels and
   measured gene axes are still needed; a gene missing from an add-on is not
   necessarily unmeasured. S1 supplies 188 aggregate cores across eight TMAs and
   19 patient labels. Please provide individual core IDs, core→lesion→patient and
   barcode mappings, exclusions and assay/QC versions. Define the parenthetical
   numerals in lesion text rather than relying on inferred counts or sizes.
   Retain distinct discovery/TMA cohort identifiers and reported independence.
8. **Record versions:** identify the intended human data version (concept
   15670280 currently resolves to restricted 18851077), restricted code 17172149,
   and the unresolved README reference 17148540. Supply permitted access routes
   and checksums for any replacement/export; public empty lists do not imply no files.
9. **Specific supplementary source clarification:** S5 Sheet1!A333, in the Gene
   column of a cDC1 DEG row, stores numeric serial `45903` with `d-mmm` formatting
   (displayed as 3 September 2025). Please supply the original gene symbol. No
   symbol has been guessed from the date. S2 pan-lineage MP6 and Visium MP1 each
   contain 49 nonempty gene entries; if a different list was used for the published
   calculations, provide its exact version rather than an inferred extra gene.

Minimum next delivery: the specimen manifest and barcode pathology export can
advance their own qualification even if other files remain restricted. Geometry,
panel and full-cell inputs separately determine which later comparisons can run.
No promise of independent validation, mechanistic inference or laboratory
readiness is requested or implied.
