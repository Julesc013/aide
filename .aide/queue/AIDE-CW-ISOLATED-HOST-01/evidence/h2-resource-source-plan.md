# H2 two-API feasibility source admission

Base: 2a44f17eb7232757133df549ac6fc519d535e71b, same reviewed task branch.
ROOT accepted h2-two-api-next-proposal.md for source/injected tests only.
Implement exactly task-owned evidence/h2_system_resource.py,
h2_system_resource_controller.py and h2_system_resource_tests.py. Borrow the
committed ObservationSession, NativeSystemApi and N1 controller read/journal/
Job helpers without editing them. Own ExecPlan/status and root planning/docs
may record this scope. Provider task/index and unrelated histories remain excluded.

Child: immutable eight-file ObservationPlan, two fixed API names, exact native
AMD64/System32 context, bounded pre-paid intent adapter, guarded resource-only
observer and strict result parsing. Parent: fresh exclusive handle-relative
journal, reservation plus both exact mapping intents flushed before child,
fixed Job/input/output/source/expiry bounds, provisional completion and no replay.
No worker wiring or new policy/limit is introduced. The source-only tests use
injected native/parent APIs and never construct an actual native resource backend.

Meaningful tests cover intent/order/ack admission, expiry at dispatch/release/
serialization, invalid tags/unadmitted or differently spelled mapped hosts,
owned releases and no repeat, malformed/mismatched replies, false qualification,
controller durability failure, lost reply, restarted reservation and exact effect
ceilings. Existing observer and N1 tests remain regression dependencies. Freeze
source, complete patch, dependency hashes and exact test commands for independent
review before preparing any real resource effect.

No actual mappings, DLL rereads, images, grants, profiles, network or activation
are admitted by this source slice. The existing interpreter, namespace and
parent authority are trusted probe premises, not an adversarial worker boundary.
The two requests cannot discharge the full 180-name inventory/128 cap, contextual
restricted-loader proof or protected-controller/credential-host qualification.
