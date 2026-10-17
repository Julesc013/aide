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
no job ran on the rejected tree. The first allocation qualified runtime behavior.
After commit, two conservative provenance failures required the separately
reviewed second allocation. [Pack result](evidence/pack-result.json), job
`11d03c4117c049738fcdbd74b521d94e`, passed six ownership checks, export-pack, doctor,
full validation and pack-status. Only manifest.yaml changed;
all 858 files remain 4,421,128 bytes total, with every payload/checksum byte and
published1.0.0 asset unchanged. Collection and retirement are verified. Both
allocations are exhausted; no further job is requested. The intermediate failures
and premature-status review correction are retained, without converting them to
successful checks.

This proves the bounded local protocol/record path. No live ledger was initialized,
peer contacted, editor configured, new worker launched or target changed. Installed
client compatibility, automatic wake-up, actual existing-worker delivery, independent
cancellation/binding replacement and downstream adoption remain separate required
outcomes. The observed VS Code app-server had no explicit shared-listener flag;
this is not an exhaustive claim that all possible connection routes are absent.

Exact source integration is governed by [integration-effect.json](evidence/integration-effect.json).
Actual commands/ref confirmations are preserved in `evidence/integration-result.log`
after execution; the proposed effect alone is not proof that it happened.

Terminal review accepted source and generated-byte qualification but held main
promotion for an applicable changelog preview. One explicitly additional preview-only
allocation is admitted; original runtime/pack results remain valid. No Git effect
has occurred at this checkpoint. See first-terminal-review.json and the amendment.
