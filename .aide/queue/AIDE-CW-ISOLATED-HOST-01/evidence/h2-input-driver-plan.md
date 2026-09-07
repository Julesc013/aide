# H2 eight-file native input driver admission

Continue at observer checkpoint 0c7788fd3660dc18e2751108ac49afe96d446801.
Only task-owned evidence/h2_system_input.py, h2_system_input_controller.py and
h2_system_input_tests.py implement this bounded probe. Existing runtime source
and limits stay frozen. Own task plan, execution/reference documentation and
source/effect evidence may change; provider records and index remain excluded.

Build a read-only child facade using the reviewed NativeSystemApi facts/read
ABI and native no-reparse opens, with no resource mapping methods. Require
native AMD64 process/host, exact System32 path and native local-volume mapping,
exact eight prior public file byte pins, finite input/output/call/clock limits,
and all nine handles held through final facts observation. Close known handles
once even on expiry; stale final serialization cannot succeed. Capture identity,
normalized native path, size/link count, owner SID and owner/DACL hash. These are
observations, not qualified system provenance or a contextual loader contract.

Build a controller that validates exact effect/source/interpreter/user/owned
parent pins; reserves one exclusive handle-relative journal before any child;
flushes intent before dispatch; rechecks admission around child creation and
while running. Existing WindowsJobHost atomically owns the ordinary child with
30-second execution timeout, output/memory/process limits. Cleanup/quiescence has
its own existing limits. Retain all uncertain state without replay/adoption.
No selected DLL maps, private image copies, ACL grants, profiles or network
operations are permitted. The ordinary Python interpreter is existing tooling,
not a qualified restricted tool image. The protected controller/namespace
premise is explicit; source pre-reads do not become OS isolation claims.

First run injected tests only: wrong architecture/root/name/bytes/facts,
malformed input, all-handle ownership, short/oversized reads, operation/time/
output limits, final-cleanup expiry, release failures and durable-intent/
pre-dispatch refusal. Freeze source and exact effect plan for ROOT review.
Actual eight-DLL reads or native facade construction require that later review.
Full 180-name inventory versus unchanged 128 API-row cap, actual resource/context
observations, OS/controller provenance, protected durable journal and restricted
Python loader remain open. No operational activation is admitted.

Primary API references:
- https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getsystemdirectoryw
- https://learn.microsoft.com/en-us/windows/win32/api/wow64apiset/nf-wow64apiset-iswow64process2
- https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfinalpathnamebyhandlew
- https://learn.microsoft.com/en-us/windows/win32/api/aclapi/nf-aclapi-getsecurityinfo
- https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntcreatefile
