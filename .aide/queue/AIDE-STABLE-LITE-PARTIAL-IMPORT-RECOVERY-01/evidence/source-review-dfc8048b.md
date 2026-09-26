# Focused independent rereview: publication input guards

Reviewer: Codex child agent `/root/partial_recovery_review`. Date: 2026-09-26.

**Verdict: ACCEPT_WITH_NOTES** for exact commit `dfc8048bc0053b0646e3cd7762d5e23758c1a7ac`, tree `85d4164fec3dd3b540e01dad9253131f00f4b362`, parent `052a0a9265274975e4fea62655dc4eee7783017a`. This acceptance is limited to the input-guard repair and my remaining publication finding. It does not qualify the full importer suite, generated pack/archive, integration, main promotion, tag, or release.

## Correctness conclusion

The remaining finding in my `052a0a92` report is addressed. At `.aide/scripts/aide_lite.py:42406-42448`, final publication now holds the verified existing controls and resolution leaf handles in the same `ExitStack` as the postimages. Their ancestors stay pinned; the leaves are regular and single-linked, and their handles permit reading but deny writers and deletion/replacement. These handles remain open through both receipt publication and intent retirement. Resolution bytes are checked against their original selected digest during guard acquisition. Present v2 controls are parsed from captured guarded bytes, validated with the existing validator, and checked against the original controls digest and disabled decisions before publication.

For absent controls, `portable_import_guard_missing_controls` at lines 41937-41961 acquires an exclusive `CREATE_NEW` reservation below pinned ancestors. A file created by a rival before acquisition causes refusal rather than replacement. The reservation is removed through its own `DELETE_ON_CLOSE` handle; the code never performs a later pathname deletion that could hit an unrelated file. The `finally` closes the owned handle, and the process-exit regression verifies operating-system cleanup after `os._exit(77)`. A change or acquisition failure before publication returns `RECOVERY_REQUIRED` with the intent retained.

Present v1 controls retain the existing advisory semantics: they are preserved and pinned through retirement, while the receipt's effectful controls digest remains `missing`. Present v2 controls retain the existing validated byte-digest and disabled-feature semantics. I found no new material defect in this focused repair.

## Verification and notes

- Exact commit, tree and parent confirmed with `git show -s --format='commit=%H%nparent=%P%ntree=%T%nsubject=%s' dfc8048bc0053b0646e3cd7762d5e23758c1a7ac`.
- `git diff --check 052a0a92 dfc8048b` passed.
- Independently ran `py -3 -B -m unittest test_export_import.ExportImportTests.test_missing_controls_guard_blocks_writer_and_cleans_after_process_exit` from `.aide/scripts/tests`: passed, 1 test in 0.259 seconds. This includes a separate Python writer denial and abrupt child-exit cleanup.
- The external bounded probe `probe_guard_compatibility_dfc8048b.py` reproduced present-v1 recovery with `RECOVERED`, a denied write at intent retirement, unchanged controls bytes, and the expected advisory receipt digest. Its v2-disabled setup stopped before recovery because I omitted the independently required `--expect-plan`; that exit-1 result is a probe setup error and is not claimed as a passing v2 runtime check. The script's `finally` called its temporary fixture cleanup. I did not repeat the fixture after the user reported critical resource pressure. Present-v2 compatibility above is a code-inspection conclusion.
- Task evidence records four focused passing tests, including controls writes at receipt/retirement, resolution writes at retirement, and fresh/update recovery. I inspected those tests and evidence but did not independently repeat all four. Full importer, dependent lifecycle, canonical validation, and delivered-byte qualification remain open.
- Documentation accurately describes the transient reservation and input handles. Queue status remains `running/PENDING` with independent review and full-suite gates recorded.

No tracked file or Git ref was modified. No test process/session remains live. The disposable compatibility fixture was released by its cleanup; only small external probe and requested review report files remain under `D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/`.
