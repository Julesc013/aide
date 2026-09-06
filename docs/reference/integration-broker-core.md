# Local integration broker foundation

Task: AIDE-CW-INTEGRATION-BROKER-01. This is an implementation slice, not completion of the full protected broker or isolated-host tasks.

The package `core/runtime/integration_broker` provides a frozen candidate producer and an independently durable broker state machine. It never installs a service, provisions an identity, contacts GitHub, invokes a model or opens credentials. The production CLI has no transport configuration or plugin loading; `apply` refuses because production integration transport is not implemented or qualified.

## Frozen content

`freeze_candidate(git, workspace, exchange, repository=..., base=..., allowed=...)` observes an exact SHA-1 Git base and emits a random bundle identifier plus canonical manifest digest. The exchange root must be outside the worker workspace.

The manifest records the repository, base commit/tree, candidate Git tree, admitted paths and complete regular-file entries: mode, Git blob identity, SHA-256 and byte length. Content blobs carry real bytes, including binary and untracked files. Deletions are represented by their absence relative to the base tree. Existing executable modes are preserved; new files are regular 100644 files on the Windows host. Staged index changes, symbolic links, junctions, gitlinks, unsafe Windows names, directory case aliases and protected-path changes are refused. This slice deliberately does not accept staged mode changes or arbitrary Git metadata mutation.

Bounds are 4,096 files, 16 MiB per file, 64 MiB total payload and 240 characters per relative path. Git runs through the existing bounded Windows Job host, with hooks, file-monitoring and global/system configuration disabled. No Git filters or checkout hooks participate in materialization.

All candidate bytes, file lists, HEAD and index observations are rechecked before bundle publication. The broker reads and verifies the frozen bytes again for every request. It materializes a new bare object database under its state root and verifies `write-tree` against the manifest. It does not copy later worker changes or stage the worker's index. Failed or interrupted materialization retains its reservation and partial artifacts for diagnosis.

A frozen content tree is distinct from the continuous worker's v0 snapshot identity, which includes original HEAD/index/control metadata.

## Broker requests and authority

`Broker(root, exchange, repository_root, git, authority)` exposes `prepare(request)`, `query(request)` and `apply(request)`. Roots must be disjoint; exact executable bytes and protected configuration are explicit inputs.

The v1 authority record binds repository, exact `refs/heads/dev` target, actor, base commit/tree, expiry, one or two lifetime requests, required check names, admitted paths, admission digest and independently reviewed verification digest. A request binds that authority digest, task, frozen bundle and verification record. Verification names separate coding/assurance sessions, passing assurance, the candidate tree and the exact passing check/artifact identities.

These structures verify consistency with externally supplied reviewed authority. A local hash alone cannot establish the authenticity of a human decision or independent reviewer. Protecting and qualifying authority/configuration sources remains required before operational activation.

The separate SQLite broker ledger uses WAL, FULL synchronous commits, immediate transactions and a unique unresolved repository/target writer. A unique task reservation prevents the same task being readmitted under another request digest in that ledger. Completed requests still consume the lifetime request budget.

State progresses through reserved, prepared, apply_intent and integrated. A persisted intent precedes transport dispatch. A lost result never permits repeating apply; only a subsequent observation can close the transaction. An absent remote observation after intent remains pending. Partial preparation is retained rather than automatically deleted or treated as complete. Expiry stops new effects but does not prevent observation of an already uncertain effect.

Integration receipts bind request digest, repository, target, actor, base, candidate tree, actual integrated commit/tree and required-check digest. This slice requires the integrated tree to equal the candidate tree; it never silently rebases reviewed work. Production transport must additionally enforce the actual remote base/checks/actor at its effect boundary and return authoritative observations.

## Local invocation

From a trusted checkout, `python -B -m core.runtime.integration_broker query --config <absolute-file> --config-sha256 <exact-byte-sha256>` reads one bounded JSON request from stdin. The config schema is `aide.broker.config.v1`, containing state_root, exchange_root, repository_root, git executable/hash and authority. Duplicate JSON keys, unknown fields and mismatched config bytes refuse.

The CLI cannot select the internal transport test seam. `apply` refuses until a separately implemented and qualified production transport is wired. No example receipt or fixture can enable it.

The v0 continuous worker is intentionally unchanged in this foundation. Coordinator-v1 export, request/receipt adoption and pinned-entrypoint integration are required next work under this same broker task, with fresh tests and source assurance. The old pin is not a permission gate or a reason to leave that implementation unfinished.

## Verification and remaining work

The scoped suite uses actual disposable local Git repositories and bounded Windows child processes for binary/untracked/delete/mode round trips, immutable handoff behavior and moved-base refusal. Durable tests cover concurrency, failed intent commits, process death, lost replies, absent observations after intent, budget/expiry refusal and corrupt receipts. Remote integration observations are explicitly injected fixtures; their passing results do not prove real GitHub effects.

WindowsJobHost remains process containment only. It launches under the existing Windows user and does not implement credential/filesystem isolation, network denial or a volume quota. The controller, untrusted coding/tests/assurance and trusted integration broker still require separate qualified host boundaries. Production PR/check enforcement, transport recovery, coordinator-v1 wiring and the real two-task demonstration remain open.

## Required next implementation under this same task

The reviewed foundation is not yet usable for the actual AIDE repository: its complete-tree handoff limit is 4,096 entries, while the current repository has 10,631 tracked files. Implement a bounded change-set handoff over trusted base Git objects; do not raise the entry budget or claim actual-repository readiness from small fixtures.

A process death after reservation but before prepared leaves a retained reserved writer. Add object-bound preparation recovery or an explicit safe repair operation, plus kill-before-prepared tests. Do not automatically delete an uncertain materialization directory, repeat remote apply, or treat lease expiry as ownership. Until then, interrupted preparation requires diagnosis and prevents unattended resumption.

Then wire coordinator-v1 frozen export/request/receipt adoption, with fresh tests and source assurance. These are authorized engineering work and are not new permission gates. Actual production transport and isolated-host qualification remain open.
