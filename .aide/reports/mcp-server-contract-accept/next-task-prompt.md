# Next Task Prompt

```text
# AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01
# Minimal Contract-Only A2A Agent Card Projection

Create and process AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01.

Use .aide/queue/index.yaml as canonical queue truth. Re-read the live repository before writing anything.

Required baseline:
- AIDE-ACCEPT-MCP-SERVER-CONTRACT-01 exists.
- Its result is ACCEPTED_WITH_WARNINGS or ACCEPTED.
- Its evidence reports missing_evidence: 0.
- It recommends AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01.

Goal:
Build a deterministic, contract-only A2A agent-card projection for AIDE.

Allowed capability:
- static A2A agent-card representation, projection, structural validation, inspection, and reporting.

Non-capabilities:
- no live A2A endpoint;
- no agent registration;
- no task delegation;
- no authentication;
- no worker execution;
- no provider/model/network call;
- no Host Contract;
- no Dominium Bridge;
- no Workbench;
- no Runtime or Service;
- no PatchTransaction apply;
- no branch/worktree, GitHub, release, promotion, or target-repository mutation.

Stop at needs_review and recommend AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01.
```
