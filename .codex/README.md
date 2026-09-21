# AIDE Codex Local Agent Files

`.codex/` holds repository-scoped Codex agent role files. It is not product code.

## Directory Roles

- No repo-local `config.toml` should be committed here. Model, reasoning effort,
  provider, service tier, approval policy, sandbox posture, and search mode are
  user/session choices.
- `agents/`: minimal custom role config files for explicit delegation.

## Repo Scope Versus Personal Scope

Repo-scoped role files may travel with this repository. Personal or global
Codex defaults should remain outside version control and should not redefine
project law that already lives in `AGENTS.md`.

## Operating Rule

Keep this directory minimal, reviewable, and aligned with repository governance.
It should improve execution reliability without pinning operator choices or
broadening product scope.
