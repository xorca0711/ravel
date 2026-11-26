# First runner attempts

All six attempts stopped during Python parsing before loading observations. The replacement v2 contracts preserve the v1 contracts and link their predecessors. The runner emitted the following receipts and stderr.

## song24_c2_S0_v1

**receipt.json**

```text
{
  "schema_version": 1,
  "analysis_id": "Song24-C2.S0.v1",
  "owner": "Song24-C2",
  "contract": "Research Article/gate3_2R_C2_song_2024/contracts/S0.v1.json",
  "contract_sha256": "3e0c50c453d41d76366e717c4789faf793c0e039041936b8082cbd95729a3101",
  "git_commit": "f15e71dca75c6fe4444b518aaf4e2ed37bffbe05",
  "started_at": "2026-11-26T03:58:06.711353+00:00",
  "argv": [
    "python",
    "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
    "S0",
    "analysis/research/runs/song24_c2_S0_v1"
  ],
  "argv_format": "repository_relative",
  "environment": {
    "python": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
    "platform": "Linux-6.18.57-x86_64-with-glibc2.41"
  },
  "inputs": [
    {
      "path": "raw_data/song_v1/geo",
      "sha256": "a848a9339f79e8aedfd67cd14b1a23df8dd9ce4564b8f2b4c2d496398be71f83",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/soft",
      "sha256": "921bb250f55db612e8548ec0a0231fbb4e7c099b47a3f2beccbf7cdf14c11b67",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/article",
      "sha256": "d355b21fd126213be87627dc9505493677e272537ac7453484e444401e9e833b",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    }
  ],
  "code": [
    {
      "path": "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
      "sha256": "5971601f7216c32daf20d4164e2380890740c42d1095748b26488dd24c0de7d8"
    }
  ],
  "status": "execution_failed",
  "outputs": [],
  "scientific_acceptance": "not_assessed",
  "verification": "pending",
  "exit_code": 1,
  "error": "Missing file: libraries.csv",
  "finished_at": "2026-11-26T03:58:06.726584+00:00"
}
```

**stderr.log**

```text
  File "/workspace/ravel-song/Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py", line 192
    markers[name] = {"n": len(selected), **{contrast: st.median(r[contrast] for r in selected)
                    ^
SyntaxError: '{' was never closed
```


## song24_c2_S1_v1

**receipt.json**

```text
{
  "schema_version": 1,
  "analysis_id": "Song24-C2.S1.v1",
  "owner": "Song24-C2",
  "contract": "Research Article/gate3_2R_C2_song_2024/contracts/S1.v1.json",
  "contract_sha256": "6df51d7e1cfa15f38417d853af11337699991f1d319ac1d119216a733f5f2138",
  "git_commit": "f15e71dca75c6fe4444b518aaf4e2ed37bffbe05",
  "started_at": "2026-11-26T03:58:06.776032+00:00",
  "argv": [
    "python",
    "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
    "S1",
    "analysis/research/runs/song24_c2_S1_v1"
  ],
  "argv_format": "repository_relative",
  "environment": {
    "python": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
    "platform": "Linux-6.18.57-x86_64-with-glibc2.41"
  },
  "inputs": [
    {
      "path": "raw_data/song_v1/m3.xlsx",
      "sha256": "d07b86a91fbbc4564f3b9bb468f21a18c1ead881a7672da41ffd82a83d906964",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m4.xlsx",
      "sha256": "445f7d2892c8f89f11cf3377adc5a32faa14cc0a1013ec39d187ab07dae52af3",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m7.xlsx",
      "sha256": "85ea8177dd24db212780664c591f72bd62aff0baa030b0aeabdfd8716519697a",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m10.xlsx",
      "sha256": "a637fe0a4c974a94c5f22fd6ddb78e09cf58b2835a87cf36e5d34f6687c6d50f",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/article",
      "sha256": "d355b21fd126213be87627dc9505493677e272537ac7453484e444401e9e833b",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    }
  ],
  "code": [
    {
      "path": "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
      "sha256": "5971601f7216c32daf20d4164e2380890740c42d1095748b26488dd24c0de7d8"
    }
  ],
  "status": "execution_failed",
  "outputs": [],
  "scientific_acceptance": "not_assessed",
  "verification": "pending",
  "exit_code": 1,
  "error": "Missing file: observations.csv",
  "finished_at": "2026-11-26T03:58:06.794466+00:00"
}
```

**stderr.log**

```text
  File "/workspace/ravel-song/Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py", line 192
    markers[name] = {"n": len(selected), **{contrast: st.median(r[contrast] for r in selected)
                    ^
SyntaxError: '{' was never closed
```


## song24_c2_S2_v1

**receipt.json**

```text
{
  "schema_version": 1,
  "analysis_id": "Song24-C2.S2.v1",
  "owner": "Song24-C2",
  "contract": "Research Article/gate3_2R_C2_song_2024/contracts/S2.v1.json",
  "contract_sha256": "624bc63f15b42b04f7c264191b175cce04267e6cfd718c3c30cb07a90b4dfbb1",
  "git_commit": "f15e71dca75c6fe4444b518aaf4e2ed37bffbe05",
  "started_at": "2026-11-26T03:58:06.851864+00:00",
  "argv": [
    "python",
    "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
    "S2",
    "analysis/research/runs/song24_c2_S2_v1"
  ],
  "argv_format": "repository_relative",
  "environment": {
    "python": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
    "platform": "Linux-6.18.57-x86_64-with-glibc2.41"
  },
  "inputs": [
    {
      "path": "raw_data/song_v1/m11.xlsx",
      "sha256": "f64405dd9dc74ec0235e2ee02deb336c4ef61d4646a54294134588878324c9b5",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m12.xlsx",
      "sha256": "02dc52715e54f4f52854c775cc430edf92cc7e4a8302557b519d15a30ca04c7d",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m13.xlsx",
      "sha256": "4cebe51a017d841de7c6e3ca180b641ac2aa6a0dbc88094540cc90eed21e9e4d",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/article",
      "sha256": "d355b21fd126213be87627dc9505493677e272537ac7453484e444401e9e833b",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    }
  ],
  "code": [
    {
      "path": "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
      "sha256": "5971601f7216c32daf20d4164e2380890740c42d1095748b26488dd24c0de7d8"
    }
  ],
  "status": "execution_failed",
  "outputs": [],
  "scientific_acceptance": "not_assessed",
  "verification": "pending",
  "exit_code": 1,
  "error": "Missing file: observations.csv",
  "finished_at": "2026-11-26T03:58:06.866924+00:00"
}
```

**stderr.log**

```text
  File "/workspace/ravel-song/Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py", line 192
    markers[name] = {"n": len(selected), **{contrast: st.median(r[contrast] for r in selected)
                    ^
SyntaxError: '{' was never closed
```


## song24_c2_S3_v1

**receipt.json**

```text
{
  "schema_version": 1,
  "analysis_id": "Song24-C2.S3.v1",
  "owner": "Song24-C2",
  "contract": "Research Article/gate3_2R_C2_song_2024/contracts/S3.v1.json",
  "contract_sha256": "1c418ed2050008d5c306f4aa6f80a7dac461dd7cb1d09325451d72555e79b11f",
  "git_commit": "f15e71dca75c6fe4444b518aaf4e2ed37bffbe05",
  "started_at": "2026-11-26T03:58:06.940803+00:00",
  "argv": [
    "python",
    "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
    "S3",
    "analysis/research/runs/song24_c2_S3_v1"
  ],
  "argv_format": "repository_relative",
  "environment": {
    "python": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
    "platform": "Linux-6.18.57-x86_64-with-glibc2.41"
  },
  "inputs": [
    {
      "path": "raw_data/song_v1/geo",
      "sha256": "a848a9339f79e8aedfd67cd14b1a23df8dd9ce4564b8f2b4c2d496398be71f83",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/soft",
      "sha256": "921bb250f55db612e8548ec0a0231fbb4e7c099b47a3f2beccbf7cdf14c11b67",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m2.xlsx",
      "sha256": "dde372104a4be2be84f80cc45cd4d242fa62b6e21f7fd23b46817b34a63a43c6",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/article",
      "sha256": "d355b21fd126213be87627dc9505493677e272537ac7453484e444401e9e833b",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    }
  ],
  "code": [
    {
      "path": "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
      "sha256": "5971601f7216c32daf20d4164e2380890740c42d1095748b26488dd24c0de7d8"
    }
  ],
  "status": "execution_failed",
  "outputs": [],
  "scientific_acceptance": "not_assessed",
  "verification": "pending",
  "exit_code": 1,
  "error": "Missing file: libraries.csv",
  "finished_at": "2026-11-26T03:58:06.957163+00:00"
}
```

**stderr.log**

```text
  File "/workspace/ravel-song/Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py", line 192
    markers[name] = {"n": len(selected), **{contrast: st.median(r[contrast] for r in selected)
                    ^
SyntaxError: '{' was never closed
```


## song24_c2_S4_v1

**receipt.json**

```text
{
  "schema_version": 1,
  "analysis_id": "Song24-C2.S4.v1",
  "owner": "Song24-C2",
  "contract": "Research Article/gate3_2R_C2_song_2024/contracts/S4.v1.json",
  "contract_sha256": "fa2ab33a1470e547b687982bb6e275f36c1418df368c09cdf33bb47e82056c90",
  "git_commit": "f15e71dca75c6fe4444b518aaf4e2ed37bffbe05",
  "started_at": "2026-11-26T03:58:07.007619+00:00",
  "argv": [
    "python",
    "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
    "S4",
    "analysis/research/runs/song24_c2_S4_v1"
  ],
  "argv_format": "repository_relative",
  "environment": {
    "python": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
    "platform": "Linux-6.18.57-x86_64-with-glibc2.41"
  },
  "inputs": [
    {
      "path": "raw_data/song_v1/m3.xlsx",
      "sha256": "d07b86a91fbbc4564f3b9bb468f21a18c1ead881a7672da41ffd82a83d906964",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m5.xlsx",
      "sha256": "111fb69f2c14a641a4e886e0aa0ae08a46782263d34068c224d2c1158c3747b6",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m12.xlsx",
      "sha256": "02dc52715e54f4f52854c775cc430edf92cc7e4a8302557b519d15a30ca04c7d",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m16.xlsx",
      "sha256": "58713135223e3884df60ab1ac4d8c1aa325674085f2d8c5bb47e008abf4ff981",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/article",
      "sha256": "d355b21fd126213be87627dc9505493677e272537ac7453484e444401e9e833b",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    }
  ],
  "code": [
    {
      "path": "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
      "sha256": "5971601f7216c32daf20d4164e2380890740c42d1095748b26488dd24c0de7d8"
    }
  ],
  "status": "execution_failed",
  "outputs": [],
  "scientific_acceptance": "not_assessed",
  "verification": "pending",
  "exit_code": 1,
  "error": "Missing file: observations.csv",
  "finished_at": "2026-11-26T03:58:07.022625+00:00"
}
```

**stderr.log**

```text
  File "/workspace/ravel-song/Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py", line 192
    markers[name] = {"n": len(selected), **{contrast: st.median(r[contrast] for r in selected)
                    ^
SyntaxError: '{' was never closed
```


## song24_c2_S5_v1

**receipt.json**

```text
{
  "schema_version": 1,
  "analysis_id": "Song24-C2.S5.v1",
  "owner": "Song24-C2",
  "contract": "Research Article/gate3_2R_C2_song_2024/contracts/S5.v1.json",
  "contract_sha256": "25ebd6148fa09c09a99c4b58742685c0ca4505403c4ca4a7d576b1b9982f425e",
  "git_commit": "f15e71dca75c6fe4444b518aaf4e2ed37bffbe05",
  "started_at": "2026-11-26T03:58:07.070986+00:00",
  "argv": [
    "python",
    "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
    "S5",
    "analysis/research/runs/song24_c2_S5_v1"
  ],
  "argv_format": "repository_relative",
  "environment": {
    "python": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
    "platform": "Linux-6.18.57-x86_64-with-glibc2.41"
  },
  "inputs": [
    {
      "path": "raw_data/song_v1/m5.xlsx",
      "sha256": "111fb69f2c14a641a4e886e0aa0ae08a46782263d34068c224d2c1158c3747b6",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m6.xlsx",
      "sha256": "771989ae8c7881ea54f97077dcad5a299d9fb8f1a492cddd4fadd94260577290",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/m15.xlsx",
      "sha256": "854fd15a5fc94be1f974fa96ba8f843cd30c93a5e155c0a32379755853b7b4fe",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    },
    {
      "path": "raw_data/song_v1/article",
      "sha256": "d355b21fd126213be87627dc9505493677e272537ac7453484e444401e9e833b",
      "study_id": "Song2024",
      "unit_ids": [],
      "role": "context",
      "independence": "unknown",
      "exposure": "exposed"
    }
  ],
  "code": [
    {
      "path": "Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py",
      "sha256": "5971601f7216c32daf20d4164e2380890740c42d1095748b26488dd24c0de7d8"
    }
  ],
  "status": "execution_failed",
  "outputs": [],
  "scientific_acceptance": "not_assessed",
  "verification": "pending",
  "exit_code": 1,
  "error": "Missing file: observations.csv",
  "finished_at": "2026-11-26T03:58:07.085204+00:00"
}
```

**stderr.log**

```text
  File "/workspace/ravel-song/Research Article/gate3_2R_C2_song_2024/scripts/analyze_v1.py", line 192
    markers[name] = {"n": len(selected), **{contrast: st.median(r[contrast] for r in selected)
                    ^
SyntaxError: '{' was never closed
```
