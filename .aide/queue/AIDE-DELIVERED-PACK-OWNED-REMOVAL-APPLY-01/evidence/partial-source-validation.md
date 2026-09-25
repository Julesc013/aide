# Partial owned-removal source validation

Date: 2026-09-25. Worktree: `D:/Projects/AIDE/aide-lifecycle-removal-apply`.
Branch base: `5dfa75e632b09f732a8150376db6840bcf149ed3`.
These checks ran on the task candidate before its source checkpoint commit.
They are not independent technical acceptance.
The source checkpoint is `cd636c9ccd0d4e07a60f8bfd9ba32bcf5ee2ebe2`,
tree `ca06e9ae9ff21a8a0de6a647b2df4a0920a6ce93`. It has the same source,
test, and documentation hashes recorded below.

The source adds `apply-removal --target ... --expect-plan <digest>` and a
target-local removal intent. It checks the current receipt and full preview
identity under the shared lifecycle lock, pins the target root, and hashes and
deletes each candidate regular file through one Windows file handle while
holding non-reparse ancestors and excluding competing write/delete handles.
Multiple hard links refuse. Changed, absent, unknown, or authored material
is preserved. A repeated exact call reconciles an interrupted sequence; a
changed preimage retains the intent and receipt for investigation.

The only implemented effects are exact receipt-owned regular-file removals.
The managed `AGENTS.md` section, authored content, portable CLI runner, and
receipt remain. The
status is `PARTIAL_REMOVAL` with exit code 2. This is not uninstall/detach
completion or stable-release evidence. Non-Windows apply fails closed.

Checks:

- `py -3 -B -m py_compile .aide/scripts/aide_lite.py .aide/scripts/tests/test_export_import.py`: PASS.
- `git diff --check`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py validate`: PASS (large output
  inspected by exit/status; this ran before the source checkpoint commit).
- Three existing removal-planner tests via `py -3 -B .aide/scripts/tests/test_export_import.py <three exact test names> -v`: PASS, 3/3 in 59.563 s.
- Direct new test on the unmerged branch: FAIL with `NameError: windows_pinned_directory` at the shared-helper dependency, before any removal effect.
- Six new adversarial tests via external runner `D:/Projects/AIDE/_review_scratch/removal-provisional-helper-tests.py`: PASS, 6/6 in 91.479 s, with only `windows_pinned_directory`, `portable_lifecycle_lock`, and `atomic_create_bytes_no_clobber` injected in memory from frozen external snapshot `D:/Projects/AIDE/_review_scratch/removal-repair-helper-snapshot.py`, SHA-256 `19172514cd0e5a50c9228e897412483f40c3dcf3d8e7c0b353726cde30c68f3a`. Cases: stale plan/receipt and authored preservation; interruption and repeat reconciliation; changed leaf at handle open; parent junction substituted at handle open; competing writer/delete attempts while the verified handle is held; hard-link refusal.
- After adding an installed-runner check, the affected test reran PASS, 1/1 in 23.682 s, using that same frozen helper snapshot. The installed target CLI could still run `plan-removal --json` after partial effects and gave the same residual plan digest.

The provisional test mechanism changes no repository source or target beyond
disposable temporary fixtures. It does not prove the eventual merged source.
The shared helper must pass independent review and enter the exact integration
candidate; then rerun new and existing tests, canonical validation, extracted
archive consumers, and a consequential source review. The separate importer
write-safety task also remains unresolved.

After `cd636c9c`, canonical `validate` exits `1` on two old generated-pack
provenance checks: the committed pack manifest records source `1a25e33e`
while the task branch HEAD is `cd636c9c`. The postcommit log is
`D:/Projects/AIDE/_review_scratch/removal-partial-postcommit-validate.log`.
No generator was run on this unqualified partial branch; combined regeneration
is an integration obligation. The earlier precommit PASS does not supersede
these current provenance failures.

Source SHA-256: `a3cdfcc14d0a9236ae8caaf0d177ed8f24aafa33800eabfee177bfff3c40c83a`.
Test SHA-256: `c42ca5af8d9342372b0ad8268fb3ae241bea3ab379c473404108fe8ddf50035c`.
Documentation SHA-256: `183d085bb8fbd100db39ce0527b1b910fa4a7f6e28bd99fa3ef84b305b8e10ce`.
