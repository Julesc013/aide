# Gate Status Table

Fill this table at the start and end of long turns when the gate is relevant.
Use `not_applicable` when a gate is outside the task.

| Gate | Start | End | Evidence |
| --- | --- | --- | --- |
| queue authority |  |  |  |
| allowed paths |  |  |  |
| dependency status |  |  |  |
| worktree cleanliness |  |  |  |
| review gate |  |  |  |
| branch-sensitive action |  |  |  |
| publication-sensitive action |  |  |  |
| target-repo mutation |  |  |  |
| provider/model/Gateway/network |  |  |  |
| external discovery |  |  |  |
| manual evidence |  |  |  |
| validation |  |  |  |
| commit policy |  |  |  |

## Status Vocabulary

- `pass`
- `pass_with_warnings`
- `blocked`
- `deferred`
- `not_applicable`
- `not_checked`

Do not use `pass` for a gate that was not checked.
