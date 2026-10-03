# Scoped host qualification

## Objective and scope

Complete one necessary AIDE repository validation through the installed scoped
command host, supervised by the existing known-good Windows job/storage owner.
Use only task.yaml paths and existing D storage. Source/bootstrap edits remain
explicit controller actions; they do not establish outer-session containment.

## Plan

1. Pin the existing exported runner, its process owner and installed Codex/Python
   executables. Reuse the configured local storage and finite budgets.
2. Add a task-local qualification adapter around the existing WindowsJobHost.
   It supplies a command-local Codex permission profile; it owns no independent
   process, allocation, reservation, retention or cleanup mechanism.
3. Exercise tiny allowed/denied writes under the owned scratch fixture. Check
   actual Windows identity and membership in the supervising Windows job.
   Refuse the real workload if the expected boundaries are not observed.
4. Run the necessary repository validation and local read-only Git check through
   that same path. Preserve complete bounded logs in the existing retained root;
   return only a compact status, failures and evidence references.
5. Record resource observations and retirement, existing aggregate-cap gaps,
   uncovered routes and any actionable host incompatibility. Review and commit
   exact evidence. Do not claim global containment or automatic dev integration.

## Dependencies and blockers

Current source: dev 1431d394. Configured D owner has no active job and empty
scratch. The installed Codex 0.145.0 supports `sandbox [OPTIONS] [COMMAND]` and
command-local named permission profiles. An absolute Python 3.14.7 invocation
worked under a read-only profile. Its inherited USERNAME is not token identity.
No live model permission is required or granted for deterministic sandbox use.

The current controller's shell and editor tools are unrestricted. Plugin and
external GitHub operations have separate controls. The managed disk threshold
is monitored, not a hard filesystem quota. Current runner retention checks are
per job; an aggregate lifetime cap has not been established. These are required
remaining product gaps, not reasons to relabel this local qualification complete.

## Recovery and idempotence

Use the runner's active receipt and recover command after interrupted owned
work; never allocate a replacement before reconciliation. One job at a time.
Negative write fixtures remain entirely within that job's owned scratch.
Changed code, profile, executable or source requires a newly bound subject.
No automatic replay of an uncertain effect. No new cleanup implementation.

## Progress and discoveries

- [x] Initial state and existing configured storage observed without mutation.
- [x] Installed permission-profile syntax confirmed and Python read probe passed.
- [x] Broad intent compiled; bounded child scope and branch plan recorded.
- [x] Frozen supervisor pinned to all 23 accepted exported Python sources;
  worker identity, membership and write boundaries observed. Requested read
  exclusion failed and remains recorded.
- [x] Real validation exited 0 with 4/4 unchanged resource regressions, aggregate
  boundary check, local Git check and verified retirement. See evidence/outcome.md.
- [x] Initial failed candidate committed as f286d266; correction and exact
  outcome prepared for a second structured commit.
- [ ] Independent review and remaining normal-entry/read-isolation closure.

## Validation record

Initial unrestricted `doctor` and `validate` returned an overall zero shell exit
with extensive PASS output. Their megabyte-scale response was truncated by the
tool, and separate command exit codes/full retained evidence were not captured.
This is insufficient containment evidence. The scoped run must retain its own
complete bounded result and individual exit codes.

Final scoped job 4afa5608 retained complete logs (4,894,501 bytes), validation
exit 0, four unchanged regressions without skips and an explicit PARTIAL scope
observation. The entry narrows the finite envelope and checks aggregate retained
capacity under the existing shared lock. The original configuration and ZIP
stayed unchanged. Production runner source and outer editor/plugin routes were
not changed. The repository-only validation was admitted independently under
the observed write/process boundary, without private inputs or a model/network
operation; it does not accept the failed read-isolation profile. Supervisor
bytecode pollution was demonstrated, corrected and exactly retired before PASS.
