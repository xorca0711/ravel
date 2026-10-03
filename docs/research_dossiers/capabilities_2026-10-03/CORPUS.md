# Supplied PDF corpus and review coverage

32 PDF files, 677 PDF pages, inspected 3 October 2026. File identity hashes are SHA-256 of the original read-only PDFs. Main papers and supplements are not independent studies. Automated text extraction is complete; the coverage column states the narrower human-readable review actually used. Full texts and private source-directory paths are not redistributed.

The earlier pypdf pass stalled on some files and was stopped; pypdfium2 completed the remaining extraction after a text-page API correction. This was a reading-cache issue, not a biological analysis or missing source. Model-definition pages P19 p12 and P20 p21 were also visually checked.

| ID | Source | PDF pages | Review used | SHA-256 |
|---|---|---:|---|---|
| P01 | [DuPage 2015 / Treg EZH2](https://doi.org/10.1016/j.immuni.2015.01.007) | 13 | Models/methods and context | `d9a6eeb979b663109fdf5eda59f62ff74b3f80e5f8bb1ea0dba01997e32c7b64` |
| P02 | [Wang 2018 / intratumoral Tregs](https://doi.org/10.1016/j.celrep.2018.05.050) | 14 | Models/methods and context | `ef3fe1cf375b373b3d24c2780b99fffe437a174df760412af7d2fb1eb4ebcc81` |
| P03 | [Zhang 2026 / Treg and NK tumor control](https://doi.org/10.1126/sciimmunol.adx4411) | 16 | Models/methods and contributions | `476c35571d5fcede9f3e32a6f53d493967f65180b3f03fbf5d0353c95d7a6b23` |
| P04 | [Saxton 2021 / IL-22](https://doi.org/10.1016/j.immuni.2021.03.008) | 23 | Models, signaling, organoid methods | `e11222f47abbf0ea7e5c1ea491c972756da9c22ebe977f436ba5a4638712c969` |
| P05 | [Saxton 2021 / IL-10](https://doi.org/10.1126/science.abc8433) | 13 | Cell systems, signaling, methods | `75466d31759718c1e863a245a69e95a9394f4dfe84a38afe4ed7ad3a12a2fd32` |
| P06 | [Yin 2019 / PKC and Wnt](https://doi.org/10.1016/j.ccell.2019.07.002) | 23 | Model/resource context | `e1c37c292bb81269a8fe4627847771fffb6a20eda168a7f478c3b1a4ea18d7a1` |
| P07 | [Tabula Muris Senis 2020](https://doi.org/10.1038/s41586-020-2496-1) | 28 | Sampling/age/model methods | `df8f29ac0d23752bee2341174f3e25b5c8a4bd9b4b4784a3e7f66e7d74267f02` |
| P08 | [Nabhan 2018 / Wnt niches](https://doi.org/10.1126/science.aam6603) | 7 | Figures and web model methods | `60a13c0744d10b08a83aef8c121d5c51533244ad8d74f5504147fa9e1a8fca98` |
| P09 | [Nabhan 2023 / Fzd agonists](https://doi.org/10.1016/j.cell.2023.05.022) | 34 | Models/methods, growth and identity | `80f91f8810312613d8926d6e190f5ed3729dfd2913015a6f0df6ee9733d85963` |
| P10 | [Nabhan 2026 / stem-niche dialogue](https://doi.org/10.1073/pnas.2606113123) | 10 | Models, scope, limitations | `a2c3784e946bbae823b8b7634da969ead72eea31dfcb230e56676be47f934b47` |
| P11 | [Nabhan 2026 / SI](https://doi.org/10.1073/pnas.2606113123) | 19 | Preparation/donor/well methods | `71cc465ddf61a3c605868e8d57a8ef665537ee8b9d64ef9acfdb2469d6a423e9` |
| P12 | [Gillich 2020 / capillary types](https://doi.org/10.1038/s41586-020-2822-7) | 29 | Lineage models and endpoints | `dafea66cf104a083f0d9889d9eb9626630e07f1d40a1dfa8ce2edc7de93b7fbc` |
| P13 | [Jones 2024 / injury-induced niche](https://doi.org/10.1126/science.ado5561) | 18 | Lineage specificity and model context | `01ad1d4cc2dbcf8a4f0e2be1708a458e16208b22dabf1521658beec3eabfe937` |
| P14 | [Travaglini/Nabhan 2020 / human atlas](https://doi.org/10.1038/s41586-020-2922-4) | 37 | Sampling and identity context | `ff83ca9d9616d148be61d46c0f05d31036cefcbaa1d6754e16929198928ebe3e` |
| P15 | [Wagner 2021 / Compass](https://doi.org/10.1016/j.cell.2021.05.045) | 40 | Models, metabolic assays, material limits | `70e95112411cf478ac445ce3d5155ee2542d33d7e28c8e54c7bb9ac5cf4707d6` |
| P16 | [Yadav 2025 / ARG1 circuit](https://doi.org/10.1172/JCI188734) | 16 | Models, functional assays, units, contributions | `b9a6f15dc2b91408acff08789584f27e4a928c9d0bd3d49dabb1065a52759744` |
| P17 | [Cardoso 2026 / early fibrotic niches](https://doi.org/10.1038/s41586-026-10399-6) | 46 | Models, reciprocal circuit, relevant figures | `f16ff424af04cfebf617e4181ffb091b42186e3a45dac31949de8eb9f784fadf` |
| P18 | [Choi 2020 / SI](https://doi.org/10.1016/j.stem.2020.06.020) | 17 | Organoid tracing/endpoint legends | `a0733ab6a463301c773ca8291d87f5638bd6e96732b09a79a31aa492055222fb` |
| P19 | [Hassan 2024 / CEBPA](https://doi.org/10.1038/s41467-024-48632-3) | 17 | Models, multiome, development context | `bbb76b27ba6370a00c8f8bb8dd97692e7be29154b4be5aa3f66e8bfba17316eb` |
| P20 | [Choi 2020 / DATP](https://doi.org/10.1016/j.stem.2020.06.020) | 25 | Models, withdrawal and lineage methods | `9315efea08e958a91cb1994406a68f2f739d1567c94bd41e4b34a069241ffd3f` |
| P21 | [England 2025 / mutant AT2](https://doi.org/10.1016/j.stem.2025.01.011) | 26 | Clone/organoid methods and relevant figures | `3167e85eae83a34a4cee7815dda5936e6a90bf4b19178b0687b1f612fc7fed1b` |
| P22 | [England 2025 / SI figures](https://doi.org/10.1016/j.stem.2025.01.011) | 19 | Independent-experiment and organoid legends | `ec94d5c85dbc952802e0772ab372889703752e6d33eea9c7dbbfc8cd05964812` |
| P23 | [England 2025 / Methods S1](https://doi.org/10.1016/j.stem.2025.01.011) | 9 | Inventory/extraction; detailed model refit not performed | `230c1378ad80c7f1423ea00dbf034df43aecdf164857c31cd16d4063fca2cb26` |
| P24 | [Yu/Lee/Choi 2026 / IL-1 review](https://doi.org/10.1016/j.smim.2026.102050) | 16 | Review context; not original capability evidence | `9ce4b7ed9511e913d0ee4f047798eb768903b5ef04953599503420882e1f89c1` |
| P25 | [Niethamer 2025 / longitudinal lung profiles](https://doi.org/10.1016/j.stem.2024.12.002) | 27 | Published host tracing/assay context; no infection protocol | `6bbf516290c1b4469bd6c9eef4659bd3a1acb6f16c50798b70492381163d7181` |
| P26 | [Niethamer 2025 / SI](https://doi.org/10.1016/j.stem.2024.12.002) | 15 | Inventory/extraction; no new sample-map qualification | `d7101cfa9325448d63b91f3778bff1565c90b743d13e2db5a806e123aba317e5` |
| P27 | [Jin / CellChat protocol](https://doi.org/10.1038/s41596-024-01045-4) | 42 | Computational reference; no wet-access inference | `ce88bb8c302f6dd29c4cf8b8e0a134856a57e57e9e13899673f89c50ac11927b` |
| P28 | [Sikkema 2023 / SI 1](https://doi.org/10.1038/s41591-023-02327-2) | 12 | Inventory/extraction; no new donor qualification | `b03475db8e1cb96596ce17d27aa75d3cd7a540eb311c6def2fdb92d79a1bb275` |
| P29 | [Sikkema 2023 / SI 2](https://doi.org/10.1038/s41591-023-02327-2) | 5 | Inventory/extraction; no new donor qualification | `aa80eba04486f07b2cc068a9c6c7445781c0331a4c2779a2121b358d00110bba` |
| P30 | [Sikkema 2023 / HLCA](https://doi.org/10.1038/s41591-023-02327-2) | 47 | Atlas integration/sampling context | `4c2d9d7f30c6a4bc0600ab3f3deed4c26911ef32f916cc72744bbdaa38b87c2e` |
| P31 | [Wolf 2018 / Scanpy](https://doi.org/10.1186/s13059-017-1382-0) | 5 | Computational reference; no wet-access inference | `f75d6ab37e64b5960101376ce79805ea6e0c42cf1bbaf3c3b272cd29583ce49e` |
| P32 | [Wolf 2019 / PAGA](https://doi.org/10.1186/s13059-019-1663-x) | 9 | Computational reference; no lineage proof | `0990914b173e5c3032caa23d8a1b06d2494f58ceb360b5f6991c816da50441f5` |

## Web coverage and limits

Primary web methods were checked for Nabhan 2018, Choi 2020, Yadav 2025, Hassan 2024 and Cardoso 2026; DOI/publisher and primary indexes corroborated other cited paper identities. Source-specific PDF page locators in [METHODS.md](METHODS.md) support the detailed local reading. A publisher error is not treated as full-text access.

The cross-field reading queue has no corresponding local PDFs in this inventory: X1 [Wheeler 2023](https://doi.org/10.1126/science.abq4822), X2 [Dhillon-Richardson 2025](https://doi.org/10.1073/pnas.2423697122), X3 [Mu 2026](https://doi.org/10.1038/s43587-026-01175-2), and X4 [Ma 2025](https://doi.org/10.1126/science.adj3020). X2/X3 have targeted primary web-method coverage; X1/X4 remain limited to primary indexed findings/platform descriptions, with publisher/CAPTCHA restrictions on attempted detailed access. Their exact method suitability is not certified.

Non-PDF workbooks, ZIP archives and pre-existing reading notes were inventoried as context but are not newly executed scientific inputs in this review. Existing audited source tables retain their earlier qualification. Downloads do not mark the owner's reading gates completed; 3A/3B reading stays open and S1/D1 numerical gates remain intact.
