# A5: attribution of the actual fixed developmental component

3 November 2026. Reviewed specification frozen at `2841bf5`; [run receipt](../../../analysis/research/runs/A5_component_attribution_v1_20261103/receipt.json) verifies. All99 members and 24 original mice are retained. The new extraction uses 7,806 eligible cells and reconstructs all 216 original unit/module and paired-module values (maximum error 1.78e-15 percentage points). Independent synthetic hypergeometric checks agree within 1.91e-11. This is exposed attribution of the same Strunz source, not independent replication or scientific acceptance.

The original positive aggregate is not a uniform increase across the six annotated gene-expression-regulation members: their **net contribution is negative in the full 99-gene component**. The four retained in the 57/53-member forms contribute small positive values. Receptor/ligand members contribute positively, while the four transport members contribute negatively to the full set. These are net subset contributions, not statements that every member shares a sign.

Only 18 of 99 members have role assignments in this deliberately bounded pre-outcome mapping. The 81 unreviewed members contribute substantially and cannot be labelled biologically nonregulatory or nonfunctional. Therefore this screen narrows the interpretation of the annotated subset; it does not establish a complete regulatory-versus-effector balance.

| Prespecified role | Members in 99/57/53 | Contribution to99 | Contribution to57 | Contribution to53 |
|---|---|---:|---:|---:|
| enzyme | 1 / 1 / 1 | +0.004652 | +0.008081 | +0.008690 |
| extracellular_structure | 3 / 1 / 1 | +0.024687 | +0.025271 | +0.027178 |
| gene_expression_regulation | 6 / 4 / 4 | -0.125824 | +0.004802 | +0.005164 |
| receptor_or_ligand | 5 / 5 / 3 | +0.148310 | +0.257592 | +0.261857 |
| transport | 4 / 0 / 0 | -0.093947 | +0.000000 | +0.000000 |
| unknown_unreviewed_in_this_pass | 81 / 47 / 45 | +0.782240 | +0.269798 | +0.308206 |

Values are equal-mouse mean contributions in detection percentage points, always divided by the original module's 99/57/53 denominator. **Do not sum these rows:** Eya2 belongs to both gene-expression regulation and enzyme roles. The full [per-member/per-mouse table](../../../analysis/research/runs/A5_component_attribution_v1_20261103/member_contributions.tsv) retains every member, sign and module contribution; [unit-level expectations](../../../analysis/research/runs/A5_component_attribution_v1_20261103/unit_gene_expectations.tsv), [cell count primitives](../../../analysis/research/runs/A5_component_attribution_v1_20261103/cell_target_counts.tsv.gz), [support](../../../analysis/research/runs/A5_component_attribution_v1_20261103/unit_support.tsv) and [aggregate parity](../../../analysis/research/runs/A5_component_attribution_v1_20261103/aggregate_parity.tsv) support review. No new gene ranking, p-value or replacement positive module was used.

The complete [role table](../../../docs/research_reviews/2026-11-03-full-priority-screening/prerequisites/A5_ROLE_TABLE_V1.tsv) and [versioned UniProt source annotations](../../../docs/research_reviews/2026-11-03-full-priority-screening/prerequisites/A5_ROLE_SOURCES_V1.json) were fixed before member outcomes. Rbpjl remains putative; Zfp462 uses an explicit source synonym; source similarity-based annotations are disclosed. UniProt skill retrieval supplied metadata, not evidence of activity in the measured cells.

The biological decision is to avoid treating the positive fixed aggregate as a uniformly activated regulatory programme. RNA recruitment remains compatible with heterogeneous structural, transport, signaling and unreviewed contributions. No lineage, regulator activity, beneficial repair or mechanism follows. The earlier destination screen and unresolved GSE303646 replication are separate and unchanged. Independent coordinator review passed the complete unit/member/contribution reconstruction (9,522 checks; maximum error 5.55e-17).
