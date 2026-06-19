# Warning Disposition

`ACCEPTED_WITH_WARNINGS` is appropriate because the accepted slice is deliberately
minimal and projection-only.

Warnings are non-blocking:

- full JSON Schema Draft validation is absent
- source freshness/resolver/event-store behavior is absent
- no model/provider/Gateway/network calls or embeddings exist
- no runtime consumer exists
- no admission, trust, patch apply, or target mutation exists
