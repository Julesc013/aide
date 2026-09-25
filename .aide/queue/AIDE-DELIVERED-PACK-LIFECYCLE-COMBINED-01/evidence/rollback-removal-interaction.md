# Rollback/removal interaction repair — source checkpoint

## Exact inputs

- Combined branch ancestry before this edit: merge `03f4b0a1ef375c5f7b2cb78208aabdb3056690d5`
  with parents `f2be45ea13ceadca6be476a2a99417101c8a00c9` and accepted
  rollback source `33824b369b844b1c7a4304844838bcb424806131`.
- Rollback source independent ACCEPT: external
  `D:\Projects\AIDE\_review_scratch\rollback-33824b36-independent-rereview.md`,
  SHA-256 `80137fae70ed0f30a93ce26ce5391c1efab5d303ddf8b315ff884a78dbc93082`.
- Current dev removal-intent loader and import effect-time guard were retained
  in the automatic code merge; only queue index, `PLANS.md`, and `IMPLEMENT.md`
  had textual conflicts, resolved by preserving both streams' appended records.

## Characterization and repair

The added Windows regression installs v1, updates to v2, then begins a real
receipt-owned removal. Before repair, rollback preview reached the underlying
import guard and raised `portable removal recovery must complete before import`
instead of recognizing its own pending-removal dependency. Red command:
`py -3 -B -m unittest discover -s .aide/scripts/tests -p test_export_import.py -k rollback_refuses_pending_removal`;
1 test, FAIL in 33.852 s, exit 1, log
`D:\Projects\AIDE\_review_scratch\rollback-removal-intent-red.log`, SHA-256
`82dee6770d27f05b7fbfa214679dd5ad3afd27d65a211a2c102ba4e8ae53a299`.

`build_portable_rollback_plan` now validates removal intent immediately after
target normalization/existence and refuses rollback before interpreting import
intent or receipt. The regression covers a pending intent with receipt, a stale
rollback preview, malformed intent, and pending intent after receipt retirement.
It asserts receipt/intent bytes remain unchanged on refusal. The same command
then passed 1 test in 45.495 s, exit 0, log
`D:\Projects\AIDE\_review_scratch\rollback-removal-intent-green.log`, SHA-256
`af4d12a1ecc9d91cb82e0f5942c797d5a6343502a7e98315db912cfe4aa0e870`.

Interim source SHA-256 `e76218d4234ada95cfa6ec790faffb1eb1e40fd323c28cdd4cce8a51578bc705`;
test SHA-256 `92cdb181c0bdf28f4ee1a3a5136222e29475e5f593ec7a81f90d4161d1d0eeb5`.
`git diff --check` passed. Full importer, canonical validation, generated
artifacts, extracted consumers and independent combined review are still open.
No `dev`, remote or real-target effect occurred.

## Removal source dependency

Frozen `d5b44626` received REQUEST_CHANGES (report SHA-256
`38876eb382b6e8115599365d0b8703ae8782fafdb3d79b419b310a0138e3392a`).
Superseding `2c4c9089` received independent ACCEPT_WITH_NOTES for source
combination (report SHA-256
`98c58303a5ce4e2e042515661b5763e0898c3cce5049436dc50c2af872a8b664`).
Neither verdict is artifact or `dev` acceptance.
