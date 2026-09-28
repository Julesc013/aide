# AIDE Lite 1.0.0 local release candidate qualification

This is a frozen **local candidate**, not a published release or parent-campaign
completion. Effect manifest: `release-effect-manifest-1.0.0.json`. Its four
asset and eleven job-receipt hashes were mechanically rechecked against local
bytes with zero mismatches. The candidate asset commit is
`92da95735736f36668f54d2851c9b85242f08a24`, tree
`747678324cb2e912860fe4cfd5e750c374962fc8`. The portable pack declares
source `fe44070dfb37ea44dbb61a253d6edbb713717442`; the accepted builder
code is descended from independently reviewed `59db02a0`. All work used the
shared owner-selected D: runner roots; each listed job exited zero, retired
scratch and released its reservation.

## Asset and replay checks

- A fresh read-only remote check found no prior AIDE Lite stable tag or GitHub
  Release. The policy's conditional first version is `1.0.0` and tag
  `aide-lite-v1.0.0`; recheck immediately before effect.
- The distinct stable ZIP SHA-256 is
  `df91a4845dc7e97b5af0125db4e22242b352a80906450de967f581f131a68f19`;
  tar SHA-256 is
  `1267223c80788768b5910339f1610c64f1ea1adb0fb9579461af8fefa76ef4d4`.
  The versioned manifest and SHA256SUMS hashes are in the effect manifest.
- Stable build `efce0c74375e402382adb71300751205`, validator
  `caaf0248cf78422486594f7c7d56b0e5` and committed-byte replay
  `1a14d2d21eea427893dfb90e45d06bd6` passed. Replay changed zero stable
  asset bytes or tracked files. Q47/Q48 no-publish projections passed their
  validators and post-commit bundle/draft replay changed zero release files.
- Export-pack replay itself advanced only the generated manifest's HEAD line;
  the committed pack retains a valid ancestor source and `pack-status` reports
  valid checksums, provenance and boundary. No zero-change claim is made for
  that standalone Q21 command across a new commit.

## Exact delivered-byte consumers

| D job | Result bound to the stable ZIP/tar |
| --- | --- |
| `fe8303a16e1741b9b54c90f37eea4dc6` | ZIP/tar extraction and checksum match, fresh/brownfield customization and update, 25 commands, project-owned bytes preserved; fresh and update partial recovery returned `RECOVERED`. |
| `5484a0215cfe46a880d9e8206cde0cfd` | 31 lifecycle commands, including repair, rollback, detach/removal and retained partial-removal cases. Synthetic successor is not published. |
| `308e4a0b09c547e794ec8d05551c98eb` | Fresh and brownfield installed context/evidence and Python-socket-guarded offline commands passed. `verify` remained WARN with 15/18 classified warnings. |
| `307e9acb58a849c39150e2b83219dd15` and `744447e3d26e45299af56a4810e387ab` | Current importer regressions: 54/54 and 56/56 passed, no skips, in 2583.948 and 3225.936 seconds. |
| `394e250216d84061936776637a486b0a` | Three real child exits at import receipt, repair file and removal receipt boundaries; exact recovery reached `RECOVERED`, `RECOVERED`, `DETACHED_RECOVERED`. |
| `df9a9ac40bcb4928beb857837a8d9250` | Ten installed CLI forms: fresh, predecessor and project-resolved partial recovery; changed resolution refused; explicit local feedback, no automatic sharing. |
| `85ec7ee5ebc04c6aac71da3ecb894847` | Installed `validate`, task status/inspect, explicit explanation/feedback and no-mutation inspection passed. `validate` exited zero with two recorded fresh-fixture warnings. |

The effect manifest pins supported project customization schemas v1/v2 and
the single strict disabled-feature ID `local_state_examples`. It declares T3
Limited Support for the qualified local Windows Lite companion profile. There
is no prior published Lite release, so the predecessor matrix is empty;
synthetic V2/V3 fixtures demonstrate update mechanics without becoming a
published compatibility claim. Native/hosted, model-enabled and non-Windows
apply profiles are excluded from this first release candidate, while remaining
in the wider active campaign.

## Limits and next gate

Installed `validate` warnings and `verify` WARN categories remain visible in
retained output. The offline guard observes Python socket attempts in the
installed CLI process, not native child traffic or OS network isolation. The
runner's quiescent cleanup proof does not assert a hostile-writer race or
crash-atomic filesystem quota. Archive validation inspects then reopens the
same local asset; one writer and unchanged hashes are required during final
qualification. This local matrix is not downloaded-asset evidence.

Independent technical **ACCEPT** for the exact effect manifest, assets,
profile and promotion/publication recovery path is required before main,
tagging or upload. Then verify remote identities, download all four assets,
check hashes and run fresh/brownfield acquisition and update from those bytes.
The parent goal remains active for wider mandatory programme work.
