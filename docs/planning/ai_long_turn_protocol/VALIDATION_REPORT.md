# Validation Report

## WorkUnit

`AI-LONG-TURN-OPERATING-PROTOCOL-00`

## Status

PASS_WITH_NOTES

## Commands

Final commands and results are recorded in:

- `.aide/queue/AI-LONG-TURN-OPERATING-PROTOCOL-00/evidence/validation.md`

Summary:

- `git diff --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AI-LONG-TURN-OPERATING-PROTOCOL-00`: PASS.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AI-LONG-TURN-OPERATING-PROTOCOL-00`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.

The Eureka-specific validation helper scripts named in the pasted prompt are
not present in this AIDE repo and were not run.

## Notes

This docs package is structural guidance only. It does not enforce behavior in
code and does not authorize branch-sensitive, publication-sensitive,
target-repo, provider/model, Gateway, network, or external discovery work.
