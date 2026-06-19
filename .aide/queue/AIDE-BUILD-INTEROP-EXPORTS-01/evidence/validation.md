# Validation

Validation run for `AIDE-BUILD-INTEROP-EXPORTS-01`:

- `git status --short --branch`: PASS; branch `main`, ahead of
  `origin/main` by one pre-existing local commit before this task.
- `git diff --check`: PASS with the existing line-ending warning for
  `.aide/queue/index.yaml`.
- `git diff --cached --check`: PASS.
- JSON parsing for preview and report JSON:
  `.aide/interop/exports/manifest.json`,
  `.aide/interop/exports/mcp-manifest.preview.json`,
  `.aide/interop/exports/a2a-agent-card.preview.json`,
  `.aide/reports/interop-exports/export-index.json`, and
  `.aide/reports/interop-exports/projection-report.json`: PASS.
- Preview hash verification against `.aide/interop/exports/manifest.json`:
  PASS for all six preview artifacts.
- Interop manifest/report consistency check: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-INTEROP-EXPORTS-01`:
  PASS; classification `complete`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-INTEROP-EXPORTS-01`:
  PASS; `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- Secret-like scan over changed files: PASS; `0` findings across `36` files.

Commit-policy validation is recorded after commit.
