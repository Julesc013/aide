# Validation Commands

- `git status --short --branch`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`
- public metadata inspection with `Invoke-RestMethod` for GitHub repository metadata, raw `info.json`, latest release metadata, and recursive file tree
- `py -3 -c "import json, pathlib; json.loads(pathlib.Path('.aide/reports/canary-profiles/more-infinite-research-v0/current.json').read_text(encoding='utf-8'))"`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CANARY-PROFILE-MORE-INFINITE-RESEARCH-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CANARY-PROFILE-MORE-INFINITE-RESEARCH-01`
- path safety scan
- credential/secret-like scan
- source-output scan
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
