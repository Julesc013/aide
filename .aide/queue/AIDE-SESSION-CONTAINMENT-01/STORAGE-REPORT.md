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
A fresh-stat correction is being qualified only against three tiny owned
fixture files; the target will not be reread.

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
