# Q07 Validation

Date: 2026-04-30

All commands were run from the repository root.

## Pre-Change Harness Checks

`py -3 scripts/aide validate`

- Result: passed with warnings, exit `0`.
- Observed before Q07 edits: `PASS_WITH_WARNINGS`, `109 info, 7 warning, 0 error`.
- Expected warnings were Q00-Q03/Q05/Q06 review gates plus stale generated manifest source fingerprint from Q07 planning.

`py -3 scripts/aide doctor`

- Result: passed with warnings, exit `0`.
- Observed the same expected review-gate and generated-manifest stale-source posture.

`py -3 scripts/aide compile`

- Result: passed, exit `0`.
- Observed dry-run mode with `mutation: none`.
- `.aide/generated/manifest.yaml` would be replaced if `compile --write` were run.

`py -3 scripts/aide migrate`

- Result: passed, exit `0`.
- Observed Q06 no-op compatibility baseline, `mutation: none`, and `migration_needed: false`.

## Post-Change Harness Checks

`py -3 scripts/aide validate`

- Result: passed with warnings, exit `0`.
- Observed after Q07 edits: `PASS_WITH_WARNINGS`, `142 info, 8 warning, 0 error`.
- Expected warnings:
  - Q00-Q03 remain at review gates.
  - Q05 and Q06 raw queue statuses remain `needs_review` even though review evidence records `PASS_WITH_NOTES`.
  - Q07 is now at the required review gate.
  - `.aide/generated/manifest.yaml` has `GENERATED-SOURCE-STALE` because Q07 changed generated-artifact source inputs and did not run `aide compile --write`.
- Dominium Bridge structural checks reported required files and boundary anchors as present.

`py -3 scripts/aide doctor`

- Result: passed with warnings, exit `0`.
- Observed no hard structural errors.
- Doctor reports Q07 Dominium Bridge baseline as AIDE-side only and says Dominium repo mutation and real Dominium generated outputs remain out of scope.

`py -3 scripts/aide compile --dry-run`

- Result: passed, exit `0`.
- Observed `mutation: none`.
- Observed `dominium_bridge_outputs_written: false`.
- Dominium target classes are reported as deferred metadata only.
- `.aide/generated/manifest.yaml` would be replaced if `compile --write` were run.

`py -3 scripts/aide migrate`

- Result: passed, exit `0`.
- Observed Q06 current no-op baseline with `mutation: none`.

`py -3 scripts/aide bakeoff`

- Result: passed, exit `0`.
- Observed metadata/readiness only, no external calls, and declared eval id `dominium-bridge-structural`.

## Tests And Syntax

`py -3 -m unittest discover -s core/harness/tests -t .`

- Result: passed, exit `0`.
- Observed: `Ran 8 tests ... OK`.

`py -3 -m unittest discover -s core/compat/tests -t .`

- Result: passed, exit `0`.
- Observed: `Ran 5 tests ... OK`.

`py -3 -m py_compile <core/harness/*.py> <core/compat/*.py> scripts/aide`

- Result: passed, exit `0`.
- Note: explicit file lists were used because PowerShell does not reliably expand globs for Python.

## Queue Checks

`py -3 scripts/aide-queue-status`

- Result: passed, exit `0`.
- Observed Q07 as `needs_review` with `planning_state: implemented`.

`py -3 scripts/aide-queue-next`

- Result: passed, exit `0`.
- Observed next pending item: `Q08-self-hosting-automation`.
- Q08 must not proceed until Q07 review is complete.

## Bridge Checks

Required file check:

- Result: passed.
- Verified `bridges/dominium/bridge.yaml`, `bridges/dominium/profiles/dominium-xstack.profile.yaml`, XStack scope/mapping records, policy overlays, generator target metadata, compatibility record, and `docs/reference/dominium-bridge.md` exist.

Anchor scan:

- Result: passed.
- Confirmed anchors for `aide.dominium-bridge.v0`, `Dominium-local and strict`, `base_policy_relation: stricter-than-aide`, `emits_outputs: false`, `compatibility_baseline_version: aide.compat-baseline.v0`, and `external_dominium_repo_mutation: prohibited`.

## Generated Artifact Checks

Final target absence check:

- Result: passed.
- `CLAUDE.md` absent.
- `.claude/` absent.

Generated manifest drift:

- Result: expected warning.
- `aide validate` reports `GENERATED-SOURCE-STALE`.
- `aide compile --dry-run` reports `.aide/generated/manifest.yaml: would_replace`.
- Q07 did not run `aide compile --write` because Q07 does not own generated artifact refresh.

## Diff And Path Checks

`git diff --check`

- Result: passed after evidence was written. Git reported line-ending normalization warnings only.

Allowed-path audit:

- Result: passed after Python `__pycache__` directories created by validation were removed.
- Changed paths are within the Q07 allowlist.
