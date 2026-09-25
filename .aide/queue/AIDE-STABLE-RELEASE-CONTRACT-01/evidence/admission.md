# Stable release contract admission evidence

## Scope and source

- Worktree: `D:/Projects/AIDE/aide-stable-release-contract` on
  `task/aide-stable-release-contract-01`, clean base
  `d4b67c96ff81eb10aeecd6763b538331844619c9` before admission edits.
- Parent: `AIDE-CONVERGENCE-AND-DELIVERY-01`; owner delegation is recorded in
  its `evidence/owner-delegation-2026-09-25.md`.
- External read-only release-contract analysis note:
  `D:/Projects/AIDE/_review_scratch/next-stable-version-and-publication-contract-d4b67c96-readonly.md`,
  SHA-256 `aaf8ab963440f7df049892ccef0eaa10a9fae47850ec68478393f04726f0db7f`.
- The parent controller reports an authenticated read-only GitHub API check
  under `BLACKGLASS-WIN1\Jules` at 2026-09-25 09:40 UTC: releases and tags
  each returned no entries, exit 0. This admission agent did not run the API
  check or assert a new authentication result. A source-bound observation
  receipt remains required before choosing version history.

## Intake and bounded interpretation

`py -3 -B .aide/scripts/aide_lite.py intent compile --prompt <bounded release
contract task>` exited 0 and wrote the four tracked `.aide/intake/latest-*`
outputs. Raw prompt SHA-256:
`093c508e6332fc2489ed08b433d492e4d72dc18b1c7197f03b24fc66724502fa`.
It classified the wording as `task_class: release`, `risk_class: release`,
`sizing_class: blocked`, `requires_split: true`, `blocked: true`, and
`safe_to_execute: false`; it ran no task, provider/model call, or network call.
The queue packet therefore admits only contract work and retains a separate
future exact release-effect WorkUnit. The generated intake files are
task-relevant downstream evidence, not canonical queue authorization.

## Admission change set

Task-local `task.yaml`, `status.yaml`, `prompt.md`, `ExecPlan.md`, and this
admission evidence; one `.aide/queue/index.yaml` entry; concise `PLANS.md`
and `IMPLEMENT.md` admission records; the four task-relevant generated intake
outputs. No release policy, product source, preview artifact, Git ref, tag,
hosted state, or consumer was changed.

## Validation and retained gates

Task inspection, JSON parsing, `git diff --check`, path audit, and final
worktree status are recorded in the companion standard evidence files.
The prepared packet initially ended at `needs_review`; the root controller
then admitted the bounded contract child as `running` under the owner's
campaign delegation, as recorded in `controller-admission.md`. No stable version, public
compatibility contract, support profile, main promotion, tag, or publication
is accepted or executed by this packet. Q47/Q48 preview-only history remains
in force.
