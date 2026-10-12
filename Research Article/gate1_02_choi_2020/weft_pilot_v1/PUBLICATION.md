# Complete-output publication and restoration

**12 October 2026: public publication and independent recovery verified.**
The owner approved this exact output-only package and its CI restoration route.
PR #149 proposes registration of the unchanged original receipt and a narrow
restoration step. Engineering integration and human scientific review remain
separate; no analysis reran, claim grade changed or new RQ was admitted.

The [public prerelease](https://github.com/xorca0711/ravel/releases/tag/choi-p001-figure1-v1)
is pinned to reviewed source `714945697b007f4a0046834b34251392c1cfbe5a`.
Its single asset, `choi-p001-figure1-v1-complete-outputs.zip`, is **105,582,086 bytes**,
SHA-256 `6e10afc432fdffb32ece7a3692c8dbb302c74604e9e67e27793c8d1856de21e2`.
Release ID is `410591160`; asset ID is `633765798`. The executed scientific source
remains `b656d06cc9f2cfdd61a6dd1f6570ec01331abf91`.

All 15 original outputs, the original receipt and a member manifest are included:
17 ZIP members. The saved matrix is 385,675,968 bytes. Original output hashes
remain in the [scientific review](SCIENTIFIC_REVIEW.md#exact-audit-anchors).
No member was recomputed, relabelled, omitted or edited. The original receipt
SHA-256 remains `24aaaaef907519391ba3c8650f96795ebe2dff4a27cd4ad9e9977852cdc5974b`.

This package excludes private recovery databases, checkpoints, Drive locators,
cloud session records, logs and source downloads. Text, HDF5 string/attribute
and PNG metadata inspection found no credential, email, private path or private
service-link pattern matches. This bounded review is not a universal privacy
proof. The five-figure visual review was reused.

## Restore without rerunning the analysis

From a checkout containing this PR, with Python 3.12+:

```bash
python analysis/scripts/restore_published_outputs.py
python analysis/scripts/research_gate.py verify analysis/research/runs/p001_figure1_v1_f001_d56ee41e13cd4327/receipt.json
python analysis/scripts/research_gate.py check
```

The [checked-in asset lock](../../../analysis/research/published_outputs/choi_figure1_v1.json)
binds release identity, archive size/hash, embedded manifest and every member.
The restoration script downloads only a locked Ravel release asset, restricts
redirect hosts, bounds bytes, checks all ZIP members before writes, rejects
unsafe/duplicate/non-regular paths, and refuses conflicting local files. It
does not execute downloaded code. Existing matching files are left intact.
The full run directory remains ignored; the original receipt alone is tracked.

Both repository CI workflows restore these published bytes before existing
checks. The scientific validator is unchanged and still requires every output
to match the frozen receipt. Missing or changed remote evidence fails CI; it
does not authorize a partial receipt, fallback recomputation or softened check.
For offline verification of a previously downloaded asset, pass
`--archive /path/to/choi-p001-figure1-v1-complete-outputs.zip` to the restoration
command. Use a new versioned release for corrections; do not replace this asset.

## Verification and remaining decisions

GitHub's uploaded digest matched the approved package; a draft download matched
independently before publication. After publication, an unauthenticated download
through the restoration script verified the archive and every member and created
all 15 missing outputs beside the byte-identical tracked receipt. The local
unchanged receipt validator also passed. Clean-checkout CI and the current-main
research gate are required for PR integration; check PR #149's latest runs.

The [scientific review](SCIENTIFIC_REVIEW.md) remains descriptive: one pooled
library per condition, no recovered pAT2 label, condition-dependent exclusions
and resolution/subcluster limitations. Publication does not resolve those limits
or record human scientific acceptance. The private coordinator retains its held
reservation and last verified checkpoint; reconcile it before another job. Weft
B4 remains on hold and is not part of this publication.
