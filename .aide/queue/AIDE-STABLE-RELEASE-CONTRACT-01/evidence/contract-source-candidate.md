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

Five principal source SHA-256 values for the original `aa3bcfec` review
subject, retained as historical evidence (the superseding values follow):

| Path | SHA-256 |
| --- | --- |
| `.aide/policies/release-versioning.yaml` | `58c3e47e6485147d137b2dfbc3ae5364e6fae4245347107f54d986e8801f538a` |
| `.aide/policies/release-publication-boundary.yaml` | `0826d00bd2b15bd469d500961f446a5671e82ef7afcc91f24d138ddf2c5ce705` |
| `.aide/policies/review-gates.yaml` | `7db8f568853e67a2a4226a26daf819397b3cb45317c02c02b9b3be2c29a2b1ef` |
| `.aide/queue/policy.yaml` | `968c23c360f693ec51ca1e008eb61dba75882e3692c58ab5801255ec30164b92` |
| `specs/control-plane/product/scope-and-profiles.md` | `750eaed071c76d97c6f4d2ac3730330e92cdcf97bef9af69888b01126d9b0acf` |

At repaired source commit `4315a8130db2923937ff3f98af2f33cc92c70c61`,
the corresponding values are:

| Path | SHA-256 |
| --- | --- |
| `.aide/policies/release-versioning.yaml` | `2fcae524a4a33b68815a68a11b2bfc4e881c39dfbb99f975560ab01d876b0575` |
| `.aide/policies/release-publication-boundary.yaml` | `0826d00bd2b15bd469d500961f446a5671e82ef7afcc91f24d138ddf2c5ce705` |
| `.aide/policies/review-gates.yaml` | `7db8f568853e67a2a4226a26daf819397b3cb45317c02c02b9b3be2c29a2b1ef` |
| `.aide/queue/policy.yaml` | `968c23c360f693ec51ca1e008eb61dba75882e3692c58ab5801255ec30164b92` |
| `specs/control-plane/product/scope-and-profiles.md` | `bb44e0b078730d7b9807c4e00da69cd9f3cf04735a7a0a31ffb40c563bbeacc4` |

## Verification and limits

- `py -3 -B .aide/scripts/tests/test_q47_release_bundle.py`: exit 0, 18
  tests, `OK` (before the final CLI/review wording additions; Q47 hard flags
  were not changed afterward).
- `py -3 -B .aide/scripts/tests/test_q48_github_release_draft.py`: exit 0,
  11 tests, `OK` (same timing and unchanged Q48 hard flags).
- The precommit `pack-status`, `validate`, and `doctor` observations were made
  before the frozen source commit and **do not qualify** `aa3bcfec`. The
  independent reviewer reran all three on exact commit `aa3bcfec`; each
  exited 1 because the retained export pack no longer had valid source
  provenance. Review report SHA-256:
  `45900dbb33e278f3681f72895afbdbbc13dfb038f4913cca3f3966f760b5dec6`.
  That exact subject received `REQUEST_CHANGES` and is superseded, not accepted.
- After merging current `dev` in commit `060de47208b3b04f4eddde4cfd6fe13687b45189`,
  the controller reran the three commands. `pack-status` exited 1 (log SHA-256
  `ac2df4ff3da9b1d363bf6fb30db0b81cd149373ceafc7cb5f31b7adcce71ccee`),
  `validate` exited 1 (`790a9cd92e47f87804dfb899db3019ade8a4ecfaa4da53fc3279e9fd94eaa692`),
  and `doctor` exited 1 (`aa281ca8ebac7c415bbe14b276493006f0955d19f9c0b0874a7b7ec0c166466b`).
  Logs remain in `D:/Projects/AIDE/_review_scratch/` with prefix
  `stable-contract-060de472-`. The reported export manifest source commit is
  `99a9e54d`; the pack has not been regenerated for this contract source.
- CLI parser help check: PowerShell loop invoked
  `py -3 -B .aide/scripts/aide_lite.py <command> --help` for `doctor`,
  `validate`, `context`, `pack`, `verify`, `task inspect`, `task status`,
  `import-pack`, `rollback-pack`, `plan-removal`, `apply-removal`, and
  `repair-owned-file`. Each returned exit 0 and its required help tokens;
  `import-pack --help` explicitly lists `--mode {full,safe}`, `--dry-run`,
  and `--expect-plan`. This was a parser-only check on the older candidate.
  Current merged source also exposes `--from-pack` and `--resolve TARGET FILE`,
  which the superseding policy now includes. Parser help alone does not
  qualify installed bytes or behavior.
- `py -3 -B .aide/scripts/aide_lite.py task inspect --task-id
  AIDE-STABLE-RELEASE-CONTRACT-01`: exit 0; `status: needs_review`,
  `missing_evidence: 0` before this additional evidence file.
- `git diff --check`: exit 0 after final edits. `git diff --name-only` reported
  only the paths listed above. No generator, commit, ref, tag, upload, API or
  target effect was run in this source slice.
- A supplementary `py -3 -B -c "import yaml, ..."` parse attempt exited 1
  because PyYAML is absent (`ModuleNotFoundError: No module named 'yaml'`).
  The precommit canonical validator result is superseded by the committed
  candidate's provenance failure; a separate PyYAML parse is not claimed.

The source WorkUnit's `.aide/export/**` and `.aide/release/**` paths are
read-only. A separate bounded integration/projection WorkUnit must regenerate
and review derived artifacts, then establish passing committed-candidate
checks before dev integration. A source-only stale-pack state is not a passing
machine gate.

The candidate does **not** choose `1.0.0` or any tag; that value is conditional
on complete fresh history and an exact frozen release manifest. Current source
and preview assets are not declared ready. The remaining path is an
independent exact contract review, later implemented behavior and final
installed/cross-version consumer qualification, separately admitted effect
WorkUnit, exact release review, and fresh observed main/tag/asset/publication
effects. Q47/Q48 history remains preview-only.
