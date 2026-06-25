# Validation Commands

Commands run for this check:

- `git status --short --branch --untracked-files=all`
- `git rev-parse HEAD`
- `git rev-parse origin/main`
- `git log -10 --oneline`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01`
- `py -3 .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01/evidence/independent_distribution_manifest_check.py`
- `py -3 -m py_compile .aide/queue/AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01/evidence/independent_distribution_manifest_check.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_distribution_manifest_v1.py"`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- scoped check-surface local-path and selected secret-like scan
- `git diff --check`
- `git diff --cached --check`

Commands intentionally not run:

- `distribution-manifest project` or `distribution-manifest validate`, because
  those regenerate source build reports outside this check task's allowed
  outputs.
- release publish, upload, tag, install/update/repair/rollback/uninstall apply,
  target mutation, network, provider/model, Workbench/MCP, and promotion
  commands.
