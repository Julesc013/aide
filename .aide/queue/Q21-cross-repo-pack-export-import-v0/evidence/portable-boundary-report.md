# Portable Boundary Report

## Boundary Rule

Q21 exports reusable AIDE Lite tooling and templates, not AIDE's own project
state. The target repo must generate its own identity, memory, context, token
reports, review packets, and evidence.

## Confirmed Exclusions

The generated pack excludes:

- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/queue/**` source queue history
- `.aide/memory/project-state.md`
- `.aide/memory/decisions.md`
- `.aide/memory/open-risks.md`
- `.aide/context/repo-snapshot.json`
- `.aide/context/repo-map.json`
- `.aide/context/repo-map.md`
- `.aide/context/test-map.json`
- `.aide/context/context-index.json`
- `.aide/context/latest-*.md`
- `.aide/reports/**`
- `.aide/controller/**`
- `.aide/routing/latest-*`
- `.aide/cache/latest-*`
- `.aide/gateway/latest-*`
- `.aide/providers/latest-*`
- `.aide/verification/latest-verification-report.md`
- `.aide/evals/runs/**`
- `.aide.local/**`
- `.env`
- obvious provider keys or secret-like strings
- raw prompt logs
- raw response logs

## Target Templates

The pack creates target-neutral templates instead:

- `.aide/profile.template.yaml`
- `.aide/memory/project-state.template.md`
- `.aide/memory/decisions.template.md`
- `.aide/memory/open-risks.template.md`
- `.aide/queue/README.template.md`
- `AGENTS.md.template`

Import creates target `.aide/profile.yaml` and memory placeholders only when
they are absent. Existing target files are not overwritten silently.

## Safety Posture

- Provider/model/network calls remain absent.
- Gateway forwarding remains absent.
- Actual `.aide.local/` state remains uncommitted and uncreated by import.
- Cache and provider status reports are excluded because they are target-specific
  generated state.
- Fixture validation is local only and does not mutate Eureka or Dominium.
