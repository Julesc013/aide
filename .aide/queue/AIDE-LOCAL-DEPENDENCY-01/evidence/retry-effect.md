# Remaining deterministic fixture allocation

Prepared 2026-10-18. Original job 9a051ea527ae4c2fb93827a7e4e74c57 at bc47743e
ran 46 tests: one failed refusal-sidecar assertion and three fixture cleanup
errors, no skips. Preserve first-result.json and the full retained test log.
Its result is collected, digest-verified, quiescent and retired; no active job
or remaining scratch exists.

The repair keeps every assertion. For a closed database without WAL sidecars,
read committed pages only to reject unknown/uninitialized/mismatched state
before SQLite can create sidecars. This snapshot is never used to authorize a
record change or supply operational status. The successful route still opens
the live database and revalidates schema/config; transactions recheck the pinned
configuration. Concurrent initialization may conservatively refuse. Incomplete
sidecar state requires reconciliation. Explicitly close the three new fixture
connections; SQLite transaction contexts do not close connections.

Run the same offline API/actual-CLI/state regression script exactly once as
allocation two of the original maximum two. Retain all 46 original test methods
and their assertions, adding one method with six absent/empty DB plus sidecar
preservation subcases (47 total methods). Refuse inconsistent sidecars before
the initialization branch, including paired sidecars without a nonempty DB.
Retry template SHA256:
b917df856019ef401d6e8daa95567fc8425c1c1aee634ebf8af0c0c362418e51.
Bind the independently reviewed staged tree and clean committed successor;
substitute only actual source_commit/source_tree after exact checks. All 48
input pins, executable, arguments and configured D runner limits remain bound.
Config digest 61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90.

No new root, live state initialization/contact, model, network, target, Git or
release effect. Collect retained streams/results and verify hashes, quiescence,
scratch retirement and reservation release. No automatic third job. An unchanged
prerequisite produces one terminal result; it does not restart a waiter.

This effect requires a new independent exact verdict. A passing result qualifies
only the cooperative local recording path, not actual host delivery, independent
cancellation, binding replacement, integration or downstream adoption.
