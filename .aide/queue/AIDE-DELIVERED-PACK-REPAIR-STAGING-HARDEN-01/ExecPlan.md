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
- [x] Add exact regressions and source fix. The baseline failed both staging
  subcases. The first source candidate was superseded after independent review
  found a setup-failure stage leak.
- [x] Freeze `e215698a`, pass 11 focused and 44 full importer tests, and
  obtain independent ACCEPT_WITH_NOTES for dev source integration.
- [x] Generate and locally validate the current-source portable pack and
  release/draft outputs with non-circular provenance.
- [x] Qualify exact extracted ZIP/tar consumers and delivered-script races;
  independent reviewer accepted the frozen local artifact scope.
- [x] Commit source-ancestor metadata convergence and prove a zero-change
  postcommit replay across all 44 release files from clean `9f2f3895`.
- [ ] Observe exact remote dev after qualified fast-forward integration.

## Recovery

Preserve the original dev history and old verdict as historical evidence,
marking its repair-safety claim superseded. Do not use source-level tests as
release acceptance. Stop on unrecognized postpublication effects.
