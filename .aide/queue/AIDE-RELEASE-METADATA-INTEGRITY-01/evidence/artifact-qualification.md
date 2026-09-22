# Artifact Qualification Evidence

- Date: 2026-09-22
- Exported source: `1397b703a9c116a5b555948b8587dc53a668237a`
- Bundle ID: `aide-lite-pack-v0-1397b703a9c116a5`
- Source repository identity: `julesc013/aide`
- Source branch identity: `not-recorded-in-pack`
- Recorded source dirty state: `false`
- Publication effect: none

## Exact Assets

- ZIP: 977452 bytes
- ZIP SHA-256: `dfd344260ee39afc0fff833f266e480c3c59f74e083da986c5ed3685a25d61c7`
- tar.gz: 649415 bytes
- tar.gz SHA-256: `57d382171974b92febe79f4a4f865dc8e386fe03213b36a2b6deff8a0c317aaa`
- Asset-index records: 9
- Release checksum records: 7
- Release validation: PASS
- GitHub draft validation: PASS

## Validation

- Q31 export-pack governance: 6 passed.
- Export/import lifecycle: 25 passed.
- Q47 release bundle: 18 passed.
- Q48 GitHub release draft: 11 passed.
- Total adjacent tests: 60 passed, 0 failed, 0 skipped.
- Canonical `validate`: PASS.
- Canonical `doctor`: PASS.
- Release bundle and release validation: PASS.
- Release draft and draft validation: PASS.
- Repeatability: 44 compared release files, 0 changed after a second complete
  bundle, validate, draft, and draft-validate cycle.
- Replacement artifact checkpoint:
  `7897f7deb80c0bb64e63ed2cc93700ef34453598`.
- Post-commit pack provenance: `PASS_SOURCE_ANCESTOR`.
- Replacement bundle, validate, draft, and draft-validate: PASS.
- Post-commit repeatability: 44 compared release files, 0 changed after a
  second complete cycle.

## Delivered-Byte Consumers

- ZIP fresh project: APPLIED with plan
  `945aa03532b4ac0a443d632812ca074833e8ab9b54bfbf2b64f1665a0a644ee4`,
  idempotent rerun NO_CHANGES, doctor PASS.
- tar.gz brownfield project: APPLIED with plan
  `a18d75d84095513d2d77d4712cae3333dbd38a832fdeb754e8c87324417759ce`,
  idempotent rerun NO_CHANGES, doctor PASS.
- Brownfield authored content remained present.
- Both disposable canary directories were removed after validation.

## Boundaries

- No Git tag was created or pushed.
- No GitHub Release was created.
- No asset was uploaded.
- No provider/model call or GitHub API mutation occurred.
- Independent exact-commit review is required before `dev` integration.

## Independent Review Repair

- Exact candidate `2819a63e` received `REQUEST_CHANGES` for three material
  issues: JSON preview identity could mask stale or malformed Markdown state,
  source ancestry honored Git replacement objects, and the committed candidate
  had not converged both release representations through a complete post-commit
  generator cycle.
- Commit `6cbd104c` requires the Markdown and JSON preview source identities to
  parse and agree; malformed or mismatched JSON refuses closed.
- Commit `b4d949c1` disables replacement objects for release ancestry checks and
  adds a real `git replace` adversarial regression.
- The generated checkpoint is committed at `dd1f39f3`; the complete post-commit
  cycle reports `PASS_SOURCE_ANCESTOR`, and another complete cycle changes zero
  bytes. The converged projection and its clean-tree replay remain before exact
  independent rereview.

The prior local checkpoint identities `75e37a4c` and `1e39c424` were never
pushed. Their commit messages used an unsupported `Build:` changelog category.
The two-commit tail was recreated as `dd1f39f3` and `198a87d2` with identical
trees and the required `Fixed:` category; no shared history or artifact bytes
changed.

Independent rereview later found absent paired JSON still failed open and the
published `198a87d2` message retained the superseded `75e37a4c` name. Repair
`f147c905` requires both preview representations; preview checkpoint
`1397b703` binds both to the repaired source. Replacement artifact checkpoint
`7897f7de` is the actual parent named by this post-commit projection.
