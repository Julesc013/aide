# Current-byte AIDE Lite efficiency candidate: local qualification

Date: 2026-09-29. WorkUnit: `AIDE-STABLE-LITE-RELEASE-EFFECT-01`.
Pack source: `3cc6bf1362aca510aced28ddbab485d4e39317d7`; pack commit: `f26fa5b3d5fc2529c876fea8af3670edc03bae34`; asset commit: `8e9c1c0c2a14350570af586089d734b7048248a0`; release-view commit: `6861954be3069b2e746d437f38bd3ff25f985673`.
The prior technical ACCEPT at `ab1a797d` applies to older bytes.

| Asset | SHA-256 |
| --- | --- |
| `aide-lite-v1.0.0.zip` | `798f44df7898072bb763090ce02317614837775f60ac813ee8c25c0188b2ac5d` |
| `aide-lite-v1.0.0.tar.gz` | `a91a6f284c48c5795012df370c7d12a0b9558eaa736def124acffffe1740cba6` |
| `aide-lite-v1.0.0.manifest.json` | `5939b831ab68a242c3fdfa689ea9fa390ba2a5d2b8f4cce05e2e89516930927e` |
| `aide-lite-v1.0.0.SHA256SUMS.txt` | `7e061f802dd1b38862485edc8b0f10946d70632d60fb8735fadcc54a45ce080d` |

## Exact local checks

- Accepted mediated Codex repeat-guard source: `48235e9a`/tree `be0db1b9`; 51/51 D-managed synthetic tests passed, no skips.
- Extracted-pack consumer: D job `07ee1e7e97ac42f5b75be9dd1f978acb` passed 1/1 without a live model turn.
- Export/build/validate and postcommit replay: jobs `8567381cd43c43f6bf356594be7a4142`, `427c1d52bda946378813349fcf1126e3`, `06d4e09eb6684c918e365175465b3809`, `d24661488e084eaa80d9aa0e56a05718`, `9e9b4289c10244f3a5468698cbdb3ec4` passed; replay changed zero tracked files.
- Current-byte six-consumer matrix: `13c5d0707412123b3ca2c79ca50c1b46be19b45c1a2950af3f6148189da988ee`; six jobs passed serially with scratch retired and reservations released.
- Delivered job forms: 12/12 accepted observations in D job `97d7974237974634a9513b4bc1cb5f41`; summary SHA-256 `87c8f9f2a5aa5fb3b6d284860418648dd39c0e229454ce858d5ccb166cae7a4e`.
- Q47/Q48 source tests: 36/36 passed, no skips, D job `264b2abbaf59479896ddc75deb3c6c1a`.
- Local Q47/Q48 build/validate and postcommit replay passed in D jobs `7026de838d6442ec910298f73ee8c200`, `3edd21e252664d86a864b268e52e2658`, `05b91c1be4244ae58ac54c01320e5988`, `0dce77250a0b4aa98ae2913875a839c2`, `e19c0486b06f4b488509db822f2a1f48`, `999905e102f449b69dc8804835ff3f18`; replay changed zero tracked files.
- `changelog preview --to 3cc6bf13` and `changelog validate` passed; changelog replay changed zero tracked files.
- First Q47 bundle job `619bf392` failed the stale changelog source-binding check; it is retained as a real failed check and was followed by regeneration and a passing bounded rerun.
- The bounded runner refused `.aide/changelog` as an unknown canonical output destination. The existing deterministic changelog CLI was used directly for that small tracked projection; this runner gap remains open.

## Limits and gates

- Candidate remains local and unpublished. No tag, main promotion, downloaded-asset consumer or arbitrary project rollout occurred.
- Ten historical-message owner decisions remain unresolved for main promotion; no decision is inferred.
- Live Codex behavior, native isolated-host effect, hosted target effects and complete usage accounting remain separately unqualified.
- New source and asset bytes require independent exact technical release ACCEPT before dev integration or publication.
