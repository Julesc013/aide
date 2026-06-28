# Prompt

Create and process `AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01`.

Repo truth outranks this prompt. Inspect the live checkout before acting.

Mission: build an AIDE self-consumer fixture v0 proving the shape of an AIDE-like installed target without treating the AIDE source repository as the target.

The fixture must cover:

- fresh install;
- profile generation;
- upgrade from previous version;
- same-version idempotence;
- target-owned-state preservation;
- rollback;
- uninstall;
- offline operation;
- source repository is not installed target.

Authority: build fixture/proof surfaces only. Do not implement real target apply, source repo apply, project canaries, release publication, provider/model/network calls, branch/worktree automation, the independent check, or acceptance.
