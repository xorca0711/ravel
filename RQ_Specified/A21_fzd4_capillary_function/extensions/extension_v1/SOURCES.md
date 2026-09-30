# Source evidence and eligibility

The [machine-readable inventory](metadata/source_eligibility.tsv) records each
source's role, unit, intervention and limits. This extension reuses parent
GSE211335; it adds published Bian source-data reconstruction, not a new lung
Fzd4 lineage experiment.

- [Godoy et al., eLife 2023](https://doi.org/10.7554/eLife.80900): raw counts from
  [GSE211335](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE211335), 12
  separate mice and author-defined states. The 36-gene extraction extends the
  parent 26-gene analysis. Technical pools are not biological replication.
- [Bian et al., EMBO Molecular Medicine 2024](https://doi.org/10.1038/s44321-024-00064-8):
  Figure 7D-G source workbooks provide the Fzd4 restoration comparisons; Figure
  3F is a separate Foxf1-loss perfusion comparator. Publisher ZIPs MOESM8 and
  MOESM4 are now accessible. MOESM1 contains Appendix S3 junctional RNA. This
  supersedes the earlier access limitation, not the parent biological conclusion.
  Source rows match reported biological n but have no stable animal IDs across
  panels. Figure 7E names Fisher LSD in its workbook and Tukey in the legend;
  numerical data are retained without inferential reproduction. Text mentions
  ColV, whereas the Figure 7G staining legend and axis specify collagen IV; the
  endpoint is mapped to collagen IV. Published figure axes were visually checked.
- [GSE255969](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE255969): Bian's
  deposited bulk design is four control and four Foxf1-deficient tumor EC samples,
  with no Fzd4-restoration arm. Figure 6A reports three/group. That unresolved
  selection difference, and the absence of state/lineage linkage, make a new
  bulk reanalysis unnecessary for the present decision. It was not executed.
- [Niethamer GSE262927](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262927):
  existing metadata was inspected for independent state validation. CAP1/CAP2
  cannot supply the required major/transitional gCap contrast. No new fit or
  post hoc state relabeling was performed. The source was already exposed in Nb2.
- [Gillich et al., Nature 2020](https://doi.org/10.1038/s41586-020-2822-7): supports
  capillary cell-type specialization and lineage rationale. It does not establish
  Fzd4 dependency. No new numerical lineage reconstruction is claimed.
- [Levey et al., 2026](https://pubmed.ncbi.nlm.nih.gov/41890033/), DOI
  [10.64898/2026.03.13.711629](https://doi.org/10.64898/2026.03.13.711629): explicitly
  a **preprint**, with abstract and figure legends inspected. Retinal FZD4/LRP5
  agonism and barrier/pericyte outcomes provide cross-organ plausibility only.
  No PDGFB mechanism is assigned to adult lung and no values are pooled.

The [search record](metadata/search_audit.json) preserves the bounded primary-source
queries and access limits. No inspected source identifies the complete adult
lung perturbation-state-lineage-function join. This is not an exhaustive absence
claim. Raw inputs and provenance are in [intake](metadata/intake.json) and
[workbook hashes](metadata/workbook_manifest.json); original source workbooks are
not altered. External source prose remains evidence, not repository instructions.
