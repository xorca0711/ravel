# Nb2: retrospective RQ review against current main

Reviewed 1 October 2026 against `origin/main` commit
`f61343cc16c83e979b071393adccdcf8084ea294`. Nb2's established package and
A19–A21 are on main but absent from this stale working checkout. This review
adds only this file: it does not restore, replace or merge the remote package.
All links below are pinned to the reviewed commit so that the evidence is
accessible without pretending the missing local files are present.

## Source inventory and execution order

Comparison of immediate article directories found **Nb2 as the only article
package present on main and absent locally**. Local `Primary` is a source archive;
local Nb3 is the new package being developed. The other main article directories
have local counterparts and are reviewed separately. This inventory concerns
article directories, not every difference between the two repository versions.

| Date and stage | Later evidence that changes the framing | RQ consequence |
|---|---|---|
| 29 September, [first-pass execution](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/Research%20Article/gate2_N1_nabhan_2023/EXECUTION.md) and [results](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/Research%20Article/gate2_N1_nabhan_2023/RESULTS.md) | Bulk input/withdrawal profiles and descriptive receptor maps separate RNA output, receptor abundance and functional growth. Culture identity, timing and several functional joins remain unresolved | Receptor expression and selected target panels cannot by themselves rank regenerative benefit |
| 29 September, [eight-branch extension](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/Research%20Article/gate2_N1_nabhan_2023/branch_analysis/RESULTS.md) | Withdrawal-associated AT1 direction survives omissions but is imprecise; narrow source-YAP and broad sustained-YT scores disagree; four paired states dissociate Fzd5 abundance from canonical-target RNA. AF1/AF2 differences weaken unique Fzd1 support. Pooled Fzd4/cycling association reverses between rounds | Favor state-dependent expansion-to-maturation, subtype-specific receptor function and maintenance-versus-renewal questions. Reject a generic YAP mediator, unique Fzd1 benefit or pooled vascular correlation as established mechanisms |
| 29 September, [RQ synthesis](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/Research%20Article/gate2_N1_nabhan_2023/RQ_DERIVATION.md) | N1/N2/N3/N5 feed A19; N6 feeds A20; N7 feeds conditional A21. N4 and N8 remain paper-local | IDs A19–A21 were already allocated; Nb3 must not reuse them |
| 30 September, [A19 context analysis](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/RQ_Specified/A19_fzd_response_reversibility/RESULTS.md) | Human CHIR-absent qPCR shows airway-marker increases and SFTPC loss, but bulk SFTPC differs and AT1/airway responses are mixed. Airway-derived cultures show transient SFTPC induction despite continued CHIR | Narrow toward retention of alveolar competence during expansion, including a pre-withdrawal acquired-state branch. CHIR absence is not verified Fzd withdrawal, and neither RNA assay measures mature descendants or AT2 reserve |
| 30 September, [A20 input-context extension](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1/RESULTS.md) | Four donors show increased canonical-response and reduced support-panel RNA after CHIR. TGF raises FZD2/collagen while reducing the support panel. RNA and functional cohorts are unmatched | Higher receptor or canonical RNA is not a support surrogate. Distinguish maintenance of a maturation-capable AT2 pool from instructive maturation, fibroblast survival and matrix effects |
| 30 September, [A21 independent-cohort analysis](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/RQ_Specified/A21_fzd4_capillary_function/RESULTS.md) and [extension](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/RQ_Specified/A21_fzd4_capillary_function/extensions/extension_v1/RESULTS.md) | Independent gCap/aerocyte pairs retain Fzd4 enrichment, while all 11 primary transitional/major-gCap pairs have less Fzd4 in the transitional state. Within-condition cycling associations remain inconsistent; vascular-restoration evidence comes from a different tumor setting | Retire the old pooled coefficient as affirmative renewal evidence. Refine toward vascular integrity enabling later repopulation, while retaining renewal-specific function as a competing hypothesis |

Dates are those in the deposited reports. Within a date, the logical dependency
is reported; no unrecorded clock-time order is inferred. RQ-owned later analyses
are not counted as new Nb2 results or independent repetitions of Nb2.

## Strict review of the surviving candidates

| Current question or source branch | Decision | Conditional framing and decisive distinction |
|---|---|---|
| [A19](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/RQ_Specified/A19_fzd_response_reversibility/README.md) | **Later evidence already incorporated; preserve the current narrowed hypothesis.** No duplicate branch is needed | Retained alveolar identity during expansion may permit mature AT1 contribution after Fzd withdrawal while retaining responsive AT2 reserve. Initial state, acquired pre-withdrawal state and later fate are distinct variables. Selection, missing maturation cues and input differences remain rivals |
| [A20](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/RQ_Specified/A20_fibroblast_fzd_context/README.md) | **Already narrowed to Fzd2 versus Fzd1 within AF1; do not restore the earlier unique-Fzd1 or broad-subtype wording** | Compare verified receptor dependence in a prospectively defined receiving state, with viable fibroblast/epithelial abundance, support, matrix and later absolute mature output kept separate. Concurrent TGF/CHIR interaction is not an initial-subtype interaction |
| [A21](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/RQ_Specified/A21_fzd4_capillary_function/README.md) | **Conditional, lower-priority candidate already refined; no affirmative expression-to-renewal claim** | Determine whether vascular integrity permits later traced renewal and aerocyte production, or whether receptor dependence is selective for regenerative entry. Expression alone cannot separate these routes; maintenance and the two descendant yields require distinct outcomes |
| Nb2-N4: loss versus blockade | **Retain paper-local and deferred** | Comparable receptor loss, protein/engagement and target breadth must be established before adaptation or compensation is invoked. There are no deletion or inhibitory-antibody RNA libraries in the analyzed bulk cohort |
| Nb2-N8: endogenous Fzd6 input | **Retain paper-local and deferred** | Synthetic receptor sufficiency and ligand RNA do not identify an endogenous dependency. A linked ligand-by-receptor contrast is needed before choosing an endogenous mediator |
| Connections to A1/A4/A8/A10/A13/A14/A15 | **Related scope only, not new hypotheses derived by this review** | Regulatory distinction, Wnt/IL-1 sequence, incremental maturation information, growth prediction and reciprocal niche questions retain different interventions or endpoints. Shared pathway names and RNA panels do not merge them |

## Register recommendation

The September 30 canonical cards already contain the useful biological
refinements. **No new biological branch or RQ ID is recommended from re-reading
Nb2 alone.** Add a provenance link if useful; preserve the current A19–A21 titles
and conditional status. In particular, do not let a stale September 29 derivation
overwrite the later A19 competence, A20 pool-maintenance or A21 integrity framing.
Any new Nb3 contribution must make a separate prediction against these current
questions, rather than merely sharing Wnt, identity or niche vocabulary.
