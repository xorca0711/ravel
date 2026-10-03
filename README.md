# Integrative reanalysis of public lung single-cell and multiome data

[![Repository checks](https://github.com/xorca0711/scRNA_seq/actions/workflows/repository-checks.yml/badge.svg)](https://github.com/xorca0711/scRNA_seq/actions/workflows/repository-checks.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)

This repository develops testable biological hypotheses through critical reading
of research articles and reanalysis of public lung single-cell RNA, multiome and
complementary experimental data. The aim is to connect observations across studies,
identify recurring molecular phenotypes and explain which differences could matter
for epithelial plasticity, injury repair and persistent tissue remodelling.

Its organizing biological question is:

> Which epithelial and immune-state programmes distinguish productive lung
> repair from persistent remodelling after injury?

The work connects source-paper evidence, question-specific analyses and hypothesis
tests in a traceable research record. Molecular associations, independently
measured outcomes and proposed mechanisms retain their own evidence requirements.
Negative and inconclusive results help narrow the next question.

## How it works

The research moves through six stages. Findings can revise an earlier question,
connect previously separate questions or close a branch that the evidence does
not support.

1. **Read research articles.** Examine the biological question, experimental
   design, main findings and unresolved issues. Record study notes and the public
   data available for analysis in the [research article roadmap](Research%20Article/README.md).
2. **Analyse the paper's data.** Reproduce accessible findings and investigate
   specific observations through atlas reconstruction, programme scoring,
   sample-level comparisons and sensitivity checks. Keep the resulting evidence
   beside its source study in `Research Article/`.
3. **Derive research questions.** Use the [literature workflow](docs/LITERATURE_WORKFLOW.md)
   to connect recent and foundational primary findings with the reproduced result.
   Turn unexplained patterns, conflicting evidence
   and limitations into explicit biological questions. The
   [research-question register](RESEARCH_QUESTIONS.md) records each question's
   rationale, existing evidence and next discriminating test.
4. **Investigate each question.** Develop its scope and analysis plan, assess
   suitable datasets, and run eligible comparisons in [RQ_Specified](RQ_Specified/README.md).
   Record results, competing explanations and remaining gaps so that the
   hypothesis becomes more specific as evidence accumulates.
5. **Connect questions and develop hypotheses.** Compare findings across questions
   for recurring phenotypes, complementary measurements or informative differences.
   Where the evidence supports a joint analysis, define a shared hypothesis and
   measurable predictions. Account for overlapping gene sets and reused samples
   before treating agreement as biological convergence or independent replication.
6. **Test the hypotheses.** Specify the comparison, biological unit, alternatives
   and results that would count against a hypothesis before confirmatory testing.
   Evaluate predictions using eligible independent datasets or available
   perturbation, lineage and functional measurements. Distinguish supported,
   unsupported and unresolved predictions; tests requiring new experimental data
   remain proposed.

Different questions are at different stages. Completing an analysis can resolve a
measurement or data limitation while leaving the biological hypothesis open. The
[research architecture](docs/RESEARCH_ARCHITECTURE.md) explains the evidence layers,
and the [remaining-work ledger](docs/research_dossiers/REMAINING_WORK.md) records
current dependencies. The [September roadmap](docs/RESEARCH_ROADMAP.md) preserves
the historical planning context.

## Start here

| To explore | Start with |
|---|---|
| Understand each hypothesis, rival and readout visually | [Illustrated RQ context guide](docs/research_dossiers/literature_context_2026-10-03/README.md) |
| Biological questions and the evidence needed to answer them | [Research-question register](RESEARCH_QUESTIONS.md) and [question workspaces](RQ_Specified/README.md) |
| Source studies, reading status and paper-specific analyses | [Research article roadmap](Research%20Article/README.md) |
| Datasets, their roles, biological units and eligibility limits | [Dataset inventory](docs/DATASETS.md) |
| Current results, remaining gaps and next decisions | [Current project state](PROGRESS.md) and [remaining-work ledger](docs/research_dossiers/REMAINING_WORK.md) |
| Figures and the reports that interpret them | [Question figure index](RQ_Specified/FIGURES.md) and [paper galleries](Research%20Article/README.md#figure-galleries) |
| Evidence grades, corrections and negative results | [Claim register](CLAIMS.md), [generated summary](docs/CLAIM_SUMMARY.md) and [negative-results index](NEGATIVE_RESULTS.md) |
| Reproduce the work or inspect analytical decisions | [Reproducibility guide](REPRODUCIBILITY.md), [documentation index](docs/README.md) and [decision record](DEVELOPMENT.md) |
| Develop a research question or contribute an analysis | [Conditional packages](docs/research_dossiers/packages_2026-10-03/README.md), [evidence dossiers](docs/research_dossiers/README.md) and [research governance](docs/RESEARCH_GOVERNANCE.md) |

## How the research is organized

**Paper studies** retain source context, deposited-data analyses and their
figures in `Research Article/`. Reading a paper, processing its deposit and
accepting a scientific interpretation are recorded separately.

**Research questions** have stable identifiers in `RESEARCH_QUESTIONS.md`.
Their plans, contracts, scripts and results live in `RQ_Specified/`. The current
register contains A0–A27 and the enabling source-identity question A12-S1;
registration does not imply validation. Shared measurements and figures have
explicit links to the questions they support.

**Execution and review** are recorded in dated reports. The
[current project state](PROGRESS.md) links completed work, remaining inputs
and open decisions. Earlier runs remain available as historical evidence.
The [research architecture](docs/RESEARCH_ARCHITECTURE.md) explains how source
evidence, measurements, interpretations and next tests connect.

## Datasets

The [dataset inventory](docs/DATASETS.md) distinguishes analysed expression,
chromatin, imaging and clone data from feasibility-only inputs and candidates
that fail a particular question's gates. Each entry links to its current use
and limitations. Shared deposits are reused evidence, not independent cohorts.

Most expression analyses start from deposited counts; some source reproductions
use deposited normalized values. Cells, libraries, pooled animals, donors and
culture preparations are different units. Exact inclusion rules, input hashes
and sample counts belong to each run's contract and provenance record.

## Figure galleries by analysis branch

Use the [question figure index](RQ_Specified/FIGURES.md) for question-specific
outputs, the [shared question gallery](analysis/figures/rq/README.md) for shared
measurements and designs, and the [paper gallery index](Research%20Article/README.md#figure-galleries)
for study-level plots. Captions identify units and interpretation limits.
Historical image titles do not override later corrections.

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
RESEARCH_QUESTIONS.md    canonical biological questions and readiness
Research Article/       source studies, paper analyses and galleries
RQ_Specified/           question-specific plans, scripts and results
analysis/               shared code, resources, corrections and figures
docs/DATASETS.md        dataset roles, units and eligibility map
docs/roadmap_runs/      dated execution and remaining-input records
docs/audits/            reviews, corrections and evidence checks
CLAIMS.md              historical graded evidence register
PROGRESS.md            current state and handoff
DEVELOPMENT.md         responsibility and decision history
AI_CONTEXT.md          working context for agents
```

The [structure contract](docs/REPOSITORY_STRUCTURE.md) defines ownership and
identifier scope. [References](REFERENCES.md) and linked study reports supply
source citations. The [portfolio summary](docs/PORTFOLIO_SUMMARY.md) and
[portfolio guide](docs/PORTFOLIO.md) offer selected examples; they are not the
complete current research index.

## Still open

The collection lacks a common functional repair outcome, and several
comparisons lack independent biological replication or linked measurements.
Age, genotype, processing, cell mixtures and state definitions remain important
alternative explanations. The [current project state](PROGRESS.md)
links the remaining inputs and decisions, including stopped and inconclusive
branches.

## Licence

Code and original written material are copyright 2026 Xorca; no reuse licence
is granted. See [LICENSE](LICENSE). Source papers and public datasets retain
their respective authors' and publishers' rights.
