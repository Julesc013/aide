# Helper Review

Helper path: `core/protocol/capability_manifest.py`.

Reviewed:

- Uses only the standard library and existing `core.protocol.envelope` /
  `core.protocol.reference_id` helpers.
- Projects from live queue acceptance status/evidence, existing protocol
  reports, OKF pages, and Reconciler reports.
- Writes deterministic JSON and Markdown reports.
- Validates required capability projection, evidence refs, accepted-with-warning
  preservation, reference syntax, OKF/Reconciler integration, and boundary
  flags.

Boundary:

- No conformance, admission, runtime, provider/model, network, Gateway, GitHub,
  branch/worktree, apply, release, or repair behavior is implemented.
