# S3 supported reader and original-track acquisition

18 November 2026. Preparation authorized by the coordinator after reviewed S4B.
This records environment and file-transfer evidence, not a biological ATAC result.
All installation/cache/source files are ignored under this worktree's `raw_data/`.
The independent learning environment and global packages were preserved.

## Actual runtime and compatibility

The default WSL inspection found Linux aarch64, glibc 2.43, Python 3.14.4, no
pip/ensurepip, no GCC/G++/make/pkg-config and no BigWig reader. Only Python 3.14
was found in the inspected standard executable directories. The available NGS
target registry listed only local; its SSH inspector did not inspect local.
These observations describe checked routes, not a claim about every possible
runtime or source feasibility.

Official [pybbi 0.4.2 files](https://pypi.org/project/pybbi/0.4.2/) include an
aarch64 CPython 3.13 wheel. The checked pyBigWig 0.3.30 release had no matching
aarch64/CPython 3.14 wheel. A supported local Python 3.13 environment therefore
avoids a source build. [uv's documented managed Python route](https://docs.astral.sh/uv/guides/install-python/)
uses Python-build-standalone distributions; this is not an official CPython binary.

| Component | Exact selection | Saved distribution SHA-256 |
|---|---|---|
| uv | 0.13.9, `py3-none-manylinux_2_28_aarch64` wheel | `ecb6028d79dc96fbeafffe5c8af62a7099487ebc05a701e76714eebcffd06375` |
| Python | 3.13.18, `cpython-3.13.18-linux-aarch64-gnu`, resolved by pinned uv | Install log retained; no independently saved archive checksum is asserted |
| pybbi | 0.4.2, `cp313-cp313-manylinux_2_17_aarch64.manylinux2014_aarch64` | `20ee599e318238b177b2c31dbe7789034ea0bfa9716e0aa06d387d7cc9f78938` |
| NumPy | 2.5.5, `cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64` | `ae2b8285d0b4eed24739c3ca9ec0fa424a0247489c01e1d5fe2815a599e11d33` |

PyPI JSON snapshots, exact wheel URLs/hashes and `requirements.lock` are retained
in `raw_data/naik2017_s3_runtime_v1/`. Wheel bytes matched the published hashes.
The extracted uv binary's SHA-256 is
`6109e47a75f2380d1cc90b00a6ee82b7b5792ddf66588625ec168545ae17512e`.
Its Python installation, executable directory and cache were all directed inside
that same directory; `--no-bin --no-registry` avoided global executable registration.
Package installation used `--no-index --require-hashes --no-build` with only the
two saved wheels, an explicit virtual-environment interpreter and copy link mode.

In WSL, from this worktree, the central reconstruction commands are:

```bash
task_runtime="$PWD/raw_data/naik2017_s3_runtime_v1"
export UV_PYTHON_INSTALL_DIR="$task_runtime/python"
export UV_PYTHON_BIN_DIR="$task_runtime/bin"
export UV_CACHE_DIR="$task_runtime/cache"
"$task_runtime/uv" python install 3.13.18 --no-bin --no-registry --no-config
"$task_runtime/uv" venv --python 3.13.18 --managed-python --no-python-downloads --no-config "$task_runtime/venv"
"$task_runtime/uv" pip install --python "$task_runtime/venv/bin/python" --no-index --find-links "$task_runtime/wheels" --require-hashes --no-build --link-mode copy --no-config -r "$task_runtime/requirements.lock"
```

These commands document a fresh setup. The existing environment already passed
installation/import checks; it should not be recreated over an existing path.

## Reader check and API semantics

The toy file and expected values were read from the public pyBigWig test source
at commit `91362c55d40da9dcf007d5e0cdb4fd6118234151`:
[fixture](https://github.com/deeptools/pyBigWig/blob/91362c55d40da9dcf007d5e0cdb4fd6118234151/pyBigWigTest/test.bw)
and [test expectations](https://github.com/deeptools/pyBigWig/blob/91362c55d40da9dcf007d5e0cdb4fd6118234151/pyBigWigTest/test.py).
The 12,966-byte file SHA-256 is
`cfbf15ba7e9559db9841b246a12a79b51c44b2215137b652dc8f35b100b7ae86`.
The supported reader recognized BigWig, matched its two exact chromosome lengths,
and returned the expected first three float32 values, approximately 0.1/0.2/0.3.
No external test code was executed. The saved `runtime_smoke.json` records the
actual Python/package versions and check time; no research track was read by it.

The installed reader API defaults to zero for unreported bases and approximate
zoom summaries when bins are requested. S3Q explicitly requests missing values as
`NaN`; any later binned numerical method must explicitly choose exact summaries
and define its missingness/denominator. A successful toy check does not certify
the full research files or their biological signal scale.

## Source transfer and ordinary preparation failures

All eight original GSM2441001–1008 files were acquired, totaling 6,679,503,736
bytes. Their exact declared GEO URLs came from the saved SOFT and S1M map.
`raw_data/naik2017_s3_sources/acquisition_manifest_v1.json` records each URL,
date/time, expected and actual size, Last-Modified/response identity, local
SHA-256 and acquisition-script hash. Two simultaneous curl downloads completed
without a track-transfer failure or resumed partial. Raw reads and D180 were not
downloaded. A local checksum verifies preserved bytes, not an author signature.

The [UCSC mm10 chromosome dictionary](https://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/mm10.chrom.sizes)
has 66 records and 1,405 bytes in the saved snapshot; SHA-256 is
`55463d59f400b2c8260d100f4b521800ee773fa9711fe3f6dad9c7887db2574f`.
Its acquisition record is retained with the source files.

Three ordinary preparation issues were resolved without weakening checks:
the uv wheel selector found two compatible aarch64 distributions and was narrowed
to the explicit glibc 2.28 wheel; Python urllib failed certificate verification
on the separate UCSC request, while normal Windows curl/Schannel verified and
retrieved that HTTPS resource; an acquisition-specification name collision stopped
before transfer and a separate transfer specification preserved the earlier HEAD
record. No TLS verification, safeguard or global environment setting was disabled.
These are distinct from the preserved earlier content restriction.

S3Q's separate frozen contract governs the first research-track header/readability
inspection. Source acquisition and a working reader alone do not establish
normalization, an original coordinate universe or an accessibility result.
