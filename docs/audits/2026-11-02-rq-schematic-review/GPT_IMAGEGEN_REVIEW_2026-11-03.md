# GPT figure production and matte review

This records the completed local-generation stage. The subsequent
[publication review](MATTE_PUBLICATION_2026-11-03.md) records the owner's request
to replace the displayed SVGs with these PNGs in PR #159.

Completed 3 November 2026 KST; production began 2 November. Scope: all 33
registered questions A0–A32. This is an editorial illustration task, not a
biological analysis, new question, or scientific acceptance decision.

## Delivered locally

All 33 questions have a distinct GPT-generated matte PNG, actually viewed during
review. The owner requested less glossy, less artificial artwork: muted pigments,
fine drawn outlines, restrained shading and clear biological compartments.
Controls occupy compact comparison labels where appropriate; paired tissues or
competing explanations retain the space required by their question.

The local production folder is `.tools/rq_imagegen_20261102/`. Its searchable
`GALLERY.html` and `GALLERY.md` contain the full set, full-resolution links, exact
selected prompts, owning guides and literature contexts. `MANIFEST.json` records
selected-image and prompt hashes, dimensions and registered source bindings.
`MATTE_REVIEW.json` records the actual-image editorial decisions. Earlier images
and prompts are retained. A0–A31 select `matte_v1`, except A25 selects `matte_v2`;
A32 selects the matte pilot `v3`.

These are local, ignored review artifacts. They have not replaced the registered
SVGs or been published to PR #159. The root README remains collection navigation.
The existing [SVG review](CELLULAR_FIGURE_REVIEW.md) remains historical evidence
for the registered illustrations.

## Corrections retained in the selected images

| Questions | Editorial correction or biological distinction |
| --- | --- |
| A4 | Plump transitional cells; selective expansion/survival shown as a separate alternative to response acquisition. |
| A6 | RNA and population composition separated; no RNA-to-activity equivalence. |
| A14, A19 | Comparable cessation/recovery timing; both scheduling alternatives connect to both relevant endpoints. |
| A15 | Active-ligand and total-supply measurements remain required, not already measured. |
| A20, A21 | Seven-helix Frizzled class illustrations; A21 explicitly omits connecting loops and keeps proposed gCap-to-aerocyte direction. |
| A23 | Entry, residence and exit remain distinct; removed numerical screen text from the qualitative illustration. |
| A24 | Stromal population remains unspecified rather than assigning an unsupported subtype. |
| A25 | Cross-sectional model alternatives retained; corrected a clipped footer in a new version. |
| A28 | CTLA4 shown with two separate membrane-spanning subunits; nuclear Foxp3 and cytoplasmic IL-17A/F retained. |
| A30 | Single-stranded cytoplasmic RNA motifs replace DNA-like nuclear helices; paired association does not imply migration. |
| A31 | Candidate GRIA1-containing assembly remains conditional, with no selected partners, ion flux or inferred receptor activity. |
| A32 | Cytosolic ARG1 premise; separate collagen and mature epithelial endpoints; lower proposed branch addresses the whole epithelial endpoint, not AT2 alone. |

Dashed hypotheses, unanswered endpoint questions, unfavorable prior observations
and interpretation limits remain visible. Protein and receptor drawings are
qualitative class illustrations, not validated molecular structures. Cell counts,
colours and illustrated arrangements are explanatory, not measured results.

## Validation and limitations

The deterministic local validator passed: 33 unique selected PNGs decoded, 33
source bindings matched and 233 local HTML references resolved. Selected images
total 70,813,358 bytes. File inspection did not modify image pixels. An initial raw
SVG checksum check detected Windows CRLF conversion; the local check was corrected
to use the existing repository's LF-normalized text-hash convention. No source SVG
changed, and no repository validator or governance rule was modified.

HEAD remains `51a3be1a26244b8d73a894629f6b854ab4b7b6c1`. Refreshed `origin/main`
remains `5eb710d03ed714e245bb8d34136afcf8034b6d96`. Git comparison confirms the root
README, registered guides, contexts, registry and SVGs are unchanged from HEAD.
The local gallery received static link/asset checks; browser interaction was not
tested. Actual generated images were viewed individually during production.

Repository validation passed 14,023 checks; the research gate against refreshed
`origin/main` returned `ok: true` with no errors. Whitespace checks passed. The
completion entry is recorded in `PROGRESS.md`. No numerical biological analysis
was rerun. There is no
remaining image-generation hold; existing scientific/data limitations are
unchanged. Selecting these drafts for tracked publication is a separate
integration step, not an automatic promotion of scientific claims.
