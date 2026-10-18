# Actual predecessor recovery: preserve the supported target states

Read-only /root/review_disked_continuation contract review recommends the existing
supported recovery route, not a new automatic downgrade promise. Published 1.0.0
already restricts rollback to equal safe payload path sets. See
`docs/reference/cross-repo-pack-export-import.md` and
`portable_rollback_receipt_baseline()` in `.aide/scripts/aide_lite.py`.
The actual archived pair has 818 then 826 safe targets: eight additions, no
removals. The private effort module and seven test modules are added; the core
module is excluded from safe import. This is distinct from the original same-path
rollback consumers, which retain every assertion and now pass on the new archive.

| Actual target state | Required observation |
| --- | --- |
| Completed actual upgrade, differing path sets | Public rollback preview/apply refuse with the specific path-set reason and no changed target byte. This is not successful rollback. |
| Interrupted ordinary or resolved upgrade | Retain the original attempt; refuse ordinary replay, wrong digest or changed resolution; recover using original exact inputs and preserve project controls. |
| Completed update with unchanged receipt-owned files, no overlay/disabled feature | Explicit exact removal preview/apply can detach fully; then safe-install the published predecessor. Verify all eight added paths are gone, original owned payload restored, project bytes and authored guidance preserved, and predecessor receipt correct. |
| Conflict-resolved overlay with project controls | Preserve the overlay and disabled features. Removal preview identifies protected ownership. Do not apply detach/reinstall, clear receipts or rewrite the overlay to force success. Manual reconciliation remains required. |

The review requires these states to be reported separately. It does not authorize
execution. A broader promise of automatic rollback across additions or complete
overlay downgrade recovery would require separately admitted product work.
This qualification retains all mandatory original forms and same-path rollback
behavior. The explicit removal/reinstall sequence must pass before it is claimed.
