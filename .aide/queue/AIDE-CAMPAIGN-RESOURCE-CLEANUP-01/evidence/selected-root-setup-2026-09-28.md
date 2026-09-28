# Selected-root setup source validation

- Owner selection: the three shared D execution roots recorded in the task;
  both existing checkouts use one control root and finite local limits. This
  source increment adds a bounded setup entry point to the existing runner.
- Scope: `core/execution/managed_workspace.py`, the existing `job` CLI,
  managed-workspace tests, the local example and runner reference. No new
  workspace, global setting, release asset or `dev` change.
- `job setup` against each already configured checkout returned
  `ALREADY_CONFIGURED`, `writes: false`, with unchanged config hashes.
  Observed config digest: `217a27d429c199879648dde2c943026d37ea6fc52d9d80d5add98ad21fed20f1`.
  Both config files remained SHA-256
  `019669f8faab4ea4e410079ea96966b16742f0e7c6d2e062246a092f1b862834`
  after the final-source setup invocation.
- Final source-input managed job `4c93fecbc9544747902b5225e0f16db3`:
  `python -m unittest discover -s .aide/scripts/tests -p test_managed_workspace.py`;
  **35 passed**, no skips, 29.577 seconds. Exit 0, quiescent; 240,201,728
  byte peak Job memory, 280 byte peak scratch. Scratch absent and reservation
  released. The retained D receipt binds the input hashes and environment.
- Six focused setup cases passed separately in job
  `81d91c90b29347fb8f90441d211e618a`: creation, read-only idempotence,
  shared populated roots, capacity refusal before and after directory creation,
  escaping/unknown/changed state, and real Windows junction refusal.
- `git diff --check` passed. `git plan` classified the current dirty task tree
  as requiring classification; all ten changed paths are task-scoped.
- Limits: tests use tiny synthetic roots and mocked capacity; Windows process
  and memory monitoring remain existing runner behavior. The frozen 1.0.0
  asset hashes and main/tag/publication gates are unchanged.

## Commit-bound result and independent review

- Frozen source `5152798b934a498d9ec6e20986263412a0d7c068`, tree
  `cb9869a8d64cd3d4f978114a0f014f9375ba2e58`, parent `76e17a4c`.
  Commit-message check passed; the source commit leaves the worktree clean.
- Managed D job `48c84ef70d2c494bb46a4ec7079532d5` bound that exact commit,
  tree and input hashes. The full managed-workspace suite passed **35 tests**
  in 23.112 seconds, no skips; exit 0, quiescent. Peak Job memory was
  239,271,936 bytes; peak scratch was 280 bytes. Scratch was retired and the
  shared reservation released.
- Independent reviewer `/root/stable_builder_repair_review` gave
  **ACCEPT_WITH_NOTES** for source integration of that exact commit/tree.
  It inspected the diff, source, tests and evidence read-only and did not
  rerun tests. No blocking defect was found. Real checkout setup exercised
  the unchanged-config path; fresh setup uses tiny synthetic roots.
- Integration decision: preserve `dev@76e17a4c` and the previously accepted
  Lite asset freeze while its main-promotion gate remains unresolved. This
  setup source is qualified on its task branch. If included in the release
  source before publication, it requires a separate exact release delta
  decision and current-source asset/consumer qualification.
