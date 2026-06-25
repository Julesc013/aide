# Prompt

Create and process `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01`.

This is a check-only task. Do not repair implementation.

Independently verify that `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01` closes the exact six material findings from `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01`:

- disposable workspace proof;
- path traversal, symlink, and reparse escape rejection;
- raw NDJSON event stream and fail-closed event handling;
- content-addressed worker artifacts;
- WorkerRun lifecycle;
- host descriptor operation scope.

If material findings remain, recommend exactly `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`.

If all material checks pass, recommend exactly `AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.
