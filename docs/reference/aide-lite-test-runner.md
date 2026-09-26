# AIDE Lite Test Runner

## Purpose

QFIX-02 makes AIDE Lite validation boring on purpose. Future agents should not
need to remember Python `unittest` import rules for a hidden `.aide/` directory
before they can trust the token-survival substrate.

## Canonical Command

Run this from the repository root:

```bash
py -3 .aide/scripts/aide_lite.py test
```

Use `python` or `python3` only when the Windows launcher is unavailable.

The command runs the existing internal AIDE Lite selftest checks, prints
PASS/FAIL output, returns nonzero on failure, writes no committed repo state,
and makes no provider, model, or network calls.

`selftest` remains supported:

```bash
py -3 .aide/scripts/aide_lite.py selftest
```

## Maintainer resource admission

Campaign builds, packaging and external unittest processes use the explicit
maintainer job path. This reuses AIDE's Windows Job process owner; it does not
activate the autonomous broker or replace the metadata-only TestJob contract.

```powershell
py -3 .aide/scripts/aide_lite.py job inspect --config <local-config> --manifest <job-json>
py -3 .aide/scripts/aide_lite.py job run --config <local-config> --manifest <job-json>
py -3 .aide/scripts/aide_lite.py job recover --config <local-config>
```

Inspection only reads state. The machine-local configuration belongs in the
existing `.aide.local/` boundary; `.aide.local.example/execution.json` contains
placeholders and finite example limits, not an approved machine placement.
`git detect` and `git plan` also inspect without writing by default; their
existing tracked report projections require explicit `--write-reports`.
All three storage roots must already exist and match their declared volume
identities. Missing/unavailable storage refuses admission without fallback.
All campaign workspaces must share one control root; its OS lock serializes
heavy jobs and their disk/memory reservations. This is not a global quota for
unmanaged tools or for jobs configured with another control root.

Job JSON identifies owner, WorkUnit, exact source commit/tree, input/oracle
file SHA-256 values, absolute executable/digest, `cwd`, literal `argv`, and
`adapter: python`, under schema `aide.maintainer-job.v1`. Module and script
commands are supported. Python temporary creation is pinned to the admitted
temporary directory; output belongs in `AIDE_JOB_OUTPUT` and caches in the
provided process-local cache variables. Additional tool adapters require
qualification of their actual output/cache placement before admission.

Memory, descendant count and combined logs have Windows Job/pipe enforcement.
Disk capacity and occupancy are monitored thresholds, not filesystem quotas
or a security sandbox. OS disk/memory counters are sampled once per second;
only owned scratch metadata is counted every 30 seconds. A short transient
may exceed the occupancy threshold between samples. Logs are truncated at the
configured byte limit and the attempt fails explicitly.

The runner persists named Job identity, process creation identity, command,
input/environment digests, limits, capacity and peaks. The Job kills owned
descendants if its controller exits. Normal/cancelled runs retain output and
bounded logs once, then remove only their ownership-marked temporary/cache
tree and release the reservation. Interrupted runs require `job recover`;
unknown aliases, changed configuration or a partial conflicting collection
remain preserved and reported for reconciliation. Neither process IDs nor
directory age authorize deletion.

## Raw unittest discovery

The supported raw unittest discovery command is:

```bash
py -3 -m unittest discover -s .aide/scripts/tests
```

QFIX-02 verified this command passes.

## Non-Canonical Command

Do not use:

```bash
py -3 -m unittest discover -s .aide/scripts/tests -t .
```

With `-t .`, `unittest` requires `.aide/scripts/tests` to be importable as a
package path from the repo root. `.aide/` is a hidden committed contract
directory, not a Python package namespace, so that form fails before loading
tests. Adding `__init__.py` files would not be the right fix because it would
blur the `.aide/` contract boundary.

## Cross-Repo Implication

Q21 Cross-Repo Pack Export / Import v0 can now rely on one obvious local command
when evaluating copied AIDE Lite packs:

```bash
py -3 .aide/scripts/aide_lite.py test
```

The command is stdlib-only and no-call, so it is safe to run before any future
Gateway/provider/runtime work.
