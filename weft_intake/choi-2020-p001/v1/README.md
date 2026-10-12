# Choi 2020 / P001: reviewed Weft handoff, v1

Recorded 12 October 2026. This package indexes the already integrated Choi
benchmark; it is not a fresh discovery, another analysis or another biological
replicate. [Manifest](manifest.json) records the evidence identities and hashes.

**Source:** Choi et al., *Inflammatory Signals Induce AT2 Cell-Derived
Damage-Associated Transient Progenitors that Mediate Alveolar Regeneration*,
Cell Stem Cell (2020), [DOI 10.1016/j.stem.2020.06.020](https://doi.org/10.1016/j.stem.2020.06.020).
Input accession: GSE145031. Published results and repository observations are
compared separately in the [scientific review](../../../Research%20Article/gate1_02_choi_2020/weft_pilot_v1/SCIENTIFIC_REVIEW.md).

## Gate assessment and permitted use

This is a retrospective map onto [Weft's gate specification](https://github.com/xorca0711/weft/blob/main/docs/GATES.md),
not evidence that an autonomous G0–G8 engine ran.

| Gate | Assessment for this package |
|---|---|
| G0/G1 scope, identity and access | Bounded source/input/runtime and publication recovery qualified for this attempt |
| G2 reading relevance | Previously read and deliberately outcome-exposed; not an unseen screening test |
| G3 data eligibility | Suitable for the stated description; one pooled library per condition cannot support animal-level treatment-effect inference |
| G4 execution readiness | Frozen contract, source, bounded runtime and output isolation qualified for the completed attempt |
| G5 reproduction | Adapted descriptive run and QC completed; four labels recovered and pAT2 absent, so exact five-state reproduction is unsupported |
| G6 extension validity | No extension performed or authorized by this handoff |
| G7 question contribution | No new canonical RQ; retain discrepancies and measurement limitations |
| G8 integration | Owner retained the bounded benchmark; [Ravel #149](https://github.com/xorca0711/ravel/pull/149) merged at `34675134a5581989d028102a93ae51eebc84a501`; both main CI workflows passed |

The [human disposition](../../../Research%20Article/gate1_02_choi_2020/weft_pilot_v1/REVIEW_DISPOSITION.md)
permits descriptive retention only. It does not accept a causal mechanism,
promote a claim grade or change A0/A1's interpretation boundaries. Review retains
annotation, denominator and resolution sensitivity, including unfavorable results.

## Materials gathered by this handoff

| Material | Canonical evidence |
|---|---|
| Historical pilot design | [Pilot plan](PILOT_CHOI_2020.md) |
| Figure/supplement/input review | [Migrated source review](PILOT_CHOI_REVIEW.md) and [input inventory](records/pilot-inputs-20261011.json) |
| Trial scientific summary | [Migrated scientific review](PILOT_CHOI_SCIENTIFIC_REVIEW.md) |
| Methods and frozen contract pointers | [Article package](../../../Research%20Article/gate1_02_choi_2020/weft_pilot_v1/README.md) |
| QC and comparison with the paper | [Scientific review](../../../Research%20Article/gate1_02_choi_2020/weft_pilot_v1/SCIENTIFIC_REVIEW.md) |
| Publication and restoration | [Publication guide](../../../Research%20Article/gate1_02_choi_2020/weft_pilot_v1/PUBLICATION.md) |
| Original run receipt | [Receipt](../../../analysis/research/runs/p001_figure1_v1_f001_d56ee41e13cd4327/receipt.json) |
| Complete output inventory and checksums | [Release lock](../../../analysis/research/published_outputs/choi_figure1_v1.json) |
| All 15 unchanged outputs | [Public release](https://github.com/xorca0711/ravel/releases/tag/choi-p001-figure1-v1) |

Run `python analysis/scripts/restore_published_outputs.py` from a Ravel checkout
to restore the published outputs into
`analysis/research/runs/p001_figure1_v1_f001_d56ee41e13cd4327/`.
It verifies the locked archive and preserves conflicting files by stopping.
It does not rerun the analysis or download raw inputs.

The three scientific dossier documents now live here; their Weft paths are
navigation stubs. Five original public receipt snapshots are retained byte for
byte here and in Weft's audit history; their earlier pending states are historical.

No full text, private Drive locator, coordinator database or additional dataset
is copied into this package. Choi's private coordinator remains held pending
reconciliation before any future job; the separate fresh-paper B4 hold is unchanged.
