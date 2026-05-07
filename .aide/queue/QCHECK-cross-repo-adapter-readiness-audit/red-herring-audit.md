# Red-Herring / Overbuild Audit

| Item | Decision | Why | Evidence Needed |
| --- | --- | --- | --- |
| Gateway skeleton | Defer | No-call status/smoke is useful as a boundary, but Gateway forwarding would distract from target proof. | Target quality gates plus explicit Gateway readiness audit. |
| Provider metadata | Defer | Offline metadata prevents unsafe future assumptions; live calls are premature. | Credential policy, billing measurement, provider tests, and reviewed Gateway boundary. |
| Adapter compiler | Keep | Concise existing-tool guidance directly supports compact packets and evidence gates. | Target use with Codex/Claude/Aider/Cline/Continue/Cursor/Windsurf. |
| Route profiles | Keep but advisory | Useful for no-call planning and hard floors; not execution. | Evidence that route decisions reduce premium review without quality loss. |
| Cache keys | Needs evidence | Metadata boundary is safe, but real cache value is unproven. | Repeat-task savings and stale-cache safety tests. |
| Outcome controller | Keep advisory | It warns on packet size and suggests optimization; applying recommendations automatically would be premature. | Correlation between recommendations and improved target outcomes. |
| Generated adapter files | Keep as previews | They are compact and non-destructive; they must not become canonical truth. | Drift review and target-tool usage evidence. |
| Export pack direct importer | Simplify/repair | Fixture import works, but real pilots avoided broad apply because target scopes were narrower. | Target-scoped import mode passing fixture and real target dry-run. |
| Large docs/reference pack surfaces | Simplify for targets | Useful for source repo, but target prompts may not allow copying broad docs. | Import profiles that distinguish full pack, lite pack, and docs-only opt-in. |
| Queue ceremony in targets | Simplify for targets | AIDE source needs forensic queue history; targets need enough evidence without copying AIDE self-history. | Pilot friction reports from Eureka/Dominium review. |
| Exact tokenizer/billing | Defer/research | Important eventually, but chars/4 is enough for queue triage. | Provider-specific billing experiment with no secrets in repo. |
| Autonomous loops | Archive until much later | Would risk quality and safety before target gates exist. | Strong eval gates, rollback, human review, and provider policy. |
