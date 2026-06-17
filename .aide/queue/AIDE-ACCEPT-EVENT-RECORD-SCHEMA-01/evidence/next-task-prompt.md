# Next Task Prompt

```text
# AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01
# Deterministic OKF-Compatible AIDE Knowledge Bundle

Create and process AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01.

Use .aide/queue/index.yaml as canonical queue truth.
Treat .aide/context/latest-task-packet.md as potentially stale unless current repo policy explicitly says otherwise.

Goal:
Implement a deterministic, read-only OKF-compatible AIDE knowledge bundle projection over current accepted and needs-review AIDE protocol work.

This is a knowledge projection slice, not runtime.

The bundle must follow OKF-style minimum shape:
- markdown files
- YAML frontmatter
- non-empty type field for every concept document
- index.md
- log.md
- standard markdown links
- file-based, human-readable, agent-readable knowledge

AIDE boundary:
- Protocol executes.
- Evidence proves.
- References identify.
- Events remember.
- OKF knowledge explains.

OKF pages must not become execution authority.

Use accepted ReferenceID and EventRecord refs where practical.

Implement only:
- deterministic OKF projection helper
- minimal validation/lint
- thin CLI dispatch if consistent with repo style
- reports
- tests
- queue evidence

Initial pages should include at least:
- index.md
- log.md
- current-state/queue.md
- current-state/review-gates.md
- current-state/stale-latest-task-packet.md
- current-state/next-work.md
- protocol/envelope.md
- protocol/evidence-packet.md
- protocol/workunit.md
- protocol/worker-run.md
- protocol/testjob.md
- protocol/reference-id.md
- protocol/event-record.md
- capabilities/minimal-contract-envelope.md
- capabilities/minimal-evidence-packet.md
- capabilities/minimal-workunit-queue.md
- capabilities/minimal-worker-run-schema.md
- capabilities/minimal-testjob-schema.md
- capabilities/minimal-reference-id-scheme.md
- capabilities/minimal-event-record-schema.md
- decisions/protocol-vs-knowledge.md
- decisions/repo-contract-vs-runtime-state.md
- decisions/okf-as-knowledge-plane.md
- risks/stale-latest-task-packet.md
- risks/acceptance-gate-debt.md
- risks/overclaiming.md

AIDE-specific frontmatter fields:
- aide_uri
- aide_status
- aide_review_state
- aide_validation_state
- aide_acceptance_state
- aide_capability_label where applicable
- explicit_non_capabilities where applicable
- generated_from
- source_refs
- evidence_refs where available
- source_hashes where cheap and deterministic
- event_refs where available

Non-goals:
- no runtime
- no event sourcing runtime
- no append-only event store
- no Reconciler
- no CapabilityManifest
- no ConformanceProfile
- no PatchTransaction
- no AdapterManifest
- no ContextPack v2
- no Service
- no Commander
- no provider/model calls
- no network
- no target repo mutation
- no active apply
- no branch/worktree automation
- no broad LLM-authored wiki
- no conversion of protocol truth into markdown authority

Validation:
- OKF structural validation
- frontmatter parse validation
- every concept has non-empty type
- index/log generated
- source_refs exist or are reported as warnings
- evidence_refs exist or are reported as warnings
- aide:// refs parse where present
- event refs parse where present
- pages do not overclaim accepted capabilities
- EventRecord is classified according to its exact current acceptance state
- stale latest-task-packet ambiguity is surfaced
- existing protocol commands remain compatible
- focused tests pass

Stop at needs_review with evidence.

Recommended next task:
AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01.
```
