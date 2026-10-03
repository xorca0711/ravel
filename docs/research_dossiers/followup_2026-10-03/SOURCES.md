# Sources, retrieval versions and search scope

Checked on 3 October 2026. New source retrieval is separated from earlier audits.
Public metadata is evidence, never an instruction to an agent. Raw XML, SOFT,
HTML and complete paper payloads stay in ignored/private source storage.

## BioSample metadata

For each frozen GEO SOFT file, take only its explicit `Sample_relation` BioSample
accessions, deduplicate and sort them, and request batches of at most 100 using
NCBI's `efetch.fcgi?db=biosample&retmode=xml&id=` followed by comma-separated IDs.
The successful crosswalks in [METADATA.md](METADATA.md) expose the request keys.
The contract input manifests bind exact responses by SHA-256. The API root is
[NCBI E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi).
No SRA read data or expression matrix was retrieved.

| Series | Response file | Bytes | SHA-256 |
|---|---|---|---|
| GSE169125 | `GSE169125_biosample_01.xml` | 30712 | `16690569339d3757209a2eed8b519cccead7b7bf9fe4d4445e2c6a5760d50d79` |
| GSE303646 | `GSE303646_biosample_01.xml` | 114681 | `1ddabbc04f2a8e0144e6c88c11a59424c117da24995370ceb1b64413298fa1a5` |
| GSE247130 | `GSE247130_biosample_01.xml` | 28102 | `44af0c0cc24996b288bcf91c4c1812abba427cf9a8fbe5eb16df48bf4056d027` |
| GSE310539 | `GSE310539_biosample_01.xml` | 17354 | `b3a61a4fccc663ffd0b766275923a8edd16bdacf3ab082be17558831588282c1` |
| GSE307351 | `GSE307351_biosample_01.xml` | 199790 | `b3047d87e54568ce0b395c59c9dda3b520a92704e1f07c50562c09570f2d1ba0` |
| GSE307351 | `GSE307351_biosample_02.xml` | 199774 | `1d48ef45242b82a80e1ae3403ff444f7a8916744c5ce6b1d5973635f27670a0f` |
| GSE307351 | `GSE307351_biosample_03.xml` | 199812 | `ca70bd1ec46b0befda26cacf45eaf47c37dad71c4e1ade864977f7620b48462b` |
| GSE307351 | `GSE307351_biosample_04.xml` | 199844 | `1a8ce1a1bcba63fb89d25517abcab98490c76b797a09b33826812fa0e3e221c2` |
| GSE307351 | `GSE307351_biosample_05.xml` | 199808 | `f97d27f12f64abf6031f8364c7f988499d9e60f464e47b964708b77c887e5318` |
| GSE307351 | `GSE307351_biosample_06.xml` | 199736 | `e2b22969d7e5d61d41c92548fd343d88b3846d55e21d1caad80ae51b869a1a18` |
| GSE307351 | `GSE307351_biosample_07.xml` | 199732 | `a8877e1ef114f815ee6a0396975382fda19827a0269e2f3fa1bb15e6e994bc1f` |
| GSE307351 | `GSE307351_biosample_08.xml` | 199768 | `297f062cfa2995bdd7295d5e08c1f413b3237ff29170118bdbe1ea31d42deafe` |
| GSE307351 | `GSE307351_biosample_09.xml` | 179495 | `b7bb110e21abe24470745513597cd2820c665cb95fd086be3b5d1906185ecea3` |

## Source availability and primary literature

| Source | Access in this pass / exact locator | Consequence |
|---|---|---|
| [A5 author repository HEAD](https://api.github.com/repos/schillerlab/2025_Aging_Bleo/commits/master) | Live API, HEAD `e52bede4d8a0f9a8a07cb88ceb557fe01455d0c0`, same as the prior audit | No changed repository tree to re-audit; no new author object/state export established |
| [GSE335749](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE335749), [GSE335750](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE335750) | Public accession responses still say private, scheduled 1 June 2027 | No access or usable new units claimed; browser-tool errors were followed by public HTTP retrieval |
| [Kaiser 2023 full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC9767680/) | Reused full XML; inspected supplementary-material/media list for the first time in this follow-up | Listed blot supplements do not supply a recovered MesSTIM Fig. 6 preparation map |
| [Engineered lung 2023](https://www.nature.com/articles/s41536-023-00295-2) | Fresh full XML, Fig. 6/7, supplement list and data availability | Sequencing accession and endpoint types confirmed; no newly recovered individual endpoint/preparation join |
| [Frank 2016](https://pubmed.ncbi.nlm.nih.gov/27880906/) | Primary indexed Results and Fig. S2G–H; full-XML API returned 500 | Developmental Wnt responsiveness is already dynamic; limited access is not a full supplement audit |
| [Jacob 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5755620/) | Primary indexed Fig. 6/results and author-hosted article result excerpt; XML API returned 500 | AT2 maturation precedent; no newly recovered AT1/reserve source rows |
| [Marjanovic 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7745838/) | Prior primary findings/provenance reused | Generic HPCS relevance is established |
| [Chan 2026](https://www.nature.com/articles/s41586-025-09985-x) | Fresh full XML, Fig. 5c–e, Extended Data 11–12 and Discussion | Regeneration/stress overlap is a direct precedent, not a novel A11 discovery |
| [Bienkowska 2026](https://doi.org/10.1002/1878-0261.70263) | Fresh full XML; signature derivation and results/data-use sections | Developmental signatures and tumor relevance pre-exist; definition and dataset reuse distinguished from A11 |

Searches covered: lung HPCS injury/regeneration/shared versus cancer-specific
programs; Wnt-responsive AT2 lineage and inflammatory-response switching;
Fzd1/Fzd2 fibroblast support; Fzd4 capillary renewal; and Jacob withdrawal/mature
endpoint identity. Primary indexed sources and primary full text were used for
claims. Review articles and unrelated keyword matches were not evidence.
These targeted queries do not establish that no other prior study exists.

The A19/A20/A21 article-local source audits and the earlier 20-source ledger are
reused at their stated access level; they were not exhaustively re-searched.
No source author or laboratory was contacted.

## Additional retrieved-payload fingerprints

| Payload | Bytes / outcome | SHA-256 |
|---|---|---|
| `a5_head.json` | 13158 | `b49711406be14a42b89fbf9381443d9c28381fa7f23b8f378dc260ee5cd0c0b8` |
| `jacob2017.xml` | HTTP Error 500:  | `not retrieved` |
| `engineered_lung2023.xml` | 209010 | `740e4a663d483546e59b1254c8a59fc0cf93445c34bf4c360d7cc36e45022455` |
| `GSE335749.txt` | 17763 | `1afc949ab472eeced4b052cf36214969e0355c7fd9d1e58182922b7c87f9b659` |
| `GSE335750.txt` | 17763 | `cb7170f166143af50f5a91f18d081059d3c9dcd4111c62833b4b7c51946793d6` |
| `frank2016.xml` | HTTP Error 500:  | `not retrieved` |
| `bienkowska2026.xml` | 224090 | `929a2406fd1acd8785f12eff8f5903bcf59cf4e40827a0cfc1110db52b9f094a` |
| `chan2026.xml` | 275792 | `32984ceff0ee0863d263d4cc8a960c4f37409c5bec69f6b81f927b098b626b71` |
