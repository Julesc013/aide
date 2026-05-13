# Q28 Validation

Status: BASELINE RECORDED.

## Baseline Before Q28 Edits

- `git status --short`: PASS; worktree initially clean.
- `git branch --show-current`: PASS; `main`.
- `git branch --all`: PASS; local `main`, remote `origin/main`, `origin/HEAD -> origin/main`.
- `git remote -v`: PASS; origin is `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD`: PASS; `600c5fb2e61b517da5276145500631e9f0ee16aa`.
- `git log --oneline --decorate -20`: PASS; latest commit was `600c5fb chore(pack): export commit and recovery policies`.
- `git tag --list`: PASS; no tags returned.
- `git check-ignore .aide.local/`: PASS; `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; existing review-gate warnings and stale generated manifest fingerprint.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same Harness warnings and `next_recommended_step: Q25 review`.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; same wider queue-state warnings.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS; 10/10 golden tasks.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS_WITH_WARNINGS; default range includes older pre-Q27 malformed commits and reports them.

## Q27 Prerequisite Check

- `.aide/policies/commit-messages.yaml`: present.
- `.aide/policies/task-resumption.yaml`: present.
- `.aide/policies/work-units.yaml`: present.
- `.aide/policies/recovery.yaml`: present.
- `.aide/hooks/commit-msg`: present.
- `.aide/git/commit-template.md`: present.
- `.aide/changelog/CHANGELOG.preview.md`: present.
- AIDE Lite `commit`, `changelog`, and `task` command families: present.
- Q27 status: `needs_review`, which is sufficient for Q28 redo under the current operator instruction.

## Final Validation

- Pending implementation.
