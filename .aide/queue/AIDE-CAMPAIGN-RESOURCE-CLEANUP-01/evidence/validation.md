# Resource recovery and bounded execution, 2026-09-26

Owner resource correction continues AIDE-CONVERGENCE-AND-DELIVERY-01. No new
checkout, clone or bulk archive was created; the partial-import checkout is
reused. Primary dev and active source are protected.

## Cleanup evidence

Twelve inactive checkouts were retired with supported Git removal, no force
and no branch deletion. Exact paths, HEADs, unchanged refs and absence checks
are in worktree-removal-first.json and worktree-retirement.json. The latter
nine contained 923,271,702 logical file bytes, not measured allocated clusters.
Checks covered clean state, ignored bytecode, ordinary metadata/no reparse or
nested repositories, inactivity and ref retention. Timed-out inspections and
unknown material remain protected. The positively identified abandoned
read-only scanner child was stopped; see stopped-owned-scanner.json.

Initial free-space observations (GiB): C 169.82, D 1.81, E 45.24; physical
memory 9.99. D's first-three-removal interval changed from 21,531,815,936 to
25,197,305,856 free bytes; the next-nine interval changed from 33,537,646,592
to 33,975,140,352. Concurrent unrelated activity prevents attribution of
those net changes solely to this cleanup. capacity-after.json records GUIDs,
later free bytes, physical/commit headroom and 24 remaining worktrees.
No unrelated project, drive-root directory, dirty/unknown state, release asset,
external review original or recovery custody was removed.

## Implementation and verification

- ManagedWorkspaceTests: **PASS**, 12 Windows/Python 3.14 cases in 20.072 s,
  no skips. Explicit tiny fixture parent; fixture cleanup completed.
- Covered disk/memory refusal without allocation, cross-process reservation
  locking, missing/wrong-volume/escaping roots, real junction refusal,
  nonmutating inspection/Git queries, bounded logs, cancellation, monitor
  failure, controller death, interrupted retirement and unique-output retention.
- Earlier failures exposed Windows DirEntry's missing link-count metadata
  and interrupted checkpoint staging. Both were repaired before the PASS.
- Four changed Python modules parsed: **PASS**. git diff --check: **PASS**.
- Actual WindowsHostTests ran through this runner: **PASS**, 10 cases in
  3.303 s; Job peak memory 59,129,856 bytes; logs 1,434 bytes. Scratch absent,
  reservation released. bounded-host-check.json/log bind that execution to
  exact input hashes, environment, limits and process identity. Later collection
  refinements require an affected replay for the final frozen source.

The actual small validation used an ephemeral fixture, not adoption of its
receipt parent as a permanent pool. Example limits: 10 GiB disk reserve,
4 GiB physical/commit reserves, 1 GiB scratch, 256 MiB retained output,
2 GiB Job memory, 16 MiB logs, one heavy job, 32 descendants, one-hour runtime,
100,000 filesystem entries. Its tiny actual-job limits are in the receipt.
Disk limits are reservations/monitored thresholds; memory/process limits use
Windows Jobs and logs use bounded pipe drains. No filesystem sandbox is claimed.
All campaign workspaces must share one configured control root. Only the
explicit Python placement adapter is currently qualified.

## Placement and next action

Canonical source: D:/Projects/AIDE/aide. Active implementation checkout:
aide-stable-lite-partial-import-recovery. Machine paths belong in ignored
.aide.local state; portable defaults contain placeholders. No approved
permanent build/test/temp/cache pool was found in inspected project/local
configuration. One placement question is pending. Heavy validation remains
paused; no fallback to C:, working directory or system temp is authorized.

Next: exact source review and small affected host replay; further proven-safe
reclamation; then the pending importer suite under the owner-resolved pool.
Parent goal remains active/incomplete. No dev/main/tag/publication effect.

## 2026-09-29 closure validation

The placement paragraph above is historical. The owner later selected the
shared D roots, both existing checkouts have identical validated ignored
configuration, and reviewed setup source `5152798b` is in current dev.

Read-only `git merge-base --is-ancestor 5152798b dev` passed. Both
`.aide.local/execution.json` files hashed to
`019669f8faab4ea4e410079ea96966b16742f0e7c6d2e062246a092f1b862834`.
The current-source D-managed export, stable build and 36-test receipts all
show quiescent exit 0, scratch absent and released reservations; exact
identities and observed peaks are in
`qualified-runner-closeout-2026-09-29.md`. `git worktree list` showed only
the two preserved checkouts. The approved scratch root had no children.
`aide_lite.py task inspect --task-id AIDE-CAMPAIGN-RESOURCE-CLEANUP-01`
reported `classification: complete`, `missing_evidence: 0`, and
`noop_already_complete` after the required task-local evidence files were
present. No additional test or resource-intensive job ran for this closeout.
