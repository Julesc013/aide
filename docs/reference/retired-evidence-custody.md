# Retired evidence custody

This is an administrative job-storage operation for complete evidence already
collected and retired by AIDE. It does not grant workers access to protected
storage, hard-limit a filesystem, contain the outer client or inventory drives.

`job custody plan --config <selected-local-config> --job-id <id>` produces an
exact plan digest. The selected configuration must contain a finite scoped
aggregate ceiling. The default view is compact; `--full` prints the complete
plan for retained review evidence. Plans admit only ordinary single-link files from owned,
quiescent, fully collected retired jobs. The receipt and owner files remain at
their original locations, byte-for-byte unchanged. The complete logs/output
map includes empty directories, original hashes and both collection digests.

`job custody apply ... --expect-plan <digest>` is a consequential effect. It
requires the exact applicable queue/effect review. Under the existing estate
lock, it reserves worst-case archive staging plus four MiB of metadata before
writing a durable custody intent in `control/active.json`. Existing pinned job
owners already refuse allocation while that latch exists. Custody never starts
a replacement job. The configured aggregate ceiling and disk headroom remain
unchanged. Limits are cooperative admission, not a hard storage quota.

The archive and manifest are verified completely before raw-copy retirement.
There must be actual net logical savings. Every original evidence byte remains
in `retained/<id>/custody.zip`; `custody.json` explicitly maps the old member
paths and records receipt/archive identities. Unknown or changed members,
redirected paths, active jobs and stale plans are refused. Raw evidence is
unique required proof; it is never classified as disposable because it is old.

`job custody recover ... --expect-plan <digest>` reconciles that exact pending
operation. Interrupted partial archives can be replaced only after the complete
original raw snapshot is reverified. A verified archive is reused while each
remaining raw member is checked. A cleanup failure leaves the reservation latch
in place and stops further allocation. Ordinary `job recover` is not the custody
recovery command; it refuses the custody schema.

`job custody verify ...` verifies every archived member without extraction.
`job custody read ... --member output/<name> [--sha256 <original-sha>]
[--offset <bytes>] [--limit <bytes>]` resolves raw or custodied evidence and
returns a bounded base64 slice, original digest and byte count. The default is
2048 bytes; maximum65536. No arbitrary extraction destination, automatic full
restore, fallback pool or evidence truncation is provided. Original raw path
references should be resolved through this interface after a reviewed custody
transition; plain filesystem consumers do not transparently decompress them.

At most16MiB of original evidence and4096 entries are eligible per operation.
Intent/manifest JSON is limited to1MiB; archive writes and expanded verification
are bounded independently. Source/receipt digests detect drift, not authority.
The executing pinned owner is selected before custody uses its guards and lock.
The new custody implementation itself requires exact source/effect qualification.
Cooperative single-writer protection does not prevent another unrestricted
process from changing paths. No claim of whole-machine cleanup follows.

Current implementation and qualification state is recorded in
[the custody WorkUnit](../../.aide/queue/AIDE-RETIRED-EVIDENCE-CUSTODY-01/ExecPlan.md).
The stable consumer matrix and unrelated release/host/model gates are unchanged.
