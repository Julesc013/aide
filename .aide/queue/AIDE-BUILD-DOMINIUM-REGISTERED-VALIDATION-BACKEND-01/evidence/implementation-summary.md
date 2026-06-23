# Implementation Summary

Built a separate registered validation backend for the proposed capability:

```text
live_dominium_validation_command_readonly_v0
```

The backend:

- preflights repository identity, pinned revision, clean status, command files, command id, and optional digests;
- uses an injected process-runner seam with independent call counting;
- uses `shell=False`, exact allowlisted argv, bounded timeout, separate stdout/stderr capture, and constrained Python environment flags;
- refuses unsupported capabilities and invalid requests before process creation;
- parses Dominium stdout JSON and maps typed Dominium result/refusal into AIDE result/refusal records;
- records before/after revision, status, tracked tree digest, and command implementation digests;
- writes ContextDescriptor, ContextPack, WorkUnit, capability descriptor, invocation request/result, EvidencePacket, EventRecord, projection, validation, and status reports.

The accepted fixture-backed adapter remains unchanged.
