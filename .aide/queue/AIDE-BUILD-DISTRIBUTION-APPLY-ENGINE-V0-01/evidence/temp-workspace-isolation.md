# Temp Workspace Isolation

The engine executes through `core/distribution/temp_workspace.py`.

Isolation properties:

- each scenario gets a fresh temporary workspace
- canonical fixture files are copied into the temporary workspace before execution
- writes are constrained to paths resolved inside the temporary workspace root
- absolute paths and traversal paths fail closed
- symlink or reparse uncertainty fails closed
- temporary workspaces are removed after successful execution

Representative execution:

- command: `py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario managed-file-update --mode apply-temp`
- result: `PASS_WITH_WARNINGS`
- temp_workspace_retained: `false`
- canonical_fixture_unchanged: `true`
- real_target_repo_modified: `false`
