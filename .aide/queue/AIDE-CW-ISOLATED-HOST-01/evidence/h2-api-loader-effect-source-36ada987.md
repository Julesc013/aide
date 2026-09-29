# Bounded API-set loader effect source, 2026-09-29

- Source commit: `36ada987bfe075b3bd903818b9cf1f17f01aadf0`.
- Source tree: `981631eea0ef36fc27244ad25e50981dd2f71384`.
- Parent `dev`: `6795abab31b41963b8aa5ab1b0eedcd997f13a26`.
- Scope: one-name ordinary loader effect controller and injected tests. The
  accepted native adapter remains byte-identical. No effect manifest was
  created, no native load occurred, and no worker activation was admitted.
- D-managed loader test job `5471f910226a43b1a7d4bfd4a10e6847`: 9/9,
  exit 0, peak memory 29,831,168 bytes, peak scratch 252 bytes. Receipt SHA-256
  `4f3ffa7a59203dd42781ea955709f10b7cb363e7a9a3c5528a01ece02d54001c`.
- D-managed query regression job `24a8adaf4fe740dab2a233ba946f06ed`:
  10/10, exit 0, peak memory 29,507,584 bytes, peak scratch 255 bytes.
  Receipt SHA-256
  `45e7ff278d5ed8de7f8fbb070d72a7ccdb06b00e99df0f7bcd9b7e1811520dc7`.
- Both managed jobs used `.aide.local/execution.json`, released reservations,
  and retired their job scratch. Their bounded logs and receipts remain under
  the configured D: retained root. Source inputs, toolchain and environment
  identities are in the receipts.
- Direct affected suite: `py -3 -B
  .aide/scripts/tests/test_continuous_worker_system_observation.py` passed
  59/59 after reverting the attempted change to the reviewed adapter.
- `py -3 -B .aide/scripts/aide_lite.py commit check --latest` and
  `git diff --check` passed.

Independent `/root/native_os_build_review` returned **ACCEPT_WITH_NOTES** for
source preservation/integration of this exact commit and tree, after checking
the shared D control journal, distinct result names, input pins, one-name
contract, OS-build gate, durable intent, query defaults and accepted adapter
identity. The reviewer did not run a native effect. Its noted follow-up is an
explicit different-output replay test before any actual effect admission; the
same shared request-ID journal already blocks that replay structurally.

Any future native effect needs a separately pinned finite D job, exact effect
review and admission. An ordinary DLL load may execute initialization or
dependencies, or reuse already loaded state, before the returned module path
can be observed. A result path is not host-byte trust, restricted execution or
worker qualification.
