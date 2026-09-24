# Local integration broker and coordinator-v1 handoff

Task: AIDE-CW-INTEGRATION-BROKER-01. Checkpoint 7e4de0c9762ac89fa6c40fda64a33b0c6f471e93 preserves the independently reviewed foundation. Checkpoint f06bcd75aafeab175202a89ea1d69c815b7bd911 adds bounded changes over trusted base objects, interrupted-preparation recovery and coordinator-v1 protocol wiring. The current continuation adds prepared-effect validation, controller evidence capsules, finite delegated issuance and offline PR observation/intent modules. The complete protected broker, isolated host and live programme remain unqualified.

The package `core/runtime/integration_broker` never installs a service, provisions an identity, contacts GitHub, invokes a model or opens credentials. Production CLI `apply` has no transport configuration or plugin loading and refuses until a legitimate transport is implemented and independently qualified.

## Frozen content

`freeze_candidate(git, workspace, exchange, repository=..., base=..., allowed=..., checkout=..., max_total=...)` observes an exact SHA-1 Git base and returns a random bundle identifier plus canonical manifest digest. The exchange root is outside the worker workspace. Candidate v2 contains only changed regular-file entries and explicit null deletions; unchanged files remain in the exact admitted base tree. Complete-tree candidate v1 remains readable for existing foundation records.

Each changed file records mode, Git blob identity, SHA-256 and byte length, with real bytes including binary and untracked content. Existing executable modes are preserved; new files are regular 100644 files on the Windows host. Staged index changes, links/junctions/gitlinks, unsafe Windows names, case aliases, redundant changes, unknown deletions and protected-path changes refuse. The existing 4,096-entry and 64 MiB payload limits bound changed content, rather than every file in the repository. The per-file limit remains 16 MiB and relative paths remain limited to 240 characters. A coordinator can supply a smaller byte reservation.

Before coding, `literal_checkout` records a base-bound precondition that every tracked file exactly matches its Git blob bytes. A CRLF or filter-transformed checkout refuses explicitly; this slice never executes unknown attributes/filters or silently normalizes content. The coordinator persists that precondition before starting coding, and freeze requires it to match the admitted base metadata.

Freeze still inspects and rechecks every regular worker file, HEAD and index so hidden index flags cannot exclude changed bytes. Only changed blobs are published. The broker verifies the manifest and every changed blob again for each request, overlays the changes onto trusted base metadata and independently checks the resulting Git tree. Materialization creates a private bare database; its alternate points only to the admitted protected broker repository's object directory. Mutable worker objects never supply unchanged base objects. Git uses the bounded Windows Job host with hooks, file monitoring and global/system Git configuration disabled.

The trusted base object store must remain available and intact. Before preparation, bounded strict Git fsck verifies actual object integrity. Existing transitive alternates, promisor settings/packs and config includes refuse. Git replacement refs and every transport protocol are disabled; no lazy network fallback can repair missing objects. A frozen tree identity is distinct from the v0 coordinator snapshot identity, which also records HEAD/index/control metadata. No candidate record silently rebases reviewed work.

## Preparation ownership and recovery

The broker serializes preparation with its kernel-held supervisor lock. Each preparation generation has a durable SQLite intent before filesystem creation. Windows NtCreateFile with FILE_CREATE and FILE_DIRECTORY_FILE returns an exclusively created directory handle atomically. Directory-list access and omitted delete sharing prevent replacement while Git fills that directory; metadata-only access would not enforce that sharing rule. The lease establishes directory object ownership, not child-file or credential isolation.

A crash releases the process's handles. The next prepare for the identical reserved request allocates a fresh generation and rebuilds from frozen evidence. Prior directories and intents remain retained; recovery never deletes or reuses them based on path, timestamps, hashes or lease age. At most three generations are admitted per request, including generations interrupted before creation. Exhaustion refuses further preparation and retains evidence for diagnosis. Prepared state is recorded only after exact tree verification and a fresh base/expiry guard.

## Broker requests and externally issued authority

`Broker(root, exchange, repository_root, git, authority)` exposes `authority_observation(frozen)`, `prepare(request)`, `query(request)`, `apply(request)` and `reconcile(request)`. Its three roots must be separate. The authority record binds repository, exact refs/heads/dev target, actor, base commit/tree, expiry, one or two lifetime requests, required check names, admitted paths, admission digest and independently reviewed verification digest. Requests bind that authority digest, task, frozen candidate and independent coding/assurance sessions with passing check artifact identities.

Authority is supplied externally. `authority_observation` reports an already issued protected authority only when all frozen evidence matches; it cannot create review approval. Because future model session IDs and candidate trees are unknown at initial programme admission, an operational authority issuer must inspect their later evidence under explicit programme delegation. The coordinator cannot mint that authority or alter its own activation. The issuer source described below implements evidence-based finite issuance; its qualified host and operational transport wiring remain required implementation. These are distinct from a new user approval requirement.

The separate SQLite ledger uses WAL, FULL synchronous commits, immediate transactions and one unresolved writer per repository/target. A unique task reservation prevents readmission under another digest; completed requests consume the lifetime budget. State progresses through reserved, prepared, apply_intent and integrated. Apply intent precedes dispatch. Lost replies are reconciled by query only; absence after intent never authorizes blind replay. Expiry stops new broker effects but permits observation of an uncertain effect.

Receipts bind request digest, repository, target, actor, base, candidate tree, integrated commit/tree and required-check digest. The integrated tree must equal the candidate tree. Production transport must enforce actual remote base/checks/actor at its effect boundary and return authoritative observations; injected local receipts do not prove those effects.

## Coordinator v1

The explicit `aide.continuous-worker.activation.v1` schema adds registered authority/query/apply commands, an exchange directory beneath budgeted coordinator state, and exact pins for every broker module. Existing v0 activation remains an explicit compatibility path. Every runtime source change requires fresh pins and qualification; old hashes cannot authorize new implementation.

After coding, real validation and independent assurance, v1 freezes candidate bytes, stores the handoff in durable state and requests externally issued authority bound to that evidence. It validates authority scope, sessions, checks and programme bounds before persisting the exact broker request. Missing authority leaves the attempt pending. Before apply, the coordinator writes a semantic dispatch intent. A separate pinned `reconcile` endpoint re-enters only the broker-owned request ledger. If the original broker died before its apply intent, the same reservation can finish preparation and dispatch once; after durable apply intent, the broker only observes and never repeats the transport. This endpoint is bounded by the existing observation budget and requires the coordinator's persisted semantic dispatch intent.

Subsequent recovery reads frozen exchange blobs and recorded process artifacts, so later mutable worker changes cannot alter the integration subject. Receipt structure, content identities and canonical receipt digest must all match before success is recorded. Unknown integration outcomes keep the writer and are queried within the finite observation budget.

The callable local CLI supports `authority`, `query`, `apply` and `reconcile` with a pinned config file and one bounded JSON stdin request. The config remains aide.broker.config.v1, containing state_root, exchange_root, repository_root, exact Git executable/hash and externally issued authority. Unknown fields, duplicate JSON keys and changed config bytes refuse. The CLI cannot select the internal transport fixture; production apply always refuses in this slice.

## Verification and remaining qualification

Tests use disposable local Git repositories, real Windows process-death boundaries and a base larger than the old complete-tree entry budget. They exercise binary/untracked/deleted files, tree identity, corrupt content, directory substitution, bounded interrupted preparation, lost replies, exact receipts, authority refusal and existing v0 behavior. Coordinator-v1 tests use the real local broker core and genuine independent test commands, with explicitly synthetic model sessions, external authority decisions and integration observations.

WindowsJobHost remains same-user process containment. It does not establish credential/filesystem isolation, network denial or volume quota. Separate qualified worker/controller/broker boundaries, production authority issuance and PR/check transport, target-store qualification and a real two-task demonstration remain required. Production transport must revalidate the selected generation object and materialized content at its own effect boundary; injected transport does not establish that qualification. The large synthetic base proves the entry-budget fix, not actual 10,631-file AIDE checkout readiness. Passing fixtures do not complete the WorkUnit, activate unattended operation or qualify FacMan Beta1.

## Prepared effect boundary

`effect_boundary.prepared_candidate(broker, request)` validates the durable
request/generation binding and compares the live volume/file identity with the
prepared directory identity. It holds directory leases and the broker lock
through `transport.apply`, checks the protected base store with strict fsck,
requires the exact permitted alternate and generated bare configuration,
compares index modes/objects with the frozen overlay, validates the complete
candidate object graph, and reads every changed blob back against frozen bytes.
A second base/expiry check precedes the yielded effect. Replacement, corrupt or
missing objects, changed index/config/alternate and moved base refuse before
apply intent. Uncertain directories remain untouched. A later transport stage
must enter this boundary again before its own effect; the directory handles do
not exclude arbitrary concurrent child-file writers or qualify credentials.

## Protected capsules and finite issuer

After its final candidate snapshot check, the coordinator publishes an exclusive
`authority-capsules/<frozen-digest>.json` under its budgeted state root. It contains
the activation digest, exact attempt, baseline/subject snapshots and recorded
coding/test/assurance process requests and responses. Publication does not issue
authority. The issuer-side parser checks snapshot identities and frozen changed
bytes, exact role argv/source pins, unique owned Job IDs, completed successful
receipts and the actual stdin/stdout/stderr hashes. It reparses Codex verdicts
against the original baseline/subject and requires distinct coding/assurance
sessions before reconstructing the frozen verification record.

`authority.Issuer(delegation_path, approved_sha256)` reads a separately pinned
finite delegation and activation. It restricts repository, exact task IDs,
paths/checks and expiry to that activation, then records one immutable issued
authority per frozen request/task in a WAL/FULL ledger. Repeated identical
issuance returns the same authority; changed evidence, over-budget issuance,
unknown tasks, altered external bytes or unqualified hosts refuse.

The operational issuer has no qualified host implementation installed. The
internal `qualification.assert_current(delegation, activation)` seam must
independently authenticate current controller/store identity, filesystem and
credential boundaries and executable inputs; there is no config-loaded plugin
or CLI shortcut. When absent, issuance refuses before ledger creation. Tests
use an explicitly synthetic qualification seam to exercise local data flow;
that fixture is not a host receipt. Protected controller authenticity cannot be
proved by self-reported booleans or content hashes alone.

## Offline PR/check observation and intent core

`pr_observation.decision(plan, observation)` validates a normalized provider
observation against an exact request/candidate commit/tree/base, request-named
branch, actor and PR. The PR must explicitly bind its base ref to dev and both
base/head repositories to the admitted repository, even when other branches or
forks share the same object IDs. The first observed PR number is immutable for
the request. Required checks bind both the application ID and workflow
source commit, the exact candidate head, successful completion and an explicit
complete-page observation. Draft/closed PRs, incomplete/skipped checks, foreign
sources and moved base cannot reach merge readiness. A merged record requires
exact candidate tree, ordered base/head parents, passing checks and observed
ancestry in the integration target. This increment supports ordinary merge
commits; it does not silently reinterpret squash/rebase results.

`ObservationStore` reserves at most two lifetime requests and one unresolved
writer per repository/target. It records at most 128 observations per request
(or a smaller plan limit) and one durable intent per object-publication,
branch-creation, PR-creation and merge stage. An absent observation after an
intent cannot authorize repeating that stage. A mutation intent must bind the
latest recorded observation and unexpired plan; terminal integration also
requires a prior merge intent and cannot later change its recorded PR result.

This module installs no provider adapter, API client, network dispatcher or
object uploader. Normalized observations are not authenticated merely because
the parser accepts their shape. A real qualified adapter must obtain complete,
fresh provider facts and enforce each admitted effect. Merge additionally needs
an externally qualified exact-base server contract and current matching target
policy. GitHub's expected-head merge request and a local base pre-read alone
are not proof of atomic exact-base refusal. AIDE currently has no hosted
workflows or branch rules; the actual target does not meet that requirement.
No target settings, credentials or operational activation changed here.

## Staged request reconciliation

`staged_transport.StagedTransport` connects a fixed PR plan and literal candidate
commit bytes to the broker ledger. `Broker.reconcile` prepares a request if
necessary, observes the exact service state, and dispatches at most one new
mutation stage. Each stage holds the prepared-generation object/content guard
and reserves its own durable intent. A lost response can reveal that a later
stage is ready, but absence never permits repeating the uncertain operation.
`query` observes service facts and may record a checked integration receipt; it
never dispatches a mutation. The earlier single-effect fixture interface retains
its original observation-only behavior after its one apply intent.

Candidate commits have one exact parent and the frozen tree, canonical actor
metadata and a fixed epoch for deterministic serialization. The protected plan
pins their object ID and reviewed message. Local Git writes/reads the literal
commit object before stage intent; no identity config, hooks or signing command
is used. A merge receipt requires the durable merge intent and verified exact
PR identity, tree, parents, complete required checks and target ancestry.

The adapter interface is internal and absent by default. No config/CLI factory
can install one. A future actual provider adapter must authenticate and bound
its observations and commands, bind a protected plan, and enforce the real
host/store and server mutation contract. Calling no-op qualification methods in
a scripted fixture establishes none of these properties. Observations have a
one-MiB response bound and the existing finite ledger budget; the registered bridge below now supplies bounded child execution. Actual API
normalization and operational host/server qualification remain required. Every dispatch must preserve the exact lease and current source
qualification through its effect boundary. No production activation is implied.

Each provider read reserves a durable attempt before calling the adapter.
Malformed, timed-out or missing responses consume the same finite budget;
restart cannot replenish it. Existing v1 observation records are conservatively
charged when the additive attempt table is first used. A failed attempt write
prevents the provider call. Immediately after the stage intent checkpoint and
current qualification check, dispatch rechecks the local target and both the
plan and authority deadlines. Expired intent is retained and cannot be replayed.

## Registered JSON provider bridge

`RegisteredBridge(registration_path, approved_sha256, plan, qualifier=...)` is an
internal adapter for `StagedTransport`. It installs no provider implementation
or CLI factory. Its separately pinned `aide.broker.bridge.v1` registration binds
the exact plan digest, fixed command, executable/script/source input hashes,
protected working directory and finite timeout, output, memory, process, call,
retained-IO and free-space limits. Only a native absolute executable or an
explicit `python.exe -I -B <absolute-script.py>` command is accepted. Unknown
fields and changed inputs refuse. The required external qualifier must supply
a bounded local check of actual protected host/store and executable trust;
fixture no-op qualification establishes none of those properties.

Each provider read receives its exact durable observation-attempt token. Each
mutation must match the current plan, latest observation and recorded stage
intent. A separate WAL/FULL bridge ledger binds the complete registration and
reserves a unique call/Job identity, input digest and worst-case retained IO
before any evidence directory or child is created. A distinct provider lock
serializes these calls while the existing broker/generation locks remain held.
At most two requests and their fixed finite call/IO budgets are retained. The
bridge refuses reuse of an observation token or mutation stage, even after a
failed or interrupted child.

The child receives one bounded `aide.broker.bridge-call.v1` JSON stdin envelope
with call ID, request digest, operation, exact plan, prepared-generation
identity/commit bytes, and, for mutations, the exact canonical observation and
digest that selected that stage. Before reservation and while the owned child
runs, the bridge rechecks that the observation is still the ledger's latest
record, its digest matches the durable stage intent, and the pure decision
function still selects the requested operation. Missing, altered, stale, or
wrong-stage bindings refuse before a child can act. Its response must use
`aide.broker.bridge-response.v1` and repeat the exact call/request/operation
identities. Observation results then pass the existing independent PR/check
parser. Mutation responses may acknowledge only `submitted`; acknowledgement
is never integration proof, and a later authoritative observation must advance
or close the request.

WindowsJobHost assigns each child atomically to its unique owned Job while
suspended. Immediately before creation, before resume, after resume and during
bounded execution, the parent rechecks source/registration pins, current local
qualification, durable authorization and both mutation deadlines. An expired
mutation intent remains uncertain and cannot authorize replay. Observations
after expiry remain available for lost-reply reconciliation. The parent drains
bounded output, quiesces descendants, fsyncs and hashes retained streams, checks
the exact stdin bytes and records the returned response digest. Missing, invalid
or oversized output and child/guard failure remain uncertain. On restart, only
recorded named Jobs may be fenced; paths are retained and PIDs never establish
ownership.

The deadline monitor bounds client execution. It cannot retract a request that
already reached a server or enforce atomic exact-base merging. A real provider
implementation still must authenticate complete current facts, enforce the
qualified remote predicate, and revalidate protected prepared content at its
effect boundary. Same-user Job containment and a sanitized environment do not
establish credential/filesystem isolation. Tests use local scripted child
processes and disposable Git objects; no actual provider, credentials, network
mutation, operational activation or completed broker qualification is implied.

## Raw GitHub observation contract

The current source adds three bounded read-only modules. `github_api.Reads`
accepts an injected `read(url, headers, timeout, max_bytes)` implementation and
returns only validated REST objects/pages. There is no installed HTTP client,
credential source or bridge-child factory. A real reader must authenticate TLS
and the intended principal, stream within the supplied byte bound, disable
redirects/retries, and run inside the separately qualified registered bridge.
Fixture readers establish parser behavior only.

Each observation has a fresh deadline of at most 120 seconds, with a separate
monotonic elapsed-time ceiling, at most 96 GET calls, eight MiB of response
bodies, one MiB per response and 128 records per collection. Attempts consume
budget before dispatch. Two-page collections require stable counts, unique
identities and exact same-origin/path/query pagination; query ordering may
vary but foreign/extra parameters and loops refuse. Duplicate JSON/header
fields, non-finite values, structural overflow and unexpected status/media
shapes refuse. A JSON null never becomes an absent object. Only an explicitly
allowed 404 can mean absence, after repository and contents access checks.

Read deadlines are independent of expired mutation authority. A finite
observation can therefore reconcile a successful merge after authority expiry;
existing broker/bridge stage checks continue to forbid expired mutations.
No parser acceptance authorizes a retry of an uncertain effect.

`github_observation.collect` reads the actual user/repository, target/candidate
Git objects, exact refs and all request-branch PRs without filtering away a
retargeted base. It checks PR list/detail identities, base/head refs and
repositories, author, state and exact commit/tree/parent facts. After checks it
re-observes the PR, target, request branch and access identity; a changed view
refuses. These reads detect observed drift and do not establish server atomicity.
For merged PRs, the immutable merge object's first parent supplies the base;
the later mutable PR base.sha is never integration proof. Exact ordered parents,
tree and target ancestry still pass the existing decision/intent ledger.

`github_checks` binds each required check's actual app, check-suite and head to
its Actions push run and exact run-attempt job. Run repository, branch, event,
head commit, workflow entry path and check/job status must agree; re-observing
the run detects a changed attempt. Missing checks wait. Exact app/head-bound queued or in-progress checks can
precede run/job publication; they produce incomplete observations without
invented workflow facts. Completed checks retain full provenance requirements;
skipped/neutral conclusions never become successful broker checks. The executed entry workflow version is
derived from the actual push event's head commit, not copied from the plan.
GitHub documents those event/run/job relationships in its
[workflow-run API](https://docs.github.com/en/rest/actions/workflow-runs),
[job API](https://docs.github.com/en/rest/actions/workflow-jobs) and
[workflow execution model](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows).
Workflow/action dependencies and a non-skippable final gate still require
reviewed target-workflow qualification; this collector does not prove them.

The initial identity parser accepts authenticated User responses only. A real
restricted principal and immutable principal-ID binding remain target work;
App installation authentication requires a separately implemented observation
path and cannot be simulated by relabelling an owner credential. Policy and
merge-contract digests are absent in collected observations, so complete
passing checks yield `qualify_target`. Only a later actual qualified target
observer may add those facts; desired plan values are never substituted.

## Concrete target and host completion work

AIDE-CW-GITHUB-TARGET-QUALIFICATION-01 owns current target observation, an exact
reviewed policy/workflow/principal proposal, actual provider implementation and
hosted adversarial acceptance. For one-parent candidate C over admitted base B,
monotonic target history and strict up-to-date checks imply that a new merge
starts at B. Expected-head matching adds head binding. REST merging still lacks
an expected base-ref argument, so same-OID PR retargeting needs an additional
server guard: the broker principal must be denied updates to all non-dev refs,
including later-created refs. The owner retains separately identified normal
branch/promotion authority. The exact item records primary sources, 13 local
Git graph counterexamples and required hosted tests. Local graph acceptance is
not GitHub enforcement qualification; no settings were installed by admission.

AIDE-CW-ISOLATED-HOST-01 now names concrete AppContainer/token, owned-root DACL,
network-capability and denial-probe work. Same-user Jobs remain containment.
Protected host/store and actual principal/target acceptance are broker close
dependencies; source preparation can start independently. The existing clone,
resume, supervisor and live-pilot tasks retain their own executable acceptance.
All broker and programme completion/activation claims remain open.

## Fixed HTTPS observation mechanism

`github_http.GitHubHTTP(plan, deadline=..., host=...)` implements real bounded
TLS GET exchanges for the existing `Reads` callback. The only production
origin is `https://api.github.com`; paths stay under the admitted repository
or `/user`. The constructor exposes no endpoint, certificate-trust, resolver,
proxy, retry, or redirect configuration. The synthetic route/trust overrides
exist only in the direct test subclass and are not installed by any worker,
configuration loader, CLI or production factory.

A trusted controller must inject a protected host with bounded, thread-safe
`assert_current(plan, "observe")` and `credential(plan, "observe")` operations.
The latter is a context manager yielding a non-printing `Credential` token and
finite expiry. The host is absent by default. No real token acquisition, storage,
principal creation, permission installation or credential discovery is present.
The exact immutable plan is supplied afresh to each host check. Observation
leases are independent of the plan's mutation expiry, preserving read-only
lost-reply reconciliation; this module implements no mutation methods.

Each attempt is consumed before transport effects. The observation has a fresh
wall deadline within 120 seconds plus a monotonic ceiling; each exchange lasts
at most 10 seconds, with at most 96 attempts and 8 MiB total received wire bytes.
The caller can reduce the per-response 1 MiB body ceiling. Concurrent reuse
refuses. The existing `Reads` budget and durable outer observation reservation
remain required. Neither a failure nor missing/ambiguous output initiates a retry.

DNS is independently bounded: its daemon can only return at most 32 addresses
into one result slot. It cannot later connect or acquire credentials after the
request deadline. Only the first address is attempted. The registered containing
child remains the final lifetime/resource boundary for the resolver and bounded
host hooks. An exchange monitor closes its owned sockets on expiry or revoked
qualification. Main-path checks occur before/after connect, TLS and send and
while receiving; slow headers, stalled TLS and stalled bodies do not extend the
absolute deadline. Cancellation checks are not a server-side atomicity guarantee.

TLS requires certificate verification, hostname verification for api.github.com,
and TLS 1.2 or later. Credentials are acquired only after the handshake proves
that policy. The implementation uses an explicit verified SSLContext and refuses
SSL_CERT_FILE, SSL_CERT_DIR and SSLKEYLOGFILE environment overrides, including
empty values. It performs no proxy lookup, trust-store changes, debug logging,
connection pooling, redirects, automatic retry or decompression. Python documents
these TLS mechanisms in its [SSL reference](https://docs.python.org/3/library/ssl.html).

`github_http_framing` supports a deliberately closed HTTP/1.1 JSON subset:
200/404, at most 64 unique ASCII headers, 64 KiB cumulative status/header bytes,
8 KiB lines, and explicit Content-Length or plain chunked bodies. A bounded
8 KiB receive buffer may contain already-arrived bytes past the current line.
The parser rejects duplicate headers, conflicting framing, absent framing,
compressed bodies, interim/redirect/error responses, oversized or truncated
bodies, chunk extensions/trailers, and more than 4,096 chunks. It does not claim
support for every legal HTTP response shape; actual GitHub response compatibility
remains part of the target's operational qualification.

Responses containing a literal or JSON-escaped credential in headers/body refuse
before publication. Exceptions from TLS, parsing and trusted host hooks are
replaced outside their catch block, so printable exception chains carry no
underlying response/token. Arbitrarily transformed secrets and untrusted code in
the protected host are outside this mechanism's trust premise. Python heap data
is not a credential-isolation boundary; the separate protected host still owns
that requirement.

The first independent-review packet binds two additive runtime modules and one
direct test. Nineteen tests use real disposable loopback TLS and per-run synthetic
certificates generated by an existing OpenSSL executable. They prove bad trust
and hostname denial before leasing, missing/revoked/expired authority before
requests, deadline checks at TCP/TLS/credential/send boundaries, no redirect or
proxy use, malformed/bounded framing, literal/escaped secret reflection refusal,
late DNS without later dispatch, concurrent/finite budgets and a complete raw
collector over the actual TLS path. The successful collector still returns
`qualify_target` with no policy digest. These are local mechanism proofs; they
establish neither a protected Windows credential host nor a restricted GitHub
principal, effective target rules, hosted exact-base enforcement or activation.

## Native Windows host source slice

`continuous_worker.windows_security` adds an internal trusted-controller
`SecurityLaunch` object for one zero-capability AppContainer profile. An
exclusive flushed reservation precedes profile creation. Existing or uncertain
reservations cannot replay or adopt a profile. WindowsJobHost supplies
SECURITY_CAPABILITIES together with the exact HANDLE_LIST and JOB_LIST in the
same suspended CreateProcess call, then observes the actual child package SID,
capability count, user/integrity/elevation/UI-access and Job membership before
resume. Its existing default remains process containment only. No worker-facing
configuration or operational host factory supplies this new object.

`windows_security_objects` creates literal owned objects with NtCreateFile
FILE_CREATE, private initial descriptors and retained handles. Sealing retires
writable file handles while pinning the original object; package grants use
those exact handles. It contains no deletion operation. Root resolution observes
one local HarddiskVolume target with QueryDosDeviceW; it refuses network, SUBST,
ambiguous prior mappings and malformed output while retaining OBJ_DONT_REPARSE
for every actual filesystem component. The first real read-only preflight
refused the DOS alias, and the corrected local-volume open passes with the
expected parent identity. Microsoft documents the distinction between the
[current drive mapping and retained prior mappings](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-querydosdevicew).

The H1 queue owns separately invoked native effect drivers. Review binds exact
source, compiled probe, owned parent/marker, local volume, user/package SIDs and
finite wall/monotonic deadlines. One created profile is retained. Continuations
require its pinned complete creation journal and original actual child receipt,
create zero profiles and reserve fresh one-shot owned roots. Existing or
uncertain reservations refuse replay. No shared ACL, capability, exemption or
network setting is changed.

Four actual attempts retain their original result and bytes:

| Attempt | Raw network observation | Overall result |
| --- | --- | --- |
| Initial native | Pending10035 without completed oracle | FAIL |
| Bounded completion | Timeout10060 without causal diagnosis | FAIL |
| Loopback diagnostic | Timeout10060, diagnostic success/NETISO_NONE0, live controls | FAIL |
| Pinned local interface | Timeout10060, diagnostic success/INTERNET_CLIENT2, live controls | PASS for exact local native probe |

The passing effect bound an exclusive listener only to 172.21.208.1, interface 50,
vEthernet (WSL), on one ephemeral port. GetUnicastIpAddressEntry/GetIfEntry2
checked exact address/index/alias/prefix, Preferred/connected and skip0 before
effects and during execution. Connect and calling-token diagnosis used the
same literal IPv4; no DNS or wildcard bind. The listener accepted ordinary
controls before and after, observed no child connection, and exact package
non-exemption stayed stable. Diagnostic2 means missing internetClient; endpoint
address does not determine the returned category. See Microsoft's
[NETISO_ERROR_TYPE definition](https://learn.microsoft.com/en-us/windows/win32/api/netfw/ne-netfw-netiso_error_type).

Timeout remains timeout. The passing predicate requires the supported
calling-token missing-capability result, actual endpoint controls and existing
token/file/controller facts together. Child exit0/exited/quiescent and empty
stderr are retained. The run used 252 of 256 read-only interface observations,
each bounded to one second/512 output bytes, with authority rechecked after the
read. These observations do not atomically lock network configuration.

Twenty-seven source/refusal tests, ten existing actual Job regressions and three
ordinary native oracle tests pass and were independently replayed. Four packets
retain exact source, binaries, reviews/effect manifests, intents, actual receipts,
stdout/stderr and scratch proof. The first three remain FAIL; later success does
not relabel them. Current raw custody navigation lives under the H1 task evidence.

This qualifies only the exact native token/local-endpoint probe. AppContainer
descendants/supervisor-death/reparse adversarial cells, private Python/Git/Codex,
controlled model channel, credential/broker host and operational acceptance
remain required. The host WorkUnit is running/PENDING; no worker was activated.

## Fixed synchronous merge source contract

`github_merge.merge_request(plan, observation)` constructs the only admitted
merge shape after the existing pure decision function has revalidated the exact
repository, pull, base/head, actor, check, policy and contract facts. It uses
`PUT /repos/{owner}/{repo}/pulls/{number}/merge`, ordinary `merge`, and always
sets the request-body `sha` to the immutable candidate commit. GitHub documents
that value as an expected-head predicate and a mismatch as HTTP 409 in its
[pull-request REST API](https://docs.github.com/en/enterprise-cloud@latest/rest/pulls/pulls#merge-a-pull-request).

The endpoint has no expected-base argument. Base SHA/ref, target ref, actor,
policy, ruleset, bypass state and principal permissions are therefore local
preconditions or still-unqualified server controls, not endpoint-atomic claims.
The source contains no sender, credentials, settings/workflow mutation or
production factory. `classify_response` accepts only bounded exact-endpoint JSON,
classifies 405/409/422 as refusals, and returns only `submitted` for a successful
response. Missing replies remain uncertain under the durable bridge's no-replay
contract; only a later authenticated observation can return `integrated`.

Thirty-one focused tests pass for exact request bytes, stale fact refusal,
response bounds and submission/integration separation. Hosted target races,
effective policy/principal observation, workflow provenance and protected
host/store qualification remain unrun.

## GitHub target-policy review contract

`github_target_policy` now owns a pure desired/current comparison and exact
review-plan builder. It has no HTTP client, credential reader, settings writer,
workflow installer, or apply entry point. An unresolved broker principal or
workflow/check application identity yields `status: blocked`, an empty
operation list, and `apply_authorized: false`.

The desired contract permits ordinary merge commits only, requires pull
requests and one strict app-bound check on `dev`, disallows dev bypass, and
prevents deletion and non-fast-forward updates. A separate all-branches-except-
dev ruleset restricts later updates, deletion, and non-fast-forward history;
the exact owner id is its only proposed bypass. Because the update restriction
does not restrict creation, a broker request branch can be created once at its
final admitted object and cannot later be moved by that principal.

The contract distinguishes guarantees precisely. Expected head, strict check,
pull-request-only dev updates, and qualified ruleset restrictions are intended
destination-enforced controls. Expected base, actor, policy digest, and
workflow source remain local preconditions. The merge endpoint still has no
atomic expected-base or policy compare-and-swap argument, hidden bypass cannot
be inferred, and an uncertain mutation must not be replayed.

The current normalized observation remains unqualified: no rulesets, effective
dev rules, classic dev protection, workflow, restricted broker principal, or
check-app identity exists. Merge, squash, and rebase are all currently enabled.
The checked-in review plan therefore contains no operations and cannot be
applied. A resolved fixture proves deterministic PATCH/POST review bytes, but
does not authorize or qualify those operations on GitHub.

## Supported Windows API-set host queries

The isolated-host H2 source now uses a separate `NativeApiSetQueryApi` around
Windows' supported `GetApiSetModuleBaseName` dependency-analysis interface.
API-set contract names are virtual loader contracts, so the earlier retained
resource-map failure is not retried or recast as file absence. The new one-use
query session binds exact names, OS build, expiry, controller guard, reservation,
per-name durable intents, HRESULTs, output lengths, and canonical host basenames.

The explicit API-set ceiling is 256, which contains the observed 180-name Python
closure and is exercised as one bounded injected workload. Query results still
mark physical-host, restricted-context, and loader qualification false. Exact
host bytes, protected controller authority, private-image grants, AppContainer
Python execution, and operational activation remain later reviewed boundaries.
