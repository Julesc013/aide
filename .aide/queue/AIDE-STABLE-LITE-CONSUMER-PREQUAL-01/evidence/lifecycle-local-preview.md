# Delivered Lite Windows lifecycle local preview, 2026-09-25

## Exact input and execution

- Pinned local preview ZIP: `D:/Projects/AIDE/aide/.aide/release/dist/aide-lite-pack-v0.zip`,
  SHA-256 `8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6`.
  Its manifest declares source commit `8365aa61b7cad51d542f88434e50bc33c5aac8fe`.
  The archive remains `preview_only`/`no_publish`; the declaration is not
  independent source provenance.
- External canary `D:/Projects/AIDE/_review_scratch/stable-lite-lifecycle-canary/canary.py`,
  SHA-256 `08ab80da60664556f16d9ba63ce9ba08f24060327de1316dad0a80ce4118dfb1`.
  It pins an external extraction/fixture helper by SHA-256
  `3f3140807520b1481181c34e95e06273e2774698cf2d384e42b5b6214f58a181`.
  The external PLAN SHA-256 is
  `b3770f935deec63292b5b5209bfc4032cf3e8f08043ca59c6b3b9a59a48d9c99`.
- Passing run: external `stable-lite-lifecycle-canary/run-20260925-second/summary.json`,
  SHA-256 `c4ccb79706c0e5d7d7cd8fc511e2fd8175c89c8cf1fcd968ca0ef9ac827fe2cd`.
  Invocation log SHA-256
  `1c8b02f7ea65fcfea88e375124c324e16e529de00f1a291b59a318fed06660fd`.
  The script exited 0 and recorded 31 delivered CLI invocations. A controller
  check independently recomputed all 31 command-log hashes and exit codes;
  mismatches: zero. The run has no `failure.txt`.

## Observed behavior

- Receipt-owned missing file repair restored exact bytes. A wrong plan digest
  refused without mutation; a rival file at the same path caused conflict
  refusal and was preserved.
- A documented post-write API interruption retained repair intent. A new
  delivered CLI process refused ordinary preview until recovery, then returned
  `RECOVERED` for the original digest and cleared the intent.
- Import of exact V1, update to a checksum-valid **synthetic disposable V2**,
  then rollback to exact V1 returned `ROLLED_BACK`; wrong-plan refusal caused
  no mutation. Authored CRLF guidance and project data survived. This does
  not prove a published predecessor/successor pair.
- Fresh and authored brownfield targets returned `DETACHED`. A changed
  receipt-owned file returned `PARTIAL_REMOVAL`, preserving that edit, the
  receipt, and the recovery runner.

## Preserved failure and evidence correction

The first run under `run-20260925-first` exited 1 when its pinned helper's
180-second subprocess limit expired during a later full import. Its failure
trace SHA-256 is
`bbe6da692968ec9ae3306a75935858fa2ca842342a86c46e52a88a46e09e5d5b`;
the first invocation log's **actual** SHA-256 is
`cab8d5ae5ea79db5220a9b12e00ac5db8b7fa0e0b901597a38e78fa1923bc30c`.
The frozen external PLAN truncates that hash. Preserve
the original PLAN and this explicit correction. The first disposable import
intent was not replayed; the passing run used a fresh target and a 900-second
per-command limit. No product failure follows from the helper timeout alone.

## Limits and next gate

This is local Windows archive prequalification, not a published release or
downloaded-byte consumer. The synthetic V2 is a fixture; `network_calls: none`
in CLI output is a declaration, not an OS network trace. Native/hosted broker,
restricted principal, real version-pair, final artifact, and publication
acceptance remain separate. An independent Codex reviewer issued
`ACCEPT_WITH_NOTES` for the exact second run in external
`stable-lite-lifecycle-canary/independent-review.md`, SHA-256
`ddb9dbf66ff59885279ee6f0ef2595019ff84ae04830edbb8f35a67018c30b71`.
The reviewer rechecked the archive and all command logs read-only, and
independently inspected target poststates. Its notes are nonblocking for this
bounded local preview only: the first-run PLAN hash typo is corrected above;
wrong-plan snapshots were asserted in the script but not serialized; offline,
hostile concurrency, real version pairs and public bytes remain unqualified.
