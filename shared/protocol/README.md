# Shared Protocol

`shared/protocol/` is the future home for transport-agnostic request and response handling between host adapters and the shared core.

This area owns envelope shape, protocol-version handling, and shared serialization expectations. It should remain independent of any one execution mode.
