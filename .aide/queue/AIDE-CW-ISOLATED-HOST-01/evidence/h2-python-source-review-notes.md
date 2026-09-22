# H2 Python source review boundary

Current source is exactly h2-python-source-manifest.json: eight authored files
at 06f2546f, aggregate c87493f3855f5356f1de47295d9eb4ca833adb943b1e04062fa4badf14dd99ab.
The complete patch includes all six new files plus the two tracked image changes.
No source changes are planned during independent review.

## Implemented and tested

The pure AMD64 PE reader bounds bytes, sections, directories, mapped extents,
imports, delay imports and export forwarders. It refuses missing terminators,
ambiguous/truncated mappings, unsupported delay/bound imports and escaping names.
It is a bounded dependency-metadata reader, not a complete Windows loader validator.
Function thunk contents, dynamic LoadLibrary calls, symbol implementation and
runtime code behavior are not qualified by this parser.

The pure SystemContract requires an exact Windows build, literal native System32
root, root/module volume and object IDs, SHA256s, physical names and named API-set
hosts. It accounts for every parsed import/delay/forwarder under 64 module,
256 MiB input, 128 API-set and 4,096 edge bounds. Physical cycles are traversed
once. The three private Python inputs must be reachable from python.exe; direct
system requests stay within the proposal's exact 18-name set. Every declared
system input is validated, including explicitly admitted inventory not reachable
from the bootstrap executable. Both reachable and inspected module sets are
reported. No generic Windows-directory or API-set wildcard is accepted.

These are controller-supplied data bindings. They do not authenticate the issuer,
prove native system ownership, establish actual API-set contextual resolution or
prove which DLLs the eventual restricted loader uses. The resulting manifest
explicitly sets loader_qualified and system_ownership_qualified false. Actual
closure may exceed the bounded supported metadata subset; that must refuse and
be resolved from concrete evidence, never treated as automatic readiness.

The library builder validates exact immutable member bytes and produces a sorted
ZIP_STORED archive with fixed metadata plus exactly python314.zip and dot on
separate LF lines in python314._pth. It admits no site hooks, bytecode or ambient
paths. Named bootstrap members are necessary data, not proof that their source
imports work. Synthetic members are inert fixtures, not an executed standard
library. A real 721-member candidate inventory previously observed remains to be
frozen/rechecked and tested under the restricted interpreter.

ImagePlan v1 value, source identity and fingerprint are preserved. Version 2
requires explicit source_file/generated_bytes tags. Generated inputs have exact
path/size/SHA256/producer admission and no invented file ID. The fixed _pth hash
is checked at plan read; all immutable derived payloads are checked and captured
before native leases or the write-ahead reservation. Both kinds use the same
held-parent journal/root, bounded stream, all-copy/all-seal/then-grant protocol.
Failure retains the consumed generation and any partial bytes; there is no
pathname cleanup, adoption or replay. Existing image/H1/candidate bounds remain.

## Exact test evidence

h2-python-final-tests.json binds all eight source files and seven dependencies,
including the unchanged provider-only index state. 95 tests passed in 4.728 s:
7 PE, 7 library, 11 named contract, 33 image, 27 security and 10 actual Job tests.
The image tests create ordinary disposable files/journals and use real Windows
read handles/stream writes, while image root creation, sealing and package grants
are explicitly modeled. Actual Job tests prove only their existing process
containment conditions. None created a private real-tool image, granted a package,
created/adopted a profile or launched Python in AppContainer.

The first library run retained a real synthetic input-map mutation failure.
The corrected builder captures validated immutable byte references before the
archive writer; the mutation regression now preserves the admitted bytes.
The pre-fix source and RED log remain in task evidence. A wrapper's default text
encoding error during a document update is separately retained; the remaining
UTF-8 document update was retried without repeating source or native effects.

## Next required qualification

Before an actual image effect, freeze the real private source identities/hashes,
selected .py bytes and deterministic outputs, exact Windows system/API-set
observations, image plan, guard budgets, target package identity and native/Python
probe binaries. Bind the same system contract to observed loaded paths/identities
and dynamic bootstrap needs. The first restricted Python command will use -I -S
-B and fixed trusted inspection code for encodings/json/os, sys.path/prefix/flags
and module origins. It also needs protected canary/controller denials and owned
scratch proof. Unexpected paths/imports are retained failures. Git/Codex loading,
model egress, credentials and operational worker activation remain separate.
No current source PASS authorizes those effects.

## Additional read-only actual-host observation

Subsequent read-only inspection of eight public Windows DLL byte streams found
five refusals of the deliberately unbound-only delay policy and three metadata
passes. Exact file hashes and raw delay fields are retained in
h2-python-system-pe-readonly-inspection.json and
h2-python-system-delay-readonly-details.json. No inspected DLL was loaded or
mapped, no image/ACL effect ran and all frozen source stayed unchanged. The next
bounded compatibility and native input observation plan is
h2-python-native-input-next-proposal.md. This concrete refusal remains open
before any actual Python runtime qualification.
