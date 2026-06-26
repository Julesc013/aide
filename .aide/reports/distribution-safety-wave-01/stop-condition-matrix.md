# Stop-Condition Matrix

| Stop Condition | Required Behavior |
| --- | --- |
| worktree has unrelated dirty changes | classify and preserve; do not sweep into task |
| predecessor missing or failed | stop and route to unblocker or repair |
| check finds material defects | stop and route to repair |
| evidence missing | stop and route to evidence repair |
| validation fails | stop and record failure or repair route |
| task reaches `needs_review` | stop current task; do not proceed downstream inside the same task |
| apply authority needed | stop; create explicit apply-authority task if appropriate |
| release or publish authority needed | stop; create explicit release-authority task if appropriate |
| target mutation requested | stop unless the active queue item explicitly authorizes it |
| provider/model/network call requested | stop unless the active queue item explicitly authorizes it |
| generated churn outside scope | restore or record as blocker; do not hide it in the commit |
| secret-like or local absolute path leak found | stop and repair generated evidence before commit |
