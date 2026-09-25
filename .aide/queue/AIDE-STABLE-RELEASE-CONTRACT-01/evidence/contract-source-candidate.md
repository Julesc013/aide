# Stable Lite contract source candidate, 2026-09-25

## Identity and decision boundary

- Worktree: `D:/Projects/AIDE/aide-stable-release-contract`, branch
  `task/aide-stable-release-contract-01`, based on admission commit
  `74093ecacb4f1f5c2670a2627b04d310904f85ca`. The containing commit
  freezes this contract candidate; its full identity is recorded by the
  subsequent exact review packet.
- Parent authority is the recorded 2026-09-25 owner delegation in
  `AIDE-CONVERGENCE-AND-DELIVERY-01/evidence/owner-delegation-2026-09-25.md`.
  This record is an agent transcription of a conversation decision, not an
  independently verified identity or an independent technical verdict.
- External read-only analysis note SHA-256:
  `aaf8ab963440f7df049892ccef0eaa10a9fae47850ec68478393f04726f0db7f`.
  Parent admission records a read-only GitHub releases/tags no-entry
  observation under `BLACKGLASS-WIN1\Jules` at 09:40 UTC. This source agent
  did not make that hosted observation. A fresh complete local/hosted history
  receipt remains required at final manifest freeze.

## Exact changed paths and rationale

- `.aide/policies/release-versioning.yaml`: conditional Lite package SemVer,
  explicit candidate Windows local CLI forms, public compatibility rules and
  independent pack/schema version axes. The Q47/Q48 `not_established` and
  `preview_only` values still describe the current artifact state.
- `specs/control-plane/product/scope-and-profiles.md`: first stable Lite
  profile target, T3/`shipping`/`companion` only after qualification,
  Windows-only lifecycle apply, archive verification and local offline use
  after acquisition, excluded optional/native/hosted/model profiles.
- `.aide/policies/review-gates.yaml`, `.aide/queue/policy.yaml`, and
  `.aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01/task.yaml`: campaign-only owner
  response route; every hard gate remains a stop, with exact independent
  technical verdict and effects required. `ACCEPT_WITH_NOTES` qualifies only
  when each note is explicit, nonblocking and disposed against the same frozen
  subject; changed subjects and unresolved notes require new review.
- `.aide/policies/release-publication-boundary.yaml`: separate future exact
  effect WorkUnit and frozen manifest, current Q48 no-publish flags retained.
- `governance/release-policy.md`, `docs/reference/aide-lite-release-bundle.md`,
  `docs/reference/github-release-draft.md`, `DOCUMENTATION.md`, `PLANS.md`,
  `IMPLEMENT.md`: reconcile current phase, references, planning and engineering
  log with the candidate boundary, with no shipping or publication assertion.
- This task's `task.yaml`, `status.yaml`, `ExecPlan.md`, and this evidence file:
  record source work and stop at `needs_review` for independent exact review.

Five principal source SHA-256 values after the final wording change:

| Path | SHA-256 |
| --- | --- |
| `.aide/policies/release-versioning.yaml` | `58c3e47e6485147d137b2dfbc3ae5364e6fae4245347107f54d986e8801f538a` |
| `.aide/policies/release-publication-boundary.yaml` | `0826d00bd2b15bd469d500961f446a5671e82ef7afcc91f24d138ddf2c5ce705` |
| `.aide/policies/review-gates.yaml` | `7db8f568853e67a2a4226a26daf819397b3cb45317c02c02b9b3be2c29a2b1ef` |
| `.aide/queue/policy.yaml` | `968c23c360f693ec51ca1e008eb61dba75882e3692c58ab5801255ec30164b92` |
| `specs/control-plane/product/scope-and-profiles.md` | `750eaed071c76d97c6f4d2ac3730330e92cdcf97bef9af69888b01126d9b0acf` |

## Verification and limits

- `py -3 -B .aide/scripts/tests/test_q47_release_bundle.py`: exit 0, 18
  tests, `OK` (before the final CLI/review wording additions; Q47 hard flags
  were not changed afterward).
- `py -3 -B .aide/scripts/tests/test_q48_github_release_draft.py`: exit 0,
  11 tests, `OK` (same timing and unchanged Q48 hard flags).
- `py -3 -B .aide/scripts/aide_lite.py pack-status`: exit 0, checksums true,
  provenance `PASS_SOURCE_ANCESTOR`, boundary PASS. This validates the
  existing ancestor pack, not regenerated current contract bytes.
- `py -3 -B .aide/scripts/aide_lite.py validate`: final exit 0, 60,909
  output lines captured in memory, zero `FAIL` lines. `doctor`: exit 0,
  88 lines, no hard validation failures. Neither command is release
  qualification.
- CLI parser help check: PowerShell loop invoked
  `py -3 -B .aide/scripts/aide_lite.py <command> --help` for `doctor`,
  `validate`, `context`, `pack`, `verify`, `task inspect`, `task status`,
  `import-pack`, `rollback-pack`, `plan-removal`, `apply-removal`, and
  `repair-owned-file`. Each returned exit 0 and its required help tokens;
  `import-pack --help` explicitly lists `--mode {full,safe}`, `--dry-run`,
  and `--expect-plan`. This proves the candidate command forms exist in the
  current source parser, not that installed bytes or behavior qualify.
- `py -3 -B .aide/scripts/aide_lite.py task inspect --task-id
  AIDE-STABLE-RELEASE-CONTRACT-01`: exit 0; `status: needs_review`,
  `missing_evidence: 0` before this additional evidence file.
- `git diff --check`: exit 0 after final edits. `git diff --name-only` reported
  only the paths listed above. No generator, commit, ref, tag, upload, API or
  target effect was run in this source slice.
- A supplementary `py -3 -B -c "import yaml, ..."` parse attempt exited 1
  because PyYAML is absent (`ModuleNotFoundError: No module named 'yaml'`).
  The canonical repository validator passed; a separate PyYAML parse is not
  claimed.

The candidate does **not** choose `1.0.0` or any tag; that value is conditional
on complete fresh history and an exact frozen release manifest. Current source
and preview assets are not declared ready. The remaining path is an
independent exact contract review, later implemented behavior and final
installed/cross-version consumer qualification, separately admitted effect
WorkUnit, exact release review, and fresh observed main/tag/asset/publication
effects. Q47/Q48 history remains preview-only.
