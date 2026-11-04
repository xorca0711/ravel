# A5 exact feature-context display specification v1

4 November2026. Review-ready, not yet frozen. This implements the candidate-process question cleared in principle in [the comparison proposal](A5_CANDIDATE_PROCESS_COMPARISON_V1.md). All earlier outcomes remain exposed. The exact map was fixed from source annotations before effect access for this new view; the view is exploratory and does not create an unexposed test.

## Biological decision and alternatives

The organizing aim is to identify which development-associated process is recruited during adult repair and what consequence merits further investigation. The existing positive Guo aggregate, negative original regulator/transport contributions and mixed destination panel motivate one narrower comparison: does the fixed component show distributed junction/basement-membrane-associated RNA in transitional relative to activated AT2 cells, or mainly signal context/heterogeneous recruitment? These explanations may coexist. The measured endpoint can nominate an architecture/localization comparison; it cannot establish assembled junctions, deposited matrix, transport function, developmental ancestry or productive repair.

Published premises and exact source/access limits are in the linked proposal and existing A5 context; this same-source re-expression is not independent replication. No new literature sweep is needed for this unchanged reviewed comparison. The strongest threats are cross-sectional state selection, sampling-time mixture and broad/cross-tissue functional annotations being mistaken for a coherent active process.

## Fixed source map and plotting order

[A5_FEATURE_DISPLAY_MAP_V1.tsv](A5_FEATURE_DISPLAY_MAP_V1.tsv) contains all99 original genes, with exact original99/57/53 memberships/manual roles, accession/version/source locators, complete GO qualifier/evidence references, uncertainty flags and inclusion/context rationale. The map SHA is recorded in [the input manifest](A5_FEATURE_DISPLAY_INPUTS_V1.json). It is the entire display map; no additional role is assigned by the plotting script.

Its mutually exclusive *layout groups* are7 junction/polarity candidates,5 basement-membrane material candidates,1 adhesion/signaling interface, original5 receptor/ligand members, original4 specialized transport members,25 peripheral architectural-context members, original6 source-nominated regulators, and46 remaining members. Layout placement does not make biological roles mutually exclusive. Original Eya2 enzyme/regulator overlap and other contextual overlaps remain annotations, never additive family totals. Every row appears once in the all-member view.

The candidate panel is exactly the first22 rows across the first5 groups. Junction/polarity: Cgn,Crb3,Dsp,Igsf5,Llgl2,Pard6b,Pkp2. Material: Col4a3,Col4a4,Col4a5,Lamb3,Lamc2. Interface: Itgb6. Signal: Areg,Egfr,Erbb3,Fzd5,Shh. Transport: Aqp5,Scnn1b,Scnn1g,Slc26a9. Pard6b/Llgl2 are included for explicit polarity source annotations despite ontology-group differences. Mal2/Myo5b/Rab25 are peripheral polarized-trafficking context, not additional specialized-output members. Ccdc120/Cep170b and generic vesicle/microtubule members remain peripheral; Matn4 is cartilage-ECM context, not nominated epithelial basement membrane. The other46 members retain their specific source rationale rather than being labeled nonfunctional. Full member rationales remain available in the map, including unreviewed/missing-function cases.

Rows use the fixed numeric display_order (group then alphabetical gene). Columns use numeric day then lexical sample_id. No clustering, effect sorting, effect-based removal or replacement gene set is permitted. The earlier six-regulator set and new GO-root associations are different definitions; no new14-root aggregate is calculated.

## Inputs, unit, endpoint and formulas

Use only immutable outputs of A5_component_attribution_v1_20261103: member_contributions.tsv, unit_support.tsv and receipt.json, plus the frozen source map/crosswalk/annotation files. Verify their manifest hashes and receipt lineage. No count matrix, target-count primitive, raw expression extraction or rarefaction rerun is needed.

Biological unit is the original24 mice. Preserve original state/depth/cell-floor qualification,32-source-sample provenance and the exposed sampling schedule; use only the24 already paired mice. Each eligible mouse must have exactly99 distinct member rows and paired support for the original activated-AT2 and transitional states, with a single consistent day. Missing/duplicate joins, altered memberships or any unqualified mouse stop execution rather than change eligibility.

Let d[m,g] be the existing delta_detection_pp: transitional-minus-activated-AT2 difference in expected detection after the original500-UMI sampling, in percentage points. Let c[m,g,M] be the existing contribution column for original moduleM (99,57,53 members). Copy these values without reconstruction from counts. Verify c=d/N for members and c=0 for nonmembers within numeric round-trip tolerance1e-10; nonmembership is displayed as excluded/NA for a module-specific interpretation, not biological zero. Verify module sizes99/57/53 against the map and original roles against the crosswalk. Tolerance validates arithmetic; it is not an effect margin.

For each gene, report equal-mouse mean d, minimum/maximum d, and counts of positive/negative/exact-zero d across the24 mice. For each original module, report copied per-mouse contributions and equal-mouse mean contribution for included members, retaining membership flags. For each observed day/gene, report n_mice, equal-mouse mean and min/max d with sign counts. Days are descriptive strata, not independent replicates; do not replace the primary equal-mouse mean with an equal-day mean. No p-values, new confidence intervals, significance calls, coherence threshold, architecture score, gene ranking or family-level summed contributions.

## Outputs and figures

Proposed run directory: `analysis/research/runs/A5_feature_context_display_v1_20261104/`.

- `all_member_values.tsv`: complete24x99 mouse/member values, original contributions/membership, day, fixed layout/role/source fields.
- `gene_summary.tsv`: all99 genes with descriptive mouse means/ranges/sign counts, module-specific means and fixed ordering; no binary coherence classification.
- `gene_day_summary.tsv`: complete observed day/gene descriptive summaries, with actual n_mice.
- `support.tsv`: all original source support rows with unchanged eligibility and explicit included-mouse disposition.
- `source_role_crosswalk.tsv`: unchanged fixed original-role/GO crosswalk for review.
- `all_members_by_mouse.png`: all99 rows and24 mouse columns, ordered as above, group separators and day annotations. Missing values are errors, not white zeros.
- `candidate_features_by_mouse.png`: the fixed22 candidate rows on the exact same mice and shared color scale; source-evidence caveats in caption.
- `summary.json`: input/map lineage, counts, arithmetic checks, day/sample ordering and descriptive scope.

Both heatmaps show d in percentage points with a diverging scale centered at zero and identical symmetric limits derived from the maximum absolute d across all99x24 values; no clipping. Color limits are a display rule, not selection. Gene names and group boundaries remain readable; group colors label layout only. Qualifier/evidence confidence belongs in the linked tables/captions and is not a causal-evidence score. The22 are a selected display, not an exhaustive inventory of junction/signaling biology. Ppl remains peripheral because its cited function concerns keratinocyte/desmosome context; this does not mean it lacks junction-related function. Other core candidates also have cross-tissue or inferred evidence. Neither figure draws functional arrows. The report will link all-member results alongside the candidate panel and preserve opposite/zero patterns.

Proposed script: `RQ_Specified/A5_developmental_programme_reuse/scripts/feature_context_display_v1.py`. Proposed contract: `analysis/research/contracts/A5.feature_context_display_v1.json`, amending `analysis/research/contracts/A5.component_attribution_v1.json`. Proposed report: `RQ_Specified/A5_developmental_programme_reuse/reports/FEATURE_CONTEXT_DISPLAY_V1_RESULTS.md`. Script/contract are prepared only after this exact review; final input/code hashes and -text attributes must be verified before the narrow freeze.

## Informative outcomes and review boundary

Distributed same-direction architecture-associated members with a different specialized-transport pattern would support an RNA-context nomination for independent localization/state comparison. A signal-restricted pattern would weaken this architectural explanation and shift the next question toward input/recipient context. Mixed or sparse architectural directions yield a qualified mixed finding or no process nomination; the aggregate cannot override them. Opposite mouse/time patterns constrain transport and must be reported. These are descriptive interpretations, not pass/fail cutoffs or evidence of causal repair.

Coordinator review of this map/spec precedes any new effect access, contract freeze or run. Then run targeted schema/input preflight and a small synthetic fixture checking joins, exclusion semantics, ordering and contribution arithmetic; verify the new receipt and inspect both figures. Coordinator numerical/biological review precedes current owner README/context/dossier updates in their existing evidence sections. A31 remains reused; no other analysis is implied.
