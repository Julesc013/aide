# AIDE Operating Law

## Project Identity

- Product name: AIDE
- Expansion: Automated Integrated Development Environment
- Pronunciation: "aid"
- Canonical short namespace: `aide`

## Repository Doctrine

- AIDE is one project with one shared core and many host adapters.
- The repository is designed for long-horizon human plus agentic development.
- Governance, inventory, matrices, implementation, evaluation, and packaging are separate concerns and should not be collapsed into a single undifferentiated workstream.
- Precision, auditability, bounded scope, and deterministic verification take precedence over marketing language.

## Self-Hosting Reboot Rules

- AIDE is being rebooted in place, not restarted from scratch.
- Preserve bootstrap-era history, phase records, documents, evidence, and blocked or deferred posture.
- `.aide/profile.yaml` and declaration catalogs under `.aide/` are the canonical self-hosting Profile/Contract for the repository.
- The filesystem queue under `.aide/queue/` is the canonical source of truth for non-trivial self-hosting work.
- The Codex extension UI, chat task queue, or ad hoc prompt history is not canonical when it conflicts with `.aide/queue/`.
- Non-trivial work must go through AIDE intake or a filesystem queue item with an ExecPlan, bounded scope, validation, and evidence.
- Small direct work is allowed only when `.aide/policies/bypass.yaml` permits it.
- Agents must write evidence and run proportionate validation before reporting substantial work as complete.
- Agents must stop at review gates defined in `.aide/policies/review-gates.yaml`.
- Generated downstream artifacts are outputs, not canonical contract records, unless a future reviewed policy explicitly marks them as canonical.
- The Profile is declarative; Harness commands are executable machinery and remain queue-scoped work.
- Do not build Runtime, Hosts, Commander, Mobile, Visual Studio, Xcode, VS Code, provider, or app-surface work ahead of the queue plan.

## Required Start-Of-Task Sequence

1. Inspect the repository state before editing.
2. Read the relevant governing documents for the task.
3. For any complex task, write a short plan before making edits.
4. Confirm the allowed paths and keep the change set inside them.
5. Execute the smallest coherent diff that satisfies the prompt.
6. Verify the result before concluding.

## Plan-First Rule

- Complex tasks require plan-first behavior.
- A task is complex if it touches multiple files, defines policy, changes architecture, introduces new structure, or has non-trivial verification requirements.
- A plan should identify objective, scope, dependencies, verification intent, and likely blockers.
- Do not start broad edits until that plan exists.

## Naming And Coverage Law

- Directory names must be based on compatibility technology or host contract, not version ranges, date spans, or vague eras.
- Exact support coverage belongs in metadata/manifests, inventory records, and support matrices.
- Do not encode exact version support into architectural source directory names.
- Do not rename established compatibility-technology directories merely because supported versions change.

## Support And Capability Law

- Support must be expressed through support tiers and capability levels, as defined in `governance/support-policy.md` and `governance/capability-levels.md`.
- Use support tiers `T0` through `T5` when describing maintenance posture.
- Use capability levels `L0` through `L4` when describing integration depth.
- Different hosts may top out at different capability levels.
- Do not imply uniform parity across all host families.
- Do not fabricate compatibility claims, support claims, or parity claims that have not been verified and recorded.

## Scope Control

- Keep diffs scoped to the task at hand.
- Avoid editing unrelated files.
- Do not silently expand scope because a broader change seems useful.
- If a cross-cutting fix is necessary for coherence, keep it minimal and record the reason in `IMPLEMENT.md`.
- Preserve existing user changes and fix forward.

## Verification Law

- No substantial task is complete until verification has been run.
- Verification should be proportionate to the change and explicit about what was checked.
- If runtime verification is not possible, perform the strongest honest structural verification available and record the gap.
- Never describe unrun work as verified.

## Planning And Execution Records

- `PLANS.md` is the working plan index for substantial tasks and multi-step efforts.
- `IMPLEMENT.md` is the engineering execution log for work that changed repository state.
- `DOCUMENTATION.md` is the root documentation index and maintenance guide.
- `.aide/profile.yaml` and related `.aide/` catalogs are the repo Profile/Contract source of truth; `AGENTS.md` points to that contract but does not replace it.
- `.aide/queue/` is the filesystem queue and canonical routing surface for non-trivial self-hosting work.
- ExecPlans under queue task directories are the unit of long-running autonomous work.
- When a substantial task is completed, update the relevant planning, execution, and documentation files in the same change set.

## When To Create Or Update Planning Documents

- Create or update `PLANS.md` when work spans multiple files, multiple milestones, dependencies, or blockers.
- Create or update `IMPLEMENT.md` when code, policy, or structure changes are landed.
- Create or update `DOCUMENTATION.md` when repository law, layout, or authoritative docs change.
- If a task is too small to justify a new plan entry, that should be an explicit judgment rather than an omission.

## Blockers And Deferrals

- State unresolved blockers explicitly.
- State deliberate deferrals explicitly.
- Distinguish between blocked, deferred, and completed work.
- Do not hide missing verification, missing compatibility evidence, or external constraints.

## Prohibited Behavior

- Do not fabricate compatibility, support, release readiness, or capability claims.
- Do not use vague supported or unsupported labels where the support-tier and capability-level model is required.
- Do not silently broaden product scope.
- Do not edit unrelated files to satisfy stylistic preference.
- Do not replace precise policy with speculative roadmap language.

## Commit Discipline

- Create at least one commit after each completed queued prompt when Git is available.
- Use detailed commit messages that identify prompt id, scope, key changes, verification status, and blocked or deferred notes.
- Prefer fix-forward history over rewriting or squashing away useful forensic context.
- If Git is not on `PATH`, use `C:\Program Files\Git\cmd\git.exe`.

## Expected Final Report After Each Task

1. A short summary of what changed.
2. A file list.
3. The verification commands that were run and whether they passed.
4. Any unresolved issues or deliberate deferrals.

<!-- AIDE-GENERATED:BEGIN section=aide-self-hosting-summary generator=aide-harness-generated-artifacts-v0 version=q05.generated-artifacts.v0 mode=managed-section sources=.aide/profile.yaml,.aide/toolchain.lock,.aide/commands/catalog.yaml,.aide/queue/policy.yaml,.aide/queue/index.yaml,docs/reference/source-of-truth.md,docs/reference/harness-v0.md,docs/reference/generated-artifacts-v0.md fingerprint=sha256:3c125754e96bd2007d2ffd5874811c4c8b837bf146207ea1a01a7f8d275ee481 manual=outside-only -->
## Generated AIDE Contract Summary

- Canonical Profile/Contract source: `.aide/`.
- Canonical long-running work queue: `.aide/queue/`.
- Generated downstream artifacts are compiled or managed outputs, not canonical truth.
- Non-trivial work must route through AIDE intake or the filesystem queue and produce evidence.
- Current accepted foundation includes Contract/Profile v0, Harness v0, Compatibility baseline records, the AIDE-side Dominium Bridge baseline, and report-first self-hosting automation.
- Runtime, full Hosts, Gateway, providers, Commander, Mobile, app surfaces, and real Dominium Bridge implementation remain deferred until queue items authorize them.
<!-- AIDE-GENERATED:END section=aide-self-hosting-summary -->

<!-- AIDE-GENERATED:BEGIN section=token-survival-core generator=aide-lite version=q16.outcome-controller.v0 mode=managed-section fingerprint=sha256:5f948815694b32f35a58a66a6b25a446d9d5d4b75840dd7082d27cd7acaaa4f7 manual=outside-only -->
## Q16 Token, Context, Verifier, Review, Ledger, Eval, And Outcome Guidance

- Use `.aide/context/latest-task-packet.md` when present instead of pasting long chat history.
- Use `.aide/context/latest-context-packet.md`, repo-map refs, test-map refs, compact project memory, and evidence packets before broad context dumps.
- Do not paste full prior transcripts, whole repo dumps, repeated roadmap dumps, secrets, provider keys, local caches, or raw prompt logs.
- Emit deltas and compact final reports with status, changed files, validation, evidence, risks, and next step.
- Generate `.aide/context/latest-review-packet.md` with `review-pack` before premium-model review.
- Run `ledger scan`, `ledger report`, and `ledger compare` for token-ledger work, and do not store raw prompts or raw responses in committed ledger records.
- Run `eval list`, `eval run`, and `eval report` for token-saving workflow changes once Q15 golden-task behavior is available.
- Treat token reduction as invalid if golden tasks fail.
- Run `outcome report` and `optimize suggest` for advisory recommendations once Q16 controller behavior is available.
- Do not implement controller recommendations automatically; use a future queue item or explicit human approval.
- Review compact review packets and verifier output only by default; ask for more context only when the packet is insufficient.
- Run `py -3 .aide/scripts/aide_lite.py doctor`, `validate`, `snapshot`, `index`, `context`, `pack`, `estimate`, `verify`, `review-pack`, `ledger`, `eval`, `outcome`, `optimize`, `adapt`, and `selftest` for token/context/verifier/review/ledger/eval/outcome work.
- Prefer exact refs such as `path#Lstart-Lend`; do not inline whole files by default.
- Treat token savings as invalid when validation, quality evidence, provenance, or review gates are weakened.
- Commit coherent subdeliverables with verbose bodies when queue work changes repo state.
<!-- AIDE-GENERATED:END section=token-survival-core -->
