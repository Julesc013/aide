# Distribution fixture portability hardening

Status: source candidate; independent review and complete-checkout validation pending.

## Scope

This increment hardens the existing `core/distribution/temp_workspace.py` and
`operation_executor.py` helpers. It does not add an installer, change an adopted
schema, activate a worker, or grant target-repository apply permission.

- One shared lexical classifier rejects drive-relative/absolute paths, streams,
  traversal, root aliases, reserved Windows device names, illegal characters,
  trailing-dot/space aliases, and unencodable Unicode.
- Backslash and slash input locators have the same meaning on all hosts.
- Exact, case-folded, normalized-Unicode and file/parent collisions refuse before
  initial writes; existing child-name aliases also refuse.
- Snapshots reject static symlinks, reparse points, hardlinks and special files.
  Regular-file hashing uses bounded chunks and checks descriptor/path identity,
  file size and modification time around reads. The snapshot/digest encoding for
  ordinary files remains unchanged.
- Initial maps are validated completely before writes. File creation is exclusive.
- Restore payload keys, paths, UTF-8 content and hashes are validated before old
  fixture cleanup. Volume-root reset is refused. Valid file/directory replacement
  is retained.
- Operation execution returns typed path refusals. `add_managed_file` cannot
  replace an already-existing file. Existing absolute/traversal/ownership refusal
  codes remain intact.

## Verification

Run from a complete candidate checkout:

```sh
python -B -m unittest discover -s .aide/scripts/tests -p test_aide_distribution_fixture_portability.py -v
python -B -m unittest discover -s .aide/scripts/tests -p 'test_aide_distribution*.py' -v
python -B .aide/scripts/aide_lite.py validate
```

The first command passed 125 tests on Linux/CPython 3.13.5 in the implementation
session. Nine explicit regressions failed against the exact baseline and passed
after the fix. The second and third commands were not run: the session had exact
blob reconstructions of the changed modules, not a complete AIDE checkout.
Branch coverage: workspace helper 95%, operation executor 81%, aggregate 89%.
These are focused test measurements, not product certification.

## Non-capabilities and retained limits

The caller must supply a trusted, disposable, single-writer fixture root. These
Python path checks do not hold an atomic handle-based confinement boundary over
all reads/writes. They do not defeat a malicious concurrent same-user writer.
Restore is still a fixture reset, not crash-atomic production rollback. Generic
`write_text`/`write_json` retain their trusted-caller contract; they are not new
root-confined publication APIs. Native Windows reparse/network/token behavior and
macOS filesystem behavior remain unqualified by this Linux run.

All changes narrow ambiguous fixture behavior. No .codex settings, model/provider
pins, credentials, branch policy, target repository or release state is changed.

References: Microsoft Learn, "Naming Files, Paths, and Namespaces"; Python
`pathlib`/`os` documentation. Exact native-platform behavior requires its own lab
profile rather than an inference from lexical tests.
