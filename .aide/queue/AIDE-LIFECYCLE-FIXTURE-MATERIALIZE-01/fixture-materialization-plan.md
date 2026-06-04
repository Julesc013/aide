# Fixture Materialization Plan

## Roots

- Fixture root: `.aide/examples/apply/lifecycle-fixtures/`
- Source pack: `.aide/examples/apply/lifecycle-fixtures/source-pack/`
- Target baselines: `.aide/examples/apply/lifecycle-fixtures/target/`
- Expected states: `.aide/examples/apply/lifecycle-fixtures/expected/`
- Expected report examples: `.aide/examples/apply/lifecycle-fixtures/expected-reports/`
- Rollback record examples: `.aide/examples/apply/lifecycle-fixtures/rollback-records/`
- Fixture reports: `.aide/reports/lifecycle-fixtures/`

## Materialization Rules

The fixture files are static checked-in examples. They are not produced by lifecycle apply execution, scoped transaction apply execution, target repository mutation, branch/worktree mutation, network calls, provider/model calls, Gateway calls, GitHub calls, release publication, or broad active-repo apply.

Protected path scenarios are represented by metadata files. This task does not create actual `.git`, `.github`, `.aide.local`, secret, credential, or environment files under the repository.

## Hash Strategy

SHA-256 is used for static fixture file hashes because the lifecycle schema layer does not define another lifecycle-specific hash algorithm. Hashes are computed from checked-in UTF-8 fixture files after materialization and recorded in `fixture-index.json`, scenario metadata, expected reports, rollback-compatible records, and task-local hash evidence where applicable.

## Review Gate

The task ends at `needs_review`. Future dry-run plan generation and any fixture apply proof remain separate WorkUnits.
