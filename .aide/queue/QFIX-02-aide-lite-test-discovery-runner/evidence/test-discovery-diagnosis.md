# Test Discovery Diagnosis

## Failing Command

Baseline confirmed the checkpoint finding:

```text
py -3 -m unittest discover -s .aide/scripts/tests -t .
```

Result: FAIL.

Python raised:

```text
ImportError: Start directory is not importable: 'D:\\Projects\\AIDE\\aide\\.aide\\scripts\\tests'
```

## Why It Fails

The `-t .` flag tells `unittest` that the repo root is the import top level.
With that top level, the start directory must be importable as a Python package
path relative to the repo root. The directory is `.aide/scripts/tests`.

That path is intentionally a hidden repo-contract directory, not a Python
package namespace. The leading `.aide` segment is not a normal importable
package name. Python's discovery logic rejects the start directory before
loading any test module.

The failure is therefore a command-shape problem, not a failing test suite.

## Hidden Directory Naming

The hidden `.aide` directory naming is involved because the `-t .` form asks
Python to treat `.aide` like a package under the root import path. AIDE keeps
`.aide/` as committed repo contract state, not importable application package
code.

## Would `__init__.py` Solve It?

Adding `__init__.py` under `.aide/scripts/tests` would not make the old command
robust. The root cause is the leading `.aide` path segment under `-t .`, not
only the absence of an `__init__.py` in the leaf directory. Treating `.aide/` as
a Python package would also blur its role as declarative repo contract state.

QFIX-02 therefore does not add package markers inside `.aide/`.

## Passing Discovery Command

This command passes:

```text
py -3 -m unittest discover -s .aide/scripts/tests
```

Result: PASS.

Baseline before edits: 90 tests passed.

After QFIX-02 tests: 94 tests passed.

This form works because discovery uses the start directory directly and does
not require `.aide` to be importable from the repo root.

## Direct Test-File Invocation

This command was also checked during implementation:

```text
py -3 -m unittest .aide/scripts/tests/test_aide_lite.py
```

Result: FAIL with an empty module-name error. It is another non-canonical module
invocation shape for a hidden directory path and is not used as the supported
runner.

## Root Shim Decision

A root-level importable shim is not needed for this repair. The no-top-level
discovery command works, and the clearer canonical command is now:

```text
py -3 .aide/scripts/aide_lite.py test
```

The shim option remains available for a future packaging phase if copied packs
need root-level test aggregation, but QFIX-02 keeps the no-install AIDE Lite
layout intact.

## Canonical Command After QFIX-02

Future agents should run:

```text
py -3 .aide/scripts/aide_lite.py test
```

For raw unittest coverage of the AIDE Lite tests, use:

```text
py -3 -m unittest discover -s .aide/scripts/tests
```

Do not use the old `-t .` form for `.aide/scripts/tests`.

## Cross-Repo Robustness

The canonical `test` command is robust for copied AIDE Lite packs because it is
anchored to the script itself, uses only Python standard library behavior, does
not require `.aide` to be importable as a package, and does not call providers,
models, or network services.
