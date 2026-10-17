# Qualified local dependency tools

The optional source adapter now provides participant-bound inbox, status, submit
and observe tools over the existing Requests ledger. It uses MCP 2025-11-25 stdio
and shared conservative database access. Reading an inbox never acknowledges
delivery, creates a worker or grants execution authority. Native work and the
integration broker retain their original owners and gates.

Managed job `eb166a5cc41941a79b101d4d41072e4f` at source
`3d78991305013fb63e5adf0c4c916d9cba00f032` passed **60 test methods**, with zero
failures, errors or skips: the original 47 plus 13 interface cases. Actual
subprocess exchanges cover separate delivery/acceptance/return/adoption, lost
reply and duplicate recovery, participant filtering, stale/spoofed bindings,
pause/expiry, protocol ordering, malformed frames, complete large histories and
unknown database preservation. The oversized-output oracle is explicitly a
controlled server test; it is not a real external effect.

[Fixture result](evidence/fixture-result.json) retains all test IDs, source hashes,
receipt digest, collection identities and measured peaks. Full logs remain in
the identified retained job. Tests took 45.825 seconds. Observed peak Job memory
was 55,656,448 bytes; scratch peak 238,302 bytes. Collection hashes, quiescence,
scratch retirement and released reservation are verified. Model requests: zero;
controller/reviewer usage and total cost: unknown.

The [first source review](evidence/first-review.json) refused unbounded output.
The repaired candidate enforces 64 KiB input and 1 MiB output limits, preserving
explicit uncertain-effect reconciliation if a response cannot be represented.
[Exact review](evidence/source-review.json) admitted only the first fixture job;
no job ran on the rejected tree. One of two allocations was used, and no further
runtime job is requested. Final validation after commit records two conservative
pack-provenance failures; scoped metadata closure is pending. Published Lite
1.0.0 assets are unchanged.

This proves the bounded local protocol/record path. No live ledger was initialized,
peer contacted, editor configured, new worker launched or target changed. Installed
client compatibility, automatic wake-up, actual existing-worker delivery, independent
cancellation/binding replacement and downstream adoption remain separate required
outcomes. The observed VS Code app-server had no explicit shared-listener flag;
this is not an exhaustive claim that all possible connection routes are absent.

Exact source integration is governed by [integration-effect.json](evidence/integration-effect.json).
Actual commands/ref confirmations are preserved in `evidence/integration-result.log`
after execution; the proposed effect alone is not proof that it happened.
