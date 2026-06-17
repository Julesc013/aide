# Validation

## Commands Run

```powershell
git status --short --branch
Get-Content .aide/reports/repo-layout/inventory.json | ConvertFrom-Json | Out-Null
Get-Content .aide/reports/repo-layout/recommendations.json | ConvertFrom-Json | Out-Null
git diff --check
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-REPO-LAYOUT-INVENTORY-01
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py task status
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-REPO-LAYOUT-INVENTORY-01
py -3 .aide/scripts/aide_lite.py repo status
py -3 .aide/scripts/aide_lite.py roots status
py -3 .aide/scripts/aide_lite.py refactor map-status
```

## Results

- `git status --short --branch`: task-owned changes only before commit.
- JSON parse: PASS for inventory and recommendations reports.
- `git diff --check`: PASS with the recurring CRLF warning for `.aide/queue/index.yaml`.
- `doctor`: PASS.
- `task inspect`: PASS; status `needs_review`, classification `complete`, missing evidence `0`.
- `validate`: PASS.
- `task status`: PASS; refreshed `.aide/reports/task-os-task-status.md` and `.aide/reports/task-os-command-status.md`.
- `task evidence`: PASS; no missing evidence.
- `repo status`: PASS; confirms 5,136 files, 0 unknown classifications, 943 generated files, 2,687 evidence files, and 608 orphan candidates.
- `roots status`: PASS; confirms 22 roots, 3 mixed roots, 19 unknown/review-required roots, 15 high-risk roots, and no-apply true.
- `refactor map-status`: PASS; confirms 0 move entries, 20 salvage entries, 0 aliases, 40 rewrite candidates, and no-apply true.

## Pending Final Check

Commit policy check will be run after commit.
