# AIDE Apply Core

This package contains standard-library helpers for AIDE apply planning records.

AIDE-APPLY-01 adds `managed_sections.py`, a fixture-safe parser and patch
planner for explicit generated-section markers. It preserves manual text outside
markers and blocks missing, duplicate, nested, malformed, binary, or ambiguous
marker cases. It does not expose real repository apply behavior.

AIDE-APPLY-02 adds `transaction_executor.py`, a scoped transaction executor v0
for explicit plans, explicit allowed paths, managed-section updates, preimage
hash checks, postimage verification, staged-change records, rollback-compatible
records, dry-run/report mode, and review-gated apply mode. It does not authorize
install apply, upgrade apply, repair apply, rollback/uninstall apply, target repo
mutation, branch/worktree mutation, provider/model calls, Gateway calls, network
calls, release publication, or broad active-repo apply.
