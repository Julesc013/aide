# Helper Review

`core/protocol/conformance_profile.py` mirrors the prior protocol-helper pattern:

- deterministic constants;
- schema loader;
- profile builder;
- case builder;
- profile and case index builders;
- source-artifact mutation sentinel;
- local structural validator;
- report writer;
- Markdown renderers;
- explicit forbidden-operation preservation.

The helper validates:

- profile ref alignment;
- SemVer profile version;
- subject reference syntax;
- unique case IDs;
- dependency existence;
- dependency cycles;
- requirement levels;
- known evaluator rules;
- required accepted outcomes;
- fail-closed aggregation;
- explicit non-capabilities;
- profile-only status flags.

The helper does not execute cases or evaluate real observed results.
