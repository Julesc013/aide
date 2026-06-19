# Remaining Risks

- Independent check and acceptance are still required before ContextPack v2 can
  be accepted.
- Source selection is a minimal deterministic set, not a full context compiler.
- No source freshness policy, event store, resolver, model budget enforcement,
  secret-redaction engine, or runtime consumer exists.
- Historical blocked ContextPack tasks remain preserved and should be resumed
  only through explicit resume tasks.
