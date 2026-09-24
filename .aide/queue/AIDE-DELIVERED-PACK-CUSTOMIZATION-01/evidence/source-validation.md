# Source validation

Date: 2026-09-24 AEST. Branch:
`task/aide-delivered-pack-customization-01`, based on remote dev `3bdeb220`.

- `py -3 .aide/scripts/tests/test_export_import.py -v`: 27/27 PASS,
  292.756 seconds. This ran before adding digest fields to each explanation.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_export_import.py -k customization -v`:
  1/1 PASS, 20.320 seconds, after the digest-field change.
- Same command with `-k feedback`: 1/1 PASS, 19.481 seconds, after the change.
- `git diff --check`: PASS.

The tests use disposable source/target fixtures. They prove project-owned
profile byte preservation, direct managed-file edit conflict before writes,
recorded rationale only for matching bytes, stale/absent rationale as unknown,
malformed metadata refusal, opt-in feedback, and no ordinary feedback output.
No live target or hosted effect was run. Final extracted-archive consumer and
generated-artifact replay remain open.

Later adversarial work found that pending completed/no-effect recovery intent
could be reconciled by a dry run. The repair returned `RECOVERY_REQUIRED`
without target writes and refused feedback without a complete plan. The full
28-case export/import suite passed after that repair in 342.578 seconds.
After adding a reserved project-metadata payload refusal and a final
current-byte rationale check, focused customization (2 cases), pending-intent
(1 case), and reserved-metadata (1 case) runs passed. Final archive
requalification is pending.

The repaired source then ran the full 29-case export/import suite (351.821
seconds), Q47 (18), Q48 (11), and Q31 (6), all PASS. A final Windows reserved
path alias refinement followed those suites. Its focused checksummed uppercase
payload refusal passed. The final archive will be regenerated from that later
source commit, and final source verification will be recorded separately.
