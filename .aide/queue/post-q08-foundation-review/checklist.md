# Post-Q08 Foundation Checklist

## Queue Packets

- [x] Q00 queue packet exists.
- [x] Q01 queue packet exists.
- [x] Q02 queue packet exists.
- [x] Q03 queue packet exists.
- [x] Q04 queue packet exists.
- [x] Q05 queue packet exists.
- [x] Q06 queue packet exists.
- [x] Q07 queue packet exists.
- [x] Q08 queue packet exists.

## Evidence

- [x] Q00 evidence exists.
- [x] Q01 evidence exists.
- [x] Q02 evidence exists.
- [x] Q03 evidence exists.
- [x] Q04 evidence exists.
- [x] Q05 evidence exists.
- [x] Q06 evidence exists.
- [x] Q07 evidence exists.
- [x] Q08 evidence exists.
- [x] Q04 review evidence exists.
- [x] Q05 review evidence exists.
- [x] Q06 review evidence exists.
- [x] Q07 review evidence exists.
- [x] Q08 review evidence exists.

## Harness Commands

- [x] `py -3 scripts/aide --help` passes.
- [x] `py -3 scripts/aide validate` passes with warnings only.
- [x] `py -3 scripts/aide doctor` passes with warnings only.
- [x] `py -3 scripts/aide compile --dry-run` passes with warnings only and writes nothing.
- [x] `py -3 scripts/aide migrate` passes and reports no-op current baseline.
- [x] `py -3 scripts/aide bakeoff` passes and makes no external calls.
- [x] `py -3 scripts/aide self-check` passes with warnings only and writes nothing.
- [!] `py -3 scripts/aide self-check --write-report` was inspected rather than run because `.aide/runs/**` is forbidden for this review task.

## Compatibility

- [x] `.aide/compat/**` baseline records exist.
- [x] `core/compat/**` baseline helpers exist.
- [x] Compatibility tests pass.
- [x] `aide migrate` reports no mutating migrations.
- [x] Replay baseline remains structural, not Runtime replay.

## Generated Artifacts

- [x] Q05 generated-artifact policy exists.
- [x] generated markers and manifest model exist.
- [x] generated outputs remain non-canonical.
- [x] `aide compile --dry-run` reports the manifest would be replaced.
- [x] stale generated manifest source fingerprint is visible.
- [x] no generated artifacts were refreshed during this review.

## Dominium Bridge

- [x] Dominium Bridge records exist under `bridges/dominium/**`.
- [x] `docs/reference/dominium-bridge.md` exists.
- [x] XStack remains Dominium-local.
- [x] Dominium Bridge is AIDE-side only.
- [x] no Dominium repository was modified.
- [x] no real Dominium generated outputs exist.

## Self-Hosting Automation

- [x] `aide self-check` exists.
- [x] self-check is report-first.
- [x] self-check writes nothing unless `--write-report` is supplied.
- [x] queue helpers remain manual/report oriented.
- [x] no automatic Codex invocation exists.
- [x] no auto-merge behavior exists.
- [x] self-check reports stale generated manifest state.

## Scope Leakage

- [x] no Runtime implementation was added by Q00-Q08 foundation review.
- [x] no Host implementation was added by Q08 review or this foundation review.
- [x] no Commander implementation exists.
- [x] no Mobile implementation exists.
- [x] no provider/model/network integration was introduced.
- [x] no release automation was introduced.
- [x] Pack/Skill/Workflow IR remains deferred.

## Warning Classification

- [x] stale generated manifest source fingerprint is classified.
- [x] missing `aide self-check` command catalog metadata is classified.
- [x] Q00-Q03/Q05/Q06 raw status nuance is classified.
- [x] stale self-check proposed-followup text is classified.
- [x] stale root-doc Q08 review phrasing is classified.
