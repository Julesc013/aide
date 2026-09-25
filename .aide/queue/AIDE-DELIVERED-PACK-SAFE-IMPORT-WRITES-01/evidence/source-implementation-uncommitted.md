# Safe importer write candidate — uncommitted source checkpoint

Date: 2026-09-25 (Australia/Sydney). Worktree:
`D:\Projects\AIDE\aide-lifecycle-safe-import`, branch
`task/aide-lifecycle-safe-import-01`, base/HEAD
`01466f9e1814b9b8b5083f9fc1ae5910986d8c62`. No Git ref mutation or
generated pack/release rewrite occurred in this implementation pass.

## Changed files

- `.aide/scripts/aide_lite.py` — Windows import writes stage under pinned
  non-reparse ancestors, publish new leaves without replacement, verify
  existing regular single-link preimages through a handle that denies rival
  write/delete sharing, and rename that opened leaf to an intent-bound backup
  before no-replace publication. Intent creation, receipt transition, and
  exact intent cleanup use the same anchored leaf rules. The backup can be
  inspected through the durable import intent when a rival wins the visible
  missing-leaf interval. Staging closes its initially writable CRT descriptor,
  then reopens and verifies the exact regular single-link bytes with rival
  write/delete sharing denied; the protected handle is the one published.
  `atomic_create_bytes_no_clobber` now uses this guarded stage for repair
  intent and payload creation after integration. `windows_pinned_directory` and
  `windows_link_from_handle` were copied from the accepted owned-repair source
  for worktree-local tests; integration must retain one reviewed definition.
- `.aide/scripts/tests/test_export_import.py` — the existing adversarial
  checks and additional backup/replay, receipt-only intent, and
  post-receipt interruption recovery checks.

SHA256 of the current uncommitted files: source
`c1ad047ef9d4cc8d51e74850b1eb48339c29b24e132ba086d6bdbc8c8e0963b2`,
tests `a5d42009ba05a9749a8bca29d4ee1049cb3138b869ccc0b266711a9c9fcddaf3`.

## Focused validation

All commands ran from this worktree with `py -3 -m unittest discover -s
.aide/scripts/tests -p test_export_import.py -k <pattern>`:

| Pattern | Result |
| --- | --- |
| `swapped_parent` | PASS, 2 tests |
| `racing_leaf` | PASS, 1 test |
| `test_import_records_baseline_and_updates_only_unchanged_owned_bytes` | PASS, 1 test |
| `test_interrupted_update_retains_exact_partial_state_and_refuses_replay` | PASS, 1 test |
| `test_dry_run_never_reconciles_a_pending_import_intent` | PASS, 1 test |
| `test_import_update_preserves_preimage_backup_when_rival_wins_publish_gap` | PASS, 1 test |
| `test_import_recovery_reports_backup_and_refuses_rival_replay` | PASS, 1 test |
| `test_import_receipt_only_transition_uses_an_intent` | PASS, 1 test |
| `test_import_recovers_after_receipt_commit_before_intent_cleanup` | PASS, 1 test |
| `test_import_receipt_does_not_follow_a_swapped_parent` | PASS, 1 test |
| `test_atomic_create_staged_bytes_refuse_rival_before_guard` | PASS, 1 test with repair-intent and managed-payload subcases |
| `test_atomic_create_staged_bytes_deny_rival_writer` | PASS, 1 test with repair-intent and managed-payload subcases |
| `test_import_staged_bytes_deny_rival_writer` | PASS, 1 test |

`py -3 -m py_compile .aide/scripts/aide_lite.py
.aide/scripts/tests/test_export_import.py` and `git diff --check` passed.
The initial full importer suite passed 35/35 in 539.971 seconds, but was
bound to its earlier start-time files. Log:
`D:\Projects\AIDE\_review_scratch\safe-import-source-suite-2026-09-25.log`.
Two intermediate full suites passed but are superseded by the guarded-stage
correction: 39/39 in 645.277 seconds at
`safe-import-final-source-suite-2026-09-25.log`, and 40/40 in 679.032 seconds
at `safe-import-frozen-source-suite-2026-09-25.log` in the same external
review scratch directory. They do not qualify the final files. A 43-test
suite bound to the source and test hashes above passed 43/43 in 631.324
seconds, exit 0, tool session `20703`. Log:
`D:\Projects\AIDE\_review_scratch\safe-import-guarded-stage-suite-2026-09-25.log`,
SHA256 `afc72385a5a960ea5780f91c8afb7d2fb769d27a3caac3485942b7fc25ad22a0`.

## Remaining qualification

The update path has a visible interval after the verified old leaf is renamed
and before the staged leaf is published. A rival leaf is preserved; the old
bytes remain at the intent-bound backup, and automatic replay refuses an
unknown state. This is recoverable but not an atomic replacement guarantee.
Interrupted backup restoration is manual pending an exact recovery design.
If an external writer changes the random stage before its guarded reopen,
publication fails closed and leaves that unverified temporary file for
inspection; AIDE does not unlink the altered file by pathname.
The Windows handle implementation was exercised on this Windows host; the
non-Windows importer retains its earlier implementation and is outside this
Windows safety claim. Combined-source, extracted-pack consumer, release
provenance, and independent source review remain pending. The accepted repair
branch wraps effectful imports in the lifecycle lock; the combined merge must
preserve that wrapper and insert these body changes into
`_apply_import_pack_unlocked`.
