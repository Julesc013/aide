# AIDE Contract Audit

Date: 2026-04-29

## Summary

The Q03 Profile/Contract v0 is present, self-describing, and honest about what is implemented. It is declarative repo truth, not a Harness, Runtime, product model, or generator.

## `profile.yaml`

State: present.

Observed posture:

- Identifies `julesc013/aide` as the AIDE self-hosting repo.
- Declares lifecycle `reboot/pre-product`.
- Declares profile mode `self-hosting`.
- Lists public model: AIDE Core, AIDE Hosts, AIDE Bridges.
- Lists internal Core split: Contract, Harness, Runtime, Compatibility, Control, SDK.
- Lists first shipped stack: Contract + Harness + Compatibility + Dominium Bridge.
- Marks Harness v0, generated artifacts, compatibility baseline, Runtime, SDK, product hosts, and bridge implementation as not implemented or deferred.

Audit result: pass with notes. The profile is useful and correctly avoids overclaiming.

## `toolchain.lock`

State: present.

Observed posture:

- Records Profile/Contract and queue schema identifiers.
- Records documented-shapes-only contract tooling.
- Records Harness as planned and executable Harness commands as not implemented.
- Records generated artifacts as not implemented and Q05-owned.
- Does not claim package, install, release, signing, worker, model, runtime, or service automation.

Audit result: pass.

## Component Declarations

State: present in `.aide/components/catalog.yaml`.

Required components are present as catalog entries:

- `core-contract`
- `core-harness`
- `core-compat`
- `core-control`
- `core-runtime-deferred`
- `core-sdk-deferred`
- `hosts-deferred`
- `bridges-dominium`
- `docs`
- `queue`

Weakness: all components live in one catalog file, so future Harness checks need clear line-oriented parsing rules or a later stronger parser.

## Command Catalog

State: present in `.aide/commands/catalog.yaml`.

Observed posture:

- Queue helper scripts are marked implemented.
- `scripts/aide-queue-run` is marked implemented-skeleton and non-mutating.
- Future Harness commands are marked planned:
  - `aide init`
  - `aide import`
  - `aide compile`
  - `aide validate`
  - `aide doctor`
  - `aide migrate`
  - `aide bakeoff`

Audit result: pass. The catalog clearly distinguishes implemented queue helpers from planned Harness commands.

## Policies

State: present.

Key policies:

- `.aide/policies/autonomy.yaml`
- `.aide/policies/bypass.yaml`
- `.aide/policies/review-gates.yaml`
- `.aide/policies/ownership.yaml`
- `.aide/policies/generated-artifacts.yaml`
- `.aide/policies/compatibility.yaml`
- `.aide/policies/validation-severity.yaml`

Audit result: pass with notes. The policies do not loosen review gates. Q04 should read them, not rewrite them.

## Tasks

State: present in `.aide/tasks/catalog.yaml`.

The task catalog describes Q00-Q08 intent and correctly says live execution status remains in `.aide/queue/`.

Weakness: Q04 is still listed as expected packet `planned` in the tasks catalog even though a Q04 planning packet now exists. This is a small metadata freshness issue for Q04 or a future cleanup, not a Q04 blocker.

## Evals

State: present in `.aide/evals/catalog.yaml`.

Current eval posture is honest:

- documentation sanity: manual structural
- queue integrity: script-assisted
- profile completeness: manual structural
- future harness smoke: planned
- future compatibility smoke: planned

Audit result: pass.

## Adapters

State: present in `.aide/adapters/catalog.yaml`.

Adapters are metadata-only for:

- Codex
- Claude Code
- OpenHands
- generic agents

Generated artifacts remain planned for Q05 and no provider/model integrations are implemented.

Audit result: pass.

## Compat Records

State: present.

- `.aide/compat/schema-version.yaml`: baseline schema version record.
- `.aide/compat/migration-baseline.yaml`: placeholder migration baseline owned by Q06.
- `.aide/compat/README.md`: compatibility reference.

Audit result: pass. Compatibility is visible but properly deferred.

## Source-Of-Truth Clarity

Source-of-truth rules are clear in:

- `.aide/profile.yaml`
- `docs/reference/source-of-truth.md`
- `docs/reference/profile-contract-v0.md`
- `.aide/policies/generated-artifacts.yaml`

Important rules:

- `.aide/` is canonical for the repo contract.
- `.aide/queue/` is canonical for task execution state.
- Generated downstream artifacts are outputs, not canonical sources.
- Runtime cache and UI task queues are not truth.
- Bootstrap-era docs remain historical evidence.

## Missing, Weak, Duplicated, Or Overbroad Areas

- Missing: executable Harness validation. This is Q04 scope.
- Weak: no full YAML parser or schema validator exists. Q04 should use restricted structural checks unless a reviewed dependency decision says otherwise.
- Weak: tasks catalog metadata is slightly stale for Q04 packet existence.
- Duplicated but acceptable: queue state appears in both index and per-task status files; `.aide/tasks/catalog.yaml` correctly avoids being live status.
- Overbroad claims: none found in the Profile/Contract records reviewed.
