# Fixture Summary

Fixture repository shape is defined in `fixture-plan.md` and `.aide/examples/apply/lifecycle/fixture-repository-spec.example.json`.

This task did not create active fixture target files and did not run lifecycle apply. Fixture materialization is deferred until after schema/example validation support.

Required future fixture classes:

- baseline files;
- generated files;
- managed-section files;
- manual content files;
- protected files;
- drifted files;
- missing-marker files;
- duplicate-marker files;
- malformed-marker files;
- nested-marker files;
- upgrade baseline and desired state;
- uninstall expected state;
- rollback expected state.
