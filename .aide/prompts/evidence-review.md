# AIDE Evidence Review Prompt

Review only the provided evidence packet. Do not request full chat history unless the evidence is insufficient to judge correctness.

## INPUTS

- task summary
- changed files
- diff summary
- tests run
- risks
- evidence packet
- verifier result and latest verification report when available

## CHECKS

- Did the work stay inside scope?
- Did it meet acceptance criteria?
- Were tests or validations run and honestly reported?
- Did it reduce or preserve token efficiency?
- Did it avoid committing secrets, local state, raw prompts, provider keys, or caches?
- Did the verifier result support the claimed outcome?
- Are unresolved risks and deferrals explicit?

## OUTPUT

Return exactly one decision:

- `PASS`
- `PASS_WITH_NOTES`
- `REQUEST_CHANGES`
- `BLOCKED`

Then provide compact sections:

- `REASONS`
- `REQUIRED_FIXES`
- `OPTIONAL_NOTES`
- `NEXT_PHASE`
