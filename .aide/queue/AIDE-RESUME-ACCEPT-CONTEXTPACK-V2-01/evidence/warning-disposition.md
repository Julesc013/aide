# Warning Disposition

Result classification: `ACCEPTED_WITH_WARNINGS`.

Warnings retained:

- ContextPack v2 remains projection-only.
- Full JSON Schema Draft validation is absent.
- No resolver, event store, freshness policy, secret-redaction engine, token
  budget enforcement, runtime consumer, model/provider/network call, embedding,
  admission, trust, patch apply, or target mutation exists.

Warnings are non-blocking for accepting the minimal projection capability.
