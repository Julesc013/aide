# Apply Lifecycle Schemas

`AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` defines the first lifecycle schema and fixture-shape layer after the scoped transaction executor was accepted with notes.

## Scope

The lifecycle schema layer covers:

- lifecycle manifests;
- lifecycle operation plans;
- lifecycle reports;
- rollback-compatible lifecycle records;
- fixture repository shape;
- non-mutating lifecycle examples.

These records prepare future fixture proof. They do not implement lifecycle apply and do not execute install, upgrade, lifecycle repair, rollback, or uninstall behavior.

## Schema Files

- `.aide/apply/lifecycle-manifest.schema.json`
- `.aide/apply/lifecycle-plan.schema.json`
- `.aide/apply/lifecycle-report.schema.json`
- `.aide/apply/lifecycle-rollback-record.schema.json`

The schemas require explicit paths, allowed roots, protected roots, preimage and postimage expectations, rollback-compatible record references, validation evidence, capability labels, and review gates.

## Fixture Shape

Future fixture materialization should use an explicit fixture root with source pack, target, expected output, reports, rollback records, and evidence subpaths. The planned shape is recorded in `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/fixture-plan.md`.

This task does not create active fixture target files and does not run fixture apply.

## Scoped Executor Interlock

Future lifecycle plans must compile to scoped transaction plans or compatible transaction bundles. They must preserve explicit path boundaries, operation allowlists, managed-section defaults, preimage hash checks, postimage verification, staged-change records, rollback-compatible records, dry-run/report mode before apply, and evidence.

Scoped transaction executor v0 still blocks multi-mutating apply before mutation. It does not implement multi-file atomic apply, rollback execution, uninstall deletion safety, target repo adoption, release publication, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

## Capability Reality

This schema layer is `needs_review`. It is not production-ready, release-ready, target-repo capable, broad-apply capable, autonomous, or install/upgrade/lifecycle repair/rollback/uninstall apply capable.
