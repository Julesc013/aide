# ReferenceID Integration Review

PatchTransaction identity uses the accepted ReferenceID kind:

```text
aide://patch-transaction/synthetic-managed-section-review-candidate-01
```

Other required references are syntactic `aide://` refs for source, queue-task,
artifact, capability, conformance-result, test-job, and evidence kinds.

Validation fails closed for:

- invalid or missing required refs;
- unknown required reference kinds;
- required capability refs outside the recognized predecessor set;
- required ConformanceResult refs outside the recognized accepted result.

No runtime reference registry or resolver service was implemented.
