# AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

Create and process `AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.

Independently check `AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`.

Verify:

- exactly one registered local read-only `dominium.validation.run` invocation;
- no arbitrary shell fallback;
- no private tool bypass;
- no broad Dominium command dispatch;
- no provider/model/network/worker behavior;
- no Workbench apply, preview/apply, or PatchTransaction apply behavior;
- no source or target repository mutation;
- deterministic ContextDescriptor, ContextPack, WorkUnit, EvidencePacket,
  EventRecord, and projection outputs;
- complete task evidence with `missing_evidence: 0`.

If the slice passes, recommend exactly:

```text
AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
```

If a material defect remains, recommend exactly:

```text
AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-REPAIR-01
```
