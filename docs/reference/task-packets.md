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
