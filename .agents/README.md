# AIDE Repo-Local Agent Workflows

`.agents/` holds reusable repo-local operational knowledge for Codex work in AIDE. It complements `AGENTS.md`; it does not replace or override it.

## What Belongs Here

- reusable task packet formats
- subagent role usage guidance
- narrow repo-local skills
- maintenance and audit support skills for recurring repository upkeep

## What Does Not Belong Here

- product source code
- broad project law already defined in `AGENTS.md`
- plan status that belongs in `PLANS.md`, `IMPLEMENT.md`, or `DOCUMENTATION.md`

## Separation Of Concerns

- `AGENTS.md` defines repository-wide operating law.
- `.codex/` defines repo-scoped Codex configuration and role bindings.
- `.agents/skills/` defines narrow reusable instructions for recurring work types.
- `scripts/maintenance/` defines reusable maintenance control-plane assets that those skills may reference.
- planning and execution records remain in the root control-plane documents.

## Operating Rule

Keep `.agents/` concise, reusable, and operational. If a document is better expressed as project source, governance, or planning state, it does not belong here.
