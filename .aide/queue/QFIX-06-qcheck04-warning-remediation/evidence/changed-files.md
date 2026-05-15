# Changed Files

## Queue And Evidence

- `.aide/queue/QFIX-06-qcheck04-warning-remediation/**`
- `.aide/queue/index.yaml`

## Runtime And Test Performance

- `.aide/scripts/aide_lite.py`
  - caches successful `run_selftest()` results for repeated in-process test calls.
  - skips `git ls-files` for non-git fixture roots.
  - reduces `_write_minimal_repo()` fixture materialization by avoiding full export-pack and full golden-task tree copies.
- `.aide/scripts/tests/test_cache_local_state.py`
- `.aide/scripts/tests/test_gateway_commands.py`
- `.aide/scripts/tests/test_outcome_controller.py`
- `.aide/scripts/tests/test_router_profile.py`
  - use the selftest golden subset in local fixtures instead of the full golden catalog.

## Generated AIDE State

- `.aide/generated/manifest.yaml`
- `.aide/evals/runs/latest-golden-tasks.json`
- `.aide/evals/runs/latest-golden-tasks.md`
- `.aide/changelog/**`
- `.aide/github/github-advisory.json`
- `.aide/github/github-advisory.md`

## Export And Release Artifacts

- `.aide/export/aide-lite-pack-v0/**`
- `.aide/release/dist/**`
- `.aide/release/github-release-*.json`
- `.aide/release/github-release-*.md`
- `.aide/release/latest-*.json`
- `.aide/release/latest-*.md`

## Boundary Notes

- No target repository files were edited.
- No branch, tag, GitHub Release, upload, or publish mutation was performed.
- No install/repair/upgrade/rollback/uninstall apply mode was run.
