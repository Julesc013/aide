# Prompt Quality Checklist

Use this before launching a long turn.

## Required

- stable task or turn id
- current repo root
- objective
- allowed paths
- non-goals
- dependencies
- validation ladder
- evidence location
- stop conditions
- final report format
- turn budget

## State To Fill From Repo

- branch
- HEAD
- worktree state
- current queue item
- latest task packet
- review gates
- known blockers

## Reject Or Split When

- the prompt asks for multiple unrelated task families
- the prompt mixes docs/control work with runtime behavior
- branch or publication actions are bundled with implementation
- target-repo or external discovery work is bundled with local docs/code work
- missing evidence would require guessing

## Good Prompt Shape

The prompt should tell the agent where to stop as clearly as where to work.
