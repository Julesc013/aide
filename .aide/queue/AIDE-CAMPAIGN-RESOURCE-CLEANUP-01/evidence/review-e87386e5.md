# Partial recovery fixture review — e87386e5

## Verdict

**ACCEPT_WITH_NOTES** — the narrowed fixtures preserve the six affected partial-recovery behavioral oracles. No blocking finding in this delta. Acceptance is limited to this test-oracle change; it does not qualify full payload breadth, delivered archives, integration, permanent storage placement, activation, or release.

## Frozen identity and scope

- Commit: `e87386e55eda38f35525518e8699867f9832802c`
- Tree: `53be4549bee73fe40ee0ac2e3b4b72e7c9d171b9`
- Parent: `8aa60c7bb8a261080dd7d21d5ffd199445264a69`
- Checkout reused read-only: `D:\Projects\AIDE\aide-stable-lite-partial-import-recovery`
- Reviewed exact Git blobs and delta in `.aide/scripts/tests/test_export_import.py`, plus the associated diagnosis, driver/evidence and task-scope statements. Production Lite, input guards, Windows execution host and durability behavior are unchanged by this commit.
- No new checkout, source write, bulk test, fixture allocation, agent, or system-temp probe was performed by this reviewer. No owned live process or temporary fixture remains. This external report is the reviewer's only new file.

## Oracle assessment

`minimal_recovery=True` selects actual source files and all portable template-map keys, including the real Lite engine, target/portable-apply templates, import contract and required files, policy files, compact-task payload and token-budget payload. It still invokes the unchanged real export builder, validates more than 20 included files and an empty boundary-violation list, freezes the resulting multi-file pack, and uses real importer durability operations. It removes unrelated source-family breadth from these six fixtures; it does not replace the importer with a test implementation.

An AST comparison of the two frozen test modules proved that exactly six test methods changed and that their bodies are identical after removing the `minimal_recovery=True` call keyword. The fixture factory is the only additional changed method. Thus assertions, injected interruptions, hostile byte edits, forged records, redigestion, receipt/intent checks and handle-denial checks are unchanged.

| Test boundary | Preserved exercised behavior |
| --- | --- |
| Fresh and predecessor update recovery | Initial and repeated interruption, implicit refusal, explicit fresh/update resume, predecessor receipt identity and authored-file preservation |
| Wrong inputs, rivals and old intent | Wrong plan/pack/mode/predecessor refusal, unwritten managed rival, changed controls, written-payload hardlink, old intent refusal and state preservation |
| Exact manual resolution | Selected bytes must match; receipt preservation on conflict; resolution handle pinned through retirement; merged and other managed bytes verified |
| Forged authored ownership | Redigested plan/receipt/intent cannot convert authored bytes into owned payload; authored bytes and partial intent preserved |
| Controls publication and retirement | Valid controls writes denied at both receipt publication and intent retirement; recovery completes with missing-controls receipt identity |
| Omitted payload coverage | Redigested omitted managed operation remains refused and partial intent remains |

The unchanged missing-controls process test retains its second-process write-denial and abrupt-exit cleanup oracle. Default full export/archive/consumer fixtures remain the original source selection and directory traversal. This patch does not introduce a reduced product profile or claim smaller supported payload scope.

## Verification and execution evidence

Reviewer commands/observations:

1. `git show -s --format="%H %T %P" e87386e55eda38f35525518e8699867f9832802c` — exact identity matched above.
2. `git diff --check 8aa60c7bb8a261080dd7d21d5ffd199445264a69 e87386e55eda38f35525518e8699867f9832802c` — PASS.
3. Python `ast.parse` of both frozen `git show <commit>:.aide/scripts/tests/test_export_import.py` objects; compare each method with `ast.dump(include_attributes=False)`, then normalize only the fixture keyword — PASS: six changed test bodies, no remaining test-body difference.
4. Read the controller's post-commit `.aide/queue/AIDE-CAMPAIGN-RESOURCE-CLEANUP-01/evidence/bounded-importer-recovery-check.json`. Its job binds the exact reviewed commit/tree and the modified test module and Lite engine SHA-256 hashes match the frozen Git blob bytes.
5. Independently verified the recorded raw-log byte count and SHA-256, then read the raw log. All seven named affected cases are `ok`; `Ran 7 tests in 25.090s`, `OK`, no skips. This is controller-executed runtime evidence, not a duplicate reviewer run.

The recorded admitted command was the real Python unittest discovery of `test_export_import.py` with the three selections `partial_recovery`, `redigested_partial_intent`, and `missing_controls_guard`. Receipt limits: 300 seconds, 128 MiB scratch, 512 MiB memory, 64 KiB logs. Observed peaks: 252,903,424 bytes Job memory; 11,654,822 bytes scratch; 1,383 raw log bytes. Result is exit 0, quiescent, retired, reservation released; recorded scratch absence was independently observed.

Raw log: `D:\Projects\AIDE\_recovery\resource-cleanup-20260926\bounded-importer-recovery-check-633105b3ca5a47b2a51bec4806f57450.log`

Raw-log SHA-256: `eb6375d9fc4fbb3f32fc26871b556c9206ca4969530b1f990f98ce8d7e261b40`

The post-commit result JSON is explicitly additional execution evidence for the frozen candidate; it is not claimed to have existed in that commit. The original full-fixture controls PASS (112.647 seconds) and prior 180-second batch timeout remain separate historical evidence. Neither was used as a PASS for these modified oracles.

## Nonblocking notes and limits

- **Coverage / scale:** These six focused tests no longer repeatedly install the full source-family payload. Their accepted coverage is the listed recovery boundaries over a valid multi-file pack. Full pack/export/archive/consumer and final delivered-byte qualification must keep their separate full fixtures and evidence. Their unchanged source is not a claim that they were executed during this review.
- **Evidence / scope:** The diagnosis and pending task posture honestly distinguish the original timeout, isolated full-case PASS, modified candidate validation and outstanding campaign work. No supported-product, full-suite, packaging, integration, or release claim follows from this acceptance.

No source repair is required for this bounded fixture-selection delta.
