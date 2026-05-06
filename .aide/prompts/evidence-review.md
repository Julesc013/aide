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
- risk summary
- non-goals and scope guard

## CHECKS

- Did the work stay inside scope?
- Did it meet acceptance criteria?
- Were tests or validations run and honestly reported?
- Did it reduce or preserve token efficiency?
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
