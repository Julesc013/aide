# Q29 Prompt Summary

Implement Merge / Land / Promote Helper v0 in the AIDE repository.

## Core Objective

Add safe local Git helper commands for:

- syncing local branch state safely;
- landing task branches into the configured integration branch, usually `dev`;
- promoting integration to canonical, usually `dev -> main`, through gates;
- planning branch pruning using ancestor containment;
- keeping live AIDE repository operations dry-run/report-only by default;
- testing all mutating helper behavior only in temporary fixture repositories.

## Required Commands

- `py -3 .aide/scripts/aide_lite.py git plan`
- `py -3 .aide/scripts/aide_lite.py git sync --dry-run`
- `py -3 .aide/scripts/aide_lite.py git land --dry-run --target dev`
- `py -3 .aide/scripts/aide_lite.py git promote --dry-run --from dev --to main`
- `py -3 .aide/scripts/aide_lite.py git prune --dry-run`

## Safety Requirements

- No live AIDE branch creation, deletion, merge, push, prune, or promotion in
  Q29.
- No remote push in Q29.
- No force push support.
- Unknown, dirty, protected, or missing-policy states block mutation.
- Pruning requires ancestor containment.
- Protected roles are never pruned.
- Helper plan output must be JSON and Markdown and contain no secrets or raw
  prompt/response content.

## Deliverables

- Q29 queue packet and evidence.
- `.aide/git/helper-policy.yaml`
- `.aide/git/helper-commands.md`
- `.aide/git/latest-helper-plan.json`
- `.aide/git/latest-helper-plan.md`
- AIDE Lite helper commands and tests.
- Q29 golden tasks.
- Documentation updates.
- Export pack sync.

## Review Gate

Stop at `needs_review`.
