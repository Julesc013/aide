# AIDE Evidence Review Prompt

Review only the provided review packet. Do not request full chat history unless the packet is insufficient to judge correctness.

## REVIEWER RULES

- Do not re-summarize the whole project.
- Do not reward scope creep.
- Do not approve missing validation as a pass.
- Do not request full repo context when file refs, evidence refs, or verifier output are enough.
- Ask for more context only when the packet is insufficient to decide safely.
- Treat verifier output as mechanical evidence, not as a substitute for judgment.

## INPUTS

- compact review packet
- task packet reference
- context packet reference
- verification report reference
- evidence packet references
- changed files summary
- validation summary
- token summary
- token ledger summary when available
- golden task summary when available
- outcome-controller recommendation summary when available
- route decision summary when available
- cache/local-state boundary summary when available
- gateway skeleton status summary when available
- risk summary
- non-goals and scope guard

## CHECKS

- Did the work stay inside scope?
- Did it meet acceptance criteria?
- Were tests or validations run and honestly reported?
- Did it reduce or preserve token efficiency?
- Did token ledger evidence avoid raw prompt/response storage and state only estimated savings?
- Did golden tasks pass when the work affects token-saving workflow quality gates?
- Are controller recommendations advisory only, evidence-sourced, and left for future queue-gated implementation?
- Is the Q17 route decision advisory only, and were hard floors preserved rather than demoted?
- Is `.aide.local/` ignored and untracked, and are cache-key reports metadata only?
- Did cache/local-state work avoid raw prompt, raw response, provider-response, semantic-answer, trace, or cache-blob storage in committed files?
- If Gateway skeleton work is in scope, does it remain local/report-only with health/status/route/summary endpoints and no provider/model forwarding?
- Did failed verifier or golden-task gates block or constrain routing where required?
- Did the work avoid using public benchmark claims as a substitute for repo-specific golden tasks?
- Did it avoid committing secrets, local state, raw prompts, provider keys, or caches?
- Did the verifier result support the claimed outcome?
- Are unresolved risks and deferrals explicit?
- Are required fixes concrete and bounded?

## DECISION VALUES

- `PASS`
- `PASS_WITH_NOTES`
- `REQUEST_CHANGES`
- `BLOCKED`

## OUTPUT

Return exactly these sections:

DECISION:
REASONS:
REQUIRED_FIXES:
OPTIONAL_NOTES:
NEXT_PHASE:
