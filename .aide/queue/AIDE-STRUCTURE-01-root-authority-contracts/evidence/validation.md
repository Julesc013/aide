# Validation

## Commands Run

```powershell
git status --short --branch
Get-Content .aide/reports/root-authority-contracts.json | ConvertFrom-Json | Out-Null
git diff --check
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-STRUCTURE-01-root-authority-contracts
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py task status
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-STRUCTURE-01-root-authority-contracts
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-STRUCTURE-01-root-authority-contracts
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-STRUCTURE-01-root-authority-contracts
git diff --check
```

## Results

- `git status --short --branch`: showed only task-owned changes before commit.
- JSON parse: PASS.
- `git diff --check`: PASS with the existing CRLF warning for `.aide/queue/index.yaml`.
- `doctor`: PASS.
- Initial `task inspect`: classified the task as partial while status was still `planning`; this was expected before final status update.
- `validate`: PASS.
- `task status`: PASS and refreshed `.aide/reports/task-os-task-status.md` and `.aide/reports/task-os-command-status.md`.
- `task evidence`: PASS; no missing evidence.
- Final `task inspect`: PASS; status `needs_review`, classification `complete`, missing evidence `0`.
- Final `task evidence`: PASS; no missing evidence.
- Final `git diff --check`: PASS with the existing CRLF warning for `.aide/queue/index.yaml`.

## Pending Final Checks

Commit policy check will be run after commit.
