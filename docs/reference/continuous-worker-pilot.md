# Continuous worker pilot

The local coordinator prototype is implemented and independently reviewed. **The live pilot is not accepted or activated.** Its decisive acceptance remains two useful admitted real tasks, distinct coding/reviewer sessions, actual tests, legitimate integration, observed closeout, and automatic continuation.

Implementation: core/runtime/continuous_worker/. It does not change the accepted fixture host, service store, FacMan controller, product plan, standing autonomy policy, or release authority.

## Execution

The opt-in command is:

    python -m core.runtime.continuous_worker run --activation <protected-file> --approval-sha256 <reviewed-file-sha256>

No service, scheduled task, model dispatch or live activation is installed by this change. The activation example is intentionally incomplete and must fail preflight. A digest binds the caller to a reviewed file; it is not a cryptographic substitute for operator authority or host access control.

The pipeline claims a task, records process intent durably, invokes Codex exec JSON/schema output, snapshots the actual candidate, runs registered independent tests, invokes a fresh read-only assurance session, and requests integration from a separately protected broker. Its apply response does not close work: a subsequent query must observe the integrated result. Successful closeout immediately selects the next dependency-ready task.

Each task references an existing admission source and its hash, explicit repository/base/workspace/allowed paths, tests and instructions. The ledger records execution; it cannot expand product scope. Both worker models are explicit activation inputs. The adapter disables nested agents, apps, hooks, remote plugins and web search, uses noninteractive approvals with the normal sandbox, and restricts login to ChatGPT account authentication. It never injects API keys or uses approval bypass flags.

The endpoint for later product execution remains complete FacMan 0.1 engineering/package acceptance, including WinForms and GTK. Human experience, signing and publication retain separate gates.

## Durability and ownership

SQLite uses full synchronous WAL commits and immediate transactions. One unresolved attempt and one effect per phase are enforced in the database. Kernel locks exclude duplicate supervisors for the programme ledger and every admitted clone.

Windows Job Objects enforce kill-on-close, process/memory limits and atomic PROC_THREAD_ATTRIBUTE_JOB_LIST assignment. The process is created suspended inside its Job before resumption. Stored PIDs are not authority to kill processes. Reconciliation opens the exact named Job; absence is meaningful because this host never creates a child outside atomic assignment.

Intent is committed before launch. A failed intent write cannot dispatch. Interrupted coding is fenced, its patch/evidence retained, and the attempt blocked for diagnosis rather than silently repeated. Lost integration responses require authoritative broker observation; apply is not replayed. This prototype does not automatically repair and readmit interrupted coding tasks.

Evidence lives outside disposable clones. Completed stream artifacts are hashed and revalidated on resumption and before assurance/integration. Base, candidate contents, index and Git control metadata are observed. Index/ref/control changes, path escapes and changed authority sources refuse progression. Git observations use bounded owned processes with filesystem-monitor hooks and optional writes disabled.

## Operator controls

Use status, pause-dispatch, resume, drain, cancel-task --task <id>, or emergency-stop, each with --state-root <protected-root>.

| Control | Behavior |
| --- | --- |
| pause-dispatch | Persist pause, let the active process finish, start no subsequent process. Resume retains phase evidence. |
| drain | Finish/reconcile the active task, then claim no next task. |
| cancel-task | Stop owned active work for that task or cancel it before claim; preserve evidence. |
| emergency-stop | Stop owned active processes and prevent dispatch; unknown remote integration still needs observation. |
| resume | Re-enable dispatch within the same admission, expiry and limits. Cannot erase cancellation or enlarge scope. |

Pending integration is polled within an explicit observation budget and programme deadline. A local blocker permits another independent task; an unresolved shared effect retains the writer. Restarting the process resumes its ledger. OS-level supervisor auto-restart is not installed or qualified.

## Resource and security limits

Activation pins executables, protected broker script inputs, runtime files, models, admissions and external qualification records. It supplies session, attempt, process, memory, output, state-storage, free-space, programme-time and integration-observation limits.

Job memory/process limits and captured output caps are enforced locally. Input/artifact space is reserved before dispatch. Time, source drift and storage thresholds are monitored during execution. Monitored thresholds can overshoot between observations or while I/O is delayed; they are not a filesystem quota. Arbitrary worker writes require a separately qualified disposable-volume quota.

Sanitized variables do not prevent same-user file access. The process host is **not a credential/filesystem sandbox**. Before live activation, qualify Codex sandboxed tool descendants, access to coordinator state/authentication files, broker identity separation, temporary roots and volume limits. External qualification records are reviewed trust inputs, not proof this module manufactures.

Session counts and wall time do not establish a dollar cap. Proposed execution uses existing Codex allowance, no API credentials and no purchase authority; actual account allowance/paid usage posture must be settled before activation.

## Integration and remaining work

A live protected integration broker is **not implemented or provisioned by this prototype**. Registered query/apply interfaces are not proof that GitHub integration exists.

The broker must enforce current repository policy, actual base/head/tree, independent assurance, required checks and allowed actor immediately before action. It must stage the candidate into a legitimate task branch/PR, preserve unknown outcomes, observe the actual integrated commit/content, and emit the request-bound receipt. It must reject changed bases rather than silently rebase assured work.

Python broker entrypoints require isolated invocation, protected working directories and explicitly pinned file arguments. Imported dependency closure is an external qualification obligation. Standalone executable brokers must also be protected.

Current FacMan delegated_dev_merge and protected_dev_merge_active are false. Its one completed-unpromoted item limit matters. AIDE has local main and no dev; this implementation creates neither branches nor worktrees. Standing delegation and integration-policy changes require a separate exact reviewed decision.

Fixed pre-admitted bases cannot follow successive changes to the same repository's dev. Before the two-task proof, select genuinely independent admitted repository tasks or implement explicitly admitted dependency-derived base preparation with fresh evidence.

## Verification

The task evidence records 51 passing tests: real Windows process/descendant termination; supervisor death before creation, after atomic suspended creation and after resume; bounded output; persisted controls/claims/intents; failing intent writes; source/index/artifact tampering; active source/storage cancellation; synthetic two-task continuation with real test commands and lost-response reconciliation.

The model and integration boundaries in that two-task test are test doubles. No result claims two real product tasks were integrated. Actual Codex model/auth/sandbox execution, the protected broker and the real two-task run remain unqualified.

Global AIDE validation reports pre-existing portable export checksum/missing-file problems under files/.aide.local.example/. They are recorded, not repaired in this task. Local pilot checks do not make the global result green.

Evidence: .aide/queue/AIDE-BUILD-CONTINUOUS-WORKER-PILOT-01/evidence/.

Official interfaces: [Codex noninteractive execution](https://developers.openai.com/codex/noninteractive) and [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

