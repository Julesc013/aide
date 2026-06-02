# Remaining Risks

- X-OS-02 requires human review before acceptance; status remains `needs_review`.
- Capability reports are source-side evidence only. Target repositories must generate their own capability reality reports after import.
- The export pack records dirty-source provenance until this X-OS-02 commit is created; checksum and boundary validation pass.
- Harness v0 still reports the pre-existing stale `.aide/generated/manifest.yaml` source fingerprint.
- `route explain` reports an advisory token budget warning and quality-gate warning, but verifier and golden status are PASS and no provider/model/network calls occurred.
- `git plan` records the expected dirty-tree advisory blocker before the X-OS-02 commit; it was run as dry-run/report-only and performed no branch, remote, worktree, or target mutation.
- One non-blocking overclaim record remains as a wording review for `capability_reality_ledger`; no blocking overclaims were detected.
- No apply-capable Task OS behavior, target mutation, branch mutation, release publication, provider/model calls, network calls, scheduler, worker, Runtime, host, UI, Gateway forwarding, MCP/A2A, or app-surface work was implemented.
