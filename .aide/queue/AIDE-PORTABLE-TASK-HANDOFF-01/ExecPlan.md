# Portable selected-task handoff

## Objective and scope

Create a finite, inspectable task-record handoff for another session using current
WorkUnit identity and existing task-current/resume observation. This advances P3
and the P8 offline relay proof. It is not automatic task import, dispatch, lease
transfer, host recovery or qualification of the complete daily-use milestone.
No existing queue, source contract, runtime ledger or authority is replaced.

The task CLI gains `task handoff export --task-id ID` (JSON stdout only) and
`task handoff inspect --bundle PATH --sha256 DIGEST [--json]` (read-only local
comparison). No output path, extraction, apply or network operation. Callers may
save explicit stdout in their own admitted space. Initial records are exactly
selected task.yaml, status.yaml and ExecPlan.md, not a recursive queue/archive
copy. Preserve raw UTF-8 record bytes via reversible JSON strings and SHA-256;
missing optional status/plan remains explicit. Task identity must resolve safely.
The existing bounded reader rejects unsafe/linked/secret-like paths and limits
reads; use existing secret detection before serializing records. No raw prompt,
response, credential or .aide.local material is included. This is not a guarantee
that arbitrary project text has no confidential content; no external transmission
is performed. Default record set is fixed, so peers cannot select arbitrary files.

A small pure helper at .aide/scripts/task_handoff.py owns finite JSON structure, validation,
required-feature refusal, digests and comparison; it has no host IO, scheduler or
provider dependency. Its one canonical source sits beside the CLI and is explicitly
included in the existing portable file catalogue, so safe installs receive it without
importing core/. Load only the helper beside the executing CLI, independent of the
selected target root; a missing helper refuses. No copied core implementation or new
packaging mechanism. CLI IO uses existing task view, bounded reads, secret checks
and Git provenance. All data is explicitly observational and non-authorizing.
Unfamiliar optional JSON and raw task fields are preserved; unknown required
semantics or incompatible schema refuse. Duplicate keys, nonfinite numbers,
malformed types/IDs/digests, excessive size/depth and altered record bytes refuse.
Require an explicit checksum for inspection; checksum integrity is not authorship.

Receiving inspection compares the same relative task records with the supplied
bundle. Missing/changed/unsafe inputs remain distinct. A match does not establish
current ownership, permissions, evidence applicability or safe execution. Known
completed work and uncertain effects remain in the preserved status/plan; do not
turn the bundle into an instruction to repeat them. Evidence stays referenced,
not transitively copied. The source Git head is provenance only; file digests
identify captured bytes even when the checkout contains uncommitted changes.
Read-before/read-after checks can detect changed inputs; do not claim an atomic
snapshot or protection against arbitrary concurrent writers.

## Sequence and verification

1. Preserve compiled intake and baseline; exact admission then guarded local branch.
2. Implement the shared codec, CLI and regressions. Preserve all existing current,
   resume and task-binding assertions. Qualify source in managed scratch, including
   separate-process export/inspection, same-task continuation records, changed and
   missing local records, unknown optional/required semantics and path/digest refusal.
3. Review one capability binding refresh. Use the existing owned exporter and
   verify explicit expected new helper/test members and changed CLI/reference
   payloads. Inspect the actual delivered CLI in fresh processes, then safe-install
   the actual pack in a disposable Git consumer and run its installed export/inspect
   commands with core/ absent. Check receipt ownership and exact helper bytes. Include one
   existing AIDE WorkUnit's real records as a read-only consumer, collected only
   in admitted job output; no live handoff state is created.
4. Existing fixed preview, terminal review, safe dev/main synchronization and
   retirement of only this local task branch.

Maximum 3 jobs, each separately reviewed and freshly admitted. Existing config
61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90 and D roots;
180 seconds, 1 GiB memory, 32 MiB scratch, 8 MiB retained and 4 GiB reserves stay.
No model, target, release, extra checkout or new storage root effects. Preserve
failures and all completed evidence; no automatic retry or reserve/cap reduction.

## Acceptance and recovery

A saved handoff inspected by a fresh process retains the same task ID, original
failed/interrupted/completed descriptions and remaining obligations. Unknown
optional data round-trips; unsupported required meanings refuse. Modified or absent
records do not silently become current. Code never executes record contents or
changes source/queue/report files. Missing observations remain unknown. Actual
source, exported and safe-installed CLI paths, exact hashes, complete tests and job retirement are
recorded. The declared proof is portable task-record inspection; actual worker
replacement and native downstream adoption remain separate campaign requirements.

## Progress

Read-only baseline at19e237cd: task-current/resume owners exist; no task-record
handoff command. Existing WorkUnit protocol and runtime integration handoff solve
different roles. Existing task-OS reference is exported; protocol envelope and
workunit_cli are not in Lite, so do not import that dependency tree into Lite.
Prepared intake only; no implementation, branch, commit or job yet.

Admission review requested an explicit installed execution profile. This revision
chooses safe-installed consumers as required acceptance, with a single delivered
helper beside the CLI. The prior unaccepted map did not authorize any effect.

Admission accepted; local task branch prepared. Codec, CLI and 20 regression
methods prepared with 59 existing methods retained. No managed job run yet.

Source review found loader cache writes and link following before any job.
Reused existing bounded ordinary-module checks and bytecode suppression; added
no-B subprocess preservation and sentinel helper-link/reparse refusal cases.

Source79 passed at40a5740e; jobea724f2028db4b2cb060b632f7a77808 fully retired.
Capability refresh independently accepted and CURRENT with unchanged classifications.
Actual portable/safe-installed consumers remain unrun pending this effect review.
