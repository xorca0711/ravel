# Missing-file request — draft, not sent

Purpose: reproduce author pathology/state composition and the specified
80-micrometer neighborhood comparison for Peng et al., DOI
[10.1016/j.ccell.2025.10.004](https://doi.org/10.1016/j.ccell.2025.10.004).
No recipient or external account is selected; no message or access request has
been submitted. A permitted public download or approved controlled-access export
would suffice. Restricted records need the source's normal access process.

1. **Sample and diagnosis manifest / Table S1:** discovery cohort identifiers,
   patient→lesion→block→section and section order/distance, platform/library/GSM
   aliases, normal versus adjacent-normal substitution, original/reviewed diagnosis.
   Which P7 library was reclassified, from which diagnosis, in which review version?
2. **WES reconciliation:** clarify GSM9226083 (`P6_AAH` in title/description versus
   `P6_AIS` in VCF filename) and provide the correct mapping without replacing
   historical labels. Reconcile 79 sequenced samples with 54 deposited GSM/VCF
   records, including matched-normal provenance and exclusions. Confirm the five
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
   boundaries, measured counts/transcripts, complete base/add-on panel, author
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
7. **Tables S2–S4 and TMA:** gene programs/signatures, exact base/add-on panels,
   distinct cohort ID, core→lesion→patient map, 188 retained cores and exclusions
   across eight TMAs, and assay/QC versions. Confirm independence of the reported
   19-patient cohort without equating its patient numbering with discovery.
8. **Record versions:** identify the intended human data version (concept
   15670280 currently resolves to restricted 18851077), restricted code 17172149,
   and the unresolved README reference 17148540. Supply permitted access routes
   and checksums for any replacement/export; public empty lists do not imply no files.

Minimum next delivery: the specimen manifest and barcode pathology export can
advance their own qualification even if other files remain restricted. Geometry,
panel and full-cell inputs separately determine which later comparisons can run.
No promise of independent validation, mechanistic inference or laboratory
readiness is requested or implied.
