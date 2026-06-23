# Architecture Boundary

Implemented generic flow:

```text
CapabilityInvocation
  -> CapabilityBinding
  -> ExecutionProvider
  -> RegisteredProcessExecutionProvider
  -> OutputDecoder
  -> CapabilityOutcome
  -> ProcessExecutionReceipt
  -> EvidencePacket/EventRecord projection
```

The generic provider is one execution provider. It is not AIDE's universal
execution ontology and does not implement host command, HTTP/gRPC, MCP, A2A, CI
job, sandbox, offline mailbox, or human/manual providers.
