# AIDE Lite 1.0.0 revised local release candidate qualification

This remains a **local candidate**. It is not a published release or completion
of the parent campaign. Independent review of the prior exact effect
`d5df63c5` returned REQUEST_CHANGES; see
`release-effect-d5df63c5-review.md`. The revised exact effect manifest binds
the corrected version policy, assets, ten current D job receipts and each of
the 28 declared CLI forms to a tested target state, environment and one or
more retained command logs. It records 39 per-form log references.

## Source, assets and replay

- Policy repair source: `545d4cc2089ed88a8fb44c17f85fdd3837ab2749`,
  tree `cd49e7a46766929babff9b08740e0cf185112b51`. The current pack
  validates with `PASS_SOURCE_ANCESTOR`; it embeds this source.
- Asset commit: `bed505ab15b2eb9e3eeaddc0303b23e45b87ea16`,
  tree `bb1fada1d6921c08ba98400326ee9532edc68288`.
- ZIP SHA-256:
  `0d3ce38d1ab946d40590c8ead55c1ed1805ab12681258e84b792817ee6aec09d`.
  Tar SHA-256:
  `95a954931997189c9310ceb10673bd8b6e038ed0aa4b4979a287badd905c15bb`.
  Separate manifest and SHA256SUMS hashes are in the effect manifest.
- Managed stable build `e9d2e14a70464a47bad30f6bc5ecb42f`, committed-byte
  replay `d1c83c492c0f4c5f8e8927407df0d880`, and validator
  `ce4fce1f9c5a449ca091c220910785a6` passed. Replay changed zero
  tracked files and zero asset bytes.
- Current-policy Q47/Q48 test job `43c291ddabf7481d80896dcf4660da1e`:
  36 tests passed in 62.146 seconds.

## New-byte delivered consumers

| Managed D job | Exact result |
| --- | --- |
| `be3d7ef03f2846e5b507ec1d89fb132c` | ZIP/tar fresh and brownfield install, customization, direct edit, disabled feature and conflict resolution passed. Added a plain resolved preview to cover a previously missing exact form. |
| `ee3f1860a8554597bcd57ad6061ae788` | Owned repair, rollback, detach/removal and interrupted recovery cases passed. |
| `4f8be0b031d74978b48361cbb075cf63` | Installed fresh and brownfield context, pack, verify and Python-socket-guarded offline flow passed. Verify retains WARN with 15/18 classified optional/context warnings. |
| `0ec74aea646542aaa206ffff1bd8889d` | Exact public partial recovery forms for fresh, synthetic predecessor and project-resolved update passed, with changed inputs refused and feedback local-only. |
| `1991347b40154c28a3f70369bc1c11f1` | Installed validate, task inspection and explicit feedback passed; exact fresh `--mode safe --dry-run --explain --feedback-out` log retained. Validate exited zero with two classified fresh-fixture warnings. |
| `500f403792f64b9fa4e51866d7993785` | Real child exits at import, repair and removal boundaries recovered successfully. |

Every listed job exited zero, retired scratch and released its shared D-root
reservation. The effect manifest pins each receipt hash and the 28 forms'
retained log hashes. A bare `task inspect` on an empty queue returns the
expected classified missing result with exit 1; populated inspection with an
explicit task ID also passed, but that option is outside this frozen public
form list. The first release has no published predecessor; update and rollback
fixtures use synthetic packs and do not establish a published compatibility
promise.

The prior 54/54 and 56/56 importer jobs remain recorded as **source regression
history**. Their importer implementation and test oracles are unchanged, but
six repository metadata/policy inputs changed, so those jobs are not used as
exact new-archive qualification. The new-byte canaries and current-policy
Q47/Q48 run supply the changed-scope evidence.

## Boundaries and next effect

The policy now distinguishes exact independent prepublication ACCEPT from
postpublication downloaded-byte checks. Q47/Q48 preview outputs remain
preview-only and no-publish. The offline guard observes Python socket attempts
in the installed CLI, not OS-native isolation. This candidate does not promise
native isolated-host, hosted, model-enabled autonomous or non-Windows lifecycle
apply behavior. Warnings remain visible in retained outputs.

Main promotion, tag and upload require a superseding independent technical
**ACCEPT** for the exact revised effect and current policy. Publication remains
incomplete until remote identities, downloaded hashes and fresh/brownfield
acquisition/update from downloaded bytes are verified. The wider campaign
remains active after a bounded Lite release.
