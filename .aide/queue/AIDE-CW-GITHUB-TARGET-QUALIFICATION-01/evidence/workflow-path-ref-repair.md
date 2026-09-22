# Documented Workflow `path@ref` Repair

Task: `AIDE-CW-GITHUB-TARGET-QUALIFICATION-01`  
Starting published review checkpoint: `b8fb89b917c9a1fc152b19263bedbe2db16c2e39`

## Scope and Result

The independent review's F-03 is repaired in source and regression coverage.
`github_checks.py` now parses GitHub workflow-run path selectors in these exact
forms:

```text
.github/workflows/aide-cw-checks.yml@task/aide-cw-<request-digest>
owner/repository/.github/workflows/aide-cw-checks.yml@task/aide-cw-<request-digest>
```

The repository prefix, if present, must match the admitted repository. The
normalized bare path and normalized `refs/heads/...` ref are retained in the
observation. The immutable plan requires that ref to equal its admitted request
branch and its workflow SHA to equal the admitted candidate commit. Decision,
intent, staged transport, and the registered bridge therefore bind the same
normalized observation bytes.

The positive fixtures exercise both documented forms. Wrong workflow path,
wrong repository prefix, wrong ref, missing ref, empty ref, a full ref where
the API selector is required, and malformed double-slash ref forms all refuse.

The task allowlist now explicitly includes the two existing end-to-end test
paths identified by the reviewer. This is a source-only scope correction
authorized by the owner request; it creates no target setting, workflow,
credential, GitHub API call, or hosted effect.

## Validation

| Command | Result |
| --- | --- |
| `py -3 -B .aide/scripts/tests/test_continuous_worker_github_observation.py -v` | PASS, 48 tests |
| `py -3 -B .aide/scripts/tests/test_continuous_worker_pr_observation.py -v` | PASS, 21 tests |
| `py -3 -B .aide/scripts/tests/test_continuous_worker_provider_bridge.py -v` | PASS, 12 tests |
| `py -3 -B .aide/scripts/tests/test_continuous_worker_github_http.py -v` | PASS, 19 tests |
| `py -3 -B .aide/scripts/tests/test_continuous_worker_integration_broker.py -v` | PASS, 36 passed; 1 skipped |
| `py -3 .aide/scripts/aide_lite.py validate` | FAIL only on inherited stale export-pack provenance: manifest `b3e5c7aa2a1732faee4a9021e64bdba65c6db1cb` differs from this task head |
| `py -3 .aide/scripts/aide_lite.py doctor` | FAIL because canonical validation remains stale on that same export-pack provenance |
| `git diff --check` | PASS |

The skipped integration case is `test_linked_blob_is_refused_even_with_matching_bytes`.
The current Windows token lacks disposable symlink creation privilege
(`WinError 1314`). This source repair neither weakens isolation nor treats the
skip as equivalent evidence.

An initial local rerun exposed stale fixture construction after the new
candidate-head plan binding was added. The fixture now sets its generated
candidate SHA before constructing the check identity; all final commands above
passed.

## Remaining Gates

- Superseding independent review of this exact repair commit.
- Restricted broker principal and workflow/check identity resolution.
- Exact target policy review, authorized hosted adversarial races, and
  destination-side predicate qualification.
- Protected-host/store close dependency and the retained Windows symlink case.

No GitHub API/network/credential/settings/hosted effect, merge, tag, release,
or `.codex`/machine configuration change was performed.
