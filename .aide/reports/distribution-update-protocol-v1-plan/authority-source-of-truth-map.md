# Authority And Source-Of-Truth Map

| Surface | Authority |
| --- | --- |
| `.aide/profile.yaml` | AIDE source repository profile/contract truth. |
| `.aide/queue/**` | Queue execution truth. |
| `.aide/install/latest-*` | Source-repo install planning evidence only. |
| `.aide/repair/latest-*` | Source-repo repair planning evidence only. |
| `.aide/upgrade/latest-*` | Source-repo upgrade planning evidence only. |
| `.aide/rollback/latest-*` | Source-repo rollback planning evidence only. |
| `.aide/uninstall/latest-*` | Source-repo uninstall planning evidence only. |
| `.aide/release/dist/**` | Local release-bundle artifact evidence, not publication. |
| `.aide/release/github-release-*` | Local GitHub Release draft evidence, not GitHub state. |
| Target `.aide/memory/**` | Target-owned preserved state. |
| Target `.aide/queue/**` | Target-owned queue truth. |
| Target generated reports | Target-local generated evidence; regenerate in target. |
| `ProjectLock` | Target's selected distribution and component digests after accepted v1 build. |
| `OwnershipLedger` | Target path/section ownership truth after accepted v1 build. |
| `InstallRecord` | Observed installed result after accepted v1 build and future apply. |

The AIDE source repository is never treated as the installed target fixture.
