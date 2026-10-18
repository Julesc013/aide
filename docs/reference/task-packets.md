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

### Offline task brief page

Add `--html` to the same explicit `task brief --task-id ID --path FILE` request
to print a self-contained page to stdout. It is mutually exclusive with `--json`;
existing text/JSON behavior and observation exit codes remain unchanged. Save
stdout to a path you choose and open it separately. AIDE does not create a file,
launch a browser, start a server or refresh the page automatically.

The page leads with the next action, recorded task and remaining obligations.
Expandable sections retain file relations, reuse candidates, evidence availability,
selected/excluded lessons and source-record hashes. The complete canonical JSON
observation and its SHA-256 remain available, including fields omitted from short
summaries. A saved observation can become stale; its digest identifies its bytes,
not their correctness, current applicability or authority.

Project values are escaped text. Controls and direction characters display as
escapes; no project value becomes a URL, style, attribute or markup. The page has
no scripts, forms, frames, remote assets or actionable file links. Fixed styles
are allowed by an exact CSP hash. Escaping and inactive markup remain necessary
regardless of browser CSP support. See the [CSP metadata reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/http-equiv),
[style hash documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/style-src)
and [native disclosure element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details).

The existing brief is limited to 64 KiB; the ASCII HTML document is limited to
512 KiB. An unsafe/oversize presentation returns exit 1 with a small refusal
page rather than partial advice. A missing distribution renderer returns exit 1
on stderr without emitting a false observation; text/JSON remain independent.
Whole-work usage remains unknown. This view does not grant execution or acceptance,
qualify a browser or vintage host, or establish live Workbench integration.

### Optional fresh helper evidence

Add `--symbol NAME` to `task brief` to inspect that identifier in the primary
`--path`. Repeat `--related-path FILE` for up to seven explicitly selected
related files. Related paths require a symbol. Without these options, the
existing brief and its text/JSON/HTML output remain unchanged; no symbol source
is read automatically.

The brief reuses `quality inspect-symbol`: current definitions, calls and import
declarations carry locations, exact source hashes and parser identity. Selection
reasons identify the task target and explicitly requested related source.
Recorded owners, test links and lessons remain separate advisory evidence.

Missing, unsupported or invalid Python source yields a partial observation.
Unsafe/duplicate selections, changed records or oversized combined output refuse.
Task records and the shared quality ledger are checked across composition;
source rechecks retain the inspector's sequential observation boundary.
The 64 KiB data and 512 KiB HTML limits remain. No directory scan, code execution,
new index, model call or browser launch is implied.

Names and syntax references do not resolve runtime binding, aliases, equivalence
or complete impact. Missing matches do not establish absence. Broaden validation
when coverage is incomplete; this view cannot narrow mandatory checks.
