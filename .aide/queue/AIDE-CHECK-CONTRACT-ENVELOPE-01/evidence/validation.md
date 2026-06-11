# Validation

Passed:

- `git status --short --branch`
  - exit code: 0
  - initial state: `## main...origin/main`
- `git remote -v`
  - exit code: 0
  - origin: `https://github.com/Julesc013/aide.git`
- `git rev-parse HEAD`
  - exit code: 0
  - result: `db3a1aba6289c955a68c55724e5e38c4622e62f1`
- `git show --stat --oneline --name-status HEAD`
  - exit code: 0
- `git show --stat --oneline --name-status db3a1aba6289c955a68c55724e5e38c4622e62f1`
  - exit code: 0
- `git show --stat --oneline --name-status f30a233230aaa227ffb05773b7fa31c8a97e5db7`
  - exit code: 0
- `git diff --check HEAD^ HEAD`
  - exit code: 0
- `py -3 .aide\scripts\aide_lite.py task status`
  - exit code: 0
  - task count: 104
- `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-CONTRACT-ENVELOPE-01`
  - exit code: 0
  - status: needs_review
  - classification: complete
  - missing evidence: 0
- `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-CONTRACT-ENVELOPE-01`
  - exit code: 0
  - evidence files: 11
  - missing: none
- `py -3 .aide\scripts\aide_lite.py contract-envelope status`
  - exit code: 0
  - result: PASS
- `py -3 .aide\scripts\aide_lite.py contract-envelope project --source lifecycle-fixture-runner`
  - exit code: 0
  - result: PASS
  - projections written: 3
- `py -3 .aide\scripts\aide_lite.py contract-envelope validate`
  - exit code: 0
  - result: PASS
  - backwards compatibility preserved: true
- `py -3 .aide\scripts\aide_lite.py lifecycle-fixture status`
  - exit code: 0
  - result: PASS
- `py -3 .aide\scripts\aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp`
  - exit code: 0
  - result: PASS
- `py -3 .aide\scripts\aide_lite.py lifecycle-fixture verify`
  - exit code: 0
  - result: PASS
  - checks: 48
- `py -3 .aide\scripts\aide_lite.py validate`
  - exit code: 0
  - result: PASS
- `py -3 .aide\scripts\aide_lite.py test`
  - exit code: 0
  - result: PASS
- `py -3 .aide\scripts\aide_lite.py commit check --latest`
  - exit code: 0
  - result: PASS for checked build commit

Generated task-os and lifecycle-fixture report churn was restored where those
files were not allowed check outputs.
