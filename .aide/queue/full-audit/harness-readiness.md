# Q04 Harness Readiness Audit

Date: 2026-04-29

## Verdict

Q04 Harness v0 is ready to implement. The plan, dependencies, contract records, and command boundaries are clear enough for a future worker.

Harness v0 itself is not present.

## Current Harness Files

| Path | State | Notes |
| --- | --- | --- |
| `core/harness/README.md` | exists | Skeleton-only; says Harness v0 is Q04. |
| `scripts/aide` | missing | Expected before Q04 implementation. |
| `core/harness/aide_harness.py` | missing | Planned Q04 implementation file. |
| `core/harness/commands.py` | missing | Planned Q04 implementation file. |
| `core/harness/contract_loader.py` | missing | Planned Q04 implementation file. |
| `core/harness/diagnostics.py` | missing | Planned Q04 implementation file. |
| `docs/reference/harness-v0.md` | missing | Planned Q04 reference. |

## Command Surface Check

`scripts/aide` does not exist, so these commands are absent:

- `aide init`
- `aide import`
- `aide compile`
- `aide validate`
- `aide doctor`
- `aide migrate`
- `aide bakeoff`

This matches `.aide/commands/catalog.yaml`, which marks them as planned future Harness commands.

## Exact Files Q04 Should Create Or Update

Expected new or updated implementation files:

- `scripts/aide`
- `core/harness/README.md`
- `core/harness/aide_harness.py`
- `core/harness/commands.py`
- `core/harness/contract_loader.py`
- `core/harness/diagnostics.py`
- optional small `core/harness/tests/**` files if the implementation keeps them lightweight
- `docs/reference/harness-v0.md`

Expected root or queue updates:

- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/commands/catalog.yaml` if command posture is updated truthfully
- `.aide/queue/index.yaml` if Q04 status changes
- `.aide/queue/Q04-harness-v0/status.yaml`
- `.aide/queue/Q04-harness-v0/ExecPlan.md`
- `.aide/queue/Q04-harness-v0/evidence/changed-files.md`
- `.aide/queue/Q04-harness-v0/evidence/validation.md`
- `.aide/queue/Q04-harness-v0/evidence/command-smoke.md`
- `.aide/queue/Q04-harness-v0/evidence/remaining-risks.md`

## Minimum Acceptance Criteria For Q04

- `scripts/aide --help` works from repo root.
- `scripts/aide validate` checks required `.aide/` files, contract anchors, queue packet coherence, and source-of-truth references.
- `scripts/aide validate` returns nonzero on hard failures.
- `scripts/aide doctor` prints actionable diagnostics.
- `scripts/aide compile` prints a deterministic compile plan and does not write generated target artifacts.
- `scripts/aide migrate` reports no-op baseline or missing compatibility records without changing repo state.
- `scripts/aide bakeoff` reports metadata/readiness only and does not call providers, models, native hosts, network resources, or external tools.
- Q04 remains Python standard-library only unless a reviewed dependency decision exists.
- Q04 writes evidence and stops at `needs_review`.

## Implementation Risks For Q04

- Overbuilding YAML/schema validation instead of small structural checks.
- Accidentally generating Q05 target artifacts during `compile`.
- Treating queue helper scripts as a full Harness.
- Marking Q00-Q03 as accepted without review or explicit authorization.
- Updating `.aide/commands/catalog.yaml` too aggressively before commands exist.
- Adding Runtime, provider, service, host, or app behavior under the label of Harness.

## Readiness Decision

Proceed with Q04 implementation. Keep it narrow, deterministic, local, and non-generating.
