# CLI Review

Registered CLI commands:

```text
py -3 .aide/scripts/aide_lite.py conformance-result status
py -3 .aide/scripts/aide_lite.py conformance-result project
py -3 .aide/scripts/aide_lite.py conformance-result validate
```

The CLI prints:

- result ref;
- profile ref;
- subject ref;
- record validity;
- record completeness;
- profile requirement satisfaction;
- execution false;
- runner null;
- admission false;
- subject admitted false;
- trusted false;
- explicit non-capability boundaries.

No run, execute, collect, admit, trust, activate, adapter-run, or mutate
subcommand is registered.
