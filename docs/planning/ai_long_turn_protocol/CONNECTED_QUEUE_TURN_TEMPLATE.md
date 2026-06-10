# Connected Queue Turn Template

Use this when a prompt may finish one WorkUnit and continue to one directly
related follow-up. Do not use it to skip reviews, dependencies, or manual gates.

```text
# <TURN-ID>

## Mode

Connected queue turn.

## Goal

Advance the current queue chain through directly related docs, evidence,
validation, or repair work until a stop condition is reached.

## Chain Budget

- maximum task families: 1
- maximum completed WorkUnits: 2
- maximum commits: 3
- stop at any manual, review, dependency, or external evidence gate

## Start State

Fill from live repo state:

- branch:
- HEAD:
- worktree:
- current queue item:
- latest task packet:
- dirty files:
- known blockers:

## Continuation Rules

Continue only when:

- the next task is explicitly named by the completed WorkUnit or queue evidence
- dependencies are satisfied
- allowed paths are known
- validation is green or warnings are classified
- no review gate blocks continuation

Stop when:

- the next task requires review first
- scope moves to another task family
- external or manual evidence is required
- branch, publication, target-repo, provider/model, Gateway, or network action
  would be needed

## Final Output

Report each WorkUnit separately, grouped by commit and validation evidence.
```
