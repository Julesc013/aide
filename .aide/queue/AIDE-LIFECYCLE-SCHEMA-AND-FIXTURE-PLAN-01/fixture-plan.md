# Fixture Repository Plan

## Fixture Root Design

Future fixture materialization should use:

- fixture root: `.aide/examples/apply/lifecycle-fixtures/`
- source pack path: `.aide/examples/apply/lifecycle-fixtures/source-pack/`
- fixture target root path: `.aide/examples/apply/lifecycle-fixtures/target/`
- expected output path: `.aide/examples/apply/lifecycle-fixtures/expected/`
- fixture reports path: `.aide/reports/lifecycle-fixtures/`
- fixture rollback records path: `.aide/reports/lifecycle-fixtures/rollback/`
- fixture evidence path: `.aide/queue/<future-task>/evidence/`

This task does not materialize those fixture target files. It only defines the shape and non-mutating examples under `.aide/examples/apply/lifecycle/`.

## Required Fixture Classes

- baseline files
- generated files
- managed-section files
- manual content files
- protected files
- drifted files
- missing-marker files
- duplicate-marker files
- malformed-marker files
- nested-marker files
- upgrade baseline
- upgrade desired state
- uninstall expected state
- rollback expected state

## Fixture Scenarios

1. Clean install into empty fixture target.
2. Install conflict with existing manual file.
3. Install managed section into existing manual file.
4. Upgrade from old generated section to new generated section.
5. Upgrade with manual content preserved.
6. Upgrade with drift detected.
7. Repair plan for missing marker.
8. Repair plan for malformed marker.
9. Rollback record generation.
10. Uninstall plan preserving manual content.
11. Protected path attempted change blocked.
12. Path traversal attempted change blocked.
13. Broad delete attempted change blocked.

## Validation Approach

Future fixture materialization should verify:

- fixture paths exist only under authorized fixture roots;
- examples parse;
- fixture manifests reference explicit paths;
- protected paths are represented and blocked;
- target class is `fixture`;
- report-only, dry-run, and fixture-apply modes are distinct;
- `target_files_mutated` is false for report-only and dry-run examples;
- capability labels are not overstated;
- no secret-like fields are present;
- no active repo apply or target repo mutation is performed.

## Deferred Work

`AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` should create the physical fixture directory tree after schema/example validation is wired. Lifecycle apply remains blocked until a later explicit apply task is reviewed.
