# Q28 Validation

## Baseline Before Q28 Edits

- `git status --short`: PASS; worktree initially clean.
- `git branch --show-current`: PASS; `main`.
- `git branch --all`: PASS; local `main`, remote `origin/main`, `origin/HEAD -> origin/main`.
- `git remote -v`: PASS; origin is `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD`: PASS; `600c5fb2e61b517da5276145500631e9f0ee16aa`.
- `git log --oneline --decorate -20`: PASS; latest commit was `600c5fb chore(pack): export commit and recovery policies`.
- `git tag --list`: PASS; no tags returned.
- `git check-ignore .aide.local/`: PASS; `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; pre-existing review-gate warnings and stale generated manifest fingerprint.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same Harness warnings and `next_recommended_step: Q25 review`.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; same wider queue-state warnings.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS; 10/10 golden tasks before Q28 goldens.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: WARN; older pre-Q27 malformed commits reported.

## Q27 Prerequisite Check

- `.aide/policies/commit-messages.yaml`: present.
- `.aide/policies/task-resumption.yaml`: present.
- `.aide/policies/work-units.yaml`: present.
- `.aide/policies/recovery.yaml`: present.
- `.aide/hooks/commit-msg`: present.
- `.aide/git/commit-template.md`: present.
- `.aide/changelog/CHANGELOG.preview.md`: present.
- AIDE Lite `commit`, `changelog`, and `task` command families: present.
- Q27 status: `needs_review`; sufficient for Q28 redo under current operator instruction.

## Targeted Q28 Validation

- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py git detect`: PASS; wrote `.aide/git/workflow-detection.json` and `.md`.
- `py -3 .aide/scripts/aide_lite.py git doctor`: PASS; current branch `main`, role `canonical`, workflow `trunk_without_dev`.
- `py -3 .aide/scripts/aide_lite.py git status`: PASS; report-only, dirty tree warning during implementation.
- `py -3 .aide/scripts/aide_lite.py git roles`: PASS.
- `py -3 .aide/scripts/aide_lite.py git workflow`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q28_git_workflow.py`: PASS; 8 tests.
- `py -3 .aide/scripts/aide_lite.py eval run --task git_workflow_policy_golden`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run --task branch_role_detection_golden`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run --task promotion_rules_golden`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run --task sync_policy_golden`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run --task prune_policy_golden`: PASS.

## Final Validation

- `git diff --check`: PASS; only Git line-ending normalization warnings.
- `git status --short`: PASS; shows expected Q28 generated artifacts and evidence before final commit.
- `git branch --show-current`: PASS; `main`.
- `git branch --all`: PASS; local `main`, remote `origin/main`; no live branches created by Q28.
- `git remote -v`: PASS; origin fetch/push URL reported; no push run.
- `git check-ignore .aide.local/`: PASS; `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; 148 info, 7 warnings, 0 errors. Warnings are pre-existing review-gate/generated-manifest posture outside Q28 branch-policy scope.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same Harness warning set.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; same queue review-gate/generated-manifest warning set.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS; includes Q28 policy anchors and workflow detection non-mutating check.
- `py -3 .aide/scripts/aide_lite.py test`: PASS after fixing the Q28 selftest fixture copy issue.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS after fixing the Q28 selftest fixture copy issue.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS; 15/15 golden tasks.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~5..HEAD`: PASS; Q28 commits all satisfy Q27 discipline.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: WARN; 20 commits scanned, 8 categories, 6 malformed pre-Q27 commits reported, no publishing.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS; 169 included files, 172 checksums, boundary PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, `DIRTY_SOURCE_RECORDED`, boundary PASS.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q29 Merge Land Promote Helper v0"`: PASS; `.aide/context/latest-task-packet.md`, 3,676 chars, 919 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS; 919 approximate tokens, within budget.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS; 141 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS; 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS; 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS; 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS; 8 tests.
- Targeted `rg` secret scan: PASS_AFTER_INSPECTION. Matches were policy/test/template/path terms such as `TOKEN`, `api_key`, `SECRET`, `PASSWORD`, `sk-ant` regex text, and `latest-task-packet`; no actual provider key, private key, `.env` content, `.aide.local` state, raw prompt, or raw response was found.

## Remediated Validation Finding

Initial broad validation found Q28 golden tasks failing inside the AIDE Lite
selftest fixture because `_write_minimal_repo` copied the golden catalog but not
the new Q28 Git policy files. Q28 fixed this by copying `Q28_REQUIRED_FILES`
into the selftest fixture. Reruns of AIDE Lite `test`, `selftest`, Harness
tests, and Gateway tests passed.

## Live Git Safety

Q28 did not create, delete, merge, push, prune, fetch, or promote any live AIDE
branches. All mutation-like behavior in Q28 is limited to committed report,
policy, docs, evidence, changelog preview, task packet, and export-pack files.
