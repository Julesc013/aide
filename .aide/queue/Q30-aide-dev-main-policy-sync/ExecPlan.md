# Q30 ExecPlan - AIDE Dev Main Policy Sync

## Purpose

Q30 makes AIDE's own branch policy explicit after Q28/Q29 added generic branch
roles and dry-run helpers. The result should make future agents understand that
`main` is accepted canonical truth, `dev` is shareable integration truth, and
task-like branches land to `dev` before a gated `dev -> main` promotion.

Q30 does not create, push, merge, promote, prune, delete, fetch, tag, or release
anything in the live AIDE repository.

## Scope

- Add the Q30 queue packet and evidence set.
- Add `.aide/git/aide-branch-policy.yaml`.
- Add generated `.aide/git/aide-dev-main-plan.json` and `.md`.
- Extend AIDE Lite policy validation and reports so AIDE branch policy is
  recognized when present.
- Add Q30 golden tasks and tests.
- Update docs and AGENTS guidance for AIDE's own dev/main workflow.
- Regenerate workflow/helper reports, changelog previews, export pack, and Q31
  task packet.

## Non-Goals

- No live `dev` creation.
- No live `dev` push.
- No live merge, land, promote, prune, branch delete, fetch, tag, or release.
- No GitHub branch protection or CI setup.
- No provider/model/network calls.
- No product runtime, Gateway forwarding, Commander, UI, mobile, MCP/A2A, or
  autonomous loop work.

## Dependencies

- Q27 commit discipline and WorkUnit recovery: present and needs_review.
- Q28 Git workflow policy and detection: present and needs_review.
- Q29 dry-run Git helpers: present and needs_review.
- Current branch topology: local `main`, remote `origin/main`, no detected
  local or remote `dev`.

## Implementation Steps

1. Record baseline Git and validation state.
2. Create Q30 queue packet and set status to running.
3. Add AIDE-specific branch policy and dev/main plan generation.
4. Harden AIDE Lite validation/reporting for AIDE branch policy.
5. Add Q30 tests and golden tasks.
6. Update docs, AGENTS guidance, command catalog, and references.
7. Regenerate reports, changelog previews, export pack, and Q31 packet.
8. Write evidence and set Q30 to `needs_review`.
9. Run final validation and commit coherent slices using Q27 discipline.

## Validation Intent

- AIDE Harness validate/doctor/self-check.
- AIDE Lite validate/test/selftest/eval run.
- AIDE Lite `git detect/doctor/status/policy/plan/sync/land/promote/prune`.
- Targeted Q30 unit tests.
- Full `.aide/scripts/tests` discovery.
- Core Harness/Compat/Gateway/Provider unit tests.
- Export-pack and pack-status.
- Commit latest/range checks.
- Changelog preview.
- Secret scan.

## Review Gate

Q30 must end at `needs_review`, not `passed`.
