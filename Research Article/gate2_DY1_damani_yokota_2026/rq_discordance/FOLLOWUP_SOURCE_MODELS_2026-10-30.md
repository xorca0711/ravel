# Follow-up source and model boundaries

30 October 2026, Asia/Seoul. Prospective exposed specification support; no new
biological estimate is reported here. The original Nb-history/later-IAV context
motivates the broader question; F4 is a non-infectious external measurement
comparison. Prior runs and original-study holds remain unchanged.

## F4: source-labelled genotype comparisons

Read [Deochand et al. 2024, Fig. 5 caption and adjacent Results](https://pmc.ncbi.nlm.nih.gov/articles/PMC11489752/#Fig5)
on this date. Fig. 5c broadly reports RNA WT n=3 and cKO n=4. The exact deposited
[sample map](../../../analysis/research/runs/DY1_P02_reference_source_v1/sample_map.tsv)
has WT RNA CTRL/IL4 rep1–3, cKO CTRL rep1–4, and cKO IL4 rep1, rep2, rep4
(GSM7885447–GSM7885449). A fourth cKO IL4 library is absent from the qualified
Updated matrix and its joined SOFT records. The caption/deposit difference is
unresolved; the analysis uses the three deposited libraries without inventing
rep3 or claiming exact author reproduction. ATAC has four libraries in each
of these genotype/condition groups.

Source genotypes distinguish WT LysM-Cre+/+; GRIP1wt/wt from cKO
LysM-Cre+/+; GRIP1fl/fl. GRIP1 here is NCOA2. The source describes biological
replicates, but source replicate labels are not validated animal, litter,
processing-batch or cross-assay matching keys. Different genotype labels do not
justify arbitrary pairing. The 24h-title/25-hour-characteristic discrepancy
persists for ATAC vehicle, as do exact annotation-version uncertainties.

The new estimands are cKO minus WT **within source-labelled IL4**, and separately
cKO minus WT **within CTRL**, in each assay. Offset 1 and all-source-feature CPM
denominators are fixed. The common assay feature universe is every feature not
all-zero across all four selected groups; a feature all-zero in one condition's
two genotypes is retained and flagged in that contrast. This common universe
keeps the baseline comparison interpretable without outcome-based feature
selection. No stimulus-by-genotype interaction is estimated.

Independent-observation Welch 95% intervals use each group's actual n, sample
variance and Satterthwaite degrees of freedom (including RNA CTRL 3 versus 4).
These are conditional illustrations under normal transformed observations and
independence within/across genotype groups, not verified population confidence
intervals. Unknown preparation/litter/batch dependence and background differences
remain unresolved. Sample standard deviations, n and numerical degeneracy are
reported alongside every contrast; zero SE is not certainty or equivalence.
Cross-modal signs and Spearman association summarize dependent mapped rows;
no peak/gene-based significance, causal effect, selected locus or target ranking
is inferred. Source nearest-TSS distance does not necessarily refer to the
Ensembl-assigned gene. Both existing mapping rules and distance subsets remain.

## F3: bounded public qualification

Read the [EGA catalogue](https://ega-archive.org/datasets/EGAD50000001206) on
30 October 2026. It describes duplicate-labelled preparations, baseline and four
later time labels, and demultiplexed RNA/accessibility FASTQs. Its headline
sample count is not an independently qualified biological n. The record links
DAC EGAC50000000485 and controlled access terms.

The separate [preprocessing resource](https://git.embl.de/grp-zaugg/SUMseq) was
checked through the web reader on this date; it returned inaccessible/internal
error. This does not establish the contents of the paper's actual
[analysis source/files repository](https://git.embl.de/grp-zaugg/sum-seq_analysis).
After the independent reviewer identified that distinction, one bounded check
of the exact analysis URL returned `400 Timeout fetching`. This adds to the
earlier feasibility assessment's analysis-page/API timeouts. No further retry,
controlled file retrieval, access request or external contact was made. The
publisher page redirected to an inaccessible authentication page. Failure to
access these resources is not evidence that public matrices do not exist.
A public processed matrix,
paired barcode files, independent donor/differentiation identifiers and valid
reuse rights for those matrices remain unqualified. F3 numerical work stays
held. Same-nucleus pairing would not establish longitudinal tracking even if
the files later become qualified.
