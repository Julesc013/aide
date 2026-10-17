# Cooperative dependency tools: bounded admission

Parent AIDE-CONVERGENCE-AND-DELIVERY-01; child AIDE-DEPENDENCY-MCP-01.
Base dev/main: 8f93cb7e021a5347e71d81a60aae4bd3f8d53602. Date 2026-10-18.

## Outcome and owner

Expose the existing Requests ledger through participant-bound local tools so an
agent can discover its inbox and submit/read/acknowledge a dependency without
editing another project's queue. Preserve Requests as the only lifecycle owner.
This is an operational stdio interface exercised by a real subprocess protocol
client; it is not yet delivery to a user's existing agent or downstream adoption.
Those outcomes remain mandatory parent follow-ons.

Read-only observation found codex-cli 0.162.0-alpha.17.2 in the installed VS Code
extension, SHA256 f5521b058ca08e249afd3b25b4681e81100181d92e73aa6b94bb8e75c2aa487b.
The observed app-server process had no explicit listen/proxy/remote-host flag.
Official documentation gives stdio as the default. This establishes no usable
shared connection to that worker; it is not an exhaustive absence-of-endpoints
claim. No server was started, global configuration changed, history read, or
peer contacted. An unrelated new server must not be called the existing worker.

## Design and bounded behavior

- Add a bounded inbox projection to Requests, retaining request IDs, revisions,
  next owner/action and cooperative limitations. Discovery never acknowledges.
- Extract existing safe database preflight/opening into one shared local access
  module. CLI retains existing init and record semantics. No new schema, state
  root, scheduler, task authority or migration.
- A stdio process is launched with exact existing root/configuration digest and
  participant/binding digest. These cannot be supplied or changed by a tool call.
  Tool reads reveal only requests involving that participant; mutations delegate
  to Requests with the bound actor. The binding is cooperative, not OS isolation.
- Four tools: inbox, status, submit, observe. No initialization, shell, dispatch,
  provider, filesystem browse, integration or release tool. No automatic marking
  of delivered/accepted. Tool results remain reported observations, not verified
  remote effects or permission grants.
- Pin the small stdio/tools subset to MCP 2025-11-25, matching the existing
  contract target. Implement newline JSON-RPC lifecycle, initialize/initialized,
  ping, tools/list, tools/call, strict frame bounds and error/refusal mapping.
  Advertise only tools. No HTTP, authentication, sampling, tasks extension,
  subscriptions or generic protocol framework. Unknown methods refuse; EOF ends
  the process without changing a dependency. Process lifetime is host-owned.
- The MCP Python SDK is absent. For this stdlib runtime profile, a small isolated
  transport avoids adding an installation requirement to the portable core. If
  protocol complexity exceeds this scope, stop and propose the upstream SDK as
  an optional dependency; do not grow a parallel framework. Protocol code must
  stay separate from lifecycle logic and can later be replaced by an SDK binding.
- Preserve the existing contract-only module's boundary; this operational adapter
  does not activate its broader catalogue. No claims of universal MCP conformance
  or installed-client compatibility from handcrafted fixtures alone.

Protocol references: official MCP 2025-11-25 basic/lifecycle, basic/transports and
server/tools at https://modelcontextprotocol.io/specification/2025-11-25/ .
Host reference: https://learn.chatgpt.com/docs/app-server .

## Allowed paths and work plan

- core/runtime/continuous_worker/requests.py (inbox projection only)
- core/runtime/continuous_worker/__main__.py (reuse safe access, optional inbox)
- core/runtime/continuous_worker/request_access.py (shared safe local access)
- core/runtime/continuous_worker/dependency_mcp.py (isolated stdio tools adapter)
- .aide/scripts/tests/test_continuous_worker_mcp.py
- .aide/scripts/tests/test_continuous_worker_requests.py (affected regressions)
- docs/reference/local-dependency-requests.md
- .aide/queue/AIDE-DEPENDENCY-MCP-01/**
- .aide/queue/index.yaml
- parent ExecPlan.md, status.yaml and this admission
- .aide/intake/latest-*, .aide/context/latest-task-packet.md
- existing compiler-owned .aide/generated/**, .aide/reports/capability-*
- PLANS.md, IMPLEMENT.md, DOCUMENTATION.md

1. Record child scope/ExecPlan; implement the interface over existing owners.
2. Independent exact source/effect review before each managed job. Test actual
   subprocess protocol exchanges, restart/duplicate recovery, participant
   filtering and spoof refusal, malformed/oversized frames, lifecycle ordering,
   expiry/pause/config mismatch and unchanged native task/effect records. Retain
   every existing Requests and State regression. Read/failed open must preserve
   unknown database bytes and directory entries.
3. Collect and retire each attempt; preserve full logs and failures. Validate
   docs/catalogues and development pack coherence without changing exports.
   If export refresh is demonstrated necessary, separately amend scope.
4. Review exact source/effect for dev/main synchronization. Commit coherent work,
   report fixture versus installed-client evidence precisely. Continue actual
   worker configuration/delivery through separately reviewed effects.

At most two offline managed fixture jobs, each separately reviewed, unchanged
runner configuration 61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90,
1 GiB Job / 180 seconds / 32 MiB scratch / 8 MiB retained and existing reserves.
No dependency acquisition/install, live ledger initialization, actual peer
contact, client configuration, network listener, model or downstream mutation.
No broader source refactor, export/archive/release/protection change.

## Authority, Git and recovery

Parent owner delegation and qualified independent admission authorize local-only
task/aide-dependency-mcp-01 from the exact base in the sole existing checkout.
Only four intake files plus this admission are owned pre-branch edits. Require
fresh helper/ref/dispatch/job checks; preserve all other branches and changes.
Admission does not authorize any integration or external effect by itself.

Original local increment is already integrated at 8f93cb7e, tree
907441ecd0c9ce868ec3783efc498cf85f6f43e5; its ignored integration-result.log retains
actual commands/ref confirmations. Its 47 runtime cases and six pack-ownership
cases passed. Its state/export evidence remains valid for unchanged bytes;
changed access/requests routes receive affected regression here.

Disconnect or unknown response: inspect by stable request ID; do not blindly
repeat non-idempotent effects, launch another worker, or claim delivery from an
MCP transport connection. Stop for changed inputs, unresolved review, or exceeded
job allocation. Keep the blocked DiskEd native ownership decision pending.
