# Effective-Rules Independent Rereview

## Decision

`REQUEST_CHANGES`

The independent reviewer examined exact commit
`963dcc7d6ede688dbfa7771c7b6d9d03dc284f4a`, tree
`0fdc57c4910568c10cb978d45cf86b6273759ad5`, against merge base
`c6fdc754844cf7d42302218ce08307a7e05dcb61`.

## Findings

1. `HIGH`: the policy comparison treated branch-effective rules as complete
   ruleset bodies and included the non-dev ruleset that explicitly excludes
   `refs/heads/dev`. The fixture copied those bodies and therefore could not
   represent the GitHub branch-rules endpoint. An endpoint-shaped current
   target remained blocked with `effective_rules_drift`.
2. `LOW`: two records described executed tests as all passing while retaining
   one explicit Windows symlink skip.

## What Passed

- The documented workflow `path@ref` repair is sound and preserves normalized
  path/ref through observation and bridge handoff.
- The 27-path range has no task-allowlist violation.
- No workflow, credential, sender, settings installer, or hosted mutation path
  was added.
- The five affected suites executed 137 tests: 136 passed and one skipped.
- Scope and claims continue to distinguish local checks from destination
  enforcement and do not claim hosted or protected-host qualification.

## Required Repair

Represent effective branch rules as endpoint-shaped individual rule objects,
derive expectations only from observed rulesets applicable to `dev`, reject
wrong or excluded ruleset contributions, correct the count prose, and obtain a
superseding exact rereview before dev integration.

No settings, workflow, credential, hosted race, branch mutation, or merge was
authorized by this review.
