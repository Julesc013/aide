# Release-effect WorkUnit admission — 2026-09-28

Controller scope review: the owner delegated bounded child admission and
qualified AIDE-scoped dev/main/release effects on 2026-09-25. This child is
limited to the local Windows Lite stable release contract and exact effects in
`task.yaml`; it does not admit native/hosted agent operation or arbitrary
target mutation. It reuses the two existing checkouts and the owner-selected
shared D runner roots. One intensive job at a time.

Dependency: independent `/root/lite_preview_review` returned
`ACCEPT_WITH_NOTES` for the local preview exact commit
`4dcd896b4a9b65ef2bf6e8ecbbd7f60809560637`, tree
`b8ae4507d6e002c8fcb4fe77b52ca4b913cc36fe`. Its custody and note
dispositions are in the predecessor WorkUnit. Admission creates no stable
release acceptance or external effect.

At admission, local and remote `dev` both read `4dcd896b`; remote `main`
read `aec53b1d`. Read-only `git ls-remote --tags origin` and
`gh release list --repo Julesc013/aide --limit 5` returned no entries on
2026-09-28. Recheck at freeze; the conditional `1.0.0` first-release rule is
not yet an assigned version or tag. The Q47/Q48 outputs are preview-only and
remain unchanged. The current Git tree has no new physical workspace.

Next executable work: classify installed validation/context warnings and
define the truthful Windows Lite profile; then implement and test a distinct
non-preview stable subject using the current AIDE generator and D runner.
