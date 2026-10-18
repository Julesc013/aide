### Fresh symbol discovery qualified

**Outcome.** The existing quality CLI now inspects explicitly selected Python
files for a helper's definitions, syntax calls and import declarations. Results
carry locations, source hashes and parser identity, alongside separate advisory
owner/documentation/test records. Missing or stale records cannot hide fresh
syntax facts. No inspected project code executes and no reports are regenerated.

Use `quality inspect-symbol portable_cli_text --path .aide/scripts/aide_lite.py`.
The JSON view supports machine consumers; the text view escapes Unicode safely.
[Command contract](../../../docs/reference/file-quality-ledger.md),
[implementation](../../scripts/quality_symbols.py),
[behavioral checks](../../scripts/tests/test_quality_symbols.py).

**Qualification.** Source passed 44 methods at 41006cce, including all 23 original
quality/repository assertions. Delivered code passed the same 44 with no failures,
errors or skips at ab7ae7c25bda0f41f069e7a59fbe439feba94865. A real safe-installed Git fixture preserved
customization, had no core tree, retained helper ownership/digests and performed
fresh read-only queries. It located portable_cli_text in both installed and real
AIDE source. An independent assertion verified the one intentional effort-binding
line difference between source and delivered CLI; no raw-equality shortcut.

**Preserved failure and recovery.** Job2 completed ownership6, export, doctor,
validate and pack-status, then failed the task runner's expected-delta assertion:
the generated command catalogue was omitted. Delivered tests had not started.
Its overall exit1, original script in 0e342967 and collected output remain.
Independent review admitted an exact catalogue correction: one quality invocation
gains inspect-symbol, with all other bytes identical. The final third allocation
reused the successful export and source tests, completed the unstarted delivered
and installed checks, then generated the required fixed four-commit preview.
No export or successful product test was repeated, and no assertion was removed.

| Attempt | Outcome |
|---|---|
| 537aee25da434729b8aa8c86c5139f87 | Source 44 passed |
| 64640393e8164835b2dd0341ac7f92ff | Export checks passed; expected-delta assertion failed; preserved |
| 3a66dbce3d86426495876c8685509f20 | Delivered 44, installed consumer and final preview passed |

All three jobs retired quiescent; collections verified, scratch absent and
reservations released. The original three-job ceiling and resource reserves were
preserved. Observed worker memory peaked 534540288 bytes and scratch 4285195 bytes.
No model calls were requested; controller/review and whole-outcome usage are unknown.

**Delivery and limits.** The development pack has 872 verified members: the helper
and its test were added; CLI, file-quality reference, derived command catalogue
and existing export metadata changed. All eight frozen release assets are
unchanged. This is qualified development delivery, not a newly published release.

Source selection is bounded to eight ordinary files, 4 MiB each and 8 MiB total;
ledger reads are capped at 16 MiB and output at 64 KiB. Omitted match counts remain
explicit. Syntax matches do not resolve runtime targets, alias behavior, semantic
equivalence or complete impact. Unselected/invalid areas remain unknown.
Sequential byte checks are not an atomic filesystem snapshot or OS isolation.
No native vintage-host support or whole-task efficiency advantage is claimed.

Original capability-binding/export FAIL observations remain. Reviewed refresh
preserved classifications and made final doctor/validate/pack-status pass.
The existing missing global review-ref warning remains advisory; this task has
its own current reviewed promotion packet.

[Integration effect](evidence/integration-effect.json) requires exact terminal
acceptance and guarded nonforce dev/main synchronization. Actual Git refs and
local integration-result.log establish its completion. Preserve successor refs
dfae9356 and f708e8c6; retire only this task branch after verified synchronization.
The wider host, downstream adoption, publication and efficiency work remains open.
