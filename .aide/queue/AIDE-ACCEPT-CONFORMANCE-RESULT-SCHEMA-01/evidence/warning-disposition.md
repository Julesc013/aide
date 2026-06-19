# Warning Disposition

Accepted warning debt:

- ConformanceResult remains evidence-projected and was not produced by a runner.
- A conformance runner is not implemented.
- Automatic observation collection is not implemented.
- The referenced profile remains candidate and is not active.
- Profile requirements satisfaction does not admit or trust the subject.
- Admission is not implemented.
- The subject is not admitted by the result.
- PatchTransaction is not implemented.
- AdapterManifest is not implemented.
- ContextPack v2 is not implemented.
- Runtime, Service, Commander, provider/model calls, branch mutation, release,
  and target apply remain unimplemented.

Disposition:

```text
ACCEPTED_WITH_WARNINGS
```

None of these warnings blocks acceptance of the bounded
`minimal_conformance_result_schema` capability because they are explicit
non-capabilities, not hidden implementation claims.
