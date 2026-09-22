# H2 bounded image preparation source review

The three-file source slice prepares admitted bytes. It does not qualify a
Python/Git/Codex toolchain or install a host. The frozen manifest binds the exact
source, complete patch, unchanged dependent inputs and final 63-test receipt:
26 image tests, 27 H1 security source regressions and 10 actual Windows Job tests.

Admission binds immutable native source/parent identities, literal paths, exact
sizes and SHA256s, a specific package SID and independent entry/byte/time budgets.
The separate 64 KiB stream API permits at most 512 MiB per file, 768 MiB per image
and 2,048 entries. Existing H1 and candidate 16 MiB limits remain unchanged.
Source handles refuse write/delete sharing and reparses; copying checks identity,
single-link ordinary-file metadata and bytes. Only complete copies can be sealed
and granted. Error paths close owned handles and retain all created objects.

Journal FILE_CREATE is relative to the exact held parent handle. The CRT adopts
that handle with O_NOINHERIT; it never reopens a DOS pathname. Both handle-transfer
failure branches close their owned resource and retain the empty reservation.
The initial intent is durable before relative image-root creation. Root sealing
also retains its exact parent handle. Existing reservations always refuse,
including after real abrupt process death before creation or during copying.
There is no cleanup, adoption or automatic retry API. Expiry remains enforced
through the final durable flush and observations.

Normalized NT names obtained from held handles support conservative overlap
refusal, alongside native object IDs. They are not a namespace lock or authority
substitute. Root components reject Win32 aliases, devices, malformed Unicode and
UTF-16 overflow while preserving valid spaces/Unicode. Actual 8.3 equal/nested
source-output aliases refuse before reservation. Literal DOS mapping observations
remain separate from relative object creation: an injected change immediately
after the pre-dispatch guard still writes the journal only through its held
parent and refuses image creation. No actual drive mapping was changed.

The 26 H2 tests use ordinary synthetic files, real native relative journals,
actual reads/writes, a 16 MiB-plus stream, empty streams, concurrency and two real
abrupt subprocess deaths. Image creation/sealing/grants in preparation tests are
explicitly modeled. Their relative-parent contract is tested with mocked native
calls. These tests do not qualify native image ACLs or executable loading. The
journal non-inheritable flag and handle-transfer failures are directly observed.

Independent review identified two P2 findings: NT/Win32 ancestor spelling and
short-name source/output overlap. Both are remediated in the current source.
The two original source/patch/test/reproduction packets remain byte-for-byte in
h2-before-root-alias-evidence.zip and h2-before-overlap-evidence.zip (12 members
each, with maps). Both reviewer's original retained fixtures remain untouched.
Earlier source-alias/final-flush deadline RED logs are also retained. No source
bytes changed during the final 63-test run.

A protected controller must supply the current guard and qualify source/store
namespace and descriptors. Synchronous kernel I/O still needs an outer owned
process to enforce a wall limit if a call stalls. PreparedImage is conditional
on that protection and does not itself qualify future worker launch paths.
H2 actual tools, generated library bytes, private image grants, loaded-module
closure and an isolated runtime run remain unqualified. No H2 profile, package
grant, real tool copy or AppContainer effect is authorized by this source packet.
H1's four consumed effect packets remain immutable and native-only.
