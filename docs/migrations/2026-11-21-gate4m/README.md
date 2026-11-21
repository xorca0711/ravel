# Gate 4M paper package locations

The [article roadmap](../../../Research%20Article/README.md#gate-4-topic-centered-reading) lists Damani–Yokota as 4M-04 and Nagaraja as 4M-02. The [per-file provenance map](../../../analysis/research/path_migrations.json) preserves earlier scientific references.

**Damani–Yokota.** All 126 original files are in the [Gate 4M package](../../../Research%20Article/gate4M_04_damani_yokota_2026/README.md). Of them, 109 had already moved from the former Gate 2 archive in an accepted migration. Each second move names its first source, retains the same hash and uses the same filename relative to the intermediate folder. The old ungated address holds two short navigation pages for immutable historical documents.

**Nagaraja.** Of 89 tracked files in the former ungated folder, 87 moved under their existing relative names. The former overview became the [analysis records index](../../../Research%20Article/gate4M_02_nagaraja_2026/ANALYSIS_RECORDS.md). Its figure-link stub was superseded by the existing [14-figure gallery](../../../Research%20Article/gate4M_02_nagaraja_2026/FIGURES.md). The 71 files referenced by contracts, receipts or the historical baseline have individual provenance records. Figures and numerical run outputs remain at their recorded locations.

**Owner review.** The proposed Damani-specific second-move rule checks the first record in the intermediate source revision, the source bytes from both revisions, the file at its final path and the absence of both archived originals. The gate rejects unrelated chains, duplicate endpoints and further moves. Archive records can be verified through both original addresses. The runner refuses replay through migrated paths. PR review governs acceptance of this change.

## Verification against main

At `9ffb1d1`, every Damani source path on main (`544c7bb`) had a Gate 4M counterpart. Comparing unfiltered Git blob bytes confirmed 125 identical files. The remaining file was the paper README with the revised reading classification. The equivalent Nagaraja inventory found 87 identical files and accounted for the two navigation pages above. The old Nagaraja directory had no remaining tracked files.

All 12 migration tests passed. The [PR governance check](https://github.com/xorca0711/ravel/actions/runs/44883299911) verified the archives against main, and the [PR repository check](https://github.com/xorca0711/ravel/actions/runs/44883299989) verified the package and its links. The [push check from the original folder-only state](https://github.com/xorca0711/ravel/actions/runs/44883296616) identified missing intermediate contract files in its historical baseline, `03cd566`. Those records remain available for inspection in Git history.
