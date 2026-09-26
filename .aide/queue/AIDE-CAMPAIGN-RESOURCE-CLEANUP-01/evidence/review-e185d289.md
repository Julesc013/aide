# Task OS golden output placement review — e185d289

## Verdict

**ACCEPT_WITH_NOTES** — no blocking finding in this test-placement delta. The real source context, golden runners and original assertions remain active while their 15 report destinations are redirected into temporary storage. A new assertion verifies source report bytes and modification times remain unchanged.

Acceptance covers this test-only source delta. It does not approve activation, dev/main integration, artifact publication or release. Permanent bulk storage placement and full archive/delivered-byte qualification remain open. Prior accepted resource, partial-recovery-oracle and task-status-reader decisions retain their own scopes.

## Exact identity and bounded scope

- Candidate: `e185d2898fb207e59c9eb5380fecf624a3e954ac`
- Tree: `f04b108474a3af0bf18434c4b81e83f33cacaabb`
- Parent: `0302b18c724d463a5865441bb717f9733d26a1eb`
- Existing checkout reused read-only: `D:\Projects\AIDE\aide-stable-lite-partial-import-recovery`
- Reviewed exact Git test delta, associated frozen receipts and relevant unchanged golden-runner/report path behavior. Production Lite, workspace admission and Windows host source blobs are unchanged from the parent.
- No new checkout, reviewer fixture/probe, bulk suite, agent, source edit or Git ref edit. No reviewer-owned live process or temporary fixture remains. Only external review reports were written.

## Correctness and oracle preservation

Only `test_x_os_01_golden_runners_pass` changes behavior in the test module. Catalog definitions continue to come from the real `REPO_ROOT`; every original task-ID membership assertion, call to `run_golden_task(REPO_ROOT, task_id)`, and PASS/errors assertion remains present. AST comparison proves that its original `XOS01_GOLDEN_TASK_IDS` loop is structurally identical and every other test body is identical to the parent.

The test snapshots the original 15 `TASK_OS_COMMAND_REPORT_FILES` paths before patching. It constructs absolute temporary destinations retaining each report's relative suffix, patches every `TASK_OS_*` string constant whose value names those destinations, and patches the report-file list consistently. The coverage equality assertion prevents omission of any report path. In the existing generators and golden runners, `repo_root / <absolute destination>` resolves to that temporary destination; all source/profile/queue/catalog reads still use the real repository root.

The inspected golden runners still generate and read actual reports, check required no-apply markers, parse classification JSON, and enforce the same schema, lifecycle and boundary conditions. Neither generators nor PASS results are mocked. Patching the destinations also redirects the report-file existence list in the context reader; that is projection-location metadata, while the real queue and latest/current task inputs remain unchanged. This review does not claim byte-identical report content when its own projection-path metadata is intentionally redirected.

`ExitStack` restores every patched module constant on exit, and the temporary-directory context retires the generated reports. After restoration and cleanup, the test compares original source report bytes and nanosecond modification times with its pre-run snapshot. Existing absence is also preserved by the `None` sentinel. This extends the oracle beyond the parent test's PASS checks and catches rewriting of any of the 15 known source projections.

## Commands and runtime evidence

Reviewer checks:

1. `git show -s --format="%H %T %P" e185d2898fb207e59c9eb5380fecf624a3e954ac` — exact identity above.
2. `git diff --check 0302b18c724d463a5865441bb717f9733d26a1eb e185d2898fb207e59c9eb5380fecf624a3e954ac` — PASS.
3. Frozen test-method AST comparison and original-loop comparison — PASS: one changed test body, original runner/assertion loop identical.
4. Frozen source comparison — Lite, managed workspace and Windows host input blobs unchanged from the parent.
5. Read frozen `.aide/queue/AIDE-CAMPAIGN-RESOURCE-CLEANUP-01/evidence/bounded-task-status-check.json`; independently hashed all four declared code-input Git blobs — all match the receipt, including changed test SHA-256 `d92b2d583fb8bbd919f9eeef202211b94f499e2ac856b9863a289411050ccfa2`.
6. Verified the retained raw-log SHA-256 and 1,964-byte size, then read its 11 named successful cases: **11 PASS in 8.554 seconds, no skips**. The modified golden test, including source byte/mtime equality, ran successfully. Actual recorded scratch absence was independently observed.

The admitted runtime command is real unittest discovery of `test_x_os_01_task_os_commands.py`. Limits: 120 seconds, 8 MiB scratch, 512 MiB memory, 64 KiB logs. Recorded observed peaks: 2,104 scratch bytes, 212,393,984 Job memory bytes, 1,964 log bytes. Receipt is quiescent, retired, scratch absent, reservation released. These are controller-executed runtime results verified from retained evidence; this reviewer did not rerun the suite.

Raw log: `D:\Projects\AIDE\_recovery\resource-cleanup-20260926\bounded-task-status-check-7d2db0fb594649818cb4bf37f605153e.log`

Raw-log SHA-256: `dbd583837ba99ce8663d6870f805a8c1d6618765199617defe6f3cd9379ee6ea`

## Nonblocking notes and limits

- **Execution identity:** The changed-test run occurred before committing this candidate. Its receipt correctly retains HEAD `0302b18c724d463a5865441bb717f9733d26a1eb` and tree `ad89d8700834cad5a99edbebc068a248eca784a0`, with the changed test input hash. All four declared code hashes match the frozen e185 blobs, supplying evidence for the actual reviewed code bytes. It is not a clean candidate-HEAD run; broader golden catalog/profile/queue context was the real checkout context, not a newly frozen full input manifest.
- **Placement:** The controller ran this test through admitted scratch, which pins the test's temporary-directory allocation. This acceptance is for that test placement and actual run; it does not authorize direct unadmitted heavy runs or establish permanent pool placement.
- **Nonmutation scope:** The new equality oracle protects the 15 known Task OS report projections. It is not a whole-filesystem nonmutation assertion. The delta preserves the real no-apply golden checks and does not expand their supported-product or artifact claims.

The original 0302 eleven-case PASS in 10.084 seconds remains separately archived as `bounded-task-status-0302-check.json`. Its raw log was also verified. The earlier external 0302 review was preserved and appended with that later result, without converting the changed-test run into an original-source result.

No source repair is required for this bounded test-placement delta.
