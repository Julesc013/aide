# Revised system observation source review boundary

Final source2 at base 236da6c2 adds the unconnected observation module and 37
direct injected tests. All 138 selected tests pass in 4.958 seconds, including
unchanged 101 PE/recipe/image/security/owned Job regressions. Source2, dependency15
and excluded working index remain unchanged across this run. The complete new
file patch includes both untracked files; ordinary git diff omits these paths.

The original source, 133-test run, manifests, notes and concrete review REDs are
retained exactly in h2-system-before-review-evidence.zip, with its separate
custody map. The final-guard RED demonstrated success after cleanup consumed
expiry, moved the clock or revoked the guard. A separate pre-call RED dispatched
one injected mapping after the guard consumed expiry. Huge integers raised an
untyped OverflowError, and a modeled case-different native mapping could inherit
a held file's identity without exact native spelling agreement. These are
historical failures, not actual native/System32 attacks or mapping effects.

Repairs check finite clocks both before and after every guard; final serialization,
size and freshness checks run inside retained failure handling after all cleanup.
Cleanup still releases known owned handles once even when guards have expired;
it never retries a release or an already consumed request. The exact mapped
native spelling must agree with freshly observed held facts, after the coarse
canonical pin match. Arbitrarily large temporal integers refuse as typed input.
The five added test methods exercise these boundaries with multiple injected
clock/guard/serialization/name cases and assert no extra dispatch or cleanup.

The plan snapshots native root/file facts, hashes and finite requests. Explicitly
pinned system hard-link counts do not change private ImageFile single-link rules
or any current recipe/candidate/H1 cap. Reservation acknowledgements equal the
exact plan fingerprint; mapping acknowledgements equal SHA256 of the exact
canonical intent. They are externally protected journal contracts, not proof of
an implemented durable store. A new process needs that journal to reject a
consumed reservation; this module does not itself qualify cross-process recovery.

Native mapping has one fixed resource-only flag combination. The native adapter
is never constructed by tests; its loader calls are injected mocks. Resource
handles are registered before post-call checks and released exactly once. An
executable-tag result requires the immediate pre-call executable base and an
unchanged before/after inventory; there is no executable-load fallback. All
synchronous native/journal calls still need an owned outer-process deadline.

No actual inspected DLL/API mappings, tool copies, grants, profiles or isolated
Python launches occurred. The 180-name API metadata superset remains above the
128-row cap. Actual OS/native ownership, contextual API hosts, complete transitive
inputs and restricted loader proof remain open. Successful result bytes retain
system_ownership_qualified, api_context_qualified and loader_qualified as false.
