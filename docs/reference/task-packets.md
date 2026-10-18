# Task packet identity and scope

Prepare a compact projection of an existing reviewed WorkUnit:

```text
py -3 .aide/scripts/aide_lite.py pack --task AIDE-DAILY-TASK-BINDING-01
py -3 .aide/scripts/aide_lite.py verify --changed-files
py -3 .aide/scripts/aide_lite.py verify --task-packet .aide/context/latest-task-packet.md
```

The packet declares `task_id`, names the task's queue records, and projects its
actual allowed/forbidden paths. The queue owns authority, acceptance and durable
state. Generating a packet neither admits implementation nor activates effects.

Verification selects scope from the latest task packet, or the supplied
`--task-packet`. Another active item and incidental identifiers in later evidence
do not replace the declared task. Task inspection and default review evidence use
the same selected identity. Unknown, escaping or conflicting declarations, missing
explicit packets, mismatched owners and missing named-task scope fail closed.
Unknown named task preparation refuses before writing the packet or snapshot.

Older `phase:` declarations remain recognized. Undeclared Q-era generic packets
retain their historical fallback for compatibility; their placeholder scope is
context and cannot authorize work. Prepare a real named WorkUnit for non-trivial
work. The structural verifier checks paths and records; it cannot prove semantic
correctness, filesystem containment, model behavior or release support.

The regression baseline and exact managed test evidence belong to
[AIDE-DAILY-TASK-BINDING-01](../../.aide/queue/AIDE-DAILY-TASK-BINDING-01/ExecPlan.md).

## Read-only current-task view

`task current` retains its task ID/status prefix and adds a compact recorded
outcome, objective, owner, next action, remaining obligations and scope.
Use `task current --task-id PROJECT-WORK-01 --json` for the versioned
`aide.task-current.v1` projection. Without `--task-id`, existing latest-packet
selection and legacy fallback apply. Invalid explicit identities refuse rather
than selecting unrelated work. Both renderings use the same observation.

`status.yaml` supplies current recorded status/result; the task's declaration and
queue-index projection remain separately identified. Index conflicts, duplicate
fields, malformed or unsupported public field shapes, and missing records are
visible issues. Missing owner or next action stays unknown. `needs_review` is not
acceptance. A passed preparation may still show unperformed target adoption.

This standard-library projection reads supported top-level public scalar fields,
folded objective text and a simple `remaining_obligations` string list. It does not
interpret arbitrary YAML tags, aliases or nested policy objects. Reads are bounded
to 128 KiB per record/reference (1 MiB for the index), 64 projected fields, 16
references and bounded diagnostics. It refuses private, escaping, linked and
non-ordinary paths. These are command read guards, not whole-client isolation.

Task-relative or `.aide/` repository-relative `*_ref` values are observed as
metadata; optional matching `*_sha256` values detect changed bytes. A present file
or matching digest does not prove acceptance or applicability to current inputs.
`applicability` remains `unverified`, and `acceptance_verified` remains false.
No referenced evidence body, private state, status update or execution is emitted.

## One development brief

Use an explicit task and file to combine the existing continuation, file-quality
and current-lesson views without generating reports or changing project state:

```text
py -3 .aide/scripts/aide_lite.py task brief --task-id PROJECT-WORK-01 --path src/repair.py
py -3 .aide/scripts/aide_lite.py task brief --task-id PROJECT-WORK-01 --path src/repair.py --json
```

The brief shows the recorded task outcome and next action, continuation advice,
the file's recorded owner and likely checks, reuse coverage and current lessons.
Task ownership and file ownership remain distinct. Scope is a reference to the
owning task, not an inferred permission. Inspect that task and its applicable
policy before acting. No worker, model, test, scan or index generation is started.

JSON uses `aide.task-brief.v1` and retains the three component observations,
task-record hashes and their limitations. `OBSERVED` (exit 0) means the component
observations were assembled; it does not establish acceptance, current quality
coverage or permission. `PARTIAL` (exit 2) identifies missing/invalid auxiliary
information or unavailable task evidence. `REFUSED` (exit 1) supplies no combined
advice after unsafe identity/path input, inconsistent task records or overflow.
Missing quality data is unindexed, not proof of no dependencies. Invalid auxiliary
data calls for reconciliation. A stale or retired lesson never restores old advice.

Task identity is exact rather than an alias or latest-packet fallback. The selected
path is one canonical repository-relative file name; it may name a planned file.
Its source content is not read merely to look up metadata. Existing exclusions
reject private/local paths. The shared quality reader checks ordinary files and
ancestors, refusing redirected or multiply linked reports rather than following them.

All existing reader bounds remain: task/status 128 KiB each, index 1 MiB, quality
report 16 MiB, and the lesson reader's finite ledger/evidence limits. Task records
are compared before and after assembly; this detects observed change, not an
atomic snapshot or hostile-writer isolation. Output is capped at 64 KiB. Human
output quotes project text and reports omitted links/lessons; JSON carries details.
Hashes establish bytes, and lesson authorship/correctness remain unverified.
Whole-work usage is unknown. This command does not qualify a new host or release.
