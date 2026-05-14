# Warning Inventory

## Baseline Findings

- `git status --short --branch`: local `main` was clean and ahead of
  `origin/main` by one commit before QFIX-05 edits.
- `py -3 .aide/scripts/aide_lite.py task status`: 50 queue items were present.
- `py -3 scripts/aide validate`: `PASS_WITH_WARNINGS` with one warning:
  `.aide/generated/manifest.yaml` source fingerprint was stale.
- `py -3 .aide/scripts/aide_lite.py validate`: `PASS`.
- `git diff --check`: `PASS`.

## Review-Gated Tasks

The following implemented tasks remained `needs_review` at baseline and are not
failures, but they block honest public-release claims until reviewed:

- `Q36-intent-compiler-prompt-normalization-v0`
- `Q37-repo-intelligence-index-v0`
- `Q38-file-quality-ledger-v0`
- `Q39-refactor-control-plane-v0`
- `Q40-root-recycling-framework-v0`
- `Q41-existing-tool-absorption-v0`
- `Q42-move-map-salvage-map-path-alias-v0`
- `Q43-install-plan-model-v0`
- `Q44-repair-doctor-model-v0`
- `Q45-upgrade-model-v0`
- `Q46-rollback-uninstall-model-v0`
- `QFIX-04-aide-lite-selftest-performance`

## Classification

- Fixable in this pass: deterministic generated manifest drift.
- Not fixable in this pass: review-gated tasks, absent public release bundle,
  absent release tag, absent live CI enforcement, and absent target-side apply
  phases. Those require reviewed future queue items.
