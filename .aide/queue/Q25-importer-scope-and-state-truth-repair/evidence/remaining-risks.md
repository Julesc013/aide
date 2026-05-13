# Remaining Risks

- Q25 is review-gated and must be reviewed before Q26 Eureka handover.
- Fixture import proves safe importer mechanics, not target handoff success.
- Eureka and Dominium target-pilot evidence still need review in their target
  repos.
- Dominium-specific golden tasks remain future work.
- Exact tokenizer/provider billing is still absent; token evidence remains
  `chars / 4` estimates.
- Gateway/provider runtime, forwarding, credentials, model calls, and network
  calls remain deferred.
- `--mode full` still exists for reviewed local fixtures; operators must not
  use it casually in product repos.
- Q27-Q29 blocker records remain as downstream history from attempts made
  before this fix-forward repair. They should be redone after Q25/Q26 review,
  not silently marked complete by Q25.
- Generated manifest source fingerprint drift and early review gates remain
  existing Harness warnings outside the Q25 pack/import repair.
- Final export provenance truthfully records dirty-state if generated before
  the final Q25 evidence commit; this is the explicit Q25 provenance convention,
  not a hidden stale-pack pass.
