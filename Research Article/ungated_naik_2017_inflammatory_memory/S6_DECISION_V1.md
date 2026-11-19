# S6: three bounded extensions from the completed Naik reconstruction

19 November 2026. Owner `Nk17-P01`. S5F is preserved at `2514379` after
coordinator review of its complete report, 38 contrasts and five figures without
further revision. This is agent progression review, not human scientific
acceptance. The coordinator authorized assessment of the three candidates below
and preparation of the first supported prospective design. The coordinator then
reviewed this assessment, S6A design and literature refresh without revision,
and authorized S6A implementation and governed execution. D180 source acquisition
and hashing are separately authorized; D180 effect extraction still needs its
own reviewed contract. The subsequent [acquisition checkpoint](D180_ACQUISITION_V1.md)
records all four completed files and hashes; reader qualification remains next.

## What the completed sequence leaves unresolved

The organizing question remains how inflammatory history alters a later
epithelial response after apparent recovery. [S2](S2_RESULTS_V1.md) describes
smaller aggregate D30 RNA contrasts; [S4](S4_RESULTS_V1.md) and
[S4B](S4B_RESULTS_V1.md) expose shared-baseline and reference dependence plus
an unresolved recorded-sex/marker discrepancy. [S3](S3_RESULTS_V1.md) measures
relative ranks near fixed annotation boundaries, not the paper's retained distal
domains. [S5M v2](S5M_RESULTS_V2.md) shows stronger acute than recovered/recall
RNA–proxy alignment. Its negative adjusted covariance does not show repression.
[S5F](S5F_RESULTS_V1.md) supplies separate functional-source measurements,
including mixed EdU and positive Il18KO history contrasts.

The closest source experiments already test inflammatory-history repair,
Aim2/CASP1/IL1R1 perturbation and long-lived accessibility. These are published
premises. The present contribution is exposed shared-source reconstruction and
measurement qualification. None of the following is a new memory mechanism,
independent replication, a global RQ registration or a human retain/reject decision.

## Assessment and proposed order

| Candidate | Actual observation → remaining comparison | What its outcomes change | Qualification and limits | Proposed disposition |
|---|---|---|---|---|
| Daily wound-area sources | F5g reported OE−Ctrl is +0.30 under Ig and +0.16 under anti-IL1R1; OE+anti equals Ctrl+Ig, while blockade also changes Ctrl. Are the within-condition area contrasts and their difference consistent across all supplied days, and how much reflects day-0 group offsets? | Same-direction area contrasts would extend the finite summary comparison; mixed/reversed/coverage-dependent contrasts would narrow it. Starting offsets could account for part of the difference. None establishes complete inhibition or residual pathway independence. | Six original EDF5e/f and EDF6d–g sheets are available, with exact labels, mm² and occupancy. Anonymous columns, declining Ns, caption discrepancies and unqualified original fit constraints remain. | First supported prospective design: [S6A draft](S6A_DAILY_AREA_DESIGN_V1.md). No new area mean or contrast calculated. |
| Fixed five-marker D6 RNA QC | S4 found two baseline libraries with near-zero Xist/high four Y-linked markers despite female metadata. D6 has stronger RNA–proxy association but lacks the full fixed marker display. Does recorded-source consistency differ in the four acute libraries? | Consistency would localize the observed marker discrepancy to the already inspected stages, without proving D6 free of confounding. Discordance would widen the source/QC uncertainty. | Four original count files and frozen S2 factors are local. Xist/D6 profiles are already partly exposed. Markers cannot establish sex, animal pairing, mixture or a preferred correction. | Supported bounded follow-up candidate after its own reviewed design; no new marker values inspected for this assessment. |
| D180 fixed TSS-proxy ranks | D6/D30 contrasts attenuate in aggregate, with heterogeneous anchors and relative-order sensitivity. Do those same finite windows show longer-term displacement and how does it compare with the frozen D30 description? | Persistent, attenuated, reversed or mixed ranks refine durability within this fixed proxy universe; no result reconstructs original retained domains or identifies chromatin memory maintenance. | Four public D180 BigWigs have live HTTP 200 headers. They are paired-end HiSeq2500, versus HiSeq4000 for D6/D30 ATAC. Full files are now acquired; chromosome dictionaries and signal readability are not yet qualified. No D180 RNA is supplied in the current source map. | Supported qualification/design candidate; retain the exact S3 universe, widths, rank formula and all five paper anchors. Acquisition subsequently completed with hashes; no reader qualification or biological calculation yet. |

The area comparison is first because the existing result poses a precise
within-condition question, and its original source files are already available
at small cost. D6 QC is a bounded source diagnostic, while D180 adds a distinct
durability question with new file qualification and a cross-time platform limit.
This order does not rank or retire any portfolio question.

## Daily-area qualification that changes the design

MOESM16 and MOESM17 total 109,483 bytes. Local copies match the coordinator's
published-source SHA-256 records. A separate read-only technical check matched
all 228 group/day occupancy records without computing outcome means or effects.
The initial metadata check encountered an openpyxl `EmptyCell.coordinate`
attribute error; using explicit row/column positions resolved that reader issue.
No scientific run failed. Source workbooks were never saved or modified.

Days differ by sheet: EDF5e 0–10, EDF5f 0–9, EDF6d 0–8, EDF6e 0–9,
EDF6f 0–10 and EDF6g 0–10. EDF6e's row 13 has no day and is not silently made
day 10. EDF6f has a labelled day 10 but both WT groups have no numeric records:
its WT history effect and difference of history effects must be NA at that day,
while its KO history effect remains eligible. A blank is not a healed wound.

EDF6g groups are Ctrl+Ig B:D, Ctrl+anti E:H, Aim2OE+Ig I:K and Aim2OE+anti L:O.
Their numeric counts are 3/4/3/4 at every day, versus main F5g fitted-summary
Ns 3/3/4/4. The final-PDF EDF6g caption states n=4, while the main caption
states n=3. All three source statements remain visible; no group swap or
summary rewrite is justified. Other extended-data caption Ns also differ from
some source groups. The [prospective design](S6A_DAILY_AREA_DESIGN_V1.md) fixes
every range and preserves these discrepancies.

## D6 and D180 qualification needed before their own runs

D6 RNA samples are GSM2440985/986 control and GSM2440987/988 acute IMQ,
SRR5133553–3556, HiSeq4000 paired-end. Use the exact S4 five-marker identities:
Xist `ENSMUSG00000086503.3`, Ddx3y `ENSMUSG00000069045.11`,
Eif2s3y `ENSMUSG00000069049.11`, Kdm5d `ENSMUSG00000056673.14`,
and Uty `ENSMUSG00000068457.14`. A later design should retain raw counts,
frozen S2 MOR/total scales and CPM, with the same log2(CPM+1) display convention.
It must not refit upstream analyses, assign sex, exclude libraries or select a
new marker set from their outcomes. Missing/ambiguous annotation stays explicit.

D180 metadata and URLs come from the saved
[S1M crosswalk](../../analysis/research/runs/naik2017_s1m_metadata_v2/library_crosswalk.tsv)
and [source fields](../../analysis/research/runs/naik2017_s1m_metadata_v2/source_fields.json).
HTTP headers were checked on 19 November at approximately 03:54 UTC:

| Sample | History | Run | Declared BigWig bytes, HTTP 200 |
|---|---|---|---:|
| GSM2652413 | PI replicate 1 | SRR5657347 | 796,895,019 |
| GSM2652414 | PI replicate 2 | SRR5657348 | 806,609,609 |
| GSM2652415 | Ctrl replicate 1 | SRR5657349 | 731,787,530 |
| GSM2652416 | Ctrl replicate 2 | SRR5657350 | 783,218,787 |

The four files total 3,118,510,945 bytes. None is local yet; an HTTP header is
not a checksum/readability or biological-scale qualification. The existing
[S3 runtime](S3_RUNTIME_V1.md) successfully processed eight original tracks;
its supported reader and fixed windows can be reused after D180 acquisition,
hashing and chromosome checks. No environment reinstall or S3 rerun is needed.
The 19 November X-drive snapshot had 73,916,723,200 bytes free, making the
compressed track storage plausible; it does not certify execution readiness.

Retain S3's 21,760 unique windows (21,775 gene mappings), chr1–19/X,
M9-derived boundary proxies, ±1/±2 kb widths and exact percentile-rank endpoint.
All five paper anchors remain Aim2, Casp1, Il1b, Il1r1 and Il18. Casp1 may
illustrate the motivating D30 pattern but cannot select the universe or replace
an unfavorable anchor. D180 contrasts would be within-time PI−Ctrl, with
unpaired library-combination spread, zero/tie flags and width sensitivity;
cross-time magnitude/sign comparisons remain platform- and rank-dependent.

## Original domains and raw reads remain separate options

The source qualification does not establish global coordinate absence.
Inspected MOESM9 contains pathway summaries rather than original retained-domain
coordinates; bounded reporting-PDF checks did not recover them. Cowley 2026's
later 934-domain universe uses GSE171596 D6/D30 FASTQs and is not Naik's original
coordinate set. Public repository private-BED references and the recorded Data S2
access failures leave that exact original-region reproduction unresolved. These
failed routes were not retried. Recovering a qualified region table would reopen
that specific comparison without changing the frozen proxy results.

Raw-read processing is an available design direction, not a demonstrated
impossibility. The saved ENA manifest lists FASTQ URLs, sizes and MD5 values for
all 12 ATAC runs: 38,256,018,859 compressed bytes, including 9,599,745,831 bytes
for the four D180 runs. These are saved metadata, not current transfer tests.
Uncompressed reads, alignment/index files, temporary storage, compatible tools,
compute duration and a compatible sample/peak/normalization design are not yet
budgeted. Such work would answer independent-processing reproducibility and
region-definition questions, while still reusing the same biological source.
It requires a separate scoped contract and resource assessment; it is not needed
to answer the first daily-area question. No raw reads were downloaded here.

## Literature overlap and the next review

Naik 2017 Figs. 4g–h, 5b,d–g and EDF5e/f, EDF6d–g are the direct precedents
and exact same source lineage. The proposed addition is a transparent daily,
within-condition contrast and day-0 decomposition, not discovery of the
published repair effect. Larsen 2021 and Cowley 2026 already provide
establishment/maintenance/long-term precedents; their existence prevents a new
mechanism or novelty claim from this extension. Previously qualified Hamdan
2026 also distinguishes closure and barrier function. A bounded 19 November
search added Walton 2026's oral-remodeling endpoint boundary and a Levra Levron
2023 spatial-priming lead, with source-version/access limits recorded in
[the literature context](LITERATURE_CONTEXT.md#s6-targeted-literature-refresh--19-november-2026).
Neither resolves the anonymous Naik animals or source-N discrepancy.

The [S6A prospective design](S6A_DAILY_AREA_DESIGN_V1.md) is coordinator-approved.
Bind the exact source map, code, tests and outputs to a separate exposed
contract, pass preflight, freeze/commit, and use the governed runner. Return
actual results for review before advancing the other candidates. No task-wide
completion, scientific acceptance or publication is recorded by this decision.
