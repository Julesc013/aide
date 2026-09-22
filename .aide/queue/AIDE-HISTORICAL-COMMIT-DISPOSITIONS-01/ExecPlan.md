# ExecPlan: Historical Commit-Message Dispositions

## Objective

Allow an exact, reviewed historical-format disposition to satisfy range
conformance without claiming that the original commit message passed.

## Scope

- Add a source registry, schema, policy, validator, and range-check reporting.
- Bind records to full commit, tree, parents, canonical message hash, and exact
  failed-check messages.
- Add raw-policy mode and adversarial disposable-Git tests.
- Prepare proposed records and an exact decision packet separately from
  mechanism acceptance.

## Non-Goals

- No history rewrite, force push, wildcard, commit-prefix match, blanket merge
  exemption, fabricated historical validation, main promotion, tag, or release.

## Progress

- [x] Inspect current checker, policy, tests, and blocker identities.
- [x] Confirm no existing executable historical-disposition mechanism.
- [x] Create an isolated task branch from current dev.
- [ ] Add failing exact-object and adversarial tests.
- [ ] Implement schema, policy, registry validation, and range reporting.
- [ ] Prove portable export excludes source decision records.
- [ ] Prepare proposed exact records and human decision packet.
- [ ] Run affected and canonical validation.
- [ ] Publish for independent review.

## Test Oracle

Without an accepted exact record, the malformed commit fails exactly as before.
An accepted record applies only when full commit, tree, ordered parents,
canonical message hash, exact failed checks, scope, decision, authority, and
record digest all match. Any mutation refuses closed. Raw-policy mode always
reports the original failure.

## Recovery

The mechanism is read-only. Remove or mark a proposed record rejected to keep
it ineffective. Resume from task evidence and committed fixtures; never rewrite
the referenced history.

