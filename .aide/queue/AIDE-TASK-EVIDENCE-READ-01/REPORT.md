### Retained evidence remains usable

**Outcome.** Task views now inspect ordinary evidence up to 1 MiB in 64-KiB
chunks. Task/status records retain their 128-KiB limits. Oversized ordinary
references retain their safe paths; private, redirected and multiply linked
paths remain refused. Evidence bodies are never included in the view.
[Contract](../../../docs/reference/task-packets.md),
[regressions](../../scripts/tests/test_task_current.py).

The completed browser task exposed the defect: its 266,385- and 282,661-byte
receipts previously appeared as record_too_large with no paths. The unchanged
predecessor reproduced that failure. Current/resume/brief now preserve both
references and recommend inspect_completed_evidence. Recorded result and
limitations remain; readable bytes do not establish acceptance or applicability.

**Validation.** All 168 source and 168 delivered methods passed without failures,
errors or skips, preserving 162 original methods. Six new regressions cover
large receipts, digest failure, inclusive limits, bounded chunks/growth and
unchanged record/reference limits. Small-evidence text/JSON matches the predecessor.

The safe-installed project preserves customization and has no core tree.
Its independent >128-KiB fixture verifies evidence bytes while retaining
unverified applicability and outstanding adoption. Installed execution against
the real AIDE task matches the full source observation and inactive HTML.
The independent distribution oracle finds only the intended effort binding.
All selected source and fixture bytes remained unchanged.

| Job | Result |
|---|---|
| cb8f978da79f4746bfcdbf0e8285cb4c |168 source methods and actual predecessor/task checks passed |
| 5c3b5a46edbe4a659847e2b0bbb730cb |6 ownership checks, refreshed export,168 delivered and installed consumers passed |
| bd851a8bc8c44aaea494ab568ffd9b45 |Retained evidence and fixed four-commit preview passed |

All three jobs retired quiescent with verified collections, no scratch and
released reservations. Peak observed worker memory: 372236288 bytes;
scratch: 5602708 bytes. No model requests. Controller/review and whole-outcome
usage remain unknown. Original stale-binding/export failures remain preserved;
the reviewed refresh kept capability classifications unchanged.

**Delivery scope.** The 875-member development pack changes only the CLI,
existing current-task tests and exporter metadata. Eight frozen release assets
remain unchanged. The source reference documents the finite new evidence budget.
The existing browser qualification remains bound to its original page; this
reader change does not claim a new visual or accessibility qualification.

[Integration effect](evidence/integration-effect.json) governs separate nonforce
dev/main synchronization. Actual refs and integration-result.log establish
delivery. Preserve dfae9356/f708e8c6 and retire only this local task branch.
Published 1.0.0, frozen unpublished1.1.0, native downstream adoption, live host
editing and whole-outcome efficiency retain their existing scope and gaps.
