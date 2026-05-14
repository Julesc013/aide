# QFIX-05 Prompt

The operator asked to go through previous prompts and tasks, fix warnings,
partials, errors, and blockers, and make the repository production-ready.

Repository law requires this broad request to be narrowed into a bounded queue
item. QFIX-05 therefore performs a release-readiness warning reconciliation:
inventory current queue and validation state, fix mechanical generated-artifact
drift if safe, and record remaining review-gated blockers honestly.

This prompt does not authorize release publication, Git tag creation, branch
mutation, provider/model/network calls, target repository mutation, or changing
review-gated tasks to `passed` without review evidence.
