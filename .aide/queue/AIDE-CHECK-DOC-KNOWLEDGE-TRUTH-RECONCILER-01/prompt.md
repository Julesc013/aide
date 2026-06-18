# Prompt

Create and process `AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`.

Use `.aide/queue/index.yaml` as canonical queue truth.

Goal: independently check `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01` and
determine whether the doc/knowledge truth reconciler is ready for acceptance,
needs hardening, is blocked, or is partial.

This is a check-only task. It may write task-local evidence and check reports.
It must not repair docs, edit OKF, regenerate OKF, rewrite context packets,
move files, rewrite references, implement generated-output ledger, implement
report index, implement schemas, add CLI behavior, call providers/network, or
mutate GitHub/branches/releases/target repos.

Because prior build context is available in this thread, record reduced
session independence and rely only on repository artifacts, tests, hashes, and
commands.
