### Proposed narrow canonical-output amendment

**Demonstrated need, before any job:** the existing runner accepts `.aide/release` but does not accept its existing `stable` subdirectory as a separate canonical destination. The whole release tree currently contains 8,302,222 bytes, including preserved packs and acquired copies, against the unchanged 8,388,608-byte canonical limit. The eight immutable stable assets occupy 4,144,109 bytes. New versioned archives need additional space under the existing `stable` directory. The initial draft manifest correctly refuses its unrecognized narrower destination. No allocation, build, asset write or export mutation occurred.

**Smallest coherent change:** extend the existing owner, retaining all limits and storage locations.

1. Add literal `.aide/release/stable` to `CANONICAL_OUTPUT_PATHS` in `core/execution/managed_workspace.py`.
2. Let `require_canonical_outputs()` recognize a requested approved destination covered by a declared approved ancestor. Validate both requested and declared names against the existing literal allowlist; reject unknown/traversal names. A child declaration cannot satisfy a broader parent request. Existing whole-release declarations continue covering stable operations.
3. Change only the stable-build and stable-validate command guards in `aide_lite.py` to request `STABLE_RELEASE_DIR`. Leave broader release/export/changelog command requirements intact.
4. Add focused methods beside the existing managed-workspace tests for exact stable custody, ancestor compatibility, parent/outside/traversal refusal, unchanged quota/volume accounting and both stable CLI guards. Preserve original test bodies and relevant native reservation/overrun/recovery assertions.
5. Run one separately reviewed bounded regression/export allocation, refreshing the existing generated pack through recoverable Git ownership after test success. Reuse unchanged release/lifecycle evidence by exact dependency identities. The actual archive build then receives its own fresh source/effect review.

**Scope amendment:** allow only the existing workspace module, Lite CLI, managed-workspace test file, owned export and four existing derived capability reports, alongside the already admitted paths. No new execution backend, policy store, storage root, pagefile, privilege or provider. Keep the 8 MiB canonical limit, other caps, 4 GiB physical/commit and 10 GiB disk reserves unchanged. Existing archived evidence remains in place.

**Finite allowance amendment:** propose thirteen local allocations total: one narrow regression/export group plus the original twelve planned build/consumer/predecessor/replay ceilings; zero are consumed. At most one export regeneration, justified by these changed portable source bytes. Every allocation, refresh, build, push and hosted effect remains separately reviewed. The earlier twelve-job admission is preserved; this document is not execution authority.

**Acceptance:** independent technical approval of this exact amendment precedes implementation. Later exact source/fixture/export review must prove the narrower destination's custody and refusal behavior, preserve legacy ancestor behavior, and bind actual code/pack identities before any versioned build. Do not widen the whole-release byte allowance or delete preserved material to manufacture admission.
