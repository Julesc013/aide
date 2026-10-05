# Managed commit prevention: implementation and qualification

AIDE now has a qualified ordinary local commit path that rejects malformed
messages before creating a candidate or advancing the branch. The exact source
commit and any subsequent branch delivery are certified by their terminal
records under `evidence/`; stable publication remains a separate campaign gate.

## Behavior delivered

`commit create` defaults to preview. Apply requires the exact final message digest,
branch, parent, staged tree and finite staged-file scope. It invokes the existing
strict checker directly; historical dispositions cannot approve a new message.

The operation owns an exclusive index lock, creates an unreferenced commit object
and verifies its message, tree and ordered parent. Git then prepares a normal
dereferenced HEAD transaction. AIDE verifies the exact direct branch and staged
inputs while Git holds HEAD and branch locks, then sends commit. Both normal
reflogs remain intact. Staged and unstaged file bytes are preserved.

Changed inputs, unknown locks, active hooks/signing/fsmonitor, unsupported Git
environment overrides and non-normal Git operations refuse specifically.
Lost transaction acknowledgement returns uncertainty and preserves the candidate.
Unconfirmed child reaping also preserves the owned index lock. Recovery never
automatically resets, amends or repeats the operation.

Public test fixtures use existing authenticated job storage and retirement.
Only permission errors reading the exact active metadata record can retry,
three attempts over at most100ms before allocation. Complete authentication
still must succeed; persistent denial, another filename or identity failure
refuses. The earlier Windows permission error's underlying cause is unknown.

## Evidence

| Check | Actual result |
|---|---|
| Native job `dc7003a7132647ceaf3fa5ef128134a1` | Parent and worker exit0 |
| Real Git/API/public CLI cases | 49 passed |
| Original Q27 regressions | 23 passed; source/assertions unchanged |
| Failures, errors, skips | Zero |
| Repository `doctor` | Exit0;73 PASS |
| Repository `validate` | Exit0;60,911 PASS |
| Capability classification refresh | All13 records/classifications unchanged |
| Native collection | All six retained files and both collection digests verified |
| Retirement | Scratch absent; reservation released; active/.next absent |

Acceptance binds `native-result-v7-passed.log` with the original parent journal
`native-invocation-v7.log`. Earlier failed jobs and rejected reviews remain
available against their original subjects. The corrected task brief and source
classification reports have separate structural evidence. Full validator output
is retained losslessly as compressed logs, with raw and compressed checksums.

## Resource and execution scope

The job used the unchanged pinned execution component, existing configured D:
storage and finite limits:16MiB scratch,1MiB retained output,2GiB Windows Job
memory,600 seconds and32 processes. The shared256MiB admission remains cooperative
and monitored; it is not a hard filesystem quota.

Measured final-job retained data was17,206 logical bytes. Sampled scratch peak
was29,856 bytes; peak process memory was322,293,760 bytes. These are this job's
observations, not a summed campaign peak or actual disk-space recovery.

The controller, editor and plugin routes remain unrestricted. Read isolation
and whole-session containment remain unqualified. Native tests made no model
calls; controller/reviewer usage is not measured here, so no total-cost or matched
efficiency improvement is claimed. Wider historical disk reclamation is separate.

## Source, documentation and delivery

Changes are bounded to the shared commit core, public CLI, meaningful regression
tests, commit policy/reference documentation, task/intake records and root plan,
implementation and documentation indexes. An independently admitted extension
refreshes exactly four existing capability reports, binding41 current source
inputs. `CURRENT` means source-byte consistency, not functional qualification.

The new path is exercised on real disposable Git repositories and must also
perform this task's necessary normal source commit. The queue completion and
branch-sync terminals retain actual object identities; the report does not invent
a future commit or tag identity. Other branch tips and tags must be preserved.

## Remaining campaign gates

- Eleven exact historical-message decisions remain proposed, including published
  `66b66938`. No published history is rewritten.
- The bounded live GPT-6.1 Sol attempt and matched-outcome efficiency evidence
  still require their respective permission and measurements.
- The actual outer-client configuration must constrain its enabled routes and
  demonstrate a useful normal workflow. Worker success does not close that gate.
- The four held release assets are unchanged. They do not contain this new
  command/core. An affected payload refresh and exact release review precede
  publication, downloaded-asset verification and supported consumer checks.
- Existing broader compatibility, checkpoint, conformance, dependency-invalidation
  and host work stays under its current queue plan. FacMan product work stays paused.

This increment closes the preventive commit defect within its tested managed
path. It does not certify a stable release or a contained whole AI session.
