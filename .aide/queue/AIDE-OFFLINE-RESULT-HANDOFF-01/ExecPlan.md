### Offline request and result continuation

**Objective.** Extend the existing portable task handoff so an offline worker can
return a bounded report, candidate patch and check record tied to the exact
request and selected source inputs. The sender can inspect returned work and
detect changed/missing/unsafe base inputs without repeating completed effects.
This implements the next P3/P8 relay increment; no second queue, scheduler,
network transport, model route or automatic patch application is introduced.

**Existing owners.** Keep the pure data codec in .aide/scripts/task_handoff.py
and IO/CLI binding in aide_lite.py. Reuse bounded ordinary-file reads, identity
checks, secret-like-content detection, deterministic JSON and exact digests.
Extend the existing helper rather than importing runtime or provider machinery
into Lite. Preserve the v1 default export/inspect behavior and every old assertion.

**Contract and useful workflow.** An explicit --input path on task handoff export
selects v2 with one to eight exact relative UTF-8 source/context inputs. Each input
retains original bytes and digest; no recursive discovery or transitive copying.
The unchanged v1 export remains available when no input is selected. V2 declares
its new required meaning so old readers refuse instead of silently ignoring it.
Paths are bounded portable relative names; case-colliding or unsafe names refuse.
The 1 MiB bundle and 128 KiB per-record limits remain. No binary archive/extraction.

Add result-export accepting a checksum-verified v2 request, explicit attempt ID,
outcome (submitted/failed/interrupted), required report and optional patch/check
text files. Fixed artifact roles carry original UTF-8 bytes/digests; every result
binds request digest, task, attempt and original source provenance. It is a
candidate observation, never accepted work. Report/check text remains untrusted.
A failed/interrupted result may preserve partial output; it is not a success.

Add result-inspect with both exact request/result digests. Reject wrong-task,
wrong-request, substituted provenance, unsupported required semantics, corruption,
truncation, duplicate keys, excessive size/depth and unsafe reads. Compare fresh
local task records and selected inputs separately; missing, changed and unreadable
bases remain explicit. A matching declared base is not full dependency coverage,
authorship, current authority, test applicability or permission to apply.
Return one compact actionable text view and a complete ASCII-safe JSON view.
No import, source rewrite, grant transfer, execution or live inbox is performed.

**Qualification.** Retain all 79 original handoff/current/resume/binding tests.
Add meaningful request/result round-trip, original-byte preservation, ambiguity,
stale/unknown input, same-request replay, failure/interruption, mismatch,
secret/path/link, partial transfer and no-write tests. Use real fresh CLI processes.
After source qualification, refresh only the existing owned development export,
test delivered code and safe-install into a disposable Git consumer with core
absent and target customization retained. Exercise a two-directory request/reply
exchange with preserved partial work, and inspect a real completed AIDE task's
bounded report/check artifacts. Verify source task records and published/frozen
release assets unchanged. No vintage OS support claim follows from modern-host
ASCII transport tests; no old host executable is installed.

**Sequence.** Exact admission permits one local task branch and managed packet
commit. Then implement, freeze source/job effect and review before native source
tests. Review actual source results before owned export and installed consumer
qualification. Finish fixed changelog preview, complete evidence, independent
terminal review and guarded dev/main synchronization; retire only this local task
branch once observed remote refs and postchecks pass. Preserve dfae9356 and
f708e8c6 branches. Frequent commits use compact-v1; no history rewriting.

**Bounds.** Maximum three managed jobs: source, delivered/installed, final preview.
Each needs exact independent review and fresh admission. Existing config digest
61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90, roots and
180-second/1-GiB/32-MiB-scratch/8-MiB-retained caps and reserves remain unchanged.
No automatic retry or lower reserve. Retain failed and interrupted results.
Code owns collection and retirement. Stop on changed refs/inputs/controls,
unqualified recovery, capacity refusal or unmet required checks; reconcile before
any new effect. All original assertions remain; no widening to new spending,
providers, installations, live targets, endpoints, release assets or privileges.

**Current baseline.** Previous turn made progress: Mini fixture and guarded
dev/main synchronization completed at 66c0b90b6aa0b68cd24659b6279f66b987cb585c. Its 15 scenario evidence remains
valid for that exact fixture; real model use is unqualified. Existing portable
handoff carries only task/status/plan, so the requested result loop is absent.
Unchanged host, DiskEd ownership and publication prerequisites are not re-probed.
This packet is preparation; implementation and execution await exact admission.
