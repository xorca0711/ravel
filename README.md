# Ravel: Public Omics Reanalysis of Cellular States, Tissue Homeostasis and Disease

[![Repository checks](https://github.com/xorca0711/ravel/actions/workflows/repository-checks.yml/badge.svg)](https://github.com/xorca0711/ravel/actions/workflows/repository-checks.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)

Ravel combines critical reading of primary literature, reproduction of accessible
findings and reanalysis of public biological data. It investigates cellular states
and molecular programmes in tissue homeostasis, injury, repair, ageing and disease,
using unresolved findings to develop testable research questions.

The project began with lung single-cell and multiome studies. Its scope now
follows the papers and questions under investigation across relevant tissues,
organisms and experimental contexts. Analyses include single-cell and bulk RNA
sequencing, RNA–chromatin comparisons, and accessible spatial, imaging,
perturbation and clonal measurements. Each study retains its own biological
units, measured endpoints and interpretation limits.

Previously named `scRNA_seq`; the
[migration record](docs/migrations/2026-10-07-ravel/README.md) documents the rename
and preservation of historical evidence.

## Start here

| What you need | Where to start |
|---|---|
| Questions, biological rationale and proposed comparisons | [Illustrated question guide](docs/research_dossiers/literature_context_2026-10-03/README.md) · [Question register](RESEARCH_QUESTIONS.md) |
| Source papers, reading status and article analyses | [Research article roadmap](Research%20Article/README.md) |
| Datasets, biological units and eligibility | [Dataset inventory](docs/DATASETS.md) |
| Current results and remaining work | [Project state](PROGRESS.md) · [Remaining-work ledger](docs/research_dossiers/REMAINING_WORK.md) |
| Figures and their interpretation | [Question figures](RQ_Specified/FIGURES.md) · [Paper galleries](Research%20Article/README.md#figure-galleries) |
| Evidence grades, corrections and negative results | [Claim summary](docs/CLAIM_SUMMARY.md) · [Full register](CLAIMS.md) · [Negative results](docs/NEGATIVE_RESULTS.md) |
| Reproduction and research development | [Reproducibility](REPRODUCIBILITY.md) · [Research governance](docs/RESEARCH_GOVERNANCE.md) · [Documentation index](docs/README.md) |

## How it works

The research moves through six stages. Findings can revise an earlier question,
connect previously separate questions or close a branch that the evidence does
not support.

1. **Read the paper.** Examine its question, design, findings and unresolved issues;
   identify accessible data and source-specific limitations.
2. **Reanalyse eligible data.** Reproduce accessible findings and test defined
   comparisons with appropriate quality control, biological units and sensitivity checks.
3. **Develop a research question.** Connect published findings and repository
   observations through the [literature workflow](docs/LITERATURE_WORKFLOW.md).
   State the remaining gap, informative comparison and interpretation limit.
4. **Investigate the question.** Develop its plan in
   [RQ_Specified](RQ_Specified/README.md), qualify inputs, and freeze a versioned
   contract before running a new analysis. Retain prior outcome exposure and all results.
5. **Connect the evidence.** Assess recurring phenotypes, complementary measurements
   and differences across studies. Check shared samples and gene sets before
   interpreting agreement as independent replication or biological convergence.
6. **Evaluate the hypothesis.** Define predictions and contrary outcomes before
   confirmatory testing. Use eligible independent or perturbation, lineage and
   functional data; comparisons requiring new experiments remain proposed.

Different questions are at different stages. Completing an analysis can resolve a
measurement or data limitation while leaving the biological hypothesis open. The
[research architecture](docs/RESEARCH_ARCHITECTURE.md) explains the evidence layers,
and the [remaining-work ledger](docs/research_dossiers/REMAINING_WORK.md) records
current dependencies.

## How the research is organized

Paper packages own source context and study-specific analyses. The canonical
question register owns stable A-series identities, while question workspaces and
[dossiers](docs/research_dossiers/README.md) develop their evidence and next tests.
The research registry locates prospective contracts, execution receipts and
versioned outputs. Registration or successful execution does not imply scientific
acceptance; dated reports preserve earlier results and corrections.

## Datasets

The [inventory](docs/DATASETS.md) separates analysed data from feasibility inputs
and candidates that do not meet a particular comparison's requirements. Most
expression analyses use deposited counts; some reproduce deposited normalized
values. Contracts record exact inputs, inclusion rules and biological units.
Reused deposits and their companion assays remain shared evidence.

## Figure galleries by analysis branch

Question and paper galleries are linked above. The
[shared gallery](analysis/figures/rq/README.md) contains cross-question measurements
and designs. Captions identify units and limits; later corrections take precedence
over historical image titles.

## Try it yourself

From a clean clone, Python 3.12 can check the tracked evidence and local links
without downloading raw datasets or installing the scientific stack:

```bash
python analysis/scripts/validate_repository.py
python -m unittest discover -s analysis/tests -q
```

These checks cover artifact consistency and selected numerical contracts;
they do not reproduce every scientific result. Scientific reruns require the
inputs, dependencies and run-specific instructions in
[REPRODUCIBILITY.md](REPRODUCIBILITY.md). Completed evidence directories should
be preserved when running a new version.

## Repository map

```text
RESEARCH_QUESTIONS.md       canonical biological questions and readiness
Research Article/           source studies, paper analyses and galleries
RQ_Specified/               question-specific plans, scripts and results
analysis/                   shared code, resources, corrections and figures
analysis/research/          question registry, contracts and execution receipts
docs/DATASETS.md            dataset roles, units and eligibility map
docs/portfolio_extensions/  grouped reviews, extension results and synthesis
docs/audits/                reviews, corrections and evidence checks
CLAIMS.md                   historical graded evidence register
PROGRESS.md                 current state and handoff
DEVELOPMENT.md              responsibility and decision history
AI_CONTEXT.md               working context for agents
```

The [structure contract](docs/REPOSITORY_STRUCTURE.md) defines ownership and
identifier scope. [References](REFERENCES.md) and study reports provide source
citations. [DEVELOPMENT.md](DEVELOPMENT.md) records AI assistance, responsibility
and rejected or revised proposals.

## Still open

Open requirements differ by question: independent biological replication,
linked early/later measurements, qualified source metadata or a direct functional
endpoint. Some repair comparisons lack a common functional outcome. Age,
genotype, processing and cell mixtures can remain alternative explanations.
Molecular scores alone do not establish fate or causality. Negative results,
stopped branches and corrections remain part of the evidence record.

## Licence

Code and original written material are copyright 2026 Xorca; no reuse licence
is granted. See [LICENSE](LICENSE). Source papers and public datasets retain
their respective authors' and publishers' rights.
