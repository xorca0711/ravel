# Originating review of the Saxton program description

1 November 2026. **Pass for the stated finite-library description and technical
integration; scientific acceptance remains unassessed.** The existing technical
chat `01a191d5-e0e2-70d2-92e0-97272f85ce11` delivered commit
`caf4dd98e8884b9f12953af9d0de2556ea33d6d0`. It includes the originating plan
`07c8752` and the pre-execution v2 freeze `404d23673194abbb388668a2aa74e2ff09399579`.
Parent integration uses `codex/saxton-program-reassessment-20261101` against
fresh main `51d3b930b3805c616e67e414390ecf060647d090`.

[Question](README.md) · [Results](RESULTS.md) · [Figures](FIGURES.md) ·
[Technical validation](VALIDATION.md) · [Exact current holds](../COMPLETION_LEDGER.md).

## What was independently checked

The originating reviewer read the production normalization, annotation, contrast,
amplitude, summary and plotting code before execution. A separate scratch
verifier imported no production code and reread the raw count/FPKM sources.
It passed all 31 contract/input/code/output bindings, every one of 35,275 primary
gene rows, the fixed 14,483-row eligibility set and 14,266-row background,
all 21 scale/view cases, 210 membership summaries, overlaps and omission ranges.
The independently frozen technical verifier provides a separate reproducible
[verification implementation](scripts/verify_v1.py); its checks and results are
recorded in [validation](VALIDATION.md#numerical-and-visual-verification).

TMM transformations were checked against the recorded factors, full source
denominators, effective library sizes, package version and normalization
constraints. Neither verifier independently reimplements edgeR's TMM algorithm.
The technical known-answer synthetic test and official edgeR execution are
additional checks, not biological replication. No biological analysis was
rerun for parent documentation changes.

All three actual PNGs were inspected individually. Labels, color bars, source
units, negative direct contrasts, background coefficient and membership counts
are readable. The wide three-target sensitivity is visible. Captions distinguish
observed omission ranges from uncertainty intervals and RNA target values from
qPCR measurements. No post-run figure rewrite was needed.

## Interpretation review

The selected IFN panel's primary direct median is -1.345 versus -0.459 for the
selected tissue-protection panel. Both broad IFN sets have median -0.163 and
share 70 eligible genes; their matching medians are not independent confirmation.
The tissue-protection panel's positive amplitude residual (+0.278) coexists with
its negative direct contrast. A positive residual means above the chosen global
reference, not preserved tissue protection. The source's anti-inflammatory panel
also has a negative residual, so its category names are not a clean causal split.

The Reg3b/Reg3g/Muc1 subset's residual changes sign across omissions on all three
scales. This unfavorable result remains. The global coefficient near 0.60 is not
a fraction of response explained, a causal parameter or proof that bulk
composition and global attenuation have been excluded. All comparisons reuse six
libraries with unverified animal/preparation identities. These findings qualify
the extent and stability of the published transcription pattern; they do not
establish STAT1/STAT3 activity, equivalence, tissue function, persistence or novelty.

## Preservation and actual failures

The first registration attempt failed because the membership configuration was
bound as an input but not as a changed scientific execution dependency. V2 added
the required binding and verifier before any real endpoints were calculated.
Methods and production code were unchanged; no gate was weakened.

The first frozen, unexecuted v1 contract was temporarily newline-normalized.
Review required restoring its exact original bytes. Independent Git tree checks
confirmed the original `ae4a3b4` blob and final handoff blob are both
`73f9c835a32c3acdbe589628eb882a3be0850e2e`; restored SHA-256 is
`0c47c9873e48a06c6f650e6840e0a6372928784de5846e75990ee3b037a2ac47`.
V1 is not a v2 receipt hash dependency. The executed v2 contract, receipt and
outputs were not changed. V2's amendment reason preserves the earlier chronology;
the later restoration is recorded separately in VALIDATION.

Three exact paths retain whitespace exceptions: the original v1 CRLF contract
and the immutable `tmm_stdout.log`/`tmm_stderr.log` captures with doubled Windows
line endings. Their contents and hashes remain intact; numerical parsing passed.
All other changed files must pass the normal whitespace check. Root attributes,
validators, archived analyses and canonical RQs are unchanged.

The synthetic suite's initial temp-file PermissionError was resolved with
approved filesystem access. It was not a content restriction. The two original
generic service refusals remain historical evidence with no triggering job
identified. **No current content refusal occurred.** The current bounded job
assessment retained the full paper context and used the existing technical chat.

## Integration validation

Technical handoff: seven targeted synthetic tests; 158 shared tests with two
expected Windows symlink skips; 12,911 repository checks; archive/provenance
checks and the base-aware research gate all passed against `51d3b93`.
The combined parent documentation/registry/navigation tree passed **12,959
repository checks** and `research_gate.py check --base origin/main` with
`ok=true` and no errors against the same freshly fetched base. Whitespace checks
passed outside the three exact preserved artifacts above. Scope inspection found
no changes to root attributes, analysis infrastructure, governance or canonical
RQ folders. Numerical tests and biological execution were not repeated after
documentation-only integration. Human retain/reject decisions and claim grades
remain untouched.
