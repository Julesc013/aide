# ExecPlan: Q25 Importer Scope And State Truth Repair

## Goal

Make the AIDE Lite Pack trustworthy enough for controlled handoff by repairing
pack integrity/provenance, narrowing import scope, and refreshing source-of-
truth guidance after Q24 and the Eureka/Dominium pilots.

## Current Baseline

Baseline before edits:

- Worktree clean at `8b19dad7f7666167f1f732b025ea36af1a2c3970`.
- Harness validate/doctor/self-check pass with warnings.
- AIDE Lite `validate` fails because committed pack checksum validation reports
  `manifest.yaml`.
- AIDE Lite `test` passes.
- `pack-status` fails before export, passes after a regeneration command.
- Existing importer dry-run into a temp fixture reports 127 operations and
  would copy broad pack roots.

## Work Plan

1. Create Q25 queue packet and evidence scaffold.
2. Repair checksum/provenance convention and pack-status validation.
3. Narrow import-pack default behavior to safe target scope while preserving a
   clear way to opt into broader optional roots.
4. Add/update AIDE Lite tests for pack integrity and scoped import.
5. Refresh profile, self-check/doctor guidance, command catalog, and docs.
6. Regenerate the pack and Q26 task packet.
7. Run full validation and record evidence.
8. Stop at `needs_review`.

## Non-Goals

- No target repo mutation.
- No live provider/model/network calls.
- No Gateway forwarding.
- No new adapter targets.
- No product feature work.

## Review Gate

Q25 must end at `needs_review`; review must happen before Q26 handover work.
