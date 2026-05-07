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
- Generated manifest source fingerprint drift remains an existing Harness
  warning and is not repaired by Q25.
- Final export provenance truthfully records dirty-state if generated before
  the final Q25 evidence commit.
