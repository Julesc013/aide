# Warning Disposition

`PASS_WITH_WARNINGS` is appropriate because the following remain intentionally
absent:

- full JSON Schema Draft validation
- model/provider/Gateway/network calls
- embedding generation
- source resolver or event store
- agent/worker/command execution
- adapter admission or trust
- patch apply or target mutation
- runtime, Service, Test Broker, Commander, or Workbench behavior

These warnings do not block acceptance review.
