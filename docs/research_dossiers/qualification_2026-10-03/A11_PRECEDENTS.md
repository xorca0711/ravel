# A11: bounded primary-source comparison

The previous review left lesion-specific novelty incomplete. This follow-up checks two direct precedents and the repository's exact signature provenance. It narrows the possible contribution; it does not certify that no other paper has tested it.

| Source and access | Established precedent | Consequence for A11 |
|---|---|---|
| [Marjanovic et al., Cancer Cell 2020](https://pubmed.ncbi.nlm.nih.gov/32707077/), primary abstract and indexed full-text findings; DOI 10.1016/j.ccell.2020.06.012 | HPCS-associated plasticity, tumorigenicity and drug resistance were reported in lung cancer. | Neither a lesion association nor generic HPCS function is a new contribution by itself. |
| [Chan et al., Nature 2026](https://www.nature.com/articles/s41586-025-09985-x), full publisher text; Abstract, lineage-tracing results and cross-tissue HPCS findings | Functional lineage/ablation work supports the state in the studied tumor model; an HPCS-like programme is also reported in regenerating epithelia. | Regeneration overlap is an established precedent, not an unanticipated discovery or sufficient proof of cancer specificity. |

The locally used `HPCS_author_top100` is an author-notebook Cluster 5 list, pinned to `common_files/clusters_cell2020.csv` at commit `b52d53c984e21d3bb3a163041fdb3f56b54c19c0`; see the [module specification](../../../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u6_specificity/module_specification.json). The [shared component contract](../../../RQ_Specified/A5_A11_shared_component_contract/config/shared_component.json) partitions source lists and excludes operational labeling genes. A reduced score is not interchangeable with a lineage-traced HPCS population or the source paper's functional experiments.

**Possible contribution:** determine whether the exact residual lesion-associated component adds reproducible information beyond shared epithelial remodeling under a defensible biological comparison. Only then could a specific functional branch be justified. The [current A11 report](../../../RQ_Specified/A11_lesion_programme_addition/README.md) retains the lesion association, unresolved beyond-shared criterion and limited acute-injury falsification. No existing result changes here, and no pathogen-related numerical work was performed.

**Qualification decision:** do not claim first discovery of HPCS plasticity, regeneration overlap or general tumor relevance. Any follow-up must compare the exact component/endpoint against prior work, recover independent units and use a functionally meaningful outcome if making a mechanism claim. Broader literature novelty and the component's causal role remain unresolved.
