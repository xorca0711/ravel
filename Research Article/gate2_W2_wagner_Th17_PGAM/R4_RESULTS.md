# Wp-R4 result: the human claim is a donor-level axis, not the module

Executed 4 October 2026 under the governed runner, twice. Contract v1
[config/human_signature_transfer_v1.json](config/human_signature_transfer_v1.json)
→ receipt
[analysis/research/runs/wp_human_signature_transfer_v1/receipt.json](../../analysis/research/runs/wp_human_signature_transfer_v1/receipt.json);
amendment v2
[config/human_signature_transfer_v2.json](config/human_signature_transfer_v2.json)
→ receipt
[analysis/research/runs/wp_human_signature_transfer_v2/receipt.json](../../analysis/research/runs/wp_human_signature_transfer_v2/receipt.json).
Both verified clean. v1 is preserved unchanged; v2 adds a matched-size random
gene-set null and nothing else. The null was written **after** reading v1, which
is why it is recorded as an amendment rather than as a pre-registered endpoint.

**Unit.** Donor. 12 donors — 6 multiple sclerosis, 6 idiopathic intracranial
hypertension — with CSF for all 12 and blood for 10, one library each. This is
the only donor-level unit anywhere in the paper. The signatures being transported
are the mouse study's own, so this is signature transport, not validation.

## What the paper claims (Fig. S4)

Both modules up in MS blood *and* CSF; the EGCG signature up in MS blood only;
the N1, P1 and P4 programmes higher in MS blood.

## 1. Deposit problems that had to be fixed first

| Problem | Effect | Fix, made before freezing |
|---|---|---|
| One CSF sample (PST83775) is deposited as an unfiltered 737,280-barcode matrix, median 0 detected genes | 0 cells; donor lost from the CSF contrast | Samples with > 100,000 barcodes get a 500-UMI cell-calling floor → 1,371 called, 623 gated |
| Hard-zero lineage exclusion (LYZ, HBB, … all zero) | 1, 8, 31 and 124 T cells retained in four blood libraries — ambient RNA makes those transcripts near-ubiquitous in blood | Gate compares summed panel signal instead → 724–2,957 cells per blood library |

Final set: 35,928 CD4-lineage (non-CD8) T cells across all 22 units, 338–4,369
per unit, no unit below the 20-cell floor. CD4 transcript is not required by the
gate, so the label is "CD4-lineage", not "CD4+".

Mouse→human mapping is symbol identity: 57/63 and 24/30 module genes, 781/928 of
the Table S3 Th17n-EGCG signature, 36/50 N1 and 85/108 P4 markers.

## 2. Disease, within tissue

| | CSF (6 vs 6) | | Blood (5 vs 5) | |
|---|---|---|---|---|
| Score | MS − IIH | BH | MS − IIH | BH |
| Pro-inflammatory (S1 HVG) | +0.003 | 0.93 | +0.055 | 0.054 |
| Pro-regulatory (S1 HVG) | 0.000 | 0.93 | +0.064 | **0.039** |
| Pathogenicity (difference) | −0.004 | 0.93 | −0.008 | 0.67 |
| Th17n EGCG (Table S3) | +0.001 | 0.93 | +0.019 | 0.31 |
| Th17n EGCG (Wp-R3) | +0.005 | 0.93 | +0.042 | 0.086 |
| Programme N1 | +0.003 | 1.00 | +0.069 | **0.039** |
| Programme N3 | −0.062 | 0.15 | +0.017 | 0.78 |
| Programme P1 | −0.042 | 0.93 | +0.005 | 0.55 |
| Programme P4 | +0.009 | 0.93 | +0.070 | **0.039** |
| Activation (declared set) | −0.040 | 0.93 | **−0.177** | **0.039** |
| Proliferation (declared set) | +0.017 | 0.93 | +0.057 | **0.039** |

**In CSF, no score separates the disease groups** — nothing reaches BH ≤ 0.05;
every module and signature score sits at BH 0.93, and the smallest adjusted value
anywhere in CSF is programme N3 at BH 0.147 (unadjusted p = 0.0087, *lower* in
MS). The paper's claim that both modules are up in MS CSF does not reproduce.

**In blood, almost everything separates them** — both modules, three programmes,
proliferation, and the activation set. Mann-Whitney on 5 versus 5 cannot return a
p below 0.0079, and several scores sit exactly at it, so these are the
extreme-rank configurations rather than precise estimates.

Two features of the blood result point away from a module-specific effect. The
activation score moves in the *opposite* direction (MS lower by 0.177) and
correlates with every module score across the ten blood donors at Spearman
−0.61 to −0.87. One donor-level axis, with MS on one side and the
intracranial-hypertension cohort on the other, moves all of these gene sets at
once.

## 3. The matched-size random gene-set null settles it

1,000 random gene sets of the same mapped size, drawn from the same gene universe
and scored identically (seed 20261004):

| Tissue | Score | Genes | Observed MS − IIH | Random-set 95 % interval | Empirical p |
|---|---|---|---|---|---|
| Blood | Pro-inflammatory | 57 | +0.055 | +0.004 to +0.070 | 0.29 |
| Blood | Pro-regulatory | 24 | +0.064 | −0.035 to +0.078 | 0.19 |
| Blood | Programme N1 | 36 | +0.069 | −0.010 to +0.071 | 0.10 |
| Blood | Programme P4 | 85 | +0.070 | +0.020 to +0.063 | **0.020** |
| Blood | Th17n EGCG (S3) | 781 | +0.019 | +0.035 to +0.046 | **0.000 (weaker than random)** |
| Blood | Th17n EGCG (Wp-R3) | 407 | +0.042 | +0.032 to +0.050 | 0.88 |
| Blood | Activation | 10 | −0.177 | −0.023 to +0.105 | **0.001** |
| Blood | Proliferation | 10 | +0.057 | −0.030 to +0.095 | 0.40 |
| CSF | Pro-inflammatory | 57 | +0.003 | −0.015 to +0.023 | 0.95 |
| CSF | Programme P1 | 27 | −0.042 | −0.020 to +0.030 | **0.003** |

**A random 57-gene set separates the two blood cohorts about as well as the
pro-inflammatory module does** — the null interval is centred above zero
(+0.004 to +0.070) and the observed value sits inside it. The same holds for the
pro-regulatory module, programme N1 and the proliferation set. The Table S3 EGCG
signature performs *worse* than matched random sets. Only three results exceed
their null: the activation set in blood (in the direction that makes MS *less*
activated), programme P4 in blood, and programme P1 in CSF (lower in MS).

So the Figure S4 blood result is reproducible as a number and is not specific to
the modules: in this cohort any gene set of comparable size separates the two
blood groups, which is what a batch, processing or cohort-composition axis looks
like. The deposit carries no processing date, batch or sequencing-run field, so
the axis cannot be identified — only shown to be non-specific. **This closes
Wp-P05 in the negative direction: the human data do not provide independent
support for the pathogenicity-module claim.**

## 4. Tissue, within donor (10 paired donors)

| Score | Median CSF − blood | Donors positive | Wilcoxon p | MS vs IIH difference p |
|---|---|---|---|---|
| Pro-inflammatory | +0.063 | 10/10 | 0.0020 | 0.095 |
| Pathogenicity | +0.049 | 9/10 | 0.0039 | 1.00 |
| Th17n EGCG (S3) | +0.014 | 9/10 | 0.0039 | 0.55 |
| Th17n EGCG (Wp-R3) | +0.029 | 9/10 | 0.0059 | 0.55 |
| Programme P1 | +0.059 | 10/10 | 0.0020 | 0.42 |
| Activation | +0.109 | 8/10 | 0.037 | 0.15 |
| Pro-regulatory | +0.007 | 6/10 | 0.70 | 0.55 |
| Proliferation | −0.013 | 4/10 | 0.56 | 0.095 |

The pro-inflammatory module, the pathogenicity score and both EGCG signatures are
higher in CSF than in the same donor's blood, consistently and with the paired
donor as the unit — the cleanest positive result in this stage. It is also
disease-independent (paired difference does not differ between MS and IIH), and
activation rises in CSF too. The honest reading is a compartment effect: CSF
T cells look more activated and more "pro-inflammatory-module-high" than blood
T cells in both diseases. Whether that is anything more than activation is not
resolvable here, because the paired contrast was not run against the random-set
null.

## 5. Independent arithmetic check

Donor-level means recomputed from the per-cell output file, outside the pipeline:
maximum absolute deviation 9.8 × 10⁻¹⁷ across all 22 units and every score; cell
counts per unit identical. The v2 null table reproduces the v1-era dry-run values
to the digit (maximum difference 0.0 in both the observed statistic and the
empirical p), confirming the fixed seed.

## 6. Limits

- Six donors per group, five per group in blood; 0.0079 is the smallest
  attainable Mann-Whitney p.
- The comparison group is an idiopathic-intracranial-hypertension cohort, not
  healthy donors, and the groups differ in more than disease.
- Symbol-identity orthology loses renamed and one-to-many orthologs
  (147 of 928 EGCG-signature genes, 14 of 50 N1 markers).
- The gate keeps all CD4-lineage T cells; the paper may have restricted to a
  memory or Th17 subset, which the deposit's own annotation would be needed to
  match.
- No batch or processing field is deposited, so the donor-level axis in blood is
  demonstrated to be non-specific but not identified.
- The random-set null was specified after seeing v1 and is reported as a post-hoc
  amendment.
