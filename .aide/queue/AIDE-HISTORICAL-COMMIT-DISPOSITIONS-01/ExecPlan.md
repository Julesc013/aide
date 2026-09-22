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
- [x] Add failing exact-object and adversarial tests.
- [x] Implement schema, policy, registry validation, and range reporting.
- [x] Prove portable export excludes source decision records.
- [x] Prepare proposed exact records and human decision packet.
- [x] Run affected and canonical validation.
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

## Decisions

- Dispositions apply only to range checks; latest, message-file, and hook
  checks remain strict.
- Accepted records bind decision and evidence paths to exact content hashes.
- The general policy and schema are portable, but this repository's decision
  registry is source-specific and excluded from export.

## Discoveries

- `bfb86c12` has one current message failure; `486e81cd` has thirteen.
- Both proposed records are visible in range output and remain ineffective.
- A clean source checkpoint is required before regenerating portable artifacts
  with trustworthy provenance.

## Retrospective

The source mechanism, adversarial tests, portable projection, and candidate
evidence are complete. The clean source checkpoint is `0dc74af4` with tree
`41137c8b`; generated pack closure is `f409dba8`. Every new branch commit passes
the raw message checker. Both real historical records remain proposed, so the
two original range failures continue to fail exactly and no integration gate
has been bypassed. The task now stops at independent mechanism review and two
exact owner/reviewer decisions.
