# Current Lite removal interruption qualification

Three necessary local consumer checks passed once on frozen source
`3460ba7a80b515495a58b325d7f64b0abc050fb9` / tree `704040e3bbb22945ecc49d1642d2fe860694f208`
and current ZIP `4a45922b1dc09cf5073c0968fd016d008cb7bc924c2905efe526ffe11f95dab0`. Exact independent preexecution
ACCEPT_WITH_NOTES had no blocking findings; its notes were disposed before
dispatch. Postexecution technical/source/ref acceptance is separate.

| Owned-file boundary | Actual job | Peak scratch bytes | Peak memory bytes | Retained logical bytes |
|---|---|---:|---:|---:|
| 0 | `3a77da5f88864f8291d1df6d8fb1bd98` | 8,329,339 | 261,468,160 | 6,817 |
| 1 | `2d2a183287e14d8387935fb836a077c0` | 8,329,339 | 262,066,176 | 6,819 |
| 50 | `eee07b9581a64391bf1c2731719fdfa9` | 8,329,339 | 261,795,840 | 6,891 |

Boundary0 exited77 after durable intent and before the first eligible unlink:
all815 managed files retained their hashes. Boundaries1/50 exited77 after the
matching eligible owned-file deletion. Each preserved intent/receipt, resumed
the same plan through a fresh delivered CLI to DETACHED, removed the remaining
owned paths and preserved authored AGENTS and project-owned content.

Every receipt/output/log digest was independently recalculated by the
controller; all jobs report retired, scratch absent and reservation released.
Full summaries/receipts/logs stay at their recorded D retained locations.
[Verification JSON](current-removal-verification.json) records their exact
identities and [admission](current-removal-admission.json) records the reviewed
subject/effect and effective ignored manifest hashes. Ignored native and
verification logs remain available in this directory. No uncertain replay.

All four immutable assets, original a241 configuration and24 supervised
dependencies remain unchanged. Existing D roots were used; temporary51c4
selection changed only scratch8->16MiB and logs6->1MiB. The unchanged256MiB
aggregate boundary is cooperative admission/monitored growth, not a hard quota.
Retained data across these three jobs totals20,527 logical bytes; this is
not a whole-campaign or allocated-space total. No canonical output, real-target
mutation, extra checkout or model request was authorized by these checks.

Earlier0/1/50 records identify older ZIPs and remain preserved. Current eight
consumer cases,49 affected source checks and unchanged71 core/host checks are
reused, not relabelled as rerun. These three jobs supplement the receipt-exit
case; no archive regeneration or broad suite repetition was required.

Outer-client/editor/read containment, ten historical dispositions, live model
permission, matched accepted-outcome efficiency, exact first-stable release
ACCEPT/tag/publication/downloaded consumers, authorized downstream adoption
and wider unknown disk cleanup remain unfinished. FacMan product work is
paused. The [full programme report](../../AIDE-ARCHITECTURE-RECONCILIATION-01/REPORT.md)
and [current asset report](../../AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/REPORT.md)
retain the broader scope and candidate roadmap.

Owner-directed source-only synchronization is separately reviewed against
[the exact three-ref effect](current-removal-source-sync-effect.json). Its
observed final identity is written after the effects to
`current-removal-final-sync.log`; this report does not invent its own commit ID.
