# Validation

Validation results:

- `git status --short --branch`: PASS. Dirty paths are limited to `.aide/queue/index.yaml`, `IMPLEMENT.md`, `PLANS.md`, `.aide/queue/AIDE-DOMINIUM-INTEGRATION-CHARTER-01/**`, and `.aide/reports/dominium-integration-charter/**`.
- `git diff --check`: PASS with Git line-ending normalization warnings for `.aide/queue/index.yaml`, `IMPLEMENT.md`, and `PLANS.md`; no whitespace errors reported.
- Charter structural validation: PASS.
  - Parsed 7 charter JSON report files.
  - Parsed Dominium `.aide/queue/current.toml` read-only.
  - Confirmed 45 critical-path nodes, unique task ids, dependency resolution, acyclicity, read-only charter status, and trust/preview ancestors for mutation-capable future nodes.
  - Confirmed 55 task-dependency-graph nodes and valid edge endpoints.
  - Confirmed 13 object-mapping rows and 15 refusal-mapping rows.
  - Confirmed generated reports/projections are not canonical.
  - Confirmed no changed path outside the allowed AIDE-local charter scope.
  - Confirmed Dominium worktree remained clean.
  - Secret-like scan used exact provider-key environment variable names, boundary-aware provider token prefixes, and private-key headers, and found no matches.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-DOMINIUM-INTEGRATION-CHARTER-01`: PASS.
  - status: `needs_review`
  - classification: `complete`
  - evidence_files: `22`
  - missing_evidence: `0`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `missing:` empty.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.

Post-commit validation to run after the commit object exists:

- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
