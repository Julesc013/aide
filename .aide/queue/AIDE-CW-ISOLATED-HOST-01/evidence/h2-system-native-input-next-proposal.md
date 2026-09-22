# Next H2 step: exact public native input observations

This is a proposal outside the frozen system-source checkpoint. It admits no
actual DLL mapping, image copy, grant, profile or restricted Python execution.

Prepare a small task-owned driver for one bounded ordinary Windows child under
the existing owned Job host. Pin driver/source/interpreter inputs and an exact
create-only output reservation before execution. Use a 30-second outer deadline,
bounded stdout/stderr and explicit retained failure output. It may observe only
the actual system directory and these eight previously hashed public DLLs:
advapi32.dll, bcrypt.dll, kernel32.dll, version.dll, ws2_32.dll, ntdll.dll,
ucrtbase.dll and kernelbase.dll. Expected bytes/SHA256s come from the unchanged
h2-delay-system-readonly-final.json; a changed file is a recorded refusal.

The driver first observes GetSystemDirectoryW and the one local DOS-volume
mapping, refusing an unexpected or ambiguous system root. Open that exact native
root and literal children read-only with the already reviewed no-reparse and
no-write/no-delete-sharing primitive. While all handles remain held, capture
actual root/file IDs, normalized native names, size/link counts, owner SIDs and
owner/DACL hashes, then hash bounded streams and reobserve facts. No directory
scan, resource mapping, export execution, protection change or hard-link creation
is permitted. NativeSystemApi's mapping methods must remain unreachable in this
first driver. All exact handles close once; any error retains its evidence.

Freeze the complete source/effect manifest and independent source/denial tests
before that ordinary observation. Its result will test the actual ABI and bind
real input facts; owner names and matching hashes alone will not automatically
qualify OS provenance or a private loader. Any unsupported native path/descriptor
layout remains a refusal with an explicit bounded repair, never a fallback.

After those actual facts are independently reviewed, prepare a separate exact
resource-observation effect for two candidate requests:
`api-ms-win-core-path-l1-1-0.dll` and `api-ms-win-crt-runtime-l1-1-0.dll`. This
is a finite feasibility subset in an identified ordinary process; it cannot qualify the complete 180-name
API inventory, circumvent the unchanged 128-row cap, or establish contextual
resolution inside the later restricted Python process. That later effect needs
an actually protected durable reservation/intent owner and held object pins.

Full transitive admission, system/controller provenance, actual private-image
grants and the restricted Python bootstrap/denial oracles remain required after
these observations. Git/Codex/model egress and operational worker activation remain
separate unqualified work.
