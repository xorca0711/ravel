# A12: original IL-1 recipient components

3 November 2026. Reviewed freeze `709b446`; [receipt](../../../analysis/research/runs/A12_il1_components_v1_20261103/receipt.json) verifies. The original twelve patients contribute 24 patient/recipient pairs, not 24 donors. All 48 full-library totals, 480 scalar log values and 24 original index reconstructions passed; maximum index error 1.11e-15. No prediction refit, new index or test was performed.

The AT2 candidate-label mean pattern is mixed: IL1RAP increases while IL1R1 decreases; IL1R2 and SIGIRR decreases contribute positively to the original signed index. IL1RN increases slightly and contributes negatively. Thus a higher combined index must not be read as every receptor component increasing or every inhibitory component decreasing. The fibroblast receptor/accessory mean directions differ, and its original unfavorable predictive result remains unchanged.

| Gene | AT2 paired delta | Fibroblast paired delta | AT2 old-index contribution | Fibroblast old-index contribution | In old response |
|---|---:|---:|---:|---:|---|
| IL1R1 | -0.1052 | -0.0988 | -0.0526 | -0.0494 | False |
| IL1RAP | +0.3553 | -0.2363 | +0.1777 | -0.1181 | False |
| IL1R2 | -0.3058 | -0.2416 | +0.1019 | +0.0805 | False |
| IL1RN | +0.0484 | +0.3840 | -0.0161 | -0.1280 | False |
| SIGIRR | -0.3266 | -0.4524 | +0.1089 | +0.1508 | False |
| MYD88 | +0.5418 | -0.0374 | +0.0000 | +0.0000 | False |
| IRAK1 | +0.7205 | +0.1141 | +0.0000 | +0.0000 | False |
| IRAK4 | +0.0817 | +0.0916 | +0.0000 | +0.0000 | False |
| NFKBIA | -0.1006 | +0.1477 | +0.0000 | +0.0000 | True |
| TNFAIP3 | +0.0933 | +0.3660 | +0.0000 | +0.0000 | True |

Deltas are equal-patient LUAD-minus-normal log2(1+CPM), computed from summed unit counts and each full gene-library denominator. The first five weights remain +1/2,+1/2,-1/3,-1/3,-1/3; added genes have no index weights. Individual patient directions/values remain in the [complete paired table](../../../analysis/research/runs/A12_il1_components_v1_20261103/paired_gene_components.tsv), with [all count primitives](../../../analysis/research/runs/A12_il1_components_v1_20261103/unit_gene_primitives.tsv) and [original-index parity](../../../analysis/research/runs/A12_il1_components_v1_20261103/original_index_parity.tsv).

MYD88/IRAK1/IRAK4 are signaling-component RNA context, not activation assays. NFKBIA/TNFAIP3 are feedback-associated RNA and overlap the old response; their concordance or discordance is not independent response evidence, effective inhibition or an IL-1-specific signal. No correlation with that response was calculated. Healthy-reference candidate-label uncertainty, tissue composition and 52–72% unassigned IL1B source remain unresolved. The screen clarifies the original index but does not attribute its predictive gain to a causal branch or demonstrate recipient competence. The ERBB sorted-library reference is a separate result and unchanged. Independent coordinator review passed 1,004 library, component and index checks (maximum error 1.78e-15).
