# Next H2 qualification slice: bind the real Windows/Python inputs

Current Python recipe source is frozen for review. This proposal identifies the
next concrete compatibility and observation work; it does not authorize actual
private-image copies, package grants, profiles or restricted Python launches.

## First resolve the observed parser subset

Read-only inspection of eight named public Windows DLLs is preserved in
h2-python-system-pe-readonly-inspection.json (1814c198d6d5c4d920479157ce61835960f78d5cbda271541e6f3906afb7dd71).
version.dll, ntdll.dll and ucrtbase.dll parse. advapi32.dll, bcrypt.dll,
kernel32.dll, ws2_32.dll and kernelbase.dll refuse the initial deliberately
unbound-only delay policy. The exact delay fields are in
h2-python-system-delay-readonly-details.json (17d467d8a3f0d08d54ab8be5184aeec61dcbc00b318e8c871413b6b97ff1ba40).
These have RVA attributes1, nonzero bound-IAT pointers and timestamp0. Preserve
these facts; do not call them malformed Windows DLLs or current parser readiness.

After the current source review/checkpoint, extend only the PE reader/direct
fixture to account explicitly for supported bound-delay metadata. Bound the
lookup, IAT, bound-IAT and unload-IAT spans using the terminated lookup count;
distinguish initialized file bytes from legitimate mapped virtual IAT storage.
Dependency names still come from the exact descriptor and file-backed lookup
names. Never follow raw bound function addresses as arbitrary file offsets.
Validate arithmetic, mapped virtual extent, terminators and all optional spans;
refuse old VA attributes and unknown layouts. Add exact synthetic zero-timestamp
bound-table and virtual-tail cases plus truncated/missing terminator/span/ordinal
failures. Re-run the unchanged real byte inventory after source review. Keep the
16 MiB/module, 64-module and 256 MiB limits. If accounting for every export
forwarder expands beyond those limits, report the exact graph and resolve its
supported scope explicitly rather than silently broadening the system set.

## Then implement a finite observation packet

Add a focused system-observation adapter and native ordinary probe under the
same host task, with direct injected refusal tests. First capture the actual OS
build, GetSystemDirectory result, normalized native root, root/object IDs and
current object descriptors. Hold read-only no-reparse handles while hashing
named system inputs. System files may have legitimate hard links; their native
observation contract is separate from private source-copy admission and must not
weaken the latter's single-link rule. Bind actual OS ownership/protection facts;
a basename, directory prefix or caller-supplied FileID is insufficient evidence.

The exact API-set host lookup needs a reviewed, bounded native observation seam.
The candidate uses LoadLibraryExW with only LOAD_LIBRARY_SEARCH_SYSTEM32 plus
LOAD_LIBRARY_AS_DATAFILE_EXCLUSIVE and LOAD_LIBRARY_AS_IMAGE_RESOURCE, then
K32GetMappedFileNameW on the actual returned mapping address and FreeLibrary on
the exact returned handle. It must distinguish an already loaded executable
handle from a resource mapping and bind both to the held native file object.
It must not use GetModuleFileName on a datafile handle, execute an export, use
DONT_RESOLVE_DLL_REFERENCES, search PATH/current directory, or change search
settings. No normal executable load is an automatic fallback.

This mapping approach is a proposed inference requiring an actual bounded probe;
it is not yet evidence of API-set contextual resolution. Unknown, truncated,
redirected, out-of-root, alias, changed-object or unsupported resource results
refuse. Resolve at most128 admitted API names and64 physical modules, never a
wildcard recursive filesystem scan. The source/effect packet must state the
exact admitted operations and total time/output/read bounds before the ordinary
mapping probe. Keep its external owned process wall bound distinct from polling.
If resource mapping cannot establish a requested host, preserve the refusal and
review an explicit supported alternative; do not fill the contract from guesses.

Microsoft documents data/resource mapping without normal DLL initialization,
existing-module handle behavior, mapping flag bits and exact FreeLibrary
ownership in [LoadLibraryExW](https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibraryexw).
[K32GetMappedFileNameW](https://learn.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-getmappedfilenamew)
reports the backing mapped file and specifies truncated-buffer refusal.
[Windows API sets](https://learn.microsoft.com/en-us/windows/win32/apiindex/windows-apisets)
explains why API contract names must not be treated as physical DLL filenames.
Those contracts guide the proposed observer; they do not qualify this host.

## One exact private Python effect after those inputs are proved

Freeze native IDs/hashes for python.exe/python314.dll/vcruntime140.dll and every
selected .py member, their deterministic ZIP/_pth bytes, actual SystemContract,
new owned image/scratch/canary objects, existing exact package SID, source and
probe binaries, explicit observation strategy, wall/read/output budgets and a
single write-ahead generation. Recheck the same roots/identities/bytes immediately
before creation/grants. Preserve original H1 evidence and do not adopt a previous
image/profile or mutate any shared tool/source/parent ACL.

The reviewed effect must run a fixed -I -S -B bootstrap importing encodings/json/os,
record sys.path/prefix/flags and Python module origins, observe actual native
loaded paths/IDs against the exact contract, and prove owned scratch plus
protected credential/controller canary denial. Actual loader observations must
include bootstrap's dynamic requests; static PE closure alone cannot establish
that condition. A separate fixed native inspector can observe the owned child
while it is held at a bounded ready/continue handshake; verify PID/Job/token and
exact child handle before reading module observations. Capture only this child.

Unexpected extension/module/path or incomplete denial is a retained failure;
close exact owned handles/processes and preserve consumed generation evidence.
No automatic allowlist expansion or replay. The immediate deliverable is one
qualified private Python bootstrap, still separate from Git/Codex/model egress,
production credential isolation and operational worker activation.
