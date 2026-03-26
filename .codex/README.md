# AIDE Codex Config

`.codex/` holds repository-scoped Codex operational configuration. It is not product code.

## Directory Roles

- `config.toml`: repo-local defaults for model, approvals, sandbox posture, bounded agent usage, and role registration.
- `agents/`: minimal custom role config files for explicit delegation.

## Repo Scope Versus Personal Scope

Repo-scoped config captures defaults that should travel with this repository. Personal or global config should remain outside version control and should not redefine project law that already lives in `AGENTS.md`.

## Operating Rule

Keep this directory minimal, reviewable, and aligned with repository governance. It should improve execution reliability without broadening product scope.
