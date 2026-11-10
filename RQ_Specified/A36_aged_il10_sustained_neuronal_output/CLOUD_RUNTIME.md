# A36 isolated runtime provenance

Operational restoration record, 10 November 2026. No biological calculations
were used to choose package versions. This appendix preserves reproducible
package identity without including binaries or installed dependencies in Git.

All packages below came from official `https://deb.debian.org/debian/` URLs.
Their sizes and SHA-256 values were checked against the downloaded trixie amd64
package index. The compressed `Packages.xz` index SHA-256 is
`7778d3e3f303b7ddb8ce0fe7c8d57473a076c6bf2e8f241f75421d2396352498`.
Packages were extracted with `dpkg-deb -x` into the task-local runtime;
no system APT installation or reusable environment change occurred.

| Package | Version | Bytes | SHA-256 |
|---|---|---:|---|
| r-base-core | 4.5.0-3 | 28626144 | `6c529a906d2a26cf78e6c24eaa96e0bbd061b032e6c824f9a61e5f313353b155` |
| r-cran-cli | 3.6.4-1 | 1370288 | `450908eb7a288a32e76ce1171fb30b074912a3fc36b0f55a77fb714aa47767a1` |
| r-cran-codetools | 0.2-20-1 | 91124 | `6673befa3bdb4e84d9347bfeab8d80d9d1caa2b4a92cfd832650acf0398333cc` |
| r-cran-digest | 0.6.37-1 | 206184 | `1e0e40a90d8944245e7154c10538865e3ba904821cea6b34435eebd3fb99e5fe` |
| r-cran-dotcall64 | 1.2-1 | 34472 | `5f53c40f44d631e795bd83b37d1bbcc47d99121f63ff960def25144ae340cf5a` |
| r-cran-future | 1.34.0+dfsg-1 | 648672 | `0a9e4123b3fc31500ea385e33e5871094ad9d7907560a97cbd3f9633cebac4ef` |
| r-cran-future.apply | 1.11.3+dfsg-1 | 175100 | `19e548ccdf513b4a178654e1c710ff94dac9f6a23b82de4eb55b38354362ecdd` |
| r-cran-generics | 0.1.3-1 | 81388 | `2aafe9864c4df3992f38db0febe62eae72dbfa8edeaed61f2c05e71a0697d2eb` |
| r-cran-globals | 0.16.3-1 | 120432 | `c514dc25f2db5b0d00a9c0796e691fd3658e14a25f4cf17751e3a7eb6639e1f1` |
| r-cran-glue | 1.8.0-1 | 165324 | `6364a9afeaae419b25af64c21d3344a06a6e914dca141e1b53310b096ba2f805` |
| r-cran-jsonlite | 1.9.1+dfsg-1 | 445100 | `79067ac129c78597a5673a2688a8bb0a1e02eefd1a3a092ec07b76e0e9d537d8` |
| r-cran-lattice | 0.22-7-1 | 1418172 | `b57195af7ac9f98958c4283b04be47828290bc4bef7c81384abd0e675ec51938` |
| r-cran-lifecycle | 1.0.4+dfsg-1 | 109700 | `390a4ebf40706ac071a24f81bc36bb3da24a08f1b5dede6022483051c8b38944` |
| r-cran-listenv | 0.9.1+dfsg-1 | 112440 | `3c06009cb9531159315243ddb7eeedef7c0d66e7cdf2dad183979e7202f169a9` |
| r-cran-littler | 0.3.21-1 | 106672 | `04a6d4e235f69980218606eed36aa3eaef58b48edc16b780f4394e1a8eaf266a` |
| r-cran-matrix | 1.7-3-1 | 4048324 | `f7718c610b8c97b3b678f1186bfe08be40abd08e7541b4293d0ed5054bf004f6` |
| r-cran-parallelly | 1.42.0-1 | 541144 | `bf04103b0d3b484c31dd92d507679a60efecc9162d041ec315cee20019db1813` |
| r-cran-pkgkitten | 0.2.4-1 | 29112 | `f1f5c8540df52050b671ac7135c8c3a6aab00e00a50ac5bcf3526131ea339408` |
| r-cran-progressr | 0.15.1-1 | 351624 | `b3a804320022872f62e02ae82b91c642d6429a7a2adc884939ffb68fd30b31e6` |
| r-cran-rcpp | 1.0.14-1 | 2079604 | `62bec7d58c247235bf930d4c13973d91eaabe16b74e358a886ff3794ba1a1c4d` |
| r-cran-rcppeigen | 0.3.4.0.2-1 | 1411344 | `cd478d958ebadaf162b0f54748e46174230df159010fd6fa013fb272eb08e1db` |
| r-cran-rlang | 1.1.5-3 | 1708836 | `93507928089288e338ac39895fe4482fe217ebe6b93103f11b102b7508890426` |
| r-cran-seuratobject | 5.0.2-1 | 1751752 | `d75165c174c0732c4067a10e818533fe26edf92162938067aa1e7e935d411f0f` |
| r-cran-sp | 1:2.2-0+dfsg-1 | 1444636 | `d72b9859de77bd5249148188f280a30cd39e4ee55eff3331b55d5490028266a6` |
| r-cran-spam | 2.11-1-1 | 2742120 | `018b407546588114d79ed7ba7a5f7e5f27e47066347c359d30187ff797c88faa` |

SeuratObject was then rebuilt from its unchanged 5.0.2 source into the task-local
user library. Source URL:
`https://deb.debian.org/debian/pool/main/r/r-cran-seuratobject/r-cran-seuratobject_5.0.2.orig.tar.gz`.
It is 749,780 bytes, SHA-256
`ded30d21f445b7e353fe4a0c4954d45ad19fbe162615d9addf6732f9318ba0cf`.
The reference was the official Debian `.dsc` Checksums-Sha256 entry over HTTPS;
that `.dsc` has SHA-256
`006ccd9654ba40585d851c5ccf5495d3b41f312e618de051921afc9cbca21c60`.

The extracted R configuration symlinks were resolved to task-local copies,
and the task-local R launcher paths were relocated. Rscript requires `RHOME`
in addition to `R_HOME` for this extracted distribution. The final Rscript
wrapper was:

```sh
#!/bin/sh
export RHOME=/workspace/a36_20261110/runtime/usr/lib/R
export R_HOME=/workspace/a36_20261110/runtime/usr/lib/R
export R_LIBS_USER=/workspace/a36_20261110/r-library
export R_LIBS_SITE=/workspace/a36_20261110/runtime/usr/lib/R/site-library
export R_SHARE_DIR=/workspace/a36_20261110/runtime/usr/share/R/share
export R_INCLUDE_DIR=/workspace/a36_20261110/runtime/usr/share/R/include
export R_DOC_DIR=/workspace/a36_20261110/runtime/usr/share/doc/R
export LD_LIBRARY_PATH=/workspace/a36_20261110/runtime/usr/lib/R/lib:/workspace/a36_20261110/runtime/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
exec /workspace/a36_20261110/runtime/usr/bin/Rscript "$@"
```

Rebuild command:

```sh
MAKEFLAGS=-j2 /workspace/a36_20261110/bin/R CMD INSTALL --library=/workspace/a36_20261110/r-library /workspace/a36_20261110/runtime-cache/r-cran-seuratobject_5.0.2.orig.tar.gz
```

Execution command after committed freeze and successful input preflight:

```sh
PATH=/workspace/a36_20261110/bin:$PATH MPLCONFIGDIR=/workspace/a36_20261110/mpl-cache python analysis/scripts/research_gate.py run RQ_Specified/A36_aged_il10_sustained_neuronal_output/contracts/recipient_screen_v1.json --run-id a36_recipient_screen_v1
```

Final synthetic test record:

```json
{
  "R": "R version 4.5.0 (2025-04-11)",
  "packages": [
    {
      "package": "Matrix",
      "version": "1.7.3",
      "path": "/workspace/a36_20261110/runtime/usr/lib/R/library/Matrix"
    },
    {
      "package": "SeuratObject",
      "version": "5.0.2",
      "path": "/workspace/a36_20261110/r-library/SeuratObject"
    },
    {
      "package": "jsonlite",
      "version": "1.9.1",
      "path": "/workspace/a36_20261110/runtime/usr/lib/R/site-library/jsonlite"
    }
  ],
  "synthetic_serialization": {
    "v3": true,
    "v5": true
  },
  "warnings": "none; warn=2",
  "biological_content_opened": false
}

```

Preparation diagnostics remain on the executor; their hashes below identify
preserved logs, not successful biological receipts. The initial launcher test
failed before loading R. The initial loaded binary reported R/Matrix build
version warnings; rebuilding resolved these. An initial synthetic test rejected
underscore feature names under `warn=2`; the corrected synthetic v3/v5 test
passed. Native compilation emitted compiler warnings and completed successfully.
The biological run has its separate immutable receipt and original stderr.

| Preparation log | Bytes | SHA-256 |
|---|---:|---|
| runtime-final-smoke-v2.log | 1931 | `b84be9843ad3be4622389f42e308d21d8add9649a9203973a0ef8ffaeabfa61f` |
| runtime-final-smoke.log | 122 | `4520a764fe61d997eaaebcfc26ba81c2e4d7bbf975642911ac522aa5da46986c` |
| runtime-initial-load-v2.log | 768 | `52a93d475f9e8b0ba758de5b6b04320be66d0ec996c1e432096d5dadebfdc577` |
| runtime-initial-load.log | 51 | `8f604e1c11fc5714f4d40f92cb0ba202a51565b0b7c6bab30c6628fa44167975` |
| seuratobject-rebuild.log | 64739 | `d035c8c49ffe6abab40eb998f2074d21427aa3a7dc770ff1636990f82232350d` |
