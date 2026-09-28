# Windows Lite warning classification before final freeze

This is a source/evidence classification, not stable release acceptance.
Reviewer acceptance remains required against final source, profile and assets.

The local preview installed `validate` exited zero and reported two warnings:
`latest-task-packet.md` was absent before a target task packet was generated,
and the optional Codex `AGENTS.md` managed adapter section was absent before
the target ran `adapt`. The candidate public Lite command list does not include
`adapt`. These are expected fresh-target initial states for no-model local CLI
operation; they must remain visible and must not be described as zero-warning
validation. If final consumers need agent guidance as part of a promised
workflow, this classification is insufficient and that workflow must be
qualified or repaired before shipping.

Installed `verify --evidence` returned WARN with zero errors: 15 fresh and 18
Git brownfield warnings in retained job `c45db84982fb43179233b77c97f38e61`.
Eleven referenced repo/quality/refactor/routing/cache/token reports and two
cache reports were absent because those optional generators had not run. The
adapter section was absent as above. The fresh non-Git fixture had no Git diff
scope; the brownfield fixture had four uncommitted paths outside its synthetic
task allowlist. The final profile can honestly promise that verification
**reports** missing inputs and scope warnings; it cannot claim the fixture was
warning-free or that a mismatched task allowlist was accepted as clean.

Python socket guarding showed these installed CLI commands completed without
Python socket calls. It did not trace native child networking. The first Lite
profile promises usable local operation after archive acquisition with all
providers disabled, not OS-level network containment or native-host isolation.
Final downloaded-byte offline qualification remains open. Synthetic V2/V3
update packs remain fixtures, not published predecessors; the first public
release has an empty declared predecessor matrix only if the final remote
history check confirms no earlier stable AIDE Lite release or tag.
