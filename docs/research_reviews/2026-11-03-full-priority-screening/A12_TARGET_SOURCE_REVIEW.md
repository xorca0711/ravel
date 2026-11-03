# A12: source rationale for five added context transcripts

3 November 2026, Asia/Seoul. Pre-run rationale review, not expression extraction
or a new mechanistic claim. The five original index genes and its algebra remain
unchanged. These five additional targets are a selected context panel, not a
complete IL-1 pathway or a new response score.

## Sources actually inspected

| Source/version | Inspected location and contribution |
|---|---|
| [De et al., *Mechanism of dysfunction of human variants of the IRAK4 kinase and a role for its kinase activity in interleukin-1 receptor signaling*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6166721/), JBC, online 16 August 2018; DOI 10.1074/jbc.RA118.003831 | HTML Results/legends Figs. 4–6 and model Fig. 9. Human dermal-fibroblast experiments distinguish signaling-complex assembly, kinase function and cytokine output. This supports MYD88/IRAK1/IRAK4 as selected signaling components and explains why their RNA abundance is not an activation measurement. It is not a demonstration in the repository's candidate alveolar cells. |
| [Wang et al., *NF-κB memory coordinates transcriptional responses to dynamic inflammatory stimuli*](https://doi.org/10.1016/j.celrep.2022.111159), Cell Reports, 16 August 2022; [author-hosted article PDF](https://taylab.uchicago.edu/uploads/9/1/8/0/91804060/PIIS2211124722009688.pdf) | PDF Results/legends Figs. 5–6, especially 6E, and model-system entry: NIH3T3 mouse fibroblasts. Nfkbia/Tnfaip3 transcripts differ across stimuli and timing; signaling dynamics and transcript snapshots are distinct measurements. This supports their feedback-associated annotation but supplies neither an IL-1-specific signature nor an epithelial feedback-strength calibration. No numerical reanalysis or transfer of the temporal model is proposed. |

These are primary-source role precedents, not independent validations of A12.
The RNA-only limit also agrees with the repository's existing [England evidence
review](../../../Research%20Article/gate2_C2_england_2025/EVIDENCE_REVIEW.md#il1r1-and-nf-kb),
which explicitly separates inducible Nfkbia RNA from measured feedback competence.

## Fixed target-to-role mapping

| Human symbol | Descriptive label | Source | Prohibited inference from this RNA screen |
|---|---|---|---|
| MYD88 | Adaptor-component transcript | De, Figs. 5/9 | Receptor engagement or complex assembly |
| IRAK1 | Signaling-component transcript | De, Figs. 5/9 | Kinase activity or a unique IL-1 input |
| IRAK4 | Signaling-component transcript | De, Figs. 4–6/9 | Active protein abundance or signaling strength |
| NFKBIA | Feedback-associated transcript | Wang, Fig. 6E | Effective inhibition, intact feedback or absence of stimulation |
| TNFAIP3 | Feedback-associated transcript | Wang, Fig. 6E | Effective inhibition, intact feedback or absence of stimulation |

No signed weight is assigned to the added genes. Higher feedback-associated RNA
may accompany stronger inflammatory input; it cannot be given an automatic
anti-inflammatory meaning. No group is labeled activated or inhibited from
these five values. Cross-sectional tissue contrasts cannot recover exposure
order or pathway dynamics.

## Remaining pre-run specification checks

The technical chat still owns exact feature IDs, original count/unit parity,
and overlap against the fixed response definition. If NFKBIA/TNFAIP3 overlap
that response, flag the overlap and do not use their concordance as independent
response evidence. Preserve all five original index contributions with their
existing weights; no refit, expanded index or shared-gene correlation. This
source review resolves target-role rationale, not those implementation checks.

## Search and access record

Actual web queries on 3 November 2026, without date/domain filters:

- `MyD88 IRAK1 IRAK4 IL-1 signaling primary study receptor complex 2010`
- `NFKBIA TNFAIP3 negative feedback IL-1 NF-kappaB primary research A20 IkappaB alpha`
- `"NF-κB memory coordinates transcriptional responses" "PMC"`
- `"NFKBIA" "IL-1" "2025" "feedback" lung epithelium`

The recent lung-focused query recovered the already known England paper; the
current local evidence review was reused. Reviews were discovery aids only.
PMC full text worked for De; Wang's PMC page and a separate 2017 IRAK paper
returned browser challenges. Wang's author-hosted article PDF supplied the
specified Results/legend and model-system reads. Supplements and source values
were not audited. No systematic citation census or correction-database search
was performed; this is sufficient for the bounded role annotation, not novelty
clearance or a new comprehensive pathway review.
