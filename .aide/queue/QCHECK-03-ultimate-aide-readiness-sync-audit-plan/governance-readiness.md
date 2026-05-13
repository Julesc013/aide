# Governance Readiness

## Q27 Commit Discipline And WorkUnit Recovery

- Status: present and `passed`.
- Evidence: present under `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/`.
- Commands: `commit`, `changelog`, and `task` command families are present.
- Tests: AIDE Lite tests and golden tasks pass.
- Exported: yes, via `aide-lite-pack-v0`.
- Target-safe: yes, hook is template-only and not auto-installed.
- Limitation: old history may remain malformed; checker reports rather than
  rewrites history.

## Q28 Git Workflow Policy

- Status: present and `passed`.
- Policies: Git workflow, branch roles, promotion, sync, prune.
- Commands: `git detect`, `git doctor`, `git status`, `git policy`.
- Exported: yes.
- Target-safe: yes, report-only by default.
- Limitation: AIDE has no `dev` branch; detection reports
  `trunk_without_dev`.

## Q29 Merge / Land / Promote Helpers

- Status: present and `passed`.
- Commands: `git sync`, `git plan`, `git land`, `git promote`, `git prune`.
- Tests: fixture mutation paths pass in unit tests.
- Exported: yes.
- Target-safe: yes, dry-run default.
- Limitation: live repo helper commands block on dirty tree, protected branch,
  missing `dev`, or source role mismatch as designed.

## Q30 AIDE Dev/Main Policy Sync

- Status: present and `passed`.
- AIDE-specific branch policy exists.
- Main is canonical; dev is integration; dev is not canonical.
- Limitation: Q30 did not create `dev`; future explicit operator action is
  still required if AIDE adopts a live integration branch.

## Q31 Export Pack Sync

- Status: present and `passed`.
- Pack includes commit, task recovery, Git workflow/helper, changelog, docs,
  golden tasks, and AIDE Lite command support.
- Pack excludes source-specific branch state, queue history, generated context,
  generated reports, `.aide.local`, secrets, raw prompts, and raw responses.
- Limitation: install/upgrade/rollback lifecycle remains future work.

## Q34 Changelog And Release Notes Generator

- Status: present and `passed`.
- Markdown and JSON preview outputs exist.
- Malformed legacy commits are reported, not hidden.
- Exported: source templates/policy/support are exported; generated previews
  are excluded as target truth.
- Limitation: no release publishing, tags, official changelog promotion, or
  semantic versioning inference.

## Q35 GitHub Protection And CI Advisory

- Status: missing/not started.
- Q35 queue directory: missing.
- GitHub policies: missing.
- GitHub command family: missing.
- Recommendation: Q35 is next.
