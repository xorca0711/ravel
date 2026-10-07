# Development and scientific ownership

This project was developed through an AI-assisted research workflow. I
directed the scientific design, dataset selection, analytical constraints,
validation standards, and biological interpretation; Claude Code assisted
extensively with implementation, execution, debugging, and documentation. AI
assistance is intentionally visible in the git history, the
`Co-Authored-By` trailers are disclosure, and nothing has been rewritten to
hide them.

This page is for human readers. The machine-oriented counterpart, repository
rules, environment constraints, and pitfalls a future AI session must not
violate, is [`AI_CONTEXT.md`](AI_CONTEXT.md).

## Figure presentation audit, 29 September 2026

The user requested completion of PR #118 after review of merged PR #117. Codex coordinated
three bounded figure reviews and integrated saved-table presentation corrections. The
[audit](docs/FIGURE_CLAIM_CORRECTIONS_2026-09-29.md) records decisions, coverage depth and
remaining reproduction inputs. No new scientific model fit or raw-RNA scoring was performed in this presentation pass; the changes do not promote biological claims.

## Who decided what

| Responsibility | Primary authority |
|---|---|
| Scientific question and dataset selection | Me |
| Experimental-design interpretation (cohorts, confounds, sort ratios) | Me |
| Analytical constraints and validation criteria | Me |
| Biological interpretation of results | Me |
| Implementation and refactoring | AI-assisted |
| Execution of computational runs | AI-assisted |
| Figures, tables, and report generation | AI-assisted |
| Review of intermediate and final outputs | Me |
| Retain / revise / reject decision on every result | Me |
| Structuring Nabhan 2026 after reading, including article/supplement/Notion synthesis, existing A10/A2 reuse and eight extension questions | Me (instruction 2026-10-01, corrected folder year to 2026); Codex source review, schema intake and pipeline scaffold. No new biological fit or scientific acceptance decision; proposed analysis contracts remain reviewable |
| Structuring Wagner 2021 after owner reading, with source reproduction and six article-local branches | Me (instruction 4 October 2026, including folder name and use of handmade notes); Codex source review and proposed structure. No numerical run, global RQ allocation or scientific acceptance |
| Literature extraction into study notes and reviewable configs (`Research Article/`) | AI-assisted; my review pending |
| Focused reproductions of the source paper's phase and myeloid claims (`phase_timecourse/`, `myeloid_focus/`) | AI-assisted, rules frozen before each run; my review pending |
| Repository framing, and what is displaced as established elsewhere | Me (instruction 2026-09-10); AI-assisted execution |
| Reading the Cardoso 2026 deposit in gates, and stopping Gate 1 when it failed (`Research Article/gate2_05_cardoso_2026/`) | Me (instruction and gate design 2026-09-12); AI-assisted execution, rules frozen before each run; my review pending |
| Relaxing the displaced-material rule for the reference-aligned primary-marker panels (PR #12) | Me (decision 2026-09-13, against the agent's recommendation to hold them back); the agent had preserved them on a branch rather than reverting them, and flagged both the displaced-material rule and the non-validated palette; the palette is still unaddressed |
| Pre-registering the post hoc Fst and Runx2 lead and running it (trial C9) | Me (instruction 2026-09-13); AI-assisted execution. The agent named the untestable half before running, reported that the effect size its own trial computed is not usable, and disclosed that T1 and T5 were not composable; my review pending on rows C65 to C72 |
| Entering roadmap paper 2 (Choi 2020) on 2026-09-13: study note, extract, trial D0 | **Agent-proposed, approved by a one-word "proceed" on an agent-written list, not a specific instruction of mine** (corrected 2026-09-15). Later that day I said to leave the paper until I had read it. On 2026-09-15 I REJECTED the AI-written study note (withdrawn; kept in git history at PR #19), relocated trial D0 and its extract under the Cardoso folder as an extension, and reserved the paper-2 folder for after my own reading. Rows C58 to C64 stand, review pending |
| Re-entering roadmap paper 2 (Choi 2020) on 2026-09-15: study note, extract, trials D1 to D7 and the corrected passes D2b and D5b | Me (instruction 2026-09-15, after reading the paper: list the possible analyses, structure the pipeline, reproduce the paper's result first, then attack its claims, proceed until nothing remains; the backbone check trial by trial; the pull request and merge); AI-assisted execution with every rule frozen before its object was opened. The agent disclosed the Sftpc-clause defect in its own rule twice and left the thresholds where they were; my review pending on rows C85 to C104 |
| Revising the reading order (Gate 2 branches 2C, 2N, 2W; papers 12 to 16 and methods references M1 to M7 added) | Me (instruction 2026-09-15); AI-assisted execution with every identifier verified against PubMed |
| Promoting the generic deposit readers out of the Cardoso helper module into the shared one | Agent proposal, my approval implied by the instruction to proceed; a gate1 folder importing from a gate2 folder was the wrong dependency direction. Verified by importing all 19 Cardoso trial modules and re-running two trials to identical results; cardoso_utils re-exports so nothing written against it changed |
| Choosing the three follow-up questions off the agent's ranked list, and accepting three negative answers plus two disclosed rule defects (trials E6, C7, C8) | Me (selection 2026-09-13); AI-assisted execution with readings frozen before the data were opened; the agent reported the margin that refuses its own C7 answer and the zero-inflation that voids its own C8 mixture test; my review pending on rows C49 to C57 |
| Extending the Hbegf lead into four public datasets once the deposit was exhausted, and accepting a frozen rule's refutation of my own agent's best lead (trials E1 to E4) | Me (instruction 2026-09-13, including the condition that the extensions run only if the first did not refute); AI-assisted execution, readings frozen before the matrices were opened; my review pending on rows C37 to C48 and on the weakening of C29 |
| Opening two branches of paper 2 on other laboratories' multiome deposits (2026-09-20): the transitional state in chromatin, and the paper's own closing Axin2 and Il1r1 question | Me (instruction 2026-09-20); AI-assisted execution. The agent refused five times before producing a statistic and retracted the one reading it produced; I corrected Route C as out of focus and directed Route A to run. Rows C116 to C150, review pending |
| Auditing rows C116 to C150 with eight adversaries and independent verifiers, and accepting all 45 confirmed findings | Me (instruction 2026-09-20: "launch a multi-agent attack workflow to testify all the claims made"); AI-assisted execution. The agent's own register prose was the thing found wrong; corrections read from tables, trial M4 added, rows C151 to C154; review pending |
| Rewriting the root README around a ledger drawn from the register, listing all fifteen opened deposits, and writing RESEARCH_QUESTIONS.md as the question-first entry point | Me (instruction 2026-09-20, including the choice to drop the Leiden UMAP and to organise by question rather than by trial); AI-assisted execution. A first draft cited seven wrong register rows, caught by printing each cited row; a second adversarial workflow checked the landed text. My retain or reject on the question-first framing pending |
| Restating the repository's purpose as hypothesis generation and keeping personal planning out of every tracked file (decision 27) | Me (instruction 2026-09-22); AI-assisted rewording, file by file, with decisions, statuses and numbers unchanged |
| Retain or reject on the gene set enrichment rows C155 to C161 (decision 28) | Me, row by row (2026-09-22); the assistant set out the evidence from the tracked artefacts and proposed wording |
| The A1 figure: adding the per-nucleus promoter violin back beside the detection-at-budget heatmap, with the ATAC depth behind it (decision 29) | Me (2026-09-22), choosing among keep, add back beside, and restore; the assistant computed the depth from the cached object and redrew the figure with script 16 |
| Retain or reject on the Choi 2020 branch rows C116 to C154 (decision 30) | Me, row by row in four themed groups (2026-09-22); the assistant checked the cited artefacts by script and set out the evidence |
| Choosing W1 as the next analysis, narrowing it to alveolar macrophages, and installing pydeseq2 (decision 31) | Me (2026-09-22); the assistant proposed the narrowing, wrote and committed the pre-registration before any count was read, and chose the genotype exclusion, the sex-gene gate and CAMERA, all pending my review |
| Selecting the next question-specific analysis, and the A5 and A11 shared component contract (decision 37) | Me (2026-09-25). I REJECTED the assistant's first recommendation, A6, as artifact-adjacent, then chose to join A5 and A11 through a shared contract in its own folder and branch, and authorized execution. The assistant selected the developmental source, wrote and committed the partition rule before any intersection, and corrected its own coverage gate and one dataset universe. At stage 4 I retained the frozen modules and chose the Kim 2020 test for A11, an injury-data audit for A5 and the register update, each the assistant's recommended option |

AI execution never meant automatic acceptance. Results were reviewed between
sessions, and several were sent back: one finding was refuted and rewritten
(decision 6 below), one annotation approach was demoted after it failed
validation (decision 5), and documentation that overstated what had run was
re-scoped rather than left to stand.

## The decisions that shaped the analysis

Abstract claims of supervision are cheap; these are the concrete decisions,
each verifiable in the repository's artefacts.

**1 · Raw data determines the workflow.** The governing brief forbade
assuming anything about the deposited data, format, species, metadata,
gene-space compatibility, reporter features, and QC thresholds all had to be
detected, not presumed. This constraint is why the pipeline found things a
template would have missed: the `SiteA`/`SiteB` lineage-reporter contigs
hiding in the mouse gene space, the human sample quantified against a
different annotation build (forcing an Ensembl-ID intersection), and
non-unique human gene symbols.

**2 · Mouse: no batch correction, because the design forbids it.** Every
mouse sample belongs to exactly one experimental group, so sample identity
and the influenza time course are the same variable, "correcting" on sample
would delete the biology under study. I had the question reframed to one that
is purely technical: do replicate animals *within* a group fail to mix?
Measured within-group replicate enrichment was 1.374 (1.0 = perfect mixing):
no correction. Reading the paper afterwards confirmed the authors integrated
nothing either.

**3 · Human: Harmony, against the pipeline's own default.** The three human
donors are healthy biological replicates, so donor separation *is* technical,
but with no condition metadata, the pipeline's automated rule declined to
recommend integration (`integration_recommended: false`). The deciding
evidence was biological: single proposed cell types were fragmenting into
donor-private clusters in the uncorrected embedding, one cell type is not
several cell types in several donors. Harmony was applied as an explicit,
logged override (`--integration harmony`), the unintegrated embedding was
retained for comparison, and the donor-driven-clustering check now reports
false. Together with decision 2 this is the point: the answer is not "batch
correction good" or "bad", **the experimental design decides.**

**4 · Author labels held out.** The deposited annotations were excluded from
every clustering and trajectory step and used only afterwards, as an answer
key. That is what makes the median cluster purity of 0.947 and the pseudotime
ordering of the labels *validation* rather than circular confirmation.

**5 · Contradicted annotations retained, not overwritten.** The blind
marker-panel annotator disagrees with the deposited labels on 3 of 29 mouse
clusters; those proposals are flagged `[CONTRADICTED]` in the tables and on
the UMAP rather than silently corrected. The instructive failure is kept on
display: cluster 0's panel score said "transitional epithelium", but it is
89.2% CAP1 endothelium expressing an interferon program, a *state* that
fooled a *type* classifier.

**6 · A convenient finding was refuted and the refutation kept.** An early
audit suggested Scrublet was over-removing the human AT0 population at up to
2× background, a finding that would have flattered the project's critical
posture. I had the test itself examined: a co-expression gate cannot audit a
co-expression detector. A stricter gate (SFTPC⁺ SCGB3A2⁺ EPCAM⁺,
lineage-negative) reversed the conclusion, AT0 flagged at 3.9% vs a 6.3%
baseline, below background, and the full sequence, including the wrong first
pass, is documented in [`docs/DOUBLETS_AND_SCRUBLET.md`](docs/DOUBLETS_AND_SCRUBLET.md).

**7 · The trajectory required a commissioned re-analysis.** The whole-atlas
embedding does not answer the regeneration question, at atlas resolution the
alveolar states are clusters, not an ordered process. I commissioned a
focused analysis restricted to the 25-sample annotated cohort's alveolar
epithelium (5,694 cells), with PAGA and diffusion pseudotime rooted in AT2,
which recovered the AT2 → Krt8⁺ transitional → AT1 ordering with the labels
held out.

**8 · The capillary injury state required compartment-specific reclustering.**
The source study reports that the persistent injury state (iCAP) is not
resolvable at top-level clustering, so it was never expected to appear as an
atlas cluster. The focused capillary analysis (43,359 cells, reclustered
within-compartment) recovered it, including its defining behaviour: it
emerges after infection and does not resolve by one year.

**9 · The CAP2 tracing result is uninformative, not negative.** The
CAP2-specific Cre lines label only 2–8% of endothelium, so their near-zero
trace rates in the injury state cannot be distinguished from insufficient
labelling. The report says "uninformative" where "negative" would have been
the stronger, and unsupportable, claim. The Kit line, which labels CAP1,
traces the injury state at 33–53% per animal, and that is the claim actually
made.

**10 · The "not done" boundary is explicit.** No ambient-RNA correction (the
required raw droplet matrices are absent for the mouse series); no formal
trajectory-DE model; no whole-lung composition claims from MACS-enriched
material (the cell-type ratio is a sort ratio); and the tool-reference pages
in `docs/` describe the published method, not what ran, the generated
[`docs/PIPELINE_AS_RUN.md`](docs/PIPELINE_AS_RUN.md) is the authoritative
used/not-used record.

**11 · Reference criteria are adopted by pre-registration, not by copying.**
(2026-09-09, under review.) The HLCA paper (Sikkema et al. 2023) was read as
the roadmap's "reference framework". Its integration benchmark, entropy
thresholds, marker filters, sample-count rule and label-transfer uncertainty
cutoff were extracted into a reviewable JSON file, and the AI session then
proposed, criterion by criterion, what this pipeline should adopt, adapt or
decline (`Research Article/gate1_04_sikkema_2023_hlca/PIPELINE_FRAMING.md`). Two
proposals are already fixed by earlier decisions: supervised scANVI on the
deposited labels is declined because it would make decision 4 circular, and
the HLCA donor-entropy threshold is not copied because it encodes 107 donors.
A first trial applied the label-entropy and donor-entropy rules to the
tracked cluster tables with the thresholds frozen from the paper before the
tables were opened. My retain/reject decisions on the extracted material,
and any rejected AI output, will be recorded here.

**12 · Framing follows cell state and niche biology, not the source paper's
injury narrative.** (Owner instruction, 2026-09-09.) The interferon and
influenza context is not the point;
results are framed by cell state, repair and niche biology, macrophage and
monocyte states, annotation robustness and curation hygiene, grouped by the
reading-order themes. The data do not change; the write-ups do. Trials S3 to S5 and
their plan follow this rule.

**13 · Rule revisions are disclosed, not silently applied.** Trial S3's
first run used a two-marker minimum and a compartment set that the source
sheet does not support; eight identities were lost and a spurious
compartment appeared. The rules were corrected, the first-run outcome was
kept in the run record, and a hierarchical assignment was added as a
post hoc sensitivity rather than swapped in as the primary. The two schemes
disagree on AT0, and that disagreement is the result, not a nuisance to be
resolved by picking the scheme that flatters the earlier AT0 candidate.

**14 · A headline that the reference route does not support is flagged,
not softened.** (2026-09-09.) With my authorisation the AI session
installed PyTorch and scvi-tools into the emulated interpreter and mapped
the human series onto the HLCA core by scArches surgery (trial S2). The
mapping reproduces the HLCA authors' own transfer of the same cells at
99.2% (level 3), so the environment is sound, and it says the "AT0
candidate analogue" subcluster is mostly AT2 or uncertain, with AT0 a
minority of the series. That contradicts the wording of the human headline
in `FINDINGS.md` and the August 2026 summary PDF. The contradiction is recorded in
`PROGRESS.md` with a proposed re-wording; the decision to retain, re-word
or reject is mine and is pending. The `scarches` package could not be
imported with the pinned anndata and was removed; the surgery uses the
scvi-tools implementation and the deviation is disclosed in the trial.

**15 · The paper's phase structure is reproduced from the trace, not from
the classifier.** (2026-09-10, under review.) The source paper's central
descriptive claim, that proliferation after injury runs in phases (immune,
then epithelium and mesenchyme, then endothelium), was reproduced from the
tracked metadata alone, with the expected peak windows frozen in the run
record before the table was opened. The Ki67-trace peak falls in the
paper's window for four of five lineages; lymphoid cells peak one harvest
later. The deposited cell-cycle call was carried as a cross-check and
disagrees for four of five lineages because it calls most lymphocytes
cycling; it is reported, not used. The myeloid compartment was then taken
from the blind atlas clustering (clusters 5, 17, 24), re-embedded with the
labels held out, and graded afterwards, at the resolution fixed from trial
S5; its per-animal composition reproduces the paper's Figure 3 (aMAC loss
and iMON expansion at 6 dpi, reconstitution by 19 to 42 dpi). Both analyses
use the deposited labels descriptively and say so, and neither computes a
P value, because the active-repair days carry two animals each. Retain,
re-word or reject is mine and pending.

**16 · Batch is tested on a key that crosses time, never on the animal, and
a rule that selected the wrong object is disclosed, not swapped.**
(2026-09-10, under review.) The reviewer's question about the myeloid
result is whether the 6 dpi inflammatory-monocyte state is a one-day batch
island. Correcting on sample cannot answer it (one animal per sample and
day). The paper's Table S3 shows that on every active-repair day and at 42
dpi the two replicate animals came from different infection rounds, so
round is a technical key that crosses time; it also carries Ki67-Cre
dosage, which makes correcting on it the conservative direction. The
compartment was embedded with and without Harmony on round, on the days
that carry both rounds. The pre-registered survival rule defined "the iMON
state" as the subcluster with the most iMON-labelled cells, and the first
run showed that this picks the 11 to 19 dpi monocyte state in both
embeddings (3.9% and 22.0% of its cells from 6 dpi), not the 6 dpi state
the question is about. As in decision 13, the first-run outcome stays in
the run record, the definition anchored on the 6 dpi cells is added as a
labelled post hoc reading, and both are reported. The same session read the
Ki67 trace by tamoxifen window for the rebuilt alveolar macrophage pool and
let two of its three pre-registered checks fail closed on a 30-cell floor
rather than lower the floor after seeing the tables. Retain or reject is
mine and pending.

**17 · The repository is an analysis log, and established material is
displaced rather than deleted.** (Owner instruction, 2026-09-10.) Two
kinds of content had accumulated that are not part of the ongoing analysis:
curation material (a summary PDF of August 2026 and its generator) and the
Krt8-high transitional work (the alveolar trajectory, its time course, and
the human KRT8 reference-aligned panels), which is established elsewhere,
outside this repository. Both were moved out of the main narrative into
`archive/` with a note on what moved, when and why; their artefacts and
scripts stay in place (then under `analysis/`; the artefacts moved with their
series to `Research Article/` on 2026-09-21, decision 25) because the validator checks
their numbers and the scripts regenerate them. The README was rewritten to open with the
claims table, to state the working question rather than a recovery
exercise, and to name H1N1 once as the injury model of one series, because
the roadmap ahead is not an influenza project. Claims were softened where
they overreached ("never resolves" became "has not resolved by 366 dpi").
The checks were renamed from portfolio to repository checks. Nothing was
deleted and no number changed.

**18 · A gate that fails is a result, and a rule that fails is disclosed
three times rather than repaired once.** (2026-09-12, under review.) I
instructed that the Cardoso 2026 paper be entered out of roadmap order and
analysed in gates, with the standing condition that an unexpected result be
reported and acted on rather than finished around. Gate 0 read the deposit
before anything was fitted and found the constraint that governs everything
after it: every deposited mouse library pools three mice and each genotype
contributes one library per sort, so no genotype contrast in that deposit
carries within-group replication. The same trial closed one of my own
proposed branches: the mesenchymal and immune libraries are a single time
point, so the paper's fibroblast-before-macrophage ordering cannot be tested
transcriptomically, and that was reported as the answer rather than
approximated with something weaker.

Gate 1 then returned "not recovered" against its own pre-registered rule, and
the rule turned out to be at fault in four separable ways: it selected
fibroblasts by a confidence floor that excluded the candidates; two genes of
the paper's marker set are mural markers, so the score peaked on smooth
muscle; a third is a myeloid transcription factor, so it also flagged a sort
contaminant; and the population it was hunting missed the Tnc floor by one
thousandth. None of these was fixed in place. The first-run outcome stands in
the record, the corrected passes sit beside it as C1b to C1d, and the
threshold was not moved after the fact, because a rule moved to fit the
result it just failed is not a rule. The same defect recurred in Gate 2b and
was handled the same way, in C2b.

Two findings came out of that stopping rather than out of the original plan.
The mesenchymal sort carries 6.5% off-target cells, among them 184 mutant
epithelial cells that are 88% Areg-positive, almost entirely in the tumour
arm; the paper is unaffected because it took its epithelium from a separate
series, but a reanalysis computing signalling inside that one library would
have been reading a contaminant as the source. And on the Areg-deletion arm,
four of the six genes in the paper's fibrotic set fall with the ligand while
Pdgfrb and Runx1 do not, which suggests the state has separable parts. Both
are mine to retain or reject, and both are recorded as Exploratory until I do.

**19 · Leave the deposit to get a testable unit, and let a rule frozen in
advance refute your own best lead.** (2026-09-13, under review.) Decision 18
recorded that the Cardoso deposit cannot test anything, and the agent's leads
from it were accordingly all Descriptive only or Exploratory. I directed that
the most interesting of them, the Hbegf lead, be extended into public data
rather than written up from one deposit, and that the extensions run only if
the first one did not refute the working picture. Four extensions were
pre-registered. Three things about how they turned out are worth recording.

First, moving datasets is what made a test possible. GSE131907 has eleven
donors with paired tumour and normal lung, so the unit becomes the donor
instead of the library, and the first admissible test in this whole section
returned AREG detection higher in epithelium than in myeloid cells within
donor, p = 0.0020. Every earlier row in the section is descriptive because of
a design choice in the deposit, not because of anything the analysis did, and
this is the demonstration.

Second, and this is the part I want kept prominently, a rule frozen before the
data were opened refuted the agent's own best lead. The three-tier fibrotic
response of C29 had been the most promising thing the Areg arm produced, and
its proposed reading was a second, tumour-specific signal driving the retained
Runx1 and Pdgfrb tier. Trial E4 asked what bleomycin alone does to the same
genes in sorted mesenchyme with no oncogene present, under a rule requiring
both injured animals to exceed both controls and with the interpretation of
each outcome written down in advance. Both genes cleared it. The
pre-specified reading therefore applied with no discretion left: the retained
tier is what an activated lung fibroblast does after any injury. The numbers of
C29 stand and its interpretation is gone, which is the correct outcome and the
reason for freezing readings rather than only thresholds.

Third, the agent reported two results that cut against its own earlier
statements without being asked to look for them. The compartment gate that E1
called "neutrophil" was 83 per cent deposited myeloid cells in a deposit with
no neutrophils at all, which changes which pre-named outcome that trial hit;
and the AREG source that E1's test established as epithelial-over-myeloid is
qualified at subtype resolution, where dendritic cells sit above both tumour
epithelial states. Both are in the trial log next to the original wording
rather than replacing it.

What the extensions did not deliver is also on the record. E2's only testable
comparison failed to detect the difference it was built on, seven donors and
p = 0.297, and the Zhao prediction could not be tested in either fibrosis
cohort because no comparison cleared the five-donor floor and the two cohorts
disagree in direction. Those are reported as Not established rather than as
trends. The one thing that replicated across three datasets, a
dendritic-cell and monocyte ligand source, is explicitly recorded as
established immunology rather than as a finding of this repository, and is
kept because it constrains a reading, not because it is new.

Mine to retain or reject: the weakening of C29, rows C37 to C48, and whether
the myeloid ligand source is worth a paragraph in the eventual writeup.

**20 · Three chosen questions, three negative answers, and two rules that
failed instead of the biology.** (2026-09-13, under review.) I picked three
jobs off the agent's ranked list: a donor-level test of the paper's axis, the
identity of the mesenchymal-sort contaminant, and whether the Areg-independent
tier is a population or a gradient. None returned a positive result, which is
the ordinary outcome of asking precise questions, and two of them failed
because the pre-registered rule was badly chosen rather than because the data
were silent. That distinction is the reason this entry exists.

**What the agent got right about its own rules.** In trial C7 the rule said to
name the best-correlating reference state and to report the margin. It did
both. The margin was 0.0056 while the same measure separated epithelium from
fibroblasts by 0.415, so the measure has compartment resolution and no state
resolution, and the named winner is meaningless. The agent reported the winner
as the rule demanded, then refused to read it, and left the threshold alone. In
trial C8 the mixture test preferred two components, which the frozen reading
calls a subpopulation, and the agent showed why that is arithmetic: 31.5 per
cent of the cells detect neither of the two genes in the score, so a spike at
zero guarantees the second component. It noted that trial C1 had used the same
test on a centred score where the problem does not arise, so the defect is the
reuse and not the original. Neither rule was edited after the fact.

**The one thing that was edited, and why that was correct.** Trial E6's depth
rule said any pair whose two members both correlate with sequencing depth is
not read. The first implementation applied it only to the primary tests, so a
significant control pair came through unmarked. The agent changed the code to
match the rule text, not the rule text to match the result, and re-ran from
cached values. I am satisfied that is a bug fix rather than a threshold move.

**The result I want kept visible.** E6's only significant correlation was a
control: epithelial TGFA against fibroblast activation, p = 0.045. Both of its
variables track sequencing depth, so the rule threw it out. Had that number
landed on AREG instead of TGFA it would have read as confirmation of the
paper's axis, and nothing but the pre-registered control would have caught it.
The primary test itself is a null, rho 0.348 at p = 0.112 over 22 donors, and
the agent reported the smallest effect the test could have seen, about rho
0.43, rather than implying the axis is absent. It also said plainly that
pooling all epithelium dilutes the state the paper's claim is about, so the
null does not contradict the paper.

**What the three jobs bought.** List A of the next-step document is now empty:
every question answerable from data on disk has been answered, five of the six
negatively or with a correction. The surviving lead is post hoc and labelled as
such: the co-organisation in the fibrotic set sits on the tier that falls, Fst
with Runx2 at a ratio of 1.735 in the control arm and gone after deletion,
while the retained genes are independently distributed in both arms. It rests
on 24 double-positive cells in a single library, and the agent said so in the
same sentence as the finding.

Mine to retain or reject: rows C49 to C57, and whether the post hoc Fst and
Runx2 lead is worth a pre-registered trial of its own.

**21 · Paper 2 was entered on a "proceed", not on a direction, and its note
is withdrawn.** (2026-09-13; corrected 2026-09-15.) The first version of this
entry said I directed a return to roadmap order starting with Choi 2020. The
session transcript says otherwise, and the record has to match it. After the
E6, C7 and C8 jobs the agent listed what remained and put "returning to
roadmap order with Choi 2020" at the end of that list as its own
recommendation. I asked whether anything more was to go, the agent repeated
the list, and I answered "proceed". The agent read that as approval of every
item and entered paper 2, study note, extract and trial D0, all before I had
read the paper. Later the same day I said I would open a session on Choi 2020
after actually reading it and that it should be left; the agent honoured that
from then on, and D1 never ran.

On 2026-09-15 I settled it. The AI-written study note is REJECTED: a note on a
paper I have not read is not mine to retain, whatever its quality, and the
folder for paper 2 will be added when I have read the paper and decided what
analysis it deserves. The note stays in git history (PR #19) and is not on
main. Trial D0, its artefacts and the marker extract are kept and relocated
under the Cardoso folder as an extension, because the deposit facts it
established (one library per condition, six raw whitelists, no counted
reporter, coverage-only ATAC) bear directly on the DATP state the Cardoso rows
lean on. The trial keeps its identifier so its run record and rows C58 to C64
stay true; nothing was re-run.

What the trial found stands as recorded: the same replication ceiling as the
Cardoso deposit, in a second key paper in a row, which is worth keeping as a
pattern rather than a surprise. These are deposits from labs whose conclusions
rest on genetics and imaging, where the transcriptome is a map rather than the
evidence, and the deposit reflects that. The reading note also stands: the
agent found that the PMC web rendering strips italicised gene symbols and
switched to the Europe PMC XML rather than filling marker sets from memory. And
the reporting defect disclosed in the first run, a single boolean that read as
"none are raw" when six of eight were, is unchanged in the record.

The rule this adds: an agent may run a deposit reality check when I say so, but
the study note for a roadmap paper is written or directed by me after I have
read the paper. "Proceed" against an agent-written list is approval of the
list, and the agent should say which items it is treating as approved before it
starts the ones that commit a reading on my behalf.

Mine to retain or reject: rows C58 to C64 only. Gate 1 on this paper is not on
the table until my own folder exists.

**22 · A frozen rule has to say what would make its own answer unreadable.**
(2026-09-13, under review.) I asked for the post hoc Fst and Runx2 lead from
trial C8 to be given a pre-registration of its own. It was, and the trial did
three things I want on the record.

It named what it could not do before it ran. Whether Areg deletion depletes
that population is not testable with anything on disk, one library per genotype
and no other Areg-flox fibroblast dataset, and the trial said so in its own
docstring rather than producing a number that looked like an answer.

It separated existence from magnitude, and only one of them survived. Above
chance co-occurrence replicates in both bleomycin animals against a null that
holds sequencing depth fixed by construction, p = 0.005 and 0.010, in a dataset
with no oncogene. The size of the effect does not: about thirty double-positive
cells per library cannot support a stable ratio, and the agent said that rather
than quoting the ratios it had computed.

And for the third time in this folder, writing the numbers out exposed a defect
in a rule rather than in a result. T1's criterion rested on a ratio that T5
forbade reading, so the two rules were not composable; the implementation took
the conservative branch, its verdict stands, and the agent flagged that the
pre-registered reading attached to that verdict is not what the data did. The
same shape appeared in C7, where the profile test named a winner without
requiring a margin, and in C8, where a mixture test was applied to a
zero-inflated score. The lesson I am taking from the three together is the one
the agent stated: freezing a threshold is not enough, and a rule also has to
say in advance what would make its own answer unreadable.

The magnitude criterion in T4 is a fourth instance of the same thing, caught
the same way. Nine of twenty-seven markers cleared "at least half the reference
magnitude", and the median marker sits at 0.535 against that 0.5 line while the
comparison libraries carry half the genes per cell. The criterion was measuring
depth. What does survive is stronger and simpler: twenty-six of twenty-seven
markers point the same way in both animals.

Mine to retain or reject: rows C65 to C72, and whether the matrix and mechanics
programme those cells carry (Piezo2, Ltbp2, P4ha3, Sdc1, Prrx2) is worth a
pre-registration of its own, given that it points away from the Areg axis
rather than into it.

**23 · Paper 2 entered at my direction after reading; the same rule defect
twice, and a state that does not separate.** (2026-09-15, under review.)
Having read Choi 2020, I asked for the possible gene analyses to be listed, a
separate folder with a structured pipeline, the paper's results reproduced
first and its claims attacked after, until nothing remained; and, part way
through, for the core logic backbone to be fetched from my notes and the
repository and checked against the plan trial by trial. That backbone check
is a table in the plan. Trials D1 to D7 ran the same day, every rule frozen in
a run record before its object was opened, and I said to proceed to the pull
request and merge when the write-up was done.

Two things belong here. First, the annotation rule I approved froze two
clauses on Sftpc detection below 0.5 (one for contaminants, one for AT1), and
in a lineage-sorted AT2 library every cluster detects Sftpc in every cell, so
the clauses could never fire. The first pass called a 337-cell AT1 cluster
hAT2 and let a ciliated cluster wear the primed-AT2 label; the organoid pass
kept a 586-cell stromal cluster, the size of the one the paper removed, and
missed a 481-cell AT1 cluster, which made the paper's Figure 7 reading look
not computable when it was. Both outcomes stand in their records, no
threshold moved, and corrected passes D2b and D5b sit beside them with one
added condition: the Sftpc clauses apply only where Sftpc separates clusters.
This is the shape of decision 22 again, the fifth and sixth instances and the
first outside the Cardoso folder: a threshold frozen on a variable that does
not vary in the deposit. The rule I take from it: before a clause is frozen,
check that the variable it tests spans the threshold somewhere in the data
the rule will see. Trial D0's marker table had Sftpc present in every library
and nobody read it that way.

Second, what reproduces and what does not. Four of the paper's five states,
the DATP time course, the hAT2 to DATP to AT1 ordering inside one library,
DATP's programmes in vivo and IL-1beta's shift of the organoid epithelium all
come back from the deposit as descriptions, and the organoid cell counts land
within 8 percent of the paper's. The primed AT2 state does not: at three
resolutions, in a sub-clustering of DATP and at the cell level, no group of
cells loses Etv5, Abca3 and Cebpa while gaining the inflammatory genes, and
the organoid cluster the paper calls 77 percent primed carries the DATP
markers with its identity genes intact. Whether that is a graded state the
paper's cluster averages made discrete, or an identity ratio my rule set too
strictly, cannot be settled without a new pre-registration; the folder
proposes one (E6) and does not run it.

Mine to retain or reject: rows C85 to C104; whether to pre-register E6;
whether to download the dissociation list (M8) and run attack A3.

**24 · The register was audited by adversaries against its own artefacts,
and the entry point was written question-first.** (2026-09-20,
under review.) I asked for the two branches of paper 2 to be run, then for a
multi-agent attack on every claim they made, then for the repository to be
scanned and cleaned with the README updated first and a new document of core
questions and remarkable phenotypes that a reader could take in cold,
rather than the register's trial-by-trial alignment.

The audit is the decision that matters. Eight adversaries and forty-seven
verifiers found that the branches' trials were mostly honest and the register
written from them was not: four numbers had been quoted that no run produced,
including the Sox9 corroboration of the branch's one validated result, which
was never in the frozen panel and existed only as a typed string; three
magnitudes were wrong against their own tables; one row named the wrong
laboratory; one was refuted by the branch's own artefacts. I accepted every
confirmed finding. The corrections were made with figures read from the CSVs,
a new trial (M4) logs the corroboration that had been asserted, frozen
docstrings and run records were left untouched with a banner beside them, and
the audit itself is rows C151 to C154. The rule I take from it is mechanical
and now binding: no number enters a summary or the register except by
formatting from the table that holds it.

Two smaller decisions of mine on the same day. I withdrew Route C of the
Axin2 branch as out of focus, because a bulk array cannot answer a
co-occurrence question at any level of replication (row C146), and I directed
that Route A run rather than wait for my reading of England 2025; it then
turned out to rest on data never deposited (row C148). For the README I chose
to replace the Leiden UMAP with a figure of the register's own shape, drawn
from `CLAIMS.md` by a script, because that shape is what this repository is.
`RESEARCH_QUESTIONS.md` went through a second adversarial fact-check before it
landed (119 findings, 17 independently verified before the session limit, the
rest checked by hand); its confirmed defects, chiefly register statuses quoted
one grade too strong and a range typed from the wrong pass, and their fifty-eight
fixes are listed in PROGRESS item 36. My retain or reject on the question-first
framing is pending.

**25 · The deposits moved beside their papers, the README was left open, and
a cost rule for multi-agent work was set.** (2026-09-21.) I asked for the
analysis folders to move into `Research Article/`, one folder per dataset, or into the
paper folder when that paper produced the deposit. GSE262927 therefore sits
under paper 1. GSE178360 sits under a folder for Murthy 2022, which is outside
the roadmap, and that folder holds a pointer note only, because decision 23
stands: no study note before I have read the paper. I asked for the README to
stay open-ended, because there is more to go, and it now says what is not
done rather than reading as finished work. And I set a rule for the
assistant, recorded in `AI_CONTEXT.md` and in the cross-project harness file:
before launching a multi-agent workflow, weigh its cost; do the deterministic
part with a script; deploy agents only where a script cannot judge, and then
with at most three lenses. The fact-check of the entry-point documents the day
before had used six checkers and forty-seven verifiers and hit the usage
limit for what a script catches faster. The move itself was done and checked
by script, with the validator, the compiler and a path-resolution check as
the gates.

**26 · Each research question gets a figure of the kind a paper shows.**
(2026-09-21.) I asked for a figure per question in `RESEARCH_QUESTIONS.md`
as a visual aid, and when the first proposal reached for summary plots I said
what I meant: the figures that research papers actually use, embeddings,
trajectory maps, violin plots, whatever fits. The five that landed are drawn
from the analysed objects by one script, cite the register row each one
illustrates, and carry no number that is not formatted from a table beside
them. They are aids to reading, not evidence, and the captions say so. One
panel was withdrawn by the assistant before I saw it: a per-nucleus promoter
count by group, which is the depth-dominated reading rows C127 and C130 record
as a mistake; it was replaced by the detection-at-budget form of the
registered statistic. I have not yet reviewed the figures themselves. I
also asked for each question to name its roadmap branch and a further
mapping, and then decided that mapping is personal planning, not analysis,
and does not belong in the repository: it is kept in my private notes, as
the assistant's reading of fit, awaiting my review.

**27 · The purpose restated: hypothesis generation, and nothing else in
the public text.** (Owner instruction, 2026-09-22.) I restated what this
repository is for: hypothesis generation from an integrative reanalysis of
public lung single-cell and multiome data, applying frameworks newer than the
source papers to surface phenotypes and data distributions. How I use the
resulting questions is personal planning; it lives in my private notes and
does not appear in any tracked file. The wording of the README, the citation
file, `RESEARCH_QUESTIONS.md`, the roadmap and its JSON, the trial plans, the
register's preamble and Potential column, `AI_CONTEXT.md`, this file and
`PROGRESS.md` was changed to match; reading-order branches are named by
theme rather than by laboratory. No decision, status, number, threshold or
frozen rule changed, and no register row was added or removed. The August
2026 archive keeps its file names, because they are paths in a record. A
first attempt at this, as one scripted bulk rewrite, was stopped by an
automated check before it ran; this pass was made file by file.

**28 · Owner review of the gene set enrichment trials, row by row.**
(2026-09-22.) The assistant set out the evidence for each row from the
tracked artefacts and I decided.

- **C161, retained as Validated, narrowed and with a third limit.** What is
  validated is the donor-level direction of each of the 62 sets, replicated
  in a held-out cohort, not a biological reading of it. The row now also
  says that both discovery nulls sample genes rather than donors, so the
  discovery FDRs are optimistic and the replication carries the claim; that
  replication does not exclude an artefact both cohorts share; and that the
  eight AT2 sets are the weakest, because the programmes that replicate there
  are ones ambient RNA from fibrotic tissue would also produce. Offered and
  not chosen: keeping the row as proposed, splitting the AT2 sets out as
  Exploratory, and rejecting the row to Descriptive only.
- **C155, retained as Descriptive only.** A metadata scan that licenses G1
  and G2 and establishes no biology. Checking it against G0's own table
  found a slip in the paper-1 trial plan, which said ten of the eleven
  inadmissible deposits are single-library; the table says eight, and the
  plan now says eight.
- **C156, retained as Descriptive only, with a timing sentence.** The failed
  G2M gate and the phase claim C9 measure different moments: C9 reads the
  Ki67 trace from the tamoxifen window (myeloid peak 6 dpi), the gate reads
  cycling at sacrifice (myeloid cycling peak 25 dpi). The row now says so.
- **C157, retained as Descriptive only.** The corrected gate was written
  after G1's tables were seen and is disclosed as such (R0); the sets come
  from the same deposit, so it checks the machinery, not the biology.
  Offered and not chosen: downgrading it to Exploratory.
- **C158, retained as Exploratory, with a caveat sentence.** Three animals at
  366 dpi carry a direction only; the nulls sample genes, and a growing
  proliferating subset would move the pseudobulk. The same direction in
  human IPF macrophages (C161) is recorded as a cross-species lead, not as
  evidence. Offered and not chosen: Not established, or rejection.
- **C159, retained as Not established.** An absence at three animals.
- **C160, retained as Descriptive only, with a pointer to C161**, where its
  held-out replication is recorded.

**29 · The A1 figure keeps both readings of promoter chromatin, side by
side.** (2026-09-22.) Decision 26 records that the assistant replaced a
per-nucleus promoter-count violin with the detection-at-budget heatmap before
I saw it. Shown both, with the depth behind them, I chose to add the violin
back beside the heatmap rather than keep the replacement alone or restore the
violin in its place. The reason is in the numbers: by group, transitional
nuclei have the highest promoter score (median 0.91 against 0.00 and 0.38)
only because they carry about twice the ATAC fragments (9,435 against 4,799
and 4,842); among nuclei with any signal they are the lowest (1.31 against
1.54 and 1.60), and at one depth budget promoter detection is flat. Read
alone, the violin would support the retracted "silenced but not closed"
reading (C120); beside the depth and the heatmap it is the clearest picture
in the repository of what row C127 records. The figure now has panels g to
i, the numbers are written to `rq_a1_groups.csv` and formatted into the
caption by script 16, and the replacement itself is retained. Offered and
not chosen: keeping the heatmap alone, and restoring the violin in its
place.

**30 · Owner review of the two Choi 2020 branches, rows C116 to C154.**
(2026-09-22.) The assistant checked by script that every artefact these
rows cite exists, then set out each row's evidence and I decided, in four
themed groups.

- *Deposit and label facts.* **C116** retained as Validated (the suffix
  inversion); **C117** retained as Not establishable; **C119** retained as
  Refuted (the label fires in uninjured neonatal wells); **C153** retained as
  Descriptive only with its claim narrowed to the papers' reported
  directions and one reported ratio, because the absolute fractions are not
  recovered (C124).
- *The chromatin question.* **C118** retained as Descriptive only (the RNA
  loss, consistency between two deposits of one laboratory, not
  replication); **C120** retained as Retracted-superseded; **C121**, **C133**
  and **C128** retained as Not established; **C122** and **C132** retained as
  Refuted; **C131** retained as Exploratory, with the uninjured-control
  caution already in the row. Offered and not chosen: C131 to Not
  established.
- *Method lessons.* **C123 to C127, C129, C130** and **C151** retained at
  their statuses (refutations of the branch's own rules, and the audit).
- *Retained as a block, to revisit.* I kept the remaining nineteen rows,
  **C134 to C150, C152** and **C154**, at their current statuses without
  reviewing them row by row, and will come back to them; their status cells
  say so. The assistant had proposed two claim-wording fixes that I have not
  decided and that were not applied: C152's claim says an unlogged number
  "is a wrong number" while its own evidence has an unlogged number that was
  right (its Potential column states the real point, that such a number is
  Not established), and C154's claim ("Route B's transitional cell set was
  reported") describes the register rather than the result.

**31 · W1 run first, narrowed to alveolar macrophages.** (2026-09-22,
under review.) Offered W1, the GSE309751 chromatin analysis, or entering
paper 3, I chose W1 and authorised installing pydeseq2 into the emulated
environment. The narrowing to the aMAC population was the assistant's
proposal, which I accepted, because it is the only myeloid population that
clears the cell floor in every arm. Three further design choices were the
assistant's and are mine to retain or reject: excluding the three
Ki67Cre/Cre animals, a machinery gate on sex genes instead of a biological
positive control, and CAMERA as the set test. The rules were committed
before any count was read (commit c5b6e53). No set cleared; the gene-level
readings are Descriptive only, and the resolution against long-term arm is
confounded with age, harvest date and sex. Rows C162 to C164 await my
review.

**32 · Delegated scientific reassessment and portfolio remediation.**
(2026-09-22.) After the repository audit, the owner explicitly authorized the
assistant to apply priority fixes, reclassify claims that no longer warranted
retention, close feasible structural gaps, and carry out improvement orders
1–4. The owner also authorized relevant additional analyses and figures for
portfolio use and requested new research questions arising from the corrected
evidence. These are delegated assistant judgments; they are not represented as
individual owner review of every changed row. Decisions 28–31 remain the
historical record of the preceding retention choices.

The corrected analyses preserve raw inputs and historical trials, using separate
output locations for epithelial-only ligand rankings, annotation/depth source
comparisons, reference gene-set inference and a unified epithelial specificity
project. Specifications are retrospective corrections on known data, not new
unseen-data preregistrations. The exact before/after claim text is recorded in
[`claim_decisions.json`](docs/remediation/2026-09-22/claim_decisions.json).

The reassessment distinguishes observed directions from calibrated biological
inference, detection from abundance and surface mechanisms, accessibility from
fate, and reference-cell split calibration from animal-level uncertainty.
Bulk-sorted associations are not relabelled as same-cell overlap. C152's
provenance contradiction and C154's bookkeeping proposition are corrected.
Reference CAMERA and normalization sensitivities replace the custom-method
interpretation of W1 while retaining its original outputs.

The structured claim index and explicit numeric bindings record the coverage of
machine checks. Previous run records are archived before replacement and new
records include content hashes and code identity. CI now covers Python sources
under both analysis and Thesis, contract tests, and generated-index consistency.
The portfolio entry point emphasizes demonstrated analyses and remaining limits;
status counts are not used as a measure of scientific calibration.

Completion, numerical results, tests and the purpose-aware next-stage decision
are in the [implementation record](docs/remediation/2026-09-22/IMPLEMENTATION_STATUS.md).

## 33. Consolidate shared questions and current status (25 September 2026)

The owner requested a repository-wide structure audit, consolidation into the
existing research-question register, updates to related Markdown documents
and the private Notion roadmap, and revised LinkedIn project text.
The former Yu RQ1–RQ4 are now A11–A14 in
[RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md); their six shared figures,
plotted tables and scripts moved into the established `analysis/` layout.
Paper-specific inference and its 17 figures stay with the paper. The
[structure contract](docs/REPOSITORY_STRUCTURE.md) documents label namespaces
and the original-to-current path mapping.

The original UMAP/PCA preparation and scientific table bytes were preserved;
only presentation labels were rerendered. Original script bytes, run records
and a relocation manifest retain the execution history. Status edits distinguish
completed feasible work from unavailable endpoints and new proposals. No
scientific threshold, claim classification or inference was changed by this
consolidation. A LinkedIn draft was prepared for owner use at the time and was
never posted; **the owner removed it from the repository on 27 September 2026** as
work that should not have been tracked here, so the link is gone and the sentence
records what happened rather than pointing at a deleted file. Personal PI-fit
planning remains in Notion.

## 34. Rework A1 lineage/function stages and execute the first batch (25 September 2026)

The owner challenged the proposed stages 3–4 and explicitly requested a review
of established tracing studies, a patched plan and initiation of analysis.
Codex implemented the revision and execution; acceptance of the resulting
scientific interpretations remains with the owner.

| Date | Proposal reworked | Reason | Decision authority |
|---|---|---|---|
| 2026-09-25 | Broad trajectory and spatial/proteomic work as the immediate A1 lineage/phenotype stages | It did not prioritize measured ancestry/descendants and same-study functional endpoints; modalities could be mistaken for interchangeable validation | Owner requested the challenge and revision; Codex developed the measured-endpoint-first implementation |
| 2026-09-25 | A biological overlap comparison of the deposited PATS H3K4me3 calls | Input headers revealed different caller region/merging settings; interval differences cannot establish a biological state distinction | Codex input audit under the owner's authorized analysis; replaced with technical audit, without relaxing gates |

The [lineage audit](RQ_Specified/A1_transitional_epithelial_state_distinction/LINEAGE_AUDIT.md)
records the primary sources. The
[batch report](RQ_Specified/A1_transitional_epithelial_state_distinction/reports/FIRST_BATCH_REPORT.md)
records the PATS source reconstruction, frozen ten-mouse IRE1α model,
descriptive ATAC/CD44 profiles, failed pathway coverage and remaining holds.
Undefined control fractions were not converted into zeros; unrelated antibody
controls were not added to the KIRA8 comparison. Numerical source versions,
hashes and model diagnostics are retained. No result was promoted to an
independent validation or universal transitional-state taxonomy.

## 35. Plan a biological-question-first restructuring (25 September 2026)

After merging PR #67, the owner requested a substantial RQ review before
remaining analysis, using their attached `RQ_FRAMING_PROPOSAL.md`. Codex prepared
a restructuring plan, not an implemented replacement
of the register. It recommended four core questions with unchanged legacy IDs,
linked supporting contracts and conditional biological branches. That structure
was not adopted: decision 36 below records the rewrite the owner actually
requested, which kept all of A1 to A14 and dropped the fixed count. The plan
document itself was deleted on 27 September 2026 as an executed planning
artefact, and the [implementation record](docs/migrations/2026-09-25-rq-reframing/README.md)
holds its before-bytes and what changed. Its one part that no other file carried
is the refutation table below.

| Date | Prior framing challenged | Review outcome | Authority |
|---|---|---|---|
| 2026-09-25 | Biological hypotheses and depth/resource/annotation diagnostics presented as peer A-series questions | Owner requested substantial reconsideration; Codex proposed consolidation around measured biological endpoints | Owner initiated the revision; the resulting plan has not yet been adopted |
| 2026-09-25 | Stronger biological headlines treated as restatements of existing measurements | Planning review distinguishes motivating observations from untested temporal, lineage, receptor-complex and absence claims | Codex's assessment of the supplied proposal, for owner review |
| 2026-09-25 | The planning summary appeared to reduce the surviving biological questions to four | Owner asked whether scientific ownership was considered and whether only four survived; Codex made ownership explicit, added the broader hypothesis inventory and removed the fixed-count recommendation | Owner requested clarification; revised grouping remains a proposal |

The review also confirmed caption-generator drift that could restore a
superseded A2 figure. Repair is specified before redraw; no generator or
biological model was run, and no numerical evidence or claim grade was changed.

### Assertions from the owner's proposal that were refused as headlines

Carried verbatim from the deleted planning document, because it is a rejection
record and those stay visible. These were the owner's proposed framings, assessed
against the claim rows that existed at the time; refusing them as headlines did
not refuse the mechanisms as hypotheses.

| Attachment assertion | Assessment against current evidence | Safer use |
|---|---|---|
| AT2 RNA loss occurs over permissive distal chromatin, with closure later | C131/C133 do not establish distal state or time order; the old genotype comparator is not a clean temporal control | Optional A1 temporal hypothesis with explicit longitudinal requirements |
| Epithelium sets the AREG available to fibroblasts | C37 is measurement-sensitive; C45 supports competing myeloid sources; RNA is not secreted availability | Context-specific source/receiver experiment, not an existing supported conclusion |
| Late interstitial macrophages are the same persisting population | Cross-sectional proportions do not identify ancestry or replacement | Population-state persistence and cell persistence become separate estimands |
| AT1 identity is largely an extension of transition because 119 genes overlap | C168 quantifies shared definition, not developmental continuity or fate | Test added endpoint information from disjoint/shared components |
| Fibroblast EGFR is predominantly homodimeric | C114 is refuted as a resource-absence claim; receptor coexpression cannot measure dimer composition | RNA competence screen; direct complex/activation assay for the mechanistic claim |
| Neoplasia adds no separable epithelial programme | Shared-HPCS elevation does not exclude an additional programme | Test a bounded candidate addition on independent validation data; report an inconclusive null honestly |
| Unassigned IL1B-positive cells form a distinct source architecture | Annotation failure is partly determined by reference and threshold; ambient/mixed profiles remain alternatives | Resolve source identity before formulating a biological state claim |

These objections do not prevent proposing the mechanisms. They prevent treating
the proposal's motivating measurements as direct tests of those mechanisms.
Novelty remains to be checked against the literature for whichever narrow
hypotheses are retained; reframing alone creates neither novelty nor evidence.

## 36. Implement the biological RQ rewrite (25 September 2026)

After the revised framing plan in PR #68, the owner explicitly requested the
actual rewrite. Codex implemented hypothesis cards, a measurement-contract
index and a shared gallery. Every A1–A14 ID remains; no four-question limit
applies. A12-S1 remains enabling, and A14 keeps two independent decisions.
This supersedes the four-core wording in the initial historical decision 35;
it does not change the scientific status of any hypothesis or claim.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-25 | Implement the biological-question-first rewrite and supporting-document separation | Codex, following the owner's framing note and corrections | Owner requested implementation | Applied to the root register and related docs; scientific interpretation remains subject to review | Distinguish this project's biological hypotheses from supporting measurement checks without discarding distinct questions |

| Date | Reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-25 | Artifact-led RQ headlines and implied four-question survival limit | They obscured positive biological hypotheses and conflated scientific value with current data readiness | Owner requested the rewrite and challenged the limit |
| 2026-09-25 | Script 16's automatic caption insertion and A3 “after repair” title | The writer could restore superseded A2 content; recovery had not been measured | Codex implemented the approved plan's ownership repair and presentation correction |

The [migration record](docs/migrations/2026-09-25-rq-reframing/README.md) preserves
original sources and the old figure. Explicit figure selection and isolated
render records replace root-document mutation. Only A3 was redrawn from existing
coordinates; no scientific model/embedding was refit and no threshold or claim
grade was changed. Authorizing this edit is not acceptance of its hypotheses as
established scientific findings.

## 37. Reject A6 as the next analysis; join A5 and A11 through a shared component contract (25 September 2026)

Asked which remaining question was most plausible to launch, the assistant first
recommended A6, ranking it by data already on disk. The owner rejected that as an
artifact-adjacent choice. A6 asks whether IPF changes macrophage states beyond their
abundance, and the boundary between composition and within-state change is set by
how finely the states are annotated, so its answer moves with a convention rather
than with the biology. The assistant then recommended A11, and on the owner's
question proposed joining A5 and A11 by sharing their component definition while
keeping the questions separate. The owner chose that design and authorized its
execution on a separate branch.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-25 | Next analysis selection | Assistant recommended A6, then A11 | Owner | A6 rejected; A5 and A11 joined through a contract | A6 resolves to a variance partition set by annotation granularity, with no named mechanism at the end |
| 2026-09-25 | Shared component contract in `RQ_Specified/A5_A11_shared_component_contract/` | Assistant | Owner requested the folder, branch and execution | Stages 1 to 3 executed; stage 4 is the owner's | Both questions need one frozen partition to stay comparable |
| 2026-09-25 | Developmental source, partition rule, Slc4a11 exclusion, source-defined lesion module | Assistant | Owner, at stage 4 | Retained as frozen | Rule committed before any intersection was computed; see the source audit and the stages 2 and 3 report |
| 2026-09-25 | A11 test design | Assistant, as the recommended option | Owner, at stage 4 | Pre-register the test in the Kim 2020 cohort and run only its eligibility gates first | The lesion module is identical to one already scored in the 23-patient cohort, so that cohort can serve only as discovery |
| 2026-09-25 | A5 path | Assistant, as the recommended option | Owner, at stage 4 | Audit a replicated adult injury time course before any scoring | A source-defined developmental list needs adult injury animals, not neonatal ones, and local data hold too few |
| 2026-09-25 | Register cards for A5 and A11 | Assistant, as the recommended option | Owner, at stage 4 | Update both on a new branch and pull request | Their readiness text predates the contract |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-25 | The assistant's A6 recommendation | Ranked by feasibility; the question is artifact-adjacent | Owner rejected it |
| 2026-09-25 | The draft contract's single coverage gate on ortholog mapping | The completed run applies the gate to the assayed fraction, which also loses genes at assay presence, and adds a unit floor | Assistant corrected it on inspection, before any freeze |
| 2026-09-25 | The first stage 3 run | Three of 33 precedent checks failed because it read the raw deposit rather than the post-QC object the precedent scored; it refused to report | The script's own fail-closed check; the attempt is preserved |
| 2026-09-25 | The A11 pre-registration's discovery reference | It cited the discovery run's narrower type 2 label; the run's own primary is its broad type 2 compartment label, which the register quotes | Assistant corrected it after the gates and before any Kim score, in a separate commit; the first power output is preserved |

Result: A11 is eligible for its test and A5 is not eligible for confirmation, for
want of independent neonatal animals. At the level of the source lists the two
questions need disjoint pairwise components, so the contract's "one shared
baseline" wording overstates what the lists support. No expression score was
computed and no claim grade changed. See the
[contract report](RQ_Specified/A5_A11_shared_component_contract/reports/STAGE2_3_REPORT.md).

Stage 4, decided by the owner the same day from a four-question selection. The
owner chose the assistant's recommended option in every question: retain the
frozen modules; test A11 in the Kim 2020 cohort after pre-registration and
eligibility gates; audit a replicated injury time course for A5; update both
register cards. Choosing a recommendation is the owner's decision, and it is
recorded as such; the options were written by the assistant, so this log names
them as its proposals.

## 38. Rewrite A2 around delivery rather than abundance, and structure its analysis (26 September 2026)

Asked what the real hypothesis for A2 was, the assistant reported that the card's
source-ranking question was already closed by the repository's own record, and
that the hypothesis underneath it concerns delivery rather than abundance. The
owner then asked for the card to be rewritten around that hypothesis and for the
analysis to be structured stepwise. Nothing was computed: no endpoint was scored
in either dataset and no claim row changed.

The argument for the reframing is that seven register rows answer the abundance
question and none supports a hierarchy (C37, C39, C40, C45, C48, C49, C50), while
C51 records why a seventh comparison would fail the same way. The mechanism
literature places the rate-limiting step in the recipient: amphiregulin activates
integrin alphaV on mesenchymal cells and releases bioactive TGF-beta from latent
complexes (Minutti et al. 2019, doi:10.1016/j.immuni.2019.01.008). A ligand that
converts a store the recipient already holds predicts the nulls C49 and C50
recorded, which is a prediction the reframed question can fail rather than a
rescue of the old one.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-26 | A2 framing | Assistant, in answer to the owner's question | Owner asked for the rewrite | Card rewritten around delivery; the abundance record is preserved in the rationale with its claim identifiers | Seven register rows close the abundance question; the mechanism names a different observable |
| 2026-09-26 | Analysis folder `RQ_Specified/A2_areg_source_delivery/` | Assistant | Owner requested the structure | Six stages declared, stage 1 authorized, nothing scored | The test is readable only if its endpoint and rule are frozen first |
| 2026-09-26 | Primary endpoint | Assistant | Pending owner retain or reject | Human Hallmark TGF-beta signalling, with the repository's five-gene fibroblast activation score as the co-primary | Both were defined outside this screen; the second carries the C50 and C51 precedent |
| 2026-09-26 | Precise absence | Assistant | Pending owner retain or reject | Declared unavailable at this design, before any test | Four units and a partial knockout, with the Areg transcript falling 1.042 log2 CPM and remaining at 6.226 |
| 2026-09-26 | Leg 2 in GSE136831 | Assistant | Pending owner retain or reject | Reuse the trial E6 instrument unchanged and change only the predictor | A new estimand in a cohort that already returned a null on the old one, with the C51 depth rule applying unchanged |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-26 | The assistant's first statement that the ligand-specificity contrast was matched within plate 3 | The design table places HBEGF on plate 4, so that contrast crosses plates; the plan labels it secondary and weaker | Assistant corrected it from the deposit before the plan was written |
| 2026-09-26 | A multi-agent workflow for this framing task | The deterministic reading and drafting did not need agents; three review lenses were applied to the drafts instead | Assistant, under the owner's cost rule |

The abundance question is not retired and no claim is re-graded. What changed is
which observable A2 commits to, and the plan states before running that leg 1 is a
within-screen association while preparation independence is unresolved, and that
leg 2 may be refused by its own depth control, in which case the refusal is the
result.

### A2 stages 1 and 2, 26 September 2026

The owner authorized stages 1 and 2 in one instruction, so the retain step the plan
placed between them was exercised as a single authorization rather than skipped. Both
stages computed no endpoint: the human sheet pass read gene symbols only, and the
freeze read covariate tables. The stage 1 script reproduces A10's recorded validation
on five genes and all 886 mouse library totals before extending the metric, and it
refuses to continue on any of seven stop rules.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-26 | Stage 1 execution | Owner instruction | Owner | Run, and all seven stop rules passed | The audit is the gate the plan placed before any freeze |
| 2026-09-26 | Stage 2 freeze | Assistant, from the stage 1 findings | Pending owner retain or reject | Frozen in a separate file, leaving the original contract unedited | The contract's recorded hash must keep verifying, so the freeze supersedes it only where it says so |
| 2026-09-26 | Depth handling | Assistant | Pending owner retain or reject | Keep every well in the primary and declare two depth-restricted sensitivities plus an interpretability floor | Excluding wells would change the rank universe, and the Areg wells are systematically deeper than their units |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-26 | The Erbb4 contrast declared in the contract | Its mouse transcript is 0.367 log2 CPM when not targeted and exactly zero when targeted, so there is no receptor to remove | Assistant dropped it at the freeze, on stage 1 evidence, before any endpoint existed |
| 2026-09-26 | The control wells' role as the unperturbed anchor | Four of the eight plate-3 control wells hold fewer than 100,000 fibroblast counts | Assistant downgraded it to descriptive context at the freeze |
| 2026-09-26 | The contract's wording "epithelial read fraction" | Ambiguous between the species read assignment and the count-based fraction; the freeze fixes the count-based one, from the same counts the endpoint uses | Assistant clarified it at the freeze |

The depth asymmetry is recorded as making the declared one-sided test conservative
rather than permissive, because a depth artefact on a mean log2 CPM score is expected
to push it upward while the prediction is downward. That is an expectation, so the
freeze requires stage 3 to report the observed depth association next to the result.

### A2 first freeze withdrawn after review, 26 September 2026

Three independent review lenses were run over the A2 documents, on biological and
literature accuracy, on statistical validity and pre-registration integrity, and on
internal consistency. They returned 17, 21 and 17 findings, six blocking, and converged
on two. In response the assistant ran a fibroblast-side covariate pass, which supplied
the decisive number, and then verified every accepted claim against the deposit or this
repository's own tables. No endpoint was scored under either freeze.

The first freeze is withdrawn, preserved unchanged, and replaced. The full argument is
in `RQ_Specified/A2_areg_source_delivery/reports/STAGE2_WITHDRAWN.md`.

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-26 | The first stage 2 freeze, its rank statistic, its exact null, its critical rank sum of 64 and its alpha | The four replicate units are copies of one plate layout with Areg always at well F07, so there is no randomization behind a uniform-rank null; 50 of 53 plate-3 targets sit at one fixed position | Assistant withdrew it on the statistics lens finding, verified against the deposit, before any score |
| 2026-09-26 | The claim that removing mouse Areg removes what the fibroblast can receive | The unedited human fibroblasts transcribe AREG at 9.846 mean log2 CPM in 99.2 per cent of plate-3 wells, above the mouse epithelial Areg removed; the repository's own cited paper (Zhou 2012) shows fibroblasts make it | Assistant measured it in a stage 1 addendum prompted by the biology lens, and withdrew the necessity claim |
| 2026-09-26 | The claim that leg 1 distinguishes delivery from abundance | One source compartment and no spatial variation in a well, so the distinguishing clause has no variance to test; the contrast moves to the spatial layer | Assistant restated leg 1 as a source-contribution contrast |
| 2026-09-26 | The Hallmark TGF-beta set as primary endpoint | It is a pathway-membership set with 16 negative regulators among 54 members and none of the five activation genes, and it is not what either cited paper measured; the five-gene activation score is | Assistant promoted the activation score and demoted the Hallmark set |
| 2026-09-26 | TDTOMATO alone as the control set | TIGIT is the article's own in-plate control at six wells per unit, already recorded in A10's source design check | Assistant adopted TIGIT plus TDTOMATO, eight control wells per unit |
| 2026-09-26 | Epithelial fraction as a primary covariate | Epithelial abundance plausibly lies on the causal path from the knockout to the fibroblast read, and about a fifth of reads are unassigned to either species | Assistant demoted it to a two-sided sensitivity with a mediation-ambiguous reading declared |
| 2026-09-26 | The consistency requirement presented as added stringency | Its exact size equalled the rank-sum size, 0.04903, so it added none | Assistant recorded the arithmetic and dropped the claim |
| 2026-09-26 | ERBB3 and ERBB4 as tests of AREG reception | Neither binds AREG; they bind neuregulins, and ERBB4 also has no receptor to remove here | Assistant reclassified them as non-AREG-receptor perturbation controls |
| 2026-09-26 | Leg 2 as a declared test | The logged trial E6 table already records the activation score against fibroblast depth at rho 0.4116 and fibroblast EGFR at 0.4918, so the inherited gate is likely to refuse it, and the machinery genes are themselves TGF-beta inducible | Assistant reclassified leg 2 as exploratory and required a co-regulation control |
| 2026-09-26 | The stage 1 report's "all seven stop rules", its count of three sub-threshold wells, and its ranking of Egfr as the weakest contrast | The plan declares four stop rules and seven audit items; six axis wells fall below the adopted floor; Erbb2 clears it in one unit of four | Assistant corrected the report in place, leaving its tables unchanged |
| 2026-09-26 | The C37 row's proposition, and "none supports a source hierarchy" | The row stated the inverse of the registered proposition and carried its grade; C45 records a ranking in the opposite direction, so the closing statement is about a depth-independent epithelial hierarchy | Assistant restored the register's wording |

The owner retain step the plan placed between stages 1 and 2 was not exercised against
stage 1's findings, because both stages were authorized in one instruction that
predates them. The second freeze is therefore recorded as provisional, and stage 3 is
not authorized.

What survives is narrower and still worth running: a descriptive effect size against
the screen's own controls, with a direction count and no p-value, which is what the
register card promised before the first freeze overreached. A2's decisive experiment
moves to the spatial layer, and the audit also produced the first evidence in this
repository that the receiver carries the machinery the mechanism needs.

### A2 legs 1 and 2 executed, 26 September 2026

The owner authorized stages 3 and 4. Leg 1 ran under the second freeze, which forbids a
p-value; the leg 2 specification was declared and committed before leg 2 ran, and
classified exploratory in advance.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-26 | Leg 1 execution | Owner instruction | Owner | Run under the second freeze, effect size only | The withdrawn rank test had no randomization behind it |
| 2026-09-26 | Leg 2 execution | Owner instruction | Owner | Run as declared exploratory | The inherited depth rule was recorded in advance as likely to refuse it |
| 2026-09-26 | Reading of the Areg null | Assistant | Pending owner retain or reject | No detectable epithelial contribution on top of an unremoved autocrine source; not absence | The recipient transcribes AREG at 9.846 against the 7.267 removed, and the knockout is partial |
| 2026-09-26 | Reading of the Itgb6 result | Assistant | Pending owner retain or reject | A proposal, not a result: one well per target per unit at a fixed position | It survives the eligibility floor, the epithelial adjustment and a culture check, but the design cannot separate target from position |
| 2026-09-26 | Claim wording | Assistant | Owner grades, and no row is added here | Four sentences proposed in the synthesis | Grading is the owner's decision |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-26 | The leg 2 correlation of +0.433 at nominal p 0.044 | The frozen C51 rule refuses the pair: the composite tracks fibroblast depth at 0.770 and the outcome at 0.412 | The rule, declared before the pair was computed |
| 2026-09-26 | The IPF stratum of leg 2, which the letter of the rule does not refuse | The predictor still tracks depth at 0.717 there, so the correlation remains a depth comparison | Assistant refused it post hoc, recorded as a tightening in the conservative direction only |
| 2026-09-26 | The first run of the post hoc culture check | It joined the imaging table on the library prefix where the deposit uses a plate prefix, so every imaging field was empty | Assistant preserved it with a note and corrected the join |
| 2026-09-26 | The first leg 2 run | It read the gene table's Ensembl column and kept the quoted header, so the row count disagreed with the matrix and the script refused | The script's own shape check; corrected to read the symbol column exactly as trial E6 does |

Two by-products are worth the record. The leg 2 instrument reproduced C50 exactly at
-0.150, so the refusal is not a broken pipeline. And the screen's fibroblasts carry the
machinery the cited mechanism needs, with integrin alphaV at 5.835, ITGB1 at 9.487, ITGB8
at 5.254, LTBP1 at 9.757 and EGFR at 5.389 mean log2 CPM, which is the first evidence in
this repository that the receiver is equipped and which bears on C36 without settling it.

### A2 leg 2 read on a common molecule budget, and the register gates audited, 27 September 2026

The owner asked for two pieces of work and told the assistant to avoid overlapping the
session that owns A15. Neither piece overlaps it: A15's own gate was excluded from the audit
and its search report is cited instead.

Leg 2's refused pair was re-measured with the C37 treatment, declared and committed before
anything ran. The standardisation brought the predictor's depth coupling from 0.770 to 0.232
and the outcome's from 0.412 to 0.341, so the frozen C51 rule no longer refuses the pair, and
the correlation then falls from 0.433 at nominal p 0.044 to 0.293 at p 0.186. The rule was
protecting against depth and nothing survives it. The result is strengthened by an internal
pattern: the correlation tracks how much of each library the measure consumes, giving 0.230,
0.293, 0.379 and 0.433 as the budget rises from 500 to 2,000 and then to the whole library.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-27 | Leg 2 second pass | Owner instruction | Owner | Run with the C37 common-budget treatment, declared first | A raw detection fraction over 52 to 608 cells across a 2.1-fold depth spread is largely a depth statistic |
| 2026-09-27 | Primary budget | Assistant | Pending owner retain or reject | Kept at 1,000 molecules as declared, despite a limitation found later | Changing it after seeing the problem would be indistinguishable from choosing a budget that reads |
| 2026-09-27 | Register gate audit | Owner instruction | Owner | One pass over GEO, two declared queries per gated question, verdicts written by hand | Eleven questions were gated on data nobody had checked against an archive |
| 2026-09-27 | A15 excluded from the audit | Assistant | Owner instruction to avoid overlap | Cited the owning session's search report instead | Repeating it would waste effort and risk a contradictory verdict |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-27 | The assistant's first version of the measure test | It asserted rate invariance at the 1,000-molecule budget. The formula was right and the assertion was wrong: invariance holds only when the budget is small relative to the smallest library, and this deposit is floored at exactly 1,000 | Assistant corrected the test to characterise the regime, before any result was reported |
| 2026-09-27 | Reading the 2,000-molecule sensitivity as the stable one | It drops 470 of 4,648 cells and sits near the measure's ceiling for typical gene rates, so its stability is saturation rather than invariance | Assistant recorded it as declared but not as the better estimate |
| 2026-09-27 | Any claim that A3 is now runnable because a deposit exists | GSE303646 matches A3's stated gate, but A3's composition-versus-state boundary is still set by annotation granularity, which is what retired A6 | Assistant recorded the deposit and withheld the recommendation pending a re-specified endpoint |

The audit's outcome: one gate met as written (A3, GSE303646), three with named candidates
whose eligibility is arithmetic (A5, A11, A13), one with half its gate met (A1), and six
blocked with a constraint that now fits in a sentence (A4, A7, A8, A9, A12, A14). Titles in
the candidate table are stored verbatim, including the archive's own punctuation, because
they are retrieved evidence.

### A13 coverage counted, 27 September 2026

The owner asked for the triad arithmetic after the gate audit named it the cheapest of the
three eligibility checks. It is counts only: nothing was fitted and no association estimated.

The pass reproduces all 240 per-donor flags the earlier trial recorded before reporting
anything new, which required recovering a rule that trial never wrote down. The Kim lung
adenocarcinoma cohort, the only one on disk never counted, gives zero complete paired triads
at the 50-cell floor under the epithelial definition the two IPF cohorts used, and three under
a wider one, against a ten-patient floor.

The zero has a definitional cause worth recording: every one of the eleven tumour samples holds
exactly zero cells labelled type 2, because the deposit annotates tumour-sample epithelium as
tumour states. So a paired tumour-versus-normal contrast and a type 2 epithelial compartment
cannot coexist in that deposit at any cohort size. Under the wider definition the binding
constraint is fibroblast recovery, with the largest fibroblast label reaching 50 cells in ten
of twenty-two samples at a median of 32.5, which is a property of the assay rather than of the
cohort.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-27 | A13 coverage count | Owner instruction | Owner | Run, counts only | The card says coverage is next and not mediation fitting |
| 2026-09-27 | The triad rule | Assistant, recovered from the earlier trial | Pending owner retain or reject | Single-label as primary, pooling as a declared sensitivity | The number the card quotes was produced under the single-label rule, so changing it would make the new count incomparable |
| 2026-09-27 | Epithelial compartment for the new cohort | Assistant | Pending owner retain or reject | Type 2 only as primary, tumour states as a declared sensitivity | Using all epithelium would inflate the new cohort relative to the two the gate already quotes |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-27 | The first coverage run, which assumed a pooled-label rule | It reproduced 230 of 240 earlier flags and disagreed on 10, every disagreement in the direction of counting more cells | The script refused at its own reproduction check and reported no new count; the attempt is preserved with a note |
| 2026-09-27 | Any reading of the three patients under the wider epithelial definition as usable coverage | Three cannot support a joint model, and the compartment is no longer the one the six and three were counted with | Assistant recorded both counts and fitted nothing |

Two sentences are proposed for the register and neither is added. The measurement contract now
records the label-level rule so the next count does not have to rediscover it.

## How outputs were reviewed

### A1 adaptive continuation, 25 September 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-25 | Recover exact CD44 identities, run paired contrasts/interaction, verify HPCS definitions and link established analysis references | Codex | Owner authorized adaptive continuation and reference checks; scientific interpretation remains for review | Execute newly eligible work and document completed, pruned and external-input branches | SRA originals resolve the RNA identity hold; author notebooks resolve annotation dependence |

| Date | Reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-25 | Earlier CD44 identity hold and HPCS definition-notebook hold | Exact SRA original filenames recover all columns; a new bounded scope retrieves the two pinned notebooks | Codex revised status from new primary evidence within owner-authorized continuation |
| 2026-09-25 | Potential interpretation of stringent HPCS labels as independent annotation support, and shared markers as disease-specific validation | Every stringent change is abstention; seven transported markers change in both CD44 genotype contrasts | Codex narrowed interpretation from executed source/data audits; historical numerical outputs retained |
| 2026-09-25 | Replicated IRE1 single-cell follow-up from the newly identified study | Each treatment group is one pooled GEM library; GSE243129 is a different neonatal experiment | Codex applied the prespecified unit/design gate before assay acquisition |

The [closure report](RQ_Specified/A1_transitional_epithelial_state_distinction/reports/EVIDENCE_CLOSURE_REPORT.md)
and [reference map](RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md)
record evidence dependencies and uncertainty. This is an authorized analysis
delivery, not an invented human acceptance of the scientific conclusions.

Every run writes its decisions to machine logs (`decisions.json`,
`analysis_log.txt`), and the original per-dataset reports and pipeline record are
*generated* from those artefacts. Later manually maintained narratives can
drift; decision 32 adds explicit generated summaries and selected numeric
bindings with stated coverage. A claim I could not trace to an artefact was
treated as unverified and removed. Work was reviewed between sessions against
[`PROGRESS.md`](PROGRESS.md), landed through pull requests, and known issues
were carried forward in writing rather than dropped.

### A1 regulatory and outcome continuation, 25 September 2026

The owner requested all three remaining avenues and established-analysis
checks, especially before regulation-to-fate work. Codex recovered primary
identities and extended source analyses; the owner has not been represented
as accepting the resulting scientific conclusions.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-25 | HPCS animal crosswalk and Hopx harvest | Codex from Supplementary Table 4, pinned demultiplexing and Fig. 2 | Owner authorized continuation; Codex applied explicit-evidence rule | Resolve 22 mice and 14-week Hopx harvest; retain library/chase and current-reporter limits | Exact animal/library/driver matches replace alias-based uncertainty |
| 2026-09-25 | AP-1 regional outcome and culture/source reanalysis | Codex after checking established papers and source tables | Owner authorized all three avenues | Use mice for nested microscopy; keep culture differentiation, regulatory suppression and selected RNA contrasts separate | Program suppression is region-dependent and not equivalent to fate rescue |

| Date | Reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-25 | Generic beneficial interpretation of AP-1/transitional-state suppression | Mouse-level HOPX responses have opposite regional directions; only three mice per genotype | Codex narrowed claims from source-informed reanalysis |
| 2026-09-25 | Assumption of 317 unique HNF1B-only genes | First new numerical launch stopped before output; four source symbols are duplicated | Codex preserved raw rows and reported 313 unique genes |
| 2026-09-25 | TP53 shared significant genes described as uniformly upregulated | Source values contain 493 shared increases, 266 shared decreases and 109 opposite directions; counts remain private | Codex audited signs and declined an unsupported interaction fit |
| 2026-09-25 | Adjacent-time ATAC correlation and large PATS raw-read processing | Shared middle time point, ambiguous age-control metadata and persistent injury/sort confounding would not resolve the proposed causal question | Codex pruned dependent work under the owner's adaptive instruction |

See the [report](RQ_Specified/A1_transitional_epithelial_state_distinction/reports/REGULATORY_FATE_REPORT.md)
for source definitions, checks and exact remaining requirements. Source requests
are drafted but unsent; the concise Notion page was not expanded.

## Where the honest failures live

- The refuted Scrublet/AT0 over-removal claim, with both rounds of the test:
  [`docs/DOUBLETS_AND_SCRUBLET.md`](docs/DOUBLETS_AND_SCRUBLET.md)
- The three contradicted cluster annotations, flagged in
  `Research Article/gate1_01_niethamer_2025/GSE262927/tables/cluster_annotation_proposals.csv`
- Thresholds that never bound, doublet calls that are a ranking rather than a
  detection, and every other caveat: [`FINDINGS.md § 6`](FINDINGS.md#5--negative-results-and-self-audits)
  and the per-dataset reports


## A5/A11 review revisions, 25 September 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-25 | Revise A5/A11 designs and proceed with biological rationale | Codex review | Owner requested proceeding with revisions and rationale | Authorized implementation and analysis; final scientific acceptance pending review | Correct provenance, estimands and claim scope before scoring |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-25 | A5 independence claim for Strunz-filtered modules | Supplement identifies the same high-resolution cohort for marker selection; negative selection is data-dependent | Codex source review; owner requested revision |
| 2026-09-25 | A11 mean estimand with Wilcoxon and overlapping transport/absence categories | HL targets location/pseudomedian; positive small effects could satisfy both labels | Codex review; owner requested revision before scores |
| 2026-09-25 | Universal baseline, biologically specific list names and credibility from low power | List overlap and test difficulty do not establish a programme, specificity or credibility | Codex review; owner requested biological rationale |


A5/A11 execution outcome: A5 external-signature recruitment is positive in 24
mice and after external identity/control exclusions. A11 lesion association
replicates in eight patients; beyond-shared BH q=0.0546875 leaves the stronger
claim unresolved. No threshold, subtype or baseline was retuned. Twenty-eight
independent numerical/provenance checks passed; the figure was inspected. A
matrix-orientation assertion and cross-language boolean parsing stopped two
technical attempts before scientific outputs; their corrections are documented
in the result report. Scientific acceptance remains for owner review.

## Status synchronization and logical review, 26 September 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-26 | Synchronize merged status, then check the analysis rationale | Codex status review | Owner explicitly requested synchronization and rationale checking | Update current entry points and record an evidence-grounded logic review; no new scientific fit | A5/A11 and A10 results were merged while handoff/index text still queued their execution |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-26 | A10 cell-autonomous/niche separation, unique outcome novelty and total-tissue wording | Species separation identifies RNA origin, A1 already includes non-RNA outcomes, and the primary is mean organoid area | Codex corrected rationale under owner-authorized review; scientific acceptance not inferred |
| 2026-09-26 | A10 conservative cross-scale margin and complete assay-validation language | Outcome centring changes SST; targeted-transcript reductions do not verify every edit or a prespecified imaging control | Codex code/evidence review; original specifications and numbers preserved |
| 2026-09-26 | A10 implied protocol completeness and exhaustive metadata exclusion | Secondary BH inference and retained-model comparisons were not fully implemented; one sample record cannot exclude metadata elsewhere | Codex recorded limitations and a diagnostic-first follow-up order; no retrospective test invented |
| 2026-09-26 | Shared-contract README's universal shared component and unchanged A5 input claim | The partition has two pairwise overlaps; revised A5 tests use additional external Guo modules | Codex aligned the entry point with the existing biological logic and completed results |

The [review](docs/LOGICAL_RATIONALE_REVIEW.md) names the supporting reports,
specifications, code and output tables. It retains the A5/A11 association results,
qualifies the small A1 regional comparison and narrows A10's descriptive claim.
No historical claim grade or numerical artifact was changed. Notion and source
paper notes were not expanded; no author request was sent.

## A10 adaptive follow-up, 26 September 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-26 | Execute the follow-up after the logical review | Codex review sequence | Owner explicitly requested proceeding | Audit design first, freeze a new descriptive specification, then execute eligible block/plate comparisons | Resolve concrete assumptions before further model expansion |
| 2026-09-26 | Restrict plate holdout to joint plate/target shift; prune unidentifiable and functional extensions | Codex from phase A diagnostics | Codex applied the owner-authorized adaptive gates; scientific acceptance remains for review | Execute bounded comparisons, stop unsupported target/plate causal claims | Only four targets span plates, preparation IDs remain absent, and guide sequences do not measure editing efficiency |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-26 | Initial exact-match assertion using GEO titles as library IDs | Titles are descriptive; explicit Library name fields identify all 886 samples | The first audit attempt stopped before output; Codex corrected parsing without changing eligibility |
| 2026-09-26 | Plate-only interpretation of transfer and expectation that proliferation alone explains the signal | Plate and target mix change together; the remaining growth block adds conditional information | Prespecified design and model comparisons narrowed the interpretation |
| 2026-09-26 | Reading a 42.39% relative error reduction as reliable absolute prediction | Full-growth held-out R-squared remains negative on three of four plates | Independent verification and absolute-error diagnostic; no result or threshold was changed |

The [follow-up report](RQ_Specified/A10_organoid_growth_outcome/reports/FOLLOWUP_RESULTS.md)
records the biological logic, prospective commits, all comparison rules and
adaptive stopping. Original results and historical claim grades remain unchanged.

A final bounded design-source check established TIGIT's author-designated control
role. It did not resolve preparations/calibration: detailed supplemental methods
could not be inspected through the bounded retrieval. The access record preserves
that limitation; it is not a claim that the supplement lacks those facts. No
study note, roadmap-reading update, author contact or model retuning occurred.


## A0 scientific pilot and adaptive stop, 26 September 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-26 | Finish the scientific pilot, then open a PR | Owner request | Owner explicitly authorized execution and PR creation | Recover eligible cohorts, freeze discovery/transfer, execute and verify the bounded pilot | A0 existed only as a local feasibility audit |
| 2026-09-26 | Substitute the viable early airway and late-enterocyte-progenitor comparisons before effects | Codex source/coverage audit | Codex within authorized adaptive analysis | Retain original cell/unit floors and 20–50-gene requirement; disclose changed biological scope | Original developmental and gut comparisons did not satisfy coverage |
| 2026-09-26 | Stop after failure of the mature intestinal endpoint | Codex implementation of the pre-V1 stopping rule | Codex applied the owner-authorized adaptive sequence; scientific acceptance pending review | Report negative primary transfer; prune P4 and avoid result-dependent rescue | Both endpoints are required; only 1/3 mice is positive against mature enterocytes |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-26 | Treating the local feasibility audit as a completed scientific pilot | No programme had been learned or transferred | Source/run audit; original bytes and results preserved |
| 2026-09-26 | Counting captures as donors or misidentifying similarly named UCSC studies | Biological replication and source identity determine eligibility | Author crosswalk and GEO identities checked before effects |
| 2026-09-26 | Two slow count-preparation implementations | Scattered storage and float parsing of integer text dominated runtime | Performance-only corrections before effects; partial attempts preserved |
| 2026-09-26 | Calling a positive stem comparison successful cross-tissue transfer | The mature endpoint fails, so a transient intermediate peak is not established | Fixed two-endpoint criterion, independently verified |
| 2026-09-26 | Equating transfer failure with absence of all conserved fate programmes | Only one RNA instrument, operational comparison and three transfer mice were tested | Interpretation narrowed; no causal or universal claim promoted |

The [result](RQ_Specified/A0_conserved_epithelial_transition_program/reports/PILOT_V1_RESULTS.md)
records all unit effects, freezes, limits and verification. The owner authorized
work and PR creation; final scientific acceptance is not invented. Historical
claim grades, original feasibility tables and unrelated primary-checkout work
remain unchanged.


## A15 proposed from A2's integrin lead, 27 September 2026

A2 closed with one measured lead that was outside its own scope: epithelial Itgb6
knockout lowered the frozen fibroblast activation score while the ligand arm did not.
The owner asked whether that deserves its own register question and, if so, for it to
be structured the way this repository structures questions. **Everything below is
assistant-proposed and pending the owner's retain or reject.** No claim row was added,
no grade changed, and the register still ends at C168.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-27 | Whether the Itgb6 lead becomes a register question | Assistant, in answer to the owner's question | Pending owner retain or reject | Recommend a new identifier, A15, with three alternatives rejected on the record | It carries its own biological proposition and its own decision, which is this register's own test for a full identifier |
| 2026-09-27 | The scope of the question | Assistant | Pending owner retain or reject | The partition of the epithelial output, not whether the integrin activates TGF-beta | The mechanism is established since 1999 and has been through two clinical programmes; a register question that re-asks it adds nothing |
| 2026-09-27 | Readiness | Assistant | Pending owner retain or reject | Blocked, with the blocking constraint named as the absence of any deposited measurement of activated TGF-beta under an integrin perturbation | A blocked question that names its missing measurement is more useful than one that says more data are needed |
| 2026-09-27 | The stage 1 eligibility gate | Assistant | Pending owner retain or reject | Six conditions frozen before any candidate dataset is opened, with a transcript score explicitly excluded as the activation readout and no pre-declared alternative | A later session must not be able to relax the readout in order to get a run; the A2 first-freeze withdrawal is the precedent |
| 2026-09-27 | Ownership of the founding observation | Assistant | Pending owner retain or reject | It stays A2's; A15 opens with no evidence of its own and has no `tables/` directory | The register's own rule is that a new biological interpretation does not inherit a historical claim's status |
| 2026-09-27 | GSE190821, the only runnable deposit | Assistant | Pending owner authorization | Named as a side-branch that bounds one rival, explicitly outside the staged test | It blocks integrin beta6 in vivo with four treated against seven control mice, but has no activation readout and no separated fibroblast compartment |
| 2026-09-27 | Branch and pull request base | Assistant | Assistant, under the owner's branch and PR rule | Branched from `Claude/a2-delivery-hypothesis` and based the pull request on it rather than on main | The workspace cross-links A2's stage 3 and stage 5 reports, which exist only on that branch while PR #85 is open; if #85 is rejected, this work needs rebasing |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-27 | Keeping the lead as a third leg of A2 | It is not an amphiregulin question, and A2's second freeze forbids adding an arm after the endpoint has been read; that would put a post hoc arm inside a closed pre-registration | Assistant, before the workspace was written |
| 2026-09-27 | Folding the lead into A9 | A9 owns the fibroblast EGFR; A15's receptor is the recipient's TGF-beta receptor and its perturbation is on the epithelium. The two share a compartment, not an estimand | Assistant |
| 2026-09-27 | Recording it as an enabling entry like A12-S1 | An enabling entry supplies a shared input to questions that keep their own decisions; this one has a proposition and a decision of its own | Assistant |
| 2026-09-27 | Recording it only as a FINDINGS lead with no card | A lead with no card has no prohibitions attached, and the two specific risks here are naming a transcript score as a TGF-beta activation measurement and reading an unrandomized single-well contrast as a mechanism | Assistant |
| 2026-09-27 | The assistant's first framing, "does epithelial integrin-mediated TGF-beta activation drive fibroblast activation" | Established outside this repository since Munger 1999, with a blocking antibody shown to prevent murine bleomycin fibrosis in 2008; the register would have been re-asking a settled mechanism | Assistant corrected it from the primary literature before the card was written |
| 2026-09-27 | Using the GSE307128 series summary | The sibling deposit's summary states the source paper's conclusions, and roadmap paper 14 is recorded as unread by the owner; only structural facts were retained, and the summary text is not quoted or relied on anywhere | Assistant, under DEVELOPMENT decision 21 |
| 2026-09-27 | Proposing GSE190821 as a test of the hypothesis | It fails gate conditions 3, 4 and 5: no activation readout, no separated fibroblast compartment, no ligand arm. Kept only as a rival-bounding side-branch | Assistant, applying the gate it had just frozen |
| 2026-09-27 | A whole-lung activation-signature run in GSE190821 | Whole lung confounds the fibroblast compartment with fibrosis extent, and reduced collagen under this antibody is already published, so the run would re-measure a known result | Assistant; recorded as feasible but non-discriminating and not recommended |
| 2026-09-27 | Editing any file under `RQ_Specified/A2_areg_source_delivery/` to add a cross-reference | Those files were under the owner's review in PR #85 when A15 was written, and adding to a document under review changes what is being reviewed. PR #85 has since merged; the decision stands and A15 remains discoverable from the register table and the `RQ_Specified` index instead | Assistant |
| 2026-09-27 | Asserting cross-species conservation of the activating motif from equal sequence lengths | Human and mouse TGF-beta1 proproteins are both 390 residues and integrin beta-6 is 788 and 787, but no alignment was performed; equal length is not conservation | Assistant narrowed its own wording; recorded as a carried assumption and as an open, small, feasible layer item |
| 2026-09-27 | A multi-agent workflow for this task | The reading, the repository searches and the drafting were deterministic, and the judgement calls were few enough to make in the open | Assistant, under the owner's cost rule |

The [registration argument](RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/REGISTER_DECISION.md)
states the case against the identifier as well as the case for it, including that nothing
can be run, that the mechanism is old, that the founding observation rests on three
readable units at one fixed well position, and that the headline contrast sets one
measured decrease against one unbounded null. The
[search report](RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/PUBLIC_DATA_SEARCH.md)
records every query with its hit count and states that keyword search over indexed
metadata cannot prove absence. The owner is being asked for three decisions: the
registration itself, the scope wording, and whether to spend a run on the side-branch.


## A15 rival-2 side-branch executed in GSE190821, 27 September 2026

The owner authorized the third of those decisions: run the GSE190821 epithelial arm to bound
rival 2. It ran, and it took **three freezes** to get a design that could be executed
honestly. **Two were withdrawn on adversarial review with nothing scored**, which is the
second and third time this repository has withdrawn a freeze before a value was read. The
question A15 itself still has no result of its own, no claim row was added, and the register
still ends at C168.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-27 | Run the side-branch | Assistant proposal, in the A15 rationale | **Owner instruction** | Executed under a frozen specification, in four stages, with the freeze committed before any value was read | It is the only runnable item in A15, and it bounds a rival rather than the hypothesis |
| 2026-09-27 | Endpoint, third attempt | Assistant, after two withdrawals | Pending owner retain or reject | A frozen epithelial identity and transitional panel, plus an endpoint-free omnibus divergence test | An omnibus question cannot be defeated by a curated set's construct validity, which is what defeated the first two |
| 2026-09-27 | Engagement control | Assistant, after the review found the paired input | Pending owner retain or reject | A frozen whole-lung collagen programme on the paired input, with its direction taken from Horan 2008 | A15 gate condition 1 requires a recorded validation that the perturbation took effect, and the first freeze had dropped it |
| 2026-09-27 | Rival 2 restated | Assistant | Pending owner retain or reject | The rival is an indirect, epithelium-mediated route, not a TGF-beta-independent one | Both papers cited for the original wording attribute their phenotypes to loss of TGF-beta activation, in their own titles |
| 2026-09-27 | The vacuous A0 rule | Assistant | Assistant, fail-closed | The frozen rule is reported as written and its vacuous case recorded, rather than reinterpreted after the fact | Changing a decision rule after seeing that it misfires on the observed data is the thing pre-registration exists to prevent |
| 2026-09-27 | Whether to execute at all | Assistant, after the second review | Assistant, under the owner's instruction to proceed | Executed, with the freeze stating before the run that the likely outcome is the uninformative one | A design-limited result reported with its limits is a result; the branch names were rewritten so none of them can overclaim |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-27 | **The first freeze, withdrawn** | Its primary endpoint could not carry rival 2's axis by construction: A0's own discovery configuration excludes the surfactant and identity genes by name, and its overlap with A1's frozen epithelial panel for this deposit is exactly zero. It also declared only a null informative while establishing no engagement check, and its decision rule was a ratio whose numerator and denominator share an arm | Three adversarial lenses, each returning three fatal findings; every factual claim verified against the tracked files before acceptance |
| 2026-09-27 | **The second freeze, withdrawn** | Its omnibus statistic rejects with probability 1.000 under a pure dispersion change with no gene's mean moving, its Hodges-Lehmann interval covered 0.9418 against the 0.9714 it reported, it declared no direction for the contrast it tested, it put `Col1a1` in both the engagement control and the purity downgrade rule, and its positive branch waived the engagement control | A second three-lens red team; both quantitative claims reproduced by simulation here before being accepted |
| 2026-09-27 | The review's recommended metalloproteinase and surfactant panel | Morris 2003 and Koth 2007 attribute their phenotypes to loss of TGF-beta activation, so such a panel would measure TGF-beta-mediated consequences and would not separate the rival from the mechanism | Assistant, from the primary literature, against the reviewing lens |
| 2026-09-27 | Two factual statements in the committed stage 1 audit | The deposit does state genotype, bleomycin dose and the 3G9 schedule, and the paired whole-lung input makes immunoprecipitation purity computable rather than unverifiable. Both were corrected in an erratum rather than by editing the committed record | Design lens; verified against the deposit's own series summary |
| 2026-09-27 | The first execution attempt's `purity breaches: none` | The purity markers had never been mapped, because the Ensembl lookup was built at stage 1 and never extended to the panels the third freeze declares, so vacuous silence was being reported as a negative result. Script 01 now requests every declared symbol, script 02 fails closed when a declared panel does not map, and an uncomputed covariate forces inconclusive | Assistant, from the run record's own `mapped: 0` |
| 2026-09-27 | Two verification failures on score reproduction | The verifier standardised across eleven libraries while the third freeze scopes each composite to the libraries entering its own contrast, so it was comparing two different estimators. The verifier was wrong, not the analysis; no result changed | Independent recomputation through numpy and scipy |
| 2026-09-27 | Calling a positive result "rival 2 stays live" | Both the A15 mechanism and rival 2 predict an epithelial change, so a positive discriminates neither. The branch is renamed so the name cannot overclaim | Coherence lens; adopted |
| 2026-09-27 | A multi-agent workflow for the deterministic work | The download, join, audit, scoring, exact tests and verification are all scripted. Agents were spent on two things a script cannot judge: the adversarial review of each freeze before any value was read, three lenses each | Assistant, under the owner's cost rule, with the owner's later instruction to parallelise |

The [result](RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/RIVAL2_RESULTS.md)
records every number, its independent verification at 39 of 39 checks, and the sentence the
artefacts would support if the owner wants a claim row. The two withdrawn freezes stay
unedited so their bytes keep verifying, and both withdrawals are written up with the
simulations that justified them. Scientific acceptance is not inferred from execution.


## Branch cleanup and the LinkedIn removal, 27 September 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-27 | Delete every branch with nothing new against `main` | Owner question, "what is unnecessary" | **Owner instruction**, conditional on the branch holding nothing new | Six merged branches deleted on both local and origin, each verified at zero commits ahead of `origin/main` first, with `git branch -d` so an unmerged branch would have been refused | No active session was ongoing and their tips are all reachable from `main`, so the refs carried nothing |
| 2026-09-27 | Delete the two branches that did hold unmerged commits | Assistant reported that neither one's content was on `main`, against the owner's stated premise | **Owner instruction, after that correction** | `rq-framing-proposal` and `codex/linkedin-media-selection` deleted; their commits recorded as `0034245` and `cd18f97` for reflog recovery | The framing proposal was a plan the research-question rewrite in PR #69 had already executed, and the owner judged the LinkedIn work should never have been tracked in this repository |
| 2026-09-27 | Remove `docs/LINKEDIN_PROJECT.md` from `main` | Assistant, after the owner said the LinkedIn work should not have been in the repository | **Owner instruction** | The file is deleted and all five referring documents are corrected | It is personal-surface promotional material, which decision 27 keeps out of every tracked file |
| 2026-09-27 | The 2026-09-25 migration manifest entry for that file | Assistant | Assistant | **Left unedited** | Nothing asserts the file still exists: the manifest is only a fallback lookup for `recorded_file`. The entry records what the migration did at the time, which is still true, and superseded records stay in-tree by convention |
| 2026-09-27 | The historical sentences in decision 33 and in PROGRESS that described the draft | Assistant | Assistant | Kept as prose, with the link removed and the removal dated in place | Rewriting a historical record to hide that the draft existed would be worse than a dangling link; the validator's link check forces one of the two, and delinking keeps the history true |

| Date | Rejected or reworked output | Reason | Authority |
|---|---|---|---|
| 2026-09-27 | The premise that the two unmerged branches held work already on `main` | Checked before deleting: `codex/linkedin-media-selection` carried 40 lines absent from `main`, and `docs/RQ_FRAMING_PROPOSAL.md` did not exist on `main` at all. Reported, and the owner confirmed the deletion anyway with a reason for each | Assistant verified rather than accepting the premise |
| 2026-09-27 | Deleting the untracked working copies in the primary checkout wholesale | All 2,158 entries were classified first. 2,050 were cache artefacts origin/main already ignores and 92 matched main apart from line endings. 16 A0 files were set aside pending a check rather than deleted. Setting them aside was right; **the reason given for it was wrong, see the rejection log below** | Assistant |
| 2026-09-27 | Merging those set-aside A0 files into `main` through PR #92 | **Not merged. PR #92 was closed as contributing nothing**, once a three-lens review showed all sixteen were already preserved on main and the two decision records were already live there | Assistant, after verifying every claim the review made |
| 2026-09-27 | **REJECTED: the claim that 16 recovered A0 files were newer than main, and that decision records A0-015 and A0-016 appeared in none of main's A0 record files** | **Both statements were false.** A0-015 and A0-016 had been live on main since 26 September in the tracked `exploratory_decisions.json`. All 16 files were already preserved on main inside `history/exploratory_execution_artifacts.zip`, 16 of 16 identical once line endings are normalised, enumerated with hashes in the live `exploratory_publication_record.json`. The recovered `decisions.json` is byte-identical LF-normalised to main's `exploratory_decisions.json`: the pre-split copy, not a variant. The false claim reached `main` in PR #91 and was corrected here | Caught by a three-lens review of the follow-up merge, then verified directly against the deposit files before the correction was written |
| 2026-09-27 | **REJECTED: the duplicate `history/recovered_working_tree_2026-09-27` archive, and the four documents written to make it discoverable** | The archive preserved zero new bytes. Its own cross-check section was wrong on every entry: it compared against `documentation_migration.json`, an archive **record**, and never opened `exploratory_execution_artifacts.zip`, the archive **zip** sitting beside it with no sibling record. The accompanying edits to A0's README, PROGRESS, AI_CONTEXT and DEVELOPMENT asserted a verifiable falsehood, and one of them told future sessions to disbelieve main's own logged stage artefacts | Discarded before being pushed; PR #92 closed as contributing nothing |
| 2026-09-27 | **The triage method that produced the error** | It compared untracked files path for path against `origin/main`. A0 deliberately keeps `decisions.json` at the feasibility stage and `exploratory_decisions.json` at the exploratory stage, so a renamed and split file read as "newer than main", and content already inside a `history/` zip read as unpreserved. Any future triage must be content-addressed across the whole tree and across every archive in `history/`, with line endings normalised | Recorded in AI_CONTEXT so a later session does not repeat it |
| 2026-09-27 | Deleting `PORTFOLIO_SUMMARY.md` alongside the LinkedIn draft | It sits in the same `docs/README.md` sentence and may be the same category of personal-surface material, but the owner named only the LinkedIn file, and widening a deletion is the owner's call | Assistant kept to the instruction and raised the question instead |
## 27 September 2026: repository-wide rationale audit and context corrections

The owner requested challenging every RQ and question-specific trial, reconciling
contexts and guiding future work. Codex reviewed merged snapshot `329c07c` in a
separate managed worktree, preserving the older checkout and all scientific outputs.
The [audit](docs/audits/2026-09-27-rq-rationale/REPORT.md) records A0–A15, A12-S1,
the trial families, exact sampling-model probes and remaining logical gaps.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-27 | Rationale audit and current-context synchronization | Codex | Owner authorized the audit/synchronization; these interpretations are assistant judgments pending review | Correct current A2/A15 language and publish the shared architecture; preserve grades, frozen records and numerical outputs | Nonsignificance, enrichment and a conditional count probe were being read more strongly than their evidence permits |

Rejected or substantially revised assistant interpretations:

| Date | Prior output | Why revised | Review authority |
|---|---|---|---|
| 2026-09-27 | A2 no coupling and automatic 100-molecule next pass | Positive nonsignificant correlation does not establish absence; conditional fixed-K/N behavior does not prove marginal depth-standardization failure | Codex under the requested logical audit; no owner claim grade inferred |
| 2026-09-27 | A15 pure IP and elimination of a composition/epithelial-state rival | Marker enrichment and wide null intervals cannot establish purity, equivalence or absence of a mediator | Same audit authority; historical decision label and estimates retained |

No individual scientific claim acceptance, A15 registration approval, public-data
exhaustion or successful raw-data replication is implied by this review.


## 27 September 2026: authorized roadmap execution

The owner requested proceeding through the research roadmap with reports between packages.
The [execution record](docs/roadmap_runs/2026-09-27/README.md) distinguishes performed
metadata/source/counting work from stopped fits and future experiments. Codex recovered
the previously unread screen supplement, checked two A5 candidates, audited regulatory/fate
linkage, calculated IL1B attribution bounds and specified a selective post-entry design.
The shared-mixture replication and supplemented-EGF findings supersede earlier assistant
statements that those aspects of screen design were unresolved. Confidence-threshold
sensitivity remains sensitivity; no source cell identity or claim grade was assigned.
No author was contacted and no experimental result was invented.


## 27 September 2026: roadmap follow-through

At the owner's instruction to proceed until nothing remained, Codex executed separately
specified exploratory A12/A13 pilots, completed the named external-candidate checks and
prepared a data/experimental handoff. [Evidence](docs/roadmap_runs/2026-09-27-followthrough/README.md).
The earlier assistant proposal treating GSE303646 as A3-ready and GSE233844 as a lung-triad
candidate was rejected by primary metadata. It is corrected with a dated notice, not
silently deleted. A13's original source-compartment rule was not overwritten: the new
pilot declares broad assigned macrophages and fixed recipient states. No human acceptance
or evidence-grade upgrade is inferred from authorization to execute.


## 27 September 2026: authorized landing and computational continuation

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-27 | Commit, PR and merge the rationale audit and roadmap follow-through | Codex | Repository owner, explicit chat instruction | Authorized landing of the current code and reports; scientific grades unchanged | Preserve the completed work before structuring and executing the next computational phase |

Before landing, the historical P0–P5 verifier was corrected to report changes in
living-document hashes separately from failures of immutable analytical inputs.
Later dated context updates are expected; all scientific source hashes remain strict.
The original verification record still identifies the script version used at that time.


## 27 September 2026: computational continuation handoff

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-27 | Land prior audit, then divide the computational continuation into resumable tasks | Codex | Owner explicitly authorized commit/PR/merge and then requested small tasks and a next-session handoff | PR #94 merged after both CI checks passed; pipeline/handoff recorded; public GSE198864 annotated object retrieved | Preserve state across sessions without treating retrieval or interrupted work as completed science |

The A11 acute-injury contrast remains a proposal pending metadata and a committed
contract. No new module score, scientific acceptance or claim-grade change occurred.
The initial combined check/merge command was automatically rejected while a check
was still running. Both checks were then separately verified successful before the
authorized merge; no check or approval was bypassed.


## England 2025 planning record, 27 September 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-27 | Source-grounded England study package and EN0-EN7 analysis structure | Codex, using the article, repository and owner-supplied reading context | Owner requested the scope; scientific interpretation remains for owner review | Plan and metadata intake prepared; no new biological run or claim-grade decision | Separate pooled sequencing experiments, preserve C3 evidence, and expose clone/spatial re-analysis routes |

The owner explicitly confirmed reading before this paper's study note was written.
Codex authored the synthesis and candidate trial choices; the record does not claim
human acceptance of those choices or that the requested re-analysis has run.
Private annotations, copyrighted PDFs, historical freezes and existing claim grades
were preserved. Source-based caveats are in the [England audit](Research%20Article/gate2_C2_england_2025/SOURCE_AUDIT.md).


## England execution record, 28 September 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-28 | First England RNA/clonal analysis batch | Codex specified the bounded contract and source-label amendment | Owner explicitly requested actual analysis after planning; scientific conclusions remain for owner review | Executed and numerically checked; no historical claim regrading | Measure genotype-associated RNA and clone-distribution alternatives without treating pooled libraries or flattened spatial pairs as individual mice |

The first independent verifier used a full-list gene denominator and failed;
correction to the already frozen mapped-gene definition resolved the check.
Biological results were not altered to pass it. The per-cell rendering denominator
is documented explicitly in the render record. Sparse distance bins are marked
visually, and stronger spatial inference remains blocked. The batch is not an
exact reproduction of the original six-state Seurat analysis or stochastic model.


## England continuation handoff, 28 September 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-28 | EN7/CD177 contract and next-session handoff | Codex specified the bounded continuation | Owner requested completion through EN7, ideas 4–6 assessment and a handoff; scientific acceptance remains open | Contract frozen before new outcomes; no continuation endpoint run | Preserve verified batch1 and carry forward concrete rules, source intake, paths and remaining gates |

The added public ENA/GitHub/Mendeley catalogue audit recovered sequencing-run
mapping but no biological pool or repeated spatial-clone identities. The Mendeley
PDF download returned HTTP 403 and was not inspected. Source simulator timing
behavior was read, not numerically evaluated. No result or historical claim was
regraded. The [handoff](docs/handoffs/2026-09-28-england-en7-cd177.md) owns the
continuation queue; this documentation is not evidence that EN7 has executed.

## England continuation session state, 28 September 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-28 | Continuation session opened; runtime, external objects and source simulator re-inspected; amendments CA1 to CA3 frozen | Claude, from the handoff and frozen contract | Owner asked to settle the state, save, commit and open a PR before any endpoint ran; scientific acceptance remains open | Recorded in [continuation amendments](Research%20Article/gate2_C2_england_2025/config/continuation_amendments.json); no continuation endpoint executed, no batch1 file changed, no claim regraded | An amendment that can change an EN6 outcome must be frozen before that endpoint is evaluated |

The session confirmed the bundled AMD64 interpreter and the checkout's scientific
packages, confirmed the Choi and Niethamer object schemas the contract relies on,
and found one source-code observation the handoff did not carry: the deposited
simulator's slow-population loss branch compares against a cumulative sum that
repeats one term, so with renewal probability 0.7 (the Red2Kras RFP block) that
loss event can never fire. Its numerical effect is not calculated. A third,
diagnostic implementation was added to the EN6 plan to attribute any difference
to that branch separately from the horizon and rate-switch behaviours already
recorded. The origin/main audit below was merged into this branch, keeping both
records. Nothing in this session is evidence that EN1 to EN7 have executed.


## 27 September 2026: audit docs/ for AI-session residue, and refuse most of the deletions

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-27 | Delete unnecessary and superseded documents under `docs/`, where the owner defined superseded as an improper log or an artefact of AI generation context | Repository owner, explicit chat instruction | Owner instructed the deletion; Claude selected the targets and refused most of them | One document deleted, four stale status heads corrected, eighteen candidates retained with reasons | Most of `docs/` is either a run record bound to a logged artefact or an input some script reads; the residue the owner described turned out to be stale prose heads, not whole files |

**What was deleted.** `docs/RQ_REFRAMING_PLAN.md`, 425 lines. It is a plan an agent wrote,
executed, and then topped with a banner stating that its own grouping recommendations are not
the current register. Its table of seven proposed assertions refused as headlines was carried
into decision 35 above before deletion, because a rejection record stays visible, and its only
inbound link now points at the implementation record that holds its before-bytes.

**What was corrected instead of deleted.** Four pages claimed a status their own logged artefact
contradicted. `docs/research_pipeline/queue.json` records `new_biological_analysis_executed` as
true with `next_task` at `C6-audit-followups`, while `PROGRESS.md`, `AI_CONTEXT.md`,
`docs/COMPUTATIONAL_RESEARCH_PIPELINE.md` and the computational handoff all still told a
returning reader to start at C1 and that no biological score was complete. The A11 acute-injury
assay had by then been scored, reported and merged. Those heads were rewritten to match the
queue and to say plainly that the earlier text was wrong; the dated sections beneath them were
left untouched.

**What was refused, and why.** Deleting these would break a gate or destroy a record:

- `docs/roadmap_runs/2026-09-27/P3_REGULATORY_FATE.md` and `P5_RECOVERY_DESIGN.md` are code
  input. `docs/roadmap_runs/2026-09-27/scripts/verify_run.py` asserts that every report named
  in `status.json` is a file.
- `LOGICAL_RATIONALE_REVIEW.md`, `RESEARCH_ROADMAP.md`, `EXPERIMENTAL_HANDOFF.md`, `P3` and `P5`
  each have their SHA-256 pinned inside a validation record. Deleting the file falsifies the
  ledger that hashed it.
- `docs/migrations/` is read by `analysis/lib/repository_paths.py`, which resolves pre-migration
  paths through its manifest and archived original bytes.
- `docs/PIPELINE_AS_RUN.md` is required by `analysis/scripts/validate_repository.py`, and
  `docs/CLAIM_SUMMARY.md` by `claim_contract.py --check`.
- `docs/NEXT_DATASET_GATE.md` is named as an inherited contract inside frozen configuration.
- The computational handoff and queue are what an open session on
  `codex/computational-research-pipeline` resumes from, and the previous commit on `main` already
  decided in writing that they stay. Its status head was corrected; the file was kept.
- The five tool pages describe tools mostly not used, which looks like residue but is deliberate:
  `docs/README.md` states that of the five, only Scrublet was used. The two Niethamer workflow
  pages share four lines and are not a duplicate pair.

**Rejected agent output.** Three review lenses ran over twenty candidates. Two of them asserted
that the deleted plan was the only record of a SHA-256, `5aaaef62...`, of the owner's supplied
`RQ_FRAMING_PROPOSAL.md`, and both used that as the reason to consolidate rather than delete.
The file contained no 64-character hex string at all, and that hash appears nowhere in the tree.
The claim was rejected and the consolidation proceeded on the refutation table alone. Two lenses
also disagreed about whether the GSE198864 byte count and hash existed outside the handoff; the
tracked intake record carries both, so the preservation lens was wrong on that point and the
handoff was kept for other reasons. No deletion in this change rests on an agent's assertion
that was not checked against the tree.

**Not established by this audit.** Whether the remaining head-stacked pages, chiefly
`RESEARCH_ROADMAP.md`, `RESEARCH_ARCHITECTURE.md`, `LOGICAL_RATIONALE_REVIEW.md` and
`NEXT_DATASET_GATE.md`, should be rewritten rather than left with appended banners. Two lenses
recommended rewriting their heads and keeping their bodies. That is a change to living
interpretation documents and is left for the owner.


## 28 September 2026: England source review and biological hypothesis rewrite

Codex reviewed the article/supplements against saved source, code and tables,
performed a bounded post-hoc same-population diagnostic, and reframed eight
assistant-proposed candidates. The [audit and revision record](docs/audits/2026-09-28-england-paper-rqs/ARCHITECTURE_REVIEW.md)
separates new interpretation from preserved analytical outputs.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-28 | England audit, eight biological cards, architecture corrections, PR and merge after checks | Codex | Repository owner, explicit chat instructions to review/reframe and then open and merge a PR | Authorized revision and publication; no new A registration or claim-grade acceptance inferred | The original wording mixed biological questions with technical checks and carried overstrong A16–A18 premises |

Rejected or substantially revised assistant output:

| Date | Prior output | Why revised | Review authority |
|---|---|---|---|
| 2026-09-28 | Eight method-heavy candidate descriptions | Owner found them hard to understand; separate biological hypothesis, context, prediction and feasibility, with technical checks linked underneath | Owner requested reframing; Codex supplies the revised interpretations |
| 2026-09-28 | A16 depth artefacts excluded; within-cluster priming consistently persists | Frozen depth verdict is inconclusive and FU_C changed the population; same-population diagnostic is heterogeneous | Codex source/code review under owner authorization |
| 2026-09-28 | A17 refit already fully specified and able by itself to overturn founder biology | Source accounting, parameter/schedule mapping and model comparison require amendment; code defect is not a biological refutation | Same review authority; historic results preserved |
| 2026-09-28 | A18 range assigned to an AREG mechanism and flat identity slope treated as separate control | Pooled rows lack inferential units; source SPP1/DLK1 lead and measurement/geometry alternatives remain open | Same review authority; no owner grade inferred |
| 2026-09-28 | E-N3/E-N5 treated as independent biological discoveries by virtue of a counting or classification improvement | Technical outputs support survival/maturation hypotheses within existing questions; they do not establish those mechanisms | Same review authority |


## 28 September 2026: review and consolidate remaining branches

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-28 | Retain appropriate unique branch work, merge, and delete remaining branch refs | Codex review | Repository owner, explicit chat instruction | Retain A16 Stage 0/1 evidence with a current interpretation correction; merge after checks; preserve dirty worktrees | One remaining remote branch contains unique results; the other and two stale local branches are already merged |

Rejected or substantially revised assistant output:

| Date | Prior output | Why revised | Review authority |
|---|---|---|---|
| 2026-09-28 | A16 Stage 1 excludes ambient RNA and detection-threshold artefacts | The contract itself limits the ambient panel; all four primary thinning rows fail the floor; reported panel correlation uses binary detection | Codex under the owner's appropriateness review |
| 2026-09-28 | C1/C2 prove a non-positional component; median matched control accounts for most signal | UMAP/gene reuse, pooled units, changing eligibility and incompatible effect scales prevent these mechanistic decompositions | Same review; numerical evidence and original scripts preserved |

The [review](docs/audits/2026-09-28-branch-consolidation/REPORT.md) records branch
identities and evidence verification. Publication authorization is not acceptance
of a biological hypothesis or a new claim grade.


## 28 September 2026: article context, claims and gallery navigation

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-28 | Separate England overview, evidence review and gallery; index completed analyses across article folders | Codex | Repository owner, explicit request to organize context, claims and figures; prior PR/merge authorization | Authorized documentation revision and publication after checks; no scientific acceptance or grade change inferred | Chronological status, source claims, repository results and proposed questions were hard to distinguish |

Rejected or substantially revised assistant output:

| Date | Prior output | Why revised | Review authority |
|---|---|---|---|
| 2026-09-28 | England README combining original planning, later execution and overstrong gallery captions | The owner found it entangled; current review separates source evidence, reanalysis and inference limits | Owner requested organization; Codex applies already documented audits |
| 2026-09-28 | England gallery described as 14 figures and as uniformly lacking animal-level units | Inventory contains 15; nonspatial clone data retain 44 source-indexed mice, unlike pooled spatial arrays | Codex inventory and existing source/unit audit |
| 2026-09-28 | Murthy page assigned C4–C7 and C9 wholesale to the human atlas | The cited block also contains mouse claims; replace the inaccurate mapping with report and register navigation | Codex navigation review; registered claims unchanged |

The [audit](docs/audits/2026-09-28-paper-navigation/REPORT.md) and
[inventory](docs/audits/2026-09-28-paper-navigation/inventory.json) record this
documentation-only revision. Original reports and images retain their bytes.

## 28 September 2026: execute adversarial-review gap fills

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-28 | Fetch current main; parallel A15 correction, A5/A12 source recovery, bounded A16/A17 follow-through and shared-document fixes | Codex adversarial review and agent proposals | Repository owner explicitly requested latest remote state and multi-agent gap-fill execution; Codex selected and froze implementation details | Authorized computational work in isolated checkout; no scientific acceptance, grade change or publication inferred | Repair the confirmed normalization defect and resolve decision-changing data gates while preserving historical evidence |

Rejected or substantially revised assistant output:

| Date | Prior output | Why revised | Review authority |
|---|---|---|---|
| 2026-09-28 | A15 raw-count median-ratio factor followed by another library-total division | Fails proportional-library invariance; replace only this sensitivity in a committed new version with independent raw-count verification | Codex review under owner-authorized correction; original evidence preserved |
| 2026-09-28 | C49 approximate significance cutoff described as a bound on absent correlations | The calculation supplies neither a confidence bound nor a powered detectable effect | Codex code/claim review; estimates and grade unchanged |
| 2026-09-28 | C36 unavailable CellChat software used as current explanation for missing reception evidence | Later ligand-resource/recipient analyses exist; they still do not measure receptor engagement | Codex evidence reconciliation; Not established retained |
| 2026-09-28 | A11 acute-assay paragraph presented under A13 | It tests the lesion module and provides no A13 triad/fibroblast evidence | Codex question-ownership correction; results unchanged |
| 2026-09-28 | A16 historical pooled/UMAP matching treated as the requested fixed-population, gene-excluded comparison | Requires new per-library construction and unchanged cells/effect scale; corrected C1 remains exploratory | Codex amended specification, committed before new outcomes; original Stage 1 preserved |

The [execution report](docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md) distinguishes
completed computational work, failed eligibility gates and measurements still
required. Assistant review and computational retention do not constitute owner
acceptance of a biological hypothesis.

## 28 September 2026: synchronize project navigation and research status

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-28 | Reorganize the root README, update dataset and paper roadmaps, reconcile related current documentation | Repository owner | Owner explicitly requested these changes; Codex selected the linked inventory and synchronization details | Remove the front claims table and paper-specific start links; preserve the full claim register, reading decisions and scientific artifacts | The landing page mixed project navigation with individual analyses and the roadmap lagged merged work |

Rejected or substantially revised assistant output:

| Date | Prior output | Why revised | Review authority |
|---|---|---|---|
| 2026-09-28 | Front claims table and A10/Nabhan-specific entries in the main Start here table | Owner requested general project navigation; this explicit preference supersedes the documentation skill's default claims-table placement | Repository owner |
| 2026-09-28 | Paper 14's analysis unstarted because its study note was unstarted; old Cardoso E1 result presented as current | A2/A10 already use the deposit, and later corrections limit the original E1 interpretation; reading and execution are separate | Codex reconciliation against tracked reports |
| 2026-09-28 | Completed A5/A12 audits still queued as ready, with C7 depending on nonexistent C6 | Later recovery reports close the audits while leaving scoring gated; the actual dependency is C6-audit-followups | Codex reconciliation against merged gap-fill records |

The [synchronization audit](docs/audits/2026-09-28-documentation-sync/REPORT.md)
records the documentation scope and preservation checks. No paper is marked
read, biological hypothesis accepted or claim grade changed by this revision.

## 28 September 2026: put the biological question first in RQ workspaces

The owner requested that every question-folder README explain its A label and
organizing biological question at first glance while retaining its distinct
analysis flow. Codex added question, motivation, scope and evidence-navigation
openings to all 10 question workspaces and the shared A5/A11 contract. The parent
index now maps every registered label without creating empty execution folders.

Status-first introductions were revised because completed/remaining tasks did
not explain the biological purpose. A5/A12 links now include the latest recovery
reports, and A13's original no-fit statement is explicitly historical alongside
the later amended pilot. These are owner-authorized documentation changes;
scientific results, hypothesis wording and acceptance decisions are preserved.

## 28 September 2026: combine rationale-depth and reframing plans

The owner requested a merged proposal from the two comparative assessments.
Codex prepared a dated plan for A0–A18, A12-S1 and the shared A5/A11 workspace,
linking each diagnosis to proposed scope, work possible now and an evidence gate
or stopping rule. The [proposal](docs/audits/2026-09-28-rq-development-proposal/PROPOSAL.md)
does not implement its candidate hypotheses or organizational recommendations.
Publication of this planning document does not imply scientific acceptance;
its contingent analyses remain proposed work subject to their evidence gates.

## 28 September 2026: amend the A16 rationale to match later evidence

The owner adopted the combined proposal's first item and asked for A16 first.
Claude Science appended a dated amendment to A16's rationale rather than
rewriting the Stage 0 text, so the original premises remain readable as
planning history. The amendment adopts the proposal's question wording inside
the workspace, records four evidence states and a claim-by-claim ledger, and
carries forward the integration review's boundaries. The frozen contract was
deliberately left unedited because CI hash-verifies it. This is an
owner-authorized documentation change; the register card, readiness row,
claim grades and the pending A16 retain/reject decision are unchanged.

## 28 September 2026: align A10's endpoint, then nominate A1's next test

Continuing the adopted proposal, Claude Science consolidated what A10's endpoint
measures and in which unit, and used that statement to bind A10 into A1's
comparison matrix. The consequential finding is negative and was not anticipated
by the proposal's wording: A10's predictor and outcome are measured at the same
time in the same well, so it cannot serve as the later outcome A1, A8 and A14
need, and no other A1 branch has a later outcome in the same units either. The
matrix therefore nominates a linkage design rather than a computational task,
and records the stop rule against pairing measurements across cohorts. Two
sub-agents produced the underlying inventories; their first dispatch was
terminated by a platform content-safety refusal and the retry completed, which is
recorded because the failure left no output and could be mistaken for a data
problem. Documentation only; no result, grade or register wording changed.

## 28 September 2026: separate workspaces for A8 and A14

The owner asked whether the two questions share enough context to be handled
together, and the answer from their cards and cited evidence was no: the overlap
is the absent mature outcome and MC1, while hypothesis, predictor, population,
perturbation, rival set and decision rule are disjoint. Claude Science therefore
created two folders rather than one shared document, on the owner's instruction,
and noted that this is a deliberate exception to the proposal's default against
new folders. Each carries the two open proposal items for its question: A8's
rationale separates a measurement check from a maturation claim and states why
neither direction of the inference is identified; A14's gives each of its two
hypotheses an independent design and decision. Both remain blocked on
measurements that do not exist, and both say so rather than proposing an analysis.
Documentation only; no result, grade or register wording changed.

## 28 September 2026: local rationale and plans for the A12 group

Continuing the adopted proposal, Claude Science wrote the A12 and A13 rationale
and plan files and one shared A12-S1 evidence map. Two things emerged that the
proposal's wording did not anticipate. First, A12's endpoint choice needed
defending rather than describing: a general inflammatory readout cannot show IL-1
specificity, and the design's answer is to put TNF in the comparator rather than
to claim selectivity. Second, A13's null is weaker than it looks -- at the
primary setting no model beats the training mean, so the closed comparison is
between two models that predict no better than a constant, which is a statement about the
instrument and not about fibroblast biology. Both are recorded in the documents
rather than smoothed over. Documentation only; no result, grade or register
wording changed.

## 29 September 2026: correct the RQ delivery review findings

The owner explicitly requested the seven review corrections and subsequently
authorized the A1 regulatory primary test only if executable. Codex applied the
A1/shared-inventory/A16 corrections, with two scoped agents updating A8 and A14;
the parent reviewed their contracts and synchronized the handoff documents.
A1 remains non-executable because the regulatory predictor and compatible
regulatory/RNA/later-outcome linkage are absent. No RNA-only substitute was run.

The [resolution note](docs/audits/2026-09-29-rq-delivery-review/CORRECTIONS.md)
records the corrections and checks. A16's presentation revision retains original
figure/script records and uses the same tracked tables. No model was fitted,
no claim grade was changed, and no biological readiness state was promoted.

## 29 September 2026: Nabhan 2023 structure and owner candidate register

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-29 | Gate 2N/N1 folder and three tracks | Owner | Owner, explicit request | Implemented as a planning package; scientific acceptance not inferred | Connect reproduction, exploration and open questions to the README purpose |
| 2026-09-29 | Eight Nabhan cards and existing-RQ crosswalk | Owner themes; Codex operational formulations | Owner requested registration; formulations remain proposals | Register locally in the requested order and link from the root register | Preserve hypotheses without duplicate global questions |

Codex read the supplied annotated 34-page paper, visually checked selected pages,
fetched three Notion context pages and public GEO metadata, and authored the package
without subagents. A managed worktree from fetched `17c0859` preserves the primary
checkout's unrelated files. No Notion page was edited.

| Date | Interpretation revised | Reason | Revised by |
|---|---|---|---|
| 2026-09-29 | Figure 4/GSE208770 as scRNA-seq in the abbreviated reading notes | Paper methods and deposit support bulk organoid RNA-seq | Codex primary-source check; owner notes preserved |
| 2026-09-29 | Undetected Fzd5/Fzd6 differences as equivalence; compensation as established | Precision is limited; incomplete editing and antibody target scope remain alternatives | Codex specification |
| 2026-09-29 | Preventative fibrosis findings as delayed-treatment or clinical IPF benefit | Paper limitations restrict those endpoints | Codex source audit |

These constraints do not reject the owner's research interests. Only metadata intake
and verification are implemented. No biological result or evidence grade is promoted.
Validation is recorded in the package's metadata.


## 29 September 2026: Nb2 initial execution

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-29 | Paper namespace and execution | Owner | Owner, explicit follow-up | Use Nb2; execute accessible first pass within the existing Gate2N/N1 folder | Preserve reading-position identity while separating this paper from Nb1 |
| 2026-09-29 | Bulk and atlas contracts, scripts, tables and six figures | Codex | Owner-authorized analysis; implementation by Codex | Frozen count adaptation and descriptive source/extension summaries; no claim promotion | Source preparation map and exact atlas/functional inputs remain unresolved |
| 2026-09-29 | Human barcode alignment recovery | Codex | Deterministic source-schema audit | Preserve failed script/contract and append amendment before extraction; restrict to114,396 annotated barcodes | All source labels are a subset of220,213 matrix barcodes; recomputed depths match metadata exactly |

The [execution report](Research%20Article/gate2_N1_nabhan_2023/RESULTS.md) owns the
new measured observations. Existing local counts and a compatible runtime were
reused; human counts were streamed once after the pre-extraction schema failure.
Frozen hashes preserve exposure and inputs. Unpaired bulk inference remains
conditional on the source's unverified independence claim. No sample was excluded
because of PCA separation, and no block was guessed from replicate suffixes.

| Date | Interpretation revised | Reason | Revised by |
|---|---|---|---|
| 2026-09-29 | Substitute Crim1 for printed Crim2 | Unresolved source name; three-gene adaptation explicitly recorded instead | Codex source/annotation audit |
| 2026-09-29 | Promote prominent oxidative-phosphorylation enrichment to a metabolic mechanism | Estimated residual gene correlation weakens the enrichment; bulk RNA is not flux | Codex prespecified sensitivity |
| 2026-09-29 | Treat vascular Fzd4 as a progenitor-specific result | Arterial and venous profiles also express it strongly | Codex descriptive extension |
| 2026-09-29 | Infer state-dependent disease effects from rare populations | Transitional-IPF and fibroblast-control unit coverage fails the main cohort threshold | Codex coverage gate |

Numerical verification recomputes panel arithmetic, contrast algebra, BH adjustment,
CPM denominators and state summaries. Root navigation and the stage ledger now
point to executed evidence. [Replay and validation](Research%20Article/gate2_N1_nabhan_2023/EXECUTION.md)
describe the precise scope. These checks do not validate the eight hypotheses.
## 29 September 2026: Nb2 branch execution and RQ specifications

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-29 | Execute branches and derive hypotheses under RQ_Specified | Owner | Owner, explicit follow-up | Create Nb2_fzd_response_context with seven focused RQs and existing N8 companion | Follow the reading-to-analysis-to-specified-question hierarchy |
| 2026-09-29 | Cross-study reference, influence and subtype analyses | Codex | Owner-authorized scope; implementation by Codex | Frozen exploratory contract; reuse prior exposure and A1 resource audit | Distinguish stable RNA leads from missing fate/mechanism evidence |
| 2026-09-29 | Count-depth schema amendment | Codex | Deterministic source audit | Preserve failure; retain count-layer denominator and require prior aggregate reconciliation | Stored QC totals differ slightly;57,380 shared unit/gene rows match exactly |
| 2026-09-29 | Local Nb2-RQ1–RQ8 IDs | Codex | Owner requested RQ specification; formulations remain proposals | Link existing A-series owners without renumbering or duplicate global questions | Organize the seven focused branches and N8 companion coherently |

| Date | Interpretation revised | Reason | Revised by |
|---|---|---|---|
| 2026-09-29 | Three source genes establish broad sustained-YAP activation | Projected reference response is unstable; reference also separates atlas AT1/AT2 | Codex measured extension |
| 2026-09-29 | More Fzd5 RNA implies more canonical target RNA | Four matched AT1/AT2 samples show opposite orderings | Codex descriptive state comparison |
| 2026-09-29 | Fzd1-rich fibroblasts imply stronger epithelial support | Subtype contrast favors Fzd2-rich AF1 for the selected support-ligand panel; functional outcome absent | Codex subtype comparison |
| 2026-09-29 | Pooled Fzd4–cycling correlation supports a progenitor mechanism | Opposite within-round correlations; no receptor perturbation or lineage endpoint | Codex post hoc rival check |

The [question results](Research%20Article/gate2_N1_nabhan_2023/branch_analysis/RESULTS.md) and
[execution record](Research%20Article/gate2_N1_nabhan_2023/branch_analysis/EXECUTION.md) own the
new evidence. The numerical verifier's first source-panel lookup used `Hippo`
instead of the actual `Hippo_associated`; correcting the lookup changed no
analysis values, and all53 checks then passed. Figure inspection corrected a
legend/label overlap and exposed experimental round in the vascular panel.
No claim grade or scientific acceptance was inferred from execution authorization.
## 29 September 2026: owner correction to Nb2 analysis hierarchy

| Date | Proposal corrected | Reason | Rejected / corrected by | Resolution |
|---|---|---|---|---|
| 2026-09-29 | Put branch analyses in RQ_Specified and label each branch Nb2-RQ1–RQ8 | The owner clarified that analyses remain under Research Article; specified RQs follow from the analysis and synthesis | Owner, explicit hierarchy correction | Move the complete bundle to the Nb2 paper, retire the premature RQ labels and retain provisional Nb2-N1–N8 candidate notes |

This supersedes the earlier location/registration decision above. It does not
reject the measured results or authorize a one-to-one mapping of branches to
future RQs. Scientific artifacts retain their original hashes. Live scripts
only change path resolution; originals and historical path aliases are recorded
in the [relocation metadata](Research%20Article/gate2_N1_nabhan_2023/branch_analysis/metadata/relocation.json).
The two RQ index edits were removed, existing A-series work was preserved, and
current navigation/handoff now follows **paper analysis → synthesis → warranted
RQ specification**. No scientific model was rerun for this structural correction.

## 29 September 2026: Nb2 PR publication

The owner explicitly requested opening a PR for the completed Nb2 paper and
branch analyses. Codex prepared the existing managed branch for publication,
retaining the paper-local hierarchy and provisional candidate status. A targeted
Git attribute preserves frozen evidence bytes across platforms. Publication
does not promote claims, register specified RQs or authorize merging.

## 29 September 2026: register question-level and atlas claims

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-29 | Register every claim across paper packages and RQ_Specified results; relabel existing rows the 29 September figure audit contradicts | Repository owner | Owner requested the registration; Claude Science proposed each grade as a delegated reassessment | Add C169-C233 in four dated sections. Append dated qualifiers to C2, C4, C29, C38, C42, C47, C51, C54, C69, C73, C74, C76 and C83. Change C4's Kit status from Validated to Descriptive only. Repair 17 package-relative artefact paths in C1, C19, C20, C22-C32, C34 and C35. Extend `claim_contract.py` with explicit family ranges | The register ended at C168 and omitted every question-level result, including A0's negative transfer. The figure audit had corrected several claims that still read at full strength in the register |

Three inventory tracks stopped before producing output: England with A16, Yu-Lee-Choi-Min,
and A1, A2, A8, A14 and A15. Each was retried once, unchanged and with the owner's
authorization, and stopped again. Those folders are listed as not inventoried in
`CLAIMS.md` and the coverage ledger. No grade was inferred for them. Historical row
wording was preserved, and each correction is appended as a dated qualifier. Grades
proposed here are not owner acceptance.

## 29 September 2026: complete the register's coverage

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-29 | Inventory the three folder groups the first pass could not read, and register their claims | Repository owner | Owner asked for the retry; Claude Science proposed each grade as a delegated reassessment | Add C234-C269 (England with A16), C270-C295 (Yu, Lee, Choi and Min) and C296-C342 (A1, A2, A15 and the A8/A14 endpoint requirements). Append dated qualifiers to C19, C31 and C34 and add two superseding artefacts to C36. Extend `claim_contract.py` to 342 | The first pass left those folders ungraded because its inventories were interrupted. Every folder under `Research Article/` and `RQ_Specified/` now has rows or a recorded reason for having none |

Two of the Yu-Lee-Choi-Min propositions were already registered through A12, as
C225 and C226, and are not duplicated. A8 and A14 hold Stage 0 material only, so
their rows record absent endpoint requirements rather than results. The three
inventories were interrupted repeatedly before this pass and completed unchanged
once the session model changed; no brief was reworded and no refused track was
taken over directly. Grades proposed here are not owner acceptance.

## 29 September 2026: reconcile Nb2 PR with current main

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-29 | Resolve PR #121 merge conflict after claim registrations landed on main | Codex | Owner requested conflict resolution | Preserve both independent appended development records; integrate main through 68ff942 | CI had passed; the blocker was a documentation merge conflict, not a failed analysis |

The incoming claim register and generated summaries are retained unchanged. The
Nb2 scientific artifacts and provisional candidate status are unchanged.

## 29 September 2026: derive questions from the combined Nb2 results

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-29 | Derive RQs after paper-local analysis and synthesis | Owner | Owner requested derivation; formulations by Codex remain proposals | Propose A19–A21 with new question plans; retain all earlier analysis in Research Article | Follow evidence-to-question hierarchy without one formal RQ per original branch |
| 2026-09-29 | Consolidation and priority | Codex | Proposed under the owner's derivation request; no biological acceptance inferred | N1/N2/N3/N5 combine in A19; N6 informs A20; N7 informs conditional A21; defer N4/N8 | Separate functional endpoints and decisions; respect failed coverage, perturbation mismatch and unfavorable round sensitivity |

The bounded primary-source check contextualizes Gaona, the Fzd2 study and Gillich;
it is not an exhaustive novelty or dataset search. New contracts disclose prior
exposure, missing quantitative design choices and unexecuted status. Source trial
bytes, A0–A18 scopes and C-grades are preserved. No scientific result is rerun.

| Date | Proposal clarified | Reason | Corrected by | Resolution |
|---|---|---|---|---|
| 2026-09-29 | RQs framed primarily as response interactions or measurement distinctions | Each RQ must be plausibly framed as a biological hypothesis, not a measurement artifact | Owner, explicit framing rule | State a reversible expansion/maturation process (A19), trophic fibroblast-state mechanism (A20) and Fzd4-dependent regenerative recruitment (A21); retain measurement issues as rivals and controls. Mechanisms remain proposed and untested |

The owner subsequently requested pushing this RQ synthesis and opening a PR.
Codex prepared the same branch for publication, retaining the proposed/untested
status and biological-hypothesis framing rule. This authorizes publication, not
scientific acceptance or merging.

## 30 September 2026: restore universal front-page navigation

| Date | Proposal corrected | Reason | Corrected by | Resolution |
|---|---|---|---|---|
| 2026-09-30 | Nabhan/Nb2-specific entries in the main README Start here table | The front page must remain universal repository context | Owner, explicit correction | Remove all three paper-specific rows; retain discovery through the Research Article and RQ indexes; record the universal-navigation rule in the structure contract |


## 30 September 2026: A19 exploratory context analysis and figures

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-30 | Execute A19 and deposit research-style figures under RQ_Specified | Owner | Owner, explicit request | Analyze eligible public inputs in the existing A19 workspace; retain paper-local Nb2 artifacts | Continue the specified biological question with source-grounded outputs |
| 2026-09-30 | Bounded source selection and exploratory RNA contrasts | Codex | Execution authorized by owner; biological interpretation remains proposed | Freeze donor pairing, panels, units and comparisons before new numeric outcomes; preserve prior narrative exposure | No inspected source supplies the complete direct Fzd/fate/reserve test |
| 2026-09-30 | Biological refinement | Codex | Proposed; no human acceptance or grade inferred | Retained alveolar competence may constrain whether ending maintenance input permits maturation | Airway-marker responses, transient induction in airway-derived cultures and bulk discordance limit a simple expansion-then-maturation account |

| Date | Output corrected or rejected | Reason | Decided by | Resolution |
|---|---|---|---|---|
| 2026-09-30 | First qPCR extraction used an EmptyCell row attribute | Empty leading cells lack that attribute | Codex, execution error | Preserve failed script/hash; record iterator row index; no scientific selection changed |
| 2026-09-30 | Initial figure script and layout | Newline escaping prevented parsing; first visual pass showed colliding labels and insufficient origin labeling | Codex, runtime and visual review | Correct escaping/spacing; label airway-derived cultures and CHIR-present knockdown comparison; no numerical changes |
| 2026-09-30 | Frozen figure shorthand suggesting a receptor-input comparator | New source data compare GSK3 contexts, not Fzd receptors | Codex, source audit | Keep frozen contract intact; final figures/captions explicitly describe the narrower comparison and leave H3 unresolved |

Codex performed public-source intake, deterministic extraction, paired summaries,
TMM normalization and fixed-panel contrasts, plus scientific plotting and
independent source/arithmetic verification. The source workbook contributes 143
rows, including three non-detects; exact donor matching yields 72 complete
contrasts. Eight selected bulk libraries contribute two source blocks, with
hairpin confounding retained. No source unit was inflated to eight donors, no
missing outcome was imputed, and no mechanistic or clinical claim was accepted.
The user's universal front-page navigation rule remains in force.


Validation: the independent A19 verifier passed source-coordinate, raw-count,
normalization and contrast arithmetic, coverage, and all 12 export hashes.
All four PDF figure sets were visually inspected after rendering. Local required
CI passed: 67 tests (one skip), claim contract, Nb1/A16 provenance and 5,233
repository checks. This validates deposited implementation/provenance, not the
parent biological mechanism. [Verification record](RQ_Specified/A19_fzd_response_reversibility/reports/repository_checks.json).


## 30 September 2026: integrate the A19 extension and external evidence

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-30 | Structure extension priorities with the existing hypothesis refinement | Owner | Owner, explicit request | Deposit a staged pipeline and draft execution specification; integrate PLAN/RESULTS/navigation | Make the narrowed biological question actionable without relabeling old results |
| 2026-09-30 | External web evidence review | Owner | Owner, explicit follow-up | Review primary studies and dataset records, map support/constraints and eligibility | Test the plausibility of the narrowed scope and locate useful data |
| 2026-09-30 | State timing and competing biological explanations | Codex | Proposed interpretation under the authorized analysis-planning task | Distinguish S0 from acquired S1; preserve reserve and add missing-cue, selection and input-context rivals | Avoid circular competence definitions, mediator adjustment and irreversible-fate assumptions |

| Date | Output corrected or qualified | Reason | Decided by | Resolution |
|---|---|---|---|---|
| 2026-09-30 | Potentially treating pre-withdrawal state as the original H2 baseline state | An acquired state may be a treatment-induced mediator | Codex, design audit | Preserve pre-exposure H2 and define a separate local H2-extension with assignment timing made explicit |
| 2026-09-30 | A strong airway-state restriction reading of the narrowed hypothesis | Receptor/input and maturation context can alter fate; withdrawal alone can lack necessary cues | Codex, external primary-source review | State a conditional, potentially modifiable restriction and retain counterevidence; no accepted mechanism inferred |

Eight primary studies were mapped, including already exposed Nb2/Hoffmann
results, prior A1 lineage context, and newer differentiation/function studies.
No reference was counted as an independent validation merely because it appears
in a second paper. Failed public XML requests remain in the intake record;
publisher/PMC sections were used where readable. Full downloaded reference
payloads remain in ignored cache. No authors were contacted and no new numerical
analysis, figure or claim grade was produced. Pre-amendment document bytes were
archived; the original exploratory_v1 scientific outputs remain unchanged.


Validation of the extension amendment passed 5,280 repository checks and 18
claim bindings. Source identity checks matched all six proposed uninfected
controls to their recorded labels; eight reference entries and available
payload hashes passed. Forty-five previous A19 artifacts remained byte-identical.
The first link check found 23 broken relative links in copied historical
Markdown; historical files were stored as .md.txt snapshots with original-path
mapping and unchanged bytes, then the check passed. No unrelated analysis or
previously passing scientific test was rerun. The planning/source check record
is under A19 reports/extension_integration_checks.json.

## 30 September 2026: A20 exploratory context execution

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-30 | Check universal README correction on main and proceed with A20 | Owner | Owner, explicit request | Fetch main; preserve local removal; execute source eligibility and frozen paired context analysis | Main still contains the article-specific rows; A20 needs source and functional boundaries |
| 2026-09-30 | Narrow A20's biological hypothesis | Codex | Proposed interpretation; owner acceptance not recorded | Separate niche persistence from changed support activity and instructive maturation | Receptor and selective ligand/collagen RNA do not identify functional mediation |

| Date | Output corrected or qualified | Reason | Decided by | Resolution |
|---|---|---|---|---|
| 2026-09-30 | Treating AF1 support-panel elevation as uniformly greater trophic activity | Hgf has the opposite direction; RNA is not secretion or function | Codex, analytical review | Report individual genes and retain distinct functional outcomes |
| 2026-09-30 | Treating AF1/AF2 as universal reparative/fibrotic classes | Collagen rankings vary across source contexts and local Col14a1 is mixed | Codex, source and crosswalk review | Retain local multi-marker comparison and stage/model boundaries |

A20's exploratory specification was frozen before new gene estimates. Original
plans are archived as exact bytes; no direct H1/H2 test or biological acceptance
is claimed. Three scientific figures show source samples and coverage limits.
The independent verifier passed 15,383 checks with 1,000 prior extraction rows
reconciled; 69 A19 artifacts stayed byte-identical. Required CI-equivalent checks
passed: 67 tests (one skipped), 18 claim bindings, Nb1/A16 provenance and 5,333
repository checks; results are recorded in the A20 report. README remains universal locally; its removal
has not landed on main, and no merge was requested or performed in this turn.

## 30 September 2026: A20 aligned priorities 1–3 extension

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-30 | Execute aligned priorities 1–3 | Owner | Owner, explicit request | Source audit plus frozen four-donor input-context analysis | Distinguish niche persistence, support/matrix activity and context |
| 2026-09-30 | Refine receptor-dependent support hypothesis | Codex | Proposed interpretation; owner biological acceptance not recorded | Preserve H1/H2; separate pool maintenance and maturation | RNA response cannot establish niche function |

| Date | Output corrected or qualified | Reason | Decided by | Resolution |
|---|---|---|---|---|
| 2026-09-30 | Forty-five-gene source mapping | FZD10 absent; gate failed before gene estimates | Codex, source mapping review | Preserve failure/amendment; retain unavailable entry; execute 44 genes without replacing a target |
| 2026-09-30 | Concurrent TGF/CHIR as a prior-state effect | Inputs are simultaneous and CHIR acts downstream of FZD | Codex, assay review | Report direct concurrent-input interaction; initial-subtype H2 remains open |
| 2026-09-30 | RNA/function matched association | Separate human donor cohorts and treatment durations | Codex, source review | No cross-cohort regression or mediation fit |
| 2026-09-30 | Jones Notch as FZD2 mechanism | Different perturbation and unresolved animal-level data units | Codex, eligibility review | Explicit full citation; use as lineage/context comparator only |

All four donors and every planned contrast remain in the tables, including
normalization sign changes and low-detection genes. No P values, population
intervals or genome-wide discovery labels were generated. Five parent documents
were archived before integration. The extension's reports retain arithmetic,
preservation, figure review and repository validation evidence. No new claim
grade, biological acceptance, commit, push or PR was produced.

Extension verification passed 39,809 arithmetic/provenance checks; 45 prior
A20 files and all 69 A19 files remain unchanged, with five A20 parent documents
archived. Required CI-equivalent checks passed: 67 tests (one skipped), 18 claim
bindings, Nb1/A16 evidence and 5,382 repository checks. All three final PDF
renders were visually checked.

## 30 September 2026: A20 primary scope narrowing

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-30 | Narrow A20 after the completed exploratory phase | Owner | Owner, explicit request to narrow | Focus on Fzd2 versus Fzd1 within one adult AF1-like context; retain absolute mature-output H1 | A bounded receptor-function question is executable only with matched functional evidence |
| 2026-09-30 | AT2 pool maintenance as focused mechanism | Codex | Working proposal; biological acceptance not recorded | Distinguish from maturation-specific support, depletion and matrix effects | Existing RNA/context evidence cannot identify the causal route |

| Date | Output corrected or qualified | Reason | Decided by | Resolution |
|---|---|---|---|---|
| 2026-09-30 | Broad subtype and pathway extensions presented alongside the primary question | This kept several biological programs active without eligible functional evidence | Codex, authorized scope amendment | Preserve original H2 but defer it; retain Notch, matrix and mediator possibilities without opening parallel programs |
| 2026-09-30 | Potential replacement of mature output by AT2 expansion | An expanded pool need not yield functional mature descendants | Codex, endpoint review | Preserve original primary endpoint and use earlier pool/fate outcomes to discriminate mechanisms |

Pre-amendment A20 documents and its package manifest are archived under
metadata/history/scope_refinement_v1. The focused design is explicitly
post-analysis. No raw data, normalization, contrast, figure, claim grade or
scientific result was changed. The scope authorization is not a biological
acceptance decision.

Narrowing validation passed: 5,400 repository checks, 18 claim bindings and
whitespace validation. All 103 unedited prior A20 files and all 69 A19 files
remain byte-identical; four revised A20 documents are archived. The universal
README is unchanged by this amendment. No scientific rerun was needed for
the documentation-only scope change.

## 30 September 2026: A21 independent context execution

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-30 | Proceed with A21 | Owner | Owner, explicit request | Execute source/cohort eligibility and frozen independent capillary context analysis | Challenge the existing expression lead and distinguish renewal from maintenance |
| 2026-09-30 | Vascular competence versus regenerative entry | Codex | Proposed interpretation; biological acceptance not recorded | Retain original lineage endpoint and conditional priority | Expression context and tumor-vessel restoration do not establish normal gCap renewal |

| Date | Output corrected or qualified | Reason | Decided by | Resolution |
|---|---|---|---|---|
| 2026-09-30 | Exact raw UMI equality to author QC totals | 718 cells differ by 1–10 UMIs; source initial filtering incompletely documented | Codex, source audit | Preserve failed script and audit; keep frozen raw normalization and add author-denominator sensitivity before gene estimates |
| 2026-09-30 | Positive pooled Fzd4-cycling lead | Original round dependence and independent within-condition inconsistency | Codex, executed analysis | Preserve coefficients but retire the pooled lead as affirmative renewal evidence |
| 2026-09-30 | Cycling-state receptor comparison | No animal reaches the frozen 20-cell floor | Codex, eligibility check | Report unavailable primary contrast; retain the single 10-cell sensitivity without claiming replication |
| 2026-09-30 | General Fzd4 rescue as restored perfusion in normal lung | Bian Figure 7 measures pathway/structure/tumor outcomes after Foxf1 loss; perfusion impairment is a different comparison | Codex, source endpoint review | State measured endpoints and tumor context; do not claim normal gCap lineage or direct Fzd4 perfusion rescue |

Twelve barcoded animals, source-state definitions, 26 genes, cell floors and
contrasts were frozen before new gene estimates. Three scientific figures show
all eligible units and coverage limitations. Failed source-workbook/ZIP downloads
remain recorded; no source values were reconstructed from bars. The independent
verifier reconciles raw counts, denominators, panels, paired contrasts and rank
summaries and preserves all 191 prior A19/A20 artifacts. No biological acceptance,
claim grade, commit, push or PR was produced.

A21 validation passed: independent raw-source arithmetic/provenance verification,
all 191 prior A19/A20 artifacts preserved, 67 tests (one skipped), 18 claim bindings,
Nb1/A16 evidence, input restoration and 5,447 repository checks. All three PDF
figures passed visual review. Validation establishes reproducibility within the
recorded scope, not a functional Fzd4 mechanism.

## 30 September 2026: A21 priorities extension

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-30 | Execute priorities 1-3 | Owner | Owner, explicit request | Reconstruct eligible vascular source data, extend all-Fzd state context and specify separate functional lineage outcomes | Narrow the biological mechanism using available evidence |
| 2026-09-30 | Focus vascular integrity versus lineage specificity | Codex | Working proposal; no biological acceptance recorded | Retain original gCap and aerocyte endpoints and conditional status | Structural tumor rescue and RNA context cannot establish adult-lung receptor-dependent renewal |

| Date | Output corrected or qualified | Reason | Decided by | Resolution |
|---|---|---|---|---|
| 2026-09-30 | Earlier Bian source archive unavailable | Current publisher media endpoint resolves ZIPs | Codex, source intake | Preserve failed requests; reconstruct five eligible workbooks with hashes and cell addresses |
| 2026-09-30 | Potential interpretation as Fzd4-rescue perfusion | Perfusion data are from Foxf1 loss; Fzd4 rescue measures structure/signaling | Codex, source audit | Keep contrasts separate; no mediation or functional-rescue claim |
| 2026-09-30 | Provisional perfusion endpoint called a vessel percentage | Published axis is lectin-positive area relative to CD31 area | Codex, visual source audit before numeric extraction | Resolve source unit in source_mapping.json without changing the contrast |
| 2026-09-30 | Broad alternative-Fzd compensation proposal | No receptor meets frozen RNA nomination criteria | Codex, completed exploratory screen | Defer candidate-specific compensation; absence and dependency remain untested |
| 2026-09-30 | Figure 7E significance reconstruction | Workbook specifies Fisher LSD while legend specifies Tukey | Codex, source audit | Preserve observations; import no P values or significance stars |
| 2026-09-30 | Initial independent-verifier global gene-symbol uniqueness check | Unrelated feature names are duplicated although all 36 targets map uniquely | Codex, verifier correction | Check the contract's selected-target uniqueness; no scientific outputs changed |

Scientific verification passed 56,225 checks. Final PDFs were rendered and reviewed.
The extension retains original source observations, prior results and archived
parent documents; the root README remains universal and unchanged by this work.
Execution authorization is not a biological acceptance or landing decision.

## 30 September 2026: PR delivery and one-line question refinement

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-09-30 | Push and open PR after final review | Owner | Owner, explicit request | Push the reviewed A19-A21 packages and open PR #123 | Publish reviewable work; no merge or biological acceptance |
| 2026-09-30 | Update one-line A19-A21 hypothesis questions within repository hierarchy | Owner | Owner requested wording update; formulations by Codex remain proposals | Synchronize folder README/PLAN/contracts, canonical register and index; retain stable IDs and primary outcomes | Reflect the refined biological questions instead of older broad titles |

| Date | Output corrected | Reason | Decided by | Resolution |
|---|---|---|---|---|
| 2026-09-30 | First PR commit omitted 16 PDF exports | Global PDF ignore rule hid locally reviewed files from staging, causing hosted link checks to fail | Codex, CI diagnosis | Add narrow scientific-figure exceptions and commit byte-identical PDFs; verify manifest coverage in the Git index |

Original question documents and manifests are archived in each question folder.
Scientific tables, figures and frozen analysis contracts are unchanged by the
wording update. Historical verification records retain their original scope.

## Nb3 source reproduction and descriptive extensions, 1 October 2026

The owner completed Nabhan 2026, requested a source-grounded pipeline using the
PDF/supplement and annotated notes, corrected the year, then assigned **Nb3**
and explicitly authorized reproduction and extensions. Codex recovered the
exact-hash full inputs, implemented declared reconstruction variants and fixed
marker-panel analyses, and retained explicit source/design holds. The
[execution guide](Research%20Article/gate2_N2_nabhan_2026/EXECUTION.md),
[reproduction review](Research%20Article/gate2_N2_nabhan_2026/reports/REPRODUCTION_REVIEW.md)
and [extension review](Research%20Article/gate2_N2_nabhan_2026/reports/EXTENSION_REVIEW.md)
separate source statistics, new computations and inference limits.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-01 | Analysis ID Nb3 and reproduction/extension execution | Owner | Owner, explicit chat instruction | Authorized | Continue the reviewed paper's pipeline in its 2026 folder |
| 2026-10-01 | Numerical v1 contract, source-marker correction, technical-well interpretation and named holds | Codex, grounded in supplied sources and prior exposure | Owner authorized execution; scientific acceptance remains pending | Record choices before fits; retain exact-source uncertainties and counterexamples | Split wells and missing source details limit inference; source code/settings must not be invented |
| 2026-10-01 | Run paired fixed-panel analysis while independent whole-transcriptome DE finishes | Codex | Within authorized execution | Hash completed normalization/panel inputs; require final full-DE source comparison | The panel branch does not depend on remaining gene-DE fits; no numerical choice changed |

The earlier assistant scaffold's statement that no new models had run is
superseded by the current execution review, while initial intake records remain
historical. No claim-register grade, A10/A2 fit or prior frozen contract was
rewritten. Figure QA corrected overlapping annotation positions in a new export
and preserved the first export. A blank-row source-table parse failed before any
identity output was written, then was corrected to skip entirely blank Excel rows;
the identity record retains that implementation history.

The full source comparison then exposed a material human S5 discrepancy. A
bounded post-hoc audit found internal source sign conflicts, strong agreement
with the source's direction summaries for five inspected targets, and independent
XML confirmation of selected complete count rows. Numeric S5 reproduction
remains failed; no label permutation or endpoint refit was used to improve
agreement. The [concordance audit](Research%20Article/gate2_N2_nabhan_2026/reports/CONCORDANCE_AUDIT.md)
is required context for the fibroblast results. Two verification/audit parsing
issues stopped before result records were written (gzip suffix handling and
an ambiguous RGS5 symbol); corrected versions preserve their implementation
history and did not change any scientific endpoint.

## Nb3 publication figures and RQ derivation, 1 October 2026

The owner requested formal figures following the repository hierarchy, then
explicitly authorized the proposed additional analyses and subsequent RQ
derivation. Codex used the sibling article galleries and shared palette,
recorded a new pre-fit contract, executed marker/control/well/depth and Hallmark
context checks, and derived two proposed biological questions with rivals and
future discriminating endpoints. The [results](Research%20Article/gate2_N2_nabhan_2026/reports/FOLLOWUP_RESULTS.md)
and [derivation](Research%20Article/gate2_N2_nabhan_2026/reports/RQ_DERIVATION.md)
are the current interpretation; source/workbook and independent-unit failures
are not silently resolved by the new analysis.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-01 | Publication figures and additional analysis followed by RQ derivation | Owner | Owner, explicit chat instructions | Authorized | Make existing results inspectable and develop evidence-grounded biological hypotheses |
| 2026-10-01 | Bounded sensitivity batch and species-appropriate Hallmark 2024.1 analysis | Codex | Within authorized analysis; scientific acceptance pending | Freeze before new fits; retain all eligible results and fixed correlation sensitivity | Reuse saved DE while testing concrete panel/depth/pathway uncertainties |
| 2026-10-01 | A19/A20 proposed cards and plans | Codex, grounded in Nb3 and primary references | Owner requested derivation; retain/reject pending | Add proposals, no claim rows or grade changes | Separate epithelial-to-niche function and homeostasis-to-state hypotheses from existing questions |

QA found a clipped S3 title and preserved the first export while shortening
only its labels in a new revision. An initial revision-atlas assertion caught a
Windows case-insensitive glob that also selected atlas files; it stopped before
writing the new atlas/receipt. Restricting selection to numbered figures fixed
it; draft exports remain in ignored tmp. No numerical endpoint changed.

## Nb3 allocation correction and candidate framing, 1 October 2026

The owner rejected the initial Nb3 A19/A20 allocation because main already
contains A19–A21. A remote check and fetch verified those Nb2/Fzd questions at
`f61343cc16c83e979b071393adccdcf8084ea294`; the working HEAD remains the older
`33b27cf`. Codex had allocated from the stale local register. The earlier
responsibility row is retained as historical evidence; its Nb3 IDs are
superseded by A22/A23 in active cards, paths, anchors and references. See the
[correction record](Research%20Article/gate2_N2_nabhan_2026/reports/RQ_ID_CORRECTION_2026-10-01.json).

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-01 | Initial Nb3 A19/A20 allocation | Codex | Owner, explicit correction | Rejected numbering; replace with A22/A23 | Main already owns A19–A21; local register was stale |
| 2026-10-01 | Nb3 A22/A23 folders and active references | Owner | Owner, explicit instruction | Relabel without changing scientific content or existing main questions | Resolve collision; retain historical logs and frozen outputs |
| 2026-10-01 | Full framing of all eight annotations | Owner requested explanation; Codex formulated cards | Within requested clarification; hypothesis acceptance pending | Record evidence, rivals and discriminating outcomes for each candidate | Earlier derivation fully developed only two RQs; missing data do not reject the remaining biological questions |

The [candidate cards](Research%20Article/gate2_N2_nabhan_2026/CANDIDATE_HYPOTHESES.md)
retain E8's tissue-specific and clinical branches beyond A22, distinguish EGF
recipient necessity from ERBB2/ERBB3 dependency, and keep fate and mechanism
claims separate from measured bulk RNA patterns. No additional analysis,
figure revision or claim-grade promotion occurred in this correction.

## Cross-article chronology review and E5 extension, 1 October 2026

The owner then authorized applying strict contribution review across every
article, explicitly using subagents, and requested public E5 metadata and a
README matching sibling hierarchy. Three subagents reviewed disjoint groups;
the parent reviewed Nb3 and accepted only distinct conditional candidates or
material interpretation constraints. [All folder decisions](docs/audits/2026-10-01-cross-article-rq-review/README.md)
include no-change and rejected-transfer outcomes. Existing main-branch
corrections take precedence over stale local readiness text. A1/A16/A17 status
was reconciled and an existing A11 paragraph was moved out of A13. Neither
action re-fitted or changed the original result.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-01 | All-article review with subagents | Owner | Owner, explicit instruction | Review chronology and integrate useful conditional contributions under existing RQs | Later analysis may narrow earlier hypotheses; avoid duplicate evidence |
| 2026-10-01 | Conditional A1/A2/A4/A8/A9/A13/A14/A18/A22 contributions | Codex and three bounded reviewers | Within authorized review; biological acceptance pending | Add dated evidence/rival/discriminator text; no grades | Make candidate relationships explicit without promoting RNA or unidentifiable effects to mechanisms |
| 2026-10-01 | External E5 GSE306184 pilot | Codex after owner's external-data request | Within existing analysis authorization | Freeze after literature/metadata exposure, before expression-value inspection; run descriptive comparisons only | Four contrasts are identifiable, but independent donors, uninjured knockdown and competent AT2 identity are not established |
| 2026-10-01 | Nb3 README and F09 | Owner requested hierarchy; Codex implemented | Within authorized documentation/figures | Align navigation and add a separate external figure | Preserve original results/atlas and expose analysis limits beside visuals |

NCBI acquisition first hit the network sandbox and succeeded after the
standard escalation review. Figure rendering first found the bundled Python
missing matplotlib, then used the existing scientific environment. A reader
expected a GSM column where pandas v1 had retained keys under `index`; the
reader now validates/renames the key without rewriting the run. Visual review
found left-label clipping; separate v2 widens the margin and preserves v1.
Failed documentation patches stopped before mutation and were corrected.

## 1 October 2026: authorize Nb3 delivery

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-01 | Commit, push and open a PR for Nb3 and the chronological RQ review | Repository owner | Repository owner, explicit chat request | Authorized delivery from current main; no merge or scientific acceptance inferred | Preserve main's A19-A21 and integrate Nb3 A22/A23 with reviewed conditional branches |

Integration uses current main for the shared indexes and the corrected A1,
A16 and A17 cards, retaining the historical decision rows. The source checkout
and unrelated local files remain preserved. No frozen numerical output or
claim grade is changed by delivery.

## 1 October 2026: structure the A22 analysis pipeline

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-01 | A22 stage graph, source registry, sample schema, intake reader and figure plan | Codex | Owner explicitly requested A22 pipeline structuring; Codex selected implementation | Structure P0-P6 and execute only source-evidence intake | Separate RNA motivation from biological identity/amount attribution and protein/function evidence |

The new intake validates preserved Nb3 hashes and extracts existing values. It
does not refit the screen or establish independent replication. P2 is a draft
requiring its own exploratory contract; P3-P5 retain source-specific gates.
The first script-writing command failed at Python string parsing before writing
files; the corrected writer saved the reader and the intake passed. Live GEO
retrieval for two series returned browser-check pages; inherited hashed source
metadata, rather than a claimed fresh retrieval, support those design facts.
No scientific acceptance or claim-grade promotion is implied.

## 1 October 2026: keep the main README general

| Date | Prior output | Why revised | Review authority |
|---|---|---|---|
| 2026-10-01 | Nb3-specific highlights and a dated figure-audit notice in the main README | The owner requested only general project context on the main README; detailed study and audit updates belong in their indexes | Repository owner, explicit README cleanup request; Codex applied the scope correction |

Removed the Nb3-only navigation row and figure announcement, retained the
existing study-gallery links in the article index, and moved the dated figure
audit reference beside the paper galleries. Main README execution links now
use the current-state page. No scientific result, figure or claim changed.

## 1 October 2026: structure the A23 analysis pipeline

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-01 | A23 pipeline, source gates, metadata intake, evidence reader and figure plan | Codex | Owner requested the same pipeline structuring for A23 | Structure P0-P6; execute source/metadata intake only | Separate state RNA, measured homeostasis, temporal ordering and restoration/mature recovery |

The inherited evidence audit preserves the eight-well mouse-QC versus seven-well
paired-depth distinction and the AT1 sign-change counterexample. A bounded
primary-source search identified GSE199329; its 2,339-byte official metadata
file was retrieved and hashed. No expression matrix was read. The GEO HTML
browser check did not prevent official FTP metadata retrieval. The publisher
source-workbook link failed retrieval, so no workbook contents are claimed.
PAM CD45 fractions are not separate patients; independent biological validation,
scientific acceptance and claim-grade promotion remain unestablished.

## 1 October 2026: reconcile the A22 pull request with main

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-01 | A22 PR #126 merge conflict resolution | Codex | Owner requested A22 CI issue resolution alongside A23 | Preserve both documentation histories and merge main | Hosted CI was passing; PR #125 introduced overlapping documentation changes |

This change preserves the universal main README, the A22 pipeline and immutable
intake evidence. It resolves a delivery blocker and does not constitute scientific
acceptance or a claim-grade change.

## 1 October 2026: execute the A23 external pilot and source audit

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-01 | A23 P2 descriptive analysis, P3 endpoint linkage, figures and conditional branch | Codex | Owner requested continuation of the A23 pipeline; Codex selected scoped implementation | Execute eligible source analyses; retain P4/P5 data gates | The available human case and mouse assay sheets do not identify a linked causal sequence |

Main now includes A22; both pipeline histories were preserved when merging it
into the A23 branch. The external archive contains nested per-library archives;
the acquisition reader was updated to extract filtered HDF5 files safely.
Ensembl homology retrieval failed, and official NCBI orthologue responses were
used instead. The first matrix attempt stopped on absent PECAM1 before outcome
summaries. An explicit v2 contract conservatively excludes VWF- or EMCN-detecting
cells without replacing the absent gene or changing readout features. The old
contract and failed-attempt record remain. No marker outcome informed the change.

The source workbook supplies cell annotations but not shared IDs across the
selected mouse assay sheets. That limits the compensation branch to a hypothesis.
The first F3 legend overlapped target-gene points; the corrected rendering has a
new filename, with the initial render retained. A targeted rendering-helper
attempt failed before writing corrected images; the indentation fix completed
the versioned render. No numerical outputs were overwritten. Hypothesis
acceptance and scientific claim grades remain open.

A concrete source-selection concern justified one additional post-pilot audit:
1,847 published PAM cells were missing from filtered matrices, while every
published control cell was present. A separate contract and immutable run
recovered all 14,210 published cells from raw matrices. The published-AT2 marker
pattern persists under both frozen QC rules. No outcome-based threshold change
or independent-replication claim was made.

The delivery dependency audit found that the repository's broad PDF ignore rule excluded the six generated A23 PDFs (five current and one superseded). A scoped figure exception, matching the existing A19-A21 and Nb3 convention, includes those receipt dependencies; source PDFs remain ignored.


## A22/A23 extension execution, 1 October 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-01 | Structure and execute A22 identity–amount and A23 transporter-RNA extensions | Codex, following the narrowed RQ discussion | Owner authorized execution; scientific acceptance pending | Two versioned analyses, reports, figures and reviewed conditional branches deposited | Test available discriminators while keeping state, protein, transport, time and recovery gaps explicit |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-01 | A22 v1 exclusion comparisons regenerated target folds | Omission effects were mixed with fold reassignment; v2 fixes the primary assignment across variants and preserves v1 | Codex during verification; no human rejection invented |
| 2026-10-01 | Initial extension-figure legend placement | A22 panel B and A23 panel B legends crowded observations; layout-v2 figures move legends and preserve initial renders | Codex visual review; numerical results unchanged |

The executed analyses weaken the broad A22 operational predictor and do not
support increased transporter RNA as an A23 buffering explanation. They do
not establish causal absence or change the owner's retain/reject decisions.

## Nb4 execution and publication request, 2 October 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-02 | Nb4 article analysis, figures and PR submission | Codex implementation following the owner’s reading and scope | Owner authorized execution, analysis label, hierarchy and publication; scientific acceptance pending | Submit the bounded study package for review | Keep source reproduction, exploratory extensions and missing evidence distinguishable; details remain [article-local](Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/EXECUTION.md) |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-02 | Numerically led figure captions and crowded annotations | Owner requested biological rationale first; visual review identified crowded labels | Owner directed caption style; Codex revised captions and retained versioned renders |

### Nb4 sequential RQ follow-through, 3 October 2026

The owner requested scoping, evidence consolidation, separate pipelines and
sequential execution before reporting. The article-local
[completed sequence](Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/RQ_SEQUENCE_RESULTS.md)
records three executed branches and retained biological endpoint holds. No
global claim grade or scientific acceptance decision changes. The PR includes
the results, fifteen-figure gallery and expanded archive checks.


## Nb4 broader proposal restructuring, 3 October 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Structure separate analysis plans for the broader atlas proposals | Codex following the owner's note-based scope correction | Owner authorized planning; scientific acceptance pending | Deposit article-local plans, source requirements and an execution queue | Preserve biological breadth while keeping eligibility and endpoint limits explicit |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | Earlier RQ derivation focused almost entirely on two existing-question extensions | Owner identified omitted disease, species, evolutionary, residency and cell-identity themes; the limited scope was an implementation choice, not evidence that the atlas is outdated | Owner challenged scope; Codex structured the broader candidate plans |

See the [planning index](Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/proposals/README.md).
Existing results, canonical numbering and scientific acceptance remain unchanged.

## Repository grounding and preservation, 3 October 2026

The owner requested a whole-repository repair after the other session completed:
fetch current main, retain time for research development, and ground all RQs in
hypotheses and evidence rather than choose a preferred RQ immediately. Codex
preserved dirty/detached work and implemented the isolated repair branch.

| Responsibility or decision | Authority and status |
|---|---|
| Whole-repo grounding, main fetch and proceeding with the proposal | Owner instruction in the current session |
| Dossiers, reconciliation, contract runner, CI and documentation | Codex implementation; owner scientific review pending |
| Keep 3A/3B reading open while S1/D1 analysis remains gated | Existing owner reading decision of 1 October; selectively recovered from local work |
| Select an RQ, accept a mechanism or promote a claim grade | Not done; remains an owner scientific decision |
| Treat frozen historical work as retrospectively preregistered | Rejected approach: prior exposure cannot be erased |
| Restore an old checkout wholesale over newer main | Rejected approach: later corrections and Nb4 work would be lost |
| Claim prompts or schemas force scientific truth | Rejected approach: structural gates and integration controls have explicit limits |

See the [repair report](docs/audits/2026-10-03-repository-repair/REPORT.md)
for per-file reconciliation, preservation and verification. No numerical
biological analysis, experiment or new claim acceptance occurred in this repair.


## Primary-source and feasibility review, 3 October 2026

The owner authorized proceeding to the next stage after the repository repair. Codex performed a bounded primary-source and feasibility review of all 24 RQs and nine Nb4 candidates. [Review and limitations](docs/research_dossiers/review_2026-10-03/README.md). No numerical biological analysis, claim promotion, RQ selection or owner scientific acceptance occurred.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Proceed to scientific grounding after the repair | Owner request | Owner authorized work; scientific acceptance pending | Record established precedents, remaining discriminators and feasibility gates | Develop the portfolio before choosing an RQ or experiment |
| 2026-10-03 | Correct first-pass dossiers and evidence locators | Codex review | Codex implementation correction; owner review pending | Restore original question direction and current evidence authority | The initial reformulation introduced scope and provenance errors |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | Codex A0 lung-maturation redirection and A2 epithelial-recipient wording | A0 displaced a stopped cross-tissue test into A8; A2 concerns fibroblast response | Codex self-correction against canonical evidence |
| 2026-10-03 | Codex A7 England and A9 Nb3 primary evidence locators | The relevant observations belong to ES1/CEBPA and the corrected ligand audit | Codex self-correction; no human rejection inferred |
| 2026-10-03 | Codex A13 epithelial-to-fibroblast framing | Reversed the original direction and overlapped A22 | Codex self-correction preserving the negative original model |
| 2026-10-03 | Codex A20 effect-beyond-pool hypothesis | Inverted the existing narrowed pool-maintenance proposal | Codex self-correction against NARROWED_HYPOTHESIS.md |
| 2026-10-03 | Broad-versus-state-selective dichotomy and automatic adjustment language | Broad effects and interactions can coexist; post-treatment state, survival and pool size may be mediators or selection variables | Codex clarified interpretation boundaries; no new causal result |


## Source and capability qualification, 3 October 2026

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Proceed to source and capability qualification | Owner request | Owner authorized stage; scientific acceptance pending | Execute four exposed metadata contracts and document all-question dispositions | Resolve source identity and specific enabling inputs without choosing an RQ |
| 2026-10-03 | Metadata parser, sample tables and mechanical verification | Codex implementation | Codex recorded execution; owner scientific review pending | Keep biological-unit count undetermined and retain current inference holds | Deposited libraries, pooled assays and subseries are not independent units |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | Runner receipts used resolved machine paths | Public receipts should contain portable replay commands, not local executable/worktree paths; execution and hash gates remain intact | Codex implementation correction with regression test; PR review pending |
| 2026-10-03 | A7 summary could be read as ten CEBPA wells | Fresh source records distinguish six CEBPA and four AP-1 condition contexts | Codex clarified source split; frozen ES1 results unchanged |
| 2026-10-03 | A11 novelty review was incomplete | Direct 2020/2026 precedents establish generic HPCS function and regeneration overlap; the exact residual-component contribution still needs qualification | Codex bounded source comparison; no owner rejection or claim promotion inferred |

See the [qualification report](docs/research_dossiers/qualification_2026-10-03/README.md). No expression values, new biological fit, wet experiment or external outreach were performed. All prior contracts, receipts and frozen scientific assets are retained.

## Source recovery and checkout consolidation, 3 October 2026

The owner explicitly authorized remaining jobs 2, 3, 4 and 6, reserved article/capability preparation for themselves, and said they would merge the PR. Codex implemented the [follow-up](docs/research_dossiers/followup_2026-10-03/README.md); scientific acceptance and integration remain owner decisions.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Consolidate primary checkout | Owner request | Owner authorized; Codex implemented | Preserve 685 paths on a local recovery branch, retain private settings and verify ignored files, then use a separate PR review branch | Make the normal checkout usable without discarding old work or merging the PR |
| 2026-10-03 | Extend metadata qualification | Owner request / Codex implementation | Codex execution; scientific acceptance pending | Freeze new contracts and verify 984 library identity joins; retain missing biological identities | Database identities are not independent units |
| 2026-10-03 | Qualify outcomes and novelty | Owner request | Codex bounded review; owner review pending | Record exact missing joins and contribution boundaries across the portfolio | Published endpoints and generic plasticity do not automatically answer the current RQs |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | A5 required a reverse GEO ID in every BioSample | Independently submitted records use MUC sample aliases and omit that field. The first run stopped; its receipt remains. A prospectively frozen source-specific amendment verifies exact declared accessions/aliases and rejects contradictory reverse IDs | Codex correction; no biological gate relaxed |
| 2026-10-03 | Hash-bound metadata code was subject to Windows newline conversion | A real checkout produced different byte hashes. Exact-byte Git attributes cover only the six bound files; frozen source contents and hashes remain unchanged | Codex portability fix; owner PR review pending |
| 2026-10-03 | General AT2 flexibility or cancer developmental-program overlap could appear novel | Frank 2016 and direct HPCS/developmental-program precedents already support those broad claims; precise residual comparisons remain open | Codex source-grounded clarification; no question rejected or result promoted |

The old worktrees and their ignored inputs remain retained. No external outreach, expression fit, laboratory work, RQ selection or PR merge occurred.

Final preservation verification also caught newline normalization of the separately archived failed A5 receipt. Codex added an exact-byte attribute for that archive and restored the original receipt bytes/hash from the retained runner output. Its failed status, the successful amendment and all scientific results remain unchanged.

## Published model review and continuation audit, 3 October 2026

The owner supplied research papers, requested funded-direction/model comparison,
confirmed no host access, and explicitly authorized a subagent for that bounded
comparison. Codex reviewed the returned private artifact and integrated public
method evidence and the [completion audit](docs/research_dossiers/capabilities_2026-10-03/NEXT_STEPS.md).
The latest request is an accurate PR revision and a Claude Science continuation
handoff. It does not constitute scientific acceptance or permission to merge.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Assess papers, published models and funded future directions | Owner | Owner authorized work; scientific review pending | Codex main reviewed 32-PDF inventory/method evidence; one user-authorized subagent wrote the private eight-lab comparison | Ground feasibility without attributing collaborators' models or grant aims to confirmed host access |
| 2026-10-03 | Audit original plan and revise open PR/handoff | Owner | Codex implementation; owner integration pending | Record each original job's completed and remaining portions; retain full experiment packages as unfinished | Prior research dossiers do not yet establish bench readiness |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | Preliminary uncommitted capability-stage index listed 24 conditional packages as deliverables | Only the model review and status audit had been written when the owner requested a continuation handoff; the final index explicitly leaves packages pending | Codex corrected its draft before integration; no human rejection inferred |
| 2026-10-03 | Published method/coauthorship/funding could be read as actual laboratory capability | Owner confirms no access; Yadav assigns Wagner spatial analysis, and future funded models need local validation | Codex and the authorized subagent qualified attribution/access; no lab availability inferred |

No existing scientific script, frozen output, source contract, run receipt or
claim grade changed. No new expression analysis, outreach, RQ selection or merge
was performed. The private comparison and handoff are intentionally outside Git.

## 3 October 2026: conditional package continuation

The owner requested continuation of the scientific handoff. Codex authored
24 packages and nine Nb4 supplements, checked targeted primary precedents and
inspected labels in a new public supporting workbook. No subagent was used.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Conditional designs and eligibility ledger | Codex under owner continuation request | Owner authorized work; scientific acceptance/integration pending | Prepare all-question drafts with explicit unknowns and stop decisions | Complete independent package development without inventing access or positive results |
| 2026-10-03 | Rochelle supporting workbook intake | Codex | Codex source-reading decision; owner review pending | Record donor/time labels and missing preparation links | Partial identity recovery does not establish the A8/A19 comparison |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | A11 draft offered alternative primary estimands | Specify patient-held-out log-loss increment; paired context differences become secondary | Codex self-review; no human rejection inferred |
| 2026-10-03 | A21 draft equated later gCap counts with renewal | Require new progeny with division evidence and retained gCap identity | Codex self-review |
| 2026-10-03 | Proposed dossier-tail and current-progress replacements | Automatic approval review rejected potential loss of prior content; all existing-document additions are append-only | Automatic approval review; Codex adopted safer edits |

No governance, validator, frozen code/output, contract, receipt or claim grade
was changed. Packages await explicit owner scientific review; no outreach,
experimental procedure, scientific acceptance or merge occurred.
See the [stage ledger](docs/research_dossiers/packages_2026-10-03/LEDGER.md).

## 3 October 2026: post-merge documentation reconciliation

GitHub records [PR #130](https://github.com/xorca0711/scRNA_seq/pull/130) merged
by `xorca0711` (Xorca) at 05:37:38 UTC into `b52ad6b`. This records repository
integration only; the merge does not supply a separate scientific-acceptance
decision. Earlier rows retain the status that applied when they were written.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Integrate research grounding and conditional packages, PR #130 | Codex under owner requests | `xorca0711`, verified GitHub merge actor | Integrated at `b52ad6b`; scientific review remains pending | Establish the repository baseline with unresolved requirements explicit |
| 2026-10-03 | Reconcile current documentation and private handoff | Codex audit; owner requested fixes | Owner authorized documentation work; new PR review pending | Point entry pages to drafted packages and current remaining work; preserve historical checkpoints | Earlier instructions still requested package drafting and PR #130 integration |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | Current-navigation wording still treated packages as unwritten and the September roadmap as current priorities | Packages were drafted in `4395ecf` and integrated in `b52ad6b`; next work is review and qualification | Codex under the owner's documentation-fix request; no new scientific decision inferred |

The main README retains its general research overview and existing claim-register
links. No claim table, scientific grading, governance or frozen evidence was
changed. The normal checkout and all retained inputs remain untouched by this
documentation revision. Private lab planning stays outside Git.

## 3 October 2026: remaining-job qualification

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Integrate documentation reconciliation, PR #131 | Codex under owner request | `xorca0711`, verified GitHub merge at 05:58:32 UTC | Integrated at `76dc9b4`; scientific acceptance remains separate | Current navigation and remaining-job accounting are available on main |
| 2026-10-03 | Proceed with remaining repository-grounding jobs | Owner | Owner authorized work; new PR/scientific review pending | Align normal checkout; qualify new source labels and A17 numerical components; review packages | Make progress on available evidence without inventing laboratory access |
| 2026-10-03 | Freeze and execute A8 metadata / A17 synthetic qualification | Codex under owner continuation | Codex bounded execution decision; scientific acceptance not assessed | Contracts frozen at `78845fc`; two successful verified receipts | Both tasks have real inputs and explicit descriptive/numerical limits |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | A4's evaluable-lineage fraction could silently exclude lost follow-up | Specify the prospective t0 denominator, separate missing/loss outcomes and bounds; survivor-conditioned fraction is secondary | Codex proposed refinement; owner scientific review pending |
| 2026-10-03 | A17 draft combined clone-size/count scoring | Size ≥2 retained measurements do not by themselves qualify a count/extinction likelihood; observation model and ascertainment must be explicit | Codex proposed refinement preserving historical evidence |

No governance gate or old scientific code/output was weakened or overwritten.
The independent verifier used standard-library RK4 after SciPy was unavailable;
the frozen runs and all failed historical receipts remain unchanged. No human
scientific acceptance, lab access, RQ selection or wet experiment is inferred.

## 3 October 2026: bounded mapping closeout

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Finish recoverable mapping work; defer scientific review and placement work | Owner | Owner authorized this scope; PR integration/scientific acceptance pending | Close current recovery task with explicit evidence holds and reopening conditions | Unknown biological links must remain honest without becoming endless repeated searches |
| 2026-10-03 | Inspect the two previously unexamined Rochelle H5 file structures | Codex under owner request | Codex bounded read-only inspection; no claim promotion | Record exact source attributes, range provenance and cross-assay limitations | Test the remaining concrete file candidate without expression fitting |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | Earlier remaining-work wording grouped all outstanding evidence and bench requirements as immediate jobs | Owner clarified that scientific review is later and actual access belongs to the placement phase; some fields may not be recoverable from current public sources | Owner scope correction, recorded by Codex |
| 2026-10-03 | Treating deferred A17 model qualification as only human review or a placement dependency | A probability/tail solver and further technical identifiability work remain genuinely unfinished | Codex clarification; no new execution or acceptance inferred |

No governance, validator, frozen scientific asset or biological interpretation
limit was weakened. The source-recovery task is closed within the inspected
scope; missing evidence is not declared universally nonexistent. Author contact
and recurring monitoring were not performed or scheduled. PR #132 remains the
owner's integration decision.

## 3 October 2026: RQ README and dossier alignment

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Integrate qualification and source closeout, PR #132 | Codex under owner scope | Owner GitHub merge, 07:27:11 UTC | Integrated at `bf7d716`; no scientific acceptance inferred | Metadata task closeout and deferred-work boundaries are on main |
| 2026-10-03 | Align the actual RQ folder READMEs with dossiers/packages | Owner | Owner requested correction; follow-up PR review pending | Add question-specific summaries to 17 RQ entrypoints and the shared A5/A11 README; align the 24-question index and all dossiers | Folder readers should see the current discriminator, endpoint, evidence and hold without reconstructing prior chats |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | Calling repository preparation settled while local RQ READMEs still had only a dossier pointer | The owner identified a real entrypoint-alignment gap; dossier package-pending prose was also stale | Owner correction, implemented by Codex |

This is documentation alignment to existing packages and recorded refinements.
It does not accept a hypothesis, change a frozen contract/result, reopen source
recovery, or start deferred biological/technical review. Existing RQ README
analysis bodies are preserved; no empty execution folders or new RQ IDs are added.


## 3 October 2026: rejection of vague visual RQ framing

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Review the atlas's broad one-line questions and generic assay bridges | Owner | Owner requested review and plausible fixes; adoption of replacements remains open | Produce a source-grounded specificity audit and proposed repairs; do not silently change canonical questions | An assay needs a named biological contrast and an interpretable outcome |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | Codex's A0–A23 visual-atlas summaries and generic assay framing | Owner found the summaries too vague/broad to yield useful hypotheses or experiments; self-review confirms lost biological specificity and conflation of supporting work with the organizing question | Owner rejected the framing; Codex recorded the rejection and proposed repairs |

The [specificity review](docs/research_dossiers/RQ_SPECIFICITY_REVIEW_2026-10-03.md)
preserves useful source evidence and distinguishes restored details from new
candidate narrowings. A technically rendered figure and passing repository
checks do not constitute scientific acceptance. The rejection does not discard
all RQs, reclassify historical findings or establish acceptance of replacements.

## 3 October 2026: apply source-qualified RQ specificity

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Check latest main and apply literature-qualified RQ fixes | Owner | Owner authorized application; scientific acceptance and integration remain pending | Reuse merged PRs #130–#133; align current cards, dossiers, packages and dedicated READMEs | Earlier summaries obscured named biology and did not distinguish published premises from the remaining contribution |
| 2026-10-03 | A4 Fzd5 entry gate; broad A14/A23 novelty language | Codex prior proposal | Codex source-grounded revision, not owner retain/reject | Do not adopt A4 gating; constrain A14 and narrow A23 entry-versus-exit comparison | Current primary evidence does not justify A4 direction; Ciminieri and Lv constrain novelty |

The application ledger distinguishes fresh source inspection from reused audits
and records access limits. Documentation changes do not amend frozen designs,
accept biological hypotheses or weaken governance. No new analysis was run.

## 3 October 2026 Nb5 scientific review and question registration

The owner requested review and potential registration/extension, then specified
that different biological focus, target and cell/context heterogeneity should
remain separately registered rather than universally covered by older RQs.
Codex completed the [bounded review](Research%20Article/gate2_N4_nabhan_aging_atlas_2020/rq_review/README.md)
and applied proposed A24–A27, an A3 extension and explicit supporting mappings.
These are agent scientific assessments under owner-authorized registration;
no human retain/reject or scientific-acceptance decision is recorded.

The broad P04 frame is narrowed prospectively to paired spleen/marrow CD8
context after outcome exposure. A27's generic within-state novelty is constrained
by older primary evidence. Biological heterogeneity preserves question identity;
it does not certify novelty or make unsupported data eligible. The governance
document's current-ID range changes only to reflect registration; no requirement,
validator, frozen contract or interpretation safeguard is weakened.


The layout validator's explicit accepted sequence advances from A0–A23 to
A0–A27. Exact order/equality is retained, with adverse tests for missing,
duplicate, reordered and unregistered IDs. Its existing script is declared as
infrastructure in the registry; scientific assets remain subject to registration.
This small validator update and the governance current-ID wording require
explicit PR review. No review approval is claimed by the authoring agent.

## 3 October 2026: literature-grounded RQ context and schematic integration

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-03 | Incorporate recent primary literature into RQ derivation and place explanatory schematics in question entrypoints | Owner | Owner requested implementation; integration and scientific review pending | Add the workflow, all-question context and versioned illustrations; preserve existing hypotheses and results | Readers need to see how prior findings support a possible extension and what each readout decides |
| 2026-10-03 | Bind explanatory SVGs/context to the registry | Codex | Explicit governance PR review pending | Add narrow provenance/drift checks without a fabricated numerical run | Instruction text alone cannot detect missing context or stale illustrations |

| Date | Proposal changed | Why | Who changed it |
|---|---|---|---|
| 2026-10-03 | Treating the previously recorded bibliography as sufficient for a wider-literature novelty answer | The owner asked about all published work; closer A25/A26 precedents require more careful boundaries | Owner scope correction; Codex propagates the sources and leaves complete overlap qualification open |

No human retain/reject decision, novelty clearance, claim promotion, model access
or laboratory readiness is inferred. The 24 earlier v2 drawings remain preserved;
four new qualitative companions cover the subsequently registered questions.

## 7 October 2026: negative-results documentation placement

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-07 | Move the generated negative-results index under docs | Owner requested root cleanup; Codex selected the docs destination | Owner requested implementation; PR integration pending | Update the generator and current navigation; preserve all 162 entries and historical snapshots | Keep root entrypoints concise while retaining visible access to negative evidence |

### PR #143 CI correction

The initial local checklist omitted the separate research-governance workflow.
CI exposed two unregistered documentation assets: the negative-results renderer
and generated claims manifest. Codex classifies these exact paths through the
existing infrastructure registry for explicit owner review in PR #143; no
scientific receipt, independent approval or claim promotion is invented. The
validator, immutable baseline and all biological asset requirements are unchanged.

## 7 October 2026: illustrated-guide readability

Owner requested a more readable illustrated-question entrypoint. Codex grouped
existing questions by topic, supplied descriptive navigation labels and direct
diagram links, and included all 31 registered guides. Grouping does not rank
questions or revise hypotheses; the underlying context, figures and scientific
acceptance remain unchanged. Implementation is prepared for PR review.


## Repository readiness audit and numerical corrections — 7 October 2026

Codex performed the owner-requested full-repository audit, implemented versioned
Wp corrections, synchronized current documentation and prepared a return checklist.
No subagent was used. Existing PR145 merge is an integration fact; it is not
scientific acceptance of every interpretation. This new audit is proposed for
review, with no human retain/reject decision or claim-grade promotion recorded.

| Date | Item | Proposed by | Decided by | Decision | Reason |
|---|---|---|---|---|---|
| 2026-10-07 | Full repo audit, fixes and two-week handoff | Owner request | Owner (scope authorization) | Execute audit and preserve evidence | Explicit request to reconcile text, QC, pipelines and latest Wagner/Wang analysis |
| 2026-10-07 | Versioned Compass, R4/M3 and documentation corrections | Codex | Owner review pending | Implemented on scoped audit branch | Reproducible sign/denominator defects and stale current indexes |

| Date | Rejected or substantially modified AI output | Reason | Rejected/reworked by |
|---|---|---|---|
| 2026-10-07 | Wp R2 claim that the negative PGAM association survives | Raw penalties were labelled as transformed consistency; corrected rho is positive | Codex audit; biological acceptance remains with owner |
| 2026-10-07 | R4 v1/v2 full-CP10K description and dependent M3 summaries | Scoring denominator used selected genes; replaced by full-gene v3/v2 corrections | Codex audit |
| 2026-10-07 | Regulatory non-movement, TPM-confound removal and definitive mechanism labels in A28/A29 | Null contrasts do not establish equivalence, matching does not solve composition, and proposed outcomes do not uniquely identify mechanisms | Codex audit; hypotheses preserved and interpretation narrowed |
| 2026-10-07 | Correction figure v3 layout | Footer overlapped x-axis label during visual QA; v4 changes layout only | Codex visual review |

Evidence: [readiness audit](docs/audits/2026-10-07-repository-readiness/REPORT.md),
[correction report](Research%20Article/gate2_W2_wagner_Th17_PGAM/CORRECTIONS_2026-10-07.md),
and [return checklist](docs/audits/2026-10-07-repository-readiness/RETURN_CHECKLIST.md).
