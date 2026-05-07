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

1. Create Q25 queue packet and evidence scaffold. Done.
2. Repair checksum/provenance convention and pack-status validation. Done.
3. Narrow import-pack default behavior to safe target scope while preserving a
   clear way to opt into broader optional roots.
   Done.
4. Add/update AIDE Lite tests for pack integrity and scoped import. Done.
5. Refresh profile, self-check/doctor guidance, command catalog, and docs.
   Done.
6. Regenerate the pack and Q26 task packet. Done.
7. Run full validation and record evidence. Done.
8. Stop at `needs_review`. Done.

## Results

- `pack-status` passes with `checksum_problems: 0`.
- Safe import dry-run reports exact writes and skips broad `core/**` and
  `docs/**` roots.
- Fixture import preserves manual `AGENTS.md` content and can run
  doctor/snapshot/index/pack.
- `scripts/aide self-check` now recommends Q25 review instead of stale
  QFIX-02/Q21 followups.
- `.aide/context/latest-task-packet.md` now targets Q26 Eureka Pilot Review And
  Handover.

## Non-Goals

- No target repo mutation.
- No live provider/model/network calls.
- No Gateway forwarding.
- No new adapter targets.
- No product feature work.

## Review Gate

Q25 must end at `needs_review`; review must happen before Q26 handover work.
