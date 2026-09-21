# Validation

## Exact Source Reproduction

| Check | Result |
|---|---|
| Seven retained `.codex` Git blobs versus `0e76df9e` | PASS; all seven blob identities match |
| `.codex/config.toml` | PASS; absent exactly as in the reviewed checkpoint |
| Active execution-setting assignment scan across `.codex/**` | PASS; zero model, provider, reasoning, service-tier, approval, sandbox, search, delegation-limit, or sandbox-network assignments |

## Structural Validation

| Command | Result |
|---|---|
| `py -3 -B -c` with `tomllib` across `.codex/agents/*.toml` | PASS; five description-only role files parsed |
| `codex --strict-config --version` | PASS; `codex-cli 0.145.0` |
| `py -3 -B .aide/scripts/aide_lite.py workunit validate` | PASS; 351 queue tasks and objects validated; no source queue, branch, target, provider, model, Gateway, or network mutation |
| `py -3 -B .aide/scripts/aide_lite.py validate` | PASS |
| `git diff --check` | PASS |

The validation helpers refreshed four tracked workunit reports. Those generated
changes were restored and are excluded from the candidate.

## Boundary

No user, profile, managed, system, machine-wide, or active-session configuration
was read or changed. No permission, approval, sandbox, or network posture was
widened. No runtime, provider, host, target, `main`, tag, or release effect ran.

## Post-Integration Validation

`dev` fast-forwarded from `be3a854a` to `4398497a` with no merge commit. From
the integrated `dev` worktree:

- Active execution-setting assignment scan: PASS; zero matches.
- `workunit validate`: PASS; 351 queue tasks and objects.
- Full `aide_lite.py validate`: PASS.
- Generated workunit report refreshes were restored and excluded.
- Remote `dev` publication: PASS at `4398497a1e43b77938636dcd0c7002d6ff045467`.
