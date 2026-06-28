# AIDE Self-Consumer Fixture v0 Status

Result: `PASS_WITH_WARNINGS`

Proposed capability: `aide_self_consumer_fixture_v0`

Scenario count: `9`

The fixture proves the shape of an AIDE-like installed target without treating the AIDE source repository as that target.

Accepted proof areas:

- fresh install
- profile generation
- upgrade from previous version
- same-version idempotence
- target-owned-state preservation
- rollback
- uninstall
- offline operation
- source repository confusion refusal

This is a fixture/proof surface only. It does not authorize real target apply, source repo apply, project canaries, release publication, provider/model/network calls, or branch/worktree automation.
