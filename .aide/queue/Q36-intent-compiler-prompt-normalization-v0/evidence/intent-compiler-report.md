# Q36 Intent Compiler Report

## Command Surface

Q36 extends `.aide/scripts/aide_lite.py` with:

- `intent`
- `intent compile`
- `intent compile --prompt "text"`
- `intent compile --file PATH`
- `intent validate`
- `intent examples`
- `intent status`

The implementation is deterministic and local-only. It uses Python standard
library behavior, repo-local policy files, queue state, latest task packet refs,
and local Git branch-state refs. It does not call providers, models, outbound
network services, GitHub APIs, Gateway forwarding, target repos, branch
mutation commands, or the compiled WorkUnit.

## Policies And Schemas

- `.aide/policies/intent.yaml` defines operating mode, source priority, input
  and output classes, task/risk/size classes, normalization rules, and non-goals.
- `.aide/policies/task-classes.yaml` defines deterministic phrase hints for
  audit, repair, docs, test, implementation, refactor, release, install,
  upgrade, rollback, git, github, adapter, context, evidence, and unknown.
- `.aide/policies/risk-classes.yaml` defines low, medium, high, destructive,
  security, governance, release, external_side_effect, and unknown risk hints.
- `.aide/policies/workunit-sizing.yaml` defines one_shot, two_shot,
  refactor_gate, live_test_gate, audit_only, split_required, and blocked rules.
- `.aide/policies/prompt-normalization.yaml` defines deterministic handling for
  vague, overbroad, unsafe, repeated, out-of-order, target-repo, product-claim,
  Git, release, install, and refactor prompts.
- `.aide/intake/intent-packet.schema.json` defines the intent packet shape.
- `.aide/intake/workunit-draft.schema.json` defines the WorkUnit draft shape.

## Generated Latest Artifacts

The final generated sample prompt is:

`Plan Q37 Repo Intelligence Index v0 from the current AIDE repository state`

Generated artifacts:

- `.aide/intake/latest-intent-packet.json`
- `.aide/intake/latest-intent-packet.md`
- `.aide/intake/latest-workunit-draft.json`
- `.aide/intake/latest-workunit-draft.md`

Latest classification:

- `task_class`: `audit`
- `risk_class`: `low`
- `sizing_class`: `audit_only`
- `safe_to_execute`: `true`
- `requires_split`: `false`
- `blocked`: `false`
- `next_action`: draft the smallest safe WorkUnit after repo-state preflight

The packet stores a SHA-256 raw prompt hash and bounded excerpt. It does not
store `raw_prompt_body`, `raw_response_body`, long prompt logs, secrets, or
provider credentials.

## Example Classifications

- `next`: context / low / audit_only; inspect latest queue state and do not invent product work.
- `fix everything`: repair / high / split_required; identify smallest failing validation.
- `clean up the repo`: refactor / high / split_required; inventory/classify before moves.
- `delete old XStack stuff`: refactor / destructive / blocked; reject direct deletion.
- `merge dev to main`: git / release / blocked; require branch plan, validation, review, and promotion evidence.
- `publish a release`: release / release / blocked; require release gates, tags/assets approval, and validation.
- `install AIDE into Dominium`: install / external_side_effect / two_shot; require target-local preflight and preservation.
- `make it production ready`: audit / release / split_required; suggest readiness audit.
- `repair failing test`: repair / medium / one_shot; require targeted failing test validation.
- `move all roots into clean layout`: refactor / destructive / split_required; root inventory/root recycling first.
