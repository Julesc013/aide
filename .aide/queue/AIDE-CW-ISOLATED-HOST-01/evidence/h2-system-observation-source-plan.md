# H2 system observation source slice

Continue from 236da6c2 under the existing host task and ROOT's reviewed source
authority. Add core/runtime/continuous_worker/windows_system_observation.py and
.aide/scripts/tests/test_continuous_worker_system_observation.py. Update only this
task's scope/status/ExecPlan/evidence and the required root planning indexes.

Implement a typed finite exact-name observation plan. Pin native System32 root,
root/file identities, exact size/hash, owner SID and descriptor hash; distinguish
read-only system hard links from unchanged private ImageFile single-link rules.
Hold no-reparse, read-only, no-write/no-delete-sharing root/file handles. The
observer checks the exact facts; a caller-provided pin does not itself establish
OS authenticity or protected controller authority. No directory scan or wildcard.

Keep current 16 MiB/file, 256 MiB aggregate, 64 total recipe modules and 128 API
rows. Bound individual reads to 64 KiB, native observation calls to 8192, result
bytes to 2 MiB and elapsed execution to 120 seconds. Each call consumes its count
before invocation, checks a finite expiry and monotonic deadline, and rechecks
the controller guard afterward. Native synchronous calls also require the later
owned outer-process deadline; polling is not an independent wall-time guarantee.

The one-use session requires controller journal reservation before native calls
and request-bound mapping intents before each mapping. Callback acknowledgements
are explicit externally protected journal contracts, not proof of durability in
this source slice. Absent, failed or ambiguous acknowledgements refuse dispatch.
A failed or incomplete mapping never retries. Returned resources are registered
for exact owned release before a post-call guard can fail; cleanup releases each
known acquired handle once and records uncertain release outcomes without retry.

The injectable native backend uses only LoadLibraryExW with fixed flags
LOAD_LIBRARY_SEARCH_SYSTEM32 | LOAD_LIBRARY_AS_DATAFILE_EXCLUSIVE |
LOAD_LIBRARY_AS_IMAGE_RESOURCE. It never accepts flags from workers or falls back
to executable loading. A returned executable handle is accepted only if its base
was present in the immediate pre-call process inventory. K32GetMappedFileNameW
must give a complete native path matching one held admitted physical file;
reobserve the exact root/file facts before accepting the result. Unexpected new
executable modules, out-of-root paths, changed identities/descriptors, unsupported
handle tags and incomplete mappings refuse. FreeLibrary releases only the exact
returned owned handle; read handles close separately in reverse acquisition order.

Direct tests use only injected native/journal operations: expired and exhausted
budgets, root/file drift, hard-link versus private rules, malformed/truncated
paths and hashes, wrong handle origin/tag, intent-before-effect and ambiguous
response handling, guard failure after acquisition, exact cleanup ownership and
release failures, empty/duplicate/over-limit declarations, source binding and
result limits. No actual observed DLL loading/mapping, private image copy, ACL
grant, profile or isolated interpreter effect is admitted. Preserve the full
180-API-name metadata inventory and unresolved 128-row/contextual-loader gap.

Official contracts: https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibraryexw
(resource-only flags, prior executable mappings and exact FreeLibrary ownership);
https://learn.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-getmappedfilenamew
(backing mapped name and truncated-buffer refusal);
https://learn.microsoft.com/en-us/windows/win32/apiindex/windows-apisets
(API contract names are not physical DLL names). These guide the implementation,
not a claim of actual contextual API resolution. Freeze exact source and direct
meaningful tests for independent review before preparing an actual effect packet.
