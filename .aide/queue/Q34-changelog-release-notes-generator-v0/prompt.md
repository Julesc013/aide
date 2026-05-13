# Q34 Prompt Summary

Implement the first robust AIDE changelog and release-notes generator from local Git evidence.

Required result:

- Generate preview-only changelog and release-note Markdown and JSON files.
- Report malformed or legacy commits instead of hiding them.
- Add changelog policy, config, templates, commands, tests, golden tasks, docs, evidence, and export-pack support.
- Prepare the Q35 GitHub Protection and CI Advisory task packet.

Boundaries:

- Do not publish releases, create tags, create GitHub Releases, push, mutate branches, rewrite history, call providers/models, or perform network calls.
- Do not mutate Eureka or Dominium.
- Keep work inside Q34 allowed paths and stop at `needs_review`.
