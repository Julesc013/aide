# Next Task Prompt

```text
AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01

Independently check AIDE-DOMINIUM-INTEGRATION-CHARTER-01.

Do not implement anything.

Use .aide/queue/index.yaml and the charter task packet as canonical AIDE truth.
Read the live AIDE and Dominium inputs pinned by the charter. Verify that the
charter is planning-only, source-faithful, non-mutating, and does not implement
or authorize Host Contract, Dominium Bridge, Workbench, runtime, service,
provider, worker, transport, command invocation, PatchTransaction apply,
repository mutation, branch/worktree automation, GitHub mutation, release, or
promotion.

Validate:
- required queue surfaces and reports exist;
- JSON parses;
- Dominium input hashes and queue facts are accurately recorded;
- every shared concept has one semantic owner;
- generated projections are not canonical;
- namespace ownership is explicit;
- refusal, diagnostic, evidence, event, transaction, and compatibility mappings
  are coherent;
- critical path and task-dependency graph are acyclic;
- task IDs are unique and dependency refs resolve;
- mutation tasks have trust and preview prerequisites;
- parallel lanes are read-only;
- no Dominium or sibling-repo files changed;
- no downstream queue directories were materialized.

Stop at needs_review. Recommend only AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01
if the check passes with warnings.
```
