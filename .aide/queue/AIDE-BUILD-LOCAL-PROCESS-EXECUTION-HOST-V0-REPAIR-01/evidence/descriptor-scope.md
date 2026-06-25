# Descriptor Scope

The repaired descriptor advertises only:

```text
probe
create_run
```

The descriptor explicitly marks these operations unsupported:

```text
attach
send_input
stream_events
resolve_runtime_approval
interrupt
pause
resume
cancel
collect_artifacts
finish
reconcile
```

This closes the overclaiming finding without expanding the local host into a general worker harness.
