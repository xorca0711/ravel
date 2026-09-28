# Integrative reanalysis of public lung single-cell and multiome data

[![Repository checks](https://github.com/xorca0711/scRNA_seq/actions/workflows/repository-checks.yml/badge.svg)](https://github.com/xorca0711/scRNA_seq/actions/workflows/repository-checks.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)

This project reanalyses public lung single-cell RNA, multiome and complementary
experimental data to develop and test questions about injury, repair and
persistent remodelling. Its organizing question is:

> Which epithelial and immune-state programmes distinguish productive lung
> repair from persistent remodelling after injury?

The work combines atlas reconstruction, programme scoring, sample-level
comparisons and cross-study analysis. It separates molecular associations from
independently measured lineage, functional and signalling outcomes. A completed
analysis may resolve a data limitation while leaving the biological question open.

## Start here

| To explore | Start with |
|---|---|
| Biological questions and the evidence needed to answer them | [Research-question register](RESEARCH_QUESTIONS.md) and [question workspaces](RQ_Specified/README.md) |
| Source studies, reading status and paper-specific analyses | [Research article roadmap](Research%20Article/README.md) |
| Datasets, their roles, biological units and eligibility limits | [Dataset inventory](docs/DATASETS.md) |
| Current results, remaining gaps and execution priorities | [Current project state](PROGRESS.md) and [research execution roadmap](docs/RESEARCH_ROADMAP.md) |
| Figures and the reports that interpret them | [Question figure index](RQ_Specified/FIGURES.md) and [paper galleries](Research%20Article/README.md#figure-galleries) |
| Evidence grades, corrections and negative results | [Claim register](CLAIMS.md), [generated summary](docs/CLAIM_SUMMARY.md) and [negative-results index](NEGATIVE_RESULTS.md) |
| Reproduce the work or inspect analytical decisions | [Reproducibility guide](REPRODUCIBILITY.md), [documentation index](docs/README.md) and [decision record](DEVELOPMENT.md) |

## How the research is organized

**Paper studies** retain source context, deposited-data analyses and their
figures in `Research Article/`. Reading a paper, processing its deposit and
accepting a scientific interpretation are recorded separately.

**Research questions** have stable identifiers in `RESEARCH_QUESTIONS.md`.
Their plans, contracts, scripts and results live in `RQ_Specified/`. The current
register contains A0–A18 and the enabling source-identity question A12-S1;
registration does not imply validation. Shared measurements and figures have
explicit links to the questions they support.

**Execution and review** are recorded in dated reports. The latest
[gap-fill execution](docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md) links
completed corrections, cohort eligibility decisions and the remaining input
for every question. Earlier runs remain available as historical evidence.
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
alternative explanations. The [execution ledger](docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md)
names the next input or decision for each question, including stopped and
inconclusive branches.

## Licence

Code and original written material are copyright 2026 Xorca; no reuse licence
is granted. See [LICENSE](LICENSE). Source papers and public datasets retain
their respective authors' and publishers' rights.
