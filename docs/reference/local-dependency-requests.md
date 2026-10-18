### Local dependency requests

The optional continuous-worker request interface records a cooperative exchange
without taking over either project's native task. It uses the existing
`coordinator.sqlite3`, transactions and event history. No daemon, model, network
transport or integration operation runs as a consequence of these commands.
The integration broker's independently reviewed candidate gate is unchanged.

The state progression is `recorded → delivered → accepted → returned → adopted`.
Delivery is the recipient's attributed receipt, acceptance links its native work,
and adoption is the sender's separate observation referencing its own checks.
Neither participant's statement proves that an external effect actually happened.
The status always identifies this distinction and returns the next owner/action.

**Opt-in configuration**

Use an explicitly owned existing runtime directory, outside disposable workspaces.
The root must already exist; initialization creates the existing coordinator
database if needed. It does not register or awaken a desktop session. Example
configuration (replace all identities, root, expiry and limits deliberately):

```json
{
  "schema": "aide.dependency-configuration.v1",
  "state_root": "D:\\approved-existing-runtime",
  "participants": {
    "requester": {"repository": "owner/facman", "owner": "facman-owner", "workspace": "registered-facman-workspace", "host": "cooperative-host", "session": "recorded-session", "generation": 1},
    "receiver": {"repository": "owner/setup", "owner": "setup-owner", "workspace": "registered-setup-workspace", "host": "cooperative-host", "session": "recorded-session", "generation": 1}
  },
  "expires_at": 1792300000,
  "max_requests": 8,
  "message_bytes": 8192
}
```

`expires_at` is an absolute Unix timestamp, not a renewable lease. The first
profile refuses changed configuration/bindings in place. Expiry does not release
any workspace owner. Configuration/binding replacement still needs a separately
reconciled interface; do not create another database to evade outstanding work.
For independent cancellation, initialize an explicitly approved new ledger with
`aide.dependency-configuration.v2` and the same fields. Existing v1 ledgers refuse
cancellation; changing their configuration in place also refuses. Older readers
reject v2 rather than overlook a cancellation. There is no automatic migration.
Maximums are 16 participants, 256 requests and 65,536 bytes per message. These
bound logical records; they are not a physical filesystem quota. Existing host
storage admission and resource monitoring remain necessary.

**Commands**

Invoke `python -B -m core.runtime.continuous_worker` with:

| Command | Required arguments | Result |
|---|---|---|
| `request-init` | `--state-root ROOT --input CONFIG --sha256 RAW_CONFIG_SHA256` | Pins configuration and returns its canonical digest plus participant binding digests |
| `request-submit` | `--state-root ROOT --configuration-sha256 DIGEST --input MESSAGE` | Records one immutable request or returns the existing identical request |
| `request-observe` | Same common arguments and a MESSAGE | Records one attributed, revision-bound stage observation |
| `request-status` | `--state-root ROOT --configuration-sha256 DIGEST --request-id ID` | Opens the database read-only and returns the current record, limitations and next action |

All outputs are JSON. Refusal exits 2. These commands require direct access to the
local state, so this is a cooperative trusted-caller profile, not a multi-user
authentication boundary. A binding digest detects mismatch, not impersonation.
The configured repository/workspace/session strings are declarations and are not
checked against a running editor or used as executable paths. No source or
evidence reference is automatically opened, fetched or trusted as permission.

The submit MESSAGE has `actor` and `request`. The actor contains `participant`
and its `binding_sha256`. The request has these exact fields:

```json
{
  "schema": "aide.dependency-request.v1",
  "id": "setup-fix-1",
  "sender": "requester",
  "recipient": "receiver",
  "sender_work": {"ref": "native-work-reference", "sha256": "64-lowercase-hex-digest"},
  "objective": "The bounded dependency change",
  "acceptance": "The recipient-owned checks and requested result",
  "references": [{"ref": "source-or-context-reference", "sha256": "64-lowercase-hex-digest"}],
  "completion": ["candidate", "validated"]
}
```

Reference objects always contain `ref` and `sha256`. Supply exact content hashes,
not the illustrative placeholders above. `completion` may name `answer`,
`candidate`, `validated`, `integrated_dev`, `promoted_main`, or `published`.
The requested level is an obligation, never a grant to produce those effects.

An observation MESSAGE contains `request_id`, `request_sha256`, `actor`, `stage`
and `detail`. The request digest comes from submit/status. Detail fields are:

| Stage | Actor | Exact detail fields |
|---|---|---|
| `delivered` | Recipient | `receipt`: reference |
| `accepted` | Recipient | `native_work`: reference; `evidence`: references |
| `returned` | Recipient | `subject`: exact result reference; `claims`: every requested obligation mapped to `PASS`, `FAILED`, `NOT_RUN` or `UNKNOWN`; `evidence`: references |
| `adopted` | Sender | `returned_sha256`: canonical digest of the entire returned observation; `verification`: sender-owned check references |

Canonical digests use the existing State `digest()` function: UTF-8 JSON, sorted
keys, compact separators, unescaped Unicode. The raw configuration file hash used
at initialization is different from its canonical digest returned by the command.
Failed/unknown/unrun obligations refuse adoption; they remain visible for native
recovery with an explicit unmet-obligation list and reconciliation/successor
action. This profile does not automatically retry, revise, reject or cancel a
task. An amendment needs a separately attributed native decision and successor;
changing an existing request ID's body refuses.

**Independent cancellation (explicit v2 configuration)**

Use the same `request-observe` command or `dependency_observe` tool. These
observations retain the last normal `stage`; they never imply adoption:

| Observation | Actor | Exact detail fields |
|---|---|---|
| `cancellation_requested` | Sender | `expected_stage`: current normal stage before adoption; `reason`: nonempty bounded text; `evidence`: references |
| `cancellation_acknowledged` | Recipient | `cancellation_sha256`: canonical digest of the entire cancellation observation; `disposition`: `not_started`, `stopped`, `already_completed` or `uncertain`; `evidence`: references |

The request digest, participant binding and expected stage must still match at
the transaction. If normal progress wins a race, inspect it before requesting
cancellation again. If cancellation wins, further normal advancement refuses.
Identical observations remain replayable without additional events; conflicting
retries refuse. All earlier native-work links, return claims and obligations stay
intact. Unknown completion remains unknown, even when the recipient reports
`already_completed`. Cancellation does not alter another request.

V2 status uses `aide.dependency-status.v2`; status and inbox add
`cancellation_state` (`none`, `requested`, `acknowledged`) and
`cancellation_disposition` (null until acknowledged). While requested, the
recipient owns reconciliation and acknowledgement. An `uncertain` acknowledgement
keeps reconciliation with that recipient; other dispositions direct the sender
to review the native outcome before any separately authorized successor.
Acknowledgements are immutable observations. Later findings belong in native
recovery evidence and an attributed successor; they cannot overwrite history.

**An acknowledgement is a participant's claim, not enforced quiescence.** These
operations do not stop a process, cancel an inference request, release a workspace,
grant authority, or independently verify effects. Paused/expired controls refuse
new observations; retained status stays readable. Disconnection does not cancel.
V1 status and ordinary behavior retain their existing shape and meaning.

**Cooperative MCP tools (qualified local profile)**

The optional source module `core.runtime.continuous_worker.dependency_mcp` exposes
the same ledger through MCP 2025-11-25 stdio. A launching host supplies the existing
state root, configuration digest, participant and binding digest:

```text
python -B -m core.runtime.continuous_worker.dependency_mcp --state-root ROOT --configuration-sha256 CONFIG_DIGEST --participant NAME --binding-sha256 BINDING_DIGEST
```

Run from the AIDE source root with an explicitly owned ledger. This command does
not initialize state or configure any editor. Every tool call rechecks the pinned
configuration and binding. Caller-controlled tool arguments cannot replace them;
the local process and its launcher are still trusted cooperative participants.

| Tool | Arguments | Effect |
|---|---|---|
| `dependency_inbox` | Optional `after` ID and `limit` (1–16) | Lists involved requests with next action and cursor; does not acknowledge |
| `dependency_status` | `request_id` | Reads one involved request and reported evidence |
| `dependency_submit` | `request` object described above | Records as the bound sender |
| `dependency_observe` | `request_id`, `request_sha256`, `stage`, `detail` | Records the bound actor's explicit observation |

The protocol implements initialization, ping and tool discovery/calls only. It
advertises no Tasks extension, sampling, resources or notifications. UTF-8 newline
input frames are limited to 65,536 bytes including protocol wrapping; output
frames may reach 1 MiB to carry accumulated observations. A larger reply produces
a protocol error explicitly warning that a mutation may already be recorded;
reconcile its stable ID before retrying. Records are never truncated. An oversized or
unterminated frame closes the connection; a host must inspect the stable request
ID after uncertain outcomes. EOF closes without cancellation or acknowledgement.
The host owns process lifetime. No network listener or background polling runs.
See the pinned [MCP lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle),
[stdio transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
and [tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools).

This limited transport is isolated from lifecycle logic. The existing broader
MCP contract catalogue remains a declaration-only preview. SDK integration or
additional protocol capabilities require their own demonstrated need and checks.
The [local qualification](../../.aide/queue/AIDE-DEPENDENCY-MCP-01/REPORT.md) passed
60 methods, including actual subprocess exchanges and all original regressions.
Installed-client integration,
automatic wake-up and actual existing-worker delivery require separate evidence;
connecting a transport does not establish that another worker accepted a request.

**Continuation and qualification**

Transactions commit each record with its history event. After an uncertain CLI
response, inspect the stable ID. Identical replays conserve the record and events;
conflicting replays refuse. Reads never deliver, start a worker or consume retry
allowance. Expired and paused state can still be inspected; new observations
respect the existing coordinator controls. Requests do not create attempts, claim
workspaces, edit native work or block unrelated native work by themselves.

The source/test/effect record is
[retained local qualification](../../.aide/queue/AIDE-LOCAL-DEPENDENCY-01/evidence/second-result.json):
47 actual CLI/API/state test methods passed without skips at cf293cb0; the first
failed attempt remains linked. [Affected pack closure](../../.aide/queue/AIDE-LOCAL-DEPENDENCY-01/evidence/pack-result.json)
also passed. The runtime interface remains source-only; the portable pack retains
its existing capability boundary. Exact integration uses the task evidence.
Local fixture qualification does not establish
automatic host delivery, authenticated peer identity, isolation, real integration,
downstream adoption or native cancellation enforcement. Those remain required increments
of the daily-use workflow. Published Lite assets do not acquire this feature from
a source commit alone.

The v2 cooperative cancellation candidate is tracked by
[AIDE-DEPENDENCY-CANCELLATION-01](../../.aide/queue/AIDE-DEPENDENCY-CANCELLATION-01/ExecPlan.md).
Its source and actual CLI/MCP qualification are separate from the earlier v1
evidence; consult the child's status before treating the new behavior as qualified.
