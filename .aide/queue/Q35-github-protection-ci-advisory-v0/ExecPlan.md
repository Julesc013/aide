# Q35 ExecPlan

## Objective

Implement Q35 as a report-only GitHub protection and CI advisory layer.

## Scope

- Add advisory policies for GitHub protection, branch protection, and CI gates.
- Add `.aide/github` generated reports.
- Add AIDE Lite `github` commands.
- Add tests and golden tasks.
- Export portable policy/docs in `aide-lite-pack-v0`.
- Refresh docs, evidence, and next task packet.

## Non-Goals

- No GitHub API calls.
- No `.github/workflows` writes.
- No branch mutation, push, tag, release, provider, model, or network calls.
- No active CI or branch protection application.

## Plan

1. Create Q35 queue packet and report-only policy files.
2. Add AIDE Lite advisory generation and validation commands.
3. Add tests and golden task coverage.
4. Generate advisory reports and export pack.
5. Refresh validation/evidence and prepare Q36 as the next planned queue item.

## Result

Q35 is implemented and validated as report-only advisory tooling. Future apply
behavior remains deferred to a separate reviewed queue phase.
