# Bounded storage custody result (2026-10-05)

One previously ranked Universal linked worktree was inspected through the
pinned Windows managed owner. It has **three modified tracked source files**
and must be preserved. No target file was edited, moved or deleted. This is
a bounded local finding, not an inventory or reclamation of the reported500GB.

| Observation | Actual result |
|---|---|
| Worker | BLACKGLASS-WIN1\CodexSandboxOffline |
| Target/master identity | Recorded Git pointer/common root verified; heads unchanged during observation |
| Logical metadata |801 entries,681 files,7,794,943 bytes |
| File state |3 modified tracked paths;0 untracked names;31 ignored bytecode names |
| Other writers / allocation / reclaimable bytes |Unknown / unknown / unknown |
| Reclaimed |0 bytes; no deletion |
| Job scratch peak / retained |17,806 bytes /21,802 logical bytes |
| Process-memory peak |81,956,864 bytes |
| Retirement |Output/log digests verified; scratch absent; reservation released |

Raw unique-byte and shared-name fields are excluded: Windows caches zero
identity/link fields in DirEntry.stat. The corrected verification retains them
as unknown; the original result and its failure remain unchanged. See
[Python documentation](https://docs.python.org/3/library/os.html#os.DirEntry.stat).
The fresh-stat correction passed one native three-file fixture:9 logical
bytes,6 bytes across distinct identities,2 shared names. Its guarded alias
retired before strict owner collection. Both output/log digests verified;
2,424 peak scratch bytes and35,217,408 peak memory bytes; scratch/reservation
retired. No target reread occurred. Actual target unique/link counts remain
unknown. See [fixture verification](evidence/storage-identity-verification.json).

The existing D pools, original execution selection,24 runtime pins and current
Lite assets remain unchanged. Cooperative256MiB admission and monitored growth
are not hard disk quotas. Outer shell/editing/plugin routes remain unrestricted;
read isolation is unqualified. This grants no cleanup, release, historical
disposition or nested model authority. FacMan product work remains paused.

Exact details: [verification](evidence/storage-custody-verification.json),
[preexecution acceptance](evidence/storage-probe-acceptance.json), and
[ExecPlan](ExecPlan.md). Full bounded raw metadata and logs remain at the
verification's retained locators. Current Lite qualification and remaining
release/efficiency gates: [current report](../AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/REPORT.md).


Changed files include the two task-local diagnostic/fixture scripts, SESSION
task/ExecPlan/report/evidence, current qualification task/ExecPlan/report,
parent status, compact task packet and PLANS/IMPLEMENT/DOCUMENTATION indexes.
No core/runtime, release payload or specification requirement text changed
in this follow-up; the earlier architecture/spec reconciliation is preserved.

Verification commands:

- `py -3 -B .aide/scripts/aide_lite.py job run --config .aide.local/session-storage-probe-execution.json --manifest .aide.local/session-storage-probe-job.json`: PASS collected/retired; raw identity fields excluded.
- `py -3 -B .aide/scripts/aide_lite.py job run --config .aide.local/scoped-job-entry-01-execution.json --manifest .aide.local/session-storage-identity-job.json`: PASS native assertions/collection/retirement.
- `py -3 -B scripts/aide validate`: PASS149 info,0 warning,0 error (structural).
- `py -3 -B .aide/scripts/aide_lite.py pack-status`: PASS checksum/provenance/boundary.
- `py -3 -B .aide/scripts/aide_lite.py commit check --message-file <owned-message>` and `git diff --check`: PASS.

Fresh source synchronization and final actual-ref verification require their
separate accepted effect; final observation is retained in
[evidence/storage-final-sync.log](evidence/storage-final-sync.log).
