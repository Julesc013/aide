# Warning Dispositions

Accepted warning debt:

- The self-consumer fixture is static fixture/proof evidence, not real target update authority.
- `distribution-apply status`, `distribution-apply plan`, and `distribution-apply verify` still expose stale build-era routing/status text for the self-consumer fixture.

Disposition:

- These warnings are non-material for accepting `aide_self_consumer_fixture_v0`.
- Boundary flags still report fixture-only, temp-workspace-only, no real target apply, no source repo apply, no release publication, no provider/model/network calls, and no branch/worktree automation.
- The stale routing/status text should be repaired next as operator-facing text debt.

Recommended next task:

`AIDE-BUILD-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01`
