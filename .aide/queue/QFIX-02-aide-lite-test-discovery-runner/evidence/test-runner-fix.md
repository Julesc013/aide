# Test Runner Fix

## Chosen Fix

QFIX-02 adds:

```text
py -3 .aide/scripts/aide_lite.py test
```

as the canonical AIDE Lite validation command.

The command is a stable alias over the existing internal selftest runner. It
keeps `selftest` available for compatibility while giving future agents a
plain, obvious validation command.

## Canonical Command

Use:

```text
py -3 .aide/scripts/aide_lite.py test
```

Result during QFIX-02: PASS.

The command:

- runs AIDE Lite internal checks in a temporary minimal repo;
- returns nonzero on failure;
- writes no committed repo state;
- makes no provider, model, or network calls;
- uses only the Python standard library.

## Compatibility Command

`selftest` remains supported:

```text
py -3 .aide/scripts/aide_lite.py selftest
```

Result during QFIX-02: PASS.

## Raw Unittest Command

Use this if raw AIDE Lite test discovery is needed:

```text
py -3 -m unittest discover -s .aide/scripts/tests
```

Result during QFIX-02: PASS, 94 tests.

## Non-Canonical Command

Do not use:

```text
py -3 -m unittest discover -s .aide/scripts/tests -t .
```

QFIX-02 intentionally documents it as invalid/non-canonical for the hidden
`.aide` path. It fails before loading tests because the start directory is not
importable under the repo-root top-level package rule.

## Regression Coverage

Tests now cover:

- importing `aide_lite.py` without CLI stdout/stderr side effects;
- `test` alias success path;
- `test` alias nonzero return on a controlled internal failure;
- command catalog mention of the canonical test command;
- Harness self-check guidance while QFIX-02 is active.

## Future Agent Guidance

For routine AIDE Lite validation before Q21 export/import, run:

```text
py -3 .aide/scripts/aide_lite.py test
py -3 -m unittest discover -s .aide/scripts/tests
```

Then run Harness, Compatibility, Gateway, and Provider tests as required by the
active queue prompt.
