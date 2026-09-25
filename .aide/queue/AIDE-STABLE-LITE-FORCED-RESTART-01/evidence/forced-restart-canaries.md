# Delivered Lite forced-process-exit qualification, 2026-09-26

## Frozen subjects and custody

- Source baseline: `dev@493e3f13c1b2e754dd8fb5f533380ba13a7b8979`,
  tree `c300dad82420b159876c5eb708c5b48de54254a4`; bounded admission
  branch `5f2441d18772188db4095c089a18f3293f1fda3e` is evidence-only.
- Local delivered ZIP SHA-256:
  `68f8b3cc07c6476999828577c59bdb8785d13509613d0351a617908c99fa784c`.
  Extracted CLI SHA-256:
  `bd0f41aa987174be44732e615da8069b7770b5b92fed6e07d46a534dfe0c1752`.
  The same audited extractor helper SHA-256 was
  `3f3140807520b1481181c34e95e06273e2774698cf2d384e42b5b6214f58a181`.
- External originals are under
  `D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/`.
  No product source, generated archive or arbitrary target was changed.

## Observed exact effects

| Run | Script SHA-256 | Summary SHA-256 | Observation |
| --- | --- | --- | --- |
| `run-493e3f13-final` | `b7b7e1e99bfe7dba94fcd7809610dd65170f3df063e8ef800a2ec6e82ba29544` | `0b2203d9580f708f2246649e713775426ab1b1da9841bb6fd78ebb2513134769` | Three child processes exited 77 immediately after import receipt, owned repair file, and removal receipt effects. Fresh extracted CLI classified pending import/repair and returned `RECOVERED`; external archive CLI returned `DETACHED_RECOVERED` after removal had deleted its in-target runner. Authored guidance and project bytes matched the computed post-removal oracle. |
| `run-rollback-493e3f13` | `a0362503d172043ec3e30f597936d09af48092b81139e751aae3748b97695c53` | `7abdde53065c8d0af2fc4ef9abea41f5b09ea76267f87b0f7cc9929826fcbdd8` | Child exited 77 after rollback receipt publication. Fresh `rollback-pack` reported `RECOVERY_REQUIRED/completed`; fresh `import-pack` with the exact predecessor/current pair returned `RECOVERED` and preserved project bytes. Successor was a synthetic checksum-valid fixture, not a published release. |
| `run-partial-493e3f13` | `ae514d3e43fe06a74e64bd7277e43bc665c8051adfc8beaabd19fd627277059e` | `0aea5792c668e9a622954a8289f35ba63644987e393e6e76ed61e902e448ca62` | Child exited 77 after the first fresh import payload. The intent survived; fresh preview and apply returned `RECOVERY_REQUIRED`, classified `partial`, and changed no target bytes. Project-owned bytes survived. Automatic completion or rollback of this partial state remains unqualified. |

Each summary was parsed and rehashed. Child logs and markers were rehashed;
their recorded exits were 77. The first combined run failed because its oracle
tried the in-target CLI after full removal had correctly deleted it. Running
the extracted CLI on that same interrupted target returned
`DETACHED_RECOVERED`. The second combined run reached recovery but its oracle
expected `AGENTS.md` to equal preinstall bytes without the managed-section
separators; actual bytes preserved the authored prefix. Both failure files and
logs remain in `run-493e3f13-first` and `run-493e3f13-corrected`. The final
run uses the computed exact post-removal byte oracle.

## Limit and next action

Independent reviewer `/root/customization_review` (`BLACKGLASS-WIN1\Jules`)
issued **ACCEPT_WITH_NOTES** for the local canary evidence only in
`D:/Projects/AIDE/_review_scratch/stable-lite-forced-restart-20260926/independent-forced-exit-canary-review.md`,
SHA-256 `bbdccecd9f7c885a30eb1b6528e355938bdbc959ff70a2a0443ed56e7e6f0dbf`.
The reviewer independently audited child logs/markers, 811-entry receipts and
810 managed-file hashes, authored/project bytes, the removal byte splice,
rollback lineage and the partial safe refusal. The report grants no `dev` or
release effect GO. Keep its original outside the repository.

These are local preview artifacts on one Windows/Python environment, with
process exit injected immediately after delivered API effects. They do not
prove arbitrary kill timing, hostile concurrency, OS network isolation,
published bytes, a real prior release, or a full release profile. Partial
import currently refuses replay safely and remains pending; implement and
qualify a bounded exact recovery path or record a supported manual recovery
guarantee that actually closes the stable contract. Obtain independent review
of these exact canaries and then route that gap to a source WorkUnit.
