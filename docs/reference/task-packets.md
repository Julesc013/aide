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
