# Current-runner AIDE Lite candidate: local qualification

Date: 2026-09-29. WorkUnit: `AIDE-STABLE-LITE-RELEASE-EFFECT-01`.
Pack source: `0795eefe1b114ba16514ff3881ec3d68834158ce`; pack commit: `d906bb2e67cf9f785ad64fae08cd102fdbbf9662`; asset commit: `4d77183fe770752850fdf78bc08afd5510d863b1`; release-view commit: `8bf41b9374d497b2b7b2d640800daefcf4a72e6a`.
The prior technical ACCEPT at `9cfa91da` applies to older bytes.

| Asset | SHA-256 |
| --- | --- |
| `aide-lite-v1.0.0.zip` | `27948415530f260479c249b2d8cc956792eff4c77a524f0225f61f1f3f2ef7b1` |
| `aide-lite-v1.0.0.tar.gz` | `b8f8ca5e961f399cb8991b0ac231c7ad05dfef8d0fce73661d054b239934a032` |
| `aide-lite-v1.0.0.manifest.json` | `fc8f0aa65c948631ac5ef344086aecdbd72242e82cd225365c8dd25460dec192` |
| `aide-lite-v1.0.0.SHA256SUMS.txt` | `a56e83a06fde9d378fcd7aa31e5ef0bab7094d64944585af9ddb3dbb9c7d0f9e` |

## Exact local checks

- Accepted bounded changelog source: `0063ab23`; 52/52 managed-workspace tests and 12/12 Q34 tests passed in D jobs, no skips.
- Export/build/validate and postcommit replay: jobs `058f202732bd443b81aefd4800792da2`, `1d7135f6b2594797b74dee78e53e35ee`, `445b07c9da1a4ffaa775e06d20f96659`, `b1b83f77030940f984697f0a28652b2f`, `ecc3a13caf6d4602b46fae3857b623f8` passed; replay changed zero tracked files.
- Current-byte six-consumer matrix: `3c844b079999c1799f8425747910fa2d860f8ced25f465fb964ddf7d533e561e`; six jobs passed serially with scratch retired and reservations released.
- Delivered job forms: 12/12 accepted observations in D job `d7006dba3b164250b1541514bf66d021`; summary SHA-256 `a7273b5d70c1ab7017caa72d02d28f210010add4acea8d5142a552f712b281e6`.
- Q47/Q48 source tests: 36/36 passed, no skips, D job `08e12666890040ed977c80e0dead8caa`.
- Local Q47/Q48 build/validate and postcommit replay passed in D jobs `7cceb8da22824fa18c2f5a0094e423e4`, `216b44d8fe58446098c85ae47afa3f35`, `f4b42c6708a141ffaab440c4c87bf5e2`, `a328b140ccb3473c9b8fd6fb2fe44a53`, `ab63417aabd844adb83abbddd8e7f2f3`, `6232baa1bfbd437dbc368693eed06bb5`; replay changed zero tracked files.
- `changelog preview --to 0795eefe1b114ba16514ff3881ec3d68834158ce` through the D-managed canonical root and `changelog validate` passed; D job `cce1ae85847640809d4fc062c0f74dd6` replay changed zero tracked files.

## Limits and gates

- Candidate remains local and unpublished. No tag, main promotion, downloaded-asset consumer or arbitrary project rollout occurred.
- Ten historical-message owner decisions remain unresolved for main promotion; no decision is inferred.
- Live Codex behavior, native isolated-host effect, hosted target effects and complete usage accounting remain separately unqualified.
- New source and asset bytes require independent exact technical release ACCEPT before dev integration or publication.
