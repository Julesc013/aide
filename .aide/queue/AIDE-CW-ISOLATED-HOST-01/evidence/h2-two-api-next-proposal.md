# Next H2 slice: two exact API resource observations

This proposal is outside the frozen N1 checkpoint and authorizes no mapping or
other effect. First complete the exact source3/read-facts checkpoint review.
Then implement and independently test a separate task-owned resource child and
controller, preserving the read-only N1 driver and existing runtime bounds.

Use the independently audited N1 facts as immutable pins for the same native
System32 root and eight files. Bind raw N1 stdout/actual-review hashes and retain
the actual KernelBase.dll spelling. Build a fresh ObservationPlan with exactly:

- api-ms-win-core-path-l1-1-0.dll
- api-ms-win-crt-runtime-l1-1-0.dll

An actual effect would re-open, hash and reobserve all eight pinned objects while
holding their read-only no-reparse handles. It could then attempt only those two
LoadLibraryExW resource requests with the unchanged flags 0x860. No executable
fallback, arbitrary request, directory scan or extra physical host admission is
permitted. A missing host, unsupported return, path spelling mismatch, byte/ID/
owner/descriptor drift or executable-inventory change is a retained refusal.
The original returned resource handle must be released exactly once. A tag0
return is admissible only if its base was already observed in that same ordinary
process before the call; it is not proof of a new restricted-process context.

The parent should own one fresh handle-relative exclusive journal. Before child
creation it must flush the request reservation and the two exact canonical
mapping intents, sequence0 and1, derived from the final plan fingerprint and
fixed flags. Treat the whole request as consumed even if the child dies before
its first mapping. The child journal adapter may acknowledge only those already
persisted exact intents in their one-use sequence; it cannot create authority or
change targets. Parent input transfer uses the existing exact inherited stdin
handle. The parent retains its exclusive journal handle until the owned child
quiesces. Final completion remains separate from the provisional journal rows.

This gives concrete write-ahead ordering and object custody for a trusted,
reviewed ordinary probe. It does not qualify an adversarial same-user worker or
prove a production protected-controller boundary: installed interpreter, source
namespace, parent process/handle authority and protected journal authenticity
remain explicit premises. If those premises are insufficient for this particular
finite feasibility experiment, first implement the missing parent/child authority
mechanism; do not re-label synthetic acknowledgement as qualified protection.
No production broker or worker wiring belongs in this experiment.

Retain finite source/interpreter/parent/expiry checks around child creation and
through execution. Use a fresh named Job with process1,256MiB and30-second child
execution limit,25-second internal observation duration and bounded stdout/stderr.
All native adapter calls and output remain under existing limits; cleanup has its
separate existing bound. No profile, private-image copy, package grant, network,
provider call, credentials or operational activation is involved. Preserve the
old consumed N1 generation unchanged. New actual effects require the exact
source/test/effect packet and independent ROOT review first.

Source tests must prove reservation and both intents are durable before dispatch;
wrong digest/name/sequence/missing intent cannot map; a consumed request cannot
restart; expiry/source drift at each boundary refuses; lost reply is terminal;
only a prior executable base or tagged resource can be attributed; backing facts
and exact observed spelling must match; every acquired read/resource handle is
released once even after guard/output failure. Reuse the existing observer tests
and add controller/journal denial tests. Native APIs stay injected during this
source stage. The actual result may be PASS or a bounded ABI/resource refusal;
either outcome must preserve raw evidence and drive a specific next repair.

Two observations are a feasibility subset, not partitions that satisfy the full
180-name API inventory against the unchanged128-row cap. No complete transitive
closure, OS trust, actual restricted Python bootstrap or loader/context
qualification follows from them. The next operational dependency remains an
exact full closure/admission decision and a separately reviewed private Python
image/denial launch, followed by Git/Codex/model and broker-host work.
