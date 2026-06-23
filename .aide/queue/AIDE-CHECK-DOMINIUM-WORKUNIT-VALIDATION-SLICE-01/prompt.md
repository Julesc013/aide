# AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

Independently review commit:

```text
8d8f511c77388b96118eb530f5361090b66911c1
```

and task:

```text
AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
```

Verify all stated build claims independently.

Pay particular attention to the authority distinction between:

- invoking the registered AIDE fixture-backed adapter;
- invoking a Dominium-owned implementation of `dominium.validation.run`.

Require:

- exactly one independently observed executor call;
- zero executor calls for unsupported capabilities;
- independently recomputed before/after workspace digests;
- typed result and typed refusal behavior;
- deterministic reruns;
- valid ContextDescriptor, ContextPack, WorkUnit, EvidencePacket, and EventRecord;
- no arbitrary shell, private tool, broad dispatch, provider/model/network,
  worker, Workbench, preview/apply, repository mutation, GitHub mutation,
  release, or promotion behavior;
- no local absolute path or secret leakage;
- `missing_evidence: 0`.

Do not repair implementation in this check task. Preserve warnings and
limitations.

If the slice passes, recommend exactly:

```text
AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
```

If the slice overclaims live Dominium command execution, recommend a bounded
repair task that corrects either the implementation or the capability label.
