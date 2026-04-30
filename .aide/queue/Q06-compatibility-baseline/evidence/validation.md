# Q06 Validation

Date: 2026-04-30

All commands were run from the repository root.

## Pre-Change Baseline

`py -3 scripts/aide validate`

- Result: passed with warnings, exit `0`.
- Observed summary: `75 info, 6 warning, 0 error`.
- Expected warnings: Q00 through Q03 and Q05 review gates, plus stale generated manifest source fingerprint from Q06 planning metadata.

`py -3 scripts/aide doctor`

- Result: passed with warnings, exit `0`.
- Observed summary: `75 info, 6 warning, 0 error`.

`py -3 scripts/aide compile`

- Result: passed, exit `0`.
- Observed: dry-run, no mutation, manifest `would_replace` because Q06 planning changed `.aide/queue/index.yaml`.

`py -3 scripts/aide migrate`

- Result: passed, exit `0`.
- Observed pre-Q06 placeholder report:
  - `compat_schema_status: baseline`
  - `migration_baseline_status: placeholder`
  - `q06_compatibility_baseline: deferred`

## Implementation Sanity Checks

`py -3 -m unittest discover -s core/compat/tests -t .`

- Result: passed, exit `0`.
- Observed: `Ran 5 tests ... OK`.

`py -3 -m unittest discover -s core/harness/tests -t .`

- Result: passed, exit `0`.
- Observed: `Ran 7 tests ... OK`.

`py -3 -m py_compile <core/harness/*.py> <core/compat/*.py> scripts/aide`

- Result: passed, exit `0`.
- Note: explicit file list was used because PowerShell does not expand globs for Python reliably.

`py -3 scripts/aide migrate`

- Result: passed, exit `0`.
- Observed:
  - `compatibility_baseline_version: aide.compat-baseline.v0`
  - `migration_engine: no-op-current-baseline`
  - `mutating_migrations_available: false`
  - `baseline-current-noop`
  - `unknown_future_versions: error`
  - `migration_needed: false`

## Generated Manifest Refresh

`py -3 scripts/aide compile --write`

- Result: passed, exit `0`.
- Purpose: refresh `.aide/generated/manifest.yaml` after Q06 changed approved Q05 source inputs.
- Observed:
  - managed sections in `AGENTS.md` and `.agents/skills/**`: `unchanged`
  - preview Claude output: `unchanged`
  - `.aide/generated/manifest.yaml`: `write`
- No generated target policy or generator behavior was changed.

## Post-Change Harness Checks

`py -3 scripts/aide validate`

- Result: passed with warnings, exit `0`.
- Observed summary: `110 info, 6 warning, 0 error`.
- Expected warnings: Q00 through Q03, Q05, and Q06 review gates.
- Generated manifest warning cleared after refresh.

`py -3 scripts/aide doctor`

- Result: passed with warnings, exit `0`.
- Observed summary: `110 info, 6 warning, 0 error`.
- Output names Q06 compatibility baseline records and recommends Q06 review.

`py -3 scripts/aide migrate`

- Result: passed, exit `0`.
- Observed current version registry and `baseline-current-noop` migration entry.

`py -3 scripts/aide compile`

- Result: passed, exit `0`.
- Observed: dry-run, no mutation, manifest `would_keep`.

`py -3 scripts/aide bakeoff`

- Result: passed, exit `0`.
- Observed: metadata/readiness only, no external calls, `q06_compatibility_smoke: structural replay baseline available`.

`py -3 scripts/aide --help`

- Result: passed, exit `0`.
- Observed command surface includes `init`, `import`, `compile`, `validate`, `doctor`, `migrate`, and `bakeoff`.

## Queue Checks

`py -3 scripts/aide-queue-status`

- Result: passed, exit `0`.
- Observed Q06 as `needs_review` with `planning_state: implemented`.

`py -3 scripts/aide-queue-next`

- Result: passed, exit `0`.
- Observed `Q07-dominium-bridge-baseline` as the next pending item. Q07 must not start until Q06 review passes.

## Compatibility Record Checks

Existence check for:

- `.aide/compat/schema-versions.yaml`
- `.aide/compat/migration-baseline.yaml`
- `.aide/compat/replay-corpus.yaml`
- `.aide/compat/upgrade-gates.yaml`
- `.aide/compat/deprecations.yaml`
- `docs/reference/compatibility-baseline.md`
- `.aide/generated/manifest.yaml`

Result: passed; all files exist.

Anchor scan:

`rg -n "aide.compat-baseline.v0|baseline-current-noop|runtime_replay: false|block_unknown_future|active_deprecations: \\[\\]|COMPAT-VERSION-CURRENT|q06_compatibility_baseline|aide.generated-manifest.v0|q05.generated-artifacts.v0" .aide\\compat core\\compat core\\harness\\commands.py docs\\reference\\compatibility-baseline.md .aide\\generated\\manifest.yaml`

- Result: passed, exit `0`.
- Observed expected anchors in compatibility records, helpers, docs, Harness, and generated manifest.

## Whitespace And Scope

`git diff --check`

- Result: passed, exit `0`.
- Git printed line-ending normalization warnings only; no whitespace errors were reported.

Allowed-path audit:

- Result: passed.
- Changed paths are inside the Q06 implementation allowlist.

## Cleanup

Validation-created Python `__pycache__` directories under `core/compat`, `core/compat/tests`, `core/harness`, `core/harness/tests`, and `scripts` were removed after test and syntax runs.
