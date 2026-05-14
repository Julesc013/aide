# Q36 Prompt Normalization Report

## No Raw Intent Execution Guarantee

Q36 compiles prompts only. It does not run the requested task, mutate branches,
push, merge, prune, create tags, publish releases, create GitHub workflows,
call GitHub APIs, call providers/models, perform outbound network calls, mutate
target repos, or write `.aide.local/`.

Every compiled packet records:

- raw prompt SHA-256 hash;
- bounded excerpt;
- interpreted goal;
- task/risk/size classes;
- safe execution flag;
- blocked and split state;
- rejected interpretations;
- repo and branch refs;
- validation and evidence hints;
- draft WorkUnit fields.

## Prompt Cases

| Prompt | Result |
| --- | --- |
| `next` | context / low / audit_only; safe only as queue/latest-task inspection. |
| `fix everything` | repair / high / split_required; not directly executable. |
| `clean up the repo` | refactor / high / split_required; inventory/classification first. |
| `delete old XStack stuff` | refactor / destructive / blocked; direct deletion rejected. |
| `merge dev to main` | git / release / blocked; requires branch/promotion policy evidence. |
| `publish a release` | release / release / blocked; requires release gates and approval. |
| `install AIDE into Dominium` | install / external_side_effect / two_shot; target preflight first. |
| `make it production ready` | audit / release / split_required; readiness audit first. |
| `repair failing test` | repair / medium / one_shot; targeted validation expected. |
| `move all roots into clean layout` | refactor / destructive / split_required; root inventory/recycling framework first. |

## Rejected Interpretations

Q36 rejects these interpretations for unsafe prompts:

- do not execute raw prompt directly;
- do not invent product work from `next` or `continue`;
- do not treat broad cleanup as permission to move/delete roots;
- do not delete XStack or other legacy systems without inventory and salvage;
- do not merge, push, promote, prune, or publish without branch/release gates;
- do not install into Eureka, Dominium, or any target repo from AIDE-local state;
- do not treat artifact existence as behavior proof;
- do not bypass queue, branch, evidence, or review policy.

## Deterministic Limits

The classifier uses phrase and policy heuristics only. It does not perform LLM
semantic inference, embeddings, vector search, live repo intelligence indexing,
or provider/model routing.
