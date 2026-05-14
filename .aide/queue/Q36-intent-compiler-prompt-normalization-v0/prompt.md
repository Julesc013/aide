# Q36 Prompt Summary

Implement Intent Compiler and Prompt Normalization v0.

Use QCHECK-03 and Q35 as context. The purpose is to make AIDE compile vague,
broad, repeated, wrong, unsafe, target-repo, or out-of-order prompts into
bounded WorkUnit drafts that use repo evidence, queue state, branch role
preflight, validation plans, evidence requirements, rejected interpretations,
and explicit non-goals.

The compiler is deterministic, local, no-call, and compile-only. It writes
reviewable intent packets and WorkUnit drafts; it does not execute the drafted
task.

Do not implement product features, provider/model calls, outbound network
calls, branch mutation, target repo mutation, install/upgrade/rollback behavior,
Gateway forwarding, release publishing, or autonomous execution.
