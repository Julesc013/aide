# Artifact Qualification Evidence

- Date: 2026-09-22
- Exported source: `7863891e581db790dce3d5e1a24ac40b3c9eb391`
- Bundle ID: `aide-lite-pack-v0-7863891e581db790`
- Source repository identity: `julesc013/aide`
- Source branch identity: `not-recorded-in-pack`
- Recorded source dirty state: `false`
- Publication effect: none

## Exact Assets

- ZIP: 976881 bytes
- ZIP SHA-256: `622224960f882e1055995c2a9ae6c408f1ba3f8ec242bfe30a5353be781040f7`
- tar.gz: 649071 bytes
- tar.gz SHA-256: `9c16ad304636badf26f9ac1029e833e548181fa411e119574e3cd71d683a4ccd`
- Asset-index records: 9
- Release checksum records: 7
- Release validation: PASS
- GitHub draft validation: PASS

## Validation

- Q31 export-pack governance: 6 passed.
- Export/import lifecycle: 25 passed.
- Q47 release bundle: 17 passed.
- Q48 GitHub release draft: 10 passed.
- Total adjacent tests: 58 passed, 0 failed, 0 skipped.
- Canonical `validate`: PASS.
- Canonical `doctor`: PASS.
- Release bundle and release validation: PASS.
- Release draft and draft validation: PASS.
- Repeatability: 44 compared release files, 0 changed after a second complete
  bundle, validate, draft, and draft-validate cycle.

## Delivered-Byte Consumers

- ZIP fresh project: APPLIED, idempotent rerun NO_CHANGES, doctor PASS.
- tar.gz brownfield project: APPLIED, idempotent rerun NO_CHANGES, doctor PASS.
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
- The remaining projection finding is closed only after the generated
  checkpoint is committed, a complete post-commit bundle/validate/draft cycle
  is committed, and another complete cycle changes zero bytes.
