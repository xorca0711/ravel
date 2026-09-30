# A19-A21 PR delivery and question wording review

30 September 2026. [PR #123](https://github.com/xorca0711/scRNA_seq/pull/123)
contains the reviewed A19-A21 exploratory packages and the universal README fix.
The owner subsequently requested updated one-line hypothesis questions using the
existing question-folder hierarchy.

Current question wording is synchronized across each folder README, PLAN and
question contract, the canonical register and the question index. The README
uses the organizing-biological-question format found in other RQ folders.
A20's focused-design question is synchronized as well. Previous document bytes
and manifests are archived under each folder's metadata/history/one_line_refinement_20260930.
[Revision details](question_revision.json) preserve previous titles, current
questions and unchanged primary outcomes. Scientific results and frozen analysis
contracts are unchanged; hypotheses remain untested.

The first GitHub CI failed on 16 figure links because a global PDF ignore rule
excluded locally reviewed exports from the initial commit. Narrow question-figure
exceptions now allow these existing PDFs to be committed without admitting raw
source caches. This corrects delivery, not scientific content. A final index
check verifies that every current package-manifest file is tracked and byte-correct.

See [delivery checks](checks.json) for the local documentation and packaging
validation. The current hosted CI state is reported on PR #123; earlier run
records retain their historical state and scope. No merge is authorized here.
