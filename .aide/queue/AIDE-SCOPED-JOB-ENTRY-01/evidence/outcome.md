# Public scoped job outcome

Source 886290be31357b40eef137c65d203fd9e170ecb3 completed the necessary
affected export refresh and unchanged full repository validation through
`aide_lite.py job run`. Job ce62387adceb40ab8bf31268a7964abd passed all
64 regressions (52 existing managed-workspace tests plus 12 scoped tests),
without errors, failures or skips. Full validation exited 0 in 13.518 seconds.
This is bounded worker qualification; whole-session containment remains open.

## Actual routes and protections

The normal public entry loads the accepted SHA-pinned ZIP directly as its
known-good process/storage owner, with no extraction or additional checkout.
It binds the prepared configuration digest, verifies the dependency closure
and executable, then uses the owner's existing estate lock and lifecycle.
Workers cannot alter the trusted archive, operator config or control receipt.

The worker ran as BLACKGLASS-WIN1\\CodexSandboxOffline inside the named
Windows Job. Source/toolchain reads, the exact active receipt read, owned
tmp/cache/output writes and the exact export destination were selected.
Network was disabled in the command profile. Direct and child fixture writes
outside their permitted directories failed; the child specifically returned
19 for PermissionError. Config, trusted-archive and control write opens failed.

The outer shell/editor still runs unrestricted as Jules. Plugin/browser routes,
other sessions, GitHub credential-dependent integration, Codex host metadata
and unmanaged tools are not governed by this worker profile. Installed Codex
0.145.0 read exclusion remains failed, preserved in the earlier qualification.
This entry is opt-in via explicit operator-local configuration; legacy jobs do
not inherit it automatically. It is not mandatory whole-session enforcement.

## Limits, destinations and measurements

| Control | Effective bound and evidence |
| --- | --- |
| Process/memory | Existing Windows Job: 32 processes, 2 GiB memory; measured peak 342,159,360 bytes |
| Runtime/logs | 900 seconds, 6 MiB retained pipes; actual logs 4,906,115 bytes |
| Scratch/cache | 8 MiB scratch plus log allowance, monitored; measured peak 4,908,585 bytes |
| Canonical export | Exact existing `.aide/export/aide-lite-pack-v0`, 16 MiB declaration, monitored; final 4,160,454 bytes |
| Aggregate | 256 MiB cooperative admission: scratch/cache, retained results/logs, control and declared canonical artifacts plus reservations, under the same lock |
| Headroom | Original 10 GiB disk and 4 GiB physical/commit reserves preserved |

All job resources use the existing
`D:/Projects/AIDE/.aide.local/execution/{scratch,retained,control}` selections.
After completion scratch was zero; retained was 187,138,974 logical bytes;
control was 13,694,135; the export was 4,160,454. These logical-byte observations
do not measure allocated disk-space recovery. Disk bounds are monitored,
not filesystem quotas. Independent pools and external host caches remain outside
this accounting. The accepted release ZIP and original execution config hashes
are unchanged.

## Retirement and demonstrated repairs

Receipt phase is retired, scratch is absent, reservation is released and the
active marker is absent. Full retained logs and output hashes are referenced
by attempt-ce62387adceb40ab8bf31268a7964abd.json. The observer returned one
terminal view; it started zero model requests. The task's workers made no model
calls. Parent/review cost and a matched-outcome efficiency comparison are not
qualified by this record.

Real execution found and repaired unnecessary release-directory permission in
export-pack, deletion of the permission-bearing export root, missing root-link
refusal, and disposable fixture ACL/readonly teardown incompatibilities. Every
failed attempt remains recorded. Pending recovery prevented further ordinary
allocation. Recovery removed only an exact verified empty fixture under its
creating identity, then the existing owner retired scratch. No machine ACL,
account, quota, clone, worktree or storage-layout changes were made.

The wider reported disk mess has not been reclaimed by this task. Unknown and
unique work remains preserved. Whole-session permissions, general private-ACL
tool cleanup, shared policy enforcement across legacy/unmanaged runners,
protected Git operations, hard capacity boundaries and actual model efficiency
remain open. Do not call the whole environment contained or the problem fixed.
