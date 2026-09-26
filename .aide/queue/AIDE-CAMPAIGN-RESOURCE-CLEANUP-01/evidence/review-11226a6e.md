# Scoped independent rereview: managed workspace repairs

Reviewer: Codex child agent `/root/partial_recovery_review`. Date: 2026-09-26.

**Verdict: ACCEPT_WITH_NOTES** for exact commit `11226a6e7fd073a599d3f0cb482d6874a6e3d11c`, tree `6ff7a9c6d6b934a1bfb7ee076c52a67034225a16`, parent `5ea1f7cdd53c79a98843a09686ef7bfc7fe9c88e`. The scope is this delta and the two required changes in my preserved `5ea1f7cd` report. I found no remaining material defect in those repairs. This is source acceptance only, not permanent storage activation, packaging qualification, integration, artifact, or release approval.

## Original findings

### 1. Broken scratch alias classification — repaired

`finish_collected` now uses lexical presence before ordinary-path and original-directory identity checks, and uses lexical absence in its final retirement receipt. Broken scratch junctions therefore reach the reparse refusal rather than skipping checks and deleting active evidence. Related active/staging/retention paths also use lexical presence checks.

I repeated the original broken-junction scenario with a tiny retained output and actual `recover()`, using frozen module bodies read from this exact commit. It now refused and preserved the active record bytes, the junction, and retained output:

```text
broken_scratch_refused link/reparse path refused
active_preserved True junction_preserved True retained_output_preserved True
```

The new regression exercises the same boundary after interrupted retirement. The lexical change does not disturb the existing genuinely absent scratch recovery case.

### 2. Source maintainer entrypoint bypass — repaired within the stated boundary

Source `test`, `selftest`, and `eval run` now guard before invoking their work. `current_context` requires actual membership in the exact named Windows Job, reads its ordinary active record, checks job/manifest identity and working root, revalidates declared executable/source/Git identities, requires the source CLI as a bound input, and requires an existing queue WorkUnit record. Environment values alone cannot satisfy named Job membership.

Source export and release generation/validation additionally refuse even after admission because their canonical repository output placement is still unqualified. Their accepted generators are preserved. This satisfies the requested minimum source guard while packaging remains paused.

The bounded probe used mocked bodies that stop before actual work:

```text
source_entrypoints_refused_without_job [1, 1, 1, 1, 1] bodies_not_called True
packaging_refused_inside_context [1, 1] builders_not_called True
portable_test_compatibility 0
owned_fixture_cleaned True
```

The five handlers were source `test`, `selftest`, `export-pack`, `release bundle`, and `eval run`. The admitted packaging case used a simulated successful context only to check that builders remain uncalled. Portable Lite compatibility is deliberately selected when the source execution owner is absent, and the source-only managed-workspace test is excluded from Lite export. Documentation now distinguishes portable commands, source admission, and paused packaging.

## Nonblocking notes and limitations

- **Required future campaign work:** Packaging output placement/reservation still needs qualification. This acceptance authorizes no packaging resumption and does not imply the user's full test/build/package routing objective is finished.
- **Activation condition:** Permanent approved pools and the shared estate control root remain operator placement decisions. No inferred activation or alternate-root authorization follows from this review.
- **Verification boundary:** I inspected the recorded 17-test Windows PASS (22.209 seconds, no skips) and new real named-Job/environment-spoof tests; I did not rerun that suite. The lead's actual small host replay is separate evidence. No full importer, archive, integration, or release verification is claimed.
- **Scope boundary:** The source guard covers these AIDE CLI entrypoints; this is not a claim that arbitrary direct Python calls or unmanaged external tools are intercepted. This rereview did not expand into a programme or scheduler audit.

## Commands and custody

- `git show -s --format='commit=%H%nparent=%P%ntree=%T%nsubject=%s' 11226a6e7fd073a599d3f0cb482d6874a6e3d11c` confirmed exact commit, tree and parent.
- `git diff --check 5ea1f7cd 11226a6e` passed.
- `py -3 -B D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/probe-managed-rereview-11226a6e.py` passed. It loads the exact managed-workspace, WindowsJobHost and AIDE Lite blobs with `git show` into memory, uses one tiny fixture under the explicitly named review parent, and launches no test/build workload.
- Probe SHA-256: `2667438eda710144e94aaf49fffc7ed5c4d2af98d228d679c3b617dccba5ffb7`.

No worktree, clone, system-temp fixture, broad scan, bulk suite, or additional agent was created. The exact created junction and owned fixture were retired. No tracked source, queue file, Git ref, or prior report original was modified by this reviewer. No probe process or fixture remains live; only the small external reproducer and this requested report remain.
