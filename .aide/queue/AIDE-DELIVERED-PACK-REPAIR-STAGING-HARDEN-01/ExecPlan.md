# ExecPlan: Windows owned repair staging hardening

## Objective and scope

The exact current dev helper can publish bytes changed by a same-user second
writer through its `mkstemp` staging leaf. Use a Windows handle that denies
competing write/delete access through no-replace link publication. Keep the
parent directory pinned and clean only the exact owned staging leaf. This
WorkUnit closes that race for owned repair intent and payload only.

## Dependencies and sequence

1. Bind the independent disposable reproduction and base dev identity.
2. Add two adversarial regression paths for intent and payload staging,
   including a prepublication rival write. Confirm baseline failure.
3. Implement guarded Windows stage creation/publication and exact cleanup.
   Run focused, full importer, release-adjacent, canonical, and adversarial
   tests immediately.
4. Freeze an exact source candidate and obtain independent security review.
5. Generate current-source portable/release bytes once, qualify extracted
   consumers and postcommit replay, obtain artifact review, then fast-forward
   dev under one writer. Record remote identity and retained gates.

## Progress

- [x] Independent reproduction found actual altered-byte publication in the
  old helper. External script and log are bound in task evidence.
- [ ] Add exact regressions and source fix.
- [ ] Qualify source, artifacts, consumers, and replay.
- [ ] Obtain independent acceptance and observe remote dev.

## Recovery

Preserve the original dev history and old verdict as historical evidence,
marking its repair-safety claim superseded. Do not use source-level tests as
release acceptance. Stop on unrecognized postpublication effects.
