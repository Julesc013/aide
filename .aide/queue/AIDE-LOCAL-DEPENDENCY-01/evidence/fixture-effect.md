# Exact first fixture effect

Candidate: the independently reviewed staged tree and its clean committed
successor on task/aide-local-dependency-01. The template contains the preparation
base; the controller substitutes only the actual committed source_commit and
source_tree after verifying the reviewed tree. All other template fields and
48 input hashes must remain exact. Template SHA256:
e4ff327db266ed238da4c66da70cc3de56650b7285d6a5737cd95dd3ed52c921.

Run `.aide/queue/AIDE-LOCAL-DEPENDENCY-01/run_checks.py` once through the existing
managed_workspace runner. This is allocation one of maximum two. No job has run.
Use the unchanged configured D root set, config digest
61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90,
1 GiB worker cap, 180-second timeout, 32 MiB scratch and 8 MiB retained limits,
existing physical/commit/storage reserves, current dispatch state and shared
estate admission. No reserve/configuration changes or automatic retries.

The test script loads exactly test_dependency_requests and the unchanged
test_continuous_worker_state. Enumerate actual test identities, retain full
results, fail on any error/failure/skip or count discrepancy. Databases, input
messages and subprocess CLI fixtures use runner TEMP exclusively. One subprocess
intentionally exits 77 after the durable request write to simulate a lost reply;
the parent checks exact exit and duplicate-safe fresh-process continuation.
The script creates no native task, live registration or live runtime state.

Expected artifacts: tests.log and tests.json, runner streams, receipt and actual
resource peaks. Collect exact hashes; reconcile quiescence, retire only owned
scratch and release reservation through the existing runner. Retain any failed
attempt and terminal cause. No new model, acquisition, target, integration,
release, notification, service or unowned process effects.

Static AST and diff checks pass. Doctor passes. Full validate is independently
recorded before source review. Initial pack attempt preceded child creation and
refused missing task; the subsequent registered-child pack passes. Neither
static checks nor that preparation refusal are behavior-test results.

Acceptance proves local cooperative recording and disposable CLI behavior only.
Real delivery, binding replacement, independent cancellation, authenticated peer
effects, whole-task efficiency and downstream adoption remain unqualified.

Original source review rejected tree 2756fe20 before any job. The repaired candidate
preflights existing schema/config through a read-only connection, checks schema
before journal changes, and exposes unmet result obligations/reconciliation. New
CLI refusal fixtures assert unchanged database bytes and absent new sidecars.
